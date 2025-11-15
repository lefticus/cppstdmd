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
| [[support.types]]      | Common definitions        | `<cstddef>`          |
|                        |                           | `<cstdlib>`          |
| [[support.limits]]     | Implementation properties | `<limits>`           |
|                        |                           | `<climits>`          |
|                        |                           | `<cfloat>`           |
| [[cstdint]]            | Integer types             | `<cstdint>`          |
| [[support.start.term]] | Start and termination     | `<cstdlib>`          |
| [[support.dynamic]]    | Dynamic memory management | `<new>`              |
| [[support.rtti]]       | Type identification       | `<typeinfo>`         |
| [[support.exception]]  | Exception handling        | `<exception>`        |
| [[support.initlist]]   | Initializer lists         | `<initializer_list>` |
| [[support.runtime]]    | Other runtime support     | `<csignal>`          |
|                        |                           | `<csetjmp>`          |
|                        |                           | `<cstdarg>`          |
|                        |                           | `<cstdlib>`          |


## Common definitions <a id="support.types">[[support.types]]</a>

### Header `<cstddef>` synopsis <a id="cstddef.syn">[[cstddef.syn]]</a>

``` cpp
namespace std {
  using ptrdiff_t = see below;
  using size_t = see below;
  using max_align_t = see below;
  using nullptr_t = decltype(nullptr);

  enum class byte : unsigned char {};

  // [support.types.byteops], byte type operations
  template <class IntType>
    constexpr byte& operator<<=(byte& b, IntType shift) noexcept;
  template <class IntType>
    constexpr byte operator<<(byte b, IntType shift) noexcept;
  template <class IntType>
    constexpr byte& operator>>=(byte& b, IntType shift) noexcept;
  template <class IntType>
    constexpr byte operator>>(byte b, IntType shift) noexcept;
  constexpr byte& operator|=(byte& l, byte r) noexcept;
  constexpr byte operator|(byte l, byte r) noexcept;
  constexpr byte& operator&=(byte& l, byte r) noexcept;
  constexpr byte operator&(byte l, byte r) noexcept;
  constexpr byte& operator^=(byte& l, byte r) noexcept;
  constexpr byte operator^(byte l, byte r) noexcept;
  constexpr byte operator~(byte b) noexcept;
  template <class IntType>
    constexpr IntType to_integer(byte b) noexcept;
}

#define NULL see below
#define offsetof(P, D) see below
```

The contents and meaning of the header `<cstddef>` are the same as the C
standard library header `<stddef.h>`, except that it does not declare
the type `wchar_t`, that it also declares the type `byte` and its
associated operations ([[support.types.byteops]]), and as noted in
[[support.types.nullptr]] and [[support.types.layout]].

ISO C 7.19

### Header `<cstdlib>` synopsis <a id="cstdlib.syn">[[cstdlib.syn]]</a>

``` cpp
namespace std {
  using size_t = see below;
  using div_t = see below;
  using ldiv_t = see below;
  using lldiv_t = see below;
}

#define NULL see below
#define EXIT_FAILURE see below
#define EXIT_SUCCESS see below
#define RAND_MAX see below
#define MB_CUR_MAX see below

namespace std {
  // Exposition-only function type aliases
  extern "C" using c-atexit-handler = void();                        // exposition only
  extern "C++" using atexit-handler = void();                        // exposition only
  extern "C" using c-compare-pred = int(const void*, const void*);   // exposition only
  extern "C++" using compare-pred = int(const void*, const void*);   // exposition only

  // [support.start.term], start and termination
  [[noreturn]] void abort() noexcept;
  int atexit(c-atexit-handler* func) noexcept;
  int atexit(atexit-handler* func) noexcept;
  int at_quick_exit(c-atexit-handler* func) noexcept;
  int at_quick_exit(atexit-handler* func) noexcept;
  [[noreturn]] void exit(int status);
  [[noreturn]] void _Exit(int status) noexcept;
  [[noreturn]] void quick_exit(int status) noexcept;

  char* getenv(const char* name);
  int system(const char* string);

  // [c.malloc], C library memory allocation
  void* aligned_alloc(size_t alignment, size_t size);
  void* calloc(size_t nmemb, size_t size);
  void free(void* ptr);
  void* malloc(size_t size);
  void* realloc(void* ptr, size_t size);

  double atof(const char* nptr);
  int atoi(const char* nptr);
  long int atol(const char* nptr);
  long long int atoll(const char* nptr);
  double strtod(const char* nptr, char** endptr);
  float strtof(const char* nptr, char** endptr);
  long double strtold(const char* nptr, char** endptr);
  long int strtol(const char* nptr, char** endptr, int base);
  long long int strtoll(const char* nptr, char** endptr, int base);
  unsigned long int strtoul(const char* nptr, char** endptr, int base);
  unsigned long long int strtoull(const char* nptr, char** endptr, int base);

  // [c.mb.wcs], multibyte / wide string and character conversion functions
  int mblen(const char* s, size_t n);
  int mbtowc(wchar_t* pwc, const char* s, size_t n);
  int wctomb(char* s, wchar_t wchar);
  size_t mbstowcs(wchar_t* pwcs, const char* s, size_t n);
  size_t wcstombs(char* s, const wchar_t* pwcs, size_t n);

  // [alg.c.library], C standard library algorithms
  void* bsearch(const void* key, const void* base, size_t nmemb, size_t size,
                c-compare-pred*\itcorr[-1] compar);
  void* bsearch(const void* key, const void* base, size_t nmemb, size_t size,
                compare-pred*\itcorr[-1] compar);
  void qsort(void* base, size_t nmemb, size_t size, c-compare-pred*\itcorr[-1] compar);
  void qsort(void* base, size_t nmemb, size_t size, compare-pred*\itcorr[-1] compar);

  // [c.math.rand], low-quality random number generation
  int rand();
  void srand(unsigned int seed);

  // [c.math.abs], absolute values
  int abs(int j);
  long int abs(long int j);
  long long int abs(long long int j);
  float abs(float j);
  double abs(double j);
  long double abs(long double j);

  long int labs(long int j);
  long long int llabs(long long int j);

  div_t div(int numer, int denom);
  ldiv_t div(long int numer, long int denom);             // see [library.c]
  lldiv_t div(long long int numer, long long int denom);  // see [library.c]
  ldiv_t ldiv(long int numer, long int denom);
  lldiv_t lldiv(long long int numer, long long int denom);
}
```

The contents and meaning of the header `<cstdlib>` are the same as the C
standard library header `<stdlib.h>`, except that it does not declare
the type `wchar_t`, and except as noted in [[support.types.nullptr]],
[[support.types.layout]], [[support.start.term]], [[c.malloc]],
[[c.mb.wcs]], [[alg.c.library]], [[c.math.rand]], and [[c.math.abs]].

[*Note 1*: Several functions have additional overloads in this
International Standard, but they have the same behavior as in the C
standard library ([[library.c]]). — *end note*]

ISO C 7.22

### Null pointers <a id="support.types.nullptr">[[support.types.nullptr]]</a>

The type `nullptr_t` is a synonym for the type of a `nullptr`
expression, and it has the characteristics described in 
[[basic.fundamental]] and  [[conv.ptr]].

[*Note 1*: Although `nullptr`’s address cannot be taken, the address of
another `nullptr_t` object that is an lvalue can be
taken. — *end note*]

The macro `NULL` is an *implementation-defined* null pointer constant.
[^1]

### Sizes, alignments, and offsets <a id="support.types.layout">[[support.types.layout]]</a>

The macro `offsetof(type, member-designator)` has the same semantics as
the corresponding macro in the C standard library header `<stddef.h>`,
but accepts a restricted set of `type` arguments in this International
Standard. Use of the `offsetof` macro with a `type` other than a
standard-layout class (Clause  [[class]]) is
conditionally-supported.[^2] The expression
`offsetof(type, member-designator)` is never type-dependent (
[[temp.dep.expr]]) and it is value-dependent ([[temp.dep.constexpr]])
if and only if `type` is dependent. The result of applying the
`offsetof` macro to a static data member or a function member is
undefined. No operation invoked by the `offsetof` macro shall throw an
exception and `noexcept(offsetof(type, member-designator))` shall be
`true`.

The type `ptrdiff_t` is an *implementation-defined* signed integer type
that can hold the difference of two subscripts in an array object, as
described in  [[expr.add]].

The type `size_t` is an *implementation-defined* unsigned integer type
that is large enough to contain the size in bytes of any object.

