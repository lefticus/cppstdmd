# Language support library <a id="language.support">[[language.support]]</a>

## General <a id="support.general">[[support.general]]</a>

This Clause describes the function signatures that are called
implicitly, and the types of objects generated implicitly, during the
execution of some C++programs. It also describes the headers that
declare these function signatures and define any related types.

The following subclauses describe common type definitions used
throughout the library, characteristics of the predefined types,
functions supporting start and termination of a C++program, support for
dynamic memory management, support for dynamic type identification,
support for exception processing, support for initializer lists, and
other runtime support, as summarized in Table 
[[tab:lang.sup.lib.summary]].

**Table: Language support library summary**

| Subclause              |                           | Header               |
| ---------------------- | ------------------------- | -------------------- |
| [[support.types]]      | Types                     | `<cstddef>`          |
|                        |                           | `<limits>`           |
| [[support.limits]]     | Implementation properties | `<climits>`          |
|                        |                           | `<cfloat>`           |
| [[cstdint]]            | Integer types             | `<cstdint>`          |
| [[support.start.term]] | Start and termination     | `<cstdlib>`          |
| [[support.dynamic]]    | Dynamic memory management | `<new>`              |
| [[support.rtti]]       | Type identification       | `<typeinfo>`         |
| [[support.exception]]  | Exception handling        | `<exception>`        |
| [[support.initlist]]   | Initializer lists         | `<initializer_list>` |
|                        |                           | `<csignal>`          |
|                        |                           | `<csetjmp>`          |
|                        |                           | `<cstdalign>`        |
| [[support.runtime]]    | Other runtime support     | `<cstdarg>`          |
|                        |                           | `<cstdbool>`         |
|                        |                           | `<cstdlib>`          |
|                        |                           | `<ctime>`            |


## Types <a id="support.types">[[support.types]]</a>

Table  [[tab:support.hdr.cstddef]] describes the header `<cstddef>`.

The contents are the same as the Standard C library header `<stddef.h>`,
with the following changes:

The macro `NULL` is an implementation-defined C++null pointer constant
in this International Standard ([[conv.ptr]]).[^1]

The macro `offsetof`(*type*, *member-designator*) accepts a restricted
set of *type* arguments in this International Standard. If *type* is not
a standard-layout class (Clause  [[class]]), the results are
undefined.[^2] The expression `offsetof`(*type*, *member-designator*) is
never type-dependent ([[temp.dep.expr]]) and it is value-dependent (
[[temp.dep.constexpr]]) if and only if *type* is dependent. The result
of applying the `offsetof` macro to a field that is a static data member
or a function member is undefined. No operation invoked by the
`offsetof` macro shall throw an exception and
`noexcept(offsetof(type, member-designator))` shall be `true`.

The type `ptrdiff_t` is an *implementation-defined* signed integer type
that can hold the difference of two subscripts in an array object, as
described in  [[expr.add]].

The type `size_t` is an *implementation-defined* unsigned integer type
that is large enough to contain the size in bytes of any object.

It is recommended that implementations choose types for `ptrdiff_t` and
`size_t` whose integer conversion ranks ([[conv.rank]]) are no greater
than that of `signed long int` unless a larger size is necessary to
contain all the possible values.

The type `max_align_t` is a POD type whose alignment requirement is at
least as great as that of every scalar type, and whose alignment
requirement is supported in every context.

`nullptr_t` is defined as follows:

``` cpp
namespace std {
  typedef decltype(nullptr) nullptr_t;
}
```

The type for which `nullptr_t` is a synonym has the characteristics
described in  [[basic.fundamental]] and  [[conv.ptr]]. Although
`nullptr`’s address cannot be taken, the address of another `nullptr_t`
object that is an lvalue can be taken.

Alignment ([[basic.align]]), Sizeof ([[expr.sizeof]]), Additive
operators ([[expr.add]]), Free store ([[class.free]]), and ISO
C 7.1.6.

## Implementation properties <a id="support.limits">[[support.limits]]</a>

### In general <a id="support.limits.general">[[support.limits.general]]</a>

The headers `<limits>` ([[limits]]), `<climits>`, and `<cfloat>` (
[[c.limits]]) supply characteristics of implementation-dependent
arithmetic types ([[basic.fundamental]]).

### Numeric limits <a id="limits">[[limits]]</a>

#### Class template `numeric_limits` <a id="limits.numeric">[[limits.numeric]]</a>

The `numeric_limits` class template provides a C++program with
information about various properties of the implementation’s
representation of the arithmetic types.

Specializations shall be provided for each arithmetic type, both
floating point and integer, including `bool`. The member
`is_specialized` shall be `true` for all such specializations of
`numeric_limits`.

For all members declared `static` `constexpr` in the `numeric_limits`
template, specializations shall define these values in such a way that
they are usable as constant expressions.

Non-arithmetic standard types, such as `complex<T>` ([[complex]]),
shall not have specializations.

#### Header `<limits>` synopsis <a id="limits.syn">[[limits.syn]]</a>

``` cpp
namespace std {
  template<class T> class numeric_limits;
  enum float_round_style;
  enum float_denorm_style;

  template<> class numeric_limits<bool>;

  template<> class numeric_limits<char>;
  template<> class numeric_limits<signed char>;
  template<> class numeric_limits<unsigned char>;
  template<> class numeric_limits<char16_t>;
  template<> class numeric_limits<char32_t>;
  template<> class numeric_limits<wchar_t>;

  template<> class numeric_limits<short>;
  template<> class numeric_limits<int>;
  template<> class numeric_limits<long>;
  template<> class numeric_limits<long long>;
  template<> class numeric_limits<unsigned short>;
  template<> class numeric_limits<unsigned int>;
  template<> class numeric_limits<unsigned long>;
  template<> class numeric_limits<unsigned long long>;

  template<> class numeric_limits<float>;
  template<> class numeric_limits<double>;
  template<> class numeric_limits<long double>;
}
```

#### Class template `numeric_limits` <a id="numeric.limits">[[numeric.limits]]</a>

``` cpp
namespace std {
  template<class T> class numeric_limits {
  public:
    static constexpr bool is_specialized = false;
    static constexpr T min() noexcept { return T(); }
    static constexpr T max() noexcept { return T(); }
    static constexpr T lowest() noexcept { return T(); }

    static constexpr int  digits = 0;
    static constexpr int  digits10 = 0;
    static constexpr int  max_digits10 = 0;
    static constexpr bool is_signed = false;
    static constexpr bool is_integer = false;
    static constexpr bool is_exact = false;
    static constexpr int  radix = 0;
    static constexpr T epsilon() noexcept { return T(); }
    static constexpr T round_error() noexcept { return T(); }

    static constexpr int  min_exponent = 0;
    static constexpr int  min_exponent10 = 0;
    static constexpr int  max_exponent = 0;
    static constexpr int  max_exponent10 = 0;

    static constexpr bool has_infinity = false;
    static constexpr bool has_quiet_NaN = false;
    static constexpr bool has_signaling_NaN = false;
    static constexpr float_denorm_style has_denorm = denorm_absent;
    static constexpr bool has_denorm_loss = false;
    static constexpr T infinity() noexcept { return T(); }
    static constexpr T quiet_NaN() noexcept { return T(); }
    static constexpr T signaling_NaN() noexcept { return T(); }
    static constexpr T denorm_min() noexcept { return T(); }

    static constexpr bool is_iec559 = false;
    static constexpr bool is_bounded = false;
    static constexpr bool is_modulo = false;

    static constexpr bool traps = false;
    static constexpr bool tinyness_before = false;
    static constexpr float_round_style round_style = round_toward_zero;
  };

  template<class T> class numeric_limits<const T>;
  template<class T> class numeric_limits<volatile T>;
  template<class T> class numeric_limits<const volatile T>;
}
```

The default `numeric_limits<T>` template shall have all members, but
with 0 or `false` values.

The value of each member of a specialization of `numeric_limits` on a
*cv*-qualified type `cv T` shall be equal to the value of the
corresponding member of the specialization on the unqualified type `T`.