[*Note 1*: It is recommended that implementations choose types for
`ptrdiff_t` and `size_t` whose integer conversion ranks ([[conv.rank]])
are no greater than that of `signed long int` unless a larger size is
necessary to contain all the possible values. — *end note*]

The type `max_align_t` is a POD type whose alignment requirement is at
least as great as that of every scalar type, and whose alignment
requirement is supported in every context.

Alignment ([[basic.align]]), Sizeof ([[expr.sizeof]]), Additive
operators ([[expr.add]]), Free store ([[class.free]]), and ISO C 7.19.

### `byte` type operations <a id="support.types.byteops">[[support.types.byteops]]</a>

``` cpp
template <class IntType>
  constexpr byte& operator<<=(byte& b, IntType shift) noexcept;
```

*Remarks:* This function shall not participate in overload resolution
unless `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to:
`return b = byte(static_cast<unsigned char>(b) << shift);`

``` cpp
template <class IntType>
  constexpr byte operator<<(byte b, IntType shift) noexcept;
```

*Remarks:* This function shall not participate in overload resolution
unless `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to:
`return byte(static_cast<unsigned char>(b) << shift);`

``` cpp
template <class IntType>
  constexpr byte& operator>>=(byte& b, IntType shift) noexcept;
```

*Remarks:* This function shall not participate in overload resolution
unless `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to:
`return b = byte(static_cast<unsigned char>(b) >> shift);`

``` cpp
template <class IntType>
  constexpr byte operator>>(byte b, IntType shift) noexcept;
```

*Remarks:* This function shall not participate in overload resolution
unless `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to:
`return byte(static_cast<unsigned char>(b) >> shift);`

``` cpp
constexpr byte& operator|=(byte& l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return l = byte(static_cast<unsigned char>(l) | static_cast<unsigned char>(r));
```

``` cpp
constexpr byte operator|(byte l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return byte(static_cast<unsigned char>(l) | static_cast<unsigned char>(r));
```

``` cpp
constexpr byte& operator&=(byte& l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return l = byte(static_cast<unsigned char>(l) & static_cast<unsigned char>(r));
```

``` cpp
constexpr byte operator&(byte l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return byte(static_cast<unsigned char>(l) & static_cast<unsigned char>(r));
```

\indexlibrarymember{operator^=}{byte}

``` cpp
constexpr byte& operator^=(byte& l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return l = byte(static_cast<unsigned char>(l) ^ static_cast<unsigned char>(r));
```

\indexlibrarymember{operator^}{byte}

``` cpp
constexpr byte operator^(byte l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return byte(static_cast<unsigned char>(l) ^ static_cast<unsigned char>(r));
```

\indexlibrarymember{operator~}{byte}

``` cpp
constexpr byte operator~(byte b) noexcept;
```

*Effects:* Equivalent to: `return byte(s̃tatic_cast<unsigned char>(b));`

``` cpp
template <class IntType>
  constexpr IntType to_integer(byte b) noexcept;
```

*Remarks:* This function shall not participate in overload resolution
unless `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to: `return IntType(b);`

## Implementation properties <a id="support.limits">[[support.limits]]</a>

### General <a id="support.limits.general">[[support.limits.general]]</a>

The headers `<limits>` ([[limits.syn]]), `<climits>` (
[[climits.syn]]), and `<cfloat>` ([[cfloat.syn]]) supply
characteristics of implementation-dependent arithmetic types (
[[basic.fundamental]]).

### Header `<limits>` synopsis <a id="limits.syn">[[limits.syn]]</a>

``` cpp
namespace std {
  // [fp.style], floating-point type properties
  enum float_round_style;
  enum float_denorm_style;