#### `numeric_limits` members <a id="numeric.limits.members">[[numeric.limits.members]]</a>

``` cpp
static constexpr T min() noexcept;
```

Minimum finite value.[^3]

For floating types with denormalization, returns the minimum positive
normalized value.

Meaningful for all specializations in which `is_bounded != false`, or
`is_bounded == false && is_signed == false`.

``` cpp
static constexpr T max() noexcept;
```

Maximum finite value.[^4]

Meaningful for all specializations in which `is_bounded != false`.

``` cpp
static constexpr T lowest() noexcept;
```

A finite value `x` such that there is no other finite value `y` where
`y < x`.[^5]

Meaningful for all specializations in which `is_bounded != false`.

``` cpp
static constexpr int digits;
```

Number of `radix` digits that can be represented without change.

For integer types, the number of non-sign bits in the representation.

For floating point types, the number of `radix` digits in the
mantissa.[^6]

``` cpp
static constexpr int digits10;
```

Number of base 10 digits that can be represented without change.[^7]

Meaningful for all specializations in which `is_bounded != false`.

``` cpp
static constexpr int max_digits10;
```

Number of base 10 digits required to ensure that values which differ are
always differentiated.

Meaningful for all floating point types.

``` cpp
static constexpr bool is_signed;
```

True if the type is signed.

Meaningful for all specializations.

``` cpp
static constexpr bool is_integer;
```

True if the type is integer.

Meaningful for all specializations.

``` cpp
static constexpr bool is_exact;
```

True if the type uses an exact representation. All integer types are
exact, but not all exact types are integer. For example, rational and
fixed-exponent representations are exact but not integer.

Meaningful for all specializations.

``` cpp
static constexpr int radix;
```

For floating types, specifies the base or radix of the exponent
representation (often 2).[^8]

For integer types, specifies the base of the representation.[^9]

Meaningful for all specializations.

``` cpp
static constexpr T epsilon() noexcept;
```

Machine epsilon: the difference between 1 and the least value greater
than 1 that is representable.[^10]

Meaningful for all floating point types.

``` cpp
static constexpr T round_error() noexcept;
```

Measure of the maximum rounding error.[^11]

``` cpp
static constexpr int  min_exponent;
```

Minimum negative integer such that `radix` raised to the power of one
less than that integer is a normalized floating point number.[^12]

Meaningful for all floating point types.

``` cpp
static constexpr int  min_exponent10;
```

Minimum negative integer such that 10 raised to that power is in the
range of normalized floating point numbers.[^13]

Meaningful for all floating point types.

``` cpp
static constexpr int  max_exponent;
```

Maximum positive integer such that `radix` raised to the power one less
than that integer is a representable finite floating point number.[^14]

Meaningful for all floating point types.

``` cpp
static constexpr int  max_exponent10;
```

Maximum positive integer such that 10 raised to that power is in the
range of representable finite floating point numbers.[^15]

Meaningful for all floating point types.

``` cpp
static constexpr bool has_infinity;
```

True if the type has a representation for positive infinity.

Meaningful for all floating point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr bool has_quiet_NaN;
```

True if the type has a representation for a quiet (non-signaling) “Not a
Number.”[^16]

Meaningful for all floating point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr bool has_signaling_NaN;
```

True if the type has a representation for a signaling “Not a
Number.”[^17]

Meaningful for all floating point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr float_denorm_style has_denorm;
```

`denorm_present` if the type allows denormalized values (variable number
of exponent bits)[^18], `denorm_absent` if the type does not allow
denormalized values, and `denorm_indeterminate` if it is indeterminate
at compile time whether the type allows denormalized values.

Meaningful for all floating point types.

``` cpp
static constexpr bool has_denorm_loss;
```

True if loss of accuracy is detected as a denormalization loss, rather
than as an inexact result.[^19]

``` cpp
static constexpr T infinity() noexcept;
```

Representation of positive infinity, if available.[^20]

Meaningful for all specializations for which `has_infinity != false`.
Required in specializations for which `is_iec559 != false`.

``` cpp
static constexpr T quiet_NaN() noexcept;
```

Representation of a quiet “Not a Number,” if available.[^21]

Meaningful for all specializations for which `has_quiet_NaN != false`.
Required in specializations for which `is_iec559 != false`.

``` cpp
static constexpr T signaling_NaN() noexcept;
```

Representation of a signaling “Not a Number,” if available.[^22]

Meaningful for all specializations for which
`has_signaling_NaN != false`. Required in specializations for which
`is_iec559 != false`.

``` cpp
static constexpr T denorm_min() noexcept;
```

Minimum positive denormalized value.[^23]

Meaningful for all floating point types.

In specializations for which `has_denorm == false`, returns the minimum
positive normalized value.

``` cpp
static constexpr bool is_iec559;
```

True if and only if the type adheres to IEC 559 standard.[^24]

Meaningful for all floating point types.

``` cpp
static constexpr bool is_bounded;
```

True if the set of values representable by the type is finite.[^25] All
fundamental types ([[basic.fundamental]]) are bounded. This member
would be false for arbitrary precision types.

Meaningful for all specializations.

``` cpp
static constexpr bool is_modulo;
```

True if the type is modulo.[^26] A type is modulo if, for any operation
involving `+`, `-`, or `*` on values of that type whose result would
fall outside the range \[`min()`, `max()`\], the value returned differs
from the true value by an integer multiple of `max() - min() + 1`.

On most machines, this is `false` for floating types, `true` for
unsigned integers, and `true` for signed integers.

Meaningful for all specializations.

``` cpp
static constexpr bool traps;
```

`true` if, at program startup, there exists a value of the type that
would cause an arithmetic operation using that value to trap.[^27]

Meaningful for all specializations.

``` cpp
static constexpr bool tinyness_before;
```

`true` if tinyness is detected before rounding.[^28]

Meaningful for all floating point types.

``` cpp
static constexpr float_round_style round_style;
```

The rounding style for the type.[^29]

Meaningful for all floating point types. Specializations for integer
types shall return `round_toward_zero`.

#### Type `float_round_style` <a id="round.style">[[round.style]]</a>

``` cpp
namespace std {
  enum float_round_style {
    round_indeterminate       = -1,
    round_toward_zero         =  0,
    round_to_nearest          =  1,
    round_toward_infinity     =  2,
    round_toward_neg_infinity =  3
  };
}
```

The rounding mode for floating point arithmetic is characterized by the
values:

- `round_indeterminate` if the rounding style is indeterminable
- `round_toward_zero` if the rounding style is toward zero
- `round_to_nearest` if the rounding style is to the nearest
  representable value
- `round_toward_infinity` if the rounding style is toward infinity
- `round_toward_neg_infinity` if the rounding style is toward negative
  infinity

#### Type `float_denorm_style` <a id="denorm.style">[[denorm.style]]</a>

``` cpp
namespace std {
  enum float_denorm_style {
    denorm_indeterminate = -1,
    denorm_absent = 0,
    denorm_present = 1
  };
}
```

The presence or absence of denormalization (variable number of exponent
bits) is characterized by the values:

- `denorm_indeterminate` if it cannot be determined whether or not the
  type allows denormalized values
- `denorm_absent` if the type does not allow denormalized values
- `denorm_present` if the type does allow denormalized values

#### `numeric_limits` specializations <a id="numeric.special">[[numeric.special]]</a>

All members shall be provided for all specializations. However, many
values are only required to be meaningful under certain conditions (for
example, `epsilon()` is only meaningful if `is_integer` is `false`). Any
value that is not “meaningful” shall be set to 0 or `false`.

``` cpp
namespace std {
  template<> class numeric_limits<float> {
  public:
    static constexpr bool is_specialized = true;

    inline static constexpr float min() noexcept { return 1.17549435E-38F; }
    inline static constexpr float max() noexcept { return 3.40282347E+38F; }
    inline static constexpr float lowest() noexcept { return -3.40282347E+38F; }

    static constexpr int digits   = 24;
    static constexpr int digits10 =  6;
    static constexpr int max_digits10 =  9;

    static constexpr bool is_signed  = true;
    static constexpr bool is_integer = false;
    static constexpr bool is_exact   = false;

    static constexpr int radix = 2;
    inline static constexpr float epsilon() noexcept     { return 1.19209290E-07F; }
    inline static constexpr float round_error() noexcept { return 0.5F; }

    static constexpr int min_exponent   = -125;
    static constexpr int min_exponent10 = - 37;
    static constexpr int max_exponent   = +128;
    static constexpr int max_exponent10 = + 38;

    static constexpr bool has_infinity             = true;
    static constexpr bool has_quiet_NaN            = true;
    static constexpr bool has_signaling_NaN        = true;
    static constexpr float_denorm_style has_denorm = denorm_absent;
    static constexpr bool has_denorm_loss          = false;

    inline static constexpr float infinity()      noexcept { return value; }
    inline static constexpr float quiet_NaN()     noexcept { return value; }
    inline static constexpr float signaling_NaN() noexcept { return value; }
    inline static constexpr float denorm_min()    noexcept { return min(); }

    static constexpr bool is_iec559  = true;
    static constexpr bool is_bounded = true;
    static constexpr bool is_modulo  = false;
    static constexpr bool traps      = true;
    static constexpr bool tinyness_before = true;

    static constexpr float_round_style round_style = round_to_nearest;
  };
}
```

The specialization for `bool` shall be provided as follows:

``` cpp
namespace std {
   template<> class numeric_limits<bool> {
   public:
     static constexpr bool is_specialized = true;
     static constexpr bool min() noexcept { return false; }
     static constexpr bool max() noexcept { return true; }
     static constexpr bool lowest() noexcept { return false; }

     static constexpr int  digits = 1;
     static constexpr int  digits10 = 0;
     static constexpr int  max_digits10 = 0;

     static constexpr bool is_signed = false;
     static constexpr bool is_integer = true;
     static constexpr bool is_exact = true;
     static constexpr int  radix = 2;
     static constexpr bool epsilon() noexcept { return 0; }
     static constexpr bool round_error() noexcept { return 0; }

     static constexpr int  min_exponent = 0;
     static constexpr int  min_exponent10 = 0;
     static constexpr int  max_exponent = 0;
     static constexpr int  max_exponent10 = 0;

     static constexpr bool has_infinity = false;
     static constexpr bool has_quiet_NaN = false;
     static constexpr bool has_signaling_NaN = false;
     static constexpr float_denorm_style has_denorm = denorm_absent;
     static constexpr bool has_denorm_loss = false;
     static constexpr bool infinity() noexcept { return 0; }
     static constexpr bool quiet_NaN() noexcept { return 0; }
     static constexpr bool signaling_NaN() noexcept { return 0; }
     static constexpr bool denorm_min() noexcept { return 0; }

     static constexpr bool is_iec559 = false;
     static constexpr bool is_bounded = true;
     static constexpr bool is_modulo = false;

     static constexpr bool traps = false;
     static constexpr bool tinyness_before = false;
     static constexpr float_round_style round_style = round_toward_zero;
   };
}
```

### C library <a id="c.limits">[[c.limits]]</a>

Table  [[tab:support.hdr.climits]] describes the header `<climits>`.

The contents are the same as the Standard C library header `<limits.h>`.
The types of the constants defined by macros in `<climits>` are not
required to match the types to which the macros refer.

Table  [[tab:support.hdr.cfloat]] describes the header `<cfloat>`.

The contents are the same as the Standard C library header `<float.h>`.

ISO C 7.1.5, 5.2.4.2.2, 5.2.4.2.1.

## Integer types <a id="cstdint">[[cstdint]]</a>

### Header `<cstdint>` synopsis <a id="cstdint.syn">[[cstdint.syn]]</a>

``` cpp
namespace std {
  typedef signed integer type int8_t;   // optional
  typedef signed integer type int16_t;  // optional
  typedef signed integer type int32_t;  // optional
  typedef signed integer type int64_t;  // optional

  typedef signed integer type int_fast8_t;
  typedef signed integer type int_fast16_t;
  typedef signed integer type int_fast32_t;
  typedef signed integer type int_fast64_t;

  typedef signed integer type int_least8_t;
  typedef signed integer type int_least16_t;
  typedef signed integer type int_least32_t;
  typedef signed integer type int_least64_t;

  typedef signed integer type intmax_t;
  typedef signed integer type intptr_t;         // optional

  typedef unsigned integer type uint8_t;        // optional
  typedef unsigned integer type uint16_t;       // optional
  typedef unsigned integer type uint32_t;       // optional
  typedef unsigned integer type uint64_t;       // optional

  typedef unsigned integer type uint_fast8_t;
  typedef unsigned integer type uint_fast16_t;
  typedef unsigned integer type uint_fast32_t;
  typedef unsigned integer type uint_fast64_t;

  typedef unsigned integer type uint_least8_t;
  typedef unsigned integer type uint_least16_t;
  typedef unsigned integer type uint_least32_t;
  typedef unsigned integer type uint_least64_t;

  typedef unsigned integer type uintmax_t;
  typedef unsigned integer type uintptr_t;      // optional
} // namespace std
```

The header also defines numerous macros of the form:

``` cpp
INT_[FAST LEAST]{8 16 32 64}_MIN
  [U]INT_[FAST LEAST]{8 16 32 64}_MAX
  INT{MAX PTR}_MIN
  [U]INT{MAX PTR}_MAX
  {PTRDIFF SIG_ATOMIC WCHAR WINT}{_MAX _MIN}
  SIZE_MAX