  // [numeric.limits], class template numeric_limits
  template<class T> class numeric_limits;

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

### Floating-point type properties <a id="fp.style">[[fp.style]]</a>

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

The rounding mode for floating-point arithmetic is characterized by the
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

The presence or absence of subnormal numbers (variable number of
exponent bits) is characterized by the values:

- `denorm_indeterminate` if it cannot be determined whether or not the
  type allows subnormal values
- `denorm_absent` if the type does not allow subnormal values
- `denorm_present` if the type does allow subnormal values

### Class template `numeric_limits` <a id="numeric.limits">[[numeric.limits]]</a>

The `numeric_limits` class template provides a C++program with
information about various properties of the implementation’s
representation of the arithmetic types.

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

For all members declared `static` `constexpr` in the `numeric_limits`
template, specializations shall define these values in such a way that
they are usable as constant expressions.

The default `numeric_limits<T>` template shall have all members, but
with 0 or `false` values.

Specializations shall be provided for each arithmetic type, both
floating-point and integer, including `bool`. The member
`is_specialized` shall be `true` for all such specializations of
`numeric_limits`.

The value of each member of a specialization of `numeric_limits` on a
cv-qualified type `cv T` shall be equal to the value of the
corresponding member of the specialization on the unqualified type `T`.

Non-arithmetic standard types, such as `complex<T>` ([[complex]]),
shall not have specializations.

#### `numeric_limits` members <a id="numeric.limits.members">[[numeric.limits.members]]</a>

Each member function defined in this subclause is signal-safe (
[[csignal.syn]]).

``` cpp
static constexpr T min() noexcept;
```

Minimum finite value.[^3]

For floating types with subnormal numbers, returns the minimum positive
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

For floating-point types, the number of `radix` digits in the
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

Meaningful for all floating-point types.

``` cpp
static constexpr bool is_signed;
```

`true` if the type is signed.

Meaningful for all specializations.

``` cpp
static constexpr bool is_integer;
```

`true` if the type is integer.

Meaningful for all specializations.

``` cpp
static constexpr bool is_exact;
```

`true` if the type uses an exact representation. All integer types are
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

Meaningful for all floating-point types.

``` cpp
static constexpr T round_error() noexcept;
```

Measure of the maximum rounding error.[^11]

``` cpp
static constexpr int  min_exponent;
```

Minimum negative integer such that `radix` raised to the power of one
less than that integer is a normalized floating-point number.[^12]

Meaningful for all floating-point types.

``` cpp
static constexpr int  min_exponent10;
```

Minimum negative integer such that 10 raised to that power is in the
range of normalized floating-point numbers.[^13]

Meaningful for all floating-point types.

``` cpp
static constexpr int  max_exponent;
```

Maximum positive integer such that `radix` raised to the power one less
than that integer is a representable finite floating-point number.[^14]

Meaningful for all floating-point types.

``` cpp
static constexpr int  max_exponent10;
```

Maximum positive integer such that 10 raised to that power is in the
range of representable finite floating-point numbers.[^15]

Meaningful for all floating-point types.

``` cpp
static constexpr bool has_infinity;
```

`true` if the type has a representation for positive infinity.

Meaningful for all floating-point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr bool has_quiet_NaN;
```

`true` if the type has a representation for a quiet (non-signaling) “Not
a Number”.[^16]

Meaningful for all floating-point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr bool has_signaling_NaN;
```

`true` if the type has a representation for a signaling “Not a
Number”.[^17]

Meaningful for all floating-point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr float_denorm_style has_denorm;
```

`denorm_present` if the type allows subnormal values (variable number of
exponent bits)[^18], `denorm_absent` if the type does not allow
subnormal values, and `denorm_indeterminate` if it is indeterminate at
compile time whether the type allows subnormal values.

Meaningful for all floating-point types.

``` cpp
static constexpr bool has_denorm_loss;
```

`true` if loss of accuracy is detected as a denormalization loss, rather
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

Representation of a quiet “Not a Number”, if available.[^21]

Meaningful for all specializations for which `has_quiet_NaN != false`.
Required in specializations for which `is_iec559 != false`.

``` cpp
static constexpr T signaling_NaN() noexcept;
```

Representation of a signaling “Not a Number”, if available.[^22]

Meaningful for all specializations for which
`has_signaling_NaN != false`. Required in specializations for which
`is_iec559 != false`.

``` cpp
static constexpr T denorm_min() noexcept;
```

Minimum positive subnormal value.[^23]

Meaningful for all floating-point types.

In specializations for which `has_denorm == false`, returns the minimum
positive normalized value.

``` cpp
static constexpr bool is_iec559;
```

`true` if and only if the type adheres to ISO/IEC/IEEE 60559.[^24]

Meaningful for all floating-point types.

``` cpp
static constexpr bool is_bounded;
```

`true` if the set of values representable by the type is finite.[^25]

[*Note 1*: All fundamental types ([[basic.fundamental]]) are bounded.
This member would be `false` for arbitrary precision
types. — *end note*]

Meaningful for all specializations.

``` cpp
static constexpr bool is_modulo;
```

`true` if the type is modulo.[^26] A type is modulo if, for any
operation involving `+`, `-`, or `*` on values of that type whose result
would fall outside the range \[`min()`, `max()`\], the value returned
differs from the true value by an integer multiple of
`max() - min() + 1`.

[*Example 1*: `is_modulo` is `false` for signed integer
types ([[basic.fundamental]]) unless an implementation, as an extension
to this International Standard, defines signed integer overflow to
wrap. — *end example*]

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

Meaningful for all floating-point types.

``` cpp
static constexpr float_round_style round_style;
```

The rounding style for the type.[^29]

Meaningful for all floating-point types. Specializations for integer
types shall return `round_toward_zero`.

#### `numeric_limits` specializations <a id="numeric.special">[[numeric.special]]</a>

All members shall be provided for all specializations. However, many
values are only required to be meaningful under certain conditions (for
example, `epsilon()` is only meaningful if `is_integer` is `false`). Any
value that is not “meaningful” shall be set to 0 or `false`.

[*Example 1*:

``` cpp
namespace std {
  template<> class numeric_limits<float> {
  public:
    static constexpr bool is_specialized = true;

    static constexpr float min() noexcept { return 1.17549435E-38F; }
    static constexpr float max() noexcept { return 3.40282347E+38F; }
    static constexpr float lowest() noexcept { return -3.40282347E+38F; }

    static constexpr int digits   = 24;
    static constexpr int digits10 =  6;
    static constexpr int max_digits10 =  9;

    static constexpr bool is_signed  = true;
    static constexpr bool is_integer = false;
    static constexpr bool is_exact   = false;

    static constexpr int radix = 2;
    static constexpr float epsilon() noexcept     { return 1.19209290E-07F; }
    static constexpr float round_error() noexcept { return 0.5F; }

    static constexpr int min_exponent   = -125;
    static constexpr int min_exponent10 = - 37;
    static constexpr int max_exponent   = +128;
    static constexpr int max_exponent10 = + 38;

    static constexpr bool has_infinity             = true;
    static constexpr bool has_quiet_NaN            = true;
    static constexpr bool has_signaling_NaN        = true;
    static constexpr float_denorm_style has_denorm = denorm_absent;
    static constexpr bool has_denorm_loss          = false;

    static constexpr float infinity()      noexcept { return value; }
    static constexpr float quiet_NaN()     noexcept { return value; }
    static constexpr float signaling_NaN() noexcept { return value; }
    static constexpr float denorm_min()    noexcept { return min(); }

    static constexpr bool is_iec559  = true;
    static constexpr bool is_bounded = true;
    static constexpr bool is_modulo  = false;
    static constexpr bool traps      = true;
    static constexpr bool tinyness_before = true;

    static constexpr float_round_style round_style = round_to_nearest;
  };
}
```

— *end example*]

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

### Header `<climits>` synopsis <a id="climits.syn">[[climits.syn]]</a>

``` cpp
#define CHAR_BIT see below
#define SCHAR_MIN see below
#define SCHAR_MAX see below
#define UCHAR_MAX see below
#define CHAR_MIN see below
#define CHAR_MAX see below
#define MB_LEN_MAX see below
#define SHRT_MIN see below
#define SHRT_MAX see below
#define USHRT_MAX see below
#define INT_MIN see below
#define INT_MAX see below
#define UINT_MAX see below
#define LONG_MIN see below
#define LONG_MAX see below
#define ULONG_MAX see below
#define LLONG_MIN see below
#define LLONG_MAX see below
#define ULLONG_MAX see below
```

The header `<climits>` defines all macros the same as the C standard
library header `<limits.h>`.

[*Note 1*: The types of the constants defined by macros in `<climits>`
are not required to match the types to which the macros
refer. — *end note*]

ISO C 5.2.4.2.1

### Header `<cfloat>` synopsis <a id="cfloat.syn">[[cfloat.syn]]</a>

``` cpp
#define FLT_ROUNDS see below
#define FLT_EVAL_METHOD see below
#define FLT_HAS_SUBNORM see below
#define DBL_HAS_SUBNORM see below
#define LDBL_HAS_SUBNORM see below
#define FLT_RADIX see below
#define FLT_MANT_DIG see below
#define DBL_MANT_DIG see below
#define LDBL_MANT_DIG see below
#define FLT_DECIMAL_DIG see below
#define DBL_DECIMAL_DIG see below
#define LDBL_DECIMAL_DIG see below
#define DECIMAL_DIG see below
#define FLT_DIG see below
#define DBL_DIG see below
#define LDBL_DIG see below
#define FLT_MIN_EXP see below
#define DBL_MIN_EXP see below
#define LDBL_MIN_EXP see below
#define FLT_MIN_10_EXP see below
#define DBL_MIN_10_EXP see below
#define LDBL_MIN_10_EXP see below
#define FLT_MAX_EXP see below
#define DBL_MAX_EXP see below
#define LDBL_MAX_EXP see below
#define FLT_MAX_10_EXP see below
#define DBL_MAX_10_EXP see below
#define LDBL_MAX_10_EXP see below
#define FLT_MAX see below
#define DBL_MAX see below
#define LDBL_MAX see below
#define FLT_EPSILON see below
#define DBL_EPSILON see below
#define LDBL_EPSILON see below
#define FLT_MIN see below
#define DBL_MIN see below
#define LDBL_MIN see below
#define FLT_TRUE_MIN see below
#define DBL_TRUE_MIN see below
#define LDBL_TRUE_MIN see below
```

The header `<cfloat>` defines all macros the same as the C standard
library header `<float.h>`.

ISO C 5.2.4.2.2

## Integer types <a id="cstdint">[[cstdint]]</a>

### Header `<cstdint>` synopsis <a id="cstdint.syn">[[cstdint.syn]]</a>

``` cpp
namespace std {
  using int8_t         = signed integer type;  // optional
  using int16_t        = signed integer type;  // optional
  using int32_t        = signed integer type;  // optional
  using int64_t        = signed integer type;  // optional

  using int_fast8_t    = signed integer type;
  using int_fast16_t   = signed integer type;
  using int_fast32_t   = signed integer type;
  using int_fast64_t   = signed integer type;

  using int_least8_t   = signed integer type;
  using int_least16_t  = signed integer type;
  using int_least32_t  = signed integer type;
  using int_least64_t  = signed integer type;

  using intmax_t       = signed integer type;
  using intptr_t       = signed integer type;   // optional

  using uint8_t        = unsigned integer type; // optional
  using uint16_t       = unsigned integer type; // optional
  using uint32_t       = unsigned integer type; // optional
  using uint64_t       = unsigned integer type; // optional

  using uint_fast8_t   = unsigned integer type;
  using uint_fast16_t  = unsigned integer type;
  using uint_fast32_t  = unsigned integer type;
  using uint_fast64_t  = unsigned integer type;

  using uint_least8_t  = unsigned integer type;
  using uint_least16_t = unsigned integer type;
  using uint_least32_t = unsigned integer type;
  using uint_least64_t = unsigned integer type;