```

plus function macros of the form:

``` cpp
[U]INT{8 16 32 64 MAX}_C
```

The header defines all functions, types, and macros the same as 7.18 in
the C standard. The macros defined by `<cstdint>` are provided
unconditionally. In particular, the symbols `__STDC_LIMIT_MACROS` and
`__STDC_CONSTANT_MACROS` (mentioned in footnotes 219, 220, and 222 in
the C standard) play no role in C++.

## Start and termination <a id="support.start.term">[[support.start.term]]</a>

Table  [[tab:support.hdr.cstdlib]] describes some of the contents of the
header `<cstdlib>`.

The contents are the same as the Standard C library header `<stdlib.h>`,
with the following changes:

``` cpp
[[noreturn]] void _Exit(int status) noexcept;
```

The function `_Exit(int status)` has additional behavior in this
International Standard:

- The program is terminated without executing destructors for objects of
  automatic, thread, or static storage duration and without calling
  functions passed to `atexit()` ([[basic.start.term]]).

``` cpp
[[noreturn]] void abort(void) noexcept;
```

The function `abort()` has additional behavior in this International
Standard:

- The program is terminated without executing destructors for objects of
  automatic, thread, or static storage duration and without calling
  functions passed to `atexit()` ([[basic.start.term]]).

``` cpp
extern "C" int atexit(void (*f)(void)) noexcept;
extern "C++" int atexit(void (*f)(void)) noexcept;
```

*Effects:* The `atexit()` functions register the function pointed to by
`f` to be called without arguments at normal program termination. It is
unspecified whether a call to `atexit()` that does not happen
before ([[intro.multithread]]) a call to `exit()` will succeed. The
`atexit()` functions do not introduce a data
race ([[res.on.data.races]]).

*Implementation limits:* The implementation shall support the
registration of at least 32 functions.

*Returns:* The `atexit()` function returns zero if the registration
succeeds, non-zero if it fails.

``` cpp
[[noreturn]] void exit(int status)
```

The function `exit()` has additional behavior in this International
Standard:

- First, objects with thread storage duration and associated with the
  current thread are destroyed. Next, objects with static storage
  duration are destroyed and functions registered by calling `atexit`
  are called.[^30] See  [[basic.start.term]] for the order of
  destructions and calls. (Automatic objects are not destroyed as a
  result of calling `exit()`.)[^31] If control leaves a registered
  function called by `exit` because the function does not provide a
  handler for a thrown exception, `std::terminate()` shall be
  called ([[except.terminate]]).
- Next, all open C streams (as mediated by the function signatures
  declared in `<cstdio>`) with unwritten buffered data are flushed, all
  open C streams are closed, and all files created by calling
  `tmpfile()` are removed.
- Finally, control is returned to the host environment. If `status` is
  zero or `EXIT_SUCCESS`, an *implementation-defined* form of the status
  *successful termination* is returned. If `status` is `EXIT_FAILURE`,
  an *implementation-defined* form of the status *unsuccessful
  termination* is returned. Otherwise the status returned is
  *implementation-defined*. [^32]

``` cpp
extern "C" int at_quick_exit(void (*f)(void)) noexcept;
extern "C++" int at_quick_exit(void (*f)(void)) noexcept;
```

*Effects:* The `at_quick_exit()` functions register the function pointed
to by `f` to be called without arguments when `quick_exit` is called. It
is unspecified whether a call to `at_quick_exit()` that does not happen
before ([[intro.multithread]]) all calls to `quick_exit` will succeed.
The `at_quick_exit()` functions do not introduce a data
race ([[res.on.data.races]]). The order of registration may be
indeterminate if `at_quick_exit` was called from more than one thread.
The `at_quick_exit` registrations are distinct from the `atexit`
registrations, and applications may need to call both registration
functions with the same argument.

*Implementation limits:* The implementation shall support the
registration of at least 32 functions.

*Returns:* Zero if the registration succeeds, non-zero if it fails.

``` cpp
[[noreturn]] void quick_exit(int status) noexcept;
```

*Effects:* Functions registered by calls to `at_quick_exit` are called
in the reverse order of their registration, except that a function shall
be called after any previously registered functions that had already
been called at the time it was registered. Objects shall not be
destroyed as a result of calling `quick_exit`. If control leaves a
registered function called by `quick_exit` because the function does not
provide a handler for a thrown exception, `std::terminate()` shall be
called.

`at_quick_exit` may call a registered function from a different thread
than the one that registered it, so registered functions should not rely
on the identity of objects with thread storage duration. After calling
registered functions, `quick_exit` shall call `_Exit(status)`. The
standard file buffers are not flushed. ISO C 7.20.4.4.

  [[basic.start]], [[basic.start.term]], ISO C 7.10.4.

## Dynamic memory management <a id="support.dynamic">[[support.dynamic]]</a>

The header `<new>` defines several functions that manage the allocation
of dynamic storage in a program. It also defines components for
reporting storage management errors.

``` cpp
namespace std {
  class bad_alloc;
  class bad_array_new_length;
  struct nothrow_t {};
  extern const nothrow_t nothrow;
  typedef void (*new_handler)();
  new_handler get_new_handler() noexcept;
  new_handler set_new_handler(new_handler new_p) noexcept;
}

void* operator new(std::size_t size);
void* operator new(std::size_t size, const std::nothrow_t&) noexcept;
void  operator delete(void* ptr) noexcept;
void  operator delete(void* ptr, const std::nothrow_t&) noexcept;
void* operator new[](std::size_t size);
void* operator new[](std::size_t size, const std::nothrow_t&) noexcept;
void  operator delete[](void* ptr) noexcept;
void  operator delete[](void* ptr, const std::nothrow_t&) noexcept;

void* operator new  (std::size_t size, void* ptr) noexcept;
void* operator new[](std::size_t size, void* ptr) noexcept;
void  operator delete  (void* ptr, void*) noexcept;
void  operator delete[](void* ptr, void*) noexcept;
```

  [[intro.memory]], [[basic.stc.dynamic]], [[expr.new]],
[[expr.delete]], [[class.free]], [[memory]].

### Storage allocation and deallocation <a id="new.delete">[[new.delete]]</a>

Except where otherwise specified, the provisions of (
[[basic.stc.dynamic]]) apply to the library versions of `operator new`
and `operator
delete`.

#### Single-object forms <a id="new.delete.single">[[new.delete.single]]</a>

``` cpp
void* operator new(std::size_t size);
```

*Effects:* The *allocation function* ([[basic.stc.dynamic.allocation]])
called by a *new-expression* ([[expr.new]]) to allocate `size` bytes of
storage suitably aligned to represent any object of that size.

*Replaceable:* a C++program may define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage ([[basic.stc.dynamic]]), or else throw a `bad_alloc` exception.
This requirement is binding on a replacement version of this function.

*Default behavior:*

- Executes a loop: Within the loop, the function first attempts to
  allocate the requested storage. Whether the attempt involves a call to
  the Standard C library function `malloc` is unspecified.
- Returns a pointer to the allocated storage if the attempt is
  successful. Otherwise, if the current
  `new_handler` ([[get.new.handler]]) is a null pointer value, throws
  `bad_alloc`.
- Otherwise, the function calls the current `new_handler`
  function ([[new.handler]]). If the called function returns, the loop
  repeats.
- The loop terminates when an attempt to allocate the requested storage
  is successful or when a called `new_handler` function does not return.

``` cpp
void* operator new(std::size_t size, const std::nothrow_t&) noexcept;
```

*Effects:* Same as above, except that it is called by a placement
version of a *new-expression* when a C++program prefers a null pointer
result as an error indication, instead of a `bad_alloc` exception.

*Replaceable:* a C++program may define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage ([[basic.stc.dynamic]]), or else return a null pointer. This
nothrow version of `operator new` returns a pointer obtained as if
acquired from the (possibly replaced) ordinary version. This requirement
is binding on a replacement version of this function.

*Default behavior:* Calls `operator new(size)`. If the call returns
normally, returns the result of that call. Otherwise, returns a null
pointer.

``` cpp
T* p1 = new T;                  // throws bad_alloc if it fails
T* p2 = new(nothrow) T;         // returns 0 if it fails
```

``` cpp
void operator delete(void* ptr) noexcept;
```

*Effects:* The *deallocation
function* ([[basic.stc.dynamic.deallocation]]) called by a
*delete-expression* to render the value of `ptr` invalid.

*Replaceable:* a C++program may define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Requires:* *ptr* shall be a null pointer or its value shall be a value
returned by an earlier call to the (possibly replaced)
`operator new(std::size_t)` or
`operator new(std::size_t,const std::nothrow_t&)` which has not been
invalidated by an intervening call to `operator delete(void*)`.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Default behavior:* If `ptr` is null, does nothing. Otherwise, reclaims
the storage allocated by the earlier call to `operator new`.

*Remarks:* It is unspecified under what conditions part or all of such
reclaimed storage will be allocated by subsequent calls to
`operator new` or any of `calloc`, `malloc`, or `realloc`, declared in
`<cstdlib>`.

``` cpp
void operator delete(void* ptr, const std::nothrow_t&) noexcept;
```

*Effects:* The *deallocation
function* ([[basic.stc.dynamic.deallocation]]) called by the
implementation to render the value of `ptr` invalid when the constructor
invoked from a nothrow placement version of the *new-expression* throws
an exception.

*Replaceable:* a C++program may define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Default behavior:* calls `operator delete(ptr)`.

#### Array forms <a id="new.delete.array">[[new.delete.array]]</a>

``` cpp
void* operator new[](std::size_t size);
```

*Effects:* The *allocation function* ([[basic.stc.dynamic.allocation]])
called by the array form of a *new-expression* ([[expr.new]]) to
allocate `size` bytes of storage suitably aligned to represent any array
object of that size or smaller.[^33]

*Replaceable:* a C++program can define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Required behavior:* Same as for `operator new(std::size_t)`. This
requirement is binding on a replacement version of this function.

*Default behavior:* Returns `operator new(size)`.

``` cpp
void* operator new[](std::size_t size, const std::nothrow_t&) noexcept;
```

*Effects:* Same as above, except that it is called by a placement
version of a *new-expression* when a C++program prefers a null pointer
result as an error indication, instead of a `bad_alloc` exception.

*Replaceable:* a C++program can define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage ([[basic.stc.dynamic]]), or return a null pointer. This
requirement is binding on a replacement version of this function.

*Default behavior:* Calls `operator new[](size)`. If the call returns
normally, returns the result of that call. Otherwise, returns a null
pointer.

``` cpp
void operator delete[](void* ptr) noexcept;
```

*Effects:* The *deallocation
function* ([[basic.stc.dynamic.deallocation]]) called by the array form
of a *delete-expression* to render the value of `ptr` invalid.

*Replaceable:* a C++program can define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Requires:* *ptr* shall be a null pointer or its value shall be the
value returned by an earlier call to `operator new[](std::size_t)` or
`operator new[](std::size_t,const std::nothrow_t&)` which has not been
invalidated by an intervening call to `operator delete[](void*)`.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Default behavior:* Calls `operator delete(ptr)`.

``` cpp
void operator delete[](void* ptr, const std::nothrow_t&) noexcept;
```

*Effects:* The *deallocation
function* ([[basic.stc.dynamic.deallocation]]) called by the
implementation to render the value of `ptr` invalid when the constructor
invoked from a nothrow placement version of the array *new-expression*
throws an exception.

*Replaceable:* a C++program may define a function with this function
signature that displaces the default version defined by the C++standard
library.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Default behavior:* calls `operator delete[](ptr)`.

#### Placement forms <a id="new.delete.placement">[[new.delete.placement]]</a>

These functions are reserved, a C++program may not define functions that
displace the versions in the Standard C++library ([[constraints]]). The
provisions of ([[basic.stc.dynamic]]) do not apply to these reserved
placement forms of `operator new` and `operator delete`.

``` cpp
void* operator new(std::size_t size, void* ptr) noexcept;
```

*Returns:* `ptr`.

*Remarks:* Intentionally performs no other action.

This can be useful for constructing an object at a known address:

``` cpp
void* place = operator new(sizeof(Something));
Something* p = new (place) Something();
```

``` cpp
void* operator new[](std::size_t size, void* ptr) noexcept;
```

*Returns:* `ptr`.

*Remarks:* Intentionally performs no other action.

``` cpp
void operator delete(void* ptr, void*) noexcept;
```

*Effects:* Intentionally performs no action.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Remarks:* Default function called when any part of the initialization
in a placement new expression that invokes the library’s non-array
placement operator new terminates by throwing an
exception ([[expr.new]]).

``` cpp
void operator delete[](void* ptr, void*) noexcept;
```

*Effects:* Intentionally performs no action.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Remarks:* Default function called when any part of the initialization
in a placement new expression that invokes the library’s array placement
operator new terminates by throwing an exception ([[expr.new]]).

#### Data races <a id="new.delete.dataraces">[[new.delete.dataraces]]</a>

For purposes of determining the existence of data races, the library
versions of `operator new`, user replacement versions of global
`operator new`, and the C standard library functions `calloc` and
`malloc` shall behave as though they accessed and modified only the
storage referenced by the return value. The library versions of
`operator delete`, user replacement versions of `operator delete`, and
the C standard library function `free` shall behave as though they
accessed and modified only the storage referenced by their first
argument. The C standard library function `realloc` shall behave as
though it accessed and modified only the storage referenced by its first
argument and by its return value. Calls to these functions that allocate
or deallocate a particular unit of storage shall occur in a single total
order, and each such deallocation call shall happen before the next
allocation (if any) in this order.

### Storage allocation errors <a id="alloc.errors">[[alloc.errors]]</a>

#### Class `bad_alloc` <a id="bad.alloc">[[bad.alloc]]</a>

``` cpp
namespace std {
  class bad_alloc : public exception {
  public:
    bad_alloc() noexcept;
    bad_alloc(const bad_alloc&) noexcept;
    bad_alloc& operator=(const bad_alloc&) noexcept;
    virtual const char* what() const noexcept;
  };
}
```

The class `bad_alloc` defines the type of objects thrown as exceptions
by the implementation to report a failure to allocate storage.

``` cpp
bad_alloc() noexcept;
```

*Effects:* Constructs an object of class `bad_alloc`.

*Remarks:* The result of calling `what()` on the newly constructed
object is implementation-defined.

``` cpp
bad_alloc(const bad_alloc&) noexcept;
    bad_alloc& operator=(const bad_alloc&) noexcept;
```

*Effects:* Copies an object of class `bad_alloc`.

``` cpp
virtual const char* what() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

#### Class `bad_array_new_length` <a id="new.badlength">[[new.badlength]]</a>

``` cpp
namespace std {
  class bad_array_new_length : public bad_alloc {
  public:
    bad_array_new_length() noexcept;
  };
}
```

The class `bad_array_new_length` defines the type of objects thrown as
exceptions by the implementation to report an attempt to allocate an
array of size less than zero or greater than an implementation-defined
limit ([[expr.new]]).

``` cpp
bad_array_new_length() noexcept;
```

*Effects:* constructs an object of class `bad_array_new_length`.

*Remarks:* the result of calling `what()` on the newly constructed
object is implementation-defined.

#### Type `new_handler` <a id="new.handler">[[new.handler]]</a>

``` cpp
typedef void (*new_handler)();
```

The type of a *handler function* to be called by `operator new()` or
`operator new[]()` ([[new.delete]]) when they cannot satisfy a request
for additional storage.

*Required behavior:* A `new_handler` shall perform one of the following:

- make more storage available for allocation and then return;
- throw an exception of type `bad_alloc` or a class derived from
  `bad_alloc`;
- terminate execution of the program without returning to the caller;

#### `set_new_handler` <a id="set.new.handler">[[set.new.handler]]</a>

``` cpp
new_handler set_new_handler(new_handler new_p) noexcept;
```

*Effects:* Establishes the function designated by `new_p` as the current
`new_handler`.

*Returns:* The previous `new_handler`.

*Remarks:* The initial `new_handler` is a null pointer.

#### `get_new_handler` <a id="get.new.handler">[[get.new.handler]]</a>

``` cpp
new_handler get_new_handler() noexcept;
```

*Returns:* The current `new_handler`. This may be a null pointer value.

## Type identification <a id="support.rtti">[[support.rtti]]</a>

The header `<typeinfo>` defines a type associated with type information
generated by the implementation. It also defines two types for reporting
dynamic type identification errors.

\synopsis{Header \texttt{\<typeinfo\>} synopsis}

``` cpp
namespace std {
  class type_info;
  class bad_cast;
  class bad_typeid;
}
```

  [[expr.dynamic.cast]], [[expr.typeid]].

### Class `type_info` <a id="type.info">[[type.info]]</a>

``` cpp
namespace std {
  class type_info {
  public:
    virtual ~type_info();
    bool operator==(const type_info& rhs) const noexcept;
    bool operator!=(const type_info& rhs) const noexcept;
    bool before(const type_info& rhs) const noexcept;
    size_t hash_code() const noexcept;
    const char* name() const noexcept;

    type_info(const type_info& rhs) = delete;            // cannot be copied
    type_info& operator=(const type_info& rhs) = delete; // cannot be copied
  };
}
```

The class `type_info` describes type information generated by the
implementation. Objects of this class effectively store a pointer to a
name for the type, and an encoded value suitable for comparing two types
for equality or collating order. The names, encoding rule, and collating
sequence for types are all unspecified and may differ between programs.

``` cpp
bool operator==(const type_info& rhs) const noexcept;
```

*Effects:* Compares the current object with `rhs`.

*Returns:* `true` if the two values describe the same type.

``` cpp
bool operator!=(const type_info& rhs) const noexcept;
```

*Returns:* `!(*this == rhs)`.

``` cpp
bool before(const type_info& rhs) const noexcept;
```

*Effects:* Compares the current object with `rhs`.

*Returns:* `true` if `*this` precedes `rhs` in the implementation’s
collation order.

``` cpp
size_t hash_code() const noexcept;
```

*Returns:* An unspecified value, except that within a single execution
of the program, it shall return the same value for any two `type_info`
objects which compare equal.

an implementation should return different values for two `type_info`
objects which do not compare equal.