  using uintmax_t      = unsigned integer type;
  using uintptr_t      = unsigned integer type; // optional
}
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

The header defines all types and macros the same as the C standard
library header `<stdint.h>`.

ISO C 7.20.

## Start and termination <a id="support.start.term">[[support.start.term]]</a>

[*Note 1*: The header `<cstdlib>` ([[cstdlib.syn]]) declares the
functions described in this subclause. — *end note*]

``` cpp
[[noreturn]] void _Exit(int status) noexcept;
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* The program is terminated without executing destructors for
objects of automatic, thread, or static storage duration and without
calling functions passed to `atexit()` ([[basic.start.term]]). The
function `_Exit` is signal-safe ([[csignal.syn]]).

``` cpp
[[noreturn]] void abort() noexcept;
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* The program is terminated without executing destructors for
objects of automatic, thread, or static storage duration and without
calling functions passed to `atexit()` ([[basic.start.term]]). The
function `abort` is signal-safe ([[csignal.syn]]).

``` cpp
int atexit(c-atexit-handler* f) noexcept;
int atexit(atexit-handler* f) noexcept;
```

*Effects:* The `atexit()` functions register the function pointed to by
`f` to be called without arguments at normal program termination. It is
unspecified whether a call to `atexit()` that does not happen
before ([[intro.multithread]]) a call to `exit()` will succeed.

[*Note 1*: The `atexit()` functions do not introduce a data
race ([[res.on.data.races]]). — *end note*]

*Implementation limits:* The implementation shall support the
registration of at least 32 functions.

*Returns:* The `atexit()` function returns zero if the registration
succeeds, nonzero if it fails.

``` cpp
[[noreturn]] void exit(int status);
```

*Effects:*

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
  *implementation-defined*.[^32]

``` cpp
int at_quick_exit(c-atexit-handler* f) noexcept;
int at_quick_exit(atexit-handler* f) noexcept;
```

*Effects:* The `at_quick_exit()` functions register the function pointed
to by `f` to be called without arguments when `quick_exit` is called. It
is unspecified whether a call to `at_quick_exit()` that does not happen
before ([[intro.multithread]]) all calls to `quick_exit` will succeed.

[*Note 2*: The `at_quick_exit()` functions do not introduce a data
race ([[res.on.data.races]]). — *end note*]

[*Note 3*: The order of registration may be indeterminate if
`at_quick_exit` was called from more than one thread. — *end note*]

[*Note 4*: The `at_quick_exit` registrations are distinct from the
`atexit` registrations, and applications may need to call both
registration functions with the same argument. — *end note*]

*Implementation limits:* The implementation shall support the
registration of at least 32 functions.

*Returns:* Zero if the registration succeeds, nonzero if it fails.

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

[*Note 5*: A function registered via `at_quick_exit` is invoked by the
thread that calls `quick_exit`, which can be a different thread than the
one that registered it, so registered functions should not rely on the
identity of objects with thread storage duration. — *end note*]

After calling registered functions, `quick_exit` shall call
`_Exit(status)`.

[*Note 6*: The standard file buffers are not flushed. — *end note*]

*Remarks:* The function `quick_exit` is signal-safe ([[csignal.syn]])
when the functions registered with `at_quick_exit` are.

  [[basic.start]], [[basic.start.term]], ISO C 7.22.4.

## Dynamic memory management <a id="support.dynamic">[[support.dynamic]]</a>

The header `<new>` defines several functions that manage the allocation
of dynamic storage in a program. It also defines components for
reporting storage management errors.

### Header `<new>` synopsis <a id="new.syn">[[new.syn]]</a>

``` cpp
namespace std {
  class bad_alloc;
  class bad_array_new_length;
  enum class align_val_t : size_t {};
  struct nothrow_t { explicit nothrow_t() = default; };
  extern const nothrow_t nothrow;
  using new_handler = void (*)();
  new_handler get_new_handler() noexcept;
  new_handler set_new_handler(new_handler new_p) noexcept;

  // [ptr.launder], pointer optimization barrier
  template <class T> constexpr T* launder(T* p) noexcept;

  // [hardware.interference], hardware interference size
  inline constexpr size_t hardware_destructive_interference_size = implementation-defined{};
  inline constexpr size_t hardware_constructive_interference_size = implementation-defined{};
}

void* operator new(std::size_t size);
void* operator new(std::size_t size, std::align_val_t alignment);
void* operator new(std::size_t size, const std::nothrow_t&) noexcept;
void* operator new(std::size_t size, std::align_val_t alignment,
                   const std::nothrow_t&) noexcept;
void  operator delete(void* ptr) noexcept;
void  operator delete(void* ptr, std::size_t size) noexcept;
void  operator delete(void* ptr, std::align_val_t alignment) noexcept;
void  operator delete(void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
void  operator delete(void* ptr, const std::nothrow_t&) noexcept;
void  operator delete(void* ptr, std::align_val_t alignment,
                      const std::nothrow_t&) noexcept;
void* operator new[](std::size_t size);
void* operator new[](std::size_t size, std::align_val_t alignment);
void* operator new[](std::size_t size, const std::nothrow_t&) noexcept;
void* operator new[](std::size_t size, std::align_val_t alignment,
                     const std::nothrow_t&) noexcept;
void  operator delete[](void* ptr) noexcept;
void  operator delete[](void* ptr, std::size_t size) noexcept;
void  operator delete[](void* ptr, std::align_val_t alignment) noexcept;
void  operator delete[](void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
void  operator delete[](void* ptr, const std::nothrow_t&) noexcept;
void  operator delete[](void* ptr, std::align_val_t alignment,
                        const std::nothrow_t&) noexcept;

void* operator new  (std::size_t size, void* ptr) noexcept;
void* operator new[](std::size_t size, void* ptr) noexcept;
void  operator delete  (void* ptr, void*) noexcept;
void  operator delete[](void* ptr, void*) noexcept;
```