``` cpp
const char* name() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]])

### Class `bad_cast` <a id="bad.cast">[[bad.cast]]</a>

``` cpp
namespace std {
  class bad_cast : public exception {
  public:
    bad_cast() noexcept;
    bad_cast(const bad_cast&) noexcept;
    bad_cast& operator=(const bad_cast&) noexcept;
    virtual const char* what() const noexcept;
  };
}
```

The class `bad_cast` defines the type of objects thrown as exceptions by
the implementation to report the execution of an invalid *dynamic-cast*
expression ([[expr.dynamic.cast]]).

``` cpp
bad_cast() noexcept;
```

*Effects:* Constructs an object of class `bad_cast`.

*Remarks:* The result of calling `what()` on the newly constructed
object is implementation-defined.

``` cpp
bad_cast(const bad_cast&) noexcept;
    bad_cast& operator=(const bad_cast&) noexcept;
```

*Effects:* Copies an object of class `bad_cast`.

``` cpp
virtual const char* what() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]])

### Class `bad_typeid` <a id="bad.typeid">[[bad.typeid]]</a>

``` cpp
namespace std {
  class bad_typeid : public exception {
  public:
    bad_typeid() noexcept;
    bad_typeid(const bad_typeid&) noexcept;
    bad_typeid& operator=(const bad_typeid&) noexcept;
    virtual const char* what() const noexcept;
  };
}
```

The class `bad_typeid` defines the type of objects thrown as exceptions
by the implementation to report a null pointer in a *typeid*
expression ([[expr.typeid]]).

``` cpp
bad_typeid() noexcept;
```

*Effects:* Constructs an object of class `bad_typeid`.

*Remarks:* The result of calling `what()` on the newly constructed
object is implementation-defined.

``` cpp
bad_typeid(const bad_typeid&) noexcept;
    bad_typeid& operator=(const bad_typeid&) noexcept;
```

*Effects:* Copies an object of class `bad_typeid`.

``` cpp
virtual const char* what() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]])

## Exception handling <a id="support.exception">[[support.exception]]</a>

The header `<exception>` defines several types and functions related to
the handling of exceptions in a C++program.

``` cpp
namespace std {
  class exception;
  class bad_exception;
  class nested_exception;

  typedef void (*unexpected_handler)();
  unexpected_handler get_unexpected() noexcept;
  unexpected_handler set_unexpected(unexpected_handler f) noexcept;
  [[noreturn]] void unexpected();

  typedef void (*terminate_handler)();
  terminate_handler get_terminate() noexcept;
  terminate_handler set_terminate(terminate_handler f) noexcept;
  [[noreturn]] void terminate() noexcept;

  bool uncaught_exception() noexcept;

  typedef unspecified exception_ptr;

  exception_ptr current_exception() noexcept;
  [[noreturn]] void rethrow_exception(exception_ptr p);
  template<class E> exception_ptr make_exception_ptr(E e) noexcept;

  [[noreturn]] template <class T> void throw_with_nested(T&& t);
  template <class E> void rethrow_if_nested(const E& e);
}
```

  [[except.special]].

### Class `exception` <a id="exception">[[exception]]</a>

``` cpp
namespace std {
  class exception {
  public:
    exception() noexcept;
    exception(const exception&) noexcept;
    exception& operator=(const exception&) noexcept;
    virtual ~exception();
    virtual const char* what() const noexcept;
  };
}
```

The class `exception` defines the base class for the types of objects
thrown as exceptions by C++standard library components, and certain
expressions, to report errors detected during program execution.

Each standard library class `T` that derives from class `exception`
shall have a publicly accessible copy constructor and a publicly
accessible copy assignment operator that do not exit with an exception.
These member functions shall meet the following postcondition: If two
objects `lhs` and `rhs` both have dynamic type `T` and `lhs` is a copy
of `rhs`, then `strcmp(lhs.what(), rhs.what())` shall equal 0.

``` cpp
exception() noexcept;
```

*Effects:* Constructs an object of class `exception`.

*Remarks:* Does not throw any exceptions.

``` cpp
exception(const exception& rhs) noexcept;
exception& operator=(const exception& rhs) noexcept;
```

*Effects:* Copies an `exception` object.

If `*this` and `rhs` both have dynamic type `exception` then
`strcmp(what(), rhs.what())` shall equal 0.

``` cpp
virtual ~exception();
```

*Effects:* Destroys an object of class `exception`.

*Remarks:* Does not throw any exceptions.

``` cpp
virtual const char* what() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]]). The return value
remains valid until the exception object from which it is obtained is
destroyed or a non-`const` member function of the exception object is
called.

### Class `bad_exception` <a id="bad.exception">[[bad.exception]]</a>

``` cpp
namespace std {
  class bad_exception : public exception {
  public:
    bad_exception() noexcept;
    bad_exception(const bad_exception&) noexcept;
    bad_exception& operator=(const bad_exception&) noexcept;
    virtual const char* what() const noexcept;
  };
}
```

The class `bad_exception` defines the type of objects thrown as
described in ([[except.unexpected]]).

``` cpp
bad_exception() noexcept;
```

*Effects:* Constructs an object of class `bad_exception`.

*Remarks:* The result of calling `what()` on the newly constructed
object is implementation-defined.

``` cpp
bad_exception(const bad_exception&) noexcept;
    bad_exception& operator=(const bad_exception&) noexcept;
```

*Effects:* Copies an object of class `bad_exception`.

``` cpp
virtual const char* what() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]]).

### Abnormal termination <a id="exception.terminate">[[exception.terminate]]</a>

#### Type `terminate_handler` <a id="terminate.handler">[[terminate.handler]]</a>

``` cpp
typedef void (*terminate_handler)();
```

The type of a *handler function* to be called by `std::terminate()` when
terminating exception processing.

*Required behavior:* A `terminate_handler` shall terminate execution of
the program without returning to the caller.

*Default behavior:* The implementation’s default `terminate_handler`
calls `abort()`.

#### `set_terminate` <a id="set.terminate">[[set.terminate]]</a>

``` cpp
terminate_handler set_terminate(terminate_handler f) noexcept;
```

*Effects:* Establishes the function designated by `f` as the current
handler function for terminating exception processing.

*Remarks:* It is unspecified whether a null pointer value designates the
default `terminate_handler`.

*Returns:* The previous `terminate_handler`.

#### `get_terminate` <a id="get.terminate">[[get.terminate]]</a>

``` cpp
terminate_handler get_terminate() noexcept;
```

*Returns:* The current `terminate_handler`. This may be a null pointer
value.

#### `terminate` <a id="terminate">[[terminate]]</a>

``` cpp
[[noreturn]] void terminate() noexcept;
```

*Remarks:* Called by the implementation when exception handling must be
abandoned for any of several reasons ([[except.terminate]]), in effect
immediately after evaluating the
*throw-expression* ([[terminate.handler]]). May also be called directly
by the program.

*Effects:* Calls the current `terminate_handler` function. A default
`terminate_handler` is always considered a callable handler in this
context.

### `uncaught_exception` <a id="uncaught">[[uncaught]]</a>

``` cpp
bool uncaught_exception() noexcept;
```

*Returns:* `true` after the current thread has initialized an exception
object ([[except.throw]]) until a handler for the exception (including
`std::unexpected()` or `std::terminate()`) is
activated ([[except.handle]]). This includes stack
unwinding ([[except.ctor]]).

*Remarks:* When `uncaught_exception()` returns `true`, throwing an
exception can result in a call of
`std::terminate()` ([[except.terminate]]).

### Exception propagation <a id="propagation">[[propagation]]</a>

``` cpp
typedef unspecified exception_ptr;
```

The type exception_ptr can be used to refer to an exception object.

`exception_ptr` shall satisfy the requirements of
`NullablePointer` ([[nullablepointer.requirements]]).

Two non-null values of type `exception_ptr` are equivalent and compare
equal if and only if they refer to the same exception.

The default constructor of `exception_ptr` produces the null value of
the type.

`exception_ptr` shall not be implicitly convertible to any arithmetic,
enumeration, or pointer type.

An implementation might use a reference-counted smart pointer as
`exception_ptr`.

For purposes of determining the presence of a data race, operations on
`exception_ptr` objects shall access and modify only the `exception_ptr`
objects themselves and not the exceptions they refer to. Use of
`rethrow_exception` on `exception_ptr` objects that refer to the same
exception object shall not introduce a data race. if `rethrow_exception`
rethrows the same exception object (rather than a copy), concurrent
access to that rethrown exception object may introduce a data race.
Changes in the number of `exception_ptr` objects that refer to a
particular exception do not introduce a data race.

``` cpp
exception_ptr current_exception() noexcept;
```

*Returns:* An `exception_ptr` object that refers to the currently
handled exception ([[except.handle]]) or a copy of the currently
handled exception, or a null `exception_ptr` object if no exception is
being handled. The referenced object shall remain valid at least as long
as there is an `exception_ptr` object that refers to it. If the function
needs to allocate memory and the attempt fails, it returns an
`exception_ptr` object that refers to an instance of `bad_alloc`. It is
unspecified whether the return values of two successive calls to
`current_exception` refer to the same exception object. That is, it is
unspecified whether `current_exception` creates a new copy each time it
is called. If the attempt to copy the current exception object throws an
exception, the function returns an `exception_ptr` object that refers to
the thrown exception or, if this is not possible, to an instance of
`bad_exception`. The copy constructor of the thrown exception may also
fail, so the implementation is allowed to substitute a `bad_exception`
object to avoid infinite recursion.

``` cpp
[[noreturn]] void rethrow_exception(exception_ptr p);
```

*Requires:* `p` shall not be a null pointer.

*Throws:* the exception object to which `p` refers.

``` cpp
template<class E> exception_ptr make_exception_ptr(E e) noexcept;
```

*Effects:* Creates an `exception_ptr` object that refers to a copy of
`e`, as if

``` cpp
try {
  throw e;
} catch(...) {
  return current_exception();
}
```

This function is provided for convenience and efficiency reasons.

### `nested_exception` <a id="except.nested">[[except.nested]]</a>

``` cpp
namespace std {
  class nested_exception {
  public:
    nested_exception() noexcept;
    nested_exception(const nested_exception&) noexcept = default;
    nested_exception& operator=(const nested_exception&) noexcept = default;
    virtual ~nested_exception() = default;

    // access functions
    [[noreturn]] void rethrow_nested() const;
    exception_ptr nested_ptr() const noexcept;
  };

  [[noreturn]] template<class T> void throw_with_nested(T&& t);
  template <class E> void rethrow_if_nested(const E& e);
}
```

The class `nested_exception` is designed for use as a mixin through
multiple inheritance. It captures the currently handled exception and
stores it for later use.

`nested_exception` has a virtual destructor to make it a polymorphic
class. Its presence can be tested for with `dynamic_cast`.

``` cpp
nested_exception() noexcept;
```

*Effects:* The constructor calls `current_exception()` and stores the
returned value.

``` cpp
[[noreturn]] void rethrow_nested() const;
```

*Effects:* If `nested_ptr()` returns a null pointer, the function calls
`std::terminate()`. Otherwise, it throws the stored exception captured
by `*this`.

``` cpp
exception_ptr nested_ptr() const noexcept;
```

*Returns:* The stored exception captured by this `nested_exception`
object.

``` cpp
[[noreturn]] template <class T> void throw_with_nested(T&& t);
```

Let `U` be `remove_reference<T>::type`.

*Requires:* `U` shall be `CopyConstructible`.

*Throws:* if `U` is a non-union class type not derived from
`nested_exception`, an exception of unspecified type that is publicly
derived from both `U` and `nested_exception` and constructed from
`std::forward<T>(t)`, otherwise `std::forward<T>(t)`.

``` cpp
template <class E> void rethrow_if_nested(const E& e);
```

*Effects:* If the dynamic type of `e` is publicly and unambiguously
derived from `nested_exception`, calls `dynamic_cast<const`
`nested_exception&>(e).rethrow_nested()`.

## Initializer lists <a id="support.initlist">[[support.initlist]]</a>

The header `<initializer_list>` defines one type.

``` cpp
namespace std {
  template<class E> class initializer_list {
  public:
    typedef E value_type;
    typedef const E& reference;
    typedef const E& const_reference;
    typedef size_t size_type;

    typedef const E* iterator;
    typedef const E* const_iterator;

    initializer_list() noexcept;

    size_t size() const noexcept;      // number of elements
    const E* begin() const noexcept;   // first element
    const E* end() const noexcept;     // one past the last element
  };