  [[intro.memory]], [[basic.stc.dynamic]], [[expr.new]],
[[expr.delete]], [[class.free]], [[memory]].

### Storage allocation and deallocation <a id="new.delete">[[new.delete]]</a>

Except where otherwise specified, the provisions of 
[[basic.stc.dynamic]] apply to the library versions of `operator new`
and `operator
delete`. If the value of an alignment argument passed to any of these
functions is not a valid alignment value, the behavior is undefined.

#### Single-object forms <a id="new.delete.single">[[new.delete.single]]</a>

``` cpp
void* operator new(std::size_t size);
void* operator new(std::size_t size, std::align_val_t alignment);
```

*Effects:* The allocation functions ([[basic.stc.dynamic.allocation]])
called by a *new-expression* ([[expr.new]]) to allocate `size` bytes of
storage. The second form is called for a type with new-extended
alignment, and allocates storage with the specified alignment. The first
form is called otherwise, and allocates storage suitably aligned to
represent any object of that size provided the object’s type does not
have new-extended alignment.

*Replaceable:* A C++program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage ([[basic.stc.dynamic]]), or else throw a `bad_alloc` exception.
This requirement is binding on any replacement versions of these
functions.

*Default behavior:*

- Executes a loop: Within the loop, the function first attempts to
  allocate the requested storage. Whether the attempt involves a call to
  the C standard library functions `malloc` or `aligned_alloc` is
  unspecified.
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
void* operator new(std::size_t size, std::align_val_t alignment, const std::nothrow_t&) noexcept;
```

*Effects:* Same as above, except that these are called by a placement
version of a *new-expression* when a C++program prefers a null pointer
result as an error indication, instead of a `bad_alloc` exception.

*Replaceable:* A C++program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage ([[basic.stc.dynamic]]), or else return a null pointer. Each of
these nothrow versions of `operator new` returns a pointer obtained as
if acquired from the (possibly replaced) corresponding non-placement
function. This requirement is binding on any replacement versions of
these functions.

*Default behavior:* Calls `operator new(size)`, or
`operator new(size, alignment)`, respectively. If the call returns
normally, returns the result of that call. Otherwise, returns a null
pointer.

[*Example 1*:

``` cpp
T* p1 = new T;                  // throws bad_alloc if it fails
T* p2 = new(nothrow) T;         // returns nullptr if it fails
```

— *end example*]

``` cpp
void operator delete(void* ptr) noexcept;
void operator delete(void* ptr, std::size_t size) noexcept;
void operator delete(void* ptr, std::align_val_t alignment) noexcept;
void operator delete(void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
```

*Effects:* The deallocation
functions ([[basic.stc.dynamic.deallocation]]) called by a
*delete-expression* to render the value of `ptr` invalid.

*Replaceable:* A C++program may define functions with any of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

If a function without a `size` parameter is defined, the program should
also define the corresponding function with a `size` parameter. If a
function with a `size` parameter is defined, the program shall also
define the corresponding version without the `size` parameter.

[*Note 1*: The default behavior below may change in the future, which
will require replacing both deallocation functions when replacing the
allocation function. — *end note*]

*Requires:* `ptr` shall be a null pointer or its value shall represent
the address of a block of memory allocated by an earlier call to a
(possibly replaced) `operator new(std::size_t)` or
`operator new(std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete`.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Requires:* If the `alignment` parameter is not present, `ptr` shall
have been returned by an allocation function without an `alignment`
parameter. If present, the `alignment` argument shall equal the
`alignment` argument passed to the allocation function that returned
`ptr`. If present, the `size` argument shall equal the `size` argument
passed to the allocation function that returned `ptr`.

*Required behavior:* A call to an `operator delete` with a `size`
parameter may be changed to a call to the corresponding
`operator delete` without a `size` parameter, without affecting memory
allocation.

[*Note 2*: A conforming implementation is for
`operator delete(void* ptr, std::size_t size)` to simply call
`operator delete(ptr)`. — *end note*]

*Default behavior:* The functions that have a `size` parameter forward
their other parameters to the corresponding function without a `size`
parameter.

[*Note 3*: See the note in the above *Replaceable:*
paragraph. — *end note*]

*Default behavior:* If `ptr` is null, does nothing. Otherwise, reclaims
the storage allocated by the earlier call to `operator new`.

*Remarks:* It is unspecified under what conditions part or all of such
reclaimed storage will be allocated by subsequent calls to
`operator new` or any of `aligned_alloc`, `calloc`, `malloc`, or
`realloc`, declared in `<cstdlib>`.

``` cpp
void operator delete(void* ptr, const std::nothrow_t&) noexcept;
void operator delete(void* ptr, std::align_val_t alignment, const std::nothrow_t&) noexcept;
```

*Effects:* The deallocation
functions ([[basic.stc.dynamic.deallocation]]) called by the
implementation to render the value of `ptr` invalid when the constructor
invoked from a nothrow placement version of the *new-expression* throws
an exception.

*Replaceable:* A C++program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

*Requires:* `ptr` shall be a null pointer or its value shall represent
the address of a block of memory allocated by an earlier call to a
(possibly replaced) `operator new(std::size_t)` or
`operator new(std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete`.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Requires:* If the `alignment` parameter is not present, `ptr` shall
have been returned by an allocation function without an `alignment`
parameter. If present, the `alignment` argument shall equal the
`alignment` argument passed to the allocation function that returned
`ptr`.

*Default behavior:* Calls `operator delete(ptr)`, or
`operator delete(ptr, alignment)`, respectively.

#### Array forms <a id="new.delete.array">[[new.delete.array]]</a>

``` cpp
void* operator new[](std::size_t size);
void* operator new[](std::size_t size, std::align_val_t alignment);
```

*Effects:* The allocation functions ([[basic.stc.dynamic.allocation]])
called by the array form of a *new-expression* ([[expr.new]]) to
allocate `size` bytes of storage. The second form is called for a type
with new-extended alignment, and allocates storage with the specified
alignment. The first form is called otherwise, and allocates storage
suitably aligned to represent any array object of that size or smaller,
provided the object’s type does not have new-extended alignment. [^33]

*Replaceable:* A C++program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

*Required behavior:* Same as for the corresponding single-object forms.
This requirement is binding on any replacement versions of these
functions.

*Default behavior:* Returns `operator new(size)`, or
`operator new(size, alignment)`, respectively.

``` cpp
void* operator new[](std::size_t size, const std::nothrow_t&) noexcept;
void* operator new[](std::size_t size, std::align_val_t alignment, const std::nothrow_t&) noexcept;
```

*Effects:* Same as above, except that these are called by a placement
version of a *new-expression* when a C++program prefers a null pointer
result as an error indication, instead of a `bad_alloc` exception.

*Replaceable:* A C++program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage ([[basic.stc.dynamic]]), or else return a null pointer. Each of
these nothrow versions of `operator new[]` returns a pointer obtained as
if acquired from the (possibly replaced) corresponding non-placement
function. This requirement is binding on any replacement versions of
these functions.

*Default behavior:* Calls `operator new[](size)`, or
`operator new[](size, alignment)`, respectively. If the call returns
normally, returns the result of that call. Otherwise, returns a null
pointer.

``` cpp
void operator delete[](void* ptr) noexcept;
void operator delete[](void* ptr, std::size_t size) noexcept;
void operator delete[](void* ptr, std::align_val_t alignment) noexcept;
void operator delete[](void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
```

*Effects:* The deallocation
functions ([[basic.stc.dynamic.deallocation]]) called by the array form
of a *delete-expression* to render the value of `ptr` invalid.

*Replaceable:* A C++program may define functions with any of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

If a function without a `size` parameter is defined, the program should
also define the corresponding function with a `size` parameter. If a
function with a `size` parameter is defined, the program shall also
define the corresponding version without the `size` parameter.

[*Note 1*: The default behavior below may change in the future, which
will require replacing both deallocation functions when replacing the
allocation function. — *end note*]

*Requires:* `ptr` shall be a null pointer or its value shall represent
the address of a block of memory allocated by an earlier call to a
(possibly replaced) `operator new[](std::size_t)` or
`operator new[](std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete[]`.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Requires:* If the `alignment` parameter is not present, `ptr` shall
have been returned by an allocation function without an `alignment`
parameter. If present, the `alignment` argument shall equal the
`alignment` argument passed to the allocation function that returned
`ptr`. If present, the `size` argument shall equal the `size` argument
passed to the allocation function that returned `ptr`.

*Required behavior:* A call to an `operator delete[]` with a `size`
parameter may be changed to a call to the corresponding
`operator delete[]` without a `size` parameter, without affecting memory
allocation.

[*Note 2*: A conforming implementation is for
`operator delete[](void* ptr, std::size_t size)` to simply call
`operator delete[](ptr)`. — *end note*]

*Default behavior:* The functions that have a `size` parameter forward
their other parameters to the corresponding function without a `size`
parameter. The functions that do not have a `size` parameter forward
their parameters to the corresponding `operator delete` (single-object)
function.

``` cpp
void operator delete[](void* ptr, const std::nothrow_t&) noexcept;
void operator delete[](void* ptr, std::align_val_t alignment, const std::nothrow_t&) noexcept;
```

*Effects:* The deallocation
functions ([[basic.stc.dynamic.deallocation]]) called by the
implementation to render the value of `ptr` invalid when the constructor
invoked from a nothrow placement version of the array *new-expression*
throws an exception.

*Replaceable:* A C++program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++standard library.

*Requires:* `ptr` shall be a null pointer or its value shall represent
the address of a block of memory allocated by an earlier call to a
(possibly replaced) `operator new[](std::size_t)` or
`operator new[](std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete[]`.

*Requires:* If an implementation has strict pointer
safety ([[basic.stc.dynamic.safety]]) then `ptr` shall be a
safely-derived pointer.

*Requires:* If the `alignment` parameter is not present, `ptr` shall
have been returned by an allocation function without an `alignment`
parameter. If present, the `alignment` argument shall equal the
`alignment` argument passed to the allocation function that returned
`ptr`.

*Default behavior:* Calls `operator delete[](ptr)`, or
`operator delete[](ptr, alignment)`, respectively.

#### Non-allocating forms <a id="new.delete.placement">[[new.delete.placement]]</a>

These functions are reserved; a C++program may not define functions that
displace the versions in the C++standard library ([[constraints]]). The
provisions of  [[basic.stc.dynamic]] do not apply to these reserved
placement forms of `operator new` and `operator delete`.

``` cpp
void* operator new(std::size_t size, void* ptr) noexcept;
```

*Returns:* `ptr`.

*Remarks:* Intentionally performs no other action.

[*Example 1*:

This can be useful for constructing an object at a known address:

``` cpp
void* place = operator new(sizeof(Something));
Something* p = new (place) Something();
```

— *end example*]

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
in a placement *new-expression* that invokes the library’s non-array
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
in a placement *new-expression* that invokes the library’s array
placement operator new terminates by throwing an
exception ([[expr.new]]).

#### Data races <a id="new.delete.dataraces">[[new.delete.dataraces]]</a>

For purposes of determining the existence of data races, the library
versions of `operator new`, user replacement versions of global
`operator new`, the C standard library functions `aligned_alloc`,
`calloc`, and `malloc`, the library versions of `operator delete`, user
replacement versions of `operator delete`, the C standard library
function `free`, and the C standard library function `realloc` shall not
introduce a data race ([[res.on.data.races]]). Calls to these functions
that allocate or deallocate a particular unit of storage shall occur in
a single total order, and each such deallocation call shall happen
before ([[intro.multithread]]) the next allocation (if any) in this
order.

### Storage allocation errors <a id="alloc.errors">[[alloc.errors]]</a>

#### Class `bad_alloc` <a id="bad.alloc">[[bad.alloc]]</a>

``` cpp
namespace std {
  class bad_alloc : public exception {
  public:
    bad_alloc() noexcept;
    bad_alloc(const bad_alloc&) noexcept;
    bad_alloc& operator=(const bad_alloc&) noexcept;
    const char* what() const noexcept override;
  };
}
```

The class `bad_alloc` defines the type of objects thrown as exceptions
by the implementation to report a failure to allocate storage.

``` cpp
bad_alloc() noexcept;
```

*Effects:* Constructs an object of class `bad_alloc`.

``` cpp
bad_alloc(const bad_alloc&) noexcept;
bad_alloc& operator=(const bad_alloc&) noexcept;
```

*Effects:* Copies an object of class `bad_alloc`.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]]).

#### Class `bad_array_new_length` <a id="new.badlength">[[new.badlength]]</a>

``` cpp
namespace std {
  class bad_array_new_length : public bad_alloc {
  public:
    bad_array_new_length() noexcept;
    const char* what() const noexcept override;
  };
}
```

The class `bad_array_new_length` defines the type of objects thrown as
exceptions by the implementation to report an attempt to allocate an
array of size less than zero or greater than an *implementation-defined*
limit ([[expr.new]]).

``` cpp
bad_array_new_length() noexcept;
```

*Effects:* constructs an object of class `bad_array_new_length`.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]]).

#### Type `new_handler` <a id="new.handler">[[new.handler]]</a>

``` cpp
using new_handler = void (*)();
```

The type of a *handler function* to be called by `operator new()` or
`operator new[]()` ([[new.delete]]) when they cannot satisfy a request
for additional storage.

*Required behavior:* A `new_handler` shall perform one of the following:

- make more storage available for allocation and then return;
- throw an exception of type `bad_alloc` or a class derived from
  `bad_alloc`;
- terminate execution of the program without returning to the caller.

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

*Returns:* The current `new_handler`.

[*Note 1*: This may be a null pointer value. — *end note*]

### Pointer optimization barrier <a id="ptr.launder">[[ptr.launder]]</a>

``` cpp
template <class T> constexpr T* launder(T* p) noexcept;
```

*Requires:* `p` represents the address *A* of a byte in memory. An
object *X* that is within its lifetime ([[basic.life]]) and whose type
is similar ([[conv.qual]]) to `T` is located at the address *A*. All
bytes of storage that would be reachable through the result are
reachable through `p` (see below).

*Returns:* A value of type `T *` that points to `X`.

*Remarks:* An invocation of this function may be used in a core constant
expression whenever the value of its argument may be used in a core
constant expression. A byte of storage is reachable through a pointer
value that points to an object *Y* if it is within the storage occupied
by *Y*, an object that is pointer-interconvertible with *Y*, or the
immediately-enclosing array object if *Y* is an array element. The
program is ill-formed if `T` is a function type or cv `void`.

[*Note 1*: If a new object is created in storage occupied by an
existing object of the same type, a pointer to the original object can
be used to refer to the new object unless the type contains `const` or
reference members; in the latter cases, this function can be used to
obtain a usable pointer to the new object.
See  [[basic.life]]. — *end note*]

[*Example 1*:

``` cpp
struct X { const int n; };
X *p = new X{3};
const int a = p->n;
new (p) X{5};                       // p does not point to new object (REF:basic.life) because X::n is const
const int b = p->n;                 // undefined behavior
const int c = std::launder(p)->n;   // OK
```

— *end example*]

### Hardware interference size <a id="hardware.interference">[[hardware.interference]]</a>

``` cpp
inline constexpr size_t hardware_destructive_interference_size = implementation-defined{};
```

This number is the minimum recommended offset between two
concurrently-accessed objects to avoid additional performance
degradation due to contention introduced by the implementation. It shall
be at least `alignof(max_align_t)`.

[*Example 1*:

``` cpp
struct keep_apart {
  alignas(hardware_destructive_interference_size) atomic<int> cat;
  alignas(hardware_destructive_interference_size) atomic<int> dog;
};
```

— *end example*]

``` cpp
inline constexpr size_t hardware_constructive_interference_size = implementation-defined{};
```

This number is the maximum recommended size of contiguous memory
occupied by two objects accessed with temporal locality by concurrent
threads. It shall be at least `alignof(max_align_t)`.

[*Example 2*:

``` cpp
struct together {
  atomic<int> dog;
  int puppy;
};
struct kennel {
  // Other data members...
  alignas(sizeof(together)) together pack;
  // Other data members...
};
static_assert(sizeof(together) <= hardware_constructive_interference_size);
```

— *end example*]

## Type identification <a id="support.rtti">[[support.rtti]]</a>

The header `<typeinfo>` defines a type associated with type information
generated by the implementation. It also defines two types for reporting
dynamic type identification errors.

### Header `<typeinfo>` synopsis <a id="typeinfo.syn">[[typeinfo.syn]]</a>

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

    type_info(const type_info& rhs) = delete;                   // cannot be copied
    type_info& operator=(const type_info& rhs) = delete;        // cannot be copied
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

*Remarks:* An implementation should return different values for two
`type_info` objects which do not compare equal.

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
    const char* what() const noexcept override;
  };
}
```

The class `bad_cast` defines the type of objects thrown as exceptions by
the implementation to report the execution of an invalid `dynamic_cast`
expression ([[expr.dynamic.cast]]).

``` cpp
bad_cast() noexcept;
```

*Effects:* Constructs an object of class `bad_cast`.

``` cpp
bad_cast(const bad_cast&) noexcept;
bad_cast& operator=(const bad_cast&) noexcept;
```

*Effects:* Copies an object of class `bad_cast`.

``` cpp
const char* what() const noexcept override;
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
    const char* what() const noexcept override;
  };
}
```

The class `bad_typeid` defines the type of objects thrown as exceptions
by the implementation to report a null pointer in a `typeid`
expression ([[expr.typeid]]).

``` cpp
bad_typeid() noexcept;
```

*Effects:* Constructs an object of class `bad_typeid`.

``` cpp
bad_typeid(const bad_typeid&) noexcept;
bad_typeid& operator=(const bad_typeid&) noexcept;
```

*Effects:* Copies an object of class `bad_typeid`.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]])

## Exception handling <a id="support.exception">[[support.exception]]</a>

The header `<exception>` defines several types and functions related to
the handling of exceptions in a C++program.

### Header `<exception>` synopsis <a id="exception.syn">[[exception.syn]]</a>

``` cpp
namespace std {
  class exception;
  class bad_exception;
  class nested_exception;

  using terminate_handler = void (*)();
  terminate_handler get_terminate() noexcept;
  terminate_handler set_terminate(terminate_handler f) noexcept;
  [[noreturn]] void terminate() noexcept;

  int uncaught_exceptions() noexcept;

  using exception_ptr = unspecified;

  exception_ptr current_exception() noexcept;
  [[noreturn]] void rethrow_exception(exception_ptr p);
  template<class E> exception_ptr make_exception_ptr(E e) noexcept;

  template <class T> [[noreturn]] void throw_with_nested(T&& t);
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

``` cpp
exception(const exception& rhs) noexcept;
exception& operator=(const exception& rhs) noexcept;
```

*Effects:* Copies an `exception` object.

*Postconditions:* If `*this` and `rhs` both have dynamic type
`exception` then the value of the expression
`strcmp(what(), rhs.what())` shall equal 0.

``` cpp
virtual ~exception();
```

*Effects:* Destroys an object of class `exception`.

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
    const char* what() const noexcept override;
  };
}
```

The class `bad_exception` defines the type of the object referenced by
the `exception_ptr` returned from a call to `current_exception` (
[[propagation]]) when the currently active exception object fails to
copy.

``` cpp
bad_exception() noexcept;
```

*Effects:* Constructs an object of class `bad_exception`.

``` cpp
bad_exception(const bad_exception&) noexcept;
bad_exception& operator=(const bad_exception&) noexcept;
```

*Effects:* Copies an object of class `bad_exception`.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a `wstring` ([[string.classes]], [[locale.codecvt]]).

### Abnormal termination <a id="exception.terminate">[[exception.terminate]]</a>

#### Type `terminate_handler` <a id="terminate.handler">[[terminate.handler]]</a>

``` cpp
using terminate_handler = void (*)();
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

*Returns:* The current `terminate_handler`.

[*Note 1*: This may be a null pointer value. — *end note*]

#### `terminate` <a id="terminate">[[terminate]]</a>

``` cpp
[[noreturn]] void terminate() noexcept;
```

*Remarks:* Called by the implementation when exception handling must be
abandoned for any of several reasons ([[except.terminate]]). May also
be called directly by the program.

*Effects:* Calls a `terminate_handler` function. It is unspecified which
`terminate_handler` function will be called if an exception is active
during a call to `set_terminate`. Otherwise calls the current
`terminate_handler` function.

[*Note 1*: A default `terminate_handler` is always considered a
callable handler in this context. — *end note*]

### `uncaught_exceptions` <a id="uncaught.exceptions">[[uncaught.exceptions]]</a>

``` cpp
int uncaught_exceptions() noexcept;
```

*Returns:* The number of uncaught exceptions ([[except.uncaught]]).

*Remarks:* When `uncaught_exceptions() > 0`, throwing an exception can
result in a call of  
`std::terminate()` ([[except.terminate]]).

### Exception propagation <a id="propagation">[[propagation]]</a>

``` cpp
using exception_ptr = unspecified;
```

The type `exception_ptr` can be used to refer to an exception object.

`exception_ptr` shall satisfy the requirements of
`NullablePointer` ([[nullablepointer.requirements]]).

Two non-null values of type `exception_ptr` are equivalent and compare
equal if and only if they refer to the same exception.

The default constructor of `exception_ptr` produces the null value of
the type.

`exception_ptr` shall not be implicitly convertible to any arithmetic,
enumeration, or pointer type.

[*Note 1*: An implementation might use a reference-counted smart
pointer as `exception_ptr`. — *end note*]

For purposes of determining the presence of a data race, operations on
`exception_ptr` objects shall access and modify only the `exception_ptr`
objects themselves and not the exceptions they refer to. Use of
`rethrow_exception` on `exception_ptr` objects that refer to the same
exception object shall not introduce a data race.

[*Note 2*: If `rethrow_exception` rethrows the same exception object
(rather than a copy), concurrent access to that rethrown exception
object may introduce a data race. Changes in the number of
`exception_ptr` objects that refer to a particular exception do not
introduce a data race. — *end note*]

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
`current_exception` refer to the same exception object.

[*Note 3*: That is, it is unspecified whether `current_exception`
creates a new copy each time it is called. — *end note*]

If the attempt to copy the current exception object throws an exception,
the function returns an `exception_ptr` object that refers to the thrown
exception or, if this is not possible, to an instance of
`bad_exception`.

[*Note 4*: The copy constructor of the thrown exception may also fail,
so the implementation is allowed to substitute a `bad_exception` object
to avoid infinite recursion. — *end note*]

``` cpp
[[noreturn]] void rethrow_exception(exception_ptr p);
```

*Requires:* `p` shall not be a null pointer.

*Throws:* The exception object to which `p` refers.

``` cpp
template<class E> exception_ptr make_exception_ptr(E e) noexcept;
```

*Effects:* Creates an `exception_ptr` object that refers to a copy of
`e`, as if:

``` cpp
try {
  throw e;
} catch(...) {
  return current_exception();
}
```

[*Note 5*: This function is provided for convenience and efficiency
reasons. — *end note*]

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

  template<class T> [[noreturn]] void throw_with_nested(T&& t);
  template <class E> void rethrow_if_nested(const E& e);
}
```

The class `nested_exception` is designed for use as a mixin through
multiple inheritance. It captures the currently handled exception and
stores it for later use.

[*Note 1*: `nested_exception` has a virtual destructor to make it a
polymorphic class. Its presence can be tested for with
`dynamic_cast`. — *end note*]

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
template <class T> [[noreturn]] void throw_with_nested(T&& t);
```

Let `U` be `decay_t<T>`.

*Requires:* `U` shall be `CopyConstructible`.

*Throws:* If
`is_class_v<U> && !is_final_v<U> && !is_base_of_v<nested_exception, U>`
is `true`, an exception of unspecified type that is publicly derived
from both `U` and `nested_exception` and constructed from
`std::forward<T>(t)`, otherwise `std::forward<T>(t)`.

``` cpp
template <class E> void rethrow_if_nested(const E& e);
```

*Effects:* If `E` is not a polymorphic class type, or if
`nested_exception` is an inaccessible or ambiguous base class of `E`,
there is no effect. Otherwise, performs:

``` cpp
if (auto p = dynamic_cast<const nested_exception*>(addressof(e)))
  p->rethrow_nested();
```

## Initializer lists <a id="support.initlist">[[support.initlist]]</a>

The header `<initializer_list>` defines a class template and several
support functions related to list-initialization (see
[[dcl.init.list]]). All functions specified in this subclause are
signal-safe ([[csignal.syn]]).

### Header `<initializer_list>` synopsis <a id="initializer_list.syn">[[initializer_list.syn]]</a>

``` cpp
namespace std {
  template<class E> class initializer_list {
  public:
    using value_type      = E;
    using reference       = const E&;
    using const_reference = const E&;
    using size_type       = size_t;

    using iterator        = const E*;
    using const_iterator  = const E*;

    constexpr initializer_list() noexcept;

    constexpr size_t size() const noexcept;     // number of elements
    constexpr const E* begin() const noexcept;  // first element
    constexpr const E* end() const noexcept;    // one past the last element
  };

  // [support.initlist.range], initializer list range access
  template<class E> constexpr const E* begin(initializer_list<E> il) noexcept;
  template<class E> constexpr const E* end(initializer_list<E> il) noexcept;
}
```

An object of type `initializer_list<E>` provides access to an array of
objects of type `const E`.

[*Note 1*: A pair of pointers or a pointer plus a length would be
obvious representations for `initializer_list`. `initializer_list` is
used to implement initializer lists as specified in  [[dcl.init.list]].
Copying an initializer list does not copy the underlying
elements. — *end note*]

If an explicit specialization or partial specialization of
`initializer_list` is declared, the program is ill-formed.

### Initializer list constructors <a id="support.initlist.cons">[[support.initlist.cons]]</a>

``` cpp
constexpr initializer_list() noexcept;
```

*Effects:* Constructs an empty `initializer_list` object.

*Postconditions:* `size() == 0`.

### Initializer list access <a id="support.initlist.access">[[support.initlist.access]]</a>

``` cpp
constexpr const E* begin() const noexcept;
```

*Returns:* A pointer to the beginning of the array. If `size() == 0` the
values of `begin()` and `end()` are unspecified but they shall be
identical.

``` cpp
constexpr const E* end() const noexcept;
```

*Returns:* `begin() + size()`.

``` cpp
constexpr size_t size() const noexcept;
```

*Returns:* The number of elements in the array.

*Complexity:* Constant time.

### Initializer list range access <a id="support.initlist.range">[[support.initlist.range]]</a>

``` cpp
template<class E> constexpr const E* begin(initializer_list<E> il) noexcept;
```

*Returns:* `il.begin()`.

``` cpp
template<class E> constexpr const E* end(initializer_list<E> il) noexcept;
```

*Returns:* `il.end()`.

## Other runtime support <a id="support.runtime">[[support.runtime]]</a>

Headers `<csetjmp>` (nonlocal jumps), `<csignal>` (signal handling),
`<cstdarg>` (variable arguments), and `<cstdlib>` (runtime environment
`getenv, system`), provide further compatibility with C code.

Calls to the function `getenv` ([[cstdlib.syn]]) shall not introduce a
data race ([[res.on.data.races]]) provided that nothing modifies the
environment.

[*Note 1*: Calls to the POSIX functions `setenv` and `putenv` modify
the environment. — *end note*]

A call to the `setlocale` function ([[c.locales]]) may introduce a data
race with other calls to the `setlocale` function or with calls to
functions that are affected by the current C locale. The implementation
shall behave as if no library function other than `locale::global` calls
the `setlocale` function.

### Header `<cstdarg>` synopsis <a id="cstdarg.syn">[[cstdarg.syn]]</a>

``` cpp
namespace std {
  using va_list = see below;
}

#define va_arg(V, P) see below
#define va_copy(VDST, VSRC) see below
#define va_end(V) see below
#define va_start(V, P) see below
```

The contents of the header `<cstdarg>` are the same as the C standard
library header `<stdarg.h>`, with the following changes: The
restrictions that ISO C places on the second parameter to the `va_start`
macro in header `<stdarg.h>` are different in this International
Standard. The parameter `parmN` is the rightmost parameter in the
variable parameter list of the function definition (the one just before
the `...`).[^34] If the parameter `parmN` is a pack expansion (
[[temp.variadic]]) or an entity resulting from a lambda capture (
[[expr.prim.lambda]]), the program is ill-formed, no diagnostic
required. If the parameter `parmN` is of a reference type, or of a type
that is not compatible with the type that results when passing an
argument for which there is no parameter, the behavior is undefined.

ISO C 7.16.1.1.

### Header `<csetjmp>` synopsis <a id="csetjmp.syn">[[csetjmp.syn]]</a>

``` cpp
namespace std {
  using jmp_buf = see below;
  [[noreturn]] void longjmp(jmp_buf env, int val);
}

#define setjmp(env) see below
```

The contents of the header `<csetjmp>` are the same as the C standard
library header `<setjmp.h>`.

The function signature `longjmp(jmp_buf jbuf, int val)` has more
restricted behavior in this International Standard. A `setjmp`/`longjmp`
call pair has undefined behavior if replacing the `setjmp` and `longjmp`
by `catch` and `throw` would invoke any non-trivial destructors for any
automatic objects.

ISO C 7.13.

### Header `<csignal>` synopsis <a id="csignal.syn">[[csignal.syn]]</a>

``` cpp
namespace std {
  using sig_atomic_t = see below;

  // [support.signal], signal handlers
  extern "C" using signal-handler = void(int);  // exposition only
  signal-handler* signal(int sig, signal-handler* func);

  int raise(int sig);
}

#define SIG_DFL see below
#define SIG_ERR see below
#define SIG_IGN see below
#define SIGABRT see below
#define SIGFPE see below
#define SIGILL see below
#define SIGINT see below
#define SIGSEGV see below
#define SIGTERM see below
```

The contents of the header `<csignal>` are the same as the C standard
library header `<signal.h>`.

### Signal handlers <a id="support.signal">[[support.signal]]</a>

A call to the function `signal` synchronizes with any resulting
invocation of the signal handler so installed.

A *plain lock-free atomic operation* is an invocation of a function `f`
from Clause  [[atomics]], such that:

- `f` is the function `atomic_is_lock_free()`, or
- `f` is the member function `is_lock_free()`, or
- `f` is a non-static member function invoked on an object `A`, such
  that `A.is_lock_free()` yields `true`, or
- `f` is a non-member function, and for every pointer-to-atomic argument
  `A` passed to `f`, `atomic_is_lock_free(A)` yields `true`.

An evaluation is *signal-safe* unless it includes one of the following:

- a call to any standard library function, except for plain lock-free
  atomic operations and functions explicitly identified as signal-safe.
  \[*Note 1*: This implicitly excludes the use of `new` and `delete`
  expressions that rely on a library-provided memory
  allocator. — *end note*]
- an access to an object with thread storage duration;
- a `dynamic_cast` expression;
- throwing of an exception;
- control entering a *try-block* or *function-try-block*;
- initialization of a variable with static storage duration requiring
  dynamic initialization ([[basic.start.dynamic]], [[stmt.dcl]]) [^35];
  or
- waiting for the completion of the initialization of a variable with
  static storage duration ([[stmt.dcl]]).

A signal handler invocation has undefined behavior if it includes an
evaluation that is not signal-safe.

The function `signal` is signal-safe if it is invoked with the first
argument equal to the signal number corresponding to the signal that
caused the invocation of the handler.

ISO C 7.14.

<!-- Link reference definitions -->
[alg.c.library]: algorithms.md#alg.c.library
[alloc.errors]: #alloc.errors
[atomics]: atomics.md#atomics
[bad.alloc]: #bad.alloc
[bad.cast]: #bad.cast
[bad.exception]: #bad.exception
[bad.typeid]: #bad.typeid
[basic.align]: basic.md#basic.align
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.start]: basic.md#basic.start
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.term]: basic.md#basic.start.term
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[c.locales]: localization.md#c.locales
[c.malloc]: utilities.md#c.malloc
[c.math.abs]: numerics.md#c.math.abs
[c.math.rand]: numerics.md#c.math.rand
[c.mb.wcs]: strings.md#c.mb.wcs
[cfloat.syn]: #cfloat.syn
[class]: class.md#class
[class.free]: special.md#class.free
[climits.syn]: #climits.syn
[complex]: numerics.md#complex
[constraints]: library.md#constraints
[conv.ptr]: conv.md#conv.ptr
[conv.qual]: conv.md#conv.qual
[conv.rank]: conv.md#conv.rank
[csetjmp.syn]: #csetjmp.syn
[csignal.syn]: #csignal.syn
[cstdarg.syn]: #cstdarg.syn
[cstddef.syn]: #cstddef.syn
[cstdint]: #cstdint
[cstdint.syn]: #cstdint.syn
[cstdlib.syn]: #cstdlib.syn
[dcl.init.list]: dcl.md#dcl.init.list
[denorm.style]: #denorm.style
[except.handle]: except.md#except.handle
[except.nested]: #except.nested
[except.special]: except.md#except.special
[except.terminate]: except.md#except.terminate
[except.uncaught]: except.md#except.uncaught
[exception]: #exception
[exception.syn]: #exception.syn
[exception.terminate]: #exception.terminate
[expr.add]: expr.md#expr.add
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.new]: expr.md#expr.new
[expr.prim.lambda]: expr.md#expr.prim.lambda
[expr.sizeof]: expr.md#expr.sizeof
[expr.typeid]: expr.md#expr.typeid
[fp.style]: #fp.style
[get.new.handler]: #get.new.handler
[get.terminate]: #get.terminate
[hardware.interference]: #hardware.interference
[initializer_list.syn]: #initializer_list.syn
[intro.memory]: intro.md#intro.memory
[intro.multithread]: intro.md#intro.multithread
[language.support]: #language.support
[library.c]: library.md#library.c
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
[new.syn]: #new.syn
[nullablepointer.requirements]: library.md#nullablepointer.requirements
[numeric.limits]: #numeric.limits
[numeric.limits.members]: #numeric.limits.members
[numeric.special]: #numeric.special
[propagation]: #propagation
[ptr.launder]: #ptr.launder
[res.on.data.races]: library.md#res.on.data.races
[round.style]: #round.style
[set.new.handler]: #set.new.handler
[set.terminate]: #set.terminate
[stmt.dcl]: stmt.md#stmt.dcl
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
[support.signal]: #support.signal
[support.start.term]: #support.start.term
[support.types]: #support.types
[support.types.byteops]: #support.types.byteops
[support.types.layout]: #support.types.layout
[support.types.nullptr]: #support.types.nullptr
[tab:lang.sup.lib.summary]: #tab:lang.sup.lib.summary
[temp.dep.constexpr]: temp.md#temp.dep.constexpr
[temp.dep.expr]: temp.md#temp.dep.expr
[temp.variadic]: temp.md#temp.variadic
[terminate]: #terminate
[terminate.handler]: #terminate.handler
[type.info]: #type.info
[typeinfo.syn]: #typeinfo.syn
[uncaught.exceptions]: #uncaught.exceptions

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

[^11]: Rounding error is described in LIA-1 Section 5.2.4 and Annex C
    Rationale Section C.5.2.4 — Rounding and rounding constants.

[^12]: Equivalent to `FLT_MIN_EXP`, `DBL_MIN_EXP`, `LDBL_MIN_EXP`.

[^13]: Equivalent to `FLT_MIN_10_EXP`, `DBL_MIN_10_EXP`,
    `LDBL_MIN_10_EXP`.

[^14]: Equivalent to `FLT_MAX_EXP`, `DBL_MAX_EXP`, `LDBL_MAX_EXP`.

[^15]: Equivalent to `FLT_MAX_10_EXP`, `DBL_MAX_10_EXP`,
    `LDBL_MAX_10_EXP`.

[^16]: Required by LIA-1.

[^17]: Required by LIA-1.

[^18]: Required by LIA-1.

[^19]: See ISO/IEC/IEEE 60559.

[^20]: Required by LIA-1.

[^21]: Required by LIA-1.

[^22]: Required by LIA-1.

[^23]: Required by LIA-1.

[^24]: ISO/IEC/IEEE 60559:2011 is the same as IEEE 754-2008.

[^25]: Required by LIA-1.

[^26]: Required by LIA-1.

[^27]: Required by LIA-1.

[^28]: Refer to ISO/IEC/IEEE 60559. Required by LIA-1.

[^29]: Equivalent to `FLT_ROUNDS`. Required by LIA-1.

[^30]: A function is called for every time it is registered.

[^31]: Objects with automatic storage duration are all destroyed in a
    program whose `main` function (@@REF:basic.start.main@@) contains no
    automatic objects and executes the call to `exit()`. Control can be
    transferred directly to such a `main` function by throwing an
    exception that is caught in `main`.

[^32]: The macros `EXIT_FAILURE` and `EXIT_SUCCESS` are defined in
    `<cstdlib>`.

[^33]: It is not the direct responsibility of `operator new[]` or
    `operator delete[]` to note the repetition count or element size of
    the array. Those operations are performed elsewhere in the array
    `new` and `delete` expressions. The array `new` expression, may,
    however, increase the `size` argument to `operator new[]` to obtain
    space to store supplemental information.

[^34]: Note that `va_start` is required to work as specified even if
    unary `operator&` is overloaded for the type of `parmN`.

[^35]: Such initialization might occur because it is the first odr-use (
    [[basic.def.odr]]) of that variable.