  // [support.initlist.range] initializer list range access
  template<class E> const E* begin(initializer_list<E> il) noexcept;
  template<class E> const E* end(initializer_list<E> il) noexcept;
}
```

An object of type `initializer_list<E>` provides access to an array of
objects of type `const E`. A pair of pointers or a pointer plus a length
would be obvious representations for `initializer_list`.
`initializer_list` is used to implement initializer lists as specified
in  [[dcl.init.list]]. Copying an initializer list does not copy the
underlying elements.

### Initializer list constructors <a id="support.initlist.cons">[[support.initlist.cons]]</a>

``` cpp
initializer_list() noexcept;
```

*Effects:* constructs an empty `initializer_list` object.

`size() == 0`

### Initializer list access <a id="support.initlist.access">[[support.initlist.access]]</a>

``` cpp
const E* begin() const noexcept;
```

*Returns:* A pointer to the beginning of the array. If `size() == 0` the
values of `begin()` and `end()` are unspecified but they shall be
identical.

``` cpp
const E* end() const noexcept;
```

*Returns:* `begin() + size()`

``` cpp
size_t size() const noexcept;
```

*Returns:* The number of elements in the array.

*Complexity:* constant time.

### Initializer list range access <a id="support.initlist.range">[[support.initlist.range]]</a>

``` cpp
template<class E> const E* begin(initializer_list<E> il) noexcept;
```

*Returns:* `il.begin()`.

``` cpp
template<class E> const E* end(initializer_list<E> il) noexcept;
```

*Returns:* `il.end()`.

## Other runtime support <a id="support.runtime">[[support.runtime]]</a>

Headers `<csetjmp>` (nonlocal jumps), `<csignal>` (signal handling),
`<cstdalign> (alignment),` `<cstdarg>` (variable arguments),
`<cstdbool>` (`\xname{bool_true_false_are_defined}`). `<cstdlib>`
(runtime environment `getenv(), system()`), and `<ctime>` (system clock
`clock(), time()`) provide further compatibility with C code.

The contents of these headers are the same as the Standard C library
headers `<setjmp.h>`, `<signal.h>`, `<stdalign.h>`, `<stdarg.h>`,
`<stdbool.h>`, `<stdlib.h>`, and `<time.h>`, respectively, with the
following changes:

The restrictions that ISO C places on the second parameter to the
`va_start()` macro in header `<stdarg.h>` are different in this
International Standard. The parameter `parmN` is the identifier of the
rightmost parameter in the variable parameter list of the function
definition (the one just before the `...`).[^34] If the parameter
`parmN` is declared with a function, array, or reference type, or with a
type that is not compatible with the type that results when passing an
argument for which there is no parameter, the behavior is undefined.

ISO C 4.8.1.1.

The function signature `longjmp(jmp_buf jbuf, int val)` has more
restricted behavior in this International Standard. A `setjmp`/`longjmp`
call pair has undefined behavior if replacing the `setjmp` and `longjmp`
by `catch` and `throw` would invoke any non-trivial destructors for any
automatic objects.

ISO C 7.10.4, 7.8, 7.6, 7.12.

Calls to the function `getenv` shall not introduce a data race (
[[res.on.data.races]]) provided that nothing modifies the environment.
Calls to the POSIX functions `setenv` and `putenv` modify the
environment.

A call to the `setlocale` function may introduce a data race with other
calls to the `setlocale` function or with calls to functions that are
affected by the current C locale. The implementation shall behave as if
no library function other than `locale::global()` calls the `setlocale`
function.

The header `<cstdalign>` and the header `<stdalign.h>` shall not define
a macro named `alignas`.

The header `<cstdbool>` and the header `<stdbool.h>` shall not define
macros named `bool`, `true`, or `false`.

The common subset of the C and C++languages consists of all
declarations, definitions, and expressions that may appear in a well
formed C++program and also in a conforming C program. A POF (“plain old
function”) is a function that uses only features from this common
subset, and that does not directly or indirectly use any function that
is not a POF, except that it may use functions defined in Clause 
[[atomics]] that are not member functions. All signal handlers shall
have C linkage. A POF that could be used as a signal handler in a
conforming C program does not produce undefined behavior when used as a
signal handler in a C++program. The behavior of any other function used
as a signal handler in a C++program is *implementation-defined*.[^35]

<!-- Link reference definitions -->
[alloc.errors]: #alloc.errors
[atomics]: atomics.md#atomics
[bad.alloc]: #bad.alloc
[bad.cast]: #bad.cast
[bad.exception]: #bad.exception
[bad.typeid]: #bad.typeid
[basic.align]: basic.md#basic.align
[basic.fundamental]: basic.md#basic.fundamental
[basic.start]: basic.md#basic.start
[basic.start.term]: basic.md#basic.start.term
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[c.limits]: #c.limits
[class]: class.md#class
[class.free]: special.md#class.free
[complex]: numerics.md#complex
[constraints]: library.md#constraints
[conv.ptr]: conv.md#conv.ptr
[conv.rank]: conv.md#conv.rank
[cstdint]: #cstdint
[cstdint.syn]: #cstdint.syn
[dcl.init.list]: dcl.md#dcl.init.list
[denorm.style]: #denorm.style
[except.ctor]: except.md#except.ctor
[except.handle]: except.md#except.handle
[except.nested]: #except.nested
[except.special]: except.md#except.special
[except.terminate]: except.md#except.terminate
[except.throw]: except.md#except.throw
[except.unexpected]: except.md#except.unexpected
[exception]: #exception
[exception.terminate]: #exception.terminate
[expr.add]: expr.md#expr.add
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.new]: expr.md#expr.new
[expr.sizeof]: expr.md#expr.sizeof
[expr.typeid]: expr.md#expr.typeid
[get.new.handler]: #get.new.handler
[get.terminate]: #get.terminate
[intro.execution]: intro.md#intro.execution
[intro.memory]: intro.md#intro.memory
[intro.multithread]: intro.md#intro.multithread
[language.support]: #language.support
[limits]: #limits
[limits.numeric]: #limits.numeric
[limits.syn]: #limits.syn
[locale.codecvt]: localization.md#locale.codecvt
[memory]: utilities.md#memory
[multibyte.strings]: library.md#multibyte.strings
[new.badlength]: #new.badlength
[new.delete]: #new.delete
[new.delete.array]: #new.delete.array
[new.delete.dataraces]: #new.delete.dataraces
[new.delete.placement]: #new.delete.placement
[new.delete.single]: #new.delete.single
[new.handler]: #new.handler
[nullablepointer.requirements]: library.md#nullablepointer.requirements
[numeric.limits]: #numeric.limits
[numeric.limits.members]: #numeric.limits.members
[numeric.special]: #numeric.special
[propagation]: #propagation
[res.on.data.races]: library.md#res.on.data.races
[round.style]: #round.style
[set.new.handler]: #set.new.handler
[set.terminate]: #set.terminate
[string.classes]: strings.md#string.classes
[support.dynamic]: #support.dynamic
[support.exception]: #support.exception
[support.general]: #support.general
[support.initlist]: #support.initlist
[support.initlist.access]: #support.initlist.access
[support.initlist.cons]: #support.initlist.cons
[support.initlist.range]: #support.initlist.range
[support.limits]: #support.limits
[support.limits.general]: #support.limits.general
[support.rtti]: #support.rtti
[support.runtime]: #support.runtime
[support.start.term]: #support.start.term
[support.types]: #support.types
[tab:lang.sup.lib.summary]: #tab:lang.sup.lib.summary
[tab:support.hdr.cfloat]: #tab:support.hdr.cfloat
[tab:support.hdr.climits]: #tab:support.hdr.climits
[tab:support.hdr.cstddef]: #tab:support.hdr.cstddef
[tab:support.hdr.cstdlib]: #tab:support.hdr.cstdlib
[temp.dep.constexpr]: temp.md#temp.dep.constexpr
[temp.dep.expr]: temp.md#temp.dep.expr
[terminate]: #terminate
[terminate.handler]: #terminate.handler
[type.info]: #type.info
[uncaught]: #uncaught

[^1]: Possible definitions include `0` and `0L`, but not `(void*)0`.

[^2]: Note that `offsetof` is required to work as specified even if
    unary `operator&` is overloaded for any of the types involved.

[^3]: Equivalent to `CHAR_MIN`, `SHRT_MIN`, `FLT_MIN`, `DBL_MIN`, etc.

[^4]: Equivalent to `CHAR_MAX`, `SHRT_MAX`, `FLT_MAX`, `DBL_MAX`, etc.

[^5]: `lowest()` is necessary because not all floating-point
    representations have a smallest (most negative) value that is the
    negative of the largest (most positive) finite value.

[^6]: Equivalent to `FLT_MANT_DIG`, `DBL_MANT_DIG`, `LDBL_MANT_DIG`.

[^7]: Equivalent to `FLT_DIG`, `DBL_DIG`, `LDBL_DIG`.

[^8]: Equivalent to `FLT_RADIX`.

[^9]: Distinguishes types with bases other than 2 (e.g. BCD).

[^10]: Equivalent to `FLT_EPSILON`, `DBL_EPSILON`, `LDBL_EPSILON`.

[^11]: Rounding error is described in ISO/IEC 10967-1 Language
    independent arithmetic - Part 1 Section 5.2.8 and Annex A Rationale
    Section A.5.2.8 - Rounding constants.

[^12]: Equivalent to `FLT_MIN_EXP`, `DBL_MIN_EXP`, `LDBL_MIN_EXP`.

[^13]: Equivalent to `FLT_MIN_10_EXP`, `DBL_MIN_10_EXP`,
    `LDBL_MIN_10_EXP`.

[^14]: Equivalent to `FLT_MAX_EXP`, `DBL_MAX_EXP`, `LDBL_MAX_EXP`.

[^15]: Equivalent to `FLT_MAX_10_EXP`, `DBL_MAX_10_EXP`,
    `LDBL_MAX_10_EXP`.

[^16]: Required by LIA-1.

[^17]: Required by LIA-1.

[^18]: Required by LIA-1.

[^19]: See IEC 559.

[^20]: Required by LIA-1.

[^21]: Required by LIA-1.

[^22]: Required by LIA-1.

[^23]: Required by LIA-1.

[^24]: International Electrotechnical Commission standard 559 is the
    same as IEEE 754.

[^25]: Required by LIA-1.

[^26]: Required by LIA-1.

[^27]: Required by LIA-1.

[^28]: Refer to IEC 559. Required by LIA-1.

[^29]: Equivalent to `FLT_ROUNDS`. Required by LIA-1.

[^30]: A function is called for every time it is registered.

[^31]: Objects with automatic storage duration are all destroyed in a
    program whose function `main()` contains no automatic objects and
    executes the call to `exit()`. Control can be transferred directly
    to such a `main()` by throwing an exception that is caught in
    `main()`.

[^32]: The macros `EXIT_FAILURE` and `EXIT_SUCCESS` are defined in
    `<cstdlib>`.

[^33]: It is not the direct responsibility of
    `operator new[](std::size_t)` or `operator delete[](void*)` to note
    the repetition count or element size of the array. Those operations
    are performed elsewhere in the array `new` and `delete` expressions.
    The array `new` expression, may, however, increase the `size`
    argument to `operator new[](std::size_t)` to obtain space to store
    supplemental information.

[^34]: Note that `va_start` is required to work as specified even if
    unary `operator&` is overloaded for the type of `parmN`.

[^35]: In particular, a signal handler using exception handling is very
    likely to have problems. Also, invoking `std::exit` may cause
    destruction of objects, including those of the standard library
    implementation, which, in general, yields undefined behavior in a
    signal handler (see  [[intro.execution]]).
