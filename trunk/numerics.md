# Numerics library <a id="numerics">[[numerics]]</a>

## General <a id="numerics.general">[[numerics.general]]</a>

This Clause describes components that C++ programs may use to perform
seminumerical operations.

The following subclauses describe components for complex number types,
random number generation, numeric ( *n*-at-a-time) arrays, generalized
numeric algorithms, and mathematical constants and functions for
floating-point types, as summarized in [[numerics.summary]].

**Table: Numerics library summary**

| Subclause                |                                                 | Header                 |
| ------------------------ | ----------------------------------------------- | ---------------------- |
| [[numeric.requirements]] | Requirements                                    |                        |
| [[cfenv]]                | Floating-point environment                      | `<cfenv>`              |
| [[complex.numbers]]      | Complex numbers                                 | `<complex>`            |
| [[rand]]                 | Random number generation                        | `<random>`             |
| [[numarray]]             | Numeric arrays                                  | `<valarray>`           |
| [[c.math]]               | Mathematical functions for floating-point types | `<cmath>`, `<cstdlib>` |
| [[numbers]]              | Numbers                                         | `<numbers>`            |
| [[linalg]]               | Linear algebra                                  | `<linalg>`             |
| [[simd]]                 | Data-parallel types                             | `<simd>`               |


## Numeric type requirements <a id="numeric.requirements">[[numeric.requirements]]</a>

The `complex` and `valarray` components are parameterized by the type of
information they contain and manipulate. A C++ program shall instantiate
these components only with a numeric type. A *numeric type* is a
cv-unqualified object type `T` that meets the
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*,
*Cpp17CopyAssignable*, and *Cpp17Destructible* requirements
[[utility.arg.requirements]].[^1]

If any operation on `T` throws an exception the effects are undefined.

In addition, many member and related functions of `valarray<T>` can be
successfully instantiated and will exhibit well-defined behavior if and
only if `T` meets additional requirements specified for each such member
or related function.

[*Example 1*: It is valid to instantiate `valarray<complex>`, but
`operator>()` will not be successfully instantiated for
`valarray<complex>` operands, since `complex` does not have any ordering
operators. — *end example*]

## The floating-point environment <a id="cfenv">[[cfenv]]</a>

### Header `<cfenv>` synopsis <a id="cfenv.syn">[[cfenv.syn]]</a>

``` cpp
#define \libmacro{FE_ALL_EXCEPT} see below
#define \libmacro{FE_DIVBYZERO} see below    // optional
#define \libmacro{FE_INEXACT} see below      // optional
#define \libmacro{FE_INVALID} see below      // optional
#define \libmacro{FE_OVERFLOW} see below     // optional
#define \libmacro{FE_UNDERFLOW} see below    // optional

#define \libmacro{FE_DOWNWARD} see below     // optional
#define \libmacro{FE_TONEAREST} see below    // optional
#define \libmacro{FE_TOWARDZERO} see below   // optional
#define \libmacro{FE_UPWARD} see below       // optional

#define \libmacro{FE_DFL_ENV} see below

namespace std {
  // types
  using fenv_t    = object type;
  using fexcept_t = object type;

  // functions
  int feclearexcept(int except);
  int fegetexceptflag(fexcept_t* pflag, int except);
  int feraiseexcept(int except);
  int fesetexceptflag(const fexcept_t* pflag, int except);
  int fetestexcept(int except);

  int fegetround();
  int fesetround(int mode);

  int fegetenv(fenv_t* penv);
  int feholdexcept(fenv_t* penv);
  int fesetenv(const fenv_t* penv);
  int feupdateenv(const fenv_t* penv);
}
```

The contents and meaning of the header `<cfenv>` are a subset of the C
standard library header `<fenv.h>` and only the declarations shown in
the synopsis above are present.

[*Note 1*: This document does not require an implementation to support
the `FENV_ACCESS` pragma; it is *implementation-defined* [[cpp.pragma]]
whether the pragma is supported. As a consequence, it is
*implementation-defined* whether these functions can be used to test
floating-point status flags, set floating-point control modes, or run
under non-default mode settings. If the pragma is used to enable control
over the floating-point environment, this document does not specify the
effect on floating-point evaluation in constant
expressions. — *end note*]

### Threads <a id="cfenv.thread">[[cfenv.thread]]</a>

The floating-point environment has thread storage duration
[[basic.stc.thread]]. The initial state for a thread’s floating-point
environment is the state of the floating-point environment of the thread
that constructs the corresponding `thread` object
[[thread.thread.class]] or `jthread` object [[thread.jthread.class]] at
the time it constructed the object.

[*Note 1*: That is, the child thread gets the floating-point state of
the parent thread at the time of the child’s creation. — *end note*]

A separate floating-point environment is maintained for each thread.
Each function accesses the environment corresponding to its calling
thread.

## Complex numbers <a id="complex.numbers">[[complex.numbers]]</a>

### General <a id="complex.numbers.general">[[complex.numbers.general]]</a>

The header `<complex>` defines a class template, and numerous functions
for representing and manipulating complex numbers.

The effect of instantiating the primary template of `complex` for any
type that is not a cv-unqualified floating-point type
[[basic.fundamental]] is unspecified. Specializations of `complex` for
cv-unqualified floating-point types are trivially copyable literal types
[[term.literal.type]].

If the result of a function is not mathematically defined or not in the
range of representable values for its type, the behavior is undefined.

If `z` is an lvalue of type cv `complex<T>` then:

- the expression `reinterpret_cast<cv{} T(&)[2]>(z)` is well-formed,
- `reinterpret_cast<cv{} T(&)[2]>(z)[0]` designates the real part of
  `z`, and
- `reinterpret_cast<cv{} T(&)[2]>(z)[1]` designates the imaginary part
  of `z`.

Moreover, if `a` is an expression of type cv `complex<T>*` and the
expression `a[i]` is well-defined for an integer expression `i`, then:

- `reinterpret_cast<cv{} T*>(a)[2 * i]` designates the real part of
  `a[i]`, and
- `reinterpret_cast<cv{} T*>(a)[2 * i + 1]` designates the imaginary
  part of `a[i]`.

### Header `<complex>` synopsis <a id="complex.syn">[[complex.syn]]</a>

``` cpp
namespace std {
  // [complex], class template complex
  template<class T> class complex;

  // [complex.ops], operators
  template<class T> constexpr complex<T> operator+(const complex<T>&, const complex<T>&);
  template<class T> constexpr complex<T> operator+(const complex<T>&, const T&);
  template<class T> constexpr complex<T> operator+(const T&, const complex<T>&);

  template<class T> constexpr complex<T> operator-(const complex<T>&, const complex<T>&);
  template<class T> constexpr complex<T> operator-(const complex<T>&, const T&);
  template<class T> constexpr complex<T> operator-(const T&, const complex<T>&);

  template<class T> constexpr complex<T> operator*(const complex<T>&, const complex<T>&);
  template<class T> constexpr complex<T> operator*(const complex<T>&, const T&);
  template<class T> constexpr complex<T> operator*(const T&, const complex<T>&);

  template<class T> constexpr complex<T> operator/(const complex<T>&, const complex<T>&);
  template<class T> constexpr complex<T> operator/(const complex<T>&, const T&);
  template<class T> constexpr complex<T> operator/(const T&, const complex<T>&);

  template<class T> constexpr complex<T> operator+(const complex<T>&);
  template<class T> constexpr complex<T> operator-(const complex<T>&);

  template<class T> constexpr bool operator==(const complex<T>&, const complex<T>&);
  template<class T> constexpr bool operator==(const complex<T>&, const T&);

  template<class T, class charT, class traits>
    basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>&, complex<T>&);

  template<class T, class charT, class traits>
    basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>&, const complex<T>&);

  // [complex.value.ops], values
  template<class T> constexpr T real(const complex<T>&);
  template<class T> constexpr T imag(const complex<T>&);

  template<class T> constexpr T abs(const complex<T>&);
  template<class T> constexpr T arg(const complex<T>&);
  template<class T> constexpr T norm(const complex<T>&);

  template<class T> constexpr complex<T> conj(const complex<T>&);
  template<class T> constexpr complex<T> proj(const complex<T>&);
  template<class T> constexpr complex<T> polar(const T&, const T& = T());

  // [complex.transcendentals], transcendentals
  template<class T> constexpr complex<T> acos(const complex<T>&);
  template<class T> constexpr complex<T> asin(const complex<T>&);
  template<class T> constexpr complex<T> atan(const complex<T>&);

  template<class T> constexpr complex<T> acosh(const complex<T>&);
  template<class T> constexpr complex<T> asinh(const complex<T>&);
  template<class T> constexpr complex<T> atanh(const complex<T>&);

  template<class T> constexpr complex<T> cos  (const complex<T>&);
  template<class T> constexpr complex<T> cosh (const complex<T>&);
  template<class T> constexpr complex<T> exp  (const complex<T>&);
  template<class T> constexpr complex<T> log  (const complex<T>&);
  template<class T> constexpr complex<T> log10(const complex<T>&);

  template<class T> constexpr complex<T> pow  (const complex<T>&, const T&);
  template<class T> constexpr complex<T> pow  (const complex<T>&, const complex<T>&);
  template<class T> constexpr complex<T> pow  (const T&, const complex<T>&);

  template<class T> constexpr complex<T> sin  (const complex<T>&);
  template<class T> constexpr complex<T> sinh (const complex<T>&);
  template<class T> constexpr complex<T> sqrt (const complex<T>&);
  template<class T> constexpr complex<T> tan  (const complex<T>&);
  template<class T> constexpr complex<T> tanh (const complex<T>&);

  // [complex.tuple], tuple interface
  template<class T> struct tuple_size;
  template<size_t I, class T> struct tuple_element;
  template<class T> struct tuple_size<complex<T>>;
  template<size_t I, class T> struct tuple_element<I, complex<T>>;
  template<size_t I, class T>
    constexpr T& get(complex<T>&) noexcept;
  template<size_t I, class T>
    constexpr T&& get(complex<T>&&) noexcept;
  template<size_t I, class T>
    constexpr const T& get(const complex<T>&) noexcept;
  template<size_t I, class T>
    constexpr const T&& get(const complex<T>&&) noexcept;

  // [complex.literals], complex literals
  inline namespace literals {
    inline namespace complex_literals {
      constexpr complex<long double> operator""il(long double);
      constexpr complex<long double> operator""il(unsigned long long);
      constexpr complex<double> operator""i(long double);
      constexpr complex<double> operator""i(unsigned long long);
      constexpr complex<float> operator""if(long double);
      constexpr complex<float> operator""if(unsigned long long);
    }
  }
}
```

### Class template `complex` <a id="complex">[[complex]]</a>

``` cpp
namespace std {
  template<class T> class complex {
  public:
    using value_type = T;

    constexpr complex(const T& re = T(), const T& im = T());
    constexpr complex(const complex&) = default;
    template<class X> constexpr explicit(see below) complex(const complex<X>&);

    constexpr T real() const;
    constexpr void real(T);
    constexpr T imag() const;
    constexpr void imag(T);

    constexpr complex& operator= (const T&);
    constexpr complex& operator+=(const T&);
    constexpr complex& operator-=(const T&);
    constexpr complex& operator*=(const T&);
    constexpr complex& operator/=(const T&);

    constexpr complex& operator=(const complex&);
    template<class X> constexpr complex& operator= (const complex<X>&);
    template<class X> constexpr complex& operator+=(const complex<X>&);
    template<class X> constexpr complex& operator-=(const complex<X>&);
    template<class X> constexpr complex& operator*=(const complex<X>&);
    template<class X> constexpr complex& operator/=(const complex<X>&);
  };
}
```

The class `complex` describes an object that can store the Cartesian
components, `real()` and `imag()`, of a complex number.

### Member functions <a id="complex.members">[[complex.members]]</a>

``` cpp
constexpr complex(const T& re = T(), const T& im = T());
```

*Ensures:* `real() == re && imag() == im` is `true`.

``` cpp
template<class X> constexpr explicit(see below) complex(const complex<X>& other);
```

*Effects:* Initializes the real part with `other.real()` and the
imaginary part with `other.imag()`.

*Remarks:* The expression inside `explicit` evaluates to `false` if and
only if the floating-point conversion rank of `T` is greater than or
equal to the floating-point conversion rank of `X`.

``` cpp
constexpr T real() const;
```

*Returns:* The value of the real component.

``` cpp
constexpr void real(T val);
```

*Effects:* Assigns `val` to the real component.

``` cpp
constexpr T imag() const;
```

*Returns:* The value of the imaginary component.

``` cpp
constexpr void imag(T val);
```

*Effects:* Assigns `val` to the imaginary component.

### Member operators <a id="complex.member.ops">[[complex.member.ops]]</a>

``` cpp
constexpr complex& operator+=(const T& rhs);
```

*Effects:* Adds the scalar value `rhs` to the real part of the complex
value `*this` and stores the result in the real part of `*this`, leaving
the imaginary part unchanged.

*Returns:* `*this`.

``` cpp
constexpr complex& operator-=(const T& rhs);
```

*Effects:* Subtracts the scalar value `rhs` from the real part of the
complex value `*this` and stores the result in the real part of `*this`,
leaving the imaginary part unchanged.

*Returns:* `*this`.

``` cpp
constexpr complex& operator*=(const T& rhs);
```

*Effects:* Multiplies the scalar value `rhs` by the complex value
`*this` and stores the result in `*this`.

*Returns:* `*this`.

``` cpp
constexpr complex& operator/=(const T& rhs);
```

*Effects:* Divides the scalar value `rhs` into the complex value `*this`
and stores the result in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> constexpr complex& operator=(const complex<X>& rhs);
```

*Effects:* Assigns the value `rhs.real()` to the real part and the value
`rhs.imag()` to the imaginary part of the complex value `*this`.

*Returns:* `*this`.

``` cpp
template<class X> constexpr complex& operator+=(const complex<X>& rhs);
```

*Effects:* Adds the complex value `rhs` to the complex value `*this` and
stores the sum in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> constexpr complex& operator-=(const complex<X>& rhs);
```

*Effects:* Subtracts the complex value `rhs` from the complex value
`*this` and stores the difference in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> constexpr complex& operator*=(const complex<X>& rhs);
```

*Effects:* Multiplies the complex value `rhs` by the complex value
`*this` and stores the product in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> constexpr complex& operator/=(const complex<X>& rhs);
```

*Effects:* Divides the complex value `rhs` into the complex value
`*this` and stores the quotient in `*this`.

*Returns:* `*this`.

### Non-member operations <a id="complex.ops">[[complex.ops]]</a>

``` cpp
template<class T> constexpr complex<T> operator+(const complex<T>& lhs);
```

*Returns:* `complex<T>(lhs)`.

``` cpp
template<class T> constexpr complex<T> operator+(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator+(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator+(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) += rhs`.

``` cpp
template<class T> constexpr complex<T> operator-(const complex<T>& lhs);
```

*Returns:* `complex<T>(-lhs.real(),-lhs.imag())`.

``` cpp
template<class T> constexpr complex<T> operator-(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator-(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator-(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) -= rhs`.

``` cpp
template<class T> constexpr complex<T> operator*(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator*(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator*(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) *= rhs`.

``` cpp
template<class T> constexpr complex<T> operator/(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator/(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator/(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) /= rhs`.

``` cpp
template<class T> constexpr bool operator==(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr bool operator==(const complex<T>& lhs, const T& rhs);
```

*Returns:* `lhs.real() == rhs.real() && lhs.imag() == rhs.imag()`.

*Remarks:* The imaginary part is assumed to be `T()`, or 0.0, for the
`T` arguments.

``` cpp
template<class T, class charT, class traits>
  basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>& is, complex<T>& x);
```

*Preconditions:* The input values are convertible to `T`.

*Effects:* Extracts a complex number `x` of the form: `u`, `(u)`, or
`(u,v)`, where `u` is the real part and `v` is the imaginary
part [[istream.formatted]].

If bad input is encountered, calls `is.setstate(ios_base::failbit)`
(which may throw `ios_base::failure`[[iostate.flags]]).

*Returns:* `is`.

*Remarks:* This extraction is performed as a series of simpler
extractions. Therefore, the skipping of whitespace is specified to be
the same for each of the simpler extractions.

``` cpp
template<class T, class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& o, const complex<T>& x);
```

*Effects:* Inserts the complex number `x` onto the stream `o` as if it
were implemented as follows:

``` cpp
basic_ostringstream<charT, traits> s;
s.flags(o.flags());
s.imbue(o.getloc());
s.precision(o.precision());
s << '(' << x.real() << ',' << x.imag() << ')';
return o << s.str();
```

[*Note 1*: In a locale in which comma is used as a decimal point
character, the use of comma as a field separator can be ambiguous.
Inserting `showpoint` into the output stream forces all outputs to show
an explicit decimal point character; as a result, all inserted sequences
of complex numbers can be extracted unambiguously. — *end note*]

### Value operations <a id="complex.value.ops">[[complex.value.ops]]</a>

``` cpp
template<class T> constexpr T real(const complex<T>& x);
```

*Returns:* `x.real()`.

``` cpp
template<class T> constexpr T imag(const complex<T>& x);
```

*Returns:* `x.imag()`.

``` cpp
template<class T> constexpr T abs(const complex<T>& x);
```

*Returns:* The magnitude of `x`.

``` cpp
template<class T> constexpr T arg(const complex<T>& x);
```

*Returns:* The phase angle of `x`, or `atan2(imag(x), real(x))`.

``` cpp
template<class T> constexpr T norm(const complex<T>& x);
```

*Returns:* The squared magnitude of `x`.

``` cpp
template<class T> constexpr complex<T> conj(const complex<T>& x);
```

*Returns:* The complex conjugate of `x`.

``` cpp
template<class T> constexpr complex<T> proj(const complex<T>& x);
```

*Returns:* The projection of `x` onto the Riemann sphere.

*Remarks:* Behaves the same as the C function `cproj`.

``` cpp
template<class T> constexpr complex<T> polar(const T& rho, const T& theta = T());
```

*Preconditions:* `rho` is non-negative and non-NaN. `theta` is finite.

*Returns:* The `complex` value corresponding to a complex number whose
magnitude is `rho` and whose phase angle is `theta`.

### Transcendentals <a id="complex.transcendentals">[[complex.transcendentals]]</a>

``` cpp
template<class T> constexpr complex<T> acos(const complex<T>& x);
```

*Returns:* The complex arc cosine of `x`.

*Remarks:* Behaves the same as the C function `cacos`.

``` cpp
template<class T> constexpr complex<T> asin(const complex<T>& x);
```

*Returns:* The complex arc sine of `x`.

*Remarks:* Behaves the same as the C function `casin`.

``` cpp
template<class T> constexpr complex<T> atan(const complex<T>& x);
```

*Returns:* The complex arc tangent of `x`.

*Remarks:* Behaves the same as the C function `catan`.

``` cpp
template<class T> constexpr complex<T> acosh(const complex<T>& x);
```

*Returns:* The complex arc hyperbolic cosine of `x`.

*Remarks:* Behaves the same as the C function `cacosh`.

``` cpp
template<class T> constexpr complex<T> asinh(const complex<T>& x);
```

*Returns:* The complex arc hyperbolic sine of `x`.

*Remarks:* Behaves the same as the C function `casinh`.

``` cpp
template<class T> constexpr complex<T> atanh(const complex<T>& x);
```

*Returns:* The complex arc hyperbolic tangent of `x`.

*Remarks:* Behaves the same as the C function `catanh`.

``` cpp
template<class T> constexpr complex<T> cos(const complex<T>& x);
```

*Returns:* The complex cosine of `x`.

``` cpp
template<class T> constexpr complex<T> cosh(const complex<T>& x);
```

*Returns:* The complex hyperbolic cosine of `x`.

``` cpp
template<class T> constexpr complex<T> exp(const complex<T>& x);
```

*Returns:* The complex base-e exponential of `x`.

``` cpp
template<class T> constexpr complex<T> log(const complex<T>& x);
```

*Returns:* The complex natural (base-e) logarithm of `x`. For all `x`,
`imag(log(x))` lies in the interval \[-π, π\].

[*Note 1*: The semantics of this function are intended to be the same
in C++ as they are for `clog` in C. — *end note*]

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> constexpr complex<T> log10(const complex<T>& x);
```

*Returns:* The complex common (base-10) logarithm of `x`, defined as
`log(x) / log(10)`.

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> constexpr complex<T> pow(const complex<T>& x, const complex<T>& y);
template<class T> constexpr complex<T> pow(const complex<T>& x, const T& y);
template<class T> constexpr complex<T> pow(const T& x, const complex<T>& y);
```

*Returns:* The complex power of base `x` raised to the `y`ᵗʰ power,
defined as `exp(y * log(x))`. The value returned for `pow(0, 0)` is
*implementation-defined*.

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> constexpr complex<T> sin(const complex<T>& x);
```

*Returns:* The complex sine of `x`.

``` cpp
template<class T> constexpr complex<T> sinh(const complex<T>& x);
```

*Returns:* The complex hyperbolic sine of `x`.

``` cpp
template<class T> constexpr complex<T> sqrt(const complex<T>& x);
```

*Returns:* The complex square root of `x`, in the range of the right
half-plane.

[*Note 2*: The semantics of this function are intended to be the same
in C++ as they are for `csqrt` in C. — *end note*]

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> constexpr complex<T> tan(const complex<T>& x);
```

*Returns:* The complex tangent of `x`.

``` cpp
template<class T> constexpr complex<T> tanh(const complex<T>& x);
```

*Returns:* The complex hyperbolic tangent of `x`.

### Tuple interface <a id="complex.tuple">[[complex.tuple]]</a>

``` cpp
template<class T>
struct tuple_size<complex<T>> : integral_constant<size_t, 2> {};

template<size_t I, class T>
struct tuple_element<I, complex<T>> {
  using type = T;
};
```

*Mandates:* `I < 2` is `true`.

``` cpp
template<size_t I, class T>
  constexpr T& get(complex<T>& z) noexcept;
template<size_t I, class T>
  constexpr T&& get(complex<T>&& z) noexcept;
template<size_t I, class T>
  constexpr const T& get(const complex<T>& z) noexcept;
template<size_t I, class T>
  constexpr const T&& get(const complex<T>&& z) noexcept;
```

*Mandates:* `I < 2` is `true`.

*Returns:* A reference to the real part of `z` if `I == 0` is `true`,
otherwise a reference to the imaginary part of `z`.

### Additional overloads <a id="cmplx.over">[[cmplx.over]]</a>

The following function templates have additional constexpr overloads:

``` cpp
arg                   norm
conj                  proj
imag                  real
```

The additional constexpr overloads are sufficient to ensure:

- If the argument has a floating-point type `T`, then it is effectively
  cast to `complex<T>`.
- Otherwise, if the argument has integer type, then it is effectively
  cast to `complex<double>`.

Function template `pow` has additional constexpr overloads sufficient to
ensure, for a call with one argument of type `complex<T1>` and the other
argument of type `T2` or `complex<T2>`, both arguments are effectively
cast to `complex<common_type_t<T1, T3>>`, where `T3` is `double` if `T2`
is an integer type and `T2` otherwise. If `common_type_t<T1, T3>` is not
well-formed, then the program is ill-formed.

### Suffixes for complex number literals <a id="complex.literals">[[complex.literals]]</a>

This subclause describes literal suffixes for constructing complex
number literals. The suffixes `i`, `il`, and `if` create complex numbers
of the types `complex<double>`, `complex<long double>`, and
`complex<float>` respectively, with their imaginary part denoted by the
given literal number and the real part being zero.

``` cpp
constexpr complex<long double> operator""il(long double d);
constexpr complex<long double> operator""il(unsigned long long d);
```

*Returns:* `complex<long double>{0.0L, static_cast<long double>(d)}`.

``` cpp
constexpr complex<double> operator""i(long double d);
constexpr complex<double> operator""i(unsigned long long d);
```

*Returns:* `complex<double>{0.0, static_cast<double>(d)}`.

``` cpp
constexpr complex<float> operator""if(long double d);
constexpr complex<float> operator""if(unsigned long long d);
```

*Returns:* `complex<float>{0.0f, static_cast<float>(d)}`.

## Random number generation <a id="rand">[[rand]]</a>

### General <a id="rand.general">[[rand.general]]</a>

Subclause [[rand]] defines a facility for generating (pseudo-)random
numbers.

In addition to a few utilities, four categories of entities are
described: *uniform random bit generators*, *random number engines*,
*random number engine adaptors*, and *random number distributions*.
These categorizations are applicable to types that meet the
corresponding requirements, to objects instantiated from such types, and
to templates producing such types when instantiated.

[*Note 1*: These entities are specified in such a way as to permit the
binding of any uniform random bit generator object `e` as the argument
to any random number distribution object `d`, thus producing a
zero-argument function object such as given by
`bind(d,e)`. — *end note*]

Each of the entities specified in [[rand]] has an associated arithmetic
type [[basic.fundamental]] identified as `result_type`. With `T` as the
`result_type` thus associated with such an entity, that entity is
characterized:

- as *boolean* or equivalently as *boolean-valued*, if `T` is `bool`;
- otherwise as *integral* or equivalently as *integer-valued*, if
  `numeric_limits<T>::is_integer` is `true`;
- otherwise as *floating-point* or equivalently as *real-valued*.

If integer-valued, an entity may optionally be further characterized as
*signed* or *unsigned*, according to `numeric_limits<T>::is_signed`.

Unless otherwise specified, all descriptions of calculations in [[rand]]
use mathematical real numbers.

Throughout [[rand]], the operators , , and \xor denote the respective
conventional bitwise operations. Further:

- the operator \rightshift denotes a bitwise right shift with
  zero-valued bits appearing in the high bits of the result, and
- the operator denotes a bitwise left shift with zero-valued bits
  appearing in the low bits of the result, and whose result is always
  taken modulo 2ʷ.

### Header `<random>` synopsis <a id="rand.synopsis">[[rand.synopsis]]</a>

``` cpp
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [rand.req.urng], uniform random bit generator requirements
  template<class G>
    concept uniform_random_bit_generator = see below;           // freestanding

  // [rand.eng.lcong], class template linear_congruential_engine
  template<class UIntType, UIntType a, UIntType c, UIntType m>
    class linear_congruential_engine;                           // partially freestanding

  // [rand.eng.mers], class template mersenne_twister_engine
  template<class UIntType, size_t w, size_t n, size_t m, size_t r,
           UIntType a, size_t u, UIntType d, size_t s,
           UIntType b, size_t t,
           UIntType c, size_t l, UIntType f>
    class mersenne_twister_engine;

  // [rand.eng.sub], class template subtract_with_carry_engine
  template<class UIntType, size_t w, size_t s, size_t r>
    class subtract_with_carry_engine;                           // partially freestanding

  // [rand.adapt.disc], class template discard_block_engine
  template<class Engine, size_t p, size_t r>
    class discard_block_engine;                                 // partially freestanding

  // [rand.adapt.ibits], class template independent_bits_engine
  template<class Engine, size_t w, class UIntType>
    class independent_bits_engine;                              // partially freestanding

  // [rand.adapt.shuf], class template shuffle_order_engine
  template<class Engine, size_t k>
    class shuffle_order_engine;

  // [rand.eng.philox], class template philox_engine
  template<class UIntType, size_t w, size_t n, size_t r, UIntType... consts>
    class philox_engine;                                        // partially freestanding

  // [rand.predef], engines and engine adaptors with predefined parameters
  using minstd_rand0  = see below;      // freestanding
  using minstd_rand   = see below;      // freestanding
  using mt19937       = see below;      // freestanding
  using mt19937_64    = see below;      // freestanding
  using ranlux24_base = see below;      // freestanding
  using ranlux48_base = see below;      // freestanding
  using ranlux24      = see below;      // freestanding
  using ranlux48      = see below;      // freestanding
  using knuth_b       = see below;
  using philox4x32    = see below;      // freestanding
  using philox4x64    = see below;      // freestanding

  using default_random_engine = see below;

  // [rand.device], class random_device
  class random_device;

  // [rand.util.seedseq], class seed_seq
  class seed_seq;

  // [rand.util.canonical], function template generate_canonical
  template<class RealType, size_t digits, class URBG>
    RealType generate_canonical(URBG& g);

  namespace ranges {
    // [alg.rand.generate], generate_random
    template<class R, class G>
      requires output_range<R, invoke_result_t<G&>> &&
               uniform_random_bit_generator<remove_cvref_t<G>>
      constexpr borrowed_iterator_t<R> generate_random(R&& r, G&& g);

    template<class G, output_iterator<invoke_result_t<G&>> O, sentinel_for<O> S>
      requires uniform_random_bit_generator<remove_cvref_t<G>>
      constexpr O generate_random(O first, S last, G&& g);

    template<class R, class G, class D>
      requires output_range<R, invoke_result_t<D&, G&>> && invocable<D&, G&> &&
               uniform_random_bit_generator<remove_cvref_t<G>> &&
               is_arithmetic_v<invoke_result_t<D&, G&>>
    constexpr borrowed_iterator_t<R> generate_random(R&& r, G&& g, D&& d);

    template<class G, class D, output_iterator<invoke_result_t<D&, G&>> O, sentinel_for<O> S>
      requires invocable<D&, G&> && uniform_random_bit_generator<remove_cvref_t<G>> &&
               is_arithmetic_v<invoke_result_t<D&, G&>>
    constexpr O generate_random(O first, S last, G&& g, D&& d);
  }

  // [rand.dist.uni.int], class template uniform_int_distribution
  template<class IntType = int>
    class uniform_int_distribution;                             // partially freestanding

  // [rand.dist.uni.real], class template uniform_real_distribution
  template<class RealType = double>
    class uniform_real_distribution;

  // [rand.dist.bern.bernoulli], class bernoulli_distribution
  class bernoulli_distribution;

  // [rand.dist.bern.bin], class template binomial_distribution
  template<class IntType = int>
    class binomial_distribution;

  // [rand.dist.bern.geo], class template geometric_distribution
  template<class IntType = int>
    class geometric_distribution;

  // [rand.dist.bern.negbin], class template negative_binomial_distribution
  template<class IntType = int>
    class negative_binomial_distribution;

  // [rand.dist.pois.poisson], class template poisson_distribution
  template<class IntType = int>
    class poisson_distribution;

  // [rand.dist.pois.exp], class template exponential_distribution
  template<class RealType = double>
    class exponential_distribution;

  // [rand.dist.pois.gamma], class template gamma_distribution
  template<class RealType = double>
    class gamma_distribution;

  // [rand.dist.pois.weibull], class template weibull_distribution
  template<class RealType = double>
    class weibull_distribution;

  // [rand.dist.pois.extreme], class template extreme_value_distribution
  template<class RealType = double>
    class extreme_value_distribution;

  // [rand.dist.norm.normal], class template normal_distribution
  template<class RealType = double>
    class normal_distribution;

  // [rand.dist.norm.lognormal], class template lognormal_distribution
  template<class RealType = double>
    class lognormal_distribution;

  // [rand.dist.norm.chisq], class template chi_squared_distribution
  template<class RealType = double>
    class chi_squared_distribution;

  // [rand.dist.norm.cauchy], class template cauchy_distribution
  template<class RealType = double>
    class cauchy_distribution;

  // [rand.dist.norm.f], class template fisher_f_distribution
  template<class RealType = double>
    class fisher_f_distribution;

  // [rand.dist.norm.t], class template student_t_distribution
  template<class RealType = double>
    class student_t_distribution;

  // [rand.dist.samp.discrete], class template discrete_distribution
  template<class IntType = int>
    class discrete_distribution;

  // [rand.dist.samp.pconst], class template piecewise_constant_distribution
  template<class RealType = double>
    class piecewise_constant_distribution;

  // [rand.dist.samp.plinear], class template piecewise_linear_distribution
  template<class RealType = double>
    class piecewise_linear_distribution;
}
```

### Requirements <a id="rand.req">[[rand.req]]</a>

#### General requirements <a id="rand.req.genl">[[rand.req.genl]]</a>

Throughout [[rand]], the effect of instantiating a template:

- that has a template type parameter named `Sseq` is undefined unless
  the corresponding template argument is cv-unqualified and meets the
  requirements of seed sequence [[rand.req.seedseq]].
- that has a template type parameter named `URBG` is undefined unless
  the corresponding template argument is cv-unqualified and meets the
  requirements of uniform random bit generator [[rand.req.urng]].
- that has a template type parameter named `Engine` is undefined unless
  the corresponding template argument is cv-unqualified and meets the
  requirements of random number engine [[rand.req.eng]].
- that has a template type parameter named `RealType` is undefined
  unless the corresponding template argument is cv-unqualified and is
  one of `float`, `double`, or `long double`.
- that has a template type parameter named `IntType` is undefined unless
  the corresponding template argument is cv-unqualified and is one of
  `short`, `int`, `long`, `long long`, `unsigned short`, `unsigned int`,
  `unsigned long`, or `unsigned long long`.
- that has a template type parameter named `UIntType` is undefined
  unless the corresponding template argument is cv-unqualified and is
  one of `unsigned short`, `unsigned int`, `unsigned long`, or
  `unsigned long long`.

Throughout [[rand]], phrases of the form “`x` is an iterator of a
specific kind” shall be interpreted as equivalent to the more formal
requirement that “`x` is a value of a type meeting the requirements of
the specified iterator type”.

Throughout [[rand]], any constructor that can be called with a single
argument and that meets a requirement specified in this subclause shall
be declared `explicit`.

#### Seed sequence requirements <a id="rand.req.seedseq">[[rand.req.seedseq]]</a>

A *seed sequence* is an object that consumes a sequence of
integer-valued data and produces a requested number of unsigned integer
values i, 0 ≤ i < 2³², based on the consumed data.

[*Note 1*: Such an object provides a mechanism to avoid replication of
streams of random variates. This can be useful, for example, in
applications requiring large numbers of random number
engines. — *end note*]

A class `S` meets the requirements of a seed sequence if the expressions
shown in [[rand.req.seedseq]] are valid and have the indicated
semantics, and if `S` also meets all other requirements of
[[rand.req.seedseq]]. In [[rand.req.seedseq]] and throughout this
subclause:

- `T` is the type named by `S`’s associated `result_type`;
- `q` is a value of type `S` and `r` is a value of type `S` or
  `const S`;
- `ib` and `ie` are input iterators with an unsigned integer
  `value_type` of at least 32 bits;
- `rb` and `re` are mutable random access iterators with an unsigned
  integer `value_type` of at least 32 bits;
- `ob` is an output iterator; and
- `il` is a value of type `initializer_list<T>`.

#### Uniform random bit generator requirements <a id="rand.req.urng">[[rand.req.urng]]</a>

A *uniform random bit generator* `g` of type `G` is a function object
returning unsigned integer values such that each value in the range of
possible results has (ideally) equal probability of being returned.

[*Note 1*: The degree to which `g`’s results approximate the ideal is
often determined statistically. — *end note*]

``` cpp
template<class G>
  concept uniform_random_bit_generator =
    invocable<G&> && unsigned_integral<invoke_result_t<G&>> &&
    requires {
      { G::min() } -> same_as<invoke_result_t<G&>>;
      { G::max() } -> same_as<invoke_result_t<G&>>;
      requires bool_constant<(G::min() < G::max())>::value;
    };
```

Let `g` be an object of type `G`. `G` models
`uniform_random_bit_generator` only if

- `G::min() <= g()`,
- `g() <= G::max()`, and
- `g()` has amortized constant complexity.

A class `G` meets the *uniform random bit generator* requirements if `G`
models `uniform_random_bit_generator`, `invoke_result_t<G&>` is an
unsigned integer type [[basic.fundamental]], and `G` provides a nested
*typedef-name* `result_type` that denotes the same type as
`invoke_result_t<G&>`.

#### Random number engine requirements <a id="rand.req.eng">[[rand.req.eng]]</a>

A *random number engine* (commonly shortened to *engine*) `e` of type
`E` is a uniform random bit generator that additionally meets the
requirements (e.g., for seeding and for input/output) specified in this
subclause.

At any given time, `e` has a state for some integer i ≥ 0. Upon
construction, `e` has an initial state . An engine’s state may be
established via a constructor, a `seed` function, assignment, or a
suitable `operator>>`.

`E`’s specification shall define:

- the size of `E`’s state in multiples of the size of `result_type`,
  given as an integral constant expression;
- the *transition algorithm* TA by which `e`’s state is advanced to its
  *successor state* ; and
- the *generation algorithm* GA by which an engine’s state is mapped to
  a value of type `result_type`.

A class `E` that meets the requirements of a uniform random bit
generator [[rand.req.urng]] also meets the requirements of a *random
number engine* if the expressions shown in [[rand.req.eng]] are valid
and have the indicated semantics, and if `E` also meets all other
requirements of [[rand.req.eng]]. In [[rand.req.eng]] and throughout
this subclause:

- `T` is the type named by `E`’s associated `result_type`;
- `e` is a value of `E`, `v` is an lvalue of `E`, `x` and `y` are
  (possibly const) values of `E`;
- `s` is a value of `T`;
- `q` is an lvalue meeting the requirements of a seed sequence
  [[rand.req.seedseq]];
- `z` is a value of type `unsigned long long`;
- `os` is an lvalue of the type of some class template specialization
  `basic_ostream<charT,` `traits>`; and
- `is` is an lvalue of the type of some class template specialization
  `basic_istream<charT,` `traits>`;

where `charT` and `traits` are constrained according to [[strings]] and
[[input.output]].[^2]

`E` shall meet the *Cpp17CopyConstructible* (
[[cpp17.copyconstructible]]) and *Cpp17CopyAssignable* (
[[cpp17.copyassignable]]) requirements. These operations shall each be
of complexity no worse than .

On hosted implementations, the following expressions are well-formed and
have the specified semantics.

``` cpp
os << x
```

*Effects:* With `os.`*`fmtflags`* set to `ios_base::dec|ios_base::left`
and the fill character set to the space character, writes to `os` the
textual representation of `x`’s current state. In the output, adjacent
numbers are separated by one or more space characters.

*Ensures:* The `os.`*`fmtflags`* and fill character are unchanged.

*Result:* reference to the type of `os`.

*Returns:* `os`.

*Complexity:* 𝑂(size of state)

``` cpp
is >> v
```

*Preconditions:* `is` provides a textual representation that was
previously written using an output stream whose imbued locale was the
same as that of `is`, and whose type’s template specialization arguments
`charT` and `traits` were respectively the same as those of `is`.

*Effects:* With `is.`*`fmtflags`* set to `ios_base::dec`, sets `v`’s
state as determined by reading its textual representation from `is`. If
bad input is encountered, ensures that `v`’s state is unchanged by the
operation and calls `is.setstate(ios_base::failbit)` (which may throw
`ios_base::failure`[[iostate.flags]]). If a textual representation
written via `os << x` was subsequently read via `is >> v`, then `x == v`
provided that there have been no intervening invocations of `x` or of
`v`.

*Ensures:* The `is.`*`fmtflags`* are unchanged.

*Result:* reference to the type of `is`.

*Returns:* `is`.

*Complexity:* 𝑂(size of state)

#### Random number engine adaptor requirements <a id="rand.req.adapt">[[rand.req.adapt]]</a>

A *random number engine adaptor* (commonly shortened to *adaptor*) `a`
of type `A` is a random number engine that takes values produced by some
other random number engine, and applies an algorithm to those values in
order to deliver a sequence of values with different randomness
properties. An engine `b` of type `B` adapted in this way is termed a
*base engine* in this context. The expression `a.base()` shall be valid
and shall return a const reference to `a`’s base engine.

The requirements of a random number engine type shall be interpreted as
follows with respect to a random number engine adaptor type.

``` cpp
A::A();
```

*Effects:* The base engine is initialized as if by its default
constructor.

``` cpp
bool operator==(const A& a1, const A& a2);
```

*Returns:* `true` if `a1`’s base engine is equal to `a2`’s base engine.
Otherwise returns `false`.

``` cpp
A::A(result_type s);
```

*Effects:* The base engine is initialized with `s`.

``` cpp
template<class Sseq> A::A(Sseq& q);
```

*Effects:* The base engine is initialized with `q`.

``` cpp
void seed();
```

*Effects:* With `b` as the base engine, invokes `b.seed()`.

``` cpp
void seed(result_type s);
```

*Effects:* With `b` as the base engine, invokes `b.seed(s)`.

``` cpp
template<class Sseq> void seed(Sseq& q);
```

*Effects:* With `b` as the base engine, invokes `b.seed(q)`.

`A` shall also meet the following additional requirements:

- The complexity of each function shall not exceed the complexity of the
  corresponding function applied to the base engine.
- The state of `A` shall include the state of its base engine. The size
  of `A`’s state shall be no less than the size of the base engine.
- Copying `A`’s state (e.g., during copy construction or copy
  assignment) shall include copying the state of the base engine of `A`.
- The textual representation of `A` shall include the textual
  representation of its base engine.

#### Random number distribution requirements <a id="rand.req.dist">[[rand.req.dist]]</a>

A *random number distribution* (commonly shortened to *distribution*)
`d` of type `D` is a function object returning values that are
distributed according to an associated mathematical *probability density
function* p(z) or according to an associated *discrete probability
function* P(zᵢ). A distribution’s specification identifies its
associated probability function p(z) or P(zᵢ).

An associated probability function is typically expressed using certain
externally-supplied quantities known as the *parameters of the
distribution*. Such distribution parameters are identified in this
context by writing, for example, p(z | a,b) or P(zᵢ | a,b), to name
specific parameters, or by writing, for example,
$p(z\,|\left\{\tcode{p}\right\})$ or
$P(z_i\,|\left\{\tcode{p}\right\})$, to denote a distribution’s
parameters `p` taken as a whole.

A class `D` meets the requirements of a *random number distribution* if
the expressions shown in [[rand.req.dist]] are valid and have the
indicated semantics, and if `D` and its associated types also meet all
other requirements of [[rand.req.dist]]. In [[rand.req.dist]] and
throughout this subclause,

- `T` is the type named by `D`’s associated `result_type`;
- `P` is the type named by `D`’s associated `param_type`;
- `d` is a value of `D`, and `x` and `y` are (possibly const) values of
  `D`;
- `glb` and `lub` are values of `T` respectively corresponding to the
  greatest lower bound and the least upper bound on the values
  potentially returned by `d`’s `operator()`, as determined by the
  current values of `d`’s parameters;
- `p` is a (possibly const) value of `P`;
- `g`, `g1`, and `g2` are lvalues of a type meeting the requirements of
  a uniform random bit generator [[rand.req.urng]];
- `os` is an lvalue of the type of some class template specialization
  `basic_ostream<charT,` `traits>`; and
- `is` is an lvalue of the type of some class template specialization
  `basic_istream<charT,` `traits>`;

where `charT` and `traits` are constrained according to [[strings]] and
[[input.output]].

`D` shall meet the *Cpp17CopyConstructible* (
[[cpp17.copyconstructible]]) and *Cpp17CopyAssignable* (
[[cpp17.copyassignable]]) requirements.

The sequence of numbers produced by repeated invocations of `d(g)` shall
be independent of any invocation of `os << d` or of any `const` member
function of `D` between any of the invocations of `d(g)`.

If a textual representation is written using `os << x` and that
representation is restored into the same or a different object `y` of
the same type using `is >> y`, repeated invocations of `y(g)` shall
produce the same sequence of numbers as would repeated invocations of
`x(g)`.

It is unspecified whether `D::param_type` is declared as a (nested)
`class` or via a `typedef`. In [[rand]], declarations of `D::param_type`
are in the form of `typedef`s for convenience of exposition only.

`P` shall meet the *Cpp17CopyConstructible* (
[[cpp17.copyconstructible]]), *Cpp17CopyAssignable* (
[[cpp17.copyassignable]]), and *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) requirements.

For each of the constructors of `D` taking arguments corresponding to
parameters of the distribution, `P` shall have a corresponding
constructor subject to the same requirements and taking arguments
identical in number, type, and default values. Moreover, for each of the
member functions of `D` that return values corresponding to parameters
of the distribution, `P` shall have a corresponding member function with
the identical name, type, and semantics.

`P` shall have a declaration of the form

``` cpp
using distribution_type =  D;
```

On hosted implementations, the following expressions are well-formed and
have the specified semantics.

``` cpp
os << x
```

*Effects:* Writes to `os` a textual representation for the parameters
and the additional internal data of `x`.

*Ensures:* The `os.`*`fmtflags`* and fill character are unchanged.

*Result:* reference to the type of `os`.

*Returns:* `os`.

``` cpp
is >> d
```

*Preconditions:* `is` provides a textual representation that was
previously written using an `os` whose imbued locale and whose type’s
template specialization arguments `charT` and `traits` were the same as
those of `is`.

*Effects:* Restores from `is` the parameters and additional internal
data of the lvalue `d`. If bad input is encountered, ensures that `d` is
unchanged by the operation and calls `is.setstate(ios_base::failbit)`
(which may throw `ios_base::failure`[[iostate.flags]]).

*Ensures:* The `is.`*`fmtflags`* are unchanged.

*Result:* reference to the type of `is`.

*Returns:* `is`.

### Random number engine class templates <a id="rand.eng">[[rand.eng]]</a>

#### General <a id="rand.eng.general">[[rand.eng.general]]</a>

Each type instantiated from a class template specified in [[rand.eng]]
meets the requirements of a random number engine [[rand.req.eng]] type.

Except where specified otherwise, the complexity of each function
specified in [[rand.eng]] is constant.

Except where specified otherwise, no function described in [[rand.eng]]
throws an exception.

Every function described in [[rand.eng]] that has a function parameter
`q` of type `Sseq&` for a template type parameter named `Sseq` that is
different from type `seed_seq` throws what and when the invocation of
`q.generate` throws.

Descriptions are provided in [[rand.eng]] only for engine operations
that are not described in [[rand.req.eng]] or for operations where there
is additional semantic information. In particular, declarations for copy
constructors, for copy assignment operators, for streaming operators,
and for equality and inequality operators are not shown in the synopses.

Each template specified in [[rand.eng]] requires one or more
relationships, involving the value(s) of its constant template
parameter(s), to hold. A program instantiating any of these templates is
ill-formed if any such required relationship fails to hold.

For every random number engine and for every random number engine
adaptor `X` defined in [[rand.eng]] and in [[rand.adapt]]:

- if the constructor
  ``` cpp
  template<class Sseq> explicit X(Sseq& q);
  ```

  is called with a type `Sseq` that does not qualify as a seed sequence,
  then this constructor shall not participate in overload resolution;
- if the member function
  ``` cpp
  template<class Sseq> void seed(Sseq& q);
  ```

  is called with a type `Sseq` that does not qualify as a seed sequence,
  then this function shall not participate in overload resolution.

The extent to which an implementation determines that a type cannot be a
seed sequence is unspecified, except that as a minimum a type shall not
qualify as a seed sequence if it is implicitly convertible to
`X::result_type`.

#### Class template `linear_congruential_engine` <a id="rand.eng.lcong">[[rand.eng.lcong]]</a>

A `linear_congruential_engine` random number engine produces unsigned
integer random numbers. The state of a `linear_congruential_engine`
object `x` is of size 1 and consists of a single integer. The transition
algorithm is a modular linear function of the form
$\mathsf{TA}(\state{x}{i}) = (a \cdot \state{x}{i} + c) \bmod m$; the
generation algorithm is $\mathsf{GA}(\state{x}{i}) = \state{x}{i+1}$.

``` cpp
namespace std {
  template<class UIntType, UIntType a, UIntType c, UIntType m>
  class linear_congruential_engine {
  public:
    // types
    using result_type = UIntType;

    // engine characteristics
    static constexpr result_type multiplier = a;
    static constexpr result_type increment = c;
    static constexpr result_type modulus = m;
    static constexpr result_type min() { return c == 0u ? 1u: 0u; }
    static constexpr result_type max() { return m - 1u; }
    static constexpr result_type default_seed = 1u;

    // constructors and seeding functions
    linear_congruential_engine() : linear_congruential_engine(default_seed) {}
    explicit linear_congruential_engine(result_type s);
    template<class Sseq> explicit linear_congruential_engine(Sseq& q);
    void seed(result_type s = default_seed);
    template<class Sseq> void seed(Sseq& q);

    // equality operators
    friend bool operator==(const linear_congruential_engine& x,
                           const linear_congruential_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os,            // hosted
                   const linear_congruential_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is,            // hosted
                   linear_congruential_engine& x);
  };
}
```

If the template parameter `m` is 0, the modulus m used throughout
[[rand.eng.lcong]] is `numeric_limits<result_type>::max()` plus 1.

[*Note 1*: m need not be representable as a value of type
`result_type`. — *end note*]

If the template parameter `m` is not 0, the following relations shall
hold: `a < m` and `c < m`.

The textual representation consists of the value of .

``` cpp
explicit linear_congruential_engine(result_type s);
```

*Effects:* If c  mod  m is 0 and `s`  mod  m is 0, sets the engine’s
state to 1, otherwise sets the engine’s state to `s`  mod  m.

``` cpp
template<class Sseq> explicit linear_congruential_engine(Sseq& q);
```

*Effects:* With $k = \left\lceil \frac{\log_2 m}{32} \right\rceil$ and a
an array (or equivalent) of length k + 3, invokes
`q.generate(`a + 0`, `a + k + 3`)` and then computes
$S = \left(\sum_{j = 0}^{k - 1} a_{j + 3} \cdot 2^{32j} \right) \bmod m$.
If c  mod  m is 0 and S is 0, sets the engine’s state to 1, else sets
the engine’s state to S.

#### Class template `mersenne_twister_engine` <a id="rand.eng.mers">[[rand.eng.mers]]</a>

A `mersenne_twister_engine` random number engine[^3]

produces unsigned integer random numbers in the closed interval
[0,2ʷ-1]. The state of a `mersenne_twister_engine` object `x` is of size
n and consists of a sequence X of n values of the type delivered by `x`;
all subscripts applied to X are to be taken modulo n.

The transition algorithm employs a twisted generalized feedback shift
register defined by shift values n and m, a twist value r, and a
conditional xor-mask a. To improve the uniformity of the result, the
bits of the raw shift register are additionally *tempered* (i.e.,
scrambled) according to a bit-scrambling matrix defined by values u, d,
s, b, t, c, and ℓ.

The state transition is performed as follows:

- Concatenate the upper w-r bits of Xᵢ₋ₙ with the lower r bits of
  $X_{i+1-n}$ to obtain an unsigned integer value Y.
- With $\alpha = a \cdot (Y \bitand 1)$, set Xᵢ to
  $X_{i+m-n} \xor (Y \rightshift 1) \xor \alpha$.

The sequence X is initialized with the help of an initialization
multiplier f.

The generation algorithm determines the unsigned integer values
z₁, z₂, z₃, z₄ as follows, then delivers z₄ as its result:

- Let $z_1 = X_i \xor \bigl(( X_i \rightshift u ) \bitand d\bigr)$.
- Let $z_2 = z_1 \xor \bigl( (z_1 \leftshift{w} s) \bitand b \bigr)$.
- Let $z_3 = z_2 \xor \bigl( (z_2 \leftshift{w} t) \bitand c \bigr)$.
- Let $z_4 = z_3 \xor ( z_3 \rightshift \ell )$.

``` cpp
namespace std {
  template<class UIntType, size_t w, size_t n, size_t m, size_t r,
           UIntType a, size_t u, UIntType d, size_t s,
           UIntType b, size_t t,
           UIntType c, size_t l, UIntType f>
  class mersenne_twister_engine {
  public:
    // types
    using result_type = UIntType;

    // engine characteristics
    static constexpr size_t word_size = w;
    static constexpr size_t state_size = n;
    static constexpr size_t shift_size = m;
    static constexpr size_t mask_bits = r;
    static constexpr UIntType xor_mask = a;
    static constexpr size_t tempering_u = u;
    static constexpr UIntType tempering_d = d;
    static constexpr size_t tempering_s = s;
    static constexpr UIntType tempering_b = b;
    static constexpr size_t tempering_t = t;
    static constexpr UIntType tempering_c = c;
    static constexpr size_t tempering_l = l;
    static constexpr UIntType initialization_multiplier = f;
    static constexpr result_type min() { return 0; }
    static constexpr result_type max() { return  2^w - 1; }
    static constexpr result_type default_seed = 5489u;

    // constructors and seeding functions
    mersenne_twister_engine() : mersenne_twister_engine(default_seed) {}
    explicit mersenne_twister_engine(result_type value);
    template<class Sseq> explicit mersenne_twister_engine(Sseq& q);
    void seed(result_type value = default_seed);
    template<class Sseq> void seed(Sseq& q);

    // equality operators
    friend bool operator==(const mersenne_twister_engine& x, const mersenne_twister_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os,            // hosted
                   const mersenne_twister_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is,            // hosted
                   mersenne_twister_engine& x);
  };
}
```

The following relations shall hold: `0 < m`, `m <= n`, `2u < w`,
`r <= w`, `u <= w`, `s <= w`, `t <= w`, `l <= w`,
`w <= numeric_limits<UIntType>::digits`, `a <= (1u << w) - 1u`,
`b <= (1u << w) - 1u`, `c <= (1u << w) - 1u`, `d <= (1u << w) - 1u`, and
`f <= (1u << w) - 1u`.

The textual representation of consists of the values of
$X_{i - n}, \dotsc, X_{i - 1}$, in that order.

``` cpp
explicit mersenne_twister_engine(result_type value);
```

*Effects:* Sets $X_{-n}$ to `value`  mod  2ʷ. Then, iteratively for
i = 1 - n, …, -1, sets Xᵢ to $$%
 \bigl[f \cdot
       \bigl(X_{i-1} \xor \bigl(X_{i-1} \rightshift (w-2)\bigr)
       \bigr)
       + i \bmod n
 \bigr] \bmod 2^w
\; \mbox{.}$$

*Complexity:* 𝑂(n).

``` cpp
template<class Sseq> explicit mersenne_twister_engine(Sseq& q);
```

*Effects:* With $k = \left\lceil w / 32 \right\rceil$ and a an array (or
equivalent) of length n ⋅ k, invokes `q.generate(`a+0`, `a+n ⋅ k`)` and
then, iteratively for i = -n,…,-1, sets Xᵢ to
$\left(\sum_{j=0}^{k-1}a_{k(i+n)+j} \cdot 2^{32j} \right) \bmod 2^w$.
Finally, if the most significant w-r bits of $X_{-n}$ are zero, and if
each of the other resulting Xᵢ is 0, changes $X_{-n}$ to 2ʷ⁻¹.

#### Class template `subtract_with_carry_engine` <a id="rand.eng.sub">[[rand.eng.sub]]</a>

A `subtract_with_carry_engine` random number engine produces unsigned
integer random numbers.

The state of a `subtract_with_carry_engine` object `x` is of size , and
consists of a sequence X of r integer values 0 ≤ Xᵢ < m  = 2ʷ; all
subscripts applied to X are to be taken modulo r. The state additionally
consists of an integer c (known as the *carry*) whose value is either 0
or 1.

The state transition is performed as follows:

- Let Y = Xᵢ₋ₛ - Xᵢ₋ᵣ - c.
- Set Xᵢ to y = Y  mod  m. Set c to 1 if Y < 0, otherwise set c to 0.

[*Note 1*: This algorithm corresponds to a modular linear function of
the form $\mathsf{TA}(\state{x}{i}) = (a \cdot \state{x}{i}) \bmod b$,
where b is of the form mʳ - mˢ + 1 and
a = b - (b - 1) / m. — *end note*]

The generation algorithm is given by $\mathsf{GA}(\state{x}{i}) = y$,
where y is the value produced as a result of advancing the engine’s
state as described above.

``` cpp
namespace std {
  template<class UIntType, size_t w, size_t s, size_t r>
  class subtract_with_carry_engine {
  public:
    // types
    using result_type = UIntType;

    // engine characteristics
    static constexpr size_t word_size = w;
    static constexpr size_t short_lag = s;
    static constexpr size_t long_lag = r;
    static constexpr result_type min() { return 0; }
    static constexpr result_type max() { return m - 1; }
    static constexpr uint_least32_t default_seed = 19780503u;

    // constructors and seeding functions
    subtract_with_carry_engine() : subtract_with_carry_engine(0u) {}
    explicit subtract_with_carry_engine(result_type value);
    template<class Sseq> explicit subtract_with_carry_engine(Sseq& q);
    void seed(result_type value = 0u);
    template<class Sseq> void seed(Sseq& q);

    // equality operators
    friend bool operator==(const subtract_with_carry_engine& x,
                           const subtract_with_carry_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os,            // hosted
                   const subtract_with_carry_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is,            // hosted
                   subtract_with_carry_engine& x);
  };
}
```

The following relations shall hold: `0u < s`, `s < r`, `0 < w`, and
`w <= numeric_limits<UIntType>::digits`.

The textual representation consists of the values of Xᵢ₋ᵣ, …, Xᵢ₋₁, in
that order, followed by c.

``` cpp
explicit subtract_with_carry_engine(result_type value);
```

*Effects:* Sets the values of $X_{-r}, \dotsc, X_{-1}$, in that order,
as specified below. If $X_{-1}$ is then 0, sets c to 1; otherwise sets c
to 0.

To set the values Xₖ, first construct `e`, a
`linear_congruential_engine` object, as if by the following definition:

``` cpp
linear_congruential_engine<uint_least32_t, 40014u, 0u, 2147483563u> e(
  value == 0u ? default_seed : static_cast<uint_least32_t>(value % 2147483563u));
```

Then, to set each Xₖ, obtain new values z₀, …, zₙ₋₁ from n = ⌈ w/32 ⌉
successive invocations of `e`. Set Xₖ to
$\left( \sum_{j=0}^{n-1} z_j \cdot 2^{32j}\right) \bmod m$.

*Complexity:* Exactly n ⋅ `r` invocations of `e`.

``` cpp
template<class Sseq> explicit subtract_with_carry_engine(Sseq& q);
```

*Effects:* With $k = \left\lceil w / 32 \right\rceil$ and a an array (or
equivalent) of length r ⋅ k, invokes `q.generate(`a + 0`, `a + r ⋅ k`)`
and then, iteratively for i = -r, …, -1, sets Xᵢ to
$\left(\sum_{j=0}^{k-1}a_{k(i+r)+j} \cdot 2^{32j} \right) \bmod m$. If
$X_{-1}$ is then 0, sets c to 1; otherwise sets c to 0.

#### Class template `philox_engine` <a id="rand.eng.philox">[[rand.eng.philox]]</a>

A `philox_engine` random number engine produces unsigned integer random
numbers in the interval \[`0`, m), where m = 2ʷ and the template
parameter w defines the range of the produced numbers. The state of a
`philox_engine` object consists of a sequence X of n unsigned integer
values of width w, a sequence K of n/2 values of `result_type`, a
sequence Y of n values of `result_type`, and a scalar i, where

- X is the interpretation of the unsigned integer *counter* value
  $Z \cedef \sum_{j = 0}^{n - 1} X_j \cdot 2^{wj}$ of n ⋅ w bits,
- K are keys, which are generated once from the seed (see constructors
  below) and remain constant unless the `seed` function [[rand.req.eng]]
  is invoked,
- Y stores a batch of output values, and
- i is an index for an element of the sequence Y.

The generation algorithm returns Yᵢ, the value stored in the iᵗʰ element
of Y after applying the transition algorithm.

The state transition is performed as if by the following algorithm:

``` cpp
i = i + 1
if (i == n) {
  Y = Philox(K, X) // see below
  Z = Z + 1
  i = 0
}
```

The `Philox` function maps the length-n/2 sequence K and the length-n
sequence X into a length-n output sequence Y. Philox applies an r-round
substitution-permutation network to the values in X. A single round of
the generation algorithm performs the following steps:

- The output sequence X' of the previous round (X in case of the first
  round) is permuted to obtain the intermediate state V:
  ``` cpp
  Vⱼ = X'_{fₙ(j)}
  ```

  where j = 0, …, n - 1 and fₙ(j) is defined in [[rand.eng.philox.f]].
  **Table: Values for the word permutation $\bm{f}_{\bm{n}}\bm{(j)}$**

  |                                               |                              |
  | --------------------------------------------- | ---------------------------- |
  | *[spans 2 columns]* $\bm{f}_{\bm{n}}\bm{(j)}$ | *[spans 4 columns]* $\bm{j}$ |
  | \multicolumn{2}{|c|}                          | 0                            | 1   | 2   | 3   |
  | $\bm{n} $                                     | 2                            | 0   | 1   | \multicolumn{2}{c|} |
  |                                               | 4                            | 2   | 1   | 0   | 3   |


  \[*Note 1*: For n = 2 the sequence is not permuted. — *end note*]
- The following computations are applied to the elements of the V
  sequence:
  ``` cpp
  X_2k + 0} = \mulhi(V_2k, Mₖ, w) \xor key^qₖ \xor V_2k + 1}
  X_2k + 1} = \mullo(V_2k, Mₖ, w)
  ```

  where:
  - μllo(`a`, `b`, `w`) is the low half of the modular multiplication of
    `a` and `b`: $(\tcode{a} \cdot \tcode{b}) \mod 2^w$,
  - μlhi(`a`, `b`, `w`) is the high half of the modular multiplication
    of `a` and `b`:
    $(\left\lfloor (\tcode{a} \cdot \tcode{b}) / 2^w \right\rfloor)$,
  - k = 0, …, n/2 - 1 is the index in the sequences,
  - q = 0, …, r - 1 is the index of the round,
  - $\mathit{key}^q_k$ is the kᵗʰ round key for round q,
    $\mathit{key}^q_k \cedef (K_k + q \cdot C_k) \mod 2^w$,
  - Kₖ are the elements of the key sequence K,
  - Mₖ is `multipliers[k]`, and
  - Cₖ is `round_consts[k]`.

After r applications of the single-round function, `Philox` returns the
sequence Y = X'.

``` cpp
namespace std {
  template<class UIntType, size_t w, size_t n, size_t r, UIntType... consts>
  class philox_engine {
    static constexpr size_t array-size = n / 2;   // exposition only
  public:
    // types
    using result_type = UIntType;

    // engine characteristics
    static constexpr size_t word_size = w;
    static constexpr size_t word_count = n;
    static constexpr size_t round_count = r;
    static constexpr array<result_type, array-size> multipliers;
    static constexpr array<result_type, array-size> round_consts;
    static constexpr result_type min() { return 0; }
    static constexpr result_type max() { return m - 1; }
    static constexpr result_type default_seed = 20111115u;

    // constructors and seeding functions
    philox_engine() : philox_engine(default_seed) {}
    explicit philox_engine(result_type value);
    template<class Sseq> explicit philox_engine(Sseq& q);
    void seed(result_type value = default_seed);
    template<class Sseq> void seed(Sseq& q);

    void set_counter(const array<result_type, n>& counter);

    // equality operators
    friend bool operator==(const philox_engine& x, const philox_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const philox_engine& x);   // hosted
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, philox_engine& x);         // hosted
  };
}
```

*Mandates:*

- `sizeof...(consts) == n` is `true`, and
- `n == 2 || n == 4` is `true`, and
- `0 < r` is `true`, and
- `0 < w && w <= numeric_limits<UIntType>::digits` is `true`.

The template parameter pack `consts` represents the Mₖ and Cₖ constants
which are grouped as follows:
$[ M_0, C_0, M_1, C_1, M_2, C_2, \dotsc, M_{n/2 - 1}, C_{n/2 - 1} ]$.

The textual representation consists of the values of
$K_0, \dotsc, K_{n/2 - 1}, X_{0}, \dotsc, X_{n - 1}, i$, in that order.

[*Note 1*: The stream extraction operator can reconstruct Y from K and
X, as needed. — *end note*]

``` cpp
explicit philox_engine(result_type value);
```

*Effects:* Sets the K₀ element of sequence K to
$\texttt{value} \mod 2^w$. All elements of sequences X and K (except K₀)
are set to `0`. The value of i is set to n - 1.

``` cpp
template<class Sseq> explicit philox_engine(Sseq& q);
```

*Effects:* With $p = \left\lceil w / 32 \right\rceil$ and an array (or
equivalent) `a` of length (n/2) ⋅ p, invokes
`q.generate(a + 0, a + n / 2 * `p`)` and then iteratively for
k = 0, …, n/2 - 1, sets Kₖ to
$\left(\sum_{j = 0}^{p - 1} a_{k p + j} \cdot 2^{32j} \right) \mod 2^w$.
All elements of sequence X are set to `0`. The value of i is set to
n - 1.

``` cpp
void set_counter(const array<result_type, n>& c);
```

*Effects:* For j = 0, …, n - 1 sets Xⱼ to $C_{n - 1 - j} \mod 2^w$. The
value of i is set to n - 1.

[*Note 1*: The counter is the value Z introduced at the beginning of
this subclause. — *end note*]

### Random number engine adaptor class templates <a id="rand.adapt">[[rand.adapt]]</a>

#### General <a id="rand.adapt.general">[[rand.adapt.general]]</a>

Each type instantiated from a class template specified in [[rand.adapt]]
meets the requirements of a random number engine adaptor
[[rand.req.adapt]] type.

Except where specified otherwise, the complexity of each function
specified in [[rand.adapt]] is constant.

Except where specified otherwise, no function described in
[[rand.adapt]] throws an exception.

Every function described in [[rand.adapt]] that has a function parameter
`q` of type `Sseq&` for a template type parameter named `Sseq` that is
different from type `seed_seq` throws what and when the invocation of
`q.generate` throws.

Descriptions are provided in [[rand.adapt]] only for adaptor operations
that are not described in subclause  [[rand.req.adapt]] or for
operations where there is additional semantic information. In
particular, declarations for copy constructors, for copy assignment
operators, for streaming operators, and for equality and inequality
operators are not shown in the synopses.

Each template specified in [[rand.adapt]] requires one or more
relationships, involving the value(s) of its constant template
parameter(s), to hold. A program instantiating any of these templates is
ill-formed if any such required relationship fails to hold.

#### Class template `discard_block_engine` <a id="rand.adapt.disc">[[rand.adapt.disc]]</a>

A `discard_block_engine` random number engine adaptor produces random
numbers selected from those produced by some base engine e. The state of
a `discard_block_engine` engine adaptor object `x` consists of the state
of its base engine `e` and an additional integer n. The size of the
state is the size of e’s state plus 1.

The transition algorithm discards all but r > 0 values from each block
of p ≥ r values delivered by e. The state transition is performed as
follows: If n ≥ r, advance the state of `e` from to and set n to 0. In
any case, then increment n and advance `e`’s then-current state to .

The generation algorithm yields the value returned by the last
invocation of `e()` while advancing `e`’s state as described above.

``` cpp
namespace std {
  template<class Engine, size_t p, size_t r>
  class discard_block_engine {
  public:
    // types
    using result_type = Engine::result_type;

    // engine characteristics
    static constexpr size_t block_size = p;
    static constexpr size_t used_block = r;
    static constexpr result_type min() { return Engine::min(); }
    static constexpr result_type max() { return Engine::max(); }

    // constructors and seeding functions
    discard_block_engine();
    explicit discard_block_engine(const Engine& e);
    explicit discard_block_engine(Engine&& e);
    explicit discard_block_engine(result_type s);
    template<class Sseq> explicit discard_block_engine(Sseq& q);
    void seed();
    void seed(result_type s);
    template<class Sseq> void seed(Sseq& q);

    // equality operators
    friend bool operator==(const discard_block_engine& x, const discard_block_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // property functions
    const Engine& base() const noexcept { return e; }

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const discard_block_engine& x);    // hosted
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, discard_block_engine& x);          // hosted

  private:
    Engine e;   // exposition only
    size_t n;   // exposition only
  };
}
```

The following relations shall hold: `0 < r` and `r <= p`.

The textual representation consists of the textual representation of `e`
followed by the value of `n`.

In addition to its behavior pursuant to subclause  [[rand.req.adapt]],
each constructor that is not a copy constructor sets `n` to 0.

#### Class template `independent_bits_engine` <a id="rand.adapt.ibits">[[rand.adapt.ibits]]</a>

An `independent_bits_engine` random number engine adaptor combines
random numbers that are produced by some base engine e, so as to produce
random numbers with a specified number of bits w. The state of an
`independent_bits_engine` engine adaptor object `x` consists of the
state of its base engine `e`; the size of the state is the size of e’s
state.

The transition and generation algorithms are described in terms of the
following integral constants:

- Let R = `e.max() - e.min() + 1` and
  $m = \left\lfloor \log_2 R \right\rfloor$.
- With n as determined below, let
  $w_0 = \left\lfloor w / n \right\rfloor$, n₀ = n - w  mod  n,
  $y_0 = 2^{w_0} \left\lfloor R / 2^{w_0} \right\rfloor$, and
  $y_1 = 2^{w_0 + 1} \left\lfloor R / 2^{w_0 + 1} \right\rfloor$.
- Let $n = \left\lceil w / m \right\rceil$ if and only if the relation
  $R - y_0 \leq \left\lfloor y_0 / n \right\rfloor$ holds as a result.
  Otherwise let $n = 1 + \left\lceil w / m \right\rceil$.

[*Note 1*: The relation w = n₀ w₀ + (n - n₀)(w₀ + 1) always
holds. — *end note*]

The transition algorithm is carried out by invoking `e()` as often as
needed to obtain n₀ values less than y₀ + `e.min()` and n - n₀ values
less than y₁ + `e.min()`.

The generation algorithm uses the values produced while advancing the
state as described above to yield a quantity S obtained as if by the
following algorithm:

``` cpp
S = 0;
for (k = 0; k \neq n₀; k += 1)  {
 do u = e() - e.min(); while (u \ge y₀);
 S = 2^{w₀ \cdot S + u \bmod 2^{w₀;
}
for (k = n₀; k \neq n; k += 1)  {
 do u = e() - e.min(); while (u \ge y₁);
 S = 2^{w₀ + 1} \cdot S + u \bmod 2^{w₀ + 1};
}
```

``` cpp
namespace std {
  template<class Engine, size_t w, class UIntType>
  class independent_bits_engine {
  public:
    // types
    using result_type = UIntType;

    // engine characteristics
    static constexpr result_type min() { return 0; }
    static constexpr result_type max() { return 2^w - 1; }

    // constructors and seeding functions
    independent_bits_engine();
    explicit independent_bits_engine(const Engine& e);
    explicit independent_bits_engine(Engine&& e);
    explicit independent_bits_engine(result_type s);
    template<class Sseq> explicit independent_bits_engine(Sseq& q);
    void seed();
    void seed(result_type s);
    template<class Sseq> void seed(Sseq& q);

    // equality operators
    friend bool operator==(const independent_bits_engine& x, const independent_bits_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // property functions
    const Engine& base() const noexcept { return e; }

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const independent_bits_engine& x); // hosted
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, independent_bits_engine& x);       // hosted

  private:
    Engine e;   // exposition only
  };
}
```

The following relations shall hold: `0 < w` and
`w <= numeric_limits<result_type>::digits`.

The textual representation consists of the textual representation of
`e`.

#### Class template `shuffle_order_engine` <a id="rand.adapt.shuf">[[rand.adapt.shuf]]</a>

A `shuffle_order_engine` random number engine adaptor produces the same
random numbers that are produced by some base engine e, but delivers
them in a different sequence. The state of a `shuffle_order_engine`
engine adaptor object `x` consists of the state of its base engine `e`,
an additional value Y of the type delivered by `e`, and an additional
sequence V of k values also of the type delivered by `e`. The size of
the state is the size of e’s state plus k + 1.

The transition algorithm permutes the values produced by e. The state
transition is performed as follows:

- Calculate an integer $j = \left\lfloor \frac{k \cdot (Y - e_{\min})}
                            {e_{\max} - e_{\min} +1}
          \right\rfloor$ .
- Set Y to Vⱼ and then set Vⱼ to `e()`.

The generation algorithm yields the last value of `Y` produced while
advancing `e`’s state as described above.

``` cpp
namespace std {
  template<class Engine, size_t k>
  class shuffle_order_engine {
  public:
    // types
    using result_type = Engine::result_type;

    // engine characteristics
    static constexpr size_t table_size = k;
    static constexpr result_type min() { return Engine::min(); }
    static constexpr result_type max() { return Engine::max(); }

    // constructors and seeding functions
    shuffle_order_engine();
    explicit shuffle_order_engine(const Engine& e);
    explicit shuffle_order_engine(Engine&& e);
    explicit shuffle_order_engine(result_type s);
    template<class Sseq> explicit shuffle_order_engine(Sseq& q);
    void seed();
    void seed(result_type s);
    template<class Sseq> void seed(Sseq& q);

    // equality operators
    friend bool operator==(const shuffle_order_engine& x, const shuffle_order_engine& y);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // property functions
    const Engine& base() const noexcept { return e; }

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const shuffle_order_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, shuffle_order_engine& x);

  private:
    Engine e;           // exposition only
    result_type V[k];   // exposition only
    result_type Y;      // exposition only
  };
}
```

The following relation shall hold: `0 < k`.

The textual representation consists of the textual representation of
`e`, followed by the `k` values of V, followed by the value of Y.

In addition to its behavior pursuant to subclause  [[rand.req.adapt]],
each constructor that is not a copy constructor initializes
`V[0]`, …, `V[k - 1]` and Y, in that order, with values returned by
successive invocations of `e()`.

### Engines and engine adaptors with predefined parameters <a id="rand.predef">[[rand.predef]]</a>

``` cpp
using minstd_rand0 =
      linear_congruential_engine<uint_fast32_t, 16'807, 0, 2'147'483'647>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `minstd_rand0` produces the value
1043618065.

``` cpp
using minstd_rand =
      linear_congruential_engine<uint_fast32_t, 48'271, 0, 2'147'483'647>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `minstd_rand` produces the value
399268537.

``` cpp
using mt19937 =
      mersenne_twister_engine<uint_fast32_t, 32, 624, 397, 31,
       0x9908'b0df, 11, 0xffff'ffff, 7, 0x9d2c'5680, 15, 0xefc6'0000, 18, 1'812'433'253>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `mt19937` produces the value
4123659995.

``` cpp
using mt19937_64 =
      mersenne_twister_engine<uint_fast64_t, 64, 312, 156, 31,
       0xb502'6f5a'a966'19e9, 29, 0x5555'5555'5555'5555, 17,
       0x71d6'7fff'eda6'0000, 37, 0xfff7'eee0'0000'0000, 43, 6'364'136'223'846'793'005>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `mt19937_64` produces the value
9981545732273789042.

``` cpp
using ranlux24_base =
      subtract_with_carry_engine<uint_fast32_t, 24, 10, 24>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `ranlux24_base` produces the value
7937952.

``` cpp
using ranlux48_base =
      subtract_with_carry_engine<uint_fast64_t, 48, 5, 12>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `ranlux48_base` produces the value
61839128582725.

``` cpp
using ranlux24 = discard_block_engine<ranlux24_base, 223, 23>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `ranlux24` produces the value
9901578.

``` cpp
using ranlux48 = discard_block_engine<ranlux48_base, 389, 11>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `ranlux48` produces the value
249142670248501.

``` cpp
using knuth_b = shuffle_order_engine<minstd_rand0,256>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation of a
default-constructed object of type `knuth_b` produces the value
1112339016.

``` cpp
using default_random_engine = implementation-defined;
```

*Remarks:* The choice of engine type named by this `typedef` is
*implementation-defined*.

[*Note 1*: The implementation can select this type on the basis of
performance, size, quality, or any combination of such factors, so as to
provide at least acceptable engine behavior for relatively casual,
inexpert, and/or lightweight use. Because different implementations can
select different underlying engine types, code that uses this `typedef`
need not generate identical sequences across
implementations. — *end note*]

``` cpp
using philox4x32 =
      philox_engine<uint_fast32_t, 32, 4, 10,
       0xCD9E8D57, 0x9E3779B9, 0xD2511F53, 0xBB67AE85>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation a
default-constructed object of type `philox4x32` produces the value
1955073260.

``` cpp
using philox4x64 =
      philox_engine<uint_fast64_t, 64, 4, 10,
       0xCA5A826395121157, 0x9E3779B97F4A7C15, 0xD2E7470EE14C6C93, 0xBB67AE8584CAA73B>;
```

*Required behavior:* The 10000ᵗʰ consecutive invocation a
default-constructed object of type `philox4x64` produces the value
3409172418970261260.

### Class `random_device` <a id="rand.device">[[rand.device]]</a>

A `random_device` uniform random bit generator produces nondeterministic
random numbers.

If implementation limitations prevent generating nondeterministic random
numbers, the implementation may employ a random number engine.

``` cpp
namespace std {
  class random_device {
  public:
    // types
    using result_type = unsigned int;

    // generator characteristics
    static constexpr result_type min() { return numeric_limits<result_type>::min(); }
    static constexpr result_type max() { return numeric_limits<result_type>::max(); }

    // constructors
    random_device() : random_device(implementation-defined) {}
    explicit random_device(const string& token);

    // generating functions
    result_type operator()();

    // property functions
    double entropy() const noexcept;

    // no copy functions
    random_device(const random_device&) = delete;
    void operator=(const random_device&) = delete;
  };
}
```

``` cpp
explicit random_device(const string& token);
```

*Throws:* A value of an *implementation-defined* type derived from
`exception` if the `random_device` cannot be initialized.

*Remarks:* The semantics of the `token` parameter and the token value
used by the default constructor are *implementation-defined*.[^4]

``` cpp
double entropy() const noexcept;
```

*Returns:* If the implementation employs a random number engine, returns
0.0. Otherwise, returns an entropy estimate[^5]

for the random numbers returned by `operator()`, in the range `min()` to
log₂( `max()`+1).

``` cpp
result_type operator()();
```

*Returns:* A nondeterministic random value, uniformly distributed
between `min()` and `max()` (inclusive). It is *implementation-defined*
how these values are generated.

*Throws:* A value of an *implementation-defined* type derived from
`exception` if a random number cannot be obtained.

### Utilities <a id="rand.util">[[rand.util]]</a>

#### Class `seed_seq` <a id="rand.util.seedseq">[[rand.util.seedseq]]</a>

``` cpp
namespace std {
  class seed_seq {
  public:
    // types
    using result_type = uint_least32_t;

    // constructors
    seed_seq() noexcept;
    template<class T>
      seed_seq(initializer_list<T> il);
    template<class InputIterator>
      seed_seq(InputIterator begin, InputIterator end);

    // generating functions
    template<class RandomAccessIterator>
      void generate(RandomAccessIterator begin, RandomAccessIterator end);

    // property functions
    size_t size() const noexcept;
    template<class OutputIterator>
      void param(OutputIterator dest) const;

    // no copy functions
    seed_seq(const seed_seq&) = delete;
    void operator=(const seed_seq&) = delete;

  private:
    vector<result_type> v;      // exposition only
  };
}
```

``` cpp
seed_seq() noexcept;
```

*Ensures:* `v.empty()` is `true`.

``` cpp
template<class T>
  seed_seq(initializer_list<T> il);
```

*Constraints:* `T` is an integer type.

*Effects:* Same as `seed_seq(il.begin(), il.end())`.

``` cpp
template<class InputIterator>
  seed_seq(InputIterator begin, InputIterator end);
```

*Mandates:* `iterator_traits<InputIterator>::value_type` is an integer
type.

*Preconditions:* `InputIterator` meets the *Cpp17InputIterator*
requirements [[input.iterators]].

*Effects:* Initializes `v` by the following algorithm:

``` cpp
for (InputIterator s = begin; s != end; ++s)
 v.push_back((*s) mod  2³²);
```

``` cpp
template<class RandomAccessIterator>
  void generate(RandomAccessIterator begin, RandomAccessIterator end);
```

*Mandates:* `iterator_traits<RandomAccessIterator>::value_type` is an
unsigned integer type capable of accommodating 32-bit quantities.

*Preconditions:* `RandomAccessIterator` meets the
*Cpp17RandomAccessIterator* requirements [[random.access.iterators]] and
the requirements of a mutable iterator.

*Effects:* Does nothing if `begin == end`. Otherwise, with
s = `v.size()` and n = `end` - `begin`, fills the supplied range
[`begin`,`end`) according to the following algorithm in which each
operation is to be carried out modulo 2³², each indexing operator
applied to `begin` is to be taken modulo n, and T(x) is defined as
$x \xor (x \rightshift 27)$:

- By way of initialization, set each element of the range to the value
  `0x8b8b8b8b`. Additionally, for use in subsequent steps, let
  p = (n - t) / 2 and let q = p + t, where $$%
       t = (n \ge 623) \mbox{ ? } 11 \mbox{ : } (n \ge 68) \mbox{ ? } 7 \mbox{ : } (n \ge 39) \mbox{ ? } 5 \mbox{ : } (n \ge 7) \mbox{ ? } 3 \mbox{ : } (n - 1)/2;$$
- With m as the larger of s + 1 and n, transform the elements of the
  range: iteratively for k = 0, …, m - 1, calculate values
  $$\begin{aligned}
       r_1 & = &
         1664525 \cdot T(    \texttt{begin[}k\texttt{]}
                        \xor \texttt{begin[}k+p\texttt{]}
                        \xor \texttt{begin[}k-1 \texttt{]}
                        )
       \\
       r_2 & = & r_1 + \left\{
         \begin{array}{cl}
           s                                  & \mbox{,  } k = 0
           \\
           k \bmod n + \texttt{v[}k-1\texttt{]} & \mbox{,  } 0 < k \le s
           \\
           k \bmod n                          & \mbox{,  } s < k
         \end{array}
       \right.
     
  \end{aligned}$$ and, in order, increment `begin[`k+p`]` by r₁,
  increment `begin[`k+q`]` by r₂, and set `begin[`k`]` to r₂.
- Transform the elements of the range again, beginning where the
  previous step ended: iteratively for k = m, …, m + n - 1, calculate
  values $$\begin{aligned}
       r_3 & = &
         1566083941 \cdot T( \texttt{begin[}k  \texttt{]}
                           + \texttt{begin[}k+p\texttt{]}
                           + \texttt{begin[}k-1\texttt{]}
                           )
       \\
       r_4 & = & r_3 - (k \bmod n)
     
  \end{aligned}$$ and, in order, update `begin[`k+p`]` by xoring it with
  r₃, update `begin[`k+q`]` by xoring it with r₄, and set `begin[`k`]`
  to r₄.

*Throws:* What and when `RandomAccessIterator` operations of `begin` and
`end` throw.

``` cpp
size_t size() const noexcept;
```

*Returns:* The number of 32-bit units that would be returned by a call
to `param()`.

*Complexity:* Constant time.

``` cpp
template<class OutputIterator>
  void param(OutputIterator dest) const;
```

*Mandates:* Values of type `result_type` are
writable [[iterator.requirements.general]] to `dest`.

*Preconditions:* `OutputIterator` meets the *Cpp17OutputIterator*
requirements [[output.iterators]].

*Effects:* Copies the sequence of prepared 32-bit units to the given
destination, as if by executing the following statement:

``` cpp
copy(v.begin(), v.end(), dest);
```

*Throws:* What and when `OutputIterator` operations of `dest` throw.

#### Function template `generate_canonical` <a id="rand.util.canonical">[[rand.util.canonical]]</a>

``` cpp
template<class RealType, size_t digits, class URBG>
  RealType generate_canonical(URBG& g);
```

Let

- r be `numeric_limits<RealType>::radix`,
- R be `g.max()` - `g.min()` + 1,
- d be the smaller of `digits` and
  `numeric_limits<RealType>::digits`,[^6]
- k be the smallest integer such that Rᵏ ≥ rᵈ, and
- x be $\left\lfloor R^k / r^d \right\rfloor$.

An *attempt* is k invocations of `g()` to obtain values g₀, …, gₖ₋₁,
respectively, and the calculation of a quantity S given by :

*Effects:* Attempts are made until S < xrᵈ.

[*Note 1*: When R is a power of r, precisely one attempt is
made. — *end note*]

*Returns:* $\left\lfloor S / x \right\rfloor / r^d$.

[*Note 2*: The return value c satisfies 0 ≤ c < 1. — *end note*]

*Throws:* What and when `g` throws.

*Complexity:* Exactly k invocations of `g` per attempt.

[*Note 3*: If the values gᵢ produced by `g` are uniformly distributed,
the instantiation’s results are distributed as uniformly as possible.
Obtaining a value in this way can be a useful step in the process of
transforming a value generated by a uniform random bit generator into a
value that can be delivered by a random number
distribution. — *end note*]

[*Note 4*: When R is a power of r, an implementation can avoid using an
arithmetic type that is wider than the output when computing
S. — *end note*]

### Random number distribution class templates <a id="rand.dist">[[rand.dist]]</a>

#### General <a id="rand.dist.general">[[rand.dist.general]]</a>

Each type instantiated from a class template specified in [[rand.dist]]
meets the requirements of a random number distribution [[rand.req.dist]]
type.

Descriptions are provided in [[rand.dist]] only for distribution
operations that are not described in [[rand.req.dist]] or for operations
where there is additional semantic information. In particular,
declarations for copy constructors, for copy assignment operators, for
streaming operators, and for equality and inequality operators are not
shown in the synopses.

The algorithms for producing each of the specified distributions are
*implementation-defined*.

The value of each probability density function p(z) and of each discrete
probability function P(zᵢ) specified in this subclause is 0 everywhere
outside its stated domain.

#### Uniform distributions <a id="rand.dist.uni">[[rand.dist.uni]]</a>

##### Class template `uniform_int_distribution` <a id="rand.dist.uni.int">[[rand.dist.uni.int]]</a>

A `uniform_int_distribution` random number distribution produces random
integers i, a ≤ i ≤ b, distributed according to the constant discrete
probability function in .

``` cpp
namespace std {
  template<class IntType = int>
  class uniform_int_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    uniform_int_distribution() : uniform_int_distribution(0) {}
    explicit uniform_int_distribution(IntType a, IntType b = numeric_limits<IntType>::max());
    explicit uniform_int_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const uniform_int_distribution& x, const uniform_int_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    result_type a() const;
    result_type b() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os,            // hosted
                   const uniform_int_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is,            // hosted
                   uniform_int_distribution& x);
  };
}
```

``` cpp
explicit uniform_int_distribution(IntType a, IntType b = numeric_limits<IntType>::max());
```

*Preconditions:* `a` ≤ `b`.

*Remarks:* `a` and `b` correspond to the respective parameters of the
distribution.

``` cpp
result_type a() const;
```

*Returns:* The value of the `a` parameter with which the object was
constructed.

``` cpp
result_type b() const;
```

*Returns:* The value of the `b` parameter with which the object was
constructed.

##### Class template `uniform_real_distribution` <a id="rand.dist.uni.real">[[rand.dist.uni.real]]</a>

A `uniform_real_distribution` random number distribution produces random
numbers x, a ≤ x < b, distributed according to the constant probability
density function in .

[*Note 1*: This implies that p(x | a,b) is undefined when
`a == b`. — *end note*]

``` cpp
namespace std {
  template<class RealType = double>
  class uniform_real_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    uniform_real_distribution() : uniform_real_distribution(0.0) {}
    explicit uniform_real_distribution(RealType a, RealType b = 1.0);
    explicit uniform_real_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const uniform_real_distribution& x,
                           const uniform_real_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    result_type a() const;
    result_type b() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const uniform_real_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, uniform_real_distribution& x);
  };
}
```

``` cpp
explicit uniform_real_distribution(RealType a, RealType b = 1.0);
```

*Preconditions:* `a` ≤ `b` and
`b` - `a` ≤ `numeric_limits<RealType>::max()`.

*Remarks:* `a` and `b` correspond to the respective parameters of the
distribution.

``` cpp
result_type a() const;
```

*Returns:* The value of the `a` parameter with which the object was
constructed.

``` cpp
result_type b() const;
```

*Returns:* The value of the `b` parameter with which the object was
constructed.

#### Bernoulli distributions <a id="rand.dist.bern">[[rand.dist.bern]]</a>

##### Class `bernoulli_distribution` <a id="rand.dist.bern.bernoulli">[[rand.dist.bern.bernoulli]]</a>

A `bernoulli_distribution` random number distribution produces `bool`
values b distributed according to the discrete probability function in .

``` cpp
namespace std {
  class bernoulli_distribution {
  public:
    // types
    using result_type = bool;
    using param_type  = unspecified;

    // constructors and reset functions
    bernoulli_distribution() : bernoulli_distribution(0.5) {}
    explicit bernoulli_distribution(double p);
    explicit bernoulli_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const bernoulli_distribution& x, const bernoulli_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    double p() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const bernoulli_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, bernoulli_distribution& x);
  };
}
```

``` cpp
explicit bernoulli_distribution(double p);
```

*Preconditions:* 0 ≤ `p` ≤ 1.

*Remarks:* `p` corresponds to the parameter of the distribution.

``` cpp
double p() const;
```

*Returns:* The value of the `p` parameter with which the object was
constructed.

##### Class template `binomial_distribution` <a id="rand.dist.bern.bin">[[rand.dist.bern.bin]]</a>

A `binomial_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
in .

``` cpp
namespace std {
  template<class IntType = int>
  class binomial_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    binomial_distribution() : binomial_distribution(1) {}
    explicit binomial_distribution(IntType t, double p = 0.5);
    explicit binomial_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const binomial_distribution& x, const binomial_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    IntType t() const;
    double p() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const binomial_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, binomial_distribution& x);
  };
}
```

``` cpp
explicit binomial_distribution(IntType t, double p = 0.5);
```

*Preconditions:* 0 ≤ `p` ≤ 1 and 0 ≤ `t`.

*Remarks:* `t` and `p` correspond to the respective parameters of the
distribution.

``` cpp
IntType t() const;
```

*Returns:* The value of the `t` parameter with which the object was
constructed.

``` cpp
double p() const;
```

*Returns:* The value of the `p` parameter with which the object was
constructed.

##### Class template `geometric_distribution` <a id="rand.dist.bern.geo">[[rand.dist.bern.geo]]</a>

A `geometric_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
in .

``` cpp
namespace std {
  template<class IntType = int>
  class geometric_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    geometric_distribution() : geometric_distribution(0.5) {}
    explicit geometric_distribution(double p);
    explicit geometric_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const geometric_distribution& x, const geometric_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    double p() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const geometric_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, geometric_distribution& x);
  };
}
```

``` cpp
explicit geometric_distribution(double p);
```

*Preconditions:* 0 < `p` < 1.

*Remarks:* `p` corresponds to the parameter of the distribution.

``` cpp
double p() const;
```

*Returns:* The value of the `p` parameter with which the object was
constructed.

##### Class template `negative_binomial_distribution` <a id="rand.dist.bern.negbin">[[rand.dist.bern.negbin]]</a>

A `negative_binomial_distribution` random number distribution produces
random integers i ≥ 0 distributed according to the discrete probability
function in .

[*Note 1*: This implies that P(i | k,p) is undefined when
`p == 1`. — *end note*]

``` cpp
namespace std {
  template<class IntType = int>
  class negative_binomial_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructor and reset functions
    negative_binomial_distribution() : negative_binomial_distribution(1) {}
    explicit negative_binomial_distribution(IntType k, double p = 0.5);
    explicit negative_binomial_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const negative_binomial_distribution& x,
                           const negative_binomial_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    IntType k() const;
    double p() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const negative_binomial_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, negative_binomial_distribution& x);
  };
}
```

``` cpp
explicit negative_binomial_distribution(IntType k, double p = 0.5);
```

*Preconditions:* 0 < `p` ≤ 1 and 0 < `k`.

*Remarks:* `k` and `p` correspond to the respective parameters of the
distribution.

``` cpp
IntType k() const;
```

*Returns:* The value of the `k` parameter with which the object was
constructed.

``` cpp
double p() const;
```

*Returns:* The value of the `p` parameter with which the object was
constructed.

#### Poisson distributions <a id="rand.dist.pois">[[rand.dist.pois]]</a>

##### Class template `poisson_distribution` <a id="rand.dist.pois.poisson">[[rand.dist.pois.poisson]]</a>

A `poisson_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
in .

The distribution parameter μ is also known as this distribution’s
*mean*.

``` cpp
namespace std {
  template<class IntType = int>
  class poisson_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    poisson_distribution() : poisson_distribution(1.0) {}
    explicit poisson_distribution(double mean);
    explicit poisson_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const poisson_distribution& x, const poisson_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    double mean() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const poisson_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, poisson_distribution& x);
  };
}
```

``` cpp
explicit poisson_distribution(double mean);
```

*Preconditions:* 0 < `mean`.

*Remarks:* `mean` corresponds to the parameter of the distribution.

``` cpp
double mean() const;
```

*Returns:* The value of the `mean` parameter with which the object was
constructed.

##### Class template `exponential_distribution` <a id="rand.dist.pois.exp">[[rand.dist.pois.exp]]</a>

An `exponential_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
in .

``` cpp
namespace std {
  template<class RealType = double>
  class exponential_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    exponential_distribution() : exponential_distribution(1.0) {}
    explicit exponential_distribution(RealType lambda);
    explicit exponential_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const exponential_distribution& x, const exponential_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType lambda() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const exponential_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, exponential_distribution& x);
  };
}
```

``` cpp
explicit exponential_distribution(RealType lambda);
```

*Preconditions:* 0 < `lambda`.

*Remarks:* `lambda` corresponds to the parameter of the distribution.

``` cpp
RealType lambda() const;
```

*Returns:* The value of the `lambda` parameter with which the object was
constructed.

##### Class template `gamma_distribution` <a id="rand.dist.pois.gamma">[[rand.dist.pois.gamma]]</a>

A `gamma_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
in .

``` cpp
namespace std {
  template<class RealType = double>
  class gamma_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    gamma_distribution() : gamma_distribution(1.0) {}
    explicit gamma_distribution(RealType alpha, RealType beta = 1.0);
    explicit gamma_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const gamma_distribution& x, const gamma_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType alpha() const;
    RealType beta() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const gamma_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, gamma_distribution& x);
  };
}
```

``` cpp
explicit gamma_distribution(RealType alpha, RealType beta = 1.0);
```

*Preconditions:* 0 < `alpha` and 0 < `beta`.

*Remarks:* `alpha` and `beta` correspond to the parameters of the
distribution.

``` cpp
RealType alpha() const;
```

*Returns:* The value of the `alpha` parameter with which the object was
constructed.

``` cpp
RealType beta() const;
```

*Returns:* The value of the `beta` parameter with which the object was
constructed.

##### Class template `weibull_distribution` <a id="rand.dist.pois.weibull">[[rand.dist.pois.weibull]]</a>

A `weibull_distribution` random number distribution produces random
numbers x ≥ 0 distributed according to the probability density function
in .

``` cpp
namespace std {
  template<class RealType = double>
  class weibull_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    weibull_distribution() : weibull_distribution(1.0) {}
    explicit weibull_distribution(RealType a, RealType b = 1.0);
    explicit weibull_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const weibull_distribution& x, const weibull_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType a() const;
    RealType b() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const weibull_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, weibull_distribution& x);
  };
}
```

``` cpp
explicit weibull_distribution(RealType a, RealType b = 1.0);
```

*Preconditions:* 0 < `a` and 0 < `b`.

*Remarks:* `a` and `b` correspond to the respective parameters of the
distribution.

``` cpp
RealType a() const;
```

*Returns:* The value of the `a` parameter with which the object was
constructed.

``` cpp
RealType b() const;
```

*Returns:* The value of the `b` parameter with which the object was
constructed.

##### Class template `extreme_value_distribution` <a id="rand.dist.pois.extreme">[[rand.dist.pois.extreme]]</a>

An `extreme_value_distribution` random number distribution produces
random numbers x distributed according to the probability density
function in .[^7]

``` cpp
namespace std {
  template<class RealType = double>
  class extreme_value_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    extreme_value_distribution() : extreme_value_distribution(0.0) {}
    explicit extreme_value_distribution(RealType a, RealType b = 1.0);
    explicit extreme_value_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const extreme_value_distribution& x,
                           const extreme_value_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType a() const;
    RealType b() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const extreme_value_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, extreme_value_distribution& x);
  };
}
```

``` cpp
explicit extreme_value_distribution(RealType a, RealType b = 1.0);
```

*Preconditions:* 0 < `b`.

*Remarks:* `a` and `b` correspond to the respective parameters of the
distribution.

``` cpp
RealType a() const;
```

*Returns:* The value of the `a` parameter with which the object was
constructed.

``` cpp
RealType b() const;
```

*Returns:* The value of the `b` parameter with which the object was
constructed.

#### Normal distributions <a id="rand.dist.norm">[[rand.dist.norm]]</a>

##### Class template `normal_distribution` <a id="rand.dist.norm.normal">[[rand.dist.norm.normal]]</a>

A `normal_distribution` random number distribution produces random
numbers x distributed according to the probability density function in .

The distribution parameters μ and σ are also known as this
distribution’s *mean* and *standard deviation*.

``` cpp
namespace std {
  template<class RealType = double>
  class normal_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    normal_distribution() : normal_distribution(0.0) {}
    explicit normal_distribution(RealType mean, RealType stddev = 1.0);
    explicit normal_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const normal_distribution& x, const normal_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType mean() const;
    RealType stddev() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const normal_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, normal_distribution& x);
  };
}
```

``` cpp
explicit normal_distribution(RealType mean, RealType stddev = 1.0);
```

*Preconditions:* 0 < `stddev`.

*Remarks:* `mean` and `stddev` correspond to the respective parameters
of the distribution.

``` cpp
RealType mean() const;
```

*Returns:* The value of the `mean` parameter with which the object was
constructed.

``` cpp
RealType stddev() const;
```

*Returns:* The value of the `stddev` parameter with which the object was
constructed.

##### Class template `lognormal_distribution` <a id="rand.dist.norm.lognormal">[[rand.dist.norm.lognormal]]</a>

A `lognormal_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
in .

``` cpp
namespace std {
  template<class RealType = double>
  class lognormal_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    lognormal_distribution() : lognormal_distribution(0.0) {}
    explicit lognormal_distribution(RealType m, RealType s = 1.0);
    explicit lognormal_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const lognormal_distribution& x, const lognormal_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType m() const;
    RealType s() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const lognormal_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, lognormal_distribution& x);
  };
}
```

``` cpp
explicit lognormal_distribution(RealType m, RealType s = 1.0);
```

*Preconditions:* 0 < `s`.

*Remarks:* `m` and `s` correspond to the respective parameters of the
distribution.

``` cpp
RealType m() const;
```

*Returns:* The value of the `m` parameter with which the object was
constructed.

``` cpp
RealType s() const;
```

*Returns:* The value of the `s` parameter with which the object was
constructed.

##### Class template `chi_squared_distribution` <a id="rand.dist.norm.chisq">[[rand.dist.norm.chisq]]</a>

A `chi_squared_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
in .

``` cpp
namespace std {
  template<class RealType = double>
  class chi_squared_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    chi_squared_distribution() : chi_squared_distribution(1.0) {}
    explicit chi_squared_distribution(RealType n);
    explicit chi_squared_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const chi_squared_distribution& x, const chi_squared_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType n() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const chi_squared_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, chi_squared_distribution& x);
  };
}
```

``` cpp
explicit chi_squared_distribution(RealType n);
```

*Preconditions:* 0 < `n`.

*Remarks:* `n` corresponds to the parameter of the distribution.

``` cpp
RealType n() const;
```

*Returns:* The value of the `n` parameter with which the object was
constructed.

##### Class template `cauchy_distribution` <a id="rand.dist.norm.cauchy">[[rand.dist.norm.cauchy]]</a>

A `cauchy_distribution` random number distribution produces random
numbers x distributed according to the probability density function in .

``` cpp
namespace std {
  template<class RealType = double>
  class cauchy_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    cauchy_distribution() : cauchy_distribution(0.0) {}
    explicit cauchy_distribution(RealType a, RealType b = 1.0);
    explicit cauchy_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const cauchy_distribution& x, const cauchy_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType a() const;
    RealType b() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const cauchy_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, cauchy_distribution& x);
  };
}
```

``` cpp
explicit cauchy_distribution(RealType a, RealType b = 1.0);
```

*Preconditions:* 0 < `b`.

*Remarks:* `a` and `b` correspond to the respective parameters of the
distribution.

``` cpp
RealType a() const;
```

*Returns:* The value of the `a` parameter with which the object was
constructed.

``` cpp
RealType b() const;
```

*Returns:* The value of the `b` parameter with which the object was
constructed.

##### Class template `fisher_f_distribution` <a id="rand.dist.norm.f">[[rand.dist.norm.f]]</a>

A `fisher_f_distribution` random number distribution produces random
numbers x ≥ 0 distributed according to the probability density function
in .

``` cpp
namespace std {
  template<class RealType = double>
  class fisher_f_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    fisher_f_distribution() : fisher_f_distribution(1.0) {}
    explicit fisher_f_distribution(RealType m, RealType n = 1.0);
    explicit fisher_f_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const fisher_f_distribution& x, const fisher_f_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType m() const;
    RealType n() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const fisher_f_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, fisher_f_distribution& x);
  };
}
```

``` cpp
explicit fisher_f_distribution(RealType m, RealType n = 1);
```

*Preconditions:* 0 < `m` and 0 < `n`.

*Remarks:* `m` and `n` correspond to the respective parameters of the
distribution.

``` cpp
RealType m() const;
```

*Returns:* The value of the `m` parameter with which the object was
constructed.

``` cpp
RealType n() const;
```

*Returns:* The value of the `n` parameter with which the object was
constructed.

##### Class template `student_t_distribution` <a id="rand.dist.norm.t">[[rand.dist.norm.t]]</a>

A `student_t_distribution` random number distribution produces random
numbers x distributed according to the probability density function in .

``` cpp
namespace std {
  template<class RealType = double>
  class student_t_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    student_t_distribution() : student_t_distribution(1.0) {}
    explicit student_t_distribution(RealType n);
    explicit student_t_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const student_t_distribution& x, const student_t_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    RealType n() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const student_t_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, student_t_distribution& x);
  };
}
```

``` cpp
explicit student_t_distribution(RealType n);
```

*Preconditions:* 0 < `n`.

*Remarks:* `n` corresponds to the parameter of the distribution.

``` cpp
RealType n() const;
```

*Returns:* The value of the `n` parameter with which the object was
constructed.

#### Sampling distributions <a id="rand.dist.samp">[[rand.dist.samp]]</a>

##### Class template `discrete_distribution` <a id="rand.dist.samp.discrete">[[rand.dist.samp.discrete]]</a>

A `discrete_distribution` random number distribution produces random
integers i, 0 ≤ i < n, distributed according to the discrete probability
function in .

Unless specified otherwise, the distribution parameters are calculated
as: $p_k = {w_k / S}$ for k = 0, …, n - 1, in which the values wₖ,
commonly known as the *weights* , shall be non-negative, non-NaN, and
non-infinity. Moreover, the following relation shall hold:
$0 < S = w_0 + \dotsb + w_{n - 1}$.

``` cpp
namespace std {
  template<class IntType = int>
  class discrete_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructor and reset functions
    discrete_distribution();
    template<class InputIterator>
      discrete_distribution(InputIterator firstW, InputIterator lastW);
    discrete_distribution(initializer_list<double> wl);
    template<class UnaryOperation>
      discrete_distribution(size_t nw, double xmin, double xmax, UnaryOperation fw);
    explicit discrete_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const discrete_distribution& x, const discrete_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    vector<double> probabilities() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const discrete_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, discrete_distribution& x);
  };
}
```

``` cpp
discrete_distribution();
```

*Effects:* Constructs a `discrete_distribution` object with n = 1 and
p₀ = 1.

[*Note 1*: Such an object will always deliver the value
0. — *end note*]

``` cpp
template<class InputIterator>
  discrete_distribution(InputIterator firstW, InputIterator lastW);
```

*Mandates:*
`is_convertible_v<iterator_traits<InputIterator>::value_type, double>`
is `true`.

*Preconditions:* `InputIterator` meets the *Cpp17InputIterator*
requirements [[input.iterators]]. If `firstW == lastW`, let n = 1 and
w₀ = 1. Otherwise, [`firstW`, `lastW`) forms a sequence w of length
n > 0.

*Effects:* Constructs a `discrete_distribution` object with
probabilities given by the .

``` cpp
discrete_distribution(initializer_list<double> wl);
```

*Effects:* Same as `discrete_distribution(wl.begin(), wl.end())`.

``` cpp
template<class UnaryOperation>
  discrete_distribution(size_t nw, double xmin, double xmax, UnaryOperation fw);
```

*Mandates:* `is_invocable_r_v<double, UnaryOperation&, double>` is
`true`.

*Preconditions:* If `nw` = 0, let n = 1, otherwise let n = `nw`. The
relation 0 < δ = (`xmax` - `xmin`) / n holds.

*Effects:* Constructs a `discrete_distribution` object with
probabilities given by the formula above, using the following values: If
`nw` = 0, let w₀ = 1. Otherwise, let wₖ = `fw`(`xmin` + k ⋅ δ + δ / 2)
for k = 0, …, n - 1.

*Complexity:* The number of invocations of `fw` does not exceed n.

``` cpp
vector<double> probabilities() const;
```

*Returns:* A `vector<double>` whose `size` member returns n and whose
`operator[]` member returns pₖ when invoked with argument k for
k = 0, …, n - 1.

##### Class template `piecewise_constant_distribution` <a id="rand.dist.samp.pconst">[[rand.dist.samp.pconst]]</a>

A `piecewise_constant_distribution` random number distribution produces
random numbers x, b₀ ≤ x < bₙ, uniformly distributed over each
subinterval [ bᵢ, bᵢ₊₁ ) according to the probability density function
in .

The n + 1 distribution parameters bᵢ, also known as this distribution’s
*interval boundaries* , shall satisfy the relation $b_i < b_{i + 1}$ for
i = 0, …, n - 1. Unless specified otherwise, the remaining n
distribution parameters are calculated as:
$$\rho_k = \frac{w_k}{S \cdot (b_{k+1}-b_k)} \text{ for } k = 0, \dotsc, n - 1 \text{ ,}$$
in which the values wₖ, commonly known as the *weights* , shall be
non-negative, non-NaN, and non-infinity. Moreover, the following
relation shall hold: 0 < S = w₀ + … + wₙ₋₁.

``` cpp
namespace std {
  template<class RealType = double>
  class piecewise_constant_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    piecewise_constant_distribution();
    template<class InputIteratorB, class InputIteratorW>
      piecewise_constant_distribution(InputIteratorB firstB, InputIteratorB lastB,
                                      InputIteratorW firstW);
    template<class UnaryOperation>
      piecewise_constant_distribution(initializer_list<RealType> bl, UnaryOperation fw);
    template<class UnaryOperation>
      piecewise_constant_distribution(size_t nw, RealType xmin, RealType xmax,
                                      UnaryOperation fw);
    explicit piecewise_constant_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const piecewise_constant_distribution& x,
                           const piecewise_constant_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    vector<result_type> intervals() const;
    vector<result_type> densities() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const piecewise_constant_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, piecewise_constant_distribution& x);
  };
}
```

``` cpp
piecewise_constant_distribution();
```

*Effects:* Constructs a `piecewise_constant_distribution` object with
n = 1, ρ₀ = 1, b₀ = 0, and b₁ = 1.

``` cpp
template<class InputIteratorB, class InputIteratorW>
  piecewise_constant_distribution(InputIteratorB firstB, InputIteratorB lastB,
                                  InputIteratorW firstW);
```

*Mandates:* Both of

- `is_convertible_v<iterator_traits<InputIteratorB>::value_type, double>`
- `is_convertible_v<iterator_traits<InputIteratorW>::value_type, double>`

are `true`.

*Preconditions:* `InputIteratorB` and `InputIteratorW` each meet the
*Cpp17InputIterator* requirements [[input.iterators]]. If
`firstB == lastB` or `++firstB == lastB`, let n = 1, w₀ = 1, b₀ = 0, and
b₁ = 1. Otherwise, [`firstB`, `lastB`) forms a sequence b of length n+1,
the length of the sequence w starting from `firstW` is at least n, and
any wₖ for k ≥ n are ignored by the distribution.

*Effects:* Constructs a `piecewise_constant_distribution` object with
parameters as specified above.

``` cpp
template<class UnaryOperation>
  piecewise_constant_distribution(initializer_list<RealType> bl, UnaryOperation fw);
```

*Mandates:* `is_invocable_r_v<double, UnaryOperation&, double>` is
`true`.

*Effects:* Constructs a `piecewise_constant_distribution` object with
parameters taken or calculated from the following values: If
`bl.size()` < 2, let n = 1, w₀ = 1, b₀ = 0, and b₁ = 1. Otherwise, let
[`bl.begin()`, `bl.end()`) form a sequence b₀, …, bₙ, and let
wₖ = `fw`((bₖ₊₁ + bₖ) / 2) for k = 0, …, n - 1.

*Complexity:* The number of invocations of `fw` does not exceed n.

``` cpp
template<class UnaryOperation>
  piecewise_constant_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
```

*Mandates:* `is_invocable_r_v<double, UnaryOperation&, double>` is
`true`.

*Preconditions:* If `nw` = 0, let n = 1, otherwise let n = `nw`. The
relation 0 < δ = (`xmax` - `xmin`) / n holds.

*Effects:* Constructs a `piecewise_constant_distribution` object with
parameters taken or calculated from the following values: Let
bₖ = `xmin` + k ⋅ δ for k = 0, …, n, and wₖ = `fw`(bₖ + δ / 2) for
k = 0, …, n - 1.

*Complexity:* The number of invocations of `fw` does not exceed n.

``` cpp
vector<result_type> intervals() const;
```

*Returns:* A `vector<result_type>` whose `size` member returns n + 1 and
whose `operator[]` member returns bₖ when invoked with argument k for
k = 0, …, n.

``` cpp
vector<result_type> densities() const;
```

*Returns:* A `vector<result_type>` whose `size` member returns n and
whose `operator[]` member returns ρₖ when invoked with argument k for
k = 0, …, n - 1.

##### Class template `piecewise_linear_distribution` <a id="rand.dist.samp.plinear">[[rand.dist.samp.plinear]]</a>

A `piecewise_linear_distribution` random number distribution produces
random numbers x, b₀ ≤ x < bₙ, distributed over each subinterval
[bᵢ, bᵢ₊₁) according to the probability density function in .

The n + 1 distribution parameters bᵢ, also known as this distribution’s
*interval boundaries* , shall satisfy the relation bᵢ < bᵢ₊₁ for
i = 0, …, n - 1. Unless specified otherwise, the remaining n + 1
distribution parameters are calculated as $\rho_k = {w_k / S}$ for
k = 0, …, n, in which the values wₖ, commonly known as the *weights at
boundaries* , shall be non-negative, non-NaN, and non-infinity.
Moreover, the following relation shall hold:
$$0 < S = \frac{1}{2} \cdot \sum_{k=0}^{n-1} (w_k + w_{k+1}) \cdot (b_{k+1} - b_k) \text{ .}$$

``` cpp
namespace std {
  template<class RealType = double>
  class piecewise_linear_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    piecewise_linear_distribution();
    template<class InputIteratorB, class InputIteratorW>
      piecewise_linear_distribution(InputIteratorB firstB, InputIteratorB lastB,
                                    InputIteratorW firstW);
    template<class UnaryOperation>
      piecewise_linear_distribution(initializer_list<RealType> bl, UnaryOperation fw);
    template<class UnaryOperation>
      piecewise_linear_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
    explicit piecewise_linear_distribution(const param_type& parm);
    void reset();

    // equality operators
    friend bool operator==(const piecewise_linear_distribution& x,
                           const piecewise_linear_distribution& y);

    // generating functions
    template<class URBG>
      result_type operator()(URBG& g);
    template<class URBG>
      result_type operator()(URBG& g, const param_type& parm);

    // property functions
    vector<result_type> intervals() const;
    vector<result_type> densities() const;
    param_type param() const;
    void param(const param_type& parm);
    result_type min() const;
    result_type max() const;

    // inserters and extractors
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const piecewise_linear_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, piecewise_linear_distribution& x);
  };
}
```

``` cpp
piecewise_linear_distribution();
```

*Effects:* Constructs a `piecewise_linear_distribution` object with
n = 1, ρ₀ = ρ₁ = 1, b₀ = 0, and b₁ = 1.

``` cpp
template<class InputIteratorB, class InputIteratorW>
  piecewise_linear_distribution(InputIteratorB firstB, InputIteratorB lastB,
                                InputIteratorW firstW);
```

*Mandates:* Both of

- `is_convertible_v<iterator_traits<InputIteratorB>::value_type, double>`
- `is_convertible_v<iterator_traits<InputIteratorW>::value_type, double>`

are `true`.

*Preconditions:* `InputIteratorB` and `InputIteratorW` each meet the
*Cpp17InputIterator* requirements [[input.iterators]]. If
`firstB == lastB` or `++firstB == lastB`, let n = 1, ρ₀ = ρ₁ = 1,
b₀ = 0, and b₁ = 1. Otherwise, [`firstB`, `lastB`) forms a sequence b of
length n+1, the length of the sequence w starting from `firstW` is at
least n+1, and any wₖ for k ≥ n + 1 are ignored by the distribution.

*Effects:* Constructs a `piecewise_linear_distribution` object with
parameters as specified above.

``` cpp
template<class UnaryOperation>
  piecewise_linear_distribution(initializer_list<RealType> bl, UnaryOperation fw);
```

*Mandates:* `is_invocable_r_v<double, UnaryOperation&, double>` is
`true`.

*Effects:* Constructs a `piecewise_linear_distribution` object with
parameters taken or calculated from the following values: If
`bl.size()` < 2, let n = 1, ρ₀ = ρ₁ = 1, b₀ = 0, and b₁ = 1. Otherwise,
let [`bl.begin(),` `bl.end()`) form a sequence b₀, …, bₙ, and let
wₖ = `fw`(bₖ) for k = 0, …, n.

*Complexity:* The number of invocations of `fw` does not exceed n+1.

``` cpp
template<class UnaryOperation>
  piecewise_linear_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
```

*Mandates:* `is_invocable_r_v<double, UnaryOperation&, double>` is
`true`.

*Preconditions:* If `nw` = 0, let n = 1, otherwise let n = `nw`. The
relation 0 < δ = (`xmax` - `xmin`) / n holds.

*Effects:* Constructs a `piecewise_linear_distribution` object with
parameters taken or calculated from the following values: Let
bₖ = `xmin` + k ⋅ δ for k = 0, …, n, and wₖ = `fw`(bₖ) for k = 0, …, n.

*Complexity:* The number of invocations of `fw` does not exceed n+1.

``` cpp
vector<result_type> intervals() const;
```

*Returns:* A `vector<result_type>` whose `size` member returns n + 1 and
whose `operator[]` member returns bₖ when invoked with argument k for
k = 0, …, n.

``` cpp
vector<result_type> densities() const;
```

*Returns:* A `vector<result_type>` whose `size` member returns n and
whose `operator[]` member returns ρₖ when invoked with argument k for
k = 0, …, n.

### Low-quality random number generation <a id="c.math.rand">[[c.math.rand]]</a>

[*Note 1*: The header `<cstdlib>` declares the functions described in
this subclause. — *end note*]

``` cpp
int rand();
void srand(unsigned int seed);
```

*Effects:* The `rand` and `srand` functions have the semantics specified
in the C standard library.

*Remarks:* The implementation may specify that particular library
functions may call `rand`. It is *implementation-defined* whether the
`rand` function may introduce data races [[res.on.data.races]].

[*Note 1*: The other random number generation facilities in this
document [[rand]] are often preferable to `rand`, because `rand`’s
underlying algorithm is unspecified. Use of `rand` therefore continues
to be non-portable, with unpredictable and oft-questionable quality and
performance. — *end note*]

## Numeric arrays <a id="numarray">[[numarray]]</a>

### Header `<valarray>` synopsis <a id="valarray.syn">[[valarray.syn]]</a>

``` cpp
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  template<class T> class valarray;         // An array of type T
  class slice;                              // a BLAS-like slice out of an array
  template<class T> class slice_array;
  class gslice;                             // a generalized slice out of an array
  template<class T> class gslice_array;
  template<class T> class mask_array;       // a masked array
  template<class T> class indirect_array;   // an indirected array

  template<class T> void swap(valarray<T>&, valarray<T>&) noexcept;

  template<class T> valarray<T> operator* (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator* (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator* (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator/ (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator/ (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator/ (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator% (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator% (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator% (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator+ (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator+ (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator+ (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator- (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator- (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator- (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator^ (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator^ (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator^ (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator& (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator& (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator& (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator| (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator| (const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator| (const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator<<(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator<<(const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator<<(const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<T> operator>>(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator>>(const valarray<T>&,
                                           const typename valarray<T>::value_type&);
  template<class T> valarray<T> operator>>(const typename valarray<T>::value_type&,
                                           const valarray<T>&);

  template<class T> valarray<bool> operator&&(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator&&(const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator&&(const typename valarray<T>::value_type&,
                                              const valarray<T>&);

  template<class T> valarray<bool> operator||(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator||(const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator||(const typename valarray<T>::value_type&,
                                              const valarray<T>&);

  template<class T> valarray<bool> operator==(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator==(const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator==(const typename valarray<T>::value_type&,
                                              const valarray<T>&);
  template<class T> valarray<bool> operator!=(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator!=(const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator!=(const typename valarray<T>::value_type&,
                                              const valarray<T>&);

  template<class T> valarray<bool> operator< (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator< (const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator< (const typename valarray<T>::value_type&,
                                              const valarray<T>&);
  template<class T> valarray<bool> operator> (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator> (const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator> (const typename valarray<T>::value_type&,
                                              const valarray<T>&);
  template<class T> valarray<bool> operator<=(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator<=(const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator<=(const typename valarray<T>::value_type&,
                                              const valarray<T>&);
  template<class T> valarray<bool> operator>=(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator>=(const valarray<T>&,
                                              const typename valarray<T>::value_type&);
  template<class T> valarray<bool> operator>=(const typename valarray<T>::value_type&,
                                              const valarray<T>&);

  template<class T> valarray<T> abs  (const valarray<T>&);
  template<class T> valarray<T> acos (const valarray<T>&);
  template<class T> valarray<T> asin (const valarray<T>&);
  template<class T> valarray<T> atan (const valarray<T>&);

  template<class T> valarray<T> atan2(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> atan2(const valarray<T>&,
                                      const typename valarray<T>::value_type&);
  template<class T> valarray<T> atan2(const typename valarray<T>::value_type&,
                                      const valarray<T>&);

  template<class T> valarray<T> cos  (const valarray<T>&);
  template<class T> valarray<T> cosh (const valarray<T>&);
  template<class T> valarray<T> exp  (const valarray<T>&);
  template<class T> valarray<T> log  (const valarray<T>&);
  template<class T> valarray<T> log10(const valarray<T>&);

  template<class T> valarray<T> pow(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> pow(const valarray<T>&, const typename valarray<T>::value_type&);
  template<class T> valarray<T> pow(const typename valarray<T>::value_type&, const valarray<T>&);

  template<class T> valarray<T> sin  (const valarray<T>&);
  template<class T> valarray<T> sinh (const valarray<T>&);
  template<class T> valarray<T> sqrt (const valarray<T>&);
  template<class T> valarray<T> tan  (const valarray<T>&);
  template<class T> valarray<T> tanh (const valarray<T>&);

  template<class T> unspecified{1} begin(valarray<T>& v);
  template<class T> unspecified{2} begin(const valarray<T>& v);
  template<class T> unspecified{1} end(valarray<T>& v);
  template<class T> unspecified{2} end(const valarray<T>& v);
}
```

The header `<valarray>` defines five class templates (`valarray`,
`slice_array`, `gslice_array`, `mask_array`, and `indirect_array`), two
classes (`slice` and `gslice`), and a series of related function
templates for representing and manipulating arrays of values.

The `valarray` array classes are defined to be free of certain forms of
aliasing, thus allowing operations on these classes to be optimized.

Any function returning a `valarray<T>` is permitted to return an object
of another type, provided all the const member functions of
`valarray<T>` are also applicable to this type. This return type shall
not add more than two levels of template nesting over the most deeply
nested argument type.[^8]

Implementations introducing such replacement types shall provide
additional functions and operators as follows:

- for every function taking a `const valarray<T>&` other than `begin`
  and `end` [[valarray.range]], identical functions taking the
  replacement types shall be added;
- for every function taking two `const valarray<T>&` arguments,
  identical functions taking every combination of `const valarray<T>&`
  and replacement types shall be added.

In particular, an implementation shall allow a `valarray<T>` to be
constructed from such replacement types and shall allow assignments and
compound assignments of such types to `valarray<T>`, `slice_array<T>`,
`gslice_array<T>`, `mask_array<T>` and `indirect_array<T>` objects.

These library functions are permitted to throw a `bad_alloc`
[[bad.alloc]] exception if there are not sufficient resources available
to carry out the operation. Note that the exception is not mandated.

### Class template `valarray` <a id="template.valarray">[[template.valarray]]</a>

#### Overview <a id="template.valarray.overview">[[template.valarray.overview]]</a>

``` cpp
namespace std {
  template<class T> class valarray {
  public:
    using value_type = T;

    // [valarray.cons], construct/destroy
    valarray();
    explicit valarray(size_t);
    valarray(const T&, size_t);
    valarray(const T*, size_t);
    valarray(const valarray&);
    valarray(valarray&&) noexcept;
    valarray(const slice_array<T>&);
    valarray(const gslice_array<T>&);
    valarray(const mask_array<T>&);
    valarray(const indirect_array<T>&);
    valarray(initializer_list<T>);
    ~valarray();

    // [valarray.assign], assignment
    valarray& operator=(const valarray&);
    valarray& operator=(valarray&&) noexcept;
    valarray& operator=(initializer_list<T>);
    valarray& operator=(const T&);
    valarray& operator=(const slice_array<T>&);
    valarray& operator=(const gslice_array<T>&);
    valarray& operator=(const mask_array<T>&);
    valarray& operator=(const indirect_array<T>&);

    // [valarray.access], element access
    const T&          operator[](size_t) const;
    T&                operator[](size_t);

    // [valarray.sub], subset operations
    valarray          operator[](slice) const;
    slice_array<T>    operator[](slice);
    valarray          operator[](const gslice&) const;
    gslice_array<T>   operator[](const gslice&);
    valarray          operator[](const valarray<bool>&) const;
    mask_array<T>     operator[](const valarray<bool>&);
    valarray          operator[](const valarray<size_t>&) const;
    indirect_array<T> operator[](const valarray<size_t>&);

    // [valarray.unary], unary operators
    valarray operator+() const;
    valarray operator-() const;
    valarray operator~() const;
    valarray<bool> operator!() const;

    // [valarray.cassign], compound assignment
    valarray& operator*= (const T&);
    valarray& operator/= (const T&);
    valarray& operator%= (const T&);
    valarray& operator+= (const T&);
    valarray& operator-= (const T&);
    valarray& operator^= (const T&);
    valarray& operator&= (const T&);
    valarray& operator|= (const T&);
    valarray& operator<<=(const T&);
    valarray& operator>>=(const T&);

    valarray& operator*= (const valarray&);
    valarray& operator/= (const valarray&);
    valarray& operator%= (const valarray&);
    valarray& operator+= (const valarray&);
    valarray& operator-= (const valarray&);
    valarray& operator^= (const valarray&);
    valarray& operator|= (const valarray&);
    valarray& operator&= (const valarray&);
    valarray& operator<<=(const valarray&);
    valarray& operator>>=(const valarray&);

    // [valarray.members], member functions
    void swap(valarray&) noexcept;

    size_t size() const;

    T sum() const;
    T min() const;
    T max() const;

    valarray shift (int) const;
    valarray cshift(int) const;
    valarray apply(T func(T)) const;
    valarray apply(T func(const T&)) const;
    void resize(size_t sz, T c = T());
  };

  template<class T, size_t cnt> valarray(const T(&)[cnt], size_t) -> valarray<T>;
}
```

The class template `valarray<T>` is a one-dimensional smart array, with
elements numbered sequentially from zero. It is a representation of the
mathematical concept of an ordered set of values. For convenience, an
object of type `valarray<T>` is referred to as an “array” throughout the
remainder of  [[numarray]]. The illusion of higher dimensionality may be
produced by the familiar idiom of computed indices, together with the
powerful subsetting capabilities provided by the generalized subscript
operators.[^9]

#### Constructors <a id="valarray.cons">[[valarray.cons]]</a>

``` cpp
valarray();
```

*Effects:* Constructs a `valarray` that has zero length.[^10]

``` cpp
explicit valarray(size_t n);
```

*Effects:* Constructs a `valarray` that has length `n`. Each element of
the array is value-initialized [[dcl.init]].

``` cpp
valarray(const T& v, size_t n);
```

*Effects:* Constructs a `valarray` that has length `n`. Each element of
the array is initialized with `v`.

``` cpp
valarray(const T* p, size_t n);
```

*Preconditions:* \[`p`, `p + n`) is a valid range.

*Effects:* Constructs a `valarray` that has length `n`. The values of
the elements of the array are initialized with the first `n` values
pointed to by the first argument.[^11]

``` cpp
valarray(const valarray& v);
```

*Effects:* Constructs a `valarray` that has the same length as `v`. The
elements are initialized with the values of the corresponding elements
of `v`.[^12]

``` cpp
valarray(valarray&& v) noexcept;
```

*Effects:* Constructs a `valarray` that has the same length as `v`. The
elements are initialized with the values of the corresponding elements
of `v`.

*Complexity:* Constant.

``` cpp
valarray(initializer_list<T> il);
```

*Effects:* Equivalent to `valarray(il.begin(), il.size())`.

``` cpp
valarray(const slice_array<T>&);
valarray(const gslice_array<T>&);
valarray(const mask_array<T>&);
valarray(const indirect_array<T>&);
```

These conversion constructors convert one of the four reference
templates to a `valarray`.

``` cpp
~valarray();
```

*Effects:* The destructor is applied to every element of `*this`; an
implementation may return all allocated memory.

#### Assignment <a id="valarray.assign">[[valarray.assign]]</a>

``` cpp
valarray& operator=(const valarray& v);
```

*Effects:* Each element of the `*this` array is assigned the value of
the corresponding element of `v`. If the length of `v` is not equal to
the length of `*this`, resizes `*this` to make the two arrays the same
length, as if by calling `resize(v.size())`, before performing the
assignment.

*Ensures:* `size() == v.size()`.

*Returns:* `*this`.

``` cpp
valarray& operator=(valarray&& v) noexcept;
```

*Effects:* `*this` obtains the value of `v`. The value of `v` after the
assignment is not specified.

*Returns:* `*this`.

*Complexity:* Linear.

``` cpp
valarray& operator=(initializer_list<T> il);
```

*Effects:* Equivalent to: `return *this = valarray(il);`

``` cpp
valarray& operator=(const T& v);
```

*Effects:* Assigns `v` to each element of `*this`.

*Returns:* `*this`.

``` cpp
valarray& operator=(const slice_array<T>&);
valarray& operator=(const gslice_array<T>&);
valarray& operator=(const mask_array<T>&);
valarray& operator=(const indirect_array<T>&);
```

*Preconditions:* The length of the array to which the argument refers
equals `size()`. The value of an element in the left-hand side of a
`valarray` assignment operator does not depend on the value of another
element in that left-hand side.

These operators allow the results of a generalized subscripting
operation to be assigned directly to a `valarray`.

#### Element access <a id="valarray.access">[[valarray.access]]</a>

``` cpp
const T& operator[](size_t n) const;
T& operator[](size_t n);
```

`n < size()` is `true`.

*Returns:* A reference to the corresponding element of the array.

[*Note 1*: The expression `(a[i] = q, a[i]) == q` evaluates to `true`
for any non-constant `valarray<T> a`, any `T q`, and for any `size_t i`
such that the value of `i` is less than the length of
`a`. — *end note*]

*Remarks:* The expression `addressof(a[i + j]) == addressof(a[i]) + j`
evaluates to `true` for all `size_t i` and `size_t j` such that
`i + j < a.size()`.

The expression `addressof(a[i]) != addressof(b[j])` evaluates to `true`
for any two arrays `a` and `b` and for any `size_t i` and `size_t j`
such that `i < a.size()` and `j < b.size()`.

[*Note 2*: This property indicates an absence of aliasing and can be
used to advantage by optimizing compilers. Compilers can take advantage
of inlining, constant propagation, loop fusion, tracking of pointers
obtained from `operator new`, and other techniques to generate efficient
`valarray`s. — *end note*]

The reference returned by the subscript operator for an array shall be
valid until the member function `resize(size_t, T)`[[valarray.members]]
is called for that array or until the lifetime of that array ends,
whichever happens first.

#### Subset operations <a id="valarray.sub">[[valarray.sub]]</a>

The member `operator[]` is overloaded to provide several ways to select
sequences of elements from among those controlled by `*this`. Each of
these operations returns a subset of the array. The const-qualified
versions return this subset as a new `valarray` object. The non-const
versions return a class template object which has reference semantics to
the original array, working in conjunction with various overloads of
`operator=` and other assigning operators to allow selective replacement
(slicing) of the controlled sequence. In each case the selected
element(s) shall exist.

``` cpp
valarray operator[](slice slicearr) const;
```

*Returns:* A `valarray` containing those elements of the controlled
sequence designated by `slicearr`.

[*Example 1*:

``` cpp
const valarray<char> v0("abcdefghijklmnop", 16);
// v0[slice(2, 5, 3)] returns valarray<char>("cfilo", 5)
```

— *end example*]

``` cpp
slice_array<T> operator[](slice slicearr);
```

*Returns:* An object that holds references to elements of the controlled
sequence selected by `slicearr`.

[*Example 2*:

``` cpp
valarray<char> v0("abcdefghijklmnop", 16);
valarray<char> v1("ABCDE", 5);
v0[slice(2, 5, 3)] = v1;
// v0 == valarray<char>("abAdeBghCjkDmnEp", 16);
```

— *end example*]

``` cpp
valarray operator[](const gslice& gslicearr) const;
```

*Returns:* A `valarray` containing those elements of the controlled
sequence designated by `gslicearr`.

[*Example 3*:

``` cpp
const valarray<char> v0("abcdefghijklmnop", 16);
const size_t lv[] = { 2, 3 };
const size_t dv[] = { 7, 2 };
const valarray<size_t> len(lv, 2), str(dv, 2);
// v0[gslice(3, len, str)] returns
// valarray<char>("dfhkmo", 6)
```

— *end example*]

``` cpp
gslice_array<T> operator[](const gslice& gslicearr);
```

*Returns:* An object that holds references to elements of the controlled
sequence selected by `gslicearr`.

[*Example 4*:

``` cpp
valarray<char> v0("abcdefghijklmnop", 16);
valarray<char> v1("ABCDEF", 6);
const size_t lv[] = { 2, 3 };
const size_t dv[] = { 7, 2 };
const valarray<size_t> len(lv, 2), str(dv, 2);
v0[gslice(3, len, str)] = v1;
// v0 == valarray<char>("abcAeBgCijDlEnFp", 16)
```

— *end example*]

``` cpp
valarray operator[](const valarray<bool>& boolarr) const;
```

*Returns:* A `valarray` containing those elements of the controlled
sequence designated by `boolarr`.

[*Example 5*:

``` cpp
const valarray<char> v0("abcdefghijklmnop", 16);
const bool vb[] = { false, false, true, true, false, true };
// v0[valarray<bool>(vb, 6)] returns
// valarray<char>("cdf", 3)
```

— *end example*]

``` cpp
mask_array<T> operator[](const valarray<bool>& boolarr);
```

*Returns:* An object that holds references to elements of the controlled
sequence selected by `boolarr`.

[*Example 6*:

``` cpp
valarray<char> v0("abcdefghijklmnop", 16);
valarray<char> v1("ABC", 3);
const bool vb[] = { false, false, true, true, false, true };
v0[valarray<bool>(vb, 6)] = v1;
// v0 == valarray<char>("abABeCghijklmnop", 16)
```

— *end example*]

``` cpp
valarray operator[](const valarray<size_t>& indarr) const;
```

*Returns:* A `valarray` containing those elements of the controlled
sequence designated by `indarr`.

[*Example 7*:

``` cpp
const valarray<char> v0("abcdefghijklmnop", 16);
const size_t vi[] = { 7, 5, 2, 3, 8 };
// v0[valarray<size_t>(vi, 5)] returns
// valarray<char>("hfcdi", 5)
```

— *end example*]

``` cpp
indirect_array<T> operator[](const valarray<size_t>& indarr);
```

*Returns:* An object that holds references to elements of the controlled
sequence selected by `indarr`.

[*Example 8*:

``` cpp
valarray<char> v0("abcdefghijklmnop", 16);
valarray<char> v1("ABCDE", 5);
const size_t vi[] = { 7, 5, 2, 3, 8 };
v0[valarray<size_t>(vi, 5)] = v1;
// v0 == valarray<char>("abCDeBgAEjklmnop", 16)
```

— *end example*]

#### Unary operators <a id="valarray.unary">[[valarray.unary]]</a>

\indexlibrarymember{operator~}{valarray}

``` cpp
valarray operator+() const;
valarray operator-() const;
valarray operator~() const;
valarray<bool> operator!() const;
```

*Mandates:* The indicated operator can be applied to operands of type
`T` and returns a value of type `T` (`bool` for `operator!`) or which
may be unambiguously implicitly converted to type `T` (`bool` for
`operator!`).

*Returns:* A `valarray` whose length is `size()`. Each element of the
returned array is initialized with the result of applying the indicated
operator to the corresponding element of the array.

#### Compound assignment <a id="valarray.cassign">[[valarray.cassign]]</a>

\indexlibrarymember{operator^=}{valarray}

``` cpp
valarray& operator*= (const valarray& v);
valarray& operator/= (const valarray& v);
valarray& operator%= (const valarray& v);
valarray& operator+= (const valarray& v);
valarray& operator-= (const valarray& v);
valarray& operator^= (const valarray& v);
valarray& operator&= (const valarray& v);
valarray& operator|= (const valarray& v);
valarray& operator<<=(const valarray& v);
valarray& operator>>=(const valarray& v);
```

*Mandates:* The indicated operator can be applied to two operands of
type `T`.

*Preconditions:* `size() == v.size()` is `true`.

The value of an element in the left-hand side of a valarray compound
assignment operator does not depend on the value of another element in
that left hand side.

*Effects:* Each of these operators performs the indicated operation on
each of the elements of `*this` and the corresponding element of `v`.

*Returns:* `*this`.

*Remarks:* The appearance of an array on the left-hand side of a
compound assignment does not invalidate references or pointers.

\indexlibrarymember{operator^=}{valarray}

``` cpp
valarray& operator*= (const T& v);
valarray& operator/= (const T& v);
valarray& operator%= (const T& v);
valarray& operator+= (const T& v);
valarray& operator-= (const T& v);
valarray& operator^= (const T& v);
valarray& operator&= (const T& v);
valarray& operator|= (const T& v);
valarray& operator<<=(const T& v);
valarray& operator>>=(const T& v);
```

*Mandates:* The indicated operator can be applied to two operands of
type `T`.

*Effects:* Each of these operators applies the indicated operation to
each element of `*this` and `v`.

*Returns:* `*this`.

*Remarks:* The appearance of an array on the left-hand side of a
compound assignment does not invalidate references or pointers to the
elements of the array.

#### Member functions <a id="valarray.members">[[valarray.members]]</a>

``` cpp
void swap(valarray& v) noexcept;
```

*Effects:* `*this` obtains the value of `v`. `v` obtains the value of
`*this`.

*Complexity:* Constant.

``` cpp
size_t size() const;
```

*Returns:* The number of elements in the array.

*Complexity:* Constant time.

``` cpp
T sum() const;
```

*Mandates:* `operator+=` can be applied to operands of type `T`.

*Preconditions:* `size() > 0` is `true`.

*Returns:* The sum of all the elements of the array. If the array has
length 1, returns the value of element 0. Otherwise, the returned value
is calculated by applying `operator+=` to a copy of an element of the
array and all other elements of the array in an unspecified order.

``` cpp
T min() const;
```

*Preconditions:* `size() > 0` is `true`.

*Returns:* The minimum value contained in `*this`. For an array of
length 1, the value of element 0 is returned. For all other array
lengths, the determination is made using `operator<`.

``` cpp
T max() const;
```

*Preconditions:* `size() > 0` is `true`.

*Returns:* The maximum value contained in `*this`. For an array of
length 1, the value of element 0 is returned. For all other array
lengths, the determination is made using `operator<`.

``` cpp
valarray shift(int n) const;
```

*Returns:* A `valarray` of length `size()`, each of whose elements *I*
is `(*this)[`*`I`*` + n]` if *`I`*` + n` is non-negative and less than
`size()`, otherwise `T()`.

[*Note 1*: If element zero is taken as the leftmost element, a positive
value of `n` shifts the elements left `n` places, with zero
fill. — *end note*]

[*Example 1*: If the argument has the value -2, the first two elements
of the result will be value-initialized [[dcl.init]]; the third element
of the result will be assigned the value of the first element of
`*this`; etc. — *end example*]

``` cpp
valarray cshift(int n) const;
```

*Returns:* A `valarray` of length `size()` that is a circular shift of
`*this`. If element zero is taken as the leftmost element, a
non-negative value of n shifts the elements circularly left n places and
a negative value of n shifts the elements circularly right -n places.

``` cpp
valarray apply(T func(T)) const;
valarray apply(T func(const T&)) const;
```

*Returns:* A `valarray` whose length is `size()`. Each element of the
returned array is assigned the value returned by applying the argument
function to the corresponding element of `*this`.

``` cpp
void resize(size_t sz, T c = T());
```

*Effects:* Changes the length of the `*this` array to `sz` and then
assigns to each element the value of the second argument. Resizing
invalidates all pointers and references to elements in the array.

### `valarray` non-member operations <a id="valarray.nonmembers">[[valarray.nonmembers]]</a>

#### Binary operators <a id="valarray.binary">[[valarray.binary]]</a>

\indexlibrarymember{operator^}{valarray}

``` cpp
template<class T> valarray<T> operator* (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator/ (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator% (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator+ (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator- (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator^ (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator& (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator| (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator<<(const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator>>(const valarray<T>&, const valarray<T>&);
```

*Mandates:* The indicated operator can be applied to operands of type
`T` and returns a value of type `T` or which can be unambiguously
implicitly converted to `T`.

*Preconditions:* The argument arrays have the same length.

*Returns:* A `valarray` whose length is equal to the lengths of the
argument arrays. Each element of the returned array is initialized with
the result of applying the indicated operator to the corresponding
elements of the argument arrays.

\indexlibrarymember{operator^}{valarray}

``` cpp
template<class T> valarray<T> operator* (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator* (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator/ (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator/ (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator% (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator% (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator+ (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator+ (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator- (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator- (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator^ (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator^ (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator& (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator& (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator| (const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator| (const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator<<(const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator<<(const typename valarray<T>::value_type&,
                                         const valarray<T>&);
template<class T> valarray<T> operator>>(const valarray<T>&,
                                         const typename valarray<T>::value_type&);
template<class T> valarray<T> operator>>(const typename valarray<T>::value_type&,
                                         const valarray<T>&);
```

*Mandates:* The indicated operator can be applied to operands of type
`T` and returns a value of type `T` or which can be unambiguously
implicitly converted to `T`.

*Returns:* A `valarray` whose length is equal to the length of the array
argument. Each element of the returned array is initialized with the
result of applying the indicated operator to the corresponding element
of the array argument and the non-array argument.

#### Logical operators <a id="valarray.comparison">[[valarray.comparison]]</a>

``` cpp
template<class T> valarray<bool> operator==(const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator!=(const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator< (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator> (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator<=(const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator>=(const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator&&(const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator||(const valarray<T>&, const valarray<T>&);
```

*Mandates:* The indicated operator can be applied to operands of type
`T` and returns a value of type `bool` or which can be unambiguously
implicitly converted to `bool`.

*Preconditions:* The two array arguments have the same length.

*Returns:* A `valarray<bool>` whose length is equal to the length of the
array arguments. Each element of the returned array is initialized with
the result of applying the indicated operator to the corresponding
elements of the argument arrays.

``` cpp
template<class T> valarray<bool> operator==(const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator==(const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator!=(const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator!=(const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator< (const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator< (const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator> (const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator> (const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator<=(const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator<=(const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator>=(const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator>=(const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator&&(const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator&&(const typename valarray<T>::value_type&,
                                            const valarray<T>&);
template<class T> valarray<bool> operator||(const valarray<T>&,
                                            const typename valarray<T>::value_type&);
template<class T> valarray<bool> operator||(const typename valarray<T>::value_type&,
                                            const valarray<T>&);
```

*Mandates:* The indicated operator can be applied to operands of type
`T` and returns a value of type `bool` or which can be unambiguously
implicitly converted to `bool`.

*Returns:* A `valarray<bool>` whose length is equal to the length of the
array argument. Each element of the returned array is initialized with
the result of applying the indicated operator to the corresponding
element of the array and the non-array argument.

#### Transcendentals <a id="valarray.transcend">[[valarray.transcend]]</a>

``` cpp
template<class T> valarray<T> abs  (const valarray<T>&);
template<class T> valarray<T> acos (const valarray<T>&);
template<class T> valarray<T> asin (const valarray<T>&);
template<class T> valarray<T> atan (const valarray<T>&);
template<class T> valarray<T> atan2(const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> atan2(const valarray<T>&, const typename valarray<T>::value_type&);
template<class T> valarray<T> atan2(const typename valarray<T>::value_type&, const valarray<T>&);
template<class T> valarray<T> cos  (const valarray<T>&);
template<class T> valarray<T> cosh (const valarray<T>&);
template<class T> valarray<T> exp  (const valarray<T>&);
template<class T> valarray<T> log  (const valarray<T>&);
template<class T> valarray<T> log10(const valarray<T>&);
template<class T> valarray<T> pow  (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> pow  (const valarray<T>&, const typename valarray<T>::value_type&);
template<class T> valarray<T> pow  (const typename valarray<T>::value_type&, const valarray<T>&);
template<class T> valarray<T> sin  (const valarray<T>&);
template<class T> valarray<T> sinh (const valarray<T>&);
template<class T> valarray<T> sqrt (const valarray<T>&);
template<class T> valarray<T> tan  (const valarray<T>&);
template<class T> valarray<T> tanh (const valarray<T>&);
```

*Mandates:* A unique function with the indicated name can be applied
(unqualified) to an operand of type `T`. This function returns a value
of type `T` or which can be unambiguously implicitly converted to type
`T`.

#### Specialized algorithms <a id="valarray.special">[[valarray.special]]</a>

``` cpp
template<class T> void swap(valarray<T>& x, valarray<T>& y) noexcept;
```

*Effects:* Equivalent to `x.swap(y)`.

### Class `slice` <a id="class.slice">[[class.slice]]</a>

#### Overview <a id="class.slice.overview">[[class.slice.overview]]</a>

``` cpp
namespace std {
  class slice {
  public:
    slice();
    slice(size_t, size_t, size_t);
    slice(const slice&);

    size_t start() const;
    size_t size() const;
    size_t stride() const;

    friend bool operator==(const slice& x, const slice& y);
  };
}
```

The `slice` class represents a BLAS-like slice from an array. Such a
slice is specified by a starting index, a length, and a stride.[^13]

#### Constructors <a id="cons.slice">[[cons.slice]]</a>

``` cpp
slice();
slice(size_t start, size_t length, size_t stride);
```

The default constructor is equivalent to `slice(0, 0, 0)`. A default
constructor is provided only to permit the declaration of arrays of
slices. The constructor with arguments for a slice takes a start,
length, and stride parameter.

[*Example 1*: `slice(3, 8, 2)` constructs a slice which selects
elements 3, 5, 7, …, 17 from an array. — *end example*]

#### Access functions <a id="slice.access">[[slice.access]]</a>

``` cpp
size_t start() const;
size_t size() const;
size_t stride() const;
```

*Returns:* The start, length, or stride specified by a `slice` object.

*Complexity:* Constant time.

#### Operators <a id="slice.ops">[[slice.ops]]</a>

``` cpp
friend bool operator==(const slice& x, const slice& y);
```

*Effects:* Equivalent to:

``` cpp
return x.start() == y.start() && x.size() == y.size() && x.stride() == y.stride();
```

### Class template `slice_array` <a id="template.slice.array">[[template.slice.array]]</a>

#### Overview <a id="template.slice.array.overview">[[template.slice.array.overview]]</a>

``` cpp
namespace std {
  template<class T> class slice_array {
  public:
    using value_type = T;

    void operator=  (const valarray<T>&) const;
    void operator*= (const valarray<T>&) const;
    void operator/= (const valarray<T>&) const;
    void operator%= (const valarray<T>&) const;
    void operator+= (const valarray<T>&) const;
    void operator-= (const valarray<T>&) const;
    void operator^= (const valarray<T>&) const;
    void operator&= (const valarray<T>&) const;
    void operator|= (const valarray<T>&) const;
    void operator<<=(const valarray<T>&) const;
    void operator>>=(const valarray<T>&) const;

    slice_array(const slice_array&);
    ~slice_array();
    const slice_array& operator=(const slice_array&) const;
    void operator=(const T&) const;

    slice_array() = delete;     // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the `slice` subscript
operator

``` cpp
slice_array<T> valarray<T>::operator[](slice);
```

It has reference semantics to a subset of an array specified by a
`slice` object.

[*Example 1*: The expression `a[slice(1, 5, 3)] = b;` has the effect of
assigning the elements of `b` to a slice of the elements in `a`. For the
slice shown, the elements selected from `a` are
1, 4, …, 13. — *end example*]

#### Assignment <a id="slice.arr.assign">[[slice.arr.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const slice_array& operator=(const slice_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which the `slice_array` object refers.

#### Compound assignment <a id="slice.arr.comp.assign">[[slice.arr.comp.assign]]</a>

\indexlibrarymember{operator^=}{slice_array}

``` cpp
void operator*= (const valarray<T>&) const;
void operator/= (const valarray<T>&) const;
void operator%= (const valarray<T>&) const;
void operator+= (const valarray<T>&) const;
void operator-= (const valarray<T>&) const;
void operator^= (const valarray<T>&) const;
void operator&= (const valarray<T>&) const;
void operator|= (const valarray<T>&) const;
void operator<<=(const valarray<T>&) const;
void operator>>=(const valarray<T>&) const;
```

These compound assignments have reference semantics, applying the
indicated operation to the elements of the argument array and selected
elements of the `valarray<T>` object to which the `slice_array` object
refers.

#### Fill function <a id="slice.arr.fill">[[slice.arr.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`slice_array` object refers.

### The `gslice` class <a id="class.gslice">[[class.gslice]]</a>

#### Overview <a id="class.gslice.overview">[[class.gslice.overview]]</a>

``` cpp
namespace std {
  class gslice {
  public:
    gslice();
    gslice(size_t s, const valarray<size_t>& l, const valarray<size_t>& d);

    size_t           start() const;
    valarray<size_t> size() const;
    valarray<size_t> stride() const;
  };
}
```

This class represents a generalized slice out of an array. A `gslice` is
defined by a starting offset (s), a set of lengths (lⱼ), and a set of
strides (dⱼ). The number of lengths shall equal the number of strides.

A `gslice` represents a mapping from a set of indices (iⱼ), equal in
number to the number of strides, to a single index k. It is useful for
building multidimensional array classes using the `valarray` template,
which is one-dimensional. The set of one-dimensional index values
specified by a `gslice` are $$k = s + \sum_j i_j d_j$$ where the
multidimensional indices iⱼ range in value from 0 to lᵢⱼ - 1.

[*Example 1*:

The `gslice` specification

``` cpp
start  = 3
length = {2, 4, 3}
stride = {19, 4, 1}
```

yields the sequence of one-dimensional indices
$$k = 3 + (0, 1) \times 19 + (0, 1, 2, 3) \times 4 + (0, 1, 2) \times 1$$
which are ordered as shown in the following table:

That is, the highest-ordered index turns fastest.

— *end example*]

It is possible to have degenerate generalized slices in which an address
is repeated.

[*Example 2*:

If the stride parameters in the previous example are changed to {1, 1,
1}, the first few elements of the resulting sequence of indices will be

— *end example*]

If a degenerate slice is used as the argument to the non-`const` version
of `operator[](const gslice&)`, the behavior is undefined.

#### Constructors <a id="gslice.cons">[[gslice.cons]]</a>

``` cpp
gslice();
gslice(size_t start, const valarray<size_t>& lengths,
       const valarray<size_t>& strides);
```

The default constructor is equivalent to
`gslice(0, valarray<size_t>(), valarray<size_t>())`. The constructor
with arguments builds a `gslice` based on a specification of start,
lengths, and strides, as explained in the previous subclause.

#### Access functions <a id="gslice.access">[[gslice.access]]</a>

``` cpp
size_t           start()  const;
valarray<size_t> size() const;
valarray<size_t> stride() const;
```

*Returns:* The representation of the start, lengths, or strides
specified for the `gslice`.

*Complexity:* `start()` is constant time. `size()` and `stride()` are
linear in the number of strides.

### Class template `gslice_array` <a id="template.gslice.array">[[template.gslice.array]]</a>

#### Overview <a id="template.gslice.array.overview">[[template.gslice.array.overview]]</a>

``` cpp
namespace std {
  template<class T> class gslice_array {
  public:
    using value_type = T;

    void operator=  (const valarray<T>&) const;
    void operator*= (const valarray<T>&) const;
    void operator/= (const valarray<T>&) const;
    void operator%= (const valarray<T>&) const;
    void operator+= (const valarray<T>&) const;
    void operator-= (const valarray<T>&) const;
    void operator^= (const valarray<T>&) const;
    void operator&= (const valarray<T>&) const;
    void operator|= (const valarray<T>&) const;
    void operator<<=(const valarray<T>&) const;
    void operator>>=(const valarray<T>&) const;

    gslice_array(const gslice_array&);
    ~gslice_array();
    const gslice_array& operator=(const gslice_array&) const;
    void operator=(const T&) const;

    gslice_array() = delete;    // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the `gslice` subscript
operator

``` cpp
gslice_array<T> valarray<T>::operator[](const gslice&);
```

It has reference semantics to a subset of an array specified by a
`gslice` object. Thus, the expression `a[gslice(1, length, stride)] = b`
has the effect of assigning the elements of `b` to a generalized slice
of the elements in `a`.

#### Assignment <a id="gslice.array.assign">[[gslice.array.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const gslice_array& operator=(const gslice_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which the `gslice_array` refers.

#### Compound assignment <a id="gslice.array.comp.assign">[[gslice.array.comp.assign]]</a>

\indexlibrarymember{operator^=}{gslice_array}

``` cpp
void operator*= (const valarray<T>&) const;
void operator/= (const valarray<T>&) const;
void operator%= (const valarray<T>&) const;
void operator+= (const valarray<T>&) const;
void operator-= (const valarray<T>&) const;
void operator^= (const valarray<T>&) const;
void operator&= (const valarray<T>&) const;
void operator|= (const valarray<T>&) const;
void operator<<=(const valarray<T>&) const;
void operator>>=(const valarray<T>&) const;
```

These compound assignments have reference semantics, applying the
indicated operation to the elements of the argument array and selected
elements of the `valarray<T>` object to which the `gslice_array` object
refers.

#### Fill function <a id="gslice.array.fill">[[gslice.array.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`gslice_array` object refers.

### Class template `mask_array` <a id="template.mask.array">[[template.mask.array]]</a>

#### Overview <a id="template.mask.array.overview">[[template.mask.array.overview]]</a>

``` cpp
namespace std {
  template<class T> class mask_array {
  public:
    using value_type = T;

    void operator=  (const valarray<T>&) const;
    void operator*= (const valarray<T>&) const;
    void operator/= (const valarray<T>&) const;
    void operator%= (const valarray<T>&) const;
    void operator+= (const valarray<T>&) const;
    void operator-= (const valarray<T>&) const;
    void operator^= (const valarray<T>&) const;
    void operator&= (const valarray<T>&) const;
    void operator|= (const valarray<T>&) const;
    void operator<<=(const valarray<T>&) const;
    void operator>>=(const valarray<T>&) const;

    mask_array(const mask_array&);
    ~mask_array();
    const mask_array& operator=(const mask_array&) const;
    void operator=(const T&) const;

    mask_array() = delete;      // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the mask subscript operator:

``` cpp
mask_array<T> valarray<T>::operator[](const valarray<bool>&);
```

It has reference semantics to a subset of an array specified by a
boolean mask. Thus, the expression `a[mask] = b;` has the effect of
assigning the elements of `b` to the masked elements in `a` (those for
which the corresponding element in `mask` is `true`).

#### Assignment <a id="mask.array.assign">[[mask.array.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const mask_array& operator=(const mask_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which the `mask_array` object refers.

#### Compound assignment <a id="mask.array.comp.assign">[[mask.array.comp.assign]]</a>

\indexlibrarymember{operator^=}{mask_array}

``` cpp
void operator*= (const valarray<T>&) const;
void operator/= (const valarray<T>&) const;
void operator%= (const valarray<T>&) const;
void operator+= (const valarray<T>&) const;
void operator-= (const valarray<T>&) const;
void operator^= (const valarray<T>&) const;
void operator&= (const valarray<T>&) const;
void operator|= (const valarray<T>&) const;
void operator<<=(const valarray<T>&) const;
void operator>>=(const valarray<T>&) const;
```

These compound assignments have reference semantics, applying the
indicated operation to the elements of the argument array and selected
elements of the `valarray<T>` object to which the `mask_array` object
refers.

#### Fill function <a id="mask.array.fill">[[mask.array.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`mask_array` object refers.

### Class template `indirect_array` <a id="template.indirect.array">[[template.indirect.array]]</a>

#### Overview <a id="template.indirect.array.overview">[[template.indirect.array.overview]]</a>

``` cpp
namespace std {
  template<class T> class indirect_array {
  public:
    using value_type = T;

    void operator=  (const valarray<T>&) const;
    void operator*= (const valarray<T>&) const;
    void operator/= (const valarray<T>&) const;
    void operator%= (const valarray<T>&) const;
    void operator+= (const valarray<T>&) const;
    void operator-= (const valarray<T>&) const;
    void operator^= (const valarray<T>&) const;
    void operator&= (const valarray<T>&) const;
    void operator|= (const valarray<T>&) const;
    void operator<<=(const valarray<T>&) const;
    void operator>>=(const valarray<T>&) const;

    indirect_array(const indirect_array&);
    ~indirect_array();
    const indirect_array& operator=(const indirect_array&) const;
    void operator=(const T&) const;

    indirect_array() = delete;  // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the indirect subscript
operator

``` cpp
indirect_array<T> valarray<T>::operator[](const valarray<size_t>&);
```

It has reference semantics to a subset of an array specified by an
`indirect_array`. Thus, the expression `a[{}indirect] = b;` has the
effect of assigning the elements of `b` to the elements in `a` whose
indices appear in `indirect`.

#### Assignment <a id="indirect.array.assign">[[indirect.array.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const indirect_array& operator=(const indirect_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which it refers.

If the `indirect_array` specifies an element in the `valarray<T>` object
to which it refers more than once, the behavior is undefined.

[*Example 1*:

``` cpp
int addr[] = {2, 3, 1, 4, 4};
valarray<size_t> indirect(addr, 5);
valarray<double> a(0., 10), b(1., 5);
a[indirect] = b;
```

results in undefined behavior since element 4 is specified twice in the
indirection.

— *end example*]

#### Compound assignment <a id="indirect.array.comp.assign">[[indirect.array.comp.assign]]</a>

\indexlibrarymember{operator^=}{indirect_array}

``` cpp
void operator*= (const valarray<T>&) const;
void operator/= (const valarray<T>&) const;
void operator%= (const valarray<T>&) const;
void operator+= (const valarray<T>&) const;
void operator-= (const valarray<T>&) const;
void operator^= (const valarray<T>&) const;
void operator&= (const valarray<T>&) const;
void operator|= (const valarray<T>&) const;
void operator<<=(const valarray<T>&) const;
void operator>>=(const valarray<T>&) const;
```

These compound assignments have reference semantics, applying the
indicated operation to the elements of the argument array and selected
elements of the `valarray<T>` object to which the `indirect_array`
object refers.

If the `indirect_array` specifies an element in the `valarray<T>` object
to which it refers more than once, the behavior is undefined.

#### Fill function <a id="indirect.array.fill">[[indirect.array.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`indirect_array` object refers.

### `valarray` range access <a id="valarray.range">[[valarray.range]]</a>

In the `begin` and `end` function templates that follow, *unspecified*1
is a type that meets the requirements of a mutable
*Cpp17RandomAccessIterator* [[random.access.iterators]] and models
`contiguous_iterator` [[iterator.concept.contiguous]], whose
`value_type` is the template parameter `T` and whose `reference` type is
`T&`. *unspecified*2 is a type that meets the requirements of a constant
*Cpp17RandomAccessIterator* and models `contiguous_iterator`, whose
`value_type` is the template parameter `T` and whose `reference` type is
`const T&`.

The iterators returned by `begin` and `end` for an array are guaranteed
to be valid until the member function `resize(size_t, T)`
[[valarray.members]] is called for that array or until the lifetime of
that array ends, whichever happens first.

``` cpp
template<class T> unspecified{1} begin(valarray<T>& v);
template<class T> unspecified{2} begin(const valarray<T>& v);
```

*Returns:* An iterator referencing the first value in the array.

``` cpp
template<class T> unspecified{1} end(valarray<T>& v);
template<class T> unspecified{2} end(const valarray<T>& v);
```

*Returns:* An iterator referencing one past the last value in the array.

## Mathematical functions for floating-point types <a id="c.math">[[c.math]]</a>

### Header `<cmath>` synopsis <a id="cmath.syn">[[cmath.syn]]</a>

``` cpp
#define \libmacro{HUGE_VAL} see below
#define \libmacro{HUGE_VALF} see below
#define \libmacro{HUGE_VALL} see below
#define \libmacro{INFINITY} see below
#define \libmacro{NAN} see below
#define \libmacro{FP_INFINITE} see below
#define \libmacro{FP_NAN} see below
#define \libmacro{FP_NORMAL} see below
#define \libmacro{FP_SUBNORMAL} see below
#define \libmacro{FP_ZERO} see below
#define \libmacro{FP_FAST_FMA} see below
#define \libmacro{FP_FAST_FMAF} see below
#define \libmacro{FP_FAST_FMAL} see below
#define \libmacro{FP_ILOGB0} see below
#define \libmacro{FP_ILOGBNAN} see below
#define \libmacro{MATH_ERRNO} see below
#define \libmacro{MATH_ERREXCEPT} see below

#define \libmacro{math_errhandling} see below

namespace std {
  using float_t = see below;
  using double_t = see below;

  constexpr floating-point-type acos(floating-point-type x);
  constexpr float               acosf(float x);
  constexpr long double         acosl(long double x);

  constexpr floating-point-type asin(floating-point-type x);
  constexpr float               asinf(float x);
  constexpr long double         asinl(long double x);

  constexpr floating-point-type atan(floating-point-type x);
  constexpr float               atanf(float x);
  constexpr long double         atanl(long double x);

  constexpr floating-point-type atan2(floating-point-type y, floating-point-type x);
  constexpr float               atan2f(float y, float x);
  constexpr long double         atan2l(long double y, long double x);

  constexpr floating-point-type cos(floating-point-type x);
  constexpr float               cosf(float x);
  constexpr long double         cosl(long double x);

  constexpr floating-point-type sin(floating-point-type x);
  constexpr float               sinf(float x);
  constexpr long double         sinl(long double x);

  constexpr floating-point-type tan(floating-point-type x);
  constexpr float               tanf(float x);
  constexpr long double         tanl(long double x);

  constexpr floating-point-type acosh(floating-point-type x);
  constexpr float               acoshf(float x);
  constexpr long double         acoshl(long double x);

  constexpr floating-point-type asinh(floating-point-type x);
  constexpr float               asinhf(float x);
  constexpr long double         asinhl(long double x);

  constexpr floating-point-type atanh(floating-point-type x);
  constexpr float               atanhf(float x);
  constexpr long double         atanhl(long double x);

  constexpr floating-point-type cosh(floating-point-type x);
  constexpr float               coshf(float x);
  constexpr long double         coshl(long double x);

  constexpr floating-point-type sinh(floating-point-type x);
  constexpr float               sinhf(float x);
  constexpr long double         sinhl(long double x);

  constexpr floating-point-type tanh(floating-point-type x);
  constexpr float               tanhf(float x);
  constexpr long double         tanhl(long double x);

  constexpr floating-point-type exp(floating-point-type x);
  constexpr float               expf(float x);
  constexpr long double         expl(long double x);

  constexpr floating-point-type exp2(floating-point-type x);
  constexpr float               exp2f(float x);
  constexpr long double         exp2l(long double x);

  constexpr floating-point-type expm1(floating-point-type x);
  constexpr float               expm1f(float x);
  constexpr long double         expm1l(long double x);

  constexpr floating-point-type frexp(floating-point-type value, int* exp);
  constexpr float               frexpf(float value, int* exp);
  constexpr long double         frexpl(long double value, int* exp);

  constexpr int ilogb(floating-point-type x);
  constexpr int ilogbf(float x);
  constexpr int ilogbl(long double x);

  constexpr floating-point-type ldexp(floating-point-type x, int exp);
  constexpr float               ldexpf(float x, int exp);
  constexpr long double         ldexpl(long double x, int exp);

  constexpr floating-point-type log(floating-point-type x);
  constexpr float               logf(float x);
  constexpr long double         logl(long double x);

  constexpr floating-point-type log10(floating-point-type x);
  constexpr float               log10f(float x);
  constexpr long double         log10l(long double x);

  constexpr floating-point-type log1p(floating-point-type x);
  constexpr float               log1pf(float x);
  constexpr long double         log1pl(long double x);

  constexpr floating-point-type log2(floating-point-type x);
  constexpr float               log2f(float x);
  constexpr long double         log2l(long double x);

  constexpr floating-point-type logb(floating-point-type x);
  constexpr float               logbf(float x);
  constexpr long double         logbl(long double x);

  constexpr floating-point-type modf(floating-point-type value, floating-point-type* iptr);
  constexpr float               modff(float value, float* iptr);
  constexpr long double         modfl(long double value, long double* iptr);

  constexpr floating-point-type scalbn(floating-point-type x, int n);
  constexpr float               scalbnf(float x, int n);
  constexpr long double         scalbnl(long double x, int n);

  constexpr floating-point-type scalbln(floating-point-type x, long int n);
  constexpr float               scalblnf(float x, long int n);
  constexpr long double         scalblnl(long double x, long int n);

  constexpr floating-point-type cbrt(floating-point-type x);
  constexpr float               cbrtf(float x);
  constexpr long double         cbrtl(long double x);

  // [c.math.abs], absolute values
  constexpr int                 abs(int j);                             // freestanding
  constexpr long int            abs(long int j);                        // freestanding
  constexpr long long int       abs(long long int j);                   // freestanding
  constexpr floating-point-type abs(floating-point-type j);             // freestanding-deleted

  constexpr floating-point-type fabs(floating-point-type x);
  constexpr float               fabsf(float x);
  constexpr long double         fabsl(long double x);

  constexpr floating-point-type hypot(floating-point-type x, floating-point-type y);
  constexpr float               hypotf(float x, float y);
  constexpr long double         hypotl(long double x, long double y);

  // [c.math.hypot3], three-dimensional hypotenuse
  constexpr floating-point-type hypot(floating-point-type x, floating-point-type y,
                                      floating-point-type z);

  constexpr floating-point-type pow(floating-point-type x, floating-point-type y);
  constexpr float               powf(float x, float y);
  constexpr long double         powl(long double x, long double y);

  constexpr floating-point-type sqrt(floating-point-type x);
  constexpr float               sqrtf(float x);
  constexpr long double         sqrtl(long double x);

  constexpr floating-point-type erf(floating-point-type x);
  constexpr float               erff(float x);
  constexpr long double         erfl(long double x);

  constexpr floating-point-type erfc(floating-point-type x);
  constexpr float               erfcf(float x);
  constexpr long double         erfcl(long double x);

  constexpr floating-point-type lgamma(floating-point-type x);
  constexpr float               lgammaf(float x);
  constexpr long double         lgammal(long double x);

  constexpr floating-point-type tgamma(floating-point-type x);
  constexpr float               tgammaf(float x);
  constexpr long double         tgammal(long double x);

  constexpr floating-point-type ceil(floating-point-type x);
  constexpr float               ceilf(float x);
  constexpr long double         ceill(long double x);

  constexpr floating-point-type floor(floating-point-type x);
  constexpr float               floorf(float x);
  constexpr long double         floorl(long double x);

  floating-point-type nearbyint(floating-point-type x);
  float               nearbyintf(float x);
  long double         nearbyintl(long double x);

  floating-point-type rint(floating-point-type x);
  float               rintf(float x);
  long double         rintl(long double x);

  long int lrint(floating-point-type x);
  long int lrintf(float x);
  long int lrintl(long double x);

  long long int llrint(floating-point-type x);
  long long int llrintf(float x);
  long long int llrintl(long double x);

  constexpr floating-point-type round(floating-point-type x);
  constexpr float               roundf(float x);
  constexpr long double         roundl(long double x);

  constexpr long int lround(floating-point-type x);
  constexpr long int lroundf(float x);
  constexpr long int lroundl(long double x);

  constexpr long long int llround(floating-point-type x);
  constexpr long long int llroundf(float x);
  constexpr long long int llroundl(long double x);

  constexpr floating-point-type trunc(floating-point-type x);
  constexpr float               truncf(float x);
  constexpr long double         truncl(long double x);

  constexpr floating-point-type fmod(floating-point-type x, floating-point-type y);
  constexpr float               fmodf(float x, float y);
  constexpr long double         fmodl(long double x, long double y);

  constexpr floating-point-type remainder(floating-point-type x, floating-point-type y);
  constexpr float               remainderf(float x, float y);
  constexpr long double         remainderl(long double x, long double y);

  constexpr floating-point-type remquo(floating-point-type x, floating-point-type y, int* quo);
  constexpr float               remquof(float x, float y, int* quo);
  constexpr long double         remquol(long double x, long double y, int* quo);

  constexpr floating-point-type copysign(floating-point-type x, floating-point-type y);
  constexpr float               copysignf(float x, float y);
  constexpr long double         copysignl(long double x, long double y);

  double      nan(const char* tagp);
  float       nanf(const char* tagp);
  long double nanl(const char* tagp);

  constexpr floating-point-type nextafter(floating-point-type x, floating-point-type y);
  constexpr float               nextafterf(float x, float y);
  constexpr long double         nextafterl(long double x, long double y);

  constexpr floating-point-type nexttoward(floating-point-type x, long double y);
  constexpr float               nexttowardf(float x, long double y);
  constexpr long double         nexttowardl(long double x, long double y);

  constexpr floating-point-type nextup(floating-point-type x);
  constexpr float               nextupf(float x);
  constexpr long double         nextupl(long double x);

  constexpr floating-point-type nextdown(floating-point-type x);
  constexpr float               nextdownf(float x);
  constexpr long double         nextdownl(long double x);

  constexpr floating-point-type fdim(floating-point-type x, floating-point-type y);
  constexpr float               fdimf(float x, float y);
  constexpr long double         fdiml(long double x, long double y);

  constexpr floating-point-type fmax(floating-point-type x, floating-point-type y);
  constexpr float               fmaxf(float x, float y);
  constexpr long double         fmaxl(long double x, long double y);

  constexpr floating-point-type fmin(floating-point-type x, floating-point-type y);
  constexpr float               fminf(float x, float y);
  constexpr long double         fminl(long double x, long double y);

  constexpr floating-point-type fmaximum(floating-point-type x, floating-point-type y);
  constexpr floating-point-type fmaximum_num(floating-point-type x, floating-point-type y);
  constexpr floating-point-type fminimum(floating-point-type x, floating-point-type y);
  constexpr floating-point-type fminimum_num(floating-point-type x, floating-point-type y);

  constexpr floating-point-type fma(floating-point-type x, floating-point-type y,
                                    floating-point-type z);
  constexpr float               fmaf(float x, float y, float z);
  constexpr long double         fmal(long double x, long double y, long double z);

  // [c.math.lerp], linear interpolation
  constexpr floating-point-type lerp(floating-point-type a, floating-point-type b,
                                     floating-point-type t) noexcept;

  // [c.math.fpclass], classification / comparison functions
  constexpr int fpclassify(floating-point-type x);
  constexpr bool isfinite(floating-point-type x);
  constexpr bool isinf(floating-point-type x);
  constexpr bool isnan(floating-point-type x);
  constexpr bool isnormal(floating-point-type x);
  constexpr bool signbit(floating-point-type x);
  constexpr bool isgreater(floating-point-type x, floating-point-type y);
  constexpr bool isgreaterequal(floating-point-type x, floating-point-type y);
  constexpr bool isless(floating-point-type x, floating-point-type y);
  constexpr bool islessequal(floating-point-type x, floating-point-type y);
  constexpr bool islessgreater(floating-point-type x, floating-point-type y);
  constexpr bool isunordered(floating-point-type x, floating-point-type y);

  // [sf.cmath], mathematical special functions

  // [sf.cmath.assoc.laguerre], associated Laguerre polynomials
  floating-point-type assoc_laguerre(unsigned n, unsigned m, floating-point-type x);
  float               assoc_laguerref(unsigned n, unsigned m, float x);
  long double         assoc_laguerrel(unsigned n, unsigned m, long double x);

  // [sf.cmath.assoc.legendre], associated Legendre functions
  floating-point-type assoc_legendre(unsigned l, unsigned m, floating-point-type x);
  float               assoc_legendref(unsigned l, unsigned m, float x);
  long double         assoc_legendrel(unsigned l, unsigned m, long double x);

  // [sf.cmath.beta], beta function
  floating-point-type beta(floating-point-type x, floating-point-type y);
  float               betaf(float x, float y);
  long double         betal(long double x, long double y);

  // [sf.cmath.comp.ellint.1], complete elliptic integral of the first kind
  floating-point-type comp_ellint_1(floating-point-type k);
  float               comp_ellint_1f(float k);
  long double         comp_ellint_1l(long double k);

  // [sf.cmath.comp.ellint.2], complete elliptic integral of the second kind
  floating-point-type comp_ellint_2(floating-point-type k);
  float               comp_ellint_2f(float k);
  long double         comp_ellint_2l(long double k);

  // [sf.cmath.comp.ellint.3], complete elliptic integral of the third kind
  floating-point-type comp_ellint_3(floating-point-type k, floating-point-type nu);
  float               comp_ellint_3f(float k, float nu);
  long double         comp_ellint_3l(long double k, long double nu);

  // [sf.cmath.cyl.bessel.i], regular modified cylindrical Bessel functions
  floating-point-type cyl_bessel_i(floating-point-type nu, floating-point-type x);
  float               cyl_bessel_if(float nu, float x);
  long double         cyl_bessel_il(long double nu, long double x);

  // [sf.cmath.cyl.bessel.j], cylindrical Bessel functions of the first kind
  floating-point-type cyl_bessel_j(floating-point-type nu, floating-point-type x);
  float               cyl_bessel_jf(float nu, float x);
  long double         cyl_bessel_jl(long double nu, long double x);

  // [sf.cmath.cyl.bessel.k], irregular modified cylindrical Bessel functions
  floating-point-type cyl_bessel_k(floating-point-type nu, floating-point-type x);
  float               cyl_bessel_kf(float nu, float x);
  long double         cyl_bessel_kl(long double nu, long double x);

  // [sf.cmath.cyl.neumann], cylindrical Neumann functions
  // cylindrical Bessel functions of the second kind
  floating-point-type cyl_neumann(floating-point-type nu, floating-point-type x);
  float               cyl_neumannf(float nu, float x);
  long double         cyl_neumannl(long double nu, long double x);

  // [sf.cmath.ellint.1], incomplete elliptic integral of the first kind
  floating-point-type ellint_1(floating-point-type k, floating-point-type phi);
  float               ellint_1f(float k, float phi);
  long double         ellint_1l(long double k, long double phi);

  // [sf.cmath.ellint.2], incomplete elliptic integral of the second kind
  floating-point-type ellint_2(floating-point-type k, floating-point-type phi);
  float               ellint_2f(float k, float phi);
  long double         ellint_2l(long double k, long double phi);

  // [sf.cmath.ellint.3], incomplete elliptic integral of the third kind
  floating-point-type ellint_3(floating-point-type k, floating-point-type nu,
                                 floating-point-type phi);
  float               ellint_3f(float k, float nu, float phi);
  long double         ellint_3l(long double k, long double nu, long double phi);

  // [sf.cmath.expint], exponential integral
  floating-point-type expint(floating-point-type x);
  float               expintf(float x);
  long double         expintl(long double x);

  // [sf.cmath.hermite], Hermite polynomials
  floating-point-type hermite(unsigned n, floating-point-type x);
  float               hermitef(unsigned n, float x);
  long double         hermitel(unsigned n, long double x);

  // [sf.cmath.laguerre], Laguerre polynomials
  floating-point-type laguerre(unsigned n, floating-point-type x);
  float               laguerref(unsigned n, float x);
  long double         laguerrel(unsigned n, long double x);

  // [sf.cmath.legendre], Legendre polynomials
  floating-point-type legendre(unsigned l, floating-point-type x);
  float               legendref(unsigned l, float x);
  long double         legendrel(unsigned l, long double x);

  // [sf.cmath.riemann.zeta], Riemann zeta function
  floating-point-type riemann_zeta(floating-point-type x);
  float               riemann_zetaf(float x);
  long double         riemann_zetal(long double x);

  // [sf.cmath.sph.bessel], spherical Bessel functions of the first kind
  floating-point-type sph_bessel(unsigned n, floating-point-type x);
  float               sph_besself(unsigned n, float x);
  long double         sph_bessell(unsigned n, long double x);

  // [sf.cmath.sph.legendre], spherical associated Legendre functions
  floating-point-type sph_legendre(unsigned l, unsigned m, floating-point-type theta);
  float               sph_legendref(unsigned l, unsigned m, float theta);
  long double         sph_legendrel(unsigned l, unsigned m, long double theta);

  // [sf.cmath.sph.neumann], spherical Neumann functions;
  // spherical Bessel functions of the second kind
  floating-point-type sph_neumann(unsigned n, floating-point-type x);
  float               sph_neumannf(unsigned n, float x);
  long double         sph_neumannl(unsigned n, long double x);
}
```

The contents and meaning of the header `<cmath>` are a subset of the C
standard library header `<math.h>` and only the declarations shown in
the synopsis above are present, with the addition of a three-dimensional
hypotenuse function [[c.math.hypot3]], a linear interpolation function
[[c.math.lerp]], and the mathematical special functions described in
[[sf.cmath]].

[*Note 1*: Several functions have additional overloads in this
document, but they have the same behavior as in the C standard library
[[library.c]]. — *end note*]

For each function with at least one parameter of type
`floating-point-type`, the implementation provides an overload for each
cv-unqualified floating-point type [[basic.fundamental]] where all uses
of `floating-point-type` in the function signature are replaced with
that floating-point type.

For each function with at least one parameter of type
`floating-point-type` other than `abs`, the implementation also provides
additional overloads sufficient to ensure that, if every argument
corresponding to a `floating-point-type` parameter has arithmetic type,
then every such argument is effectively cast to the floating-point type
with the greatest floating-point conversion rank and greatest
floating-point conversion subrank among the types of all such arguments,
where arguments of integer type are considered to have the same
floating-point conversion rank as `double`. If no such floating-point
type with the greatest rank and subrank exists, then overload resolution
does not result in a usable candidate [[over.match.general]] from the
overloads provided by the implementation.

An invocation of `nexttoward` is ill-formed if the argument
corresponding to the `floating-point-type` parameter has extended
floating-point type.

### Absolute values <a id="c.math.abs">[[c.math.abs]]</a>

[*Note 1*: The headers `<cstdlib>` and `<cmath>` declare the functions
described in this subclause. — *end note*]

``` cpp
constexpr int abs(int j);
constexpr long int abs(long int j);
constexpr long long int abs(long long int j);
```

*Effects:* These functions have the semantics specified in the C
standard library for the functions `abs`, `labs`, and `llabs`,
respectively.

*Remarks:* If `abs` is called with an argument of type `X` for which
`is_unsigned_v<X>` is `true` and if `X` cannot be converted to `int` by
integral promotion [[conv.prom]], the program is ill-formed.

[*Note 1*: Allowing arguments that can be promoted to `int` provides
compatibility with C. — *end note*]

``` cpp
constexpr floating-point-type abs(floating-point-type x);
```

*Returns:* The absolute value of `x`.

### Three-dimensional hypotenuse <a id="c.math.hypot3">[[c.math.hypot3]]</a>

``` cpp
constexpr floating-point-type hypot(floating-point-type x, floating-point-type y,
                                    floating-point-type z);
```

*Returns:* $\sqrt{x^2+y^2+z^2}$.

### Linear interpolation <a id="c.math.lerp">[[c.math.lerp]]</a>

``` cpp
constexpr floating-point-type lerp(floating-point-type a, floating-point-type b,
                                   floating-point-type t) noexcept;
```

*Returns:* a+t(b-a).

*Remarks:* Let `r` be the value returned. If
`isfinite(a) && isfinite(b)`, then:

- If `t == 0`, then `r == a`.
- If `t == 1`, then `r == b`.
- If `t >= 0 && t <= 1`, then `isfinite(r)`.
- If `isfinite(t) && a == b`, then `r == a`.
- If `isfinite(t) || !isnan(t) && b - a != 0`, then `!isnan(r)`.

Let *`CMP`*`(x,y)` be `1` if `x > y`, `-1` if `x < y`, and `0`
otherwise. For any `t1` and `t2`, the product of
*`CMP`*`(lerp(a, b, t2), lerp(a, b, t1))`, *`CMP`*`(t2, t1)`, and
*`CMP`*`(b, a)` is non-negative.

### Classification / comparison functions <a id="c.math.fpclass">[[c.math.fpclass]]</a>

The classification / comparison functions behave the same as the C
macros with the corresponding names defined in the C standard library.

### Mathematical special functions <a id="sf.cmath">[[sf.cmath]]</a>

#### General <a id="sf.cmath.general">[[sf.cmath.general]]</a>

If any argument value to any of the functions specified in [[sf.cmath]]
is a NaN (Not a Number), the function shall return a NaN but it shall
not report a domain error. Otherwise, the function shall report a domain
error for just those argument values for which:

- the function description’s *Returns:* element explicitly specifies a
  domain and those argument values fall outside the specified domain, or
- the corresponding mathematical function value has a nonzero imaginary
  component, or
- the corresponding mathematical function is not mathematically
  defined.[^14]

Unless otherwise specified, each function is defined for all finite
values, for negative infinity, and for positive infinity.

#### Associated Laguerre polynomials <a id="sf.cmath.assoc.laguerre">[[sf.cmath.assoc.laguerre]]</a>

``` cpp
floating-point-type assoc_laguerre(unsigned n, unsigned m, floating-point-type x);
float        assoc_laguerref(unsigned n, unsigned m, float x);
long double  assoc_laguerrel(unsigned n, unsigned m, long double x);
```

*Effects:* These functions compute the associated Laguerre polynomials
of their respective arguments `n`, `m`, and `x`.

*Returns:* Lₙᵐ(x), where Lₙᵐ is given by , Lₙ₊ₘ is given by , n is `n`,
m is `m`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128` or if `m >= 128`.

#### Associated Legendre functions <a id="sf.cmath.assoc.legendre">[[sf.cmath.assoc.legendre]]</a>

``` cpp
floating-point-type assoc_legendre(unsigned l, unsigned m, floating-point-type x);
float        assoc_legendref(unsigned l, unsigned m, float x);
long double  assoc_legendrel(unsigned l, unsigned m, long double x);
```

*Effects:* These functions compute the associated Legendre functions of
their respective arguments `l`, `m`, and `x`.

*Returns:* P_ℓ^m(x), where P_ℓ^m is given by , P_ℓ is given by , ℓ is
`l`, m is `m`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `l >= 128`.

#### Beta function <a id="sf.cmath.beta">[[sf.cmath.beta]]</a>

``` cpp
floating-point-type beta(floating-point-type x, floating-point-type y);
float        betaf(float x, float y);
long double  betal(long double x, long double y);
```

*Effects:* These functions compute the beta function of their respective
arguments `x` and `y`.

*Returns:* B(x, y), where B is given by , x is `x` and y is `y`.

#### Complete elliptic integral of the first kind <a id="sf.cmath.comp.ellint.1">[[sf.cmath.comp.ellint.1]]</a>

``` cpp
floating-point-type comp_ellint_1(floating-point-type k);
float        comp_ellint_1f(float k);
long double  comp_ellint_1l(long double k);
```

*Effects:* These functions compute the complete elliptic integral of the
first kind of their respective arguments `k`.

*Returns:* K(k), where K is given by and k is `k`.

See also [[sf.cmath.ellint.1]].

#### Complete elliptic integral of the second kind <a id="sf.cmath.comp.ellint.2">[[sf.cmath.comp.ellint.2]]</a>

``` cpp
floating-point-type comp_ellint_2(floating-point-type k);
float        comp_ellint_2f(float k);
long double  comp_ellint_2l(long double k);
```

*Effects:* These functions compute the complete elliptic integral of the
second kind of their respective arguments `k`.

*Returns:* E(k), where E is given by and k is `k`.

See also [[sf.cmath.ellint.2]].

#### Complete elliptic integral of the third kind <a id="sf.cmath.comp.ellint.3">[[sf.cmath.comp.ellint.3]]</a>

``` cpp
floating-point-type comp_ellint_3(floating-point-type k, floating-point-type nu);
float        comp_ellint_3f(float k, float nu);
long double  comp_ellint_3l(long double k, long double nu);
```

*Effects:* These functions compute the complete elliptic integral of the
third kind of their respective arguments `k` and `nu`.

*Returns:* $\mathsf{\Pi}(\nu, k)$, where $\mathsf{\Pi}$ is given by , k
is `k`, and $\nu$ is `nu`.

See also [[sf.cmath.ellint.3]].

#### Regular modified cylindrical Bessel functions <a id="sf.cmath.cyl.bessel.i">[[sf.cmath.cyl.bessel.i]]</a>

``` cpp
floating-point-type cyl_bessel_i(floating-point-type nu, floating-point-type x);
float        cyl_bessel_if(float nu, float x);
long double  cyl_bessel_il(long double nu, long double x);
```

*Effects:* These functions compute the regular modified cylindrical
Bessel functions of their respective arguments `nu` and `x`.

*Returns:* $\mathsf{I}_\nu(x)$, where $\mathsf{I}_\nu$ is given by ,
$\nu$ is `nu`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

See also [[sf.cmath.cyl.bessel.j]].

#### Cylindrical Bessel functions of the first kind <a id="sf.cmath.cyl.bessel.j">[[sf.cmath.cyl.bessel.j]]</a>

``` cpp
floating-point-type cyl_bessel_j(floating-point-type nu, floating-point-type x);
float        cyl_bessel_jf(float nu, float x);
long double  cyl_bessel_jl(long double nu, long double x);
```

*Effects:* These functions compute the cylindrical Bessel functions of
the first kind of their respective arguments `nu` and `x`.

*Returns:* $\mathsf{J}_\nu(x)$, where $\mathsf{J}_\nu$ is given by ,
$\nu$ is `nu`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

#### Irregular modified cylindrical Bessel functions <a id="sf.cmath.cyl.bessel.k">[[sf.cmath.cyl.bessel.k]]</a>

``` cpp
floating-point-type cyl_bessel_k(floating-point-type nu, floating-point-type x);
float        cyl_bessel_kf(float nu, float x);
long double  cyl_bessel_kl(long double nu, long double x);
```

*Effects:* These functions compute the irregular modified cylindrical
Bessel functions of their respective arguments `nu` and `x`.

*Returns:* $\mathsf{K}_\nu(x)$, where $\mathsf{K}_\nu$ is given by ,
$\nu$ is `nu`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

See also [[sf.cmath.cyl.bessel.i]], [[sf.cmath.cyl.bessel.j]],
[[sf.cmath.cyl.neumann]].

#### Cylindrical Neumann functions <a id="sf.cmath.cyl.neumann">[[sf.cmath.cyl.neumann]]</a>

``` cpp
floating-point-type cyl_neumann(floating-point-type nu, floating-point-type x);
float        cyl_neumannf(float nu, float x);
long double  cyl_neumannl(long double nu, long double x);
```

*Effects:* These functions compute the cylindrical Neumann functions,
also known as the cylindrical Bessel functions of the second kind, of
their respective arguments `nu` and `x`.

*Returns:* $\mathsf{N}_\nu(x)$, where $\mathsf{N}_\nu$ is given by ,
$\nu$ is `nu`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

See also [[sf.cmath.cyl.bessel.j]].

#### Incomplete elliptic integral of the first kind <a id="sf.cmath.ellint.1">[[sf.cmath.ellint.1]]</a>

``` cpp
floating-point-type ellint_1(floating-point-type k, floating-point-type phi);
float        ellint_1f(float k, float phi);
long double  ellint_1l(long double k, long double phi);
```

*Effects:* These functions compute the incomplete elliptic integral of
the first kind of their respective arguments `k` and `phi` (`phi`
measured in radians).

*Returns:* F(k, φ), where F is given by , k is `k`, and φ is `phi`.

#### Incomplete elliptic integral of the second kind <a id="sf.cmath.ellint.2">[[sf.cmath.ellint.2]]</a>

``` cpp
floating-point-type ellint_2(floating-point-type k, floating-point-type phi);
float        ellint_2f(float k, float phi);
long double  ellint_2l(long double k, long double phi);
```

*Effects:* These functions compute the incomplete elliptic integral of
the second kind of their respective arguments `k` and `phi` (`phi`
measured in radians).

*Returns:* E(k, φ), where E is given by , k is `k`, and φ is `phi`.

#### Incomplete elliptic integral of the third kind <a id="sf.cmath.ellint.3">[[sf.cmath.ellint.3]]</a>

``` cpp
floating-point-type ellint_3(floating-point-type k, floating-point-type nu,
                             floating-point-type phi);
float        ellint_3f(float k, float nu, float phi);
long double  ellint_3l(long double k, long double nu, long double phi);
```

*Effects:* These functions compute the incomplete elliptic integral of
the third kind of their respective arguments `k`, `nu`, and `phi` (`phi`
measured in radians).

*Returns:* $\mathsf{\Pi}(\nu, k, \phi)$, where $\mathsf{\Pi}$ is given
by , $\nu$ is `nu`, k is `k`, and φ is `phi`.

#### Exponential integral <a id="sf.cmath.expint">[[sf.cmath.expint]]</a>

``` cpp
floating-point-type expint(floating-point-type x);
float        expintf(float x);
long double  expintl(long double x);
```

*Effects:* These functions compute the exponential integral of their
respective arguments `x`.

*Returns:* Ei(x), where Ei is given by and x is `x`.

#### Hermite polynomials <a id="sf.cmath.hermite">[[sf.cmath.hermite]]</a>

``` cpp
floating-point-type hermite(unsigned n, floating-point-type x);
float        hermitef(unsigned n, float x);
long double  hermitel(unsigned n, long double x);
```

*Effects:* These functions compute the Hermite polynomials of their
respective arguments `n` and `x`.

*Returns:* Hₙ(x), where Hₙ is given by , n is `n`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

#### Laguerre polynomials <a id="sf.cmath.laguerre">[[sf.cmath.laguerre]]</a>

``` cpp
floating-point-type laguerre(unsigned n, floating-point-type x);
float        laguerref(unsigned n, float x);
long double  laguerrel(unsigned n, long double x);
```

*Effects:* These functions compute the Laguerre polynomials of their
respective arguments `n` and `x`.

*Returns:* Lₙ(x), where Lₙ is given by , n is `n`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

#### Legendre polynomials <a id="sf.cmath.legendre">[[sf.cmath.legendre]]</a>

``` cpp
floating-point-type legendre(unsigned l, floating-point-type x);
float        legendref(unsigned l, float x);
long double  legendrel(unsigned l, long double x);
```

*Effects:* These functions compute the Legendre polynomials of their
respective arguments `l` and `x`.

*Returns:* P_ℓ(x), where P_ℓ is given by , l is `l`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `l >= 128`.

#### Riemann zeta function <a id="sf.cmath.riemann.zeta">[[sf.cmath.riemann.zeta]]</a>

``` cpp
floating-point-type riemann_zeta(floating-point-type x);
float        riemann_zetaf(float x);
long double  riemann_zetal(long double x);
```

*Effects:* These functions compute the Riemann zeta function of their
respective arguments `x`.

*Returns:* ζ(x), where ζ is given by and x is `x`.

#### Spherical Bessel functions of the first kind <a id="sf.cmath.sph.bessel">[[sf.cmath.sph.bessel]]</a>

``` cpp
floating-point-type sph_bessel(unsigned n, floating-point-type x);
float        sph_besself(unsigned n, float x);
long double  sph_bessell(unsigned n, long double x);
```

*Effects:* These functions compute the spherical Bessel functions of the
first kind of their respective arguments `n` and `x`.

*Returns:* jₙ(x), where jₙ is given by , n is `n`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

See also [[sf.cmath.cyl.bessel.j]].

#### Spherical associated Legendre functions <a id="sf.cmath.sph.legendre">[[sf.cmath.sph.legendre]]</a>

``` cpp
floating-point-type sph_legendre(unsigned l, unsigned m, floating-point-type theta);
float        sph_legendref(unsigned l, unsigned m, float theta);
long double  sph_legendrel(unsigned l, unsigned m, long double theta);
```

*Effects:* These functions compute the spherical associated Legendre
functions of their respective arguments `l`, `m`, and `theta` (`theta`
measured in radians).

*Returns:* Y_ℓ^m(θ, 0), where Y_ℓ^m is given by , l is `l`, m is `m`,
and θ is `theta`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `l >= 128`.

See also [[sf.cmath.assoc.legendre]].

#### Spherical Neumann functions <a id="sf.cmath.sph.neumann">[[sf.cmath.sph.neumann]]</a>

``` cpp
floating-point-type sph_neumann(unsigned n, floating-point-type x);
float        sph_neumannf(unsigned n, float x);
long double  sph_neumannl(unsigned n, long double x);
```

*Effects:* These functions compute the spherical Neumann functions, also
known as the spherical Bessel functions of the second kind, of their
respective arguments `n` and `x`.

*Returns:* nₙ(x), where nₙ is given by , n is `n`, and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

See also [[sf.cmath.cyl.neumann]].

## Numbers <a id="numbers">[[numbers]]</a>

### Header `<numbers>` synopsis <a id="numbers.syn">[[numbers.syn]]</a>

``` cpp
namespace std::numbers {
  template<class T> constexpr T e_v          = unspecified;
  template<class T> constexpr T log2e_v      = unspecified;
  template<class T> constexpr T log10e_v     = unspecified;
  template<class T> constexpr T pi_v         = unspecified;
  template<class T> constexpr T inv_pi_v     = unspecified;
  template<class T> constexpr T inv_sqrtpi_v = unspecified;
  template<class T> constexpr T ln2_v        = unspecified;
  template<class T> constexpr T ln10_v       = unspecified;
  template<class T> constexpr T sqrt2_v      = unspecified;
  template<class T> constexpr T sqrt3_v      = unspecified;
  template<class T> constexpr T inv_sqrt3_v  = unspecified;
  template<class T> constexpr T egamma_v     = unspecified;
  template<class T> constexpr T phi_v        = unspecified;

  template<floating_point T> constexpr T e_v<T>          = see below;
  template<floating_point T> constexpr T log2e_v<T>      = see below;
  template<floating_point T> constexpr T log10e_v<T>     = see below;
  template<floating_point T> constexpr T pi_v<T>         = see below;
  template<floating_point T> constexpr T inv_pi_v<T>     = see below;
  template<floating_point T> constexpr T inv_sqrtpi_v<T> = see below;
  template<floating_point T> constexpr T ln2_v<T>        = see below;
  template<floating_point T> constexpr T ln10_v<T>       = see below;
  template<floating_point T> constexpr T sqrt2_v<T>      = see below;
  template<floating_point T> constexpr T sqrt3_v<T>      = see below;
  template<floating_point T> constexpr T inv_sqrt3_v<T>  = see below;
  template<floating_point T> constexpr T egamma_v<T>     = see below;
  template<floating_point T> constexpr T phi_v<T>        = see below;

  inline constexpr double e          = e_v<double>;
  inline constexpr double log2e      = log2e_v<double>;
  inline constexpr double log10e     = log10e_v<double>;
  inline constexpr double pi         = pi_v<double>;
  inline constexpr double inv_pi     = inv_pi_v<double>;
  inline constexpr double inv_sqrtpi = inv_sqrtpi_v<double>;
  inline constexpr double ln2        = ln2_v<double>;
  inline constexpr double ln10       = ln10_v<double>;
  inline constexpr double sqrt2      = sqrt2_v<double>;
  inline constexpr double sqrt3      = sqrt3_v<double>;
  inline constexpr double inv_sqrt3  = inv_sqrt3_v<double>;
  inline constexpr double egamma     = egamma_v<double>;
  inline constexpr double phi        = phi_v<double>;
}
```

### Mathematical constants <a id="math.constants">[[math.constants]]</a>

The library-defined partial specializations of mathematical constant
variable templates are initialized with the nearest representable values
of e, log₂ e, log₁₀ e, π, $\frac{1}{\pi}$, $\frac{1}{\sqrt{\pi}}$,
$\ln 2$, $\ln 10$, $\sqrt{2}$, $\sqrt{3}$, $\frac{1}{\sqrt{3}}$, the
Euler-Mascheroni γ constant, and the golden ratio φ constant
$\frac{1+\sqrt{5}}{2}$, respectively.

Pursuant to [[namespace.std]], a program may partially or explicitly
specialize a mathematical constant variable template provided that the
specialization depends on a program-defined type.

A program that instantiates a primary template of a mathematical
constant variable template is ill-formed.

## Basic linear algebra algorithms <a id="linalg">[[linalg]]</a>

### Overview <a id="linalg.overview">[[linalg.overview]]</a>

Subclause [[linalg]] defines basic linear algebra algorithms. The
algorithms that access the elements of arrays view those elements
through `mdspan` [[views.multidim]].

### Header `<linalg>` synopsis <a id="linalg.syn">[[linalg.syn]]</a>

``` cpp
namespace std::linalg {
  // [linalg.tags.order], storage order tags
  struct column_major_t;
  inline constexpr column_major_t column_major;
  struct row_major_t;
  inline constexpr row_major_t row_major;

  // [linalg.tags.triangle], triangle tags
  struct upper_triangle_t;
  inline constexpr upper_triangle_t upper_triangle;
  struct lower_triangle_t;
  inline constexpr lower_triangle_t lower_triangle;

  // [linalg.tags.diagonal], diagonal tags
  struct implicit_unit_diagonal_t;
  inline constexpr implicit_unit_diagonal_t implicit_unit_diagonal;
  struct explicit_diagonal_t;
  inline constexpr explicit_diagonal_t explicit_diagonal;

  // [linalg.layout.packed], class template layout_blas_packed
  template<class Triangle, class StorageOrder>
    class layout_blas_packed;

  // [linalg.helpers], exposition-only helpers

  // [linalg.helpers.concepts], linear algebra argument concepts
  template<class T>
    constexpr bool is-mdspan = see below;               // exposition only

  template<class T>
    concept in-vector = see below;                      // exposition only

  template<class T>
    concept out-vector = see below;                     // exposition only

  template<class T>
    concept inout-vector = see below;                   // exposition only

  template<class T>
    concept in-matrix = see below;                      // exposition only

  template<class T>
    concept out-matrix = see below;                     // exposition only

  template<class T>
    concept inout-matrix = see below;                   // exposition only

  template<class T>
    concept possibly-packed-inout-matrix = see below;   // exposition only

  template<class T>
    concept in-object = see below;                      // exposition only

  template<class T>
    concept out-object = see below;                     // exposition only

  template<class T>
    concept inout-object = see below;                   // exposition only

  // [linalg.scaled], scaled in-place transformation

  // [linalg.scaled.scaledaccessor], class template scaled_accessor
  template<class ScalingFactor, class NestedAccessor>
    class scaled_accessor;

  // [linalg.scaled.scaled], function template scaled
  template<class ScalingFactor,
           class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto scaled(ScalingFactor alpha, mdspan<ElementType, Extents, Layout, Accessor> x);

  // [linalg.conj], conjugated in-place transformation

  // [linalg.conj.conjugatedaccessor], class template conjugated_accessor
  template<class NestedAccessor>
    class conjugated_accessor;

  // [linalg.conj.conjugated], function template conjugated
  template<class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto conjugated(mdspan<ElementType, Extents, Layout, Accessor> a);

  // [linalg.transp], transpose in-place transformation

  // [linalg.transp.layout.transpose], class template layout_transpose
  template<class Layout>
    class layout_transpose;

  // [linalg.transp.transposed], function template transposed
  template<class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto transposed(mdspan<ElementType, Extents, Layout, Accessor> a);

  // [linalg.conjtransposed], conjugated transpose in-place transformation
  template<class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto conjugate_transposed(mdspan<ElementType, Extents, Layout, Accessor> a);

  // [linalg.algs.blas1], BLAS 1 algorithms

  // [linalg.algs.blas1.givens], Givens rotations

  // [linalg.algs.blas1.givens.lartg], compute Givens rotation

  template<class Real>
    struct setup_givens_rotation_result {
      Real c;
      Real s;
      Real r;
    };
  template<class Real>
    struct setup_givens_rotation_result<complex<Real>> {
      Real c;
      complex<Real> s;
      complex<Real> r;
    };

  template<class Real>
    setup_givens_rotation_result<Real> setup_givens_rotation(Real a, Real b) noexcept;

  template<class Real>
    setup_givens_rotation_result<complex<Real>>
      setup_givens_rotation(complex<Real> a, complex<Real> b) noexcept;

  // [linalg.algs.blas1.givens.rot], apply computed Givens rotation
  template<inout-vector InOutVec1, inout-vector InOutVec2, class Real>
    void apply_givens_rotation(InOutVec1 x, InOutVec2 y, Real c, Real s);
  template<class ExecutionPolicy, inout-vector InOutVec1, inout-vector InOutVec2, class Real>
    void apply_givens_rotation(ExecutionPolicy&& exec,
                               InOutVec1 x, InOutVec2 y, Real c, Real s);
  template<inout-vector InOutVec1, inout-vector InOutVec2, class Real>
    void apply_givens_rotation(InOutVec1 x, InOutVec2 y, Real c, complex<Real> s);
  template<class ExecutionPolicy, inout-vector InOutVec1, inout-vector InOutVec2, class Real>
    void apply_givens_rotation(ExecutionPolicy&& exec,
                               InOutVec1 x, InOutVec2 y, Real c, complex<Real> s);

  // [linalg.algs.blas1.swap], swap elements
  template<inout-object InOutObj1, inout-object InOutObj2>
    void swap_elements(InOutObj1 x, InOutObj2 y);
  template<class ExecutionPolicy, inout-object InOutObj1, inout-object InOutObj2>
    void swap_elements(ExecutionPolicy&& exec, InOutObj1 x, InOutObj2 y);

  // [linalg.algs.blas1.scal], multiply elements by scalar
  template<class Scalar, inout-object InOutObj>
    void scale(Scalar alpha, InOutObj x);
  template<class ExecutionPolicy, class Scalar, inout-object InOutObj>
    void scale(ExecutionPolicy&& exec, Scalar alpha, InOutObj x);

  // [linalg.algs.blas1.copy], copy elements
  template<in-object InObj, out-object OutObj>
    void copy(InObj x, OutObj y);
  template<class ExecutionPolicy, in-object InObj, out-object OutObj>
    void copy(ExecutionPolicy&& exec, InObj x, OutObj y);

  // [linalg.algs.blas1.add], add elementwise
  template<in-object InObj1, in-object InObj2, out-object OutObj>
    void add(InObj1 x, InObj2 y, OutObj z);
  template<class ExecutionPolicy, in-object InObj1, in-object InObj2, out-object OutObj>
    void add(ExecutionPolicy&& exec, InObj1 x, InObj2 y, OutObj z);

  // [linalg.algs.blas1.dot], dot product of two vectors
  template<in-vector InVec1, in-vector InVec2, class Scalar>
    Scalar dot(InVec1 v1, InVec2 v2, Scalar init);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, class Scalar>
    Scalar dot(ExecutionPolicy&& exec, InVec1 v1, InVec2 v2, Scalar init);
  template<in-vector InVec1, in-vector InVec2>
    auto dot(InVec1 v1, InVec2 v2);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2>
    auto dot(ExecutionPolicy&& exec, InVec1 v1, InVec2 v2);

  template<in-vector InVec1, in-vector InVec2, class Scalar>
    Scalar dotc(InVec1 v1, InVec2 v2, Scalar init);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, class Scalar>
    Scalar dotc(ExecutionPolicy&& exec, InVec1 v1, InVec2 v2, Scalar init);
  template<in-vector InVec1, in-vector InVec2>
    auto dotc(InVec1 v1, InVec2 v2);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2>
    auto dotc(ExecutionPolicy&& exec, InVec1 v1, InVec2 v2);

  // [linalg.algs.blas1.ssq], scaled sum of squares of a vector's elements
  template<class Scalar>
    struct sum_of_squares_result {
      Scalar scaling_factor;
      Scalar scaled_sum_of_squares;
    };
  template<in-vector InVec, class Scalar>
    sum_of_squares_result<Scalar>
      vector_sum_of_squares(InVec v, sum_of_squares_result<Scalar> init);
  template<class ExecutionPolicy, in-vector InVec, class Scalar>
    sum_of_squares_result<Scalar>
      vector_sum_of_squares(ExecutionPolicy&& exec,
                            InVec v, sum_of_squares_result<Scalar> init);

  // [linalg.algs.blas1.nrm2], Euclidean norm of a vector
  template<in-vector InVec, class Scalar>
    Scalar vector_two_norm(InVec v, Scalar init);
  template<class ExecutionPolicy, in-vector InVec, class Scalar>
    Scalar vector_two_norm(ExecutionPolicy&& exec, InVec v, Scalar init);
  template<in-vector InVec>
    auto vector_two_norm(InVec v);
  template<class ExecutionPolicy, in-vector InVec>
    auto vector_two_norm(ExecutionPolicy&& exec, InVec v);

  // [linalg.algs.blas1.asum], sum of absolute values of vector elements
  template<in-vector InVec, class Scalar>
    Scalar vector_abs_sum(InVec v, Scalar init);
  template<class ExecutionPolicy, in-vector InVec, class Scalar>
    Scalar vector_abs_sum(ExecutionPolicy&& exec, InVec v, Scalar init);
  template<in-vector InVec>
    auto vector_abs_sum(InVec v);
  template<class ExecutionPolicy, in-vector InVec>
    auto vector_abs_sum(ExecutionPolicy&& exec, InVec v);

  // [linalg.algs.blas1.iamax], index of maximum absolute value of vector elements
  template<in-vector InVec>
    typename InVec::extents_type vector_idx_abs_max(InVec v);
  template<class ExecutionPolicy, in-vector InVec>
    typename InVec::extents_type vector_idx_abs_max(ExecutionPolicy&& exec, InVec v);

  // [linalg.algs.blas1.matfrobnorm], Frobenius norm of a matrix
  template<in-matrix InMat, class Scalar>
    Scalar matrix_frob_norm(InMat A, Scalar init);
  template<class ExecutionPolicy, in-matrix InMat, class Scalar>
    Scalar matrix_frob_norm(ExecutionPolicy&& exec, InMat A, Scalar init);
  template<in-matrix InMat>
    auto matrix_frob_norm(InMat A);
  template<class ExecutionPolicy, in-matrix InMat>
    auto matrix_frob_norm(ExecutionPolicy&& exec, InMat A);

  // [linalg.algs.blas1.matonenorm], one norm of a matrix
  template<in-matrix InMat, class Scalar>
    Scalar matrix_one_norm(InMat A, Scalar init);
  template<class ExecutionPolicy, in-matrix InMat, class Scalar>
    Scalar matrix_one_norm(ExecutionPolicy&& exec, InMat A, Scalar init);
  template<in-matrix InMat>
    auto matrix_one_norm(InMat A);
  template<class ExecutionPolicy, in-matrix InMat>
    auto matrix_one_norm(ExecutionPolicy&& exec, InMat A);

  // [linalg.algs.blas1.matinfnorm], infinity norm of a matrix
  template<in-matrix InMat, class Scalar>
    Scalar matrix_inf_norm(InMat A, Scalar init);
  template<class ExecutionPolicy, in-matrix InMat, class Scalar>
    Scalar matrix_inf_norm(ExecutionPolicy&& exec, InMat A, Scalar init);
  template<in-matrix InMat>
    auto matrix_inf_norm(InMat A);
  template<class ExecutionPolicy, in-matrix InMat>
    auto matrix_inf_norm(ExecutionPolicy&& exec, InMat A);

  // [linalg.algs.blas2], BLAS 2 algorithms

  // [linalg.algs.blas2.gemv], general matrix-vector product
  template<in-matrix InMat, in-vector InVec, out-vector OutVec>
    void matrix_vector_product(InMat A, InVec x, OutVec y);
  template<class ExecutionPolicy, in-matrix InMat, in-vector InVec, out-vector OutVec>
    void matrix_vector_product(ExecutionPolicy&& exec, InMat A, InVec x, OutVec y);
  template<in-matrix InMat, in-vector InVec1, in-vector InVec2, out-vector OutVec>
    void matrix_vector_product(InMat A, InVec1 x, InVec2 y, OutVec z);
  template<class ExecutionPolicy,
           in-matrix InMat, in-vector InVec1, in-vector InVec2, out-vector OutVec>
    void matrix_vector_product(ExecutionPolicy&& exec, InMat A, InVec1 x, InVec2 y, OutVec z);

  // [linalg.algs.blas2.symv], symmetric matrix-vector product
  template<in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
    void symmetric_matrix_vector_product(InMat A, Triangle t, InVec x, OutVec y);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
    void symmetric_matrix_vector_product(ExecutionPolicy&& exec,
                                         InMat A, Triangle t, InVec x, OutVec y);
  template<in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2,
           out-vector OutVec>
    void symmetric_matrix_vector_product(InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2,
           out-vector OutVec>
    void symmetric_matrix_vector_product(ExecutionPolicy&& exec,
                                         InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);

  // [linalg.algs.blas2.hemv], Hermitian matrix-vector product
  template<in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
    void hermitian_matrix_vector_product(InMat A, Triangle t, InVec x, OutVec y);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
    void hermitian_matrix_vector_product(ExecutionPolicy&& exec,
                                         InMat A, Triangle t, InVec x, OutVec y);
  template<in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2,
           out-vector OutVec>
    void hermitian_matrix_vector_product(InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2,
           out-vector OutVec>
    void hermitian_matrix_vector_product(ExecutionPolicy&& exec,
                                         InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);

  // [linalg.algs.blas2.trmv], triangular matrix-vector product

  // Overwriting triangular matrix-vector product
  template<in-matrix InMat, class Triangle, class DiagonalStorage, in-vector InVec,
           out-vector OutVec>
    void triangular_matrix_vector_product(InMat A, Triangle t, DiagonalStorage d,
                                          InVec x, OutVec y);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, in-vector InVec,
           out-vector OutVec>
    void triangular_matrix_vector_product(ExecutionPolicy&& exec,
                                          InMat A, Triangle t, DiagonalStorage d,
                                          InVec x, OutVec y);

  // In-place triangular matrix-vector product
  template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
    void triangular_matrix_vector_product(InMat A, Triangle t, DiagonalStorage d, InOutVec y);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
    void triangular_matrix_vector_product(ExecutionPolicy&& exec,
                                          InMat A, Triangle t, DiagonalStorage d, InOutVec y);

  // Updating triangular matrix-vector product
  template<in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec1, in-vector InVec2, out-vector OutVec>
    void triangular_matrix_vector_product(InMat A, Triangle t, DiagonalStorage d,
                                          InVec1 x, InVec2 y, OutVec z);
  template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec1, in-vector InVec2, out-vector OutVec>
    void triangular_matrix_vector_product(ExecutionPolicy&& exec,
                                          InMat A, Triangle t, DiagonalStorage d,
                                          InVec1 x, InVec2 y, OutVec z);

  // [linalg.algs.blas2.trsv], solve a triangular linear system

  // Solve a triangular linear system, not in place
  template<in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec, out-vector OutVec, class BinaryDivideOp>
    void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d,
                                        InVec b, OutVec x, BinaryDivideOp divide);
  template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec, out-vector OutVec, class BinaryDivideOp>
    void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d,
                                        InVec b, OutVec x, BinaryDivideOp divide);
  template<in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec, out-vector OutVec>
    void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d,
                                        InVec b, OutVec x);
  template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec, out-vector OutVec>
    void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d,
                                        InVec b, OutVec x);

  // Solve a triangular linear system, in place
  template<in-matrix InMat, class Triangle, class DiagonalStorage,
           inout-vector InOutVec, class BinaryDivideOp>
    void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d,
                                        InOutVec b, BinaryDivideOp divide);
  template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
           inout-vector InOutVec, class BinaryDivideOp>
    void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d,
                                        InOutVec b, BinaryDivideOp divide);
  template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
    void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d, InOutVec b);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
    void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d, InOutVec b);

  // [linalg.algs.blas2.rank1], nonsymmetric rank-1 matrix update
  template<in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
    void matrix_rank_1_update(InVec1 x, InVec2 y, InOutMat A);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
    void matrix_rank_1_update(ExecutionPolicy&& exec, InVec1 x, InVec2 y, InOutMat A);

  template<in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
    void matrix_rank_1_update_c(InVec1 x, InVec2 y, InOutMat A);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
    void matrix_rank_1_update_c(ExecutionPolicy&& exec, InVec1 x, InVec2 y, InOutMat A);

  // [linalg.algs.blas2.symherrank1], symmetric or Hermitian rank-1 matrix update
  template<class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_1_update(Scalar alpha, InVec x, InOutMat A, Triangle t);
  template<class ExecutionPolicy,
           class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_1_update(ExecutionPolicy&& exec,
                                        Scalar alpha, InVec x, InOutMat A, Triangle t);
  template<in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_1_update(InVec x, InOutMat A, Triangle t);
  template<class ExecutionPolicy,
           in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_1_update(ExecutionPolicy&& exec, InVec x, InOutMat A, Triangle t);

  template<class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_1_update(Scalar alpha, InVec x, InOutMat A, Triangle t);
  template<class ExecutionPolicy,
           class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_1_update(ExecutionPolicy&& exec,
                                        Scalar alpha, InVec x, InOutMat A, Triangle t);
  template<in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_1_update(InVec x, InOutMat A, Triangle t);
  template<class ExecutionPolicy,
           in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_1_update(ExecutionPolicy&& exec, InVec x, InOutMat A, Triangle t);

  // [linalg.algs.blas2.rank2], symmetric and Hermitian rank-2 matrix updates

  // symmetric rank-2 matrix update
  template<in-vector InVec1, in-vector InVec2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_2_update(InVec1 x, InVec2 y, InOutMat A, Triangle t);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_2_update(ExecutionPolicy&& exec,
                                        InVec1 x, InVec2 y, InOutMat A, Triangle t);

  // Hermitian rank-2 matrix update
  template<in-vector InVec1, in-vector InVec2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_2_update(InVec1 x, InVec2 y, InOutMat A, Triangle t);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_2_update(ExecutionPolicy&& exec,
                                        InVec1 x, InVec2 y, InOutMat A, Triangle t);

  // [linalg.algs.blas3], BLAS 3 algorithms

  // [linalg.algs.blas3.gemm], general matrix-matrix product
  template<in-matrix InMat1, in-matrix InMat2, out-matrix OutMat>
    void matrix_product(InMat1 A, InMat2 B, OutMat C);
  template<class ExecutionPolicy, in-matrix InMat1, in-matrix InMat2, out-matrix OutMat>
    void matrix_product(ExecutionPolicy&& exec,
                        InMat1 A, InMat2 B, OutMat C);
  template<in-matrix InMat1, in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
    void matrix_product(InMat1 A, InMat2 B, InMat3 E, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
    void matrix_product(ExecutionPolicy&& exec,
                        InMat1 A, InMat2 B, InMat3 E, OutMat C);

  // [linalg.algs.blas3.xxmm], symmetric, Hermitian, and triangular matrix-matrix product

  template<in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
    void symmetric_matrix_product(InMat1 A, Triangle t, InMat2 B, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
    void symmetric_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, Triangle t, InMat2 B, OutMat C);

  template<in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
    void hermitian_matrix_product(InMat1 A, Triangle t, InMat2 B, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
    void hermitian_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, Triangle t, InMat2 B, OutMat C);

  template<in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat>
    void triangular_matrix_product(InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat>
    void triangular_matrix_product(ExecutionPolicy&& exec,
                                   InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void symmetric_matrix_product(InMat1 A, InMat2 B, Triangle t, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void symmetric_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, InMat2 B, Triangle t, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void hermitian_matrix_product(InMat1 A, InMat2 B, Triangle t, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void hermitian_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, InMat2 B, Triangle t, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
           out-matrix OutMat>
    void triangular_matrix_product(InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
           out-matrix OutMat>
    void triangular_matrix_product(ExecutionPolicy&& exec,
                                   InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, OutMat C);

  template<in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
           out-matrix OutMat>
    void symmetric_matrix_product(InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
           out-matrix OutMat>
    void symmetric_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);

  template<in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
           out-matrix OutMat>
    void hermitian_matrix_product(InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
           out-matrix OutMat>
    void hermitian_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);

  template<in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
    void triangular_matrix_product(InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, InMat3 E,
                                   OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
    void triangular_matrix_product(ExecutionPolicy&& exec,
                                   InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, InMat3 E,
                                   OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
           out-matrix OutMat>
    void symmetric_matrix_product(InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
           out-matrix OutMat>
    void symmetric_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
           out-matrix OutMat>
    void hermitian_matrix_product(InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
           out-matrix OutMat>
    void hermitian_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
           in-matrix InMat3, out-matrix OutMat>
    void triangular_matrix_product(InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, InMat3 E,
                                   OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
           in-matrix InMat3, out-matrix OutMat>
    void triangular_matrix_product(ExecutionPolicy&& exec,
                                   InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, InMat3 E,
                                   OutMat C);

  // [linalg.algs.blas3.trmm], in-place triangular matrix-matrix product

  template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_left_product(InMat A, Triangle t, DiagonalStorage d, InOutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_left_product(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d, InOutMat C);

  template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_right_product(InMat A, Triangle t, DiagonalStorage d, InOutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_right_product(ExecutionPolicy&& exec,
                                         InMat A, Triangle t, DiagonalStorage d, InOutMat C);

  // [linalg.algs.blas3.rankk], rank-k update of a symmetric or Hermitian matrix

  // rank-k symmetric matrix update
  template<class Scalar, in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_k_update(Scalar alpha, InMat A, InOutMat C, Triangle t);
  template<class ExecutionPolicy, class Scalar,
           in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_k_update(ExecutionPolicy&& exec,
                                        Scalar alpha, InMat A, InOutMat C, Triangle t);

  template<in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_k_update(InMat A, InOutMat C, Triangle t);
  template<class ExecutionPolicy,
           in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_k_update(ExecutionPolicy&& exec,
                                        InMat A, InOutMat C, Triangle t);

  // rank-k Hermitian matrix update
  template<class Scalar, in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_k_update(Scalar alpha, InMat A, InOutMat C, Triangle t);
  template<class ExecutionPolicy,
           class Scalar, in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_k_update(ExecutionPolicy&& exec,
                                        Scalar alpha, InMat A, InOutMat C, Triangle t);

  template<in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_k_update(InMat A, InOutMat C, Triangle t);
  template<class ExecutionPolicy,
           in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_k_update(ExecutionPolicy&& exec,
                                        InMat A, InOutMat C, Triangle t);

  // [linalg.algs.blas3.rank2k], rank-2k update of a symmetric or Hermitian matrix

  // rank-2k symmetric matrix update
  template<in-matrix InMat1, in-matrix InMat2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_2k_update(InMat1 A, InMat2 B, InOutMat C, Triangle t);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_2k_update(ExecutionPolicy&& exec,
                                         InMat1 A, InMat2 B, InOutMat C, Triangle t);

  // rank-2k Hermitian matrix update
  template<in-matrix InMat1, in-matrix InMat2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_2k_update(InMat1 A, InMat2 B, InOutMat C, Triangle t);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2,
           possibly-packed-inout-matrix InOutMat, class Triangle>
    void hermitian_matrix_rank_2k_update(ExecutionPolicy&& exec,
                                         InMat1 A, InMat2 B, InOutMat C, Triangle t);

  // [linalg.algs.blas3.trsm], solve multiple triangular linear systems

  // solve multiple triangular systems on the left, not-in-place
  template<in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_left_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                             InMat2 B, OutMat X, BinaryDivideOp divide);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                             InMat1 A, Triangle t, DiagonalStorage d,
                                             InMat2 B, OutMat X, BinaryDivideOp divide);
  template<in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat>
    void triangular_matrix_matrix_left_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                             InMat2 B, OutMat X);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat>
    void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                             InMat1 A, Triangle t, DiagonalStorage d,
                                             InMat2 B, OutMat X);

  // solve multiple triangular systems on the right, not-in-place
  template<in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_right_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                              InMat2 B, OutMat X, BinaryDivideOp divide);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                              InMat1 A, Triangle t, DiagonalStorage d,
                                              InMat2 B, OutMat X, BinaryDivideOp divide);
  template<in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat>
    void triangular_matrix_matrix_right_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                              InMat2 B, OutMat X);
  template<class ExecutionPolicy,
           in-matrix InMat1, class Triangle, class DiagonalStorage,
           in-matrix InMat2, out-matrix OutMat>
    void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                              InMat1 A, Triangle t, DiagonalStorage d,
                                              InMat2 B, OutMat X);

  // solve multiple triangular systems on the left, in-place
  template<in-matrix InMat, class Triangle, class DiagonalStorage,
           inout-matrix InOutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_left_solve(InMat A, Triangle t, DiagonalStorage d,
                                             InOutMat B, BinaryDivideOp divide);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage,
           inout-matrix InOutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                             InMat A, Triangle t, DiagonalStorage d,
                                             InOutMat B, BinaryDivideOp divide);
  template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_matrix_left_solve(InMat A, Triangle t, DiagonalStorage d,
                                             InOutMat B);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                             InMat A, Triangle t, DiagonalStorage d,
                                             InOutMat B);

  // solve multiple triangular systems on the right, in-place
  template<in-matrix InMat, class Triangle, class DiagonalStorage,
           inout-matrix InOutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_right_solve(InMat A, Triangle t, DiagonalStorage d,
                                              InOutMat B, BinaryDivideOp divide);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage,
           inout-matrix InOutMat, class BinaryDivideOp>
    void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                              InMat A, Triangle t, DiagonalStorage d,
                                              InOutMat B, BinaryDivideOp divide);
  template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_matrix_right_solve(InMat A, Triangle t, DiagonalStorage d,
                                              InOutMat B);
  template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                              InMat A, Triangle t, DiagonalStorage d,
                                              InOutMat B);
}
```

### General <a id="linalg.general">[[linalg.general]]</a>

For the effects of all functions in [[linalg]], when the effects are
described as “computes R = E” or “compute R = E” (for some R and
mathematical expression E), the following apply:

- E has the conventional mathematical meaning as written.
- The pattern $x^T$ should be read as “the transpose of x.”
- The pattern $x^H$ should be read as “the conjugate transpose of x.”
- When R is the same name as a function parameter whose type is a
  template parameter with `Out` in its name, the intent is that the
  result of the computation is written to the elements of the function
  parameter `R`.

Some of the functions and types in [[linalg]] distinguish between the
“rows” and the “columns” of a matrix. For a matrix `A` and a
multidimensional index `i, j` in `A.extents()`,

- *row* `i` of `A` is the set of elements `A[i, k1]` for all `k1` such
  that `i, k1` is in `A.extents()`; and
- *column* `j` of `A` is the set of elements `A[k0, j]` for all `k0`
  such that `k0, j` is in `A.extents()`.

Some of the functions in [[linalg]] distinguish between the “upper
triangle,” “lower triangle,” and “diagonal” of a matrix.

- The *diagonal* is the set of all elements of `A` accessed by `A[i,i]`
  for 0 ≤ `i` \< min(`A.extent(0)`, `A.extent(1)`).
- The *upper triangle* of a matrix `A` is the set of all elements of `A`
  accessed by `A[i,j]` with `i` ≤ `j`. It includes the diagonal.
- The *lower triangle* of `A` is the set of all elements of `A` accessed
  by `A[i,j]` with `i` ≥ `j`. It includes the diagonal.

For any function `F` that takes a parameter named `t`, `t` applies to
accesses done through the parameter preceding `t` in the parameter list
of `F`. Let `m` be such an access-modified function parameter. `F` will
only access the triangle of `m` specified by `t`. For accesses `m[i, j]`
outside the triangle specified by `t`, `F` will use the value

- `conj-if-needed(m[j, i])` if the name of `F` starts with `hermitian`,
- `m[j, i]` if the name of `F` starts with `symmetric`, or
- the additive identity if the name of `F` starts with `triangular`.

[*Example 1*:

Small vector product accessing only specified triangle. It would not be
a precondition violation for the non-accessed matrix element to be
non-zero.

``` cpp
template<class Triangle>
void triangular_matrix_vector_2x2_product(
       mdspan<const float, extents<int, 2, 2>> m,
       Triangle t,
       mdspan<const float, extents<int, 2>> x,
       mdspan<float, extents<int, 2>> y) {

  static_assert(is_same_v<Triangle, lower_triangle_t> ||
                is_same_v<Triangle, upper_triangle_t>);

  if constexpr (is_same_v<Triangle, lower_triangle_t>) {
    y[0] = m[0,0] * x[0];       // + 0 * x[1]
    y[1] = m[1,0] * x[0] + m[1,1] * x[1];
  } else {                      // upper_triangle_t
    y[0] = m[0,0] * x[0] + m[0,1] * x[1];
    y[1] = /* 0 * x[0] + */ m[1,1] * x[1];
  }
}
```

— *end example*]

For any function `F` that takes a parameter named `d`, `d` applies to
accesses done through the previous-of-the-previous parameter of `d` in
the parameter list of `F`. Let `m` be such an access-modified function
parameter. If `d` specifies that an implicit unit diagonal is to be
assumed, then

- `F` will not access the diagonal of `m`; and
- the algorithm will interpret `m` as if it has a unit diagonal, that
  is, a diagonal each of whose elements behaves as a two-sided
  multiplicative identity (even if `m`’s value type does not have a
  two-sided multiplicative identity).

Otherwise, if `d` specifies that an explicit diagonal is to be assumed,
then `F` will access the diagonal of `m`.

Within all the functions in [[linalg]], any calls to `abs`, `conj`,
`imag`, and `real` are unqualified.

Two `mdspan` objects `x` and `y` *alias* each other, if they have the
same extents `e`, and for every pack of integers `i` which is a
multidimensional index in `e`, `x[i...]` and `y[i...]` refer to the same
element.

[*Note 1*: This means that `x` and `y` view the same elements in the
same order. — *end note*]

Two `mdspan` objects `x` and `y` *overlap* each other, if for some pack
of integers `i` that is a multidimensional index in `x.extents()`, there
exists a pack of integers `j` that is a multidimensional index in
`y.extents()`, such that `x[i...]` and `y[j...]` refer to the same
element.

[*Note 2*: Aliasing is a special case of overlapping. If `x` and `y` do
not overlap, then they also do not alias each other. — *end note*]

### Requirements <a id="linalg.reqs">[[linalg.reqs]]</a>

#### Linear algebra value types <a id="linalg.reqs.val">[[linalg.reqs.val]]</a>

Throughout [[linalg]], the following types are :

- the `value_type` type alias of any input or output `mdspan`
  parameter(s) of any function in [[linalg]]; and
- the `Scalar` template parameter (if any) of any function or class in
  [[linalg]].

Linear algebra value types shall model `semiregular`.

A value-initialized object of linear algebra value type shall act as the
additive identity.

#### Algorithm and class requirements <a id="linalg.reqs.alg">[[linalg.reqs.alg]]</a>

[[linalg.reqs.alg]] lists common requirements for all algorithms and
classes in [[linalg]].

All of the following statements presume that the algorithm’s asymptotic
complexity requirements, if any, are satisfied.

- The function may make arbitrarily many objects of any linear algebra
  value type, value-initializing or direct-initializing them with any
  existing object of that type.
- The *triangular solve algorithms* in [[linalg.algs.blas2.trsv]],
  [[linalg.algs.blas3.trmm]], [[linalg.algs.blas3.trsm]], and
  [[linalg.algs.blas3.inplacetrsm]] either have a `BinaryDivideOp`
  template parameter (see [[linalg.algs.reqs]]) and a binary function
  object parameter `divide` of that type, or they have effects
  equivalent to invoking such an algorithm. Triangular solve algorithms
  interpret `divide(a, b)` as `a` times the multiplicative inverse of
  `b`. Each triangular solve algorithm uses a sequence of evaluations of
  `*`, `*=`, `divide`, unary `+`, binary `+`, `+=`, unary `-`, binary
  `-`, `-=`, and `=` operators that would produce the result specified
  by the algorithm’s *Effects* and *Remarks* when operating on elements
  of a field with noncommutative multiplication. It is a precondition of
  the algorithm that any addend, any subtrahend, any partial sum of
  addends in any order (treating any difference as a sum with the second
  term negated), any factor, any partial product of factors respecting
  their order, any numerator (first argument of `divide`), any
  denominator (second argument of `divide`), and any assignment is a
  well-formed expression.
- Each function in [[linalg.algs.blas1]], [[linalg.algs.blas2]], and
  [[linalg.algs.blas3]] that is not a triangular solve algorithm will
  use a sequence of evaluations of `*`, `*=`, `+`, `+=`, and `=`
  operators that would produce the result specified by the algorithm’s
  *Effects* and *Remarks* when operating on elements of a semiring with
  noncommutative multiplication. It is a precondition of the algorithm
  that any addend, any partial sum of addends in any order, any factor,
  any partial product of factors respecting their order, and any
  assignment is a well-formed expression.
- If the function has an output `mdspan`, then all addends, subtrahends
  (for the triangular solve algorithms), or results of the `divide`
  parameter on intermediate terms (if the function takes a `divide`
  parameter) are assignable and convertible to the output `mdspan`’s
  `value_type`.
- The function may reorder addends and partial sums arbitrarily.
  \[*Note 2*: Factors in each product are not reordered; multiplication
  is not necessarily commutative. — *end note*]

[*Note 1*: The above requirements do not prohibit implementation
approaches and optimization techniques which are not user-observable. In
particular, if for all input and output arguments the `value_type` is a
floating-point type, implementers are free to leverage approximations,
use arithmetic operations not explicitly listed above, and compute
floating-point sums in any way that improves their
accuracy. — *end note*]

[*Note 2*:

For all functions in [[linalg]], suppose that all input and output
`mdspan` have as `value_type` a floating-point type, and any `Scalar`
template argument has a floating-point type. Then, functions can do all
of the following:

- compute floating-point sums in any way that improves their accuracy
  for arbitrary input;
- perform additional arithmetic operations (other than those specified
  by the function’s wording and [[linalg.reqs.alg]]) in order to improve
  performance or accuracy; and
- use approximations (that might not be exact even if computing with
  real numbers), instead of computations that would be exact if it were
  possible to compute without rounding error;

as long as

- the function satisfies the complexity requirements; and
- the function is logarithmically stable, as defined in Demmel 2007.
  Strassen’s algorithm for matrix-matrix multiply is an example of a
  logarithmically stable algorithm.

— *end note*]

### Tag classes <a id="linalg.tags">[[linalg.tags]]</a>

#### Storage order tags <a id="linalg.tags.order">[[linalg.tags.order]]</a>

The storage order tags describe the order of elements in an `mdspan`
with `layout_blas_packed` [[linalg.layout.packed]] layout.

``` cpp
struct column_major_t {
  explicit column_major_t() = default;
};
inline constexpr column_major_t column_major{};

struct row_major_t {
  explicit row_major_t() = default;
};
inline constexpr row_major_t row_major{};
```

`column_major_t` indicates a column-major order, and `row_major_t`
indicates a row-major order.

#### Triangle tags <a id="linalg.tags.triangle">[[linalg.tags.triangle]]</a>

``` cpp
struct upper_triangle_t {
  explicit upper_triangle_t() = default;
};
inline constexpr upper_triangle_t upper_triangle{};

struct lower_triangle_t {
  explicit lower_triangle_t() = default;
};
inline constexpr lower_triangle_t lower_triangle{};
```

These tag classes specify whether algorithms and other users of a matrix
(represented as an `mdspan`) access the upper triangle
(`upper_triangle_t`) or lower triangle (`lower_triangle_t`) of the
matrix (see also [[linalg.general]]). This is also subject to the
restrictions of `implicit_unit_diagonal_t` if that tag is also used as a
function argument; see below.

#### Diagonal tags <a id="linalg.tags.diagonal">[[linalg.tags.diagonal]]</a>

``` cpp
struct implicit_unit_diagonal_t {
  explicit implicit_unit_diagonal_t() = default;
};
inline constexpr implicit_unit_diagonal_t implicit_unit_diagonal{};

struct explicit_diagonal_t {
  explicit explicit_diagonal_t() = default;
};
inline constexpr explicit_diagonal_t explicit_diagonal{};
```

These tag classes specify whether algorithms access the matrix’s
diagonal entries, and if not, then how algorithms interpret the matrix’s
implicitly represented diagonal values.

The `implicit_unit_diagonal_t` tag indicates that an implicit unit
diagonal is to be assumed [[linalg.general]].

The `explicit_diagonal_t` tag indicates that an explicit diagonal is
used [[linalg.general]].

### Layouts for packed matrix types <a id="linalg.layout.packed">[[linalg.layout.packed]]</a>

#### Overview <a id="linalg.layout.packed.overview">[[linalg.layout.packed.overview]]</a>

`layout_blas_packed` is an `mdspan` layout mapping policy that
represents a square matrix that stores only the entries in one triangle,
in a packed contiguous format. Its `Triangle` template parameter
determines whether an `mdspan` with this layout stores the upper or
lower triangle of the matrix. Its `StorageOrder` template parameter
determines whether the layout packs the matrix’s elements in
column-major or row-major order.

A `StorageOrder` of `column_major_t` indicates column-major ordering.
This packs matrix elements starting with the leftmost (least column
index) column, and proceeding column by column, from the top entry
(least row index).

A `StorageOrder` of `row_major_t` indicates row-major ordering. This
packs matrix elements starting with the topmost (least row index) row,
and proceeding row by row, from the leftmost (least column index) entry.

[*Note 1*: `layout_blas_packed` describes the data layout used by the
BLAS’ Symmetric Packed (SP), Hermitian Packed (HP), and Triangular
Packed (TP) matrix types. — *end note*]

``` cpp
namespace std::linalg {
  template<class Triangle, class StorageOrder>
  class layout_blas_packed {
  public:
    using triangle_type = Triangle;
    using storage_order_type = StorageOrder;

    template<class Extents>
    struct mapping {
    public:
      using extents_type = Extents;
      using index_type = extents_type::index_type;
      using size_type = extents_type::size_type;
      using rank_type = extents_type::rank_type;
      using layout_type = layout_blas_packed;

      // [linalg.layout.packed.cons], constructors
      constexpr mapping() noexcept = default;
      constexpr mapping(const mapping&) noexcept = default;
      constexpr mapping(const extents_type&) noexcept;
      template<class OtherExtents>
        constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
          mapping(const mapping<OtherExtents>& other) noexcept;

      constexpr mapping& operator=(const mapping&) noexcept = default;

      // [linalg.layout.packed.obs], observers
      constexpr const extents_type& extents() const noexcept { return extents_; }

      constexpr index_type required_span_size() const noexcept;

      template<class Index0, class Index1>
        constexpr index_type operator() (Index0 ind0, Index1 ind1) const noexcept;

      static constexpr bool is_always_unique() noexcept {
        return (extents_type::static_extent(0) != dynamic_extent &&
                extents_type::static_extent(0) < 2) ||
               (extents_type::static_extent(1) != dynamic_extent &&
                extents_type::static_extent(1) < 2);
      }
      static constexpr bool is_always_exhaustive() noexcept { return true; }
      static constexpr bool is_always_strided() noexcept
        { return is_always_unique(); }

      constexpr bool is_unique() const noexcept {
        return extents_.extent(0) < 2;
      }
      constexpr bool is_exhaustive() const noexcept { return true; }
      constexpr bool is_strided() const noexcept {
        return extents_.extent(0) < 2;
      }

      constexpr index_type stride(rank_type) const noexcept;

      template<class OtherExtents>
        friend constexpr bool operator==(const mapping&, const mapping<OtherExtents>&) noexcept;

    private:
      extents_type extents_{};     // exposition only
    };
  };
}
```

*Mandates:*

- `Triangle` is either `upper_triangle_t` or `lower_triangle_t`,
- `StorageOrder` is either `column_major_t` or `row_major_t`,
- `Extents` is a specialization of `std::extents`,
- `Extents::rank()` equals 2,
- one of
  ``` cpp
  extents_type::static_extent(0) == dynamic_extent,
  extents_type::static_extent(1) == dynamic_extent, or
  extents_type::static_extent(0) == extents_type::static_extent(1)
  ```

  is `true`, and
- if `Extents::rank_dynamic() == 0` is `true`, let Nₛ be equal to
  `Extents::static_extent(0)`; then, Nₛ × (Nₛ + 1) is representable as a
  value of type `index_type`.

`layout_blas_packed<T, SO>::mapping<E>` is a trivially copyable type
that models `regular` for each `T`, `SO`, and `E`.

#### Constructors <a id="linalg.layout.packed.cons">[[linalg.layout.packed.cons]]</a>

``` cpp
constexpr mapping(const extents_type& e) noexcept;
```

*Preconditions:*

- Let N be equal to `e.extent(0)`. Then, N × (N+1) is representable as a
  value of type `index_type`[[basic.fundamental]].
- `e.extent(0)` equals `e.extent(1)`.

*Effects:* Direct-non-list-initializes *extents\_* with `e`.

``` cpp
template<class OtherExtents>
  explicit(!is_convertible_v<OtherExtents, extents_type>)
    constexpr mapping(const mapping<OtherExtents>& other) noexcept;
```

*Constraints:* `is_constructible_v<extents_type, OtherExtents>` is
`true`.

*Preconditions:* Let N be `other.extents().extent(0)`. Then, N × (N+1)
is representable as a value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

#### Observers <a id="linalg.layout.packed.obs">[[linalg.layout.packed.obs]]</a>

``` cpp
constexpr index_type required_span_size() const noexcept;
```

*Returns:* *`extents_`*`.extent(0) * (`*`extents_`*`.extent(0) + 1)/2`.

[*Note 1*: For example, a 5 x 5 packed matrix only stores 15 matrix
elements. — *end note*]

``` cpp
template<class Index0, class Index1>
  constexpr index_type operator() (Index0 ind0, Index1 ind1) const noexcept;
```

*Constraints:*

- `is_convertible_v<Index0, index_type>` is `true`,
- `is_convertible_v<Index1, index_type>` is `true`,
- `is_nothrow_constructible_v<index_type, Index0>` is `true`, and
- `is_nothrow_constructible_v<index_type, Index1>` is `true`.

Let `i` be `extents_type::`*`index-cast`*`(ind0)`, and let `j` be
`extents_type::`*`index-cast`*`(ind1)`.

*Preconditions:* `i, j` is a multidimensional index in
*extents\_*[[mdspan.overview]].

*Returns:* Let `N` be *`extents_`*`.extent(0)`. Then

- `(*this)(j, i)` if `i > j` is `true`; otherwise
- `i + j * (j + 1)/2` if
  ``` cpp
  is_same_v<StorageOrder, column_major_t> && is_same_v<Triangle, upper_triangle_t>
  ```

  is `true` or
  ``` cpp
  is_same_v<StorageOrder, row_major_t> && is_same_v<Triangle, lower_triangle_t>
  ```

  is `true`; otherwise
- `j + N * i - i * (i + 1)/2`.

``` cpp
constexpr index_type stride(rank_type r) const noexcept;
```

*Preconditions:*

- `is_strided()` is `true`, and
- `r < extents_type::rank()` is `true`.

*Returns:* `1`.

``` cpp
template<class OtherExtents>
  friend constexpr bool operator==(const mapping& x, const mapping<OtherExtents>& y) noexcept;
```

*Effects:* Equivalent to: `return x.extents() == y.extents();`

### Exposition-only helpers <a id="linalg.helpers">[[linalg.helpers]]</a>

#### *abs-if-needed* <a id="linalg.helpers.abs">[[linalg.helpers.abs]]</a>

The name *abs-if-needed* denotes an exposition-only function object. The
expression `abs-if-needed(E)` for a subexpression `E` whose type is `T`
is expression-equivalent to:

- `E` if `T` is an unsigned integer;
- otherwise, `std::abs(E)` if `T` is an arithmetic type,
- otherwise, `abs(E)`, if that expression is valid, with overload
  resolution performed in a context that includes the declaration
  ``` cpp
  template<class U> U abs(U) = delete;
  ```

  If the function selected by overload resolution does not return the
  absolute value of its input, the program is ill-formed, no diagnostic
  required.

#### *conj-if-needed* <a id="linalg.helpers.conj">[[linalg.helpers.conj]]</a>

The name *conj-if-needed* denotes an exposition-only function object.
The expression `conj-if-needed(E)` for a subexpression `E` whose type is
`T` is expression-equivalent to:

- `conj(E)`, if `T` is not an arithmetic type and the expression
  `conj(E)` is valid, with overload resolution performed in a context
  that includes the declaration
  ``` cpp
  template<class U> U conj(const U&) = delete;
  ```

  If the function selected by overload resolution does not return the
  complex conjugate of its input, the program is ill-formed, no
  diagnostic required;
- otherwise, `E`.

#### *real-if-needed* <a id="linalg.helpers.real">[[linalg.helpers.real]]</a>

The name *real-if-needed* denotes an exposition-only function object.
The expression `real-if-needed(E)` for a subexpression `E` whose type is
`T` is expression-equivalent to:

- `real(E)`, if `T` is not an arithmetic type and the expression
  `real(E)` is valid, with overload resolution performed in a context
  that includes the declaration
  ``` cpp
  template<class U> U real(const U&) = delete;
  ```

  If the function selected by overload resolution does not return the
  real part of its input, the program is ill-formed, no diagnostic
  required;
- otherwise, `E`.

#### *imag-if-needed* <a id="linalg.helpers.imag">[[linalg.helpers.imag]]</a>

The name *imag-if-needed* denotes an exposition-only function object.
The expression `imag-if-needed(E)` for a subexpression `E` whose type is
`T` is expression-equivalent to:

- `imag(E)`, if `T` is not an arithmetic type and the expression
  `imag(E)` is valid, with overload resolution performed in a context
  that includes the declaration
  ``` cpp
  template<class U> U imag(const U&) = delete;
  ```

  If the function selected by overload resolution does not return the
  imaginary part of its input, the program is ill-formed, no diagnostic
  required;
- otherwise, `((void)E, T{})`.

#### Argument concepts <a id="linalg.helpers.concepts">[[linalg.helpers.concepts]]</a>

The exposition-only concepts defined in this section constrain the
algorithms in [[linalg]].

``` cpp
template<class T>
  constexpr bool is-mdspan = false;

template<class ElementType, class Extents, class Layout, class Accessor>
  constexpr bool is-mdspan<mdspan<ElementType, Extents, Layout, Accessor>> = true;

template<class T>
  concept in-vector =
    is-mdspan<T> && T::rank() == 1;

template<class T>
  concept out-vector =
    is-mdspan<T> && T::rank() == 1 &&
    is_assignable_v<typename T::reference, typename T::element_type> && T::is_always_unique();

template<class T>
  concept inout-vector =
    is-mdspan<T> && T::rank() == 1 &&
    is_assignable_v<typename T::reference, typename T::element_type> && T::is_always_unique();

template<class T>
  concept in-matrix =
    is-mdspan<T> && T::rank() == 2;

template<class T>
  concept out-matrix =
    is-mdspan<T> && T::rank() == 2 &&
    is_assignable_v<typename T::reference, typename T::element_type> && T::is_always_unique();

template<class T>
  concept inout-matrix =
    is-mdspan<T> && T::rank() == 2 &&
    is_assignable_v<typename T::reference, typename T::element_type> && T::is_always_unique();

template<class T>
  constexpr bool is-layout-blas-packed = false;    // exposition only

template<class Triangle, class StorageOrder>
  constexpr bool is-layout-blas-packed<layout_blas_packed<Triangle, StorageOrder>> = true;

template<class T>
  concept possibly-packed-inout-matrix =
    is-mdspan<T> && T::rank() == 2 &&
    is_assignable_v<typename T::reference, typename T::element_type> &&
    (T::is_always_unique() || is-layout-blas-packed<typename T::layout_type>);

template<class T>
  concept in-object =
    is-mdspan<T> && (T::rank() == 1 || T::rank() == 2);

template<class T>
  concept out-object =
    is-mdspan<T> && (T::rank() == 1 || T::rank() == 2) &&
    is_assignable_v<typename T::reference, typename T::element_type> && T::is_always_unique();

template<class T>
  concept inout-object =
    is-mdspan<T> && (T::rank() == 1 || T::rank() == 2) &&
    is_assignable_v<typename T::reference, typename T::element_type> && T::is_always_unique();
```

If a function in [[linalg]] accesses the elements of a parameter
constrained by `in-vector`, `in-matrix`, or `in-object`, those accesses
will not modify the elements.

Unless explicitly permitted, any `inout-vector`, `inout-matrix`,
`inout-object`, `out-vector`, `out-matrix`, `out-object`, or
`possibly-packed-inout-matrix` parameter of a function in [[linalg]]
shall not overlap any other `mdspan` parameter of the function.

#### Mandates <a id="linalg.helpers.mandates">[[linalg.helpers.mandates]]</a>

[*Note 1*: These exposition-only helper functions use the less
constraining input concepts even for the output arguments, because the
additional constraint for assignability of elements is not necessary,
and they are sometimes used in a context where the third argument is an
input type too. — *end note*]

``` cpp
template<class MDS1, class MDS2>
  requires(is-mdspan<MDS1> && is-mdspan<MDS2>)
  constexpr
  bool compatible-static-extents(size_t r1, size_t r2) {         // exposition only
    return MDS1::static_extent(r1) == dynamic_extent ||
           MDS2::static_extent(r2) == dynamic_extent ||
           MDS1::static_extent(r1) == MDS2::static_extent(r2);
  }

template<in-vector In1, in-vector In2, in-vector Out>
  constexpr bool possibly-addable() {                            // exposition only
    return compatible-static-extents<Out, In1>(0, 0) &&
           compatible-static-extents<Out, In2>(0, 0) &&
           compatible-static-extents<In1, In2>(0, 0);
  }

template<in-matrix In1, in-matrix In2, in-matrix Out>
  constexpr bool possibly-addable() {                            // exposition only
    return compatible-static-extents<Out, In1>(0, 0) &&
           compatible-static-extents<Out, In1>(1, 1) &&
           compatible-static-extents<Out, In2>(0, 0) &&
           compatible-static-extents<Out, In2>(1, 1) &&
           compatible-static-extents<In1, In2>(0, 0) &&
           compatible-static-extents<In1, In2>(1, 1);
  }

template<in-matrix InMat, in-vector InVec, in-vector OutVec>
  constexpr bool possibly-multipliable() {                       // exposition only
    return compatible-static-extents<OutVec, InMat>(0, 0) &&
           compatible-static-extents<InMat, InVec>(1, 0);
  }

template<in-vector InVec, in-matrix InMat, in-vector OutVec>
  constexpr bool possibly-multipliable() {                       // exposition only
    return compatible-static-extents<OutVec, InMat>(0, 1) &&
           compatible-static-extents<InMat, InVec>(0, 0);
  }

template<in-matrix InMat1, in-matrix InMat2, in-matrix OutMat>
  constexpr bool possibly-multipliable() {                       // exposition only
    return compatible-static-extents<OutMat, InMat1>(0, 0) &&
           compatible-static-extents<OutMat, InMat2>(1, 1) &&
           compatible-static-extents<InMat1, InMat2>(1, 0);
  }
```

#### Preconditions <a id="linalg.helpers.precond">[[linalg.helpers.precond]]</a>

[*Note 1*: These exposition-only helper functions use the less
constraining input concepts even for the output arguments, because the
additional constraint for assignability of elements is not necessary,
and they are sometimes used in a context where the third argument is an
input type too. — *end note*]

``` cpp
constexpr bool addable(                                          // exposition only
  const in-vector auto& in1, const in-vector auto& in2, const in-vector auto& out) {
  return out.extent(0) == in1.extent(0) && out.extent(0) == in2.extent(0);
}

constexpr bool addable(                                          // exposition only
  const in-matrix auto& in1,  const in-matrix auto& in2, const in-matrix auto& out) {
  return out.extent(0) == in1.extent(0) && out.extent(1) == in1.extent(1) &&
         out.extent(0) == in2.extent(0) && out.extent(1) == in2.extent(1);
}

constexpr bool multipliable(                                     // exposition only
  const in-matrix auto& in_mat, const in-vector auto& in_vec, const in-vector auto& out_vec) {
  return out_vec.extent(0) == in_mat.extent(0) && in_mat.extent(1) == in_vec.extent(0);
}

constexpr bool multipliable( // exposition only
  const in-vector auto& in_vec, const in-matrix auto& in_mat, const in-vector auto& out_vec) {
  return out_vec.extent(0) == in_mat.extent(1) && in_mat.extent(0) == in_vec.extent(0);
}

constexpr bool multipliable(                                     // exposition only
  const in-matrix auto& in_mat1, const in-matrix auto& in_mat2, const in-matrix auto& out_mat) {
  return out_mat.extent(0) == in_mat1.extent(0) && out_mat.extent(1) == in_mat2.extent(1) &&
         in_mat1.extent(1) == in_mat2.extent(0);
}
```

### Scaled in-place transformation <a id="linalg.scaled">[[linalg.scaled]]</a>

#### Introduction <a id="linalg.scaled.intro">[[linalg.scaled.intro]]</a>

The `scaled` function takes a value `alpha` and an `mdspan` `x`, and
returns a new read-only `mdspan` that represents the elementwise product
of `alpha` with each element of `x`.

[*Example 1*:

``` cpp
using Vec = mdspan<double, dextents<size_t, 1>>;

// z = alpha * x + y
void z_equals_alpha_times_x_plus_y(double alpha, Vec x, Vec y, Vec z) {
  add(scaled(alpha, x), y, z);
}

// z = alpha * x + beta * y
void z_equals_alpha_times_x_plus_beta_times_y(double alpha, Vec x, double beta, Vec y, Vec z) {
  add(scaled(alpha, x), scaled(beta, y), z);
}
```

— *end example*]

#### Class template `scaled_accessor` <a id="linalg.scaled.scaledaccessor">[[linalg.scaled.scaledaccessor]]</a>

The class template `scaled_accessor` is an `mdspan` accessor policy
which upon access produces scaled elements. It is part of the
implementation of `scaled` [[linalg.scaled.scaled]].

``` cpp
namespace std::linalg {
  template<class ScalingFactor, class NestedAccessor>
  class scaled_accessor {
  public:
    using element_type =
      add_const_t<decltype(declval<ScalingFactor>() * declval<NestedAccessor::element_type>())>;
    using reference = remove_const_t<element_type>;
    using data_handle_type = NestedAccessor::data_handle_type;
    using offset_policy = scaled_accessor<ScalingFactor, NestedAccessor::offset_policy>;

    constexpr scaled_accessor() = default;
    template<class OtherNestedAccessor>
      explicit(!is_convertible_v<OtherNestedAccessor, NestedAccessor>)
        constexpr scaled_accessor(const scaled_accessor<ScalingFactor,
                                                        OtherNestedAccessor>& other);
    constexpr scaled_accessor(const ScalingFactor& s, const NestedAccessor& a);

    constexpr reference access(data_handle_type p, size_t i) const;
    constexpr offset_policy::data_handle_type offset(data_handle_type p, size_t i) const;

    constexpr const ScalingFactor& scaling_factor() const noexcept { return scaling-factor; }
    constexpr const NestedAccessor& nested_accessor() const noexcept { return nested-accessor; }

  private:
    ScalingFactor scaling-factor{};                              // exposition only
    NestedAccessor nested-accessor{};                            // exposition only
  };
}
```

*Mandates:*

- `element_type` is valid and denotes a type,
- `is_copy_constructible_v<reference>` is `true`,
- `is_reference_v<element_type>` is `false`,
- `ScalingFactor` models `semiregular`, and
- `NestedAccessor` meets the accessor policy requirements
  [[mdspan.accessor.reqmts]].

``` cpp
template<class OtherNestedAccessor>
  explicit(!is_convertible_v<OtherNestedAccessor, NestedAccessor>)
    constexpr scaled_accessor(const scaled_accessor<ScalingFactor, OtherNestedAccessor>& other);
```

*Constraints:*
`is_constructible_v<NestedAccessor, const OtherNestedAccessor&>` is
`true`.

*Effects:*

- Direct-non-list-initializes *scaling-factor* with
  `other.scaling_factor()`, and
- direct-non-list-initializes *nested-accessor* with
  `other.nested_accessor()`.

``` cpp
constexpr scaled_accessor(const ScalingFactor& s, const NestedAccessor& a);
```

*Effects:*

- Direct-non-list-initializes *scaling-factor* with `s`, and
- direct-non-list-initializes *nested-accessor* with `a`.

``` cpp
constexpr reference access(data_handle_type p, size_t i) const;
```

*Returns:*

``` cpp
scaling_factor() * NestedAccessor::element_type(nested-accessor.access(p, i))
```

``` cpp
constexpr offset_policy::data_handle_type offset(data_handle_type p, size_t i) const;
```

*Returns:* *`nested-accessor`*`.offset(p, i)`

#### Function template `scaled` <a id="linalg.scaled.scaled">[[linalg.scaled.scaled]]</a>

The `scaled` function template takes a scaling factor `alpha` and an
`mdspan` `x`, and returns a new read-only `mdspan` with the same domain
as `x`, that represents the elementwise product of `alpha` with each
element of `x`.

``` cpp
template<class ScalingFactor,
           class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto scaled(ScalingFactor alpha, mdspan<ElementType, Extents, Layout, Accessor> x);
```

Let `SA` be `scaled_accessor<ScalingFactor, Accessor>`.

*Returns:*

``` cpp
mdspan<typename SA::element_type, Extents, Layout, SA>(x.data_handle(), x.mapping(),
                                                       SA(alpha, x.accessor()))
```

[*Example 1*:

``` cpp
void test_scaled(mdspan<double, extents<int, 10>> x)
{
  auto x_scaled = scaled(5.0, x);
  for (int i = 0; i < x.extent(0); ++i) {
    assert(x_scaled[i] == 5.0 * x[i]);
  }
}
```

— *end example*]

### Conjugated in-place transformation <a id="linalg.conj">[[linalg.conj]]</a>

#### Introduction <a id="linalg.conj.intro">[[linalg.conj.intro]]</a>

The `conjugated` function takes an `mdspan` `x`, and returns a new
read-only `mdspan` `y` with the same domain as `x`, whose elements are
the complex conjugates of the corresponding elements of `x`.

#### Class template `conjugated_accessor` <a id="linalg.conj.conjugatedaccessor">[[linalg.conj.conjugatedaccessor]]</a>

The class template `conjugated_accessor` is an `mdspan` accessor policy
which upon access produces conjugate elements. It is part of the
implementation of `conjugated` [[linalg.conj.conjugated]].

``` cpp
namespace std::linalg {
  template<class NestedAccessor>
  class conjugated_accessor {
  public:
    using element_type =
      add_const_t<decltype(conj-if-needed(declval<NestedAccessor::element_type>()))>;
    using reference = remove_const_t<element_type>;
    using data_handle_type = NestedAccessor::data_handle_type;
    using offset_policy = conjugated_accessor<NestedAccessor::offset_policy>;

    constexpr conjugated_accessor() = default;
    constexpr conjugated_accessor(const NestedAccessor& acc);
    template<class OtherNestedAccessor>
      explicit(!is_convertible_v<OtherNestedAccessor, NestedAccessor>)
      constexpr conjugated_accessor(const conjugated_accessor<OtherNestedAccessor>& other);

    constexpr reference access(data_handle_type p, size_t i) const;

    constexpr typename offset_policy::data_handle_type
      offset(data_handle_type p, size_t i) const;

    constexpr const NestedAccessor& nested_accessor() const noexcept { return nested-accessor_; }

  private:
    NestedAccessor nested-accessor_{};                           // exposition only
  };
}
```

*Mandates:*

- `element_type` is valid and denotes a type,
- `is_copy_constructible_v<reference>` is `true`,
- `is_reference_v<element_type>` is `false`, and
- `NestedAccessor` meets the accessor policy requirements
  [[mdspan.accessor.reqmts]].

``` cpp
constexpr conjugated_accessor(const NestedAccessor& acc);
```

*Effects:* Direct-non-list-initializes *nested-accessor\_* with `acc`.

``` cpp
template<class OtherNestedAccessor>
  explicit(!is_convertible_v<OtherNestedAccessor, NestedAccessor>)
    constexpr conjugated_accessor(const conjugated_accessor<OtherNestedAccessor>& other);
```

*Constraints:*
`is_constructible_v<NestedAccessor, const OtherNestedAccessor&>` is
`true`.

*Effects:* Direct-non-list-initializes *nested-accessor\_* with
`other.nested_accessor()`.

``` cpp
constexpr reference access(data_handle_type p, size_t i) const;
```

*Returns:*
*`conj-if-needed`*`(NestedAccessor::element_type(`*`nested-accessor_`*`.access(p, i)))`

``` cpp
constexpr typename offset_policy::data_handle_type offset(data_handle_type p, size_t i) const;
```

*Returns:* *`nested-accessor_`*`.offset(p, i)`

#### Function template `conjugated` <a id="linalg.conj.conjugated">[[linalg.conj.conjugated]]</a>

``` cpp
template<class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto conjugated(mdspan<ElementType, Extents, Layout, Accessor> a);
```

Let `A` be

- `remove_cvref_t<decltype(a.accessor().nested_accessor())>` if
  `Accessor` is a specialization of `conjugated_accessor`;
- otherwise, `Accessor` if `remove_cvref_t<ElementType>` is an
  arithmetic type;
- otherwise, `conjugated_accessor<Accessor>` if the expression `conj(E)`
  is valid for any subexpression `E` whose type is
  `remove_cvref_t<ElementType>` with overload resolution performed in a
  context that includes the declaration
  `template<class U> U conj(const U&) = delete;`;
- otherwise, `Accessor`.

*Returns:* Let `MD` be
`mdspan<typename A::element_type, Extents, Layout, A>`.

- `MD(a.data_handle(), a.mapping(), a.accessor().nested_accessor())` if
  `Accessor` is aspecialization of `conjugated_accessor`;
- otherwise, `a`, if `is_same_v<A, Accessor>` is `true`;
- otherwise,
  `MD(a.data_handle(), a.mapping(), conjugated_accessor(a.accessor()))`.

[*Example 1*:

``` cpp
void test_conjugated_complex(mdspan<complex<double>, extents<int, 10>> a) {
  auto a_conj = conjugated(a);
  for (int i = 0; i < a.extent(0); ++i) {
    assert(a_conj[i] == conj(a[i]);
  }
  auto a_conj_conj = conjugated(a_conj);
  for (int i = 0; i < a.extent(0); ++i) {
    assert(a_conj_conj[i] == a[i]);
  }
}

void test_conjugated_real(mdspan<double, extents<int, 10>> a) {
  auto a_conj = conjugated(a);
  for (int i = 0; i < a.extent(0); ++i) {
    assert(a_conj[i] == a[i]);
  }
  auto a_conj_conj = conjugated(a_conj);
  for (int i = 0; i < a.extent(0); ++i) {
    assert(a_conj_conj[i] == a[i]);
  }
}
```

— *end example*]

### Transpose in-place transformation <a id="linalg.transp">[[linalg.transp]]</a>

#### Introduction <a id="linalg.transp.intro">[[linalg.transp.intro]]</a>

`layout_transpose` is an `mdspan` layout mapping policy that swaps the
two indices, extents, and strides of any unique `mdspan` layout mapping
policy.

The `transposed` function takes an `mdspan` representing a matrix, and
returns a new `mdspan` representing the transpose of the input matrix.

#### Exposition-only helpers for `layout_transpose` and `transposed` <a id="linalg.transp.helpers">[[linalg.transp.helpers]]</a>

The exposition-only *transpose-extents* function takes an `extents`
object representing the extents of a matrix, and returns a new `extents`
object representing the extents of the transpose of the matrix.

The exposition-only alias template `transpose-extents-t<InputExtents>`
gives the type of `transpose-extents(e)` for a given `extents` object
`e` of type `InputExtents`.

``` cpp
template<class IndexType, size_t InputExtent0, size_t InputExtent1>
  constexpr extents<IndexType, InputExtent1, InputExtent0>
    transpose-extents(const extents<IndexType, InputExtent0, InputExtent1>& in);   // exposition only
```

*Returns:*
`extents<IndexType, InputExtent1, InputExtent0>(in.extent(1), in.extent(0))`

``` cpp
template<class InputExtents>
  using transpose-extents-t =
    decltype(transpose-extents(declval<InputExtents>()));        // exposition only
```

#### Class template `layout_transpose` <a id="linalg.transp.layout.transpose">[[linalg.transp.layout.transpose]]</a>

`layout_transpose` is an `mdspan` layout mapping policy that swaps the
two indices, extents, and strides of any `mdspan` layout mapping policy.

``` cpp
namespace std::linalg {
  template<class Layout>
  class layout_transpose {
  public:
    using nested_layout_type = Layout;

    template<class Extents>
    struct mapping {
    private:
      using nested-mapping-type =
        Layout::template mapping<transpose-extents-t<Extents>>;  // exposition only

    public:
      using extents_type = Extents;
      using index_type = extents_type::index_type;
      using size_type = extents_type::size_type;
      using rank_type = extents_type::rank_type;
      using layout_type = layout_transpose;

      constexpr explicit mapping(const nested-mapping-type&);

      constexpr const extents_type& extents() const noexcept { return extents_; }

      constexpr index_type required_span_size() const
        { return nested-mapping_.required_span_size();

      template<class Index0, class Index1>
        constexpr index_type operator()(Index0 ind0, Index1 ind1) const
        { return nested-mapping_(ind1, ind0); }

      constexpr const nested-mapping-type& nested_mapping() const noexcept
        { return nested-mapping_; }

      static constexpr bool is_always_unique() noexcept
        { return nested-mapping-type::is_always_unique(); }
      static constexpr bool is_always_exhaustive() noexcept
        { return nested-mapping-type::is_always_exhaustive(); }
      static constexpr bool is_always_strided() noexcept
        { return nested-mapping-type::is_always_strided(); }

      constexpr bool is_unique() const { return nested-mapping_.is_unique(); }
      constexpr bool is_exhaustive() const { return nested-mapping_.is_exhaustive(); }
      constexpr bool is_strided() const { return nested-mapping_.is_strided(); }

      constexpr index_type stride(size_t r) const;

      template<class OtherExtents>
        friend constexpr bool operator==(const mapping& x, const mapping<OtherExtents>& y);

    private:
      nested-mapping-type nested-mapping_;                       // exposition only
      extents_type extents_;                                     // exposition only
    };
  };
}
```

`Layout` shall meet the layout mapping policy requirements
[[mdspan.layout.policy.reqmts]].

*Mandates:*

- `Extents` is a specialization of `std::extents`, and
- `Extents::rank()` equals 2.

``` cpp
constexpr explicit mapping(const nested-mapping-type& map);
```

*Effects:*

- Initializes *nested-mapping\_* with `map`, and
- initializes *extents\_* with *`transpose-extents`*`(map.extents())`.

``` cpp
constexpr index_type stride(size_t r) const;
```

*Preconditions:*

- `is_strided()` is `true`, and
- `r < 2` is `true`.

*Returns:* *`nested-mapping_`*`.stride(r == 0 ? 1 : 0)`

``` cpp
template<class OtherExtents>
  friend constexpr bool operator==(const mapping& x, const mapping<OtherExtents>& y);
```

*Constraints:* The expression
`x.`*`nested-mapping_`*` == y.`*`nested-mapping_`* is well-formed and
its result is convertible to `bool`.

*Returns:* `x.`*`nested-mapping_`*` == y.`*`nested-mapping_`*.

#### Function template `transposed` <a id="linalg.transp.transposed">[[linalg.transp.transposed]]</a>

The `transposed` function takes a rank-2 `mdspan` representing a matrix,
and returns a new `mdspan` representing the input matrix’s transpose.
The input matrix’s data are not modified, and the returned `mdspan`
accesses the input matrix’s data in place.

``` cpp
template<class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto transposed(mdspan<ElementType, Extents, Layout, Accessor> a);
```

*Mandates:* `Extents::rank() == 2` is `true`.

Let `ReturnExtents` be *`transpose-extents-t`*`<Extents>`. Let `R` be
`mdspan<ElementType, ReturnExtents, ReturnLayout, Accessor>`, where
`ReturnLayout` is:

- `layout_right` if `Layout` is `layout_left`;
- otherwise, `layout_left` if `Layout` is `layout_right`;
- otherwise, `layout_right_padded<PaddingValue>` if `Layout` is
  `layout_left_padded<PaddingValue>` for some `size_t` value
  `PaddingValue`;
- otherwise, `layout_left_padded<PaddingValue>` if `Layout` is
  `layout_right_padded<PaddingValue>` for some `size_t` value
  `PaddingValue`;
- otherwise, `layout_stride` if `Layout` is `layout_stride`;
- otherwise,
  `layout_blas_packed<OppositeTriangle, OppositeStorageOrder>`, if
  `Layout` is `layout_blas_packed<Triangle, StorageOrder>` for some
  `Triangle` and `StorageOrder`, where
  - `OppositeTriangle` is
    ``` cpp
    conditional_t<is_same_v<Triangle, upper_triangle_t>,
                  lower_triangle_t, upper_triangle_t>
    ```

    and
  - `OppositeStorageOrder` is
    ``` cpp
    conditional_t<is_same_v<StorageOrder, column_major_t>, row_major_t, column_major_t>
    ```
- otherwise, `NestedLayout` if `Layout` is
  `layout_transpose<NestedLayout>` for some `NestedLayout`;
- otherwise, `layout_transpose<Layout>`.

*Returns:* With `ReturnMapping` being the type
`typename ReturnLayout::template mapping<ReturnExtents>`:

- if `Layout` is `layout_left`, `layout_right`, or a specialization of
  `layout_blas_packed`,
  ``` cpp
  R(a.data_handle(), ReturnMapping(transpose-extents(a.mapping().extents())),
    a.accessor())
  ```
- otherwise,
  ``` cpp
  R(a.data_handle(), ReturnMapping(transpose-extents(a.mapping().extents()),
    a.mapping().stride(1)), a.accessor())
  ```

  if `Layout` is `layout_left_padded<PaddingValue>` for some `size_t`
  value `PaddingValue`;
- otherwise,
  ``` cpp
  R(a.data_handle(), ReturnMapping(transpose-extents(a.mapping().extents()),
    a.mapping().stride(0)), a.accessor())
  ```

  if `Layout` is `layout_right_padded<PaddingValue>` for some `size_t`
  value `PaddingValue`;
- otherwise, if `Layout` is `layout_stride`,
  ``` cpp
  R(a.data_handle(), ReturnMapping(transpose-extents(a.mapping().extents()),
    array{a.mapping().stride(1), a.mapping().stride(0)}), a.accessor())
  ```
- otherwise, if `Layout` is a specialization of `layout_transpose`,
  ``` cpp
  R(a.data_handle(), a.mapping().nested_mapping(), a.accessor())
  ```
- otherwise,
  ``` cpp
  R(a.data_handle(), ReturnMapping(a.mapping()), a.accessor())
  ```

[*Example 1*:

``` cpp
void test_transposed(mdspan<double, extents<size_t, 3, 4>> a) {
  const auto num_rows = a.extent(0);
  const auto num_cols = a.extent(1);

  auto a_t = transposed(a);
  assert(num_rows == a_t.extent(1));
  assert(num_cols == a_t.extent(0));
  assert(a.stride(0) == a_t.stride(1));
  assert(a.stride(1) == a_t.stride(0));

  for (size_t row = 0; row < num_rows; ++row) {
    for (size_t col = 0; col < num_rows; ++col) {
      assert(a[row, col] == a_t[col, row]);
    }
  }

  auto a_t_t = transposed(a_t);
  assert(num_rows == a_t_t.extent(0));
  assert(num_cols == a_t_t.extent(1));
  assert(a.stride(0) == a_t_t.stride(0));
  assert(a.stride(1) == a_t_t.stride(1));

  for (size_t row = 0; row < num_rows; ++row) {
    for (size_t col = 0; col < num_rows; ++col) {
      assert(a[row, col] == a_t_t[row, col]);
    }
  }
}
```

— *end example*]

### Conjugate transpose in-place transform <a id="linalg.conjtransposed">[[linalg.conjtransposed]]</a>

The `conjugate_transposed` function returns a conjugate transpose view
of an object. This combines the effects of `transposed` and
`conjugated`.

``` cpp
template<class ElementType, class Extents, class Layout, class Accessor>
    constexpr auto conjugate_transposed(mdspan<ElementType, Extents, Layout, Accessor> a);
```

*Effects:* Equivalent to: `return conjugated(transposed(a));`

[*Example 1*:

``` cpp
void test_conjugate_transposed(mdspan<complex<double>, extents<size_t, 3, 4>> a) {
  const auto num_rows = a.extent(0);
  const auto num_cols = a.extent(1);

  auto a_ct = conjugate_transposed(a);
  assert(num_rows == a_ct.extent(1));
  assert(num_cols == a_ct.extent(0));
  assert(a.stride(0) == a_ct.stride(1));
  assert(a.stride(1) == a_ct.stride(0));

  for (size_t row = 0; row < num_rows; ++row) {
    for (size_t col = 0; col < num_rows; ++col) {
      assert(a[row, col] == conj(a_ct[col, row]));
    }
  }

  auto a_ct_ct = conjugate_transposed(a_ct);
  assert(num_rows == a_ct_ct.extent(0));
  assert(num_cols == a_ct_ct.extent(1));
  assert(a.stride(0) == a_ct_ct.stride(0));
  assert(a.stride(1) == a_ct_ct.stride(1));

  for (size_t row = 0; row < num_rows; ++row) {
    for (size_t col = 0; col < num_rows; ++col) {
      assert(a[row, col] == a_ct_ct[row, col]);
      assert(conj(a_ct[col, row]) == a_ct_ct[row, col]);
    }
  }
}
```

— *end example*]

### Algorithm requirements based on template parameter name <a id="linalg.algs.reqs">[[linalg.algs.reqs]]</a>

Throughout [[linalg.algs.blas1]], [[linalg.algs.blas2]], and
[[linalg.algs.blas3]], where the template parameters are not
constrained, the names of template parameters are used to express the
following constraints.

- `is_execution_policy<ExecutionPolicy>::value` is `true`
  [[execpol.type]].
- `Real` is any type such that `complex<Real>` is specified
  [[complex.numbers.general]].
- `Triangle` is either `upper_triangle_t` or `lower_triangle_t`.
- `DiagonalStorage` is either `implicit_unit_diagonal_t` or
  `explicit_diagonal_t`.

[*Note 1*: Function templates that have a template parameter named
`ExecutionPolicy` are parallel algorithms
[[algorithms.parallel.defns]]. — *end note*]

### BLAS 1 algorithms <a id="linalg.algs.blas1">[[linalg.algs.blas1]]</a>

#### Complexity <a id="linalg.algs.blas1.complexity">[[linalg.algs.blas1.complexity]]</a>

*Complexity:* All algorithms in [[linalg.algs.blas1]] with `mdspan`
parameters perform a count of `mdspan` array accesses and arithmetic
operations that is linear in the maximum product of extents of any
`mdspan` parameter.

#### Givens rotations <a id="linalg.algs.blas1.givens">[[linalg.algs.blas1.givens]]</a>

##### Compute Givens rotation <a id="linalg.algs.blas1.givens.lartg">[[linalg.algs.blas1.givens.lartg]]</a>

``` cpp
template<class Real>
  setup_givens_rotation_result<Real> setup_givens_rotation(Real a, Real b) noexcept;

template<class Real>
  setup_givens_rotation_result<complex<Real>>
    setup_givens_rotation(complex<Real> a, complex<Real> b) noexcept;
```

These functions compute the Givens plane rotation represented by the two
values c and s such that the 2 x 2 system of equations
$$\left[ \begin{matrix}
c             & s \\
-\overline{s} & c \\
\end{matrix} \right]
\cdot
\left[ \begin{matrix}
a \\
b \\
\end{matrix} \right]
=
\left[ \begin{matrix}
r \\
0 \\
\end{matrix} \right]$$

holds, where c is always a real scalar, and c² + |s|^2 = 1. That is, c
and s represent a 2 x 2 matrix, that when multiplied by the right by the
input vector whose components are a and b, produces a result vector
whose first component r is the Euclidean norm of the input vector, and
whose second component is zero.

[*Note 1*: These functions correspond to the LAPACK function
`xLARTG`. — *end note*]

*Returns:* `c, s, r`, where `c` and `s` form the Givens plane rotation
corresponding to the input `a` and `b`, and `r` is the Euclidean norm of
the two-component vector formed by `a` and `b`.

##### Apply a computed Givens rotation to vectors <a id="linalg.algs.blas1.givens.rot">[[linalg.algs.blas1.givens.rot]]</a>

``` cpp
template<inout-vector InOutVec1, inout-vector InOutVec2, class Real>
  void apply_givens_rotation(InOutVec1 x, InOutVec2 y, Real c, Real s);
template<class ExecutionPolicy, inout-vector InOutVec1, inout-vector InOutVec2, class Real>
  void apply_givens_rotation(ExecutionPolicy&& exec,
                             InOutVec1 x, InOutVec2 y, Real c, Real s);
template<inout-vector InOutVec1, inout-vector InOutVec2, class Real>
  void apply_givens_rotation(InOutVec1 x, InOutVec2 y, Real c, complex<Real> s);
template<class ExecutionPolicy, inout-vector InOutVec1, inout-vector InOutVec2, class Real>
  void apply_givens_rotation(ExecutionPolicy&& exec,
                             InOutVec1 x, InOutVec2 y, Real c, complex<Real> s);
```

[*Note 2*: These functions correspond to the BLAS function
`xROT`. — *end note*]

*Mandates:* *`compatible-static-extents`*`<InOutVec1, InOutVec2>(0, 0)`
is `true`.

*Preconditions:* `x.extent(0)` equals `y.extent(0)`.

*Effects:* Applies the plane rotation specified by `c` and `s` to the
input vectors `x` and `y`, as if the rotation were a 2 x 2 matrix and
the input vectors were successive rows of a matrix with two rows.

#### Swap matrix or vector elements <a id="linalg.algs.blas1.swap">[[linalg.algs.blas1.swap]]</a>

``` cpp
template<inout-object InOutObj1, inout-object InOutObj2>
  void swap_elements(InOutObj1 x, InOutObj2 y);
template<class ExecutionPolicy, inout-object InOutObj1, inout-object InOutObj2>
  void swap_elements(ExecutionPolicy&& exec, InOutObj1 x, InOutObj2 y);
```

[*Note 1*: These functions correspond to the BLAS function
`xSWAP`. — *end note*]

*Constraints:* `x.rank()` equals `y.rank()`.

*Mandates:* For all `r` in the range [0, `x.rank()`),

``` cpp
compatible-static-extents<InOutObj1, InOutObj2>(r, r)
```

is `true`.

*Preconditions:* `x.extents()` equals `y.extents()`.

*Effects:* Swaps all corresponding elements of `x` and `y`.

#### Multiply the elements of an object in place by a scalar <a id="linalg.algs.blas1.scal">[[linalg.algs.blas1.scal]]</a>

``` cpp
template<class Scalar, inout-object InOutObj>
  void scale(Scalar alpha, InOutObj x);
template<class ExecutionPolicy, class Scalar, inout-object InOutObj>
  void scale(ExecutionPolicy&& exec, Scalar alpha, InOutObj x);
```

[*Note 1*: These functions correspond to the BLAS function
`xSCAL`. — *end note*]

*Effects:* Overwrites x with the result of computing the elementwise
multiplication α x, where the scalar α is `alpha`.

#### Copy elements of one matrix or vector into another <a id="linalg.algs.blas1.copy">[[linalg.algs.blas1.copy]]</a>

``` cpp
template<in-object InObj, out-object OutObj>
  void copy(InObj x, OutObj y);
template<class ExecutionPolicy, in-object InObj, out-object OutObj>
  void copy(ExecutionPolicy&& exec, InObj x, OutObj y);
```

[*Note 1*: These functions correspond to the BLAS function
`xCOPY`. — *end note*]

*Constraints:* `x.rank()` equals `y.rank()`.

*Mandates:* For all `r` in the range [ 0, `x.rank()`),

``` cpp
compatible-static-extents<InObj, OutObj>(r, r)
```

is `true`.

*Preconditions:* `x.extents()` equals `y.extents()`.

*Effects:* Assigns each element of x to the corresponding element of y.

#### Add vectors or matrices elementwise <a id="linalg.algs.blas1.add">[[linalg.algs.blas1.add]]</a>

``` cpp
template<in-object InObj1, in-object InObj2, out-object OutObj>
  void add(InObj1 x, InObj2 y, OutObj z);
template<class ExecutionPolicy, in-object InObj1, in-object InObj2, out-object OutObj>
  void add(ExecutionPolicy&& exec,
           InObj1 x, InObj2 y, OutObj z);
```

[*Note 1*: These functions correspond to the BLAS function
`xAXPY`. — *end note*]

*Constraints:* `x.rank()`, `y.rank()`, and `z.rank()` are all equal.

*Mandates:* *`possibly-addable`*`<InObj1, InObj2, OutObj>()` is `true`.

*Preconditions:* *`addable`*`(x,y,z)` is `true`.

*Effects:* Computes z = x + y.

*Remarks:* `z` may alias `x` or `y`.

#### Dot product of two vectors <a id="linalg.algs.blas1.dot">[[linalg.algs.blas1.dot]]</a>

[*Note 1*: The functions in this section correspond to the BLAS
functions `xDOT`, `xDOTU`, and `xDOTC`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas1.dot]].

*Mandates:* `compatible-static-extents<InVec1, InVec2>(0, 0)` is `true`.

*Preconditions:* `v1.extent(0)` equals `v2.extent(0)`.

``` cpp
template<in-vector InVec1, in-vector InVec2, class Scalar>
  Scalar dot(InVec1 v1, InVec2 v2, Scalar init);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, class Scalar>
  Scalar dot(ExecutionPolicy&& exec,
             InVec1 v1, InVec2 v2, Scalar init);
```

These functions compute a non-conjugated dot product with an explicitly
specified result type.

*Returns:* Let `N` be `v1.extent(0)`.

- `init` if `N` is zero;
- otherwise, *GENERALIZED_SUM*(plus\<\>(), init, v1\[0\]\*v2\[0\], …,
  v1\[N-1\]\*v2\[N-1\]).

*Remarks:* If `InVec1::value_type`, `InVec2::value_type`, and `Scalar`
are all floating-point types or specializations of `complex`, and if
`Scalar` has higher precision than `InVec1::value_type` or
`InVec2::value_type`, then intermediate terms in the sum use `Scalar`’s
precision or greater.

``` cpp
template<in-vector InVec1, in-vector InVec2>
    auto dot(InVec1 v1, InVec2 v2);
  template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2>
    auto dot(ExecutionPolicy&& exec,
             InVec1 v1, InVec2 v2);
```

These functions compute a non-conjugated dot product with a default
result type.

*Effects:* Let `T` be
`decltype(declval<typename InVec1::value_type>() * declval<typename InVec2::value_type>())`.
Then,

- the two-parameter overload is equivalent to:
  ``` cpp
  return dot(v1, v2, T{});
  ```

  and
- the three-parameter overload is equivalent to:
  ``` cpp
  return dot(std::forward<ExecutionPolicy>(exec), v1, v2, T{});
  ```

``` cpp
template<in-vector InVec1, in-vector InVec2, class Scalar>
  Scalar dotc(InVec1 v1, InVec2 v2, Scalar init);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, class Scalar>
  Scalar dotc(ExecutionPolicy&& exec,
              InVec1 v1, InVec2 v2, Scalar init);
```

These functions compute a conjugated dot product with an explicitly
specified result type.

*Effects:*

- The three-parameter overload is equivalent to:
  ``` cpp
  return dot(conjugated(v1), v2, init);
  ```

  and
- the four-parameter overload is equivalent to:
  ``` cpp
  return dot(std::forward<ExecutionPolicy>(exec), conjugated(v1), v2, init);
  ```

``` cpp
template<in-vector InVec1, in-vector InVec2>
  auto dotc(InVec1 v1, InVec2 v2);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2>
  auto dotc(ExecutionPolicy&& exec,
            InVec1 v1, InVec2 v2);
```

These functions compute a conjugated dot product with a default result
type.

*Effects:* Let `T` be
`decltype(`*`conj-if-needed`*`(declval<typename InVec1::value_type>()) * declval<typename InVec2::value_type>())`.
Then,

- the two-parameter overload is equivalent to:
  ``` cpp
  return dotc(v1, v2, T{});
  ```

  and
- the three-parameter overload is equivalent to
  ``` cpp
  return dotc(std::forward<ExecutionPolicy>(exec), v1, v2, T{});
  ```

#### Scaled sum of squares of a vector’s elements <a id="linalg.algs.blas1.ssq">[[linalg.algs.blas1.ssq]]</a>

``` cpp
template<in-vector InVec, class Scalar>
  sum_of_squares_result<Scalar> vector_sum_of_squares(InVec v, sum_of_squares_result<Scalar> init);
template<class ExecutionPolicy, in-vector InVec, class Scalar>
  sum_of_squares_result<Scalar> vector_sum_of_squares(ExecutionPolicy&& exec,
                                                      InVec v, sum_of_squares_result<Scalar> init);
```

[*Note 1*: These functions correspond to the LAPACK function
`xLASSQ`. — *end note*]

*Mandates:*
`decltype(`*`abs-if-needed`*`(declval<typename InVec::value_type>()))`
is convertible to `Scalar`.

*Effects:* Returns a value `result` such that

- `result.scaling_factor` is the maximum of `init.scaling_factor` and
  *`abs-if-needed`*`(x[i])` for all `i` in the domain of `v`; and
- let `s2init` be
  ``` cpp
  init.scaling_factor * init.scaling_factor * init.scaled_sum_of_squares
  ```

  then
  `result.scaling_factor * result.scaling_factor * result.scaled_sum_of_squares`
  equals the sum of `s2init` and the squares of
  *`abs-if-needed`*`(x[i])` for all `i` in the domain of `v`.

*Remarks:* If `InVec::value_type`, and `Scalar` are all floating-point
types or specializations of `complex`, and if `Scalar` has higher
precision than `InVec::value_type`, then intermediate terms in the sum
use `Scalar`’s precision or greater.

#### Euclidean norm of a vector <a id="linalg.algs.blas1.nrm2">[[linalg.algs.blas1.nrm2]]</a>

``` cpp
template<in-vector InVec, class Scalar>
  Scalar vector_two_norm(InVec v, Scalar init);
template<class ExecutionPolicy, in-vector InVec, class Scalar>
  Scalar vector_two_norm(ExecutionPolicy&& exec, InVec v, Scalar init);
```

[*Note 1*: These functions correspond to the BLAS function
`xNRM2`. — *end note*]

*Mandates:* Let `a` be
*`abs-if-needed`*`(declval<typename InVec::value_type>())`. Then,
`decltype(init + a * a` is convertible to `Scalar`.

*Returns:* The square root of the sum of the square of `init` and the
squares of the absolute values of the elements of `v`.

[*Note 2*: For `init` equal to zero, this is the Euclidean norm (also
called 2-norm) of the vector `v`. — *end note*]

*Remarks:* If `InVec::value_type`, and `Scalar` are all floating-point
types or specializations of `complex`, and if `Scalar` has higher
precision than `InVec::value_type`, then intermediate terms in the sum
use `Scalar`’s precision or greater.

[*Note 3*: An implementation of this function for floating-point types
`T` can use the `scaled_sum_of_squares` result from
`vector_sum_of_squares(x, {.scaling_factor=1.0, .scaled_sum_of_squares=init})`. — *end note*]

``` cpp
template<in-vector InVec>
  auto vector_two_norm(InVec v);
template<class ExecutionPolicy, in-vector InVec>
  auto vector_two_norm(ExecutionPolicy&& exec, InVec v);
```

*Effects:* Let `a` be
*`abs-if-needed`*`(declval<typename InVec::value_type>())`. Let `T` be
`decltype(a * a)`. Then,

- the one-parameter overload is equivalent to:
  ``` cpp
  return vector_two_norm(v, T{});
  ```

  and
- the two-parameter overload is equivalent to:
  ``` cpp
  return vector_two_norm(std::forward<ExecutionPolicy>(exec), v, T{});
  ```

#### Sum of absolute values of vector elements <a id="linalg.algs.blas1.asum">[[linalg.algs.blas1.asum]]</a>

``` cpp
template<in-vector InVec, class Scalar>
  Scalar vector_abs_sum(InVec v, Scalar init);
template<class ExecutionPolicy, in-vector InVec, class Scalar>
  Scalar vector_abs_sum(ExecutionPolicy&& exec, InVec v, Scalar init);
```

[*Note 1*: These functions correspond to the BLAS functions `SASUM`,
`DASUM`, `SCASUM`, and `DZASUM`. — *end note*]

*Mandates:*

``` cpp
decltype(init + abs-if-needed(real-if-needed(declval<typename InVec::value_type>())) +
                abs-if-needed(imag-if-needed(declval<typename InVec::value_type>())))
```

is convertible to `Scalar`.

*Returns:* Let `N` be `v.extent(0)`.

- `init` if `N` is zero;
- otherwise, if `InVec::value_type` is an arithmetic type,
  ``` cpp
  GENERALIZED_SUM(plus<>(), init, abs-if-needed(v[0]), …, abs-if-needed(v[N-1]))
  ```
- otherwise,
  ``` cpp
  GENERALIZED_SUM(plus<>(), init,
         abs-if-needed(real-if-needed(v[0])) + abs-if-needed(imag-if-needed(v[0])),
         …,
         abs-if-needed(real-if-needed(v[N-1])) + abs-if-needed(imag-if-needed(v[N-1])))
  ```

*Remarks:* If `InVec::value_type` and `Scalar` are all floating-point
types or specializations of `complex`, and if `Scalar` has higher
precision than `InVec::value_type`, then intermediate terms in the sum
use `Scalar`’s precision or greater.

``` cpp
template<in-vector InVec>
  auto vector_abs_sum(InVec v);
template<class ExecutionPolicy, in-vector InVec>
  auto vector_abs_sum(ExecutionPolicy&& exec, InVec v);
```

*Effects:* Let `T` be `typename InVec::value_type`. Then,

- the one-parameter overload is equivalent to:
  ``` cpp
  return vector_abs_sum(v, T{});
  ```

  and
- the two-parameter overload is equivalent to:
  ``` cpp
  return vector_abs_sum(std::forward<ExecutionPolicy>(exec), v, T{});
  ```

#### Index of maximum absolute value of vector elements <a id="linalg.algs.blas1.iamax">[[linalg.algs.blas1.iamax]]</a>

``` cpp
template<in-vector InVec>
  typename InVec::extents_type vector_idx_abs_max(InVec v);
template<class ExecutionPolicy, in-vector InVec>
  typename InVec::extents_type vector_idx_abs_max(ExecutionPolicy&& exec, InVec v);
```

[*Note 1*: These functions correspond to the BLAS function
`IxAMAX`. — *end note*]

Let `T` be

``` cpp
decltype(abs-if-needed(real-if-needed(declval<typename InVec::value_type>())) +
         abs-if-needed(imag-if-needed(declval<typename InVec::value_type>())))
```

*Mandates:* `declval<T>() < declval<T>()` is a valid expression.

*Returns:*

- `numeric_limits<typename InVec::size_type>::max()` if `v` has zero
  elements;
- otherwise, the index of the first element of `v` having largest
  absolute value, if `InVec::value_type` is an arithmetic type;
- otherwise, the index of the first element `vₑ` of `v` for which
  ``` cpp
  abs-if-needed(real-if-needed($v_e$)) + abs-if-needed(imag-if-needed($v_e$))
  ```

  has the largest value.

#### Frobenius norm of a matrix <a id="linalg.algs.blas1.matfrobnorm">[[linalg.algs.blas1.matfrobnorm]]</a>

[*Note 1*: These functions exist in the BLAS standard but are not part
of the reference implementation. — *end note*]

``` cpp
template<in-matrix InMat, class Scalar>
  Scalar matrix_frob_norm(InMat A, Scalar init);
template<class ExecutionPolicy, in-matrix InMat, class Scalar>
  Scalar matrix_frob_norm(ExecutionPolicy&& exec, InMat A, Scalar init);
```

*Mandates:* Let `a` be
*`abs-if-needed`*`(declval<typename InMat::value_type>())`. Then,
`decltype(init + a * a)` is convertible to `Scalar`.

*Returns:* The square root of the sum of squares of `init` and the
absolute values of the elements of `A`.

[*Note 1*: For `init` equal to zero, this is the Frobenius norm of the
matrix `A`. — *end note*]

*Remarks:* If `InMat::value_type` and `Scalar` are all floating-point
types or specializations of `complex`, and if `Scalar` has higher
precision than `InMat::value_type`, then intermediate terms in the sum
use `Scalar`’s precision or greater.

``` cpp
template<in-matrix InMat>
  auto matrix_frob_norm(InMat A);
template<class ExecutionPolicy, in-matrix InMat>
  auto matrix_frob_norm(ExecutionPolicy&& exec, InMat A);
```

*Effects:* Let `a` be
*`abs-if-needed`*`(declval<typename InMat::value_type>())`. Let `T` be
`decltype(a * a)`. Then,

- the one-parameter overload is equivalent to:
  ``` cpp
  return matrix_frob_norm(A, T{});
  ```

  and
- the two-parameter overload is equivalent to:
  ``` cpp
  return matrix_frob_norm(std::forward<ExecutionPolicy>(exec), A, T{});
  ```

#### One norm of a matrix <a id="linalg.algs.blas1.matonenorm">[[linalg.algs.blas1.matonenorm]]</a>

[*Note 1*: These functions exist in the BLAS standard but are not part
of the reference implementation. — *end note*]

``` cpp
template<in-matrix InMat, class Scalar>
  Scalar matrix_one_norm(InMat A, Scalar init);
template<class ExecutionPolicy, in-matrix InMat, class Scalar>
  Scalar matrix_one_norm(ExecutionPolicy&& exec, InMat A, Scalar init);
```

*Mandates:*
`decltype(`*`abs-if-needed`*`(declval<typename InMat::value_type>()))`
is convertible to `Scalar`.

*Returns:*

- `init` if `A.extent(1)` is zero;
- otherwise, the sum of `init` and the one norm of the matrix A.

[*Note 1*: The one norm of the matrix `A` is the maximum over all
columns of `A`, of the sum of the absolute values of the elements of the
column. — *end note*]

*Remarks:* If `InMat::value_type` and `Scalar` are all floating-point
types or specializations of `complex`, and if `Scalar` has higher
precision than `InMat::value_type`, then intermediate terms in the sum
use `Scalar`’s precision or greater.

``` cpp
template<in-matrix InMat>
  auto matrix_one_norm(InMat A);
template<class ExecutionPolicy, in-matrix InMat>
  auto matrix_one_norm(ExecutionPolicy&& exec, InMat A);
```

*Effects:* Let `T` be
`decltype(`*`abs-if-needed`*`(declval<typename InMat::value_type>())`.
Then,

- the one-parameter overload is equivalent to:
  ``` cpp
  return matrix_one_norm(A, T{});
  ```

  and
- the two-parameter overload is equivalent to:
  ``` cpp
  return matrix_one_norm(std::forward<ExecutionPolicy>(exec), A, T{});
  ```

#### Infinity norm of a matrix <a id="linalg.algs.blas1.matinfnorm">[[linalg.algs.blas1.matinfnorm]]</a>

[*Note 1*: These functions exist in the BLAS standard but are not part
of the reference implementation. — *end note*]

``` cpp
template<in-matrix InMat, class Scalar>
  Scalar matrix_inf_norm(InMat A, Scalar init);
template<class ExecutionPolicy, in-matrix InMat, class Scalar>
  Scalar matrix_inf_norm(ExecutionPolicy&& exec, InMat A, Scalar init);
```

*Mandates:*
`decltype(`*`abs-if-needed`*`(declval<typename InMat::value_type>()))`
is convertible to `Scalar`.

*Returns:*

- `init` if `A.extent(0)` is zero;
- otherwise, the sum of `init` and the infinity norm of the matrix `A`.

[*Note 1*: The infinity norm of the matrix `A` is the maximum over all
rows of `A`, of the sum of the absolute values of the elements of the
row. — *end note*]

*Remarks:* If `InMat::value_type` and `Scalar` are all floating-point
types or specializations of `complex`, and if `Scalar` has higher
precision than `InMat::value_type`, then intermediate terms in the sum
use `Scalar`’s precision or greater.

``` cpp
template<in-matrix InMat>
  auto matrix_inf_norm(InMat A);
template<class ExecutionPolicy, in-matrix InMat>
  auto matrix_inf_norm(ExecutionPolicy&& exec, InMat A);
```

*Effects:* Let `T` be
`decltype(`*`abs-if-needed`*`(declval<typename InMat::value_type>())`.
Then,

- the one-parameter overload is equivalent to:
  ``` cpp
  return matrix_inf_norm(A, T{});
  ```

  and
- the two-parameter overload is equivalent to:
  ``` cpp
  return matrix_inf_norm(std::forward<ExecutionPolicy>(exec), A, T{});
  ```

### BLAS 2 algorithms <a id="linalg.algs.blas2">[[linalg.algs.blas2]]</a>

#### General matrix-vector product <a id="linalg.algs.blas2.gemv">[[linalg.algs.blas2.gemv]]</a>

[*Note 1*: These functions correspond to the BLAS function
`xGEMV`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.gemv]].

*Mandates:*

- `possibly-multipliable<decltype(A), decltype(x), decltype(y)>()` is
  `true`, and
- `possibly-addable<decltype(x), decltype(y), decltype(z)>()` is `true`
  for those overloads that take a `z` parameter.

*Preconditions:*

- `multipliable(A,x,y)` is `true`, and
- `addable(x,y,z)` is `true` for those overloads that take a `z`
  parameter.

*Complexity:* \bigoh{\texttt{x.extent(0)} \times \texttt{A.extent(1)}}.

``` cpp
template<in-matrix InMat, in-vector InVec, out-vector OutVec>
  void matrix_vector_product(InMat A, InVec x, OutVec y);
template<class ExecutionPolicy, in-matrix InMat, in-vector InVec, out-vector OutVec>
  void matrix_vector_product(ExecutionPolicy&& exec, InMat A, InVec x, OutVec y);
```

These functions perform an overwriting matrix-vector product.

*Effects:* Computes y = A x.

[*Example 1*:

``` cpp
constexpr size_t num_rows = 5;
constexpr size_t num_cols = 6;

// y = 3.0 * A * x
void scaled_matvec_1(mdspan<double, extents<size_t, num_rows, num_cols>> A,
  mdspan<double, extents<size_t, num_cols>> x, mdspan<double, extents<size_t, num_rows>> y) {
  matrix_vector_product(scaled(3.0, A), x, y);
}

// z = 7.0 times the transpose of A, times y
void scaled_transposed_matvec(mdspan<double, extents<size_t, num_rows, num_cols>> A,
  mdspan<double, extents<size_t, num_rows>> y, mdspan<double, extents<size_t, num_cols>> z) {
  matrix_vector_product(scaled(7.0, transposed(A)), y, z);
}
```

— *end example*]

``` cpp
template<in-matrix InMat, in-vector InVec1, in-vector InVec2, out-vector OutVec>
    void matrix_vector_product(InMat A, InVec1 x, InVec2 y, OutVec z);
  template<class ExecutionPolicy,
           in-matrix InMat, in-vector InVec1, in-vector InVec2, out-vector OutVec>
    void matrix_vector_product(ExecutionPolicy&& exec,
                               InMat A, InVec1 x, InVec2 y, OutVec z);
```

These functions perform an updating matrix-vector product.

*Effects:* Computes z = y + A x.

*Remarks:* `z` may alias `y`.

[*Example 2*:

``` cpp
// y = 3.0 * A * x + 2.0 * y
void scaled_matvec_2(mdspan<double, extents<size_t, num_rows, num_cols>> A,
  mdspan<double, extents<size_t, num_cols>> x, mdspan<double, extents<size_t, num_rows>> y) {
  matrix_vector_product(scaled(3.0, A), x, scaled(2.0, y), y);
}
```

— *end example*]

#### Symmetric matrix-vector product <a id="linalg.algs.blas2.symv">[[linalg.algs.blas2.symv]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xSYMV` and
`xSPMV`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.symv]].

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
- `possibly-multipliable<decltype(A), decltype(x), decltype(y)>()` is
  `true`; and
- `possibly-addable<decltype(x), decltype(y), decltype(z)>()` is `true`
  for those overloads that take a `z` parameter.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`,
- `multipliable(A,x,y)` is `true`, and
- `addable(x,y,z)` is `true` for those overloads that take a `z`
  parameter.

*Complexity:* \bigoh{\texttt{x.extent(0)} \times \texttt{A.extent(1)}}.

``` cpp
template<in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
  void symmetric_matrix_vector_product(InMat A, Triangle t, InVec x, OutVec y);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
  void symmetric_matrix_vector_product(ExecutionPolicy&& exec,
                                       InMat A, Triangle t, InVec x, OutVec y);
```

These functions perform an overwriting symmetric matrix-vector product,
taking into account the `Triangle` parameter that applies to the
symmetric matrix `A`[[linalg.general]].

*Effects:* Computes y = A x.

``` cpp
template<in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2, out-vector OutVec>
  void symmetric_matrix_vector_product(InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2, out-vector OutVec>
  void symmetric_matrix_vector_product(ExecutionPolicy&& exec,
                                       InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);
```

These functions perform an updating symmetric matrix-vector product,
taking into account the `Triangle` parameter that applies to the
symmetric matrix `A`[[linalg.general]].

*Effects:* Computes z = y + A x.

*Remarks:* `z` may alias `y`.

#### Hermitian matrix-vector product <a id="linalg.algs.blas2.hemv">[[linalg.algs.blas2.hemv]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xHEMV` and
`xHPMV`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.hemv]].

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
- `possibly-multipliable<decltype(A), decltype(x), decltype(y)>()` is
  `true`; and
- `possibly-addable<decltype(x), decltype(y), decltype(z)>()` is `true`
  for those overloads that take a `z` parameter.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`,
- `multipliable(A, x, y)` is `true`, and
- `addable(x, y, z)` is `true` for those overloads that take a `z`
  parameter.

*Complexity:* \bigoh{\texttt{x.extent(0)} \times \texttt{A.extent(1)}}.

``` cpp
template<in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
  void hermitian_matrix_vector_product(InMat A, Triangle t, InVec x, OutVec y);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, in-vector InVec, out-vector OutVec>
  void hermitian_matrix_vector_product(ExecutionPolicy&& exec,
                                       InMat A, Triangle t, InVec x, OutVec y);
```

These functions perform an overwriting Hermitian matrix-vector product,
taking into account the `Triangle` parameter that applies to the
Hermitian matrix `A`[[linalg.general]].

*Effects:* Computes y = A x.

``` cpp
template<in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2, out-vector OutVec>
  void hermitian_matrix_vector_product(InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, in-vector InVec1, in-vector InVec2, out-vector OutVec>
  void hermitian_matrix_vector_product(ExecutionPolicy&& exec,
                                       InMat A, Triangle t, InVec1 x, InVec2 y, OutVec z);
```

These functions perform an updating Hermitian matrix-vector product,
taking into account the `Triangle` parameter that applies to the
Hermitian matrix `A`[[linalg.general]].

*Effects:* Computes z = y + A x.

*Remarks:* `z` may alias `y`.

#### Triangular matrix-vector product <a id="linalg.algs.blas2.trmv">[[linalg.algs.blas2.trmv]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xTRMV` and
`xTPMV`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.trmv]].

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
- `compatible-static-extents<decltype(A), decltype(y)>(0, 0)` is `true`;
- `compatible-static-extents<decltype(A), decltype(x)>(0, 0)` is `true`
  for those overloads that take an `x` parameter; and
- `compatible-static-extents<decltype(A), decltype(z)>(0, 0)` is `true`
  for those overloads that take a `z` parameter.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`,
- `A.extent(0)` equals `y.extent(0)`,
- `A.extent(0)` equals `x.extent(0)` for those overloads that take an
  `x` parameter, and
- `A.extent(0)` equals `z.extent(0)` for those overloads that take a `z`
  parameter.

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, in-vector InVec,
         out-vector OutVec>
  void triangular_matrix_vector_product(InMat A, Triangle t, DiagonalStorage d, InVec x, OutVec y);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, class DiagonalStorage, in-vector InVec,
         out-vector OutVec>
  void triangular_matrix_vector_product(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d, InVec x, OutVec y);
```

These functions perform an overwriting triangular matrix-vector product,
taking into account the `Triangle` and `DiagonalStorage` parameters that
apply to the triangular matrix `A`[[linalg.general]].

*Effects:* Computes y = A x.

*Complexity:* 𝑂(`x.extent(0)` `A.extent(1)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
  void triangular_matrix_vector_product(InMat A, Triangle t, DiagonalStorage d, InOutVec y);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
  void triangular_matrix_vector_product(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d, InOutVec y);
```

These functions perform an in-place triangular matrix-vector product,
taking into account the `Triangle` and `DiagonalStorage` parameters that
apply to the triangular matrix `A`[[linalg.general]].

[*Note 1*: Performing this operation in place hinders parallelization.
However, other `ExecutionPolicy` specific optimizations, such as
vectorization, are still possible. — *end note*]

*Effects:* Computes a vector y' such that y' = A y, and assigns each
element of y' to the corresponding element of y.

*Complexity:* 𝑂(`y.extent(0)` `A.extent(1)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage,
         in-vector InVec1, in-vector InVec2, out-vector OutVec>
  void triangular_matrix_vector_product(InMat A, Triangle t, DiagonalStorage d,
                                        InVec1 x, InVec2 y, OutVec z);
template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
         in-vector InVec1, in-vector InVec2, out-vector OutVec>
  void triangular_matrix_vector_product(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d,
                                        InVec1 x, InVec2 y, OutVec z);
```

These functions perform an updating triangular matrix-vector product,
taking into account the `Triangle` and `DiagonalStorage` parameters that
apply to the triangular matrix `A`[[linalg.general]].

*Effects:* Computes z = y + A x.

*Complexity:* 𝑂(`x.extent(0)` `A.extent(1)`).

*Remarks:* `z` may alias `y`.

#### Solve a triangular linear system <a id="linalg.algs.blas2.trsv">[[linalg.algs.blas2.trsv]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xTRSV` and
`xTPSV`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.trsv]].

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
- `compatible-static-extents<decltype(A), decltype(b)>(0, 0)` is `true`;
  and
- `compatible-static-extents<decltype(A), decltype(x)>(0, 0)` is `true`
  for those overloads that take an `x` parameter.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`,
- `A.extent(0)` equals `b.extent(0)`, and
- `A.extent(0)` equals `x.extent(0)` for those overloads that take an
  `x` parameter.

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec, out-vector OutVec, class BinaryDivideOp>
    void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d,
                                        InVec b, OutVec x, BinaryDivideOp divide);
  template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
           in-vector InVec, out-vector OutVec, class BinaryDivideOp>
    void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                        InMat A, Triangle t, DiagonalStorage d,
                                        InVec b, OutVec x, BinaryDivideOp divide);
```

These functions perform a triangular solve, taking into account the
`Triangle` and `DiagonalStorage` parameters that apply to the triangular
matrix `A`[[linalg.general]].

*Effects:* Computes a vector x' such that b = A x', and assigns each
element of x' to the corresponding element of x. If no such x' exists,
then the elements of `x` are valid but unspecified.

*Complexity:* 𝑂(`A.extent(1)` `b.extent(0)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage,
         in-vector InVec, out-vector OutVec>
  void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d, InVec b, OutVec x);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_vector_solve(A, t, d, b, x, divides<void>{});
```

``` cpp
template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
         in-vector InVec, out-vector OutVec>
  void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                      InMat A, Triangle t, DiagonalStorage d, InVec b, OutVec x);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_vector_solve(std::forward<ExecutionPolicy>(exec),
                               A, t, d, b, x, divides<void>{});
```

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage,
         inout-vector InOutVec, class BinaryDivideOp>
  void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d,
                                      InOutVec b, BinaryDivideOp divide);
template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
         inout-vector InOutVec, class BinaryDivideOp>
  void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                      InMat A, Triangle t, DiagonalStorage d,
                                      InOutVec b, BinaryDivideOp divide);
```

These functions perform an in-place triangular solve, taking into
account the `Triangle` and `DiagonalStorage` parameters that apply to
the triangular matrix `A`[[linalg.general]].

[*Note 1*: Performing triangular solve in place hinders
parallelization. However, other `ExecutionPolicy` specific
optimizations, such as vectorization, are still possible. — *end note*]

*Effects:* Computes a vector x' such that b = A x', and assigns each
element of x' to the corresponding element of b. If no such x' exists,
then the elements of `b` are valid but unspecified.

*Complexity:* 𝑂(`A.extent(1)` `b.extent(0)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
  void triangular_matrix_vector_solve(InMat A, Triangle t, DiagonalStorage d, InOutVec b);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_vector_solve(A, t, d, b, divides<void>{});
```

``` cpp
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, class DiagonalStorage, inout-vector InOutVec>
  void triangular_matrix_vector_solve(ExecutionPolicy&& exec,
                                      InMat A, Triangle t, DiagonalStorage d, InOutVec b);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_vector_solve(std::forward<ExecutionPolicy>(exec),
                               A, t, d, b, divides<void>{});
```

#### Rank-1 (outer product) update of a matrix <a id="linalg.algs.blas2.rank1">[[linalg.algs.blas2.rank1]]</a>

``` cpp
template<in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
  void matrix_rank_1_update(InVec1 x, InVec2 y, InOutMat A);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
  void matrix_rank_1_update(ExecutionPolicy&& exec, InVec1 x, InVec2 y, InOutMat A);
```

These functions perform a nonsymmetric nonconjugated rank-1 update.

[*Note 1*: These functions correspond to the BLAS functions `xGER` (for
real element types) and `xGERU` (for complex element
types). — *end note*]

*Mandates:* *`possibly-multipliable`*`<InOutMat, InVec2, InVec1>()` is
`true`.

*Preconditions:* *`multipliable`*`(A, y, x)` is `true`.

*Effects:* Computes a matrix A' such that $A' = A + x y^T$, and assigns
each element of A' to the corresponding element of A.

*Complexity:* 𝑂(`x.extent(0)` `y.extent(0)`).

``` cpp
template<in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
  void matrix_rank_1_update_c(InVec1 x, InVec2 y, InOutMat A);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2, inout-matrix InOutMat>
  void matrix_rank_1_update_c(ExecutionPolicy&& exec, InVec1 x, InVec2 y, InOutMat A);
```

These functions perform a nonsymmetric conjugated rank-1 update.

[*Note 2*: These functions correspond to the BLAS functions `xGER` (for
real element types) and `xGERC` (for complex element
types). — *end note*]

*Effects:*

- For the overloads without an `ExecutionPolicy` argument, equivalent
  to:
  ``` cpp
  matrix_rank_1_update(x, conjugated(y), A);
  ```
- otherwise, equivalent to:
  ``` cpp
  matrix_rank_1_update(std::forward<ExecutionPolicy>(exec), x, conjugated(y), A);
  ```

#### Symmetric or Hermitian Rank-1 (outer product) update of a matrix <a id="linalg.algs.blas2.symherrank1">[[linalg.algs.blas2.symherrank1]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xSYR`,
`xSPR`, `xHER`, and `xHPR`. They have overloads taking a scaling factor
`alpha`, because it would be impossible to express the update
$A = A - x x^T$ otherwise. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.symherrank1]].

*Mandates:*

- If `InOutMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
  and
- `compatible-static-extents<decltype(A), decltype(x)>(0, 0)` is `true`.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`, and
- `A.extent(0)` equals `x.extent(0)`.

*Complexity:* \bigoh{\texttt{x.extent(0)} \times \texttt{x.extent(0)}}.

``` cpp
template<class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_1_update(Scalar alpha, InVec x, InOutMat A, Triangle t);
template<class ExecutionPolicy,
         class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_1_update(ExecutionPolicy&& exec,
                                      Scalar alpha, InVec x, InOutMat A, Triangle t);
```

These functions perform a symmetric rank-1 update of the symmetric
matrix `A`, taking into account the `Triangle` parameter that applies to
`A`[[linalg.general]].

*Effects:* Computes a matrix A' such that $A' = A + \alpha x x^T$, where
the scalar α is `alpha`, and assigns each element of A' to the
corresponding element of A.

``` cpp
template<in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_1_update(InVec x, InOutMat A, Triangle t);
template<class ExecutionPolicy,
         in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_1_update(ExecutionPolicy&& exec, InVec x, InOutMat A, Triangle t);
```

These functions perform a symmetric rank-1 update of the symmetric
matrix `A`, taking into account the `Triangle` parameter that applies to
`A`[[linalg.general]].

*Effects:* Computes a matrix A' such that $A' = A + x x^T$ and assigns
each element of A' to the corresponding element of A.

``` cpp
template<class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_1_update(Scalar alpha, InVec x, InOutMat A, Triangle t);
template<class ExecutionPolicy,
         class Scalar, in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_1_update(ExecutionPolicy&& exec,
                                      Scalar alpha, InVec x, InOutMat A, Triangle t);
```

These functions perform a Hermitian rank-1 update of the Hermitian
matrix `A`, taking into account the `Triangle` parameter that applies to
`A`[[linalg.general]].

*Effects:* Computes A' such that $A' = A + \alpha x x^H$, where the
scalar α is `alpha`, and assigns each element of A' to the corresponding
element of A.

``` cpp
template<in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_1_update(InVec x, InOutMat A, Triangle t);
template<class ExecutionPolicy,
         in-vector InVec, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_1_update(ExecutionPolicy&& exec, InVec x, InOutMat A, Triangle t);
```

These functions perform a Hermitian rank-1 update of the Hermitian
matrix `A`, taking into account the `Triangle` parameter that applies to
`A`[[linalg.general]].

*Effects:* Computes a matrix A' such that $A' = A + x x^H$ and assigns
each element of A' to the corresponding element of A.

#### Symmetric and Hermitian rank-2 matrix updates <a id="linalg.algs.blas2.rank2">[[linalg.algs.blas2.rank2]]</a>

[*Note 1*: These functions correspond to the BLAS functions
`xSYR2`,`xSPR2`, `xHER2` and `xHPR2`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas2.rank2]].

*Mandates:*

- If `InOutMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
  and
- `possibly-multipliable<decltype(A), decltype(x), decltype(y)>()` is
  `true`.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`, and
- `multipliable(A, x, y)` is `true`.

*Complexity:* \bigoh{\texttt{x.extent(0)} \times \texttt{y.extent(0)}}.

``` cpp
template<in-vector InVec1, in-vector InVec2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_2_update(InVec1 x, InVec2 y, InOutMat A, Triangle t);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_2_update(ExecutionPolicy&& exec,
                                      InVec1 x, InVec2 y, InOutMat A, Triangle t);
```

These functions perform a symmetric rank-2 update of the symmetric
matrix `A`, taking into account the `Triangle` parameter that applies to
`A`[[linalg.general]].

*Effects:* Computes A' such that $A' = A + x y^T + y x^T$ and assigns
each element of A' to the corresponding element of A.

``` cpp
template<in-vector InVec1, in-vector InVec2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_2_update(InVec1 x, InVec2 y, InOutMat A, Triangle t);
template<class ExecutionPolicy, in-vector InVec1, in-vector InVec2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_2_update(ExecutionPolicy&& exec,
                                      InVec1 x, InVec2 y, InOutMat A, Triangle t);
```

These functions perform a Hermitian rank-2 update of the Hermitian
matrix `A`, taking into account the `Triangle` parameter that applies to
`A`[[linalg.general]].

*Effects:* Computes A' such that $A' = A + x y^H + y x^H$ and assigns
each element of A' to the corresponding element of A.

### BLAS 3 algorithms <a id="linalg.algs.blas3">[[linalg.algs.blas3]]</a>

#### General matrix-matrix product <a id="linalg.algs.blas3.gemm">[[linalg.algs.blas3.gemm]]</a>

[*Note 1*: These functions correspond to the BLAS function
`xGEMM`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas3.gemm]] in addition to function-specific elements.

*Mandates:*
`possibly-multipliable<decltype(A), decltype(B), decltype(C)>()` is
`true`.

*Preconditions:* `multipliable(A, B, C)` is `true`.

*Complexity:*
\bigoh{\texttt{A.extent(0)} \times \texttt{A.extent(1)} \times \texttt{B.extent(1)}}.

``` cpp
template<in-matrix InMat1, in-matrix InMat2, out-matrix OutMat>
    void matrix_product(InMat1 A, InMat2 B, OutMat C);
  template<class ExecutionPolicy, in-matrix InMat1, in-matrix InMat2, out-matrix OutMat>
    void matrix_product(ExecutionPolicy&& exec, InMat1 A, InMat2 B, OutMat C);
```

*Effects:* Computes C = A B.

``` cpp
template<in-matrix InMat1, in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
  void matrix_product(InMat1 A, InMat2 B, InMat3 E, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
  void matrix_product(ExecutionPolicy&& exec, InMat1 A, InMat2 B, InMat3 E, OutMat C);
```

*Mandates:* *`possibly-addable`*`<InMat3, InMat3, OutMat>()` is `true`.

*Preconditions:* *`addable`*`(E, E, C)` is `true`.

*Effects:* Computes C = E + A B.

*Remarks:* `C` may alias `E`.

#### Symmetric, Hermitian, and triangular matrix-matrix product <a id="linalg.algs.blas3.xxmm">[[linalg.algs.blas3.xxmm]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xSYMM`,
`xHEMM`, and `xTRMM`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas3.xxmm]] in addition to function-specific elements.

*Mandates:*

- `possibly-multipliable<decltype(A), decltype(B), decltype(C)>()` is
  `true`, and
- `possibly-addable<decltype(E), decltype(E), decltype(C)>()` is `true`
  for those overloads that take an `E` parameter.

*Preconditions:*

- `multipliable(A, B, C)` is `true`, and
- `addable(E, E, C)` is `true` for those overloads that take an `E`
  parameter.

*Complexity:*
\bigoh{\texttt{A.extent(0)} \times \texttt{A.extent(1)} \times \texttt{B.extent(1)}}.

``` cpp
template<in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
  void symmetric_matrix_product(InMat1 A, Triangle t, InMat2 B, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
  void symmetric_matrix_product(ExecutionPolicy&& exec, InMat1 A, Triangle t, InMat2 B, OutMat C);

template<in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
  void hermitian_matrix_product(InMat1 A, Triangle t, InMat2 B, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, in-matrix InMat2, out-matrix OutMat>
  void hermitian_matrix_product(ExecutionPolicy&& exec, InMat1 A, Triangle t, InMat2 B, OutMat C);

template<in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat>
  void triangular_matrix_product(InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, OutMat C);
template<class ExecutionPolicy, in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat>
  void triangular_matrix_product(ExecutionPolicy&& exec,
                                 InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, OutMat C);
```

These functions perform a matrix-matrix multiply, taking into account
the `Triangle` and `DiagonalStorage` (if applicable) parameters that
apply to the symmetric, Hermitian, or triangular (respectively) matrix
`A`[[linalg.general]].

*Mandates:*

- If `InMat1` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument; and
- *`compatible-static-extents`*`<InMat1, InMat1>(0, 1)` is `true`.

*Preconditions:* `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes C = A B.

``` cpp
template<in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void symmetric_matrix_product(InMat1 A, InMat2 B, Triangle t, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void symmetric_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, InMat2 B, Triangle t, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void hermitian_matrix_product(InMat1 A, InMat2 B, Triangle t, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, out-matrix OutMat>
    void hermitian_matrix_product(ExecutionPolicy&& exec,
                                  InMat1 A, InMat2 B, Triangle t, OutMat C);

  template<in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
           out-matrix OutMat>
    void triangular_matrix_product(InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, OutMat C);
  template<class ExecutionPolicy,
           in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
           out-matrix OutMat>
    void triangular_matrix_product(ExecutionPolicy&& exec,
                                   InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, OutMat C);
```

These functions perform a matrix-matrix multiply, taking into account
the `Triangle` and `DiagonalStorage` (if applicable) parameters that
apply to the symmetric, Hermitian, or triangular (respectively) matrix
`B`[[linalg.general]].

*Mandates:*

- If `InMat2` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument; and
- *`compatible-static-extents`*`<InMat2, InMat2>(0, 1)` is `true`.

*Preconditions:* `B.extent(0) == B.extent(1)` is `true`.

*Effects:* Computes C = A B.

``` cpp
template<in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
         out-matrix OutMat>
  void symmetric_matrix_product(InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
         out-matrix OutMat>
  void symmetric_matrix_product(ExecutionPolicy&& exec,
                                InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);

template<in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
         out-matrix OutMat>
  void hermitian_matrix_product(InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, in-matrix InMat2, in-matrix InMat3,
         out-matrix OutMat>
  void hermitian_matrix_product(ExecutionPolicy&& exec,
                                InMat1 A, Triangle t, InMat2 B, InMat3 E, OutMat C);

template<in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
  void triangular_matrix_product(InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, InMat3 E,
                                 OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, in-matrix InMat3, out-matrix OutMat>
  void triangular_matrix_product(ExecutionPolicy&& exec,
                                 InMat1 A, Triangle t, DiagonalStorage d, InMat2 B, InMat3 E,
                                 OutMat C);
```

These functions perform a potentially overwriting matrix-matrix
multiply-add, taking into account the `Triangle` and `DiagonalStorage`
(if applicable) parameters that apply to the symmetric, Hermitian, or
triangular (respectively) matrix `A`[[linalg.general]].

*Mandates:*

- If `InMat1` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument; and
- *`compatible-static-extents`*`<InMat1, InMat1>(0, 1)` is `true`.

*Preconditions:* `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes C = E + A B.

*Remarks:* `C` may alias `E`.

``` cpp
template<in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
         out-matrix OutMat>
  void symmetric_matrix_product(InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
         out-matrix OutMat>
  void symmetric_matrix_product(ExecutionPolicy&& exec,
                                InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);

template<in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
         out-matrix OutMat>
  void hermitian_matrix_product(InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, in-matrix InMat2, class Triangle, in-matrix InMat3,
         out-matrix OutMat>
  void hermitian_matrix_product(ExecutionPolicy&& exec,
                                InMat1 A, InMat2 B, Triangle t, InMat3 E, OutMat C);

template<in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
         in-matrix InMat3, out-matrix OutMat>
  void triangular_matrix_product(InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, InMat3 E,
                                 OutMat C);
template<class ExecutionPolicy,
         in-matrix InMat1, in-matrix InMat2, class Triangle, class DiagonalStorage,
         in-matrix InMat3, out-matrix OutMat>
  void triangular_matrix_product(ExecutionPolicy&& exec,
                                 InMat1 A, InMat2 B, Triangle t, DiagonalStorage d, InMat3 E,
                                 OutMat C);
```

These functions perform a potentially overwriting matrix-matrix
multiply-add, taking into account the `Triangle` and `DiagonalStorage`
(if applicable) parameters that apply to the symmetric, Hermitian, or
triangular (respectively) matrix `B`[[linalg.general]].

*Mandates:*

- If `InMat2` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument; and
- *`compatible-static-extents`*`<InMat2, InMat2>(0, 1)` is `true`.

*Preconditions:* `B.extent(0) == B.extent(1)` is `true`.

*Effects:* Computes C = E + A B.

*Remarks:* `C` may alias `E`.

#### In-place triangular matrix-matrix product <a id="linalg.algs.blas3.trmm">[[linalg.algs.blas3.trmm]]</a>

These functions perform an in-place matrix-matrix multiply, taking into
account the `Triangle` and `DiagonalStorage` parameters that apply to
the triangular matrix `A` [[linalg.general]].

[*Note 1*: These functions correspond to the BLAS function
`xTRMM`. — *end note*]

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_left_product(InMat A, Triangle t, DiagonalStorage d, InOutMat C);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_left_product(ExecutionPolicy&& exec,
                                      InMat A, Triangle t, DiagonalStorage d, InOutMat C);
```

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- *`possibly-multipliable`*`<InMat, InOutMat, InOutMat>()` is `true`;
  and
- *`compatible-static-extents`*`<InMat, InMat>(0, 1)` is `true`.

*Preconditions:*

- *`multipliable`*`(A, C, C)` is `true`, and
- `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes a matrix C' such that C' = A C and assigns each
element of C' to the corresponding element of C.

*Complexity:* 𝑂(`A.extent(0)` `A.extent(1)` `C.extent(0)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_right_product(InMat A, Triangle t, DiagonalStorage d, InOutMat C);
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_right_product(ExecutionPolicy&& exec,
                                       InMat A, Triangle t, DiagonalStorage d, InOutMat C);
```

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- *`possibly-multipliable`*`<InOutMat, InMat, InOutMat>()` is `true`;
  and
- *`compatible-static-extents`*`<InMat, InMat>(0, 1)` is `true`.

*Preconditions:*

- *`multipliable`*`(C, A, C)` is `true`, and
- `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes a matrix C' such that C' = C A and assigns each
element of C' to the corresponding element of C.

*Complexity:* 𝑂(`A.extent(0)` `A.extent(1)` `C.extent(0)`).

#### Rank-k update of a symmetric or Hermitian matrix <a id="linalg.algs.blas3.rankk">[[linalg.algs.blas3.rankk]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xSYRK` and
`xHERK`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas3.rankk]].

*Mandates:*

- If `InOutMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`;
- `compatible-static-extents<decltype(C), decltype(C)>(0, 1)` is `true`;
  and
- `compatible-static-extents<decltype(A), decltype(C)>(0, 0)` is `true`.

*Preconditions:*

- `A.extent(0)` equals `A.extent(1)`,
- `C.extent(0)` equals `C.extent(1)`, and
- `A.extent(0)` equals `C.extent(0)`.

*Complexity:*
\bigoh{\texttt{A.extent(0)} \times \texttt{A.extent(1)} \times \texttt{C.extent(0)}}.

``` cpp
template<class Scalar, in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_k_update(Scalar alpha, InMat A, InOutMat C, Triangle t);
  template<class ExecutionPolicy, class Scalar,
           in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
    void symmetric_matrix_rank_k_update(ExecutionPolicy&& exec,
                                        Scalar alpha, InMat A, InOutMat C, Triangle t);
```

*Effects:* Computes a matrix C' such that $C' = C + \alpha A A^T$, where
the scalar α is `alpha`, and assigns each element of C' to the
corresponding element of C.

``` cpp
template<in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_k_update(InMat A, InOutMat C, Triangle t);
template<class ExecutionPolicy,
         in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_k_update(ExecutionPolicy&& exec,
                                      InMat A, InOutMat C, Triangle t);
```

*Effects:* Computes a matrix C' such that $C' = C + A A^T$, and assigns
each element of C' to the corresponding element of C.

``` cpp
template<class Scalar, in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_k_update(Scalar alpha, InMat A, InOutMat C, Triangle t);
template<class ExecutionPolicy,
         class Scalar, in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_k_update(ExecutionPolicy&& exec,
                                      Scalar alpha, InMat A, InOutMat C, Triangle t);
```

*Effects:* Computes a matrix C' such that $C' = C + \alpha A A^H$, where
the scalar α is `alpha`, and assigns each element of C' to the
corresponding element of C.

``` cpp
template<in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_k_update(InMat A, InOutMat C, Triangle t);
template<class ExecutionPolicy,
         in-matrix InMat, possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_k_update(ExecutionPolicy&& exec,
                                      InMat A, InOutMat C, Triangle t);
```

*Effects:* Computes a matrix C' such that $C' = C + A A^H$, and assigns
each element of C' to the corresponding element of C.

#### Rank-2k update of a symmetric or Hermitian matrix <a id="linalg.algs.blas3.rank2k">[[linalg.algs.blas3.rank2k]]</a>

[*Note 1*: These functions correspond to the BLAS functions `xSYR2K`
and `xHER2K`. — *end note*]

The following elements apply to all functions in
[[linalg.algs.blas3.rank2k]].

*Mandates:*

- If `InOutMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- `possibly-addable<decltype(A), decltype(B), decltype(C)>()` is `true`;
  and
- `compatible-static-extents<decltype(A), decltype(A)>(0, 1)` is `true`.

*Preconditions:*

- `addable(A, B, C)` is `true`, and
- `A.extent(0)` equals `A.extent(1)`.

*Complexity:*
\bigoh{\texttt{A.extent(0)} \times \texttt{A.extent(1)} \times \texttt{C.extent(0)}}.

``` cpp
template<in-matrix InMat1, in-matrix InMat2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_2k_update(InMat1 A, InMat2 B, InOutMat C, Triangle t);
template<class ExecutionPolicy, in-matrix InMat1, in-matrix InMat2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void symmetric_matrix_rank_2k_update(ExecutionPolicy&& exec,
                                       InMat1 A, InMat2 B, InOutMat C, Triangle t);
```

*Effects:* Computes a matrix C' such that $C' = C + A B^T + B A^T$, and
assigns each element of C' to the corresponding element of C.

``` cpp
template<in-matrix InMat1, in-matrix InMat2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_2k_update(InMat1 A, InMat2 B, InOutMat C, Triangle t);
template<class ExecutionPolicy,
         in-matrix InMat1, in-matrix InMat2,
         possibly-packed-inout-matrix InOutMat, class Triangle>
  void hermitian_matrix_rank_2k_update(ExecutionPolicy&& exec,
                                       InMat1 A, InMat2 B, InOutMat C, Triangle t);
```

*Effects:* Computes a matrix C' such that $C' = C + A B^H + B A^H$, and
assigns each element of C' to the corresponding element of C.

#### Solve multiple triangular linear systems <a id="linalg.algs.blas3.trsm">[[linalg.algs.blas3.trsm]]</a>

[*Note 1*: These functions correspond to the BLAS function
`xTRSM`. — *end note*]

``` cpp
template<in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_left_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                           InMat2 B, OutMat X, BinaryDivideOp divide);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                           InMat1 A, Triangle t, DiagonalStorage d,
                                           InMat2 B, OutMat X, BinaryDivideOp divide);
```

These functions perform multiple matrix solves, taking into account the
`Triangle` and `DiagonalStorage` parameters that apply to the triangular
matrix `A`[[linalg.general]].

*Mandates:*

- If `InMat1` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- *`possibly-multipliable`*`<InMat1, OutMat, InMat2>()` is `true`; and
- *`compatible-static-extents`*`<InMat1, InMat1>(0, 1)` is `true`.

*Preconditions:*

- *`multipliable`*`(A, X, B)` is `true`, and
- `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes X' such that AX' = B, and assigns each element of X'
to the corresponding element of X. If no such X' exists, then the
elements of `X` are valid but unspecified.

*Complexity:* 𝑂(`A.extent(0)` `X.extent(1)` `X.extent(1)`).

[*Note 2*: Since the triangular matrix is on the left, the desired
`divide` implementation in the case of noncommutative multiplication is
mathematically equivalent to $y^{-1} x$, where x is the first argument
and y is the second argument, and $y^{-1}$ denotes the multiplicative
inverse of y. — *end note*]

``` cpp
template<in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat>
  void triangular_matrix_matrix_left_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                           InMat2 B, OutMat X);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_left_solve(A, t, d, B, X, divides<void>{});
```

``` cpp
template<class ExecutionPolicy, in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat>
  void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                           InMat1 A, Triangle t, DiagonalStorage d,
                                           InMat2 B, OutMat X);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_left_solve(std::forward<ExecutionPolicy>(exec),
                                    A, t, d, B, X, divides<void>{});
```

``` cpp
template<in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_right_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                            InMat2 B, OutMat X, BinaryDivideOp divide);
template<class ExecutionPolicy,
         in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                            InMat1 A, Triangle t, DiagonalStorage d,
                                            InMat2 B, OutMat X, BinaryDivideOp divide);
```

These functions perform multiple matrix solves, taking into account the
`Triangle` and `DiagonalStorage` parameters that apply to the triangular
matrix `A`[[linalg.general]].

*Mandates:*

- If `InMat1` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- *`possibly-multipliable`*`<OutMat, InMat1, InMat2>()` is `true`; and
- *`compatible-static-extents`*`<InMat1, InMat1>(0,1)` is `true`.

*Preconditions:*

- *`multipliable`*`(X, A, B)` is `true`, and
- `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes X' such that X'A = B, and assigns each element of X'
to the corresponding element of X. If no such X' exists, then the
elements of `X` are valid but unspecified.

*Complexity:* O( `B.extent(0)` ⋅ `B.extent(1)` ⋅ `A.extent(1)` )

[*Note 1*: Since the triangular matrix is on the right, the desired
`divide` implementation in the case of noncommutative multiplication is
mathematically equivalent to $x y^{-1}$, where x is the first argument
and y is the second argument, and $y^{-1}$ denotes the multiplicative
inverse of y. — *end note*]

``` cpp
template<in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat>
  void triangular_matrix_matrix_right_solve(InMat1 A, Triangle t, DiagonalStorage d,
                                            InMat2 B, OutMat X);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_right_solve(A, t, d, B, X, divides<void>{});
```

``` cpp
template<class ExecutionPolicy, in-matrix InMat1, class Triangle, class DiagonalStorage,
         in-matrix InMat2, out-matrix OutMat>
  void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                            InMat1 A, Triangle t, DiagonalStorage d,
                                            InMat2 B, OutMat X);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_right_solve(std::forward<ExecutionPolicy>(exec),
                                     A, t, d, B, X, divides<void>{});
```

#### Solve multiple triangular linear systems in-place <a id="linalg.algs.blas3.inplacetrsm">[[linalg.algs.blas3.inplacetrsm]]</a>

[*Note 1*: These functions correspond to the BLAS function
`xTRSM`. — *end note*]

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage,
         inout-matrix InOutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_left_solve(InMat A, Triangle t, DiagonalStorage d,
                                           InOutMat B, BinaryDivideOp divide);
template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
         inout-matrix InOutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                           InMat A, Triangle t, DiagonalStorage d,
                                           InOutMat B, BinaryDivideOp divide);
```

These functions perform multiple in-place matrix solves, taking into
account the `Triangle` and `DiagonalStorage` parameters that apply to
the triangular matrix `A`[[linalg.general]].

[*Note 1*: This algorithm makes it possible to compute factorizations
like Cholesky and LU in place. Performing triangular solve in place
hinders parallelization. However, other `ExecutionPolicy` specific
optimizations, such as vectorization, are still possible. — *end note*]

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- *`possibly-multipliable`*`<InMat, InOutMat, InOutMat>()` is `true`;
  and
- *`compatible-static-extents`*`<InMat, InMat>(0, 1)` is `true`.

*Preconditions:*

- *`multipliable`*`(A, B, B)` is `true`, and
- `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes X' such that AX' = B, and assigns each element of X'
to the corresponding element of B. If so such X' exists, then the
elements of `B` are valid but unspecified.

*Complexity:* 𝑂(`A.extent(0)` `A.extent(1)` `B.extent(1)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_matrix_left_solve(InMat A, Triangle t, DiagonalStorage d,
                                           InOutMat B);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_left_solve(A, t, d, B, divides<void>{});
```

``` cpp
template<class ExecutionPolicy,
           in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
    void triangular_matrix_matrix_left_solve(ExecutionPolicy&& exec,
                                             InMat A, Triangle t, DiagonalStorage d,
                                             InOutMat B);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_left_solve(std::forward<ExecutionPolicy>(exec),
                                    A, t, d, B, divides<void>{});
```

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage,
         inout-matrix InOutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_right_solve(InMat A, Triangle t, DiagonalStorage d,
                                            InOutMat B, BinaryDivideOp divide);
template<class ExecutionPolicy, in-matrix InMat, class Triangle, class DiagonalStorage,
         inout-matrix InOutMat, class BinaryDivideOp>
  void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                            InMat A, Triangle t, DiagonalStorage d,
                                            InOutMat B, BinaryDivideOp divide);
```

These functions perform multiple in-place matrix solves, taking into
account the `Triangle` and `DiagonalStorage` parameters that apply to
the triangular matrix `A`[[linalg.general]].

[*Note 2*: This algorithm makes it possible to compute factorizations
like Cholesky and LU in place. Performing triangular solve in place
hinders parallelization. However, other `ExecutionPolicy` specific
optimizations, such as vectorization, are still possible. — *end note*]

*Mandates:*

- If `InMat` has `layout_blas_packed` layout, then the layout’s
  `Triangle` template argument has the same type as the function’s
  `Triangle` template argument;
- *`possibly-multipliable`*`<InOutMat, InMat, InOutMat>()` is `true`;
  and
- *`compatible-static-extents`*`<InMat, InMat>(0, 1)` is `true`.

*Preconditions:*

- *`multipliable`*`(B, A, B)` is `true`, and
- `A.extent(0) == A.extent(1)` is `true`.

*Effects:* Computes X' such that X'A = B, and assigns each element of X'
to the corresponding element of B. If so such X' exists, then the
elements of `B` are valid but unspecified.

*Complexity:* 𝑂(`A.extent(0)` `A.extent(1)` `B.extent(1)`).

``` cpp
template<in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_matrix_right_solve(InMat A, Triangle t, DiagonalStorage d, InOutMat B);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_right_solve(A, t, d, B, divides<void>{});
```

``` cpp
template<class ExecutionPolicy,
         in-matrix InMat, class Triangle, class DiagonalStorage, inout-matrix InOutMat>
  void triangular_matrix_matrix_right_solve(ExecutionPolicy&& exec,
                                            InMat A, Triangle t, DiagonalStorage d,
                                            InOutMat B);
```

*Effects:* Equivalent to:

``` cpp
triangular_matrix_matrix_right_solve(std::forward<ExecutionPolicy>(exec),
                                     A, t, d, B, divides<void>{});
```

## Data-parallel types <a id="simd">[[simd]]</a>

### General <a id="simd.general">[[simd.general]]</a>

Subclause [[simd]] defines data-parallel types and operations on these
types.

[*Note 1*: The intent is to support acceleration through data-parallel
execution resources where available, such as SIMD registers and
instructions or execution units driven by a common instruction decoder.
SIMD stands for “Single Instruction Stream – Multiple Data Stream”; it
is defined in Flynn 1966. — *end note*]

The set of comprises

- all standard integer types, character types, and the types `float` and
  `double` [[basic.fundamental]];
- `std::float16_t`, `std::float32_t`, and `std::float64_t` if defined
  [[basic.extended.fp]]; and
- `complex<T>` where `T` is a vectorizable floating-point type.

The term *data-parallel type* refers to all enabled specializations of
the `basic_vec` and `basic_mask` class templates. A
*data-parallel object* is an object of data-parallel type.

Each specialization of `basic_vec` or `basic_mask` is either enabled or
disabled, as described in [[simd.overview]] and [[simd.mask.overview]].

A data-parallel type consists of one or more elements of an underlying
vectorizable type, called the *element type*. The number of elements is
a constant for each data-parallel type and called the *width* of that
type. The elements in a data-parallel type are indexed from 0 to
$\textrm{width} - 1$.

An *element-wise operation* applies a specified operation to the
elements of one or more data-parallel objects. Each such application is
unsequenced with respect to the others. A *unary element-wise operation*
is an element-wise operation that applies a unary operation to each
element of a data-parallel object. A *binary element-wise operation* is
an element-wise operation that applies a binary operation to
corresponding elements of two data-parallel objects.

Given a `basic_mask<Bytes, Abi>` object `mask`, the *selected indices*
signify the integers i in the range \[`0`, `mask.size()`) for which
`mask[i]` is `true`. Given a data-parallel object `data`, the
*selected elements* signify the elements `data[i]` for all selected
indices i.

The conversion from an arithmetic type `U` to a vectorizable type `T` is
*value-preserving* if all possible values of `U` can be represented with
type `T`.

### Exposition-only types, variables, and concepts <a id="simd.expos">[[simd.expos]]</a>

``` cpp
using simd-size-type = see belownc;                                    // exposition only
template<size_t Bytes> using integer-from = see belownc;               // exposition only

template<class T, class Abi>
  constexpr simd-size-type simd-size-v = see belownc;                  // exposition only
template<class T> constexpr size_t mask-element-size = see belownc;    // exposition only

template<class T>
  concept \defexposconceptnc{constexpr-wrapper-like} =                                   // exposition only
    convertible_to<T, decltype(T::value)> &&
    equality_comparable_with<T, decltype(T::value)> &&
    bool_constant<T() == T::value>::value &&
    bool_constant<static_cast<decltype(T::value)>(T()) == T::value>::value;

template<class T> using deduced-vec-t = see belownc;                   // exposition only

template<class V, class T> using make-compatible-simd-t = see belownc; // exposition only

template<class V>
  concept \defexposconceptnc{simd-vec-type} =                                            // exposition only
    same_as<V, basic_vec<typename V::value_type, typename V::abi_type>> &&
    is_default_constructible_v<V>;

template<class V>
  concept \defexposconceptnc{simd-mask-type} =                                           // exposition only
    same_as<V, basic_mask<mask-element-size<V>, typename V::abi_type>> &&
    is_default_constructible_v<V>;

template<class V>
  concept \defexposconceptnc{simd-floating-point} =                                      // exposition only
    simd-vec-type<V> && floating_point<typename V::value_type>;

template<class V>
  concept \defexposconceptnc{simd-integral} =                                            // exposition only
    simd-vec-type<V> && integral<typename V::value_type>;

template<class V>
  using simd-complex-value-type = V::value_type::value_type; // exposition only

template<class V>
  concept \defexposconceptnc{simd-complex} =                                             // exposition only
    simd-vec-type<V> && same_as<typename V::value_type, complex<simd-complex-value-type<V>>>;

template<class... Ts>
  concept \defexposconceptnc{math-floating-point} =                                      // exposition only
    (exposition onlyconceptnc{simd-floating-point}<deduced-vec-t<Ts>> || ...);

template<class... Ts>
  requires exposition onlyconceptnc{math-floating-point}<Ts...>
    using math-common-simd-t = see belownc;                            // exposition only

template<class BinaryOperation, class T>
  concept exposition onlyconceptnc{reduction-binary-operation} = see belownc;                    // exposition only

// [simd.expos.abi], simd ABI tags
template<class T> using native-abi = see belownc;                      // exposition only
template<class T, simd-size-type N> using deduce-abi-t = see belownc@;  // exposition only

// [simd.flags], load and store flags
struct convert-flag;                                                 // exposition only
struct aligned-flag;                                                 // exposition only
template<size_t N> struct overaligned-flag;                          // exposition only
```

#### Exposition-only helpers <a id="simd.expos.defn">[[simd.expos.defn]]</a>

``` cpp
using simd-size-type = see below;
```

*simd-size-type* is an alias for a signed integer type.

``` cpp
template<size_t Bytes> using integer-from = see below;
```

*`integer-from`*`<Bytes>` is an alias for a signed integer type `T` such
that `sizeof(T)` equals `Bytes`.

``` cpp
template<class T, class Abi>
  constexpr simd-size-type simd-size-v = see below;
```

*`simd-size-v`*`<T, Abi>` denotes the width of `basic_vec<T, Abi>` if
the specialization `basic_vec<T, Abi>` is enabled, or `0` otherwise.

``` cpp
template<class T> constexpr size_t mask-element-size = see below;
```

*`mask-element-size`*`<basic_mask<Bytes, Abi>>` has the value `Bytes`.

``` cpp
template<class T> using deduced-vec-t = see below;
```

Let `x` denote an lvalue of type `const T`.

*`deduced-vec-t`*`<T>` is an alias for

- `decltype(x + x)`, if the type of `x + x` is an enabled specialization
  of `basic_vec`; otherwise
- `void`.

``` cpp
template<class V, class T> using make-compatible-simd-t = see below;
```

Let `x` denote an lvalue of type `const T`.

*`make-compatible-simd-t`*`<V, T>` is an alias for

- *`deduced-vec-t`*`<T>`, if that type is not `void`, otherwise
- `vec<decltype(x + x), V::size()>`.

``` cpp
template<class... Ts>
  requires math-floating-point<Ts...>
    using math-common-simd-t = see below;
```

Let `T0` denote `Ts...[0]`. Let `T1` denote `Ts...[1]`. Let `TRest`
denote a pack such that `T0, T1, TRest...` is equivalent to `Ts...`.

Let *`math-common-simd-t`*`<Ts...>` be an alias for

- *`deduced-vec-t`*`<T0>`, if `sizeof...(Ts)` equals 1; otherwise
- `common_type_t<`*`deduced-vec-t`*`<T0>, `*`deduced-vec-t`*`<T1>>`, if
  `sizeof...(Ts)` equals 2 and
  `math-floating-point<T0> && math-floating-point<T1>` is `true`;
  otherwise
- `common_type_t<`*`deduced-vec-t`*`<T0>, T1>`, if `sizeof...(Ts)`
  equals 2 and `<T0>` is `true`; otherwise
- `common_type_t<T0, `*`deduced-vec-t`*`<T1>>`, if `sizeof...(Ts)`
  equals 2; otherwise
- `common_type_t<`*`math-common-simd-t`*`<T0, T1>, TRest...>`, if
  *`math-common-simd-t`*`<T0, T1>` is valid and denotes a type;
  otherwise
- `common_type_t<`*`math-common-simd-t`*`<TRest...>, T0, T1>`.

``` cpp
template<class BinaryOperation, class T>
  concept reduction-binary-operation =
    requires (const BinaryOperation binary_op, const vec<T, 1> v) {
      { binary_op(v, v) } -> same_as<vec<T, 1>>;
    };
```

Types `BinaryOperation` and `T` model
`reduction-binary-operation<BinaryOperation, T>` only if:

- `BinaryOperation` is a binary element-wise operation and the operation
  is commutative.
- An object of type `BinaryOperation` can be invoked with two arguments
  of type `basic_vec<T, Abi>`, with unspecified ABI tag `Abi`, returning
  a `basic_vec<T, Abi>`.

#### `simd` ABI tags <a id="simd.expos.abi">[[simd.expos.abi]]</a>

``` cpp
template<class T> using native-abi = see below;
template<class T, simd-size-type N> using deduce-abi-t = see below;
```

An *ABI tag* is a type that indicates a choice of size and binary
representation for objects of data-parallel type.

[*Note 1*: The intent is for the size and binary representation to
depend on the target architecture and compiler flags. The ABI tag,
together with a given element type, implies the width. — *end note*]

[*Note 2*: The ABI tag is orthogonal to selecting the machine
instruction set. The selected machine instruction set limits the usable
ABI tag types, though (see [[simd.overview]]). The ABI tags enable users
to safely pass objects of data-parallel type between translation unit
boundaries (e.g., function calls or I/O). — *end note*]

An implementation defines ABI tag types as necessary for the following
aliases.

*`deduce-abi-t`*`<T, N>` is defined if

- `T` is a vectorizable type,
- `N` is greater than zero, and
- `N` is not larger than an implementation-defined maximum.

The *implementation-defined* maximum for `N` is not smaller than 64 and
can differ depending on `T`.

Where present, *`deduce-abi-t`*`<T, N>` names an ABI tag type such that

- *`simd-size-v`*`<T, `*`deduce-abi-t`*`<T, N>>` equals `N`,
- `basic_vec<T, `*`deduce-abi-t`*`<T, N>>` is enabled [[simd.overview]],
  and
- `basic_mask<sizeof(T), `*`deduce-abi-t`*`<`*`integer-from`*`<sizeof(T)>, N>>`
  is enabled.

*`native-abi`*`<T>` is an *implementation-defined* alias for an ABI tag.
`basic_vec<T, `*`native-abi`*`<T>>` is an enabled specialization.

[*Note 3*: The intent is to use the ABI tag producing the most
efficient data-parallel execution for the element type `T` on the
currently targeted system. For target architectures with ISA extensions,
compiler flags can change the type of the *`native-abi`*`<T>`
alias. — *end note*]

[*Example 1*:

Consider a target architecture supporting the ABI tags `__simd128` and
`__simd256`, where hardware support for `__simd256` exists only for
floating-point types. The implementation therefore defines
*`native-abi`*`<T>` as an alias for

- `__simd256` if `T` is a floating-point type, and
- `__simd128` otherwise.

— *end example*]

### Header `<simd>` synopsis <a id="simd.syn">[[simd.syn]]</a>

``` cpp
namespace std::simd {
  // [simd.traits], type traits
  template<class T, class U = typename T::value_type> struct alignment;
  template<class T, class U = typename T::value_type>
    constexpr size_t alignment_v = alignment<T, U>::value;

  template<class T, class V> struct rebind { using type = see below; };
  template<class T, class V> using rebind_t = rebind<T, V>::type;
  template<simd-size-type N, class V> struct resize { using type = see below; };
  template<simd-size-type N, class V> using resize_t = resize<N, V>::type;

  // [simd.flags], load and store flags
  template<class... Flags> struct flags;
  inline constexpr flags<> flag_default{};
  inline constexpr flags<convert-flag> flag_convert{};
  inline constexpr flags<aligned-flag> flag_aligned{};
  template<size_t N> requires (has_single_bit(N))
    constexpr flags<overaligned-flag<N>> flag_overaligned{};

  // [simd.iterator], class template simd-iterator
  template<class V>
    class simd-iterator;                // exposition only

  // [simd.class], class template basic_vec
  template<class T, class Abi = native-abi<T>> class basic_vec;
  template<class T, simd-size-type N = simd-size-v<T, native-abi<T>>>
    using vec = basic_vec<T, deduce-abi-t<T, N>>;

  // [simd.reductions], reductions
  template<class T, class Abi, class BinaryOperation = plus<>>
    constexpr T reduce(const basic_vec<T, Abi>&, BinaryOperation = {});
  template<class T, class Abi, class BinaryOperation = plus<>>
    constexpr T reduce(
      const basic_vec<T, Abi>& x, const typename basic_vec<T, Abi>::mask_type& mask,
      BinaryOperation binary_op = {}, type_identity_t<T> identity_element = see below);

  template<class T, class Abi>
    constexpr T reduce_min(const basic_vec<T, Abi>&) noexcept;
  template<class T, class Abi>
    constexpr T reduce_min(const basic_vec<T, Abi>&,
                           const typename basic_vec<T, Abi>::mask_type&) noexcept;
  template<class T, class Abi>
    constexpr T reduce_max(const basic_vec<T, Abi>&) noexcept;
  template<class T, class Abi>
    constexpr T reduce_max(const basic_vec<T, Abi>&,
                           const typename basic_vec<T, Abi>::mask_type&) noexcept;

  // [simd.loadstore], load and store functions
  template<class V = see below, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R>
    constexpr V unchecked_load(R&& r, flags<Flags...> f = {});
  template<class V = see below, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R>
    constexpr V unchecked_load(R&& r, const typename V::mask_type& k,
                               flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, class... Flags>
    constexpr V unchecked_load(I first, iter_difference_t<I> n,
                               flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, class... Flags>
    constexpr V unchecked_load(I first, iter_difference_t<I> n,
                               const typename V::mask_type& k, flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    constexpr V unchecked_load(I first, S last, flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    constexpr V unchecked_load(I first, S last, const typename V::mask_type& k,
                               flags<Flags...> f = {});

  template<class V = see below, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R>
    constexpr V partial_load(R&& r, flags<Flags...> f = {});
  template<class V = see below, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R>
    constexpr V partial_load(R&& r, const typename V::mask_type& k,
                             flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, class... Flags>
    constexpr V partial_load(I first, iter_difference_t<I> n, flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, class... Flags>
    constexpr V partial_load(I first, iter_difference_t<I> n,
                             const typename V::mask_type& k, flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    constexpr V partial_load(I first, S last, flags<Flags...> f = {});
  template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    constexpr V partial_load(I first, S last, const typename V::mask_type& k,
                             flags<Flags...> f = {});

  template<class T, class Abi, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
    constexpr void unchecked_store(const basic_vec<T, Abi>& v, R&& r,
                                   flags<Flags...> f = {});
  template<class T, class Abi, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
    constexpr void unchecked_store(const basic_vec<T, Abi>& v, R&& r,
      const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first,
                                   iter_difference_t<I> n, flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first,
      iter_difference_t<I> n, const typename basic_vec<T, Abi>::mask_type& mask,
      flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first, S last,
                                   flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first, S last,
      const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});

  template<class T, class Abi, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
    constexpr void partial_store(const basic_vec<T, Abi>& v, R&& r,
                                 flags<Flags...> f = {});
  template<class T, class Abi, ranges::contiguous_range R, class... Flags>
    requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
    constexpr void partial_store(const basic_vec<T, Abi>& v, R&& r,
      const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void partial_store(
      const basic_vec<T, Abi>& v, I first, iter_difference_t<I> n, flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void partial_store(
      const basic_vec<T, Abi>& v, I first, iter_difference_t<I> n,
      const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void partial_store(const basic_vec<T, Abi>& v, I first, S last,
                                 flags<Flags...> f = {});
  template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
    requires indirectly_writable<I, T>
    constexpr void partial_store(const basic_vec<T, Abi>& v, I first, S last,
      const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});

  // [simd.permute.static], static permute
  static constexpr simd-size-type zero_element   = implementation-defined  // value of simd::zero_element;
  static constexpr simd-size-type uninit_element = implementation-defined  // value of simd::uninit_element;

  template<simd-size-type N = see below, simd-vec-type V, class IdxMap>
    constexpr resize_t<N, V> permute(const V& v, IdxMap&& idxmap);
  template<simd-size-type N = see below, simd-mask-type M, class IdxMap>
    constexpr resize_t<N, M> permute(const M& v, IdxMap&& idxmap);

  // [simd.permute.dynamic], dynamic permute
  template<simd-vec-type V, simd-integral I>
    constexpr resize_t<I::size(), V> permute(const V& v, const I& indices);
  template<simd-mask-type M, simd-integral I>
    constexpr resize_t<I::size(), M> permute(const M& v, const I& indices);

  // [simd.permute.mask], mask permute
  template<simd-vec-type V>
    constexpr V compress(const V& v, const typename V::mask_type& selector);
  template<simd-mask-type M>
    constexpr M compress(const M& v, const type_identity_t<M>& selector);
  template<simd-vec-type V>
    constexpr V compress(const V& v, const typename V::mask_type& selector,
                         const typename V::value_type& fill_value);
  template<simd-mask-type M>
    constexpr M compress(const M& v, const type_identity_t<M>& selector,
                         const typename M::value_type& fill_value);

  template<simd-vec-type V>
    constexpr V expand(const V& v, const typename V::mask_type& selector,
                       const V& original = {});
  template<simd-mask-type M>
    constexpr M expand(const M& v, const type_identity_t<M>& selector,
                       const M& original = {});

  // [simd.permute.memory], memory permute
  template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr V unchecked_gather_from(R&& in, const I& indices, flags<Flags...> f = {});
  template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr V unchecked_gather_from(R&& in, const typename I::mask_type& mask,
                                      const I& indices, flags<Flags...> f = {});

  template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr V partial_gather_from(R&& in, const I& indices, flags<Flags...> f = {});
  template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr V partial_gather_from(R&& in, const typename I::mask_type& mask,
                                    const I& indices, flags<Flags...> f = {});

  template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr void unchecked_scatter_to(const V& v, R&& out,
                                        const I& indices, flags<Flags...> f = {});
  template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr void unchecked_scatter_to(const V& v, R&& out, const typename I::mask_type& mask,
                                        const I& indices, flags<Flags...> f = {});

  template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr void partial_scatter_to(const V& v, R&& out,
                                      const I& indices, flags<Flags...> f = {});
  template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
    requires ranges::sized_range<R>
    constexpr void partial_scatter_to(const V& v, R&& out, const typename I::mask_type& mask,
                                      const I& indices, flags<Flags...> f = {});

  // [simd.creation], creation
  template<class T, class Abi>
    constexpr auto chunk(const basic_vec<typename T::value_type, Abi>& x) noexcept;
  template<class T, class Abi>
    constexpr auto chunk(const basic_mask<mask-element-size<T>, Abi>& x) noexcept;

  template<simd-size-type N, class T, class Abi>
    constexpr auto chunk(const basic_vec<T, Abi>& x) noexcept;
  template<simd-size-type N, size_t Bytes, class Abi>
    constexpr auto chunk(const basic_mask<Bytes, Abi>& x) noexcept;

  template<class T, class... Abis>
    constexpr basic_vec<T, deduce-abi-t<T, (basic_vec<T, Abis>::size() + ...)>>
      cat(const basic_vec<T, Abis>&...) noexcept;
  template<size_t Bytes, class... Abis>
    constexpr basic_mask<Bytes, deduce-abi-t<integer-from<Bytes>,
                              (basic_mask<Bytes, Abis>::size() + ...)>>
      cat(const basic_mask<Bytes, Abis>&...) noexcept;

  // [simd.alg], algorithms
  template<class T, class Abi>
    constexpr basic_vec<T, Abi>
      min(const basic_vec<T, Abi>& a, const basic_vec<T, Abi>& b) noexcept;
  template<class T, class Abi>
    constexpr basic_vec<T, Abi>
      max(const basic_vec<T, Abi>& a, const basic_vec<T, Abi>& b) noexcept;
  template<class T, class Abi>
    constexpr pair<basic_vec<T, Abi>, basic_vec<T, Abi>>
      minmax(const basic_vec<T, Abi>& a, const basic_vec<T, Abi>& b) noexcept;
  template<class T, class Abi>
    constexpr basic_vec<T, Abi>
      clamp(const basic_vec<T, Abi>& v, const basic_vec<T, Abi>& lo,
            const basic_vec<T, Abi>& hi);

  template<class T, class U>
    constexpr auto select(bool c, const T& a, const U& b)
    -> remove_cvref_t<decltype(c ? a : b)>;
  template<size_t Bytes, class Abi, class T, class U>
    constexpr auto select(const basic_mask<Bytes, Abi>& c, const T& a, const U& b)
    noexcept -> decltype(simd-select-impl(c, a, b));

  // [simd.math], mathematical functions
  template<math-floating-point V> constexpr deduced-vec-t<V> acos(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> asin(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> atan(const V& x);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> atan2(const V0& y, const V1& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> cos(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> sin(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> tan(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> acosh(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> asinh(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> atanh(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> cosh(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> sinh(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> tanh(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> exp(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> exp2(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> expm1(const V& x);
  template<math-floating-point V>
    constexpr deduced-vec-t<V>
      frexp(const V& value, rebind_t<int, deduced-vec-t<V>>* exp);
  template<math-floating-point V>
    constexpr rebind_t<int, deduced-vec-t<V>> ilogb(const V& x);
  template<math-floating-point V>
    constexpr deduced-vec-t<V> ldexp(const V& x, const rebind_t<int, deduced-vec-t<V>>& exp);
  template<math-floating-point V> constexpr deduced-vec-t<V> log(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> log10(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> log1p(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> log2(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> logb(const V& x);
  template<class T, class Abi>
    constexpr basic_vec<T, Abi>
      modf(const type_identity_t<basic_vec<T, Abi>>& value, basic_vec<T, Abi>* iptr);
  template<math-floating-point V>
    constexpr deduced-vec-t<V> scalbn(const V& x, const rebind_t<int, deduced-vec-t<V>>& n);
  template<math-floating-point V>
    constexpr deduced-vec-t<V> scalbln(
      const V& x, const rebind_t<long int, deduced-vec-t<V>>& n);
  template<math-floating-point V> constexpr deduced-vec-t<V> cbrt(const V& x);
  template<signed_integral T, class Abi>
    constexpr basic_vec<T, Abi> abs(const basic_vec<T, Abi>& j);
  template<math-floating-point V> constexpr deduced-vec-t<V> abs(const V& j);
  template<math-floating-point V> constexpr deduced-vec-t<V> fabs(const V& x);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> hypot(const V0& x, const V1& y);
  template<class V0, class V1, class V2>
    constexpr math-common-simd-t<V0, V1, V2> hypot(const V0& x, const V1& y, const V2& z);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> pow(const V0& x, const V1& y);
  template<math-floating-point V> constexpr deduced-vec-t<V> sqrt(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> erf(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> erfc(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> lgamma(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> tgamma(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> ceil(const V& x);
  template<math-floating-point V> constexpr deduced-vec-t<V> floor(const V& x);
  template<math-floating-point V> deduced-vec-t<V> nearbyint(const V& x);
  template<math-floating-point V> deduced-vec-t<V> rint(const V& x);
  template<math-floating-point V>
    rebind_t<long int, deduced-vec-t<V>> lrint(const V& x);
  template<math-floating-point V>
    rebind_t<long long int, V> llrint(const deduced-vec-t<V>& x);
  template<math-floating-point V>
    constexpr deduced-vec-t<V> round(const V& x);
  template<math-floating-point V>
    constexpr rebind_t<long int, deduced-vec-t<V>> lround(const V& x);
  template<math-floating-point V>
    constexpr rebind_t<long long int, deduced-vec-t<V>> llround(const V& x);
  template<math-floating-point V>
    constexpr deduced-vec-t<V> trunc(const V& x);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> fmod(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> remainder(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1>
      remquo(const V0& x, const V1& y, rebind_t<int, math-common-simd-t<V0, V1>>* quo);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> copysign(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> nextafter(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> fdim(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> fmax(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr math-common-simd-t<V0, V1> fmin(const V0& x, const V1& y);
  template<class V0, class V1, class V2>
    constexpr math-common-simd-t<V0, V1, V2> fma(const V0& x, const V1& y, const V2& z);
  template<class V0, class V1, class V2>
    constexpr math-common-simd-t<V0, V1, V2>
      lerp(const V0& a, const V1& b, const V2& t) noexcept;
  template<math-floating-point V>
    constexpr rebind_t<int, deduced-vec-t<V>> fpclassify(const V& x);
  template<math-floating-point V>
    constexpr typename deduced-vec-t<V>::mask_type isfinite(const V& x);
  template<math-floating-point V>
    constexpr typename deduced-vec-t<V>::mask_type isinf(const V& x);
  template<math-floating-point V>
    constexpr typename deduced-vec-t<V>::mask_type isnan(const V& x);
  template<math-floating-point V>
    constexpr typename deduced-vec-t<V>::mask_type isnormal(const V& x);
  template<math-floating-point V>
    constexpr typename deduced-vec-t<V>::mask_type signbit(const V& x);
  template<class V0, class V1>
    constexpr typename math-common-simd-t<V0, V1>::mask_type
      isgreater(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr typename math-common-simd-t<V0, V1>::mask_type
      isgreaterequal(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr typename math-common-simd-t<V0, V1>::mask_type
      isless(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr typename math-common-simd-t<V0, V1>::mask_type
      islessequal(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr typename math-common-simd-t<V0, V1>::mask_type
      islessgreater(const V0& x, const V1& y);
  template<class V0, class V1>
    constexpr typename math-common-simd-t<V0, V1>::mask_type
      isunordered(const V0& x, const V1& y);
  template<math-floating-point V>
    deduced-vec-t<V> assoc_laguerre(const rebind_t<unsigned, deduced-vec-t<V>>& n,
                                    const rebind_t<unsigned, deduced-vec-t<V>>& m, const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> assoc_legendre(const rebind_t<unsigned, deduced-vec-t<V>>& l,
                                    const rebind_t<unsigned, deduced-vec-t<V>>& m, const V& x);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> beta(const V0& x, const V1& y);
  template<math-floating-point V> deduced-vec-t<V> comp_ellint_1(const V& k);
  template<math-floating-point V> deduced-vec-t<V> comp_ellint_2(const V& k);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> comp_ellint_3(const V0& k, const V1& nu);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> cyl_bessel_i(const V0& nu, const V1& x);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> cyl_bessel_j(const V0& nu, const V1& x);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> cyl_bessel_k(const V0& nu, const V1& x);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> cyl_neumann(const V0& nu, const V1& x);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> ellint_1(const V0& k, const V1& phi);
  template<class V0, class V1>
    math-common-simd-t<V0, V1> ellint_2(const V0& k, const V1& phi);
  template<class V0, class V1, class V2>
    math-common-simd-t<V0, V1, V2> ellint_3(const V0& k, const V1& nu, const V2& phi);
  template<math-floating-point V> deduced-vec-t<V> expint(const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> hermite(const rebind_t<unsigned, deduced-vec-t<V>>& n, const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> laguerre(const rebind_t<unsigned, deduced-vec-t<V>>& n, const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> legendre(const rebind_t<unsigned, deduced-vec-t<V>>& l, const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> riemann_zeta(const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> sph_bessel(
      const rebind_t<unsigned, deduced-vec-t<V>>& n, const V& x);
  template<math-floating-point V>
    deduced-vec-t<V> sph_legendre(const rebind_t<unsigned, deduced-vec-t<V>>& l,
      const rebind_t<unsigned, deduced-vec-t<V>>& m, const V& theta);
  template<math-floating-point V>
    deduced-vec-t<V>
      sph_neumann(const rebind_t<unsigned, deduced-vec-t<V>>& n, const V& x);

  // [simd.bit], bit manipulation
  template<simd-vec-type V> constexpr V byteswap(const V& v) noexcept;
  template<simd-vec-type V> constexpr V bit_ceil(const V& v) noexcept;
  template<simd-vec-type V> constexpr V bit_floor(const V& v) noexcept;

  template<simd-vec-type V>
    constexpr typename V::mask_type has_single_bit(const V& v) noexcept;

  template<simd-vec-type V0, simd-vec-type V1>
    constexpr V0 rotl(const V0& v, const V1& s) noexcept;
  template<simd-vec-type V>
    constexpr V  rotl(const V& v, int s) noexcept;

  template<simd-vec-type V0, simd-vec-type V1>
    constexpr V0 rotr(const V0& v, const V1& s) noexcept;
  template<simd-vec-type V>
    constexpr V  rotr(const V& v, int s) noexcept;

  template<simd-vec-type V>
    constexpr rebind_t<make_signed_t<typename V::value_type>, V>
      bit_width(const V& v) noexcept;
  template<simd-vec-type V>
    constexpr rebind_t<make_signed_t<typename V::value_type>, V>
      countl_zero(const V& v) noexcept;
  template<simd-vec-type V>
    constexpr rebind_t<make_signed_t<typename V::value_type>, V>
      countl_one(const V& v) noexcept;
  template<simd-vec-type V>
    constexpr rebind_t<make_signed_t<typename V::value_type>, V>
      countr_zero(const V& v) noexcept;
  template<simd-vec-type V>
    constexpr rebind_t<make_signed_t<typename V::value_type>, V>
      countr_one(const V& v) noexcept;
  template<simd-vec-type V>
    constexpr rebind_t<make_signed_t<typename V::value_type>, V>
      popcount(const V& v) noexcept;

  // [simd.complex.math], complex math
  template<simd-complex V>
    constexpr rebind_t<simd-complex-value-type<V>, V> real(const V&) noexcept;

  template<simd-complex V>
    constexpr rebind_t<simd-complex-value-type<V>, V> imag(const V&) noexcept;

  template<simd-complex V>
    constexpr rebind_t<simd-complex-value-type<V>, V> abs(const V&);

  template<simd-complex V>
    constexpr rebind_t<simd-complex-value-type<V>, V> arg(const V&);

  template<simd-complex V>
    constexpr rebind_t<simd-complex-value-type<V>, V> norm(const V&);

  template<simd-complex V> constexpr V conj(const V&);
  template<simd-complex V> constexpr V proj(const V&);
  template<simd-complex V> constexpr V exp(const V& v);
  template<simd-complex V> constexpr V log(const V& v);
  template<simd-complex V> constexpr V log10(const V& v);

  template<simd-complex V> constexpr V sqrt(const V& v);
  template<simd-complex V> constexpr V sin(const V& v);
  template<simd-complex V> constexpr V asin(const V& v);
  template<simd-complex V> constexpr V cos(const V& v);
  template<simd-complex V> constexpr V acos(const V& v);
  template<simd-complex V> constexpr V tan(const V& v);
  template<simd-complex V> constexpr V atan(const V& v);
  template<simd-complex V> constexpr V sinh(const V& v);
  template<simd-complex V> constexpr V asinh(const V& v);
  template<simd-complex V> constexpr V cosh(const V& v);
  template<simd-complex V> constexpr V acosh(const V& v);
  template<simd-complex V> constexpr V tanh(const V& v);
  template<simd-complex V> constexpr V atanh(const V& v);

  template<simd-floating-point V>
    rebind_t<complex<typename V::value_type>, V> polar(const V& x, const V& y = {});

  template<simd-complex V> constexpr V pow(const V& x, const V& y);

  // [simd.mask.class], class template basic_mask
  template<size_t Bytes, class Abi = native-abi<integer-from<Bytes>>> class basic_mask;
  template<class T, simd-size-type N = simd-size-v<T, native-abi<T>>>
    using mask = basic_mask<sizeof(T), deduce-abi-t<T, N>>;

  // [simd.mask.reductions], reductions
  template<size_t Bytes, class Abi>
    constexpr bool all_of(const basic_mask<Bytes, Abi>&) noexcept;
  template<size_t Bytes, class Abi>
    constexpr bool any_of(const basic_mask<Bytes, Abi>&) noexcept;
  template<size_t Bytes, class Abi>
    constexpr bool none_of(const basic_mask<Bytes, Abi>&) noexcept;
  template<size_t Bytes, class Abi>
    constexpr simd-size-type reduce_count(const basic_mask<Bytes, Abi>&) noexcept;
  template<size_t Bytes, class Abi>
    constexpr simd-size-type reduce_min_index(const basic_mask<Bytes, Abi>&);
  template<size_t Bytes, class Abi>
    constexpr simd-size-type reduce_max_index(const basic_mask<Bytes, Abi>&);

  constexpr bool all_of(same_as<bool> auto) noexcept;
  constexpr bool any_of(same_as<bool> auto) noexcept;
  constexpr bool none_of(same_as<bool> auto) noexcept;
  constexpr simd-size-type reduce_count(same_as<bool> auto) noexcept;
  constexpr simd-size-type reduce_min_index(same_as<bool> auto);
  constexpr simd-size-type reduce_max_index(same_as<bool> auto);
}

namespace std {
  // See [simd.alg], algorithms
  using simd::min;
  using simd::max;
  using simd::minmax;
  using simd::clamp;

  // See [simd.math], mathematical functions
  using simd::acos;
  using simd::asin;
  using simd::atan;
  using simd::atan2;
  using simd::cos;
  using simd::sin;
  using simd::tan;
  using simd::acosh;
  using simd::asinh;
  using simd::atanh;
  using simd::cosh;
  using simd::sinh;
  using simd::tanh;
  using simd::exp;
  using simd::exp2;
  using simd::expm1;
  using simd::frexp;
  using simd::ilogb;
  using simd::ldexp;
  using simd::log;
  using simd::log10;
  using simd::log1p;
  using simd::log2;
  using simd::logb;
  using simd::modf;
  using simd::scalbn;
  using simd::scalbln;
  using simd::cbrt;
  using simd::abs;
  using simd::fabs;
  using simd::hypot;
  using simd::pow;
  using simd::sqrt;
  using simd::erf;
  using simd::erfc;
  using simd::lgamma;
  using simd::tgamma;
  using simd::ceil;
  using simd::floor;
  using simd::nearbyint;
  using simd::rint;
  using simd::lrint;
  using simd::llrint;
  using simd::round;
  using simd::lround;
  using simd::llround;
  using simd::trunc;
  using simd::fmod;
  using simd::remainder;
  using simd::remquo;
  using simd::copysign;
  using simd::nextafter;
  using simd::fdim;
  using simd::fmax;
  using simd::fmin;
  using simd::fma;
  using simd::lerp;
  using simd::fpclassify;
  using simd::isfinite;
  using simd::isinf;
  using simd::isnan;
  using simd::isnormal;
  using simd::signbit;
  using simd::isgreater;
  using simd::isgreaterequal;
  using simd::isless;
  using simd::islessequal;
  using simd::islessgreater;
  using simd::isunordered;
  using simd::assoc_laguerre;
  using simd::assoc_legendre;
  using simd::beta;
  using simd::comp_ellint_1;
  using simd::comp_ellint_2;
  using simd::comp_ellint_3;
  using simd::cyl_bessel_i;
  using simd::cyl_bessel_j;
  using simd::cyl_bessel_k;
  using simd::cyl_neumann;
  using simd::ellint_1;
  using simd::ellint_2;
  using simd::ellint_3;
  using simd::expint;
  using simd::hermite;
  using simd::laguerre;
  using simd::legendre;
  using simd::riemann_zeta;
  using simd::sph_bessel;
  using simd::sph_legendre;
  using simd::sph_neumann;

  // See [simd.bit], bit manipulation
  using simd::byteswap;
  using simd::bit_ceil;
  using simd::bit_floor;
  using simd::has_single_bit;
  using simd::rotl;
  using simd::rotr;
  using simd::bit_width;
  using simd::countl_zero;
  using simd::countl_one;
  using simd::countr_zero;
  using simd::countr_one;
  using simd::popcount;

  // See [simd.complex.math], vec complex math
  using simd::real;
  using simd::imag;
  using simd::arg;
  using simd::norm;
  using simd::conj;
  using simd::proj;
  using simd::polar;
}
```

### Type traits <a id="simd.traits">[[simd.traits]]</a>

``` cpp
template<class T, class U = typename T::value_type> struct alignment { see below };
```

`alignment<T, U>` has a member `value` if and only if

- `T` is a specialization of `basic_mask` and `U` is `bool`, or
- `T` is a specialization of `basic_vec` and `U` is a vectorizable type.

If `value` is present, the type `alignment<T, U>` is a `BinaryTypeTrait`
with a base characteristic of `integral_constant<size_t, N>` for some
unspecified `N`[[simd.ctor,simd.loadstore]].

[*Note 1*: `value` identifies the alignment restrictions on pointers
used for (converting) loads and stores for the given type `T` on arrays
of type `U`. — *end note*]

The behavior of a program that adds specializations for `alignment` is
undefined.

``` cpp
template<class T, class V> struct rebind { using type = see below; };
```

The member `type` is present if and only if

- `V` is a data-parallel type,
- `T` is a vectorizable type, and
- *`deduce-abi-t`*`<T, V::size()>` has a member type `type`.

If V is a specialization of `basic_vec`, let `Abi1` denote an ABI tag
such that `basic_vec<T, Abi1>::size()` equals `V::size()`. If V is a
specialization of `basic_mask`, let `Abi1` denote an ABI tag such that
`basic_mask<sizeof(T), Abi1>::size()` equals `V::size()`.

Where present, the member typedef `type` names `basic_vec<T, Abi1>` if V
is a specialization of `basic_vec` or `basic_mask<sizeof(T), Abi1>` if V
is a specialization of `basic_mask`.

``` cpp
template<simd-size-type N, class V> struct resize { using type = see below; };
```

Let `T` denote

- `typename V::value_type` if `V` is a specialization of `basic_vec`,
- otherwise *`integer-from`*`<`*`mask-element-size`*`<V>>` if `V` is a
  specialization of `basic_mask`.

The member `type` is present if and only if

- `V` is a data-parallel type, and
- *`deduce-abi-t`*`<T, N>` has a member type `type`.

If V is a specialization of `basic_vec`, let `Abi1` denote an ABI tag
such that `basic_vec<T, Abi1>::size()` equals `N`. If V is a
specialization of `basic_mask`, let `Abi1` denote an ABI tag such that
`basic_mask<sizeof(T), Abi1>::size()` equals `N`.

Where present, the member typedef `type` names `basic_vec<T, Abi1>` if V
is a specialization of `basic_vec` or `basic_mask<sizeof(T), Abi1>` if V
is a specialization of `basic_mask`.

### Load and store flags <a id="simd.flags">[[simd.flags]]</a>

#### Class template `flags` overview <a id="simd.flags.overview">[[simd.flags.overview]]</a>

``` cpp
namespace std::simd {
  template<class... Flags> struct flags {
    // [simd.flags.oper], flags operators
    template<class... Other>
      friend consteval auto operator|(flags, flags<Other...>);
  };
}
```

[*Note 1*: The class template `flags` acts like an integer bit-flag for
types. — *end note*]

*Constraints:* Every type in the parameter pack `Flags` is one of
`convert-flag`, `aligned-flag`, or `overaligned-{flag}<N>`.

#### `flags` operators <a id="simd.flags.oper">[[simd.flags.oper]]</a>

``` cpp
template<class... Other>
  friend consteval auto operator|(flags a, flags<Other...> b);
```

*Returns:* A default-initialized object of type `flags<Flags2...>` for
some `Flags2` where every type in `Flags2` is present either in template
parameter pack `Flags` or in template parameter pack `Other`, and every
type in template parameter packs `Flags` and `Other` is present in
`Flags2`. If the packs `Flags` and `Other` contain two different
specializations *`overaligned-flag`*`<N1>` and
*`overaligned-flag`*`<N2>`, `Flags2` is not required to contain the
specialization *`overaligned-flag`*`<std::min(N1, N2)>`.

### Class template *simd-iterator* <a id="simd.iterator">[[simd.iterator]]</a>

``` cpp
namespace std::simd {
  template<class V>
  class simd-iterator {                                                 // exposition only
    V* data_ = nullptr;                                                 // exposition only
    simd-size-type offset_ = 0;                                         // exposition only

    constexpr simd-iterator(V& d, simd-size-type off) noexcept;         // exposition only

  public:
    using value_type = V::value_type;
    using iterator_category = input_iterator_tag;
    using iterator_concept = random_access_iterator_tag;
    using difference_type = simd-size-type;

    constexpr simd-iterator() = default;

    constexpr simd-iterator(const simd-iterator&) = default;
    constexpr simd-iterator& operator=(const simd-iterator&) = default;

    constexpr simd-iterator(const simd-iterator<remove_const_t<V>>&) requires is_const_v<V>;

    constexpr value_type operator*() const;

    constexpr simd-iterator& operator++();
    constexpr simd-iterator operator++(int);
    constexpr simd-iterator& operator--();
    constexpr simd-iterator operator--(int);

    constexpr simd-iterator& operator+=(difference_type n);
    constexpr simd-iterator& operator-=(difference_type n);

    constexpr value_type operator[](difference_type n) const;

    friend constexpr bool operator==(simd-iterator a, simd-iterator b) = default;
    friend constexpr bool operator==(simd-iterator a, default_sentinel_t) noexcept;
    friend constexpr auto operator<=>(simd-iterator a, simd-iterator b);

    friend constexpr simd-iterator operator+(simd-iterator i, difference_type n);
    friend constexpr simd-iterator operator+(difference_type n, simd-iterator i);
    friend constexpr simd-iterator operator-(simd-iterator i, difference_type n);

    friend constexpr difference_type operator-(simd-iterator a, simd-iterator b);
    friend constexpr difference_type operator-(simd-iterator i, default_sentinel_t) noexcept;
    friend constexpr difference_type operator-(default_sentinel_t, simd-iterator i) noexcept;
  };
}
```

``` cpp
constexpr simd-iterator(V& d, simd-size-type off) noexcept;
```

*Effects:* Initializes *data\_* with `addressof(d)` and *offset\_* with
`off`.

``` cpp
constexpr simd-iterator(const simd-iterator<remove_const_t<V>>& i) requires is_const_v<V>;
```

*Effects:* Initializes *data\_* with `i.`*`data_`* and *offset\_* with
`i.`*`offset_`*.

``` cpp
constexpr value_type operator*() const;
```

*Effects:* Equivalent to: `return (*`*`data_`*`)[`*`offset_`*`];`

``` cpp
constexpr simd-iterator& operator++();
```

*Effects:* Equivalent to: `return *this += 1;`

``` cpp
constexpr simd-iterator operator++(int);
```

*Effects:* Equivalent to:

``` cpp
simd-iterator tmp = *this;
*this += 1;
return tmp;
```

``` cpp
constexpr simd-iterator& operator--();
```

*Effects:* Equivalent to: `return *this -= 1;`

``` cpp
constexpr simd-iterator operator--(int);
```

*Effects:* Equivalent to:

``` cpp
simd-iterator tmp = *this;
*this -= 1;
return tmp;
```

``` cpp
constexpr simd-iterator& operator+=(difference_type n);
```

*Preconditions:* *`offset_`*` + n` is in the range \[`0`, `V::size()`\].

*Effects:* Equivalent to:

``` cpp
offset_ += n;
return *this;
```

``` cpp
constexpr simd-iterator& operator-=(difference_type n);
```

*Preconditions:* *`offset_`*` - n` is in the range \[`0`, `V::size()`\].

*Effects:* Equivalent to:

``` cpp
offset_ -= n;
return *this;
```

``` cpp
constexpr value_type operator[](difference_type n) const;
```

*Effects:* Equivalent to: `return (*`*`data_`*`)[`*`offset_`*` + n];`

``` cpp
friend constexpr bool operator==(simd-iterator i, default_sentinel_t) noexcept;
```

*Effects:* Equivalent to: `return i.`*`offset_`*` == V::size();`

``` cpp
friend constexpr auto operator<=>(simd-iterator a, simd-iterator b);
```

*Preconditions:* `a.`*`data_`*` == b.`*`data_`* is `true`.

*Effects:* Equivalent to: `return a.`*`offset_`*` <=> b.`*`offset_`*`;`

``` cpp
friend constexpr simd-iterator operator+(simd-iterator i, difference_type n);
friend constexpr simd-iterator operator+(difference_type n, simd-iterator i);
```

*Effects:* Equivalent to: `return i += n;`

``` cpp
friend constexpr simd-iterator operator-(simd-iterator i, difference_type n);
```

*Effects:* Equivalent to: `return i -= n;`

``` cpp
friend constexpr difference_type operator-(simd-iterator a, simd-iterator b);
```

*Preconditions:* `a.`*`data_`*` == b.`*`data_`* is `true`.

*Effects:* Equivalent to: `return a.`*`offset_`*` - b.`*`offset_`*`;`

``` cpp
friend constexpr difference_type operator-(simd-iterator i, default_sentinel_t) noexcept;
```

*Effects:* Equivalent to: `return i.`*`offset_`*` - V::size();`

``` cpp
friend constexpr difference_type operator-(default_sentinel_t, simd-iterator i) noexcept;
```

*Effects:* Equivalent to: `return V::size() - i.`*`offset_`*`;`

### Class template `basic_vec` <a id="simd.class">[[simd.class]]</a>

#### Overview <a id="simd.overview">[[simd.overview]]</a>

``` cpp
namespace std::simd {
  template<class T, class Abi> class basic_vec {
  public:
    using value_type = T;
    using mask_type = basic_mask<sizeof(T), Abi>;
    using abi_type = Abi;
    using iterator = simd-iterator<basic_vec>;
    using const_iterator = simd-iterator<const basic_vec>;

    constexpr iterator begin() noexcept { return {*this, 0}; }
    constexpr const_iterator begin() const noexcept { return {*this, 0}; }
    constexpr const_iterator cbegin() const noexcept { return {*this, 0}; }
    constexpr default_sentinel_t end() const noexcept { return {}; }
    constexpr default_sentinel_t cend() const noexcept { return {}; }

    static constexpr integral_constant<simd-size-type, simd-size-v<T, Abi>> size {};

    constexpr basic_vec() noexcept = default;

    // [simd.ctor], basic_vec constructors
    template<class U>
      constexpr explicit(see below) basic_vec(U&& value) noexcept;
    template<class U, class UAbi>
      constexpr explicit(see below) basic_vec(const basic_vec<U, UAbi>&) noexcept;
    template<class G>
      constexpr explicit basic_vec(G&& gen);
    template<class R, class... Flags>
      constexpr basic_vec(R&& range, flags<Flags...> = {});
    template<class R, class... Flags>
      constexpr basic_vec(R&& range, const mask_type& mask, flags<Flags...> = {});
    template<simd-floating-point V>
      constexpr explicit(see below) basic_vec(const V& reals, const V& imags = {}) noexcept;

    // [simd.subscr], basic_vec subscript operators
    constexpr value_type operator[](simd-size-type) const;
    template<simd-integral I>
      constexpr resize_t<I::size(), basic_vec> operator[](const I& indices) const;

    // [simd.complex.access], basic_vec complex accessors
    constexpr auto real() const noexcept;
    constexpr auto imag() const noexcept;
    template<simd-floating-point V>
      constexpr void real(const V& v) noexcept;
    template<simd-floating-point V>
      constexpr void imag(const V& v) noexcept;

    // [simd.unary], basic_vec unary operators
    constexpr basic_vec& operator++() noexcept;
    constexpr basic_vec operator++(int) noexcept;
    constexpr basic_vec& operator--() noexcept;
    constexpr basic_vec operator--(int) noexcept;
    constexpr mask_type operator!() const noexcept;
    constexpr basic_vec operator~() const noexcept;
    constexpr basic_vec operator+() const noexcept;
    constexpr basic_vec operator-() const noexcept;

    // [simd.binary], basic_vec binary operators
    friend constexpr basic_vec operator+(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator-(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator*(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator/(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator%(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator&(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator|(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator^(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator<<(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator>>(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec operator<<(const basic_vec&, simd-size-type) noexcept;
    friend constexpr basic_vec operator>>(const basic_vec&, simd-size-type) noexcept;

    // [simd.cassign], basic_vec compound assignment
    friend constexpr basic_vec& operator+=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator-=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator*=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator/=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator%=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator&=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator|=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator^=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator<<=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator>>=(basic_vec&, const basic_vec&) noexcept;
    friend constexpr basic_vec& operator<<=(basic_vec&, simd-size-type) noexcept;
    friend constexpr basic_vec& operator>>=(basic_vec&, simd-size-type) noexcept;

    // [simd.comparison], basic_vec compare operators
    friend constexpr mask_type operator==(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr mask_type operator!=(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr mask_type operator>=(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr mask_type operator<=(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr mask_type operator>(const basic_vec&, const basic_vec&) noexcept;
    friend constexpr mask_type operator<(const basic_vec&, const basic_vec&) noexcept;

    // [simd.cond], basic_vec exposition only conditional operators
    friend constexpr basic_vec simd-select-impl( // exposition only
      const mask_type&, const basic_vec&, const basic_vec&) noexcept;
  };

  template<class R, class... Ts>
    basic_vec(R&& r, Ts...) -> see below;
}
```

Every specialization of `basic_vec` is a complete type. The
specialization of `basic_vec<T, Abi>` is

- enabled, if `T` is a vectorizable type, and there exists value `N` in
  the range \[`1`, `64`\], such that `Abi` is `deduce-abi-t<T, N>`,
- otherwise, disabled, if `T` is not a vectorizable type,
- otherwise, it is *implementation-defined* if such a specialization is
  enabled.

If `basic_vec<T, Abi>` is disabled, then the specialization has a
deleted default constructor, deleted destructor, deleted copy
constructor, and deleted copy assignment. In addition only the
`value_type`, `abi_type`, and `mask_type` members are present.

If `basic_vec<T, Abi>` is enabled, then `basic_vec<T, Abi>` is trivially
copyable, default-initialization of an object of such a type
default-initializes all elements, and value-initialization
value-initializes all elements [[dcl.init.general]].

*Recommended practice:* Implementations should support implicit
conversions between specializations of `basic_vec` and appropriate
*implementation-defined* types.

[*Note 1*: Appropriate types are non-standard vector types which are
available in the implementation. — *end note*]

#### Constructors <a id="simd.ctor">[[simd.ctor]]</a>

``` cpp
template<class U> constexpr explicit(see below) basic_vec(U&& value) noexcept;
```

Let `From` denote the type `remove_cvref_t<U>`.

*Constraints:* `value_type` satisfies `constructible_from<U>`.

*Effects:* Initializes each element to the value of the argument after
conversion to `value_type`.

*Remarks:* The expression inside `explicit` evaluates to `false` if and
only if `U` satisfies `convertible_to<value_type>`, and either

- `From` is not an arithmetic type and does not satisfy
  `constexpr-wrapper-like`,
- `From` is an arithmetic type and the conversion from `From` to
  `value_type` is value-preserving [[simd.general]], or
- `From` satisfies `constexpr-wrapper-like`,
  `remove_const_t<decltype(From::value)>` is an arithmetic type, and
  `From::value` is representable by `value_type`.

``` cpp
template<class U, class UAbi>
  constexpr explicit(see below) basic_vec(const basic_vec<U, UAbi>& x) noexcept;
```

*Constraints:* *`simd-size-v`*`<U, UAbi> == size()` is `true`.

*Effects:* Initializes the iᵗʰ element with `static_cast<T>(x[`i`])` for
all i in the range of \[`0`, `size()`).

*Remarks:* The expression inside `explicit` evaluates to `true` if
either

- the conversion from `U` to `value_type` is not value-preserving, or
- both `U` and `value_type` are integral types and the integer
  conversion rank [[conv.rank]] of `U` is greater than the integer
  conversion rank of `value_type`, or
- both `U` and `value_type` are floating-point types and the
  floating-point conversion rank [[conv.rank]] of `U` is greater than
  the floating-point conversion rank of `value_type`.

``` cpp
template<class G> constexpr explicit basic_vec(G&& gen);
```

Let `From`ᵢ denote the type
`decltype(gen(integral_constant<`*`simd-size-type`*`, `i`>()))`.

*Constraints:* `From`ᵢ satisfies `convertible_to<value_type>` for all i
in the range of \[`0`, `size()`). In addition, for all i in the range of
\[`0`, `size()`), if `From`ᵢ is an arithmetic type, conversion from
`From`ᵢ to `value_type` is value-preserving.

*Effects:* Initializes the iᵗʰ element with
`static_cast<value_type>(gen(integral_constant<`*`simd-size-type`*`, i>()))`
for all i in the range of \[`0`, `size()`).

*Remarks:* `gen` is invoked exactly once for each i, in increasing order
of i.

``` cpp
template<class R, class... Flags>
  constexpr basic_vec(R&& r, flags<Flags...> = {});
template<class R, class... Flags>
  constexpr basic_vec(R&& r, const mask_type& mask, flags<Flags...> = {});
```

Let `mask` be `mask_type(true)` for the overload with no `mask`
parameter.

*Constraints:*

- `R` models `ranges::contiguous_range` and `ranges::sized_range`,
- `ranges::size(r)` is a constant expression, and
- `ranges::size(r)` is equal to `size()`.

*Mandates:*

- `ranges::range_value_t<R>` is a vectorizable type, and
- if the template parameter pack `Flags` does not contain
  *`convert-flag`*, then the conversion from `ranges::range_value_t<R>`
  to `value_type` is value-preserving.

*Preconditions:*

- If the template parameter pack `Flags` contains *`aligned-flag`*,
  `ranges::data(r)` points to storage aligned by
  `alignment_v<basic_vec, ranges::range_value_t<R>>`.
- If the template parameter pack `Flags` contains
  *`overaligned-flag`*`<N>`, `ranges::data(r)` points to storage aligned
  by `N`.

*Effects:* Initializes the iᵗʰ element with
`mask[`i`] ? static_cast<T>(ranges::data(r)[`i`]) : T()` for all i in
the range of \[`0`, `size()`).

``` cpp
template<class R, class... Ts>
  basic_vec(R&& r, Ts...) -> see below;
```

*Constraints:*

- `R` models `ranges::contiguous_range` and `ranges::sized_range`, and
- `ranges::size(r)` is a constant expression.

*Remarks:* The deduced type is equivalent to
`vec<ranges::range_value_t<R>, ranges::size(r)>`.

``` cpp
template<simd-floating-point V>
  constexpr explicit(see below)
    basic_vec(const V& reals, const V& imags = {}) noexcept;
```

*Constraints:*

- `simd-complex<basic_vec>` is modeled, and
- `V::size() == size()` is `true`.

*Effects:* Initializes the iᵗʰ element with
`value_type(reals[`i`], imags[`i`])` for all i in the range \[`0`,
`size()`).

*Remarks:* The expression inside `explicit` evaluates to `false` if and
only if the floating-point conversion rank of `T::value_type` is greater
than or equal to the floating-point conversion rank of `V::value_type`.

#### Subscript operator <a id="simd.subscr">[[simd.subscr]]</a>

``` cpp
constexpr value_type operator[](simd-size-type i) const;
```

*Preconditions:* `i >= 0 && i < size()` is `true`.

*Returns:* The value of the iᵗʰ element.

*Throws:* Nothing.

``` cpp
template<simd-integral I>
  constexpr resize_t<I::size(), basic_vec> operator[](const I& indices) const;
```

*Effects:* Equivalent to: `return permute(*this, indices);`

#### Complex accessors <a id="simd.complex.access">[[simd.complex.access]]</a>

``` cpp
constexpr auto real() const noexcept;
constexpr auto imag() const noexcept;
```

*Constraints:* `simd-complex<basic_vec>` is modeled.

*Returns:* An object of type
`rebind_t<typename T::value_type, basic_vec>` where the iᵗʰ element is
initialized to the result of *`cmplx-func`*`(operator[](`i`))` for all i
in the range \[`0`, `size()`), where *`cmplx-func`* is the corresponding
function from `<complex>`.

``` cpp
template<simd-floating-point V>
  constexpr void real(const V& v) noexcept;
template<simd-floating-point V>
  constexpr void imag(const V& v) noexcept;
```

*Constraints:*

- `simd-complex<basic_vec>` is modeled,
- `same_as<typename V::value_type, typename T::value_type>` is modeled,
  and
- `V::size() == size()` is `true`.

*Effects:* Replaces each element of the `basic_vec` object such that the
iᵗʰ element is replaced with
`value_type(v[`i`], operator[](`i`).imag())` or
`value_type(operator[](`i`).real(), v[`i`])` for `real` and `imag`
respectively, for all i in the range \[`0`, `size()`).

#### Unary operators <a id="simd.unary">[[simd.unary]]</a>

Effects in [[simd.unary]] are applied as unary element-wise operations.

``` cpp
constexpr basic_vec& operator++() noexcept;
```

*Constraints:* `requires (value_type a) { ++a; }` is `true`.

*Effects:* Increments every element by one.

*Returns:* `*this`.

``` cpp
constexpr basic_vec operator++(int) noexcept;
```

*Constraints:* `requires (value_type a) { a++; }` is `true`.

*Effects:* Increments every element by one.

*Returns:* A copy of `*this` before incrementing.

``` cpp
constexpr basic_vec& operator--() noexcept;
```

*Constraints:* `requires (value_type a) { –a; }` is `true`.

*Effects:* Decrements every element by one.

*Returns:* `*this`.

``` cpp
constexpr basic_vec operator--(int) noexcept;
```

*Constraints:* `requires (value_type a) { a–; }` is `true`.

*Effects:* Decrements every element by one.

*Returns:* A copy of `*this` before decrementing.

``` cpp
constexpr mask_type operator!() const noexcept;
```

*Constraints:* `requires (const value_type a) { !a; }` is `true`.

*Returns:* A `basic_mask` object with the iᵗʰ element set to
`!operator[](`i`)` for all i in the range of \[`0`, `size()`).

``` cpp
constexpr basic_vec operator~() const noexcept;
```

*Constraints:* `requires (const value_type a) { ~a; }` is `true`.

*Returns:* A `basic_vec` object with the iᵗʰ element set to
`~operator[](`i`)` for all i in the range of \[`0`, `size()`).

``` cpp
constexpr basic_vec operator+() const noexcept;
```

*Constraints:* `requires (const value_type a) { +a; }` is `true`.

*Returns:* `*this`.

``` cpp
constexpr basic_vec operator-() const noexcept;
```

*Constraints:* `requires (const value_type a) { -a; }` is `true`.

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
`-operator[](`i`)` for all i in the range of \[`0`, `size()`).

### `basic_vec` non-member operations <a id="simd.nonmembers">[[simd.nonmembers]]</a>

#### Binary operators <a id="simd.binary">[[simd.binary]]</a>

``` cpp
friend constexpr basic_vec operator+(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator-(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator*(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator/(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator%(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator&(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator|(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator^(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator<<(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec operator>>(const basic_vec& lhs, const basic_vec& rhs) noexcept;
```

Let *op* be the operator.

*Constraints:* `requires (value_type a, value_type b) { a `*`op`*` b; }`
is `true`.

*Returns:* A `basic_vec` object initialized with the results of applying
*op* to `lhs` and `rhs` as a binary element-wise operation.

``` cpp
friend constexpr basic_vec operator<<(const basic_vec& v, simd-size-type n) noexcept;
friend constexpr basic_vec operator>>(const basic_vec& v, simd-size-type n) noexcept;
```

Let *op* be the operator.

*Constraints:*
`requires (value_type a, `*`simd-size-type`*` b) { a `*`op`*` b; }` is
`true`.

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of applying *op* to `v[`i`]` and `n` for all i in the range
of \[`0`, `size()`).

#### Compound assignment <a id="simd.cassign">[[simd.cassign]]</a>

``` cpp
friend constexpr basic_vec& operator+=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator-=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator*=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator/=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator%=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator&=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator|=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator^=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator<<=(basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr basic_vec& operator>>=(basic_vec& lhs, const basic_vec& rhs) noexcept;
```

Let *op* be the operator.

*Constraints:* `requires (value_type a, value_type b) { a `*`op`*` b; }`
is `true`.

*Effects:* These operators apply the indicated operator to `lhs` and
`rhs` as an element-wise operation.

*Returns:* `lhs`.

``` cpp
friend constexpr basic_vec& operator<<=(basic_vec& lhs, simd-size-type n) noexcept;
friend constexpr basic_vec& operator>>=(basic_vec& lhs, simd-size-type n) noexcept;
```

Let *op* be the operator.

*Constraints:*
`requires (value_type a, `*`simd-size-type`*` b) { a `*`op`*` b; }` is
`true`.

*Effects:* Equivalent to:
`return operator `*`op`*` (lhs, basic_vec(n));`

#### Comparison operators <a id="simd.comparison">[[simd.comparison]]</a>

``` cpp
friend constexpr mask_type operator==(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr mask_type operator!=(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr mask_type operator>=(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr mask_type operator<=(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr mask_type operator>(const basic_vec& lhs, const basic_vec& rhs) noexcept;
friend constexpr mask_type operator<(const basic_vec& lhs, const basic_vec& rhs) noexcept;
```

Let *op* be the operator.

*Constraints:* `requires (value_type a, value_type b) { a `*`op`*` b; }`
is `true`.

*Returns:* A `basic_mask` object initialized with the results of
applying *op* to `lhs` and `rhs` as a binary element-wise operation.

#### Exposition-only conditional operators <a id="simd.cond">[[simd.cond]]</a>

``` cpp
friend constexpr basic_vec
simd-select-impl(const mask_type& mask, const basic_vec& a, const basic_vec& b) noexcept;
```

*Returns:* A `basic_vec` object where the iᵗʰ element equals
`mask[`i`] ? a[`i`] : b[`i`]` for all i in the range of \[`0`,
`size()`).

#### Reductions <a id="simd.reductions">[[simd.reductions]]</a>

``` cpp
template<class T, class Abi, class BinaryOperation = plus<>>
  constexpr T reduce(const basic_vec<T, Abi>& x, BinaryOperation binary_op = {});
```

*Constraints:* `BinaryOperation` models `reduction-binary-operation<T>`.

*Preconditions:* `binary_op` does not modify `x`.

*Returns:* *GENERALIZED_SUM*(binary_op, vec\<T, 1\>(x\[0\]), …, vec\<T,
1\>(x\[x.size() - 1\]))\[0\] [[numerics.defns]].

*Throws:* Any exception thrown from `binary_op`.

``` cpp
template<class T, class Abi, class BinaryOperation = plus<>>
  constexpr T reduce(
    const basic_vec<T, Abi>& x, const typename basic_vec<T, Abi>::mask_type& mask,
    BinaryOperation binary_op = {}, type_identity_t<T> identity_element = see below);
```

*Constraints:*

- `BinaryOperation` models `reduction-binary-operation<T>`.
- An argument for `identity_element` is provided for the invocation,
  unless `BinaryOperation` is one of `plus<>`, `multiplies<>`,
  `bit_and<>`, `bit_or<>`, or `bit_xor<>`.

*Preconditions:*

- `binary_op` does not modify `x`.
- For all finite values `y` representable by `T`, the results of
  `y == binary_op(vec<T, 1>(identity_element), vec<T, 1>(y))[0]` and
  `y == binary_op(vec<T, 1>(y), vec<T, 1>(identity_element))[0]` are
  `true`.

*Returns:* If `none_of(mask)` is `true`, returns `identity_element`.
Otherwise, returns *GENERALIZED_SUM*(binary_op, vec\<T, 1\>(x\[k₀\]), …,
vec\<T, 1\>(x\[kₙ\]))\[0\] where k₀, …, kₙ are the selected indices of
`mask`.

*Throws:* Any exception thrown from `binary_op`.

*Remarks:* The default argument for `identity_element` is equal to

- `T()` if `BinaryOperation` is `plus<>`,
- `T(1)` if `BinaryOperation` is `multiplies<>`,
- `T(~T())` if `BinaryOperation` is `bit_and<>`,
- `T()` if `BinaryOperation` is `bit_or<>`, or
- `T()` if `BinaryOperation` is `bit_xor<>`.

``` cpp
template<class T, class Abi> constexpr T reduce_min(const basic_vec<T, Abi>& x) noexcept;
```

*Constraints:* `T` models `totally_ordered`.

*Returns:* The value of an element `x[`j`]` for which `x[`i`] < x[`j`]`
is `false` for all i in the range of \[`0`,
`basic_vec<T, Abi>::size()`).

``` cpp
template<class T, class Abi>
  constexpr T reduce_min(
    const basic_vec<T, Abi>&, const typename basic_vec<T, Abi>::mask_type&) noexcept;
```

*Constraints:* `T` models `totally_ordered`.

*Returns:* If `none_of(mask)` is `true`, returns
`numeric_limits<T>::max()`. Otherwise, returns the value of a selected
element `x[`j`]` for which `x[`i`] < x[`j`]` is `false` for all selected
indices i of `mask`.

``` cpp
template<class T, class Abi> constexpr T reduce_max(const basic_vec<T, Abi>& x) noexcept;
```

*Constraints:* `T` models `totally_ordered`.

*Returns:* The value of an element `x[`j`]` for which `x[`j`] < x[`i`]`
is `false` for all i in the range of \[`0`,
`basic_vec<T, Abi>::size()`).

``` cpp
template<class T, class Abi>
  constexpr T reduce_max(
    const basic_vec<T, Abi>&, const typename basic_vec<T, Abi>::mask_type&) noexcept;
```

*Constraints:* `T` models `totally_ordered`.

*Returns:* If `none_of(mask)` is `true`, returns
`numeric_limits<V::value_type>::lowest()`. Otherwise, returns the value
of a selected element `x[`j`]` for which `x[`j`] < x[`i`]` is `false`
for all selected indices i of `mask`.

#### Load and store functions <a id="simd.loadstore">[[simd.loadstore]]</a>

``` cpp
template<class V = see below, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R>
  constexpr V unchecked_load(R&& r, flags<Flags...> f = {});
template<class V = see below, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R>
  constexpr V unchecked_load(R&& r, const typename V::mask_type& mask, flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, class... Flags>
  constexpr V unchecked_load(I first, iter_difference_t<I> n, flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, class... Flags>
  constexpr V unchecked_load(I first, iter_difference_t<I> n, const typename V::mask_type& mask,
                             flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  constexpr V unchecked_load(I first, S last, flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  constexpr V unchecked_load(I first, S last, const typename V::mask_type& mask,
                             flags<Flags...> f = {});
```

Let

- `mask` be `V::mask_type(true)` for the overloads with no `mask`
  parameter;
- `R` be `span<const iter_value_t<I>>` for the overloads with no
  template parameter `R`;
- `r` be `R(first, n)` for the overloads with an `n` parameter and
  `R(first, last)` for the overloads with a `last` parameter.

*Mandates:* If `ranges::size(r)` is a constant expression then
`ranges::size(r)` ≥ `V::size()`.

*Preconditions:*

- \[`first`, `first + n`) is a valid range for the overloads with an `n`
  parameter.
- \[`first`, `last`) is a valid range for the overloads with a `last`
  parameter.
- `ranges::size(r)` ≥ `V::size()`

*Effects:* Equivalent to: `return partial_load<V>(r, mask, f);`

*Remarks:* The default argument for template parameter `V` is
`basic_vec<ranges::range_value_t<R>>`.

``` cpp
template<class V = see below, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R>
  constexpr V partial_load(R&& r, flags<Flags...> f = {});
template<class V = see below, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R>
  constexpr V partial_load(R&& r, const typename V::mask_type& mask, flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, class... Flags>
  constexpr V partial_load(I first, iter_difference_t<I> n, flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, class... Flags>
  constexpr V partial_load(I first, iter_difference_t<I> n, const typename V::mask_type& mask,
                           flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  constexpr V partial_load(I first, S last, flags<Flags...> f = {});
template<class V = see below, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  constexpr V partial_load(I first, S last, const typename V::mask_type& mask,
                           flags<Flags...> f = {});
```

Let

- `mask` be `V::mask_type(true)` for the overloads with no `mask`
  parameter;
- `R` be `span<const iter_value_t<I>>` for the overloads with no
  template parameter `R`;
- `r` be `R(first, n)` for the overloads with an `n` parameter and
  `R(first, last)` for the overloads with a `last` parameter.

*Mandates:*

- `ranges::range_value_t<R>` is a vectorizable type,
- `same_as<remove_cvref_t<V>, V>` is `true`,
- `V` is an enabled specialization of `basic_vec`, and
- if the template parameter pack `Flags` does not contain
  *`convert-flag`*, then the conversion from `ranges::range_value_t<R>`
  to `V::value_type` is value-preserving.

*Preconditions:*

- \[`first`, `first + n`) is a valid range for the overloads with an `n`
  parameter.
- \[`first`, `last`) is a valid range for the overloads with a `last`
  parameter.
- If the template parameter pack `Flags` contains *`aligned-flag`*,
  `ranges::data(r)` points to storage aligned by
  `alignment_v<V, ranges::range_value_t<R>>`.
- If the template parameter pack `Flags` contains
  *`overaligned-flag`*`<N>`, `ranges::data(r)` points to storage aligned
  by `N`.

*Effects:* Initializes the iᵗʰ element with  
`mask[`i`] && `i` < ranges::size(r) ? static_cast<T>(ranges::data(r)[`i`]) : T()`
for all i in the range of \[`0`, `V::size()`).

*Remarks:* The default argument for template parameter `V` is
`basic_vec<ranges::range_value_t<R>>`.

``` cpp
template<class T, class Abi, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
  constexpr void unchecked_store(const basic_vec<T, Abi>& v, R&& r, flags<Flags...> f = {});
template<class T, class Abi, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
  constexpr void unchecked_store(const basic_vec<T, Abi>& v, R&& r,
    const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first, iter_difference_t<I> n,
                                 flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first, iter_difference_t<I> n,
    const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first, S last,
                                 flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void unchecked_store(const basic_vec<T, Abi>& v, I first, S last,
    const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
```

Let

- `mask` be `basic_vec<T, Abi>::mask_type(true)` for the overloads with
  no `mask` parameter;
- `R` be `span<iter_value_t<I>>` for the overloads with no template
  parameter `R`;
- `r` be `R(first, n)` for the overloads with an `n` parameter and
  `R(first, last)` for the overloads with a `last` parameter.

*Mandates:* If `ranges::size(r)` is a constant expression then
`ranges::size(r)` ≥ *`simd-size-v`*`<T, Abi>`.

*Preconditions:*

- \[`first`, `first + n`) is a valid range for the overloads with an `n`
  parameter.
- \[`first`, `last`) is a valid range for the overloads with a `last`
  parameter.
- `ranges::size(r)` ≥ *`simd-size-v`*`<T, Abi>`

*Effects:* Equivalent to: `partial_store(v, r, mask, f)`.

``` cpp
template<class T, class Abi, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
  constexpr void partial_store(const basic_vec<T, Abi>& v, R&& r, flags<Flags...> f = {});
template<class T, class Abi, ranges::contiguous_range R, class... Flags>
  requires ranges::sized_range<R> && indirectly_writable<ranges::iterator_t<R>, T>
  constexpr void partial_store(const basic_vec<T, Abi>& v, R&& r,
    const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void partial_store(const basic_vec<T, Abi>& v, I first, iter_difference_t<I> n,
                               flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void partial_store(const basic_vec<T, Abi>& v, I first, iter_difference_t<I> n,
    const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void partial_store(const basic_vec<T, Abi>& v, I first, S last,
                               flags<Flags...> f = {});
template<class T, class Abi, contiguous_iterator I, sized_sentinel_for<I> S, class... Flags>
  requires indirectly_writable<I, T>
  constexpr void partial_store(const basic_vec<T, Abi>& v, I first, S last,
    const typename basic_vec<T, Abi>::mask_type& mask, flags<Flags...> f = {});
```

Let

- `mask` be `basic_vec<T, Abi>::mask_type(true)` for the overloads with
  no `mask` parameter;
- `R` be `span<iter_value_t<I>>` for the overloads with no template
  parameter `R`;
- `r` be `R(first, n)` for the overloads with an `n` parameter and
  `R(first, last)` for the overloads with a `last` parameter.

*Mandates:*

- `ranges::range_value_t<R>` is a vectorizable type, and
- if the template parameter pack `Flags` does not contain
  *`convert-flag`*, then the conversion from `T` to
  `ranges::range_value_t<R>` is value-preserving.

*Preconditions:*

- \[`first`, `first + n`) is a valid range for the overloads with an `n`
  parameter.
- \[`first`, `last`) is a valid range for the overloads with a `last`
  parameter.
- If the template parameter pack `Flags` contains *`aligned-flag`*,
  `ranges::data(r)` points to storage aligned by
  `alignment_v<basic_vec<T, Abi>, ranges::range_value_t<R>>`.
- If the template parameter pack `Flags` contains
  *`overaligned-flag`*`<N>`, `ranges::data(r)` points to storage aligned
  by `N`.

*Effects:* For all i in the range of \[`0`,
`basic_vec<T, Abi>::size()`), if `mask[`i`] && `i` < ranges::size(r)` is
`true`, evaluates `ranges::data(r)[`i`] = v[`i`]`.

#### Static permute <a id="simd.permute.static">[[simd.permute.static]]</a>

``` cpp
template<simd-size-type N = see below, simd-vec-type V, class IdxMap>
  constexpr resize_t<N, V> permute(const V& v, IdxMap&& idxmap);
template<simd-size-type N = see below, simd-mask-type M, class IdxMap>
  constexpr resize_t<N, M> permute(const M& v, IdxMap&& idxmap);
```

Let:

- *`gen-fn`*`(i)` be `idxmap(i, V::size())` if that expression is
  well-formed, and `idxmap(i)` otherwise.
- *perm-fn* be the following exposition-only function template:
  ``` cpp
  template<simd-size-type I>
  typename V::value_type perm-fn() {
    constexpr auto src_index = gen-fn(I);
    if constexpr (src_index == zero_element) {
      return typename V::value_type();
    } else if constexpr (src_index == uninit_element) {
      return unspecified-value;
    } else {
      return v[src_index];
    }
  }
  ```

*Constraints:* At least one of
`invoke_result_t<IdxMap&, `*`simd-size-type`*`>` and
`invoke_result_t<IdxMap&, `*`simd-size-type`*`, `*`simd-size-type`*`>`
satisfies `integral`.

*Mandates:* *`gen-fn`*`(`i`)` is a constant expression whose value is
`zero_element`, `uninit_element`, or in the range \[`0`, `V::size()`),
for all i in the range \[`0`, `N`).

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to the result of *`perm-fn`*`<`i`>()` for all i in the range \[`0`,
`N`).

*Remarks:* The default argument for template parameter `N` is
`V::size()`.

#### Dynamic permute <a id="simd.permute.dynamic">[[simd.permute.dynamic]]</a>

``` cpp
template<simd-vec-type V, simd-integral I>
  constexpr resize_t<I::size(), V> permute(const V& v, const I& indices);
template<simd-mask-type M, simd-integral I>
  constexpr resize_t<I::size(), M> permute(const M& v, const I& indices);
```

*Preconditions:* All values in `indices` are in the range \[`0`,
`V::size()`).

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to the result of `v[indices[`i`]]` for all i in the range \[`0`,
`I::size()`).

#### Mask permute <a id="simd.permute.mask">[[simd.permute.mask]]</a>

``` cpp
template<simd-vec-type V>
  constexpr V compress(const V& v, const typename V::mask_type& selector);
template<simd-mask-type M>
  constexpr M compress(const M& v, const type_identity_t<M>& selector);
```

Let:

- *`bit-index`*`(`i`)` be a function which returns the index of the iᵗʰ
  element of `selector` that is `true`.
- *`select-value`*`(`i`)` be a function which returns
  `v[`*`bit-index`*`(`i`)]` for i in the range \[`0`,
  `reduce_count(selector)`) and a valid but unspecified value otherwise.
  \[*Note 3*: Different calls to *select-value* can return different
  unspecified values. — *end note*]

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to the result of *`select-value`*`(`i`)` for all i in the range \[`0`,
`V::size()`).

``` cpp
template<simd-vec-type V>
  constexpr V compress(const V& v, const typename V::mask_type& selector,
                       const typename V::value_type& fill_value);
template<simd-mask-type M>
  constexpr M compress(const M& v, const type_identity_t<M>& selector,
                       const typename M::value_type& fill_value);
```

Let:

- *`bit-index`*`(`i`)` be a function which returns the index of the iᵗʰ
  element of `selector` that is `true`.
- *`select-value`*`(`i`)` be a function which returns
  `v[`*`bit-index`*`(`i`)]` for i in the range \[`0`,
  `reduce_count(selector)`) and `fill_value` otherwise.

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to the result of *`select-value`*`(`i`)` for all i in the range \[`0`,
`V::size()`).

``` cpp
template<simd-vec-type V>
  constexpr V expand(const V& v, const typename V::mask_type& selector, const V& original = {});
template<simd-mask-type M>
  constexpr M expand(const M& v, const type_identity_t<M>& selector, const M& original = {});
```

Let:

- *set-indices* be a list of the index positions of `true` elements in
  `selector`, in ascending order.
- *`bit-lookup`*`(`b`)` be a function which returns the index where b
  appears in *`set-indices`*.
- *`select-value`*`(`i`)` be a function which returns
  `v[`*`bit-lookup`*`(`i`)]` if `selector[`i`]` is `true`, otherwise
  returns `original[`i`]`.

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to the result of *`select-value`*`(`i`)` for all i in the range \[`0`,
`V::size()`).

#### Memory permute <a id="simd.permute.memory">[[simd.permute.memory]]</a>

``` cpp
template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr V unchecked_gather_from(R&& in, const I& indices, flags<Flags...> f = {});
template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr V unchecked_gather_from(R&& in, const typename I::mask_type& mask,
                                    const I& indices, flags<Flags...> f = {});
```

Let `mask` be `typename I::mask_type(true)` for the overload with no
`mask` parameter.

*Preconditions:* All values in
`select(mask, indices, typename I::value_type())` are in the range
\[`0`, `ranges::size(in)`).

*Effects:* Equivalent to:
`return partial_gather_from<V>(in, mask, indices, f);`

*Remarks:* The default argument for template parameter `V` is
`vec<ranges::range_value_t<R>, I::size()>`.

``` cpp
template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr V partial_gather_from(R&& in, const I& indices, flags<Flags...> f = {});
template<class V = see below, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr V partial_gather_from(R&& in, const typename I::mask_type& mask,
                                  const I& indices, flags<Flags...> f = {});
```

Let:

- `mask` be `typename I::mask_type(true)` for the overload with no
  `mask` parameter;
- `T` be `typename V::value_type`.

*Mandates:*

- `ranges::range_value_t<R>` is a vectorizable type,
- `same_as<remove_cvref_t<V>, V>` is `true`,
- `V` is an enabled specialization of `basic_vec`,
- `V::size() == I::size()` is `true`, and
- if the template parameter pack `Flags` does not contain
  *convert-flag*, then the conversion from `ranges::range_value_t<R>` to
  `T` is value-preserving.

*Preconditions:*

- If the template parameter pack `Flags` contains *aligned-flag*,
  `ranges::data(in)` points to storage aligned by
  `alignment_v<V, ranges::range_value_t<R>>`.
- If the template parameter pack `Flags` contains
  *`overaligned-flag`*`<N>`, `ranges::data(in)` points to storage
  aligned by `N`.

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of

``` cpp
mask[i] && indices[i] < ranges::size(in) ? static_cast<T>(ranges::data(in)[indices[i]]) : T()
```

for all i in the range \[`0`, `I::size()`).

*Remarks:* The default argument for template parameter `V` is
`vec<ranges::range_value_t<R>, I::size()>`.

``` cpp
template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr void unchecked_scatter_to(const V& v, R&& out, const I& indices,
                                      flags<Flags...> f = {});
template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr void unchecked_scatter_to(const V& v, R&& out, const typename I::mask_type& mask,
                                      const I& indices, flags<Flags...> f = {});
```

Let `mask` be `typename I::mask_type(true)` for the overload with no
`mask` parameter.

*Preconditions:* All values in
`select(mask, indices, typename I::value_type())` are in the range
\[`0`, `ranges::size(out)`).

*Effects:* Equivalent to:
`partial_scatter_to(v, out, mask, indices, f);`

``` cpp
template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr void
  partial_scatter_to(const V& v, R&& out, const I& indices, flags<Flags...> f = {});
template<simd-vec-type V, ranges::contiguous_range R, simd-integral I, class... Flags>
  requires ranges::sized_range<R>
  constexpr void partial_scatter_to(const V& v, R&& out, const typename I::mask_type& mask,
                                    const I& indices, flags<Flags...> f = {});
```

Let `mask` be `typename I::mask_type(true)` for the overload with no
`mask` parameter.

*Constraints:* `V::size() == I::size()` is `true`.

*Mandates:*

- `ranges::range_value_t<R>` is a vectorizable type, and
- if the template parameter pack `Flags` does not contain
  *convert-flag*, then the conversion from `typename V::value_type` to
  `ranges::range_value_t<R>` is value-preserving.

*Preconditions:*

- For all selected indices i the values `indices[`i`]` are unique.
- If the template parameter pack `Flags` contains *aligned-flag*,
  `ranges::data(out)` points to storage aligned by
  `alignment_v<V, ranges::range_value_t<R>>`.
- If the template parameter pack `Flags` contains
  *`overaligned-flag`*`<N>`, `ranges::data(out)` points to storage
  aligned by `N`.

*Effects:* For all i in the range \[`0`, `I::size()`), if
`mask[`i`] && (indices[`i`] < ranges::size(out))` is `true`, evaluates
`ranges::data(out)[indices[`i`]] = v[`i`]`.

#### Creation <a id="simd.creation">[[simd.creation]]</a>

``` cpp
template<class T, class Abi>
  constexpr auto chunk(const basic_vec<typename T::value_type, Abi>& x) noexcept;
template<class T, class Abi>
  constexpr auto chunk(const basic_mask<mask-element-size<T>, Abi>& x) noexcept;
```

*Constraints:*

- For the first overload, `T` is an enabled specialization of
  `basic_vec`. If
  `basic_vec<typename T::value_type, Abi>::size() % T::size()` is not
  `0`, then
  `resize_t<basic_vec<typename T::value_type, Abi>::size() % T::size(), T>`
  is valid and denotes a type.
- For the second overload, `T` is an enabled specialization of
  `basic_mask`. If
  `basic_mask<`*`mask-element-size`*`<T>, Abi>::size() % T::size()` is
  not `0`, then
  `resize_t<basic_mask<`*`mask-element-size`*`<T>, Abi>::size() % T::size(), T>`
  is valid and denotes a type.

Let N be `x.size() / T::size()`.

*Returns:*

- If `x.size() % T::size() == 0` is `true`, an `array<T, `N`>` with the
  iᵗʰ `basic_vec` or `basic_mask` element of the jᵗʰ `array` element
  initialized to the value of the element in `x` with index
  i` + `j` * T::size()`.
- Otherwise, a `tuple` of N objects of type `T` and one object of type
  `resize_t<x.size() % T::size(), T>`. The iᵗʰ `basic_vec` or
  `basic_mask` element of the jᵗʰ `tuple` element of type `T` is
  initialized to the value of the element in `x` with index
  i` + `j` * T::size()`. The iᵗʰ `basic_vec` or `basic_mask` element of
  the Nᵗʰ `tuple` element is initialized to the value of the element in
  `x` with index i` + `N` * T::size()`.

``` cpp
template<simd-size-type N, class T, class Abi>
  constexpr auto chunk(const basic_vec<T, Abi>& x) noexcept;
```

*Effects:* Equivalent to:
`return chunk<resize_t<N, basic_vec<T, Abi>>>(x);`

``` cpp
template<simd-size-type N, size_t Bytes, class Abi>
  constexpr auto chunk(const basic_mask<Bytes, Abi>& x) noexcept;
```

*Effects:* Equivalent to:
`return chunk<resize_t<N, basic_mask<Bytes, Abi>>>(x);`

``` cpp
template<class T, class... Abis>
  constexpr vec<T, (basic_vec<T, Abis>::size() + ...)>
    cat(const basic_vec<T, Abis>&... xs) noexcept;
template<size_t Bytes, class... Abis>
  constexpr basic_mask<Bytes, deduce-abi-t<integer-from<Bytes>,
                            (basic_mask<Bytes, Abis>::size() + ...)>>
    cat(const basic_mask<Bytes, Abis>&... xs) noexcept;
```

*Constraints:*

- For the first overload `vec<T, (basic_vec<T, Abis>::size() + ...)>` is
  enabled.
- For the second overload
  `basic_mask<Bytes, `*`deduce-abi-t`*`<`*`integer-from`*`<Bytes>, (basic_mask<Bytes, Abis>::size() + ...)>>`
  is enabled.

*Returns:* A data-parallel object initialized with the concatenated
values in the `xs` pack of data-parallel objects: The iᵗʰ
`basic_vec`/`basic_mask` element of the jᵗʰ parameter in the `xs` pack
is copied to the return value’s element with index i + the sum of the
width of the first j parameters in the `xs` pack.

#### Algorithms <a id="simd.alg">[[simd.alg]]</a>

``` cpp
template<class T, class Abi>
  constexpr basic_vec<T, Abi> min(const basic_vec<T, Abi>& a,
                                  const basic_vec<T, Abi>& b) noexcept;
```

*Constraints:* `T` models `totally_ordered`.

*Returns:* The result of the element-wise application of
`min(a[`i`], b[`i`])` for all i in the range of \[`0`,
`basic_vec<T, Abi>::size()`).

``` cpp
template<class T, class Abi>
  constexpr basic_vec<T, Abi> max(const basic_vec<T, Abi>& a,
                                  const basic_vec<T, Abi>& b) noexcept;
```

*Constraints:* `T` models `totally_ordered`.

*Returns:* The result of the element-wise application of
`max(a[`i`], b[`i`])` for all i in the range of \[`0`,
`basic_vec<T, Abi>::size()`).

``` cpp
template<class T, class Abi>
  constexpr pair<basic_vec<T, Abi>, basic_vec<T, Abi>>
    minmax(const basic_vec<T, Abi>& a, const basic_vec<T, Abi>& b) noexcept;
```

*Effects:* Equivalent to: `return pair{min(a, b), max(a, b)};`

``` cpp
template<class T, class Abi>
  constexpr basic_vec<T, Abi> clamp(
    const basic_vec<T, Abi>& v, const basic_vec<T, Abi>& lo, const basic_vec<T, Abi>& hi);
```

*Constraints:* `T` models `totally_ordered`.

*Preconditions:* No element in `lo` is greater than the corresponding
element in `hi`.

*Returns:* The result of element-wise application of
`clamp(v[`i`], lo[`i`], hi[`i`])` for all i in the range of \[`0`,
`basic_vec<T, Abi>::size()`).

``` cpp
template<class T, class U>
  constexpr auto select(bool c, const T& a, const U& b)
  -> remove_cvref_t<decltype(c ? a : b)>;
```

*Effects:* Equivalent to: `return c ? a : b;`

``` cpp
template<size_t Bytes, class Abi, class T, class U>
  constexpr auto select(const basic_mask<Bytes, Abi>& c, const T& a, const U& b)
  noexcept -> decltype(simd-select-impl(c, a, b));
```

*Effects:* Equivalent to:

``` cpp
return simd-select-impl(c, a, b);
```

where *`simd-select-impl`* is found by argument-dependent
lookup [[basic.lookup.argdep]] contrary to [[contents]].

#### Mathematical functions <a id="simd.math">[[simd.math]]</a>

``` cpp
template<math-floating-point V>
  constexpr rebind_t<int, deduced-vec-t<V>> ilogb(const V& x);
template<math-floating-point V>
  constexpr deduced-vec-t<V> ldexp(const V& x, const rebind_t<int, deduced-vec-t<V>>& exp);
template<math-floating-point V>
  constexpr deduced-vec-t<V> scalbn(const V& x, const rebind_t<int, deduced-vec-t<V>>& n);
template<math-floating-point V>
  constexpr deduced-vec-t<V>
    scalbln(const V& x, const rebind_t<long int, deduced-vec-t<V>>& n);
template<signed_integral T, class Abi>
  constexpr basic_vec<T, Abi> abs(const basic_vec<T, Abi>& j);
template<math-floating-point V>
  constexpr deduced-vec-t<V> abs(const V& j);
template<math-floating-point V>
  constexpr deduced-vec-t<V> fabs(const V& x);
template<math-floating-point V>
  constexpr deduced-vec-t<V> ceil(const V& x);
template<math-floating-point V>
  constexpr deduced-vec-t<V> floor(const V& x);
template<math-floating-point V>
  deduced-vec-t<V> nearbyint(const V& x);
template<math-floating-point V>
  deduced-vec-t<V> rint(const V& x);
template<math-floating-point V>
  rebind_t<long int, deduced-vec-t<V>> lrint(const V& x);
template<math-floating-point V>
  rebind_t<long long int, deduced-vec-t<V>> llrint(const V& x);
template<math-floating-point V>
  constexpr deduced-vec-t<V> round(const V& x);
template<math-floating-point V>
  constexpr rebind_t<long int, deduced-vec-t<V>> lround(const V& x);
template<math-floating-point V>
  constexpr rebind_t<long long int, deduced-vec-t<V>> llround(const V& x);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> fmod(const V0& x, const V1& y);
template<math-floating-point V>
  constexpr deduced-vec-t<V> trunc(const V& x);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> remainder(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> copysign(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> nextafter(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> fdim(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> fmax(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> fmin(const V0& x, const V1& y);
template<class V0, class V1, class V2>
  constexpr math-common-simd-t<V0, V1, V2> fma(const V0& x, const V1& y, const V2& z);
template<math-floating-point V>
  constexpr rebind_t<int, deduced-vec-t<V>> fpclassify(const V& x);
template<math-floating-point V>
  constexpr typename deduced-vec-t<V>::mask_type isfinite(const V& x);
template<math-floating-point V>
  constexpr typename deduced-vec-t<V>::mask_type isinf(const V& x);
template<math-floating-point V>
  constexpr typename deduced-vec-t<V>::mask_type isnan(const V& x);
template<math-floating-point V>
  constexpr typename deduced-vec-t<V>::mask_type isnormal(const V& x);
template<math-floating-point V>
  constexpr typename deduced-vec-t<V>::mask_type signbit(const V& x);
template<class V0, class V1>
  constexpr typename math-common-simd-t<V0, V1>::mask_type isgreater(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr typename math-common-simd-t<V0, V1>::mask_type
    isgreaterequal(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr typename math-common-simd-t<V0, V1>::mask_type isless(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr typename math-common-simd-t<V0, V1>::mask_type islessequal(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr typename math-common-simd-t<V0, V1>::mask_type islessgreater(const V0& x, const V1& y);
template<class V0, class V1>
  constexpr typename math-common-simd-t<V0, V1>::mask_type isunordered(const V0& x, const V1& y);
```

Let `Ret` denote the return type of the specialization of a function
template with the name *`math-func`*. Let *`math-func-vec`* denote:

``` cpp
template<class... Args>
Ret math-func-vec(Args... args) {
  return Ret([&](simd-size-type i) {
    return math-func(make-compatible-simd-t<Ret, Args>(args)[i]...);
  });
}
```

*Returns:* A value `ret` of type `Ret`, that is element-wise equal to
the result of calling *`math-func-vec`* with the arguments of the above
functions. If in an invocation of a scalar overload of *`math-func`* for
index `i` in *`math-func-vec`* a domain, pole, or range error would
occur, the value of `ret[i]` is unspecified.

*Remarks:* It is unspecified whether `errno`[[errno]] is accessed.

``` cpp
template<math-floating-point V> constexpr deduced-vec-t<V> acos(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> asin(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> atan(const V& x);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> atan2(const V0& y, const V1& x);
template<math-floating-point V> constexpr deduced-vec-t<V> cos(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> sin(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> tan(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> acosh(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> asinh(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> atanh(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> cosh(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> sinh(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> tanh(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> exp(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> exp2(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> expm1(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> log(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> log10(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> log1p(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> log2(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> logb(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> cbrt(const V& x);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> hypot(const V0& x, const V1& y);
template<class V0, class V1, class V2>
  constexpr math-common-simd-t<V0, V1, V2> hypot(const V0& x, const V1& y, const V2& z);
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> pow(const V0& x, const V1& y);
template<math-floating-point V> constexpr deduced-vec-t<V> sqrt(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> erf(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> erfc(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> lgamma(const V& x);
template<math-floating-point V> constexpr deduced-vec-t<V> tgamma(const V& x);
template<class V0, class V1, class V2>
  constexpr math-common-simd-t<V0, V1, V2> lerp(const V0& a, const V1& b, const V2& t) noexcept;
template<math-floating-point V>
  deduced-vec-t<V> assoc_laguerre(const rebind_t<unsigned, deduced-vec-t<V>>& n, const
    rebind_t<unsigned, deduced-vec-t<V>>& m, const V& x);
template<math-floating-point V>
  deduced-vec-t<V> assoc_legendre(const rebind_t<unsigned, deduced-vec-t<V>>& l, const
    rebind_t<unsigned, deduced-vec-t<V>>& m, const V& x);
template<class V0, class V1>
  math-common-simd-t<V0, V1> beta(const V0& x, const V1& y);
template<math-floating-point V> deduced-vec-t<V> comp_ellint_1(const V& k);
template<math-floating-point V> deduced-vec-t<V> comp_ellint_2(const V& k);
template<class V0, class V1>
  math-common-simd-t<V0, V1> comp_ellint_3(const V0& k, const V1& nu);
template<class V0, class V1>
  math-common-simd-t<V0, V1> cyl_bessel_i(const V0& nu, const V1& x);
template<class V0, class V1>
  math-common-simd-t<V0, V1> cyl_bessel_j(const V0& nu, const V1& x);
template<class V0, class V1>
  math-common-simd-t<V0, V1> cyl_bessel_k(const V0& nu, const V1& x);
template<class V0, class V1>
  math-common-simd-t<V0, V1> cyl_neumann(const V0& nu, const V1& x);
template<class V0, class V1>
  math-common-simd-t<V0, V1> ellint_1(const V0& k, const V1& phi);
template<class V0, class V1>
  math-common-simd-t<V0, V1> ellint_2(const V0& k, const V1& phi);
template<class V0, class V1, class V2>
  math-common-simd-t<V0, V1, V2> ellint_3(const V0& k, const V1& nu, const V2& phi);
template<math-floating-point V> deduced-vec-t<V> expint(const V& x);
template<math-floating-point V> deduced-vec-t<V> hermite(const rebind_t<unsigned,
deduced-vec-t<V>>& n, const V& x);
template<math-floating-point V> deduced-vec-t<V> laguerre(const rebind_t<unsigned,
deduced-vec-t<V>>& n, const V& x);
template<math-floating-point V> deduced-vec-t<V> legendre(const rebind_t<unsigned,
deduced-vec-t<V>>& l, const V& x);
template<math-floating-point V> deduced-vec-t<V> riemann_zeta(const V& x);
template<math-floating-point V> deduced-vec-t<V> sph_bessel(const rebind_t<unsigned,
deduced-vec-t<V>>& n, const V& x);
template<math-floating-point V>
  deduced-vec-t<V> sph_legendre(const rebind_t<unsigned, deduced-vec-t<V>>& l,
                                 const rebind_t<unsigned, deduced-vec-t<V>>& m,
                                 const V& theta);
template<math-floating-point V> deduced-vec-t<V> sph_neumann(const rebind_t<unsigned,
deduced-vec-t<V>>& n, const V& x);
```

Let `Ret` denote the return type of the specialization of a function
template with the name *`math-func`*. Let *`math-func-vec`* denote:

``` cpp
template<class... Args>
Ret math-func-vec(Args... args) {
  return Ret([&](simd-size-type i) {
    return math-func(make-compatible-simd-t<Ret, Args>(args)[i]...);
  });
}
```

*Returns:* A value `ret` of type `Ret`, that is element-wise
approximately equal to the result of calling *`math-func-vec`* with the
arguments of the above functions. If in an invocation of a scalar
overload of *`math-func`* for index `i` in *`math-func-vec`* a domain,
pole, or range error would occur, the value of `ret[i]` is unspecified.

*Remarks:* It is unspecified whether `errno`[[errno]] is accessed.

``` cpp
template<math-floating-point V>
  constexpr deduced-vec-t<V> frexp(const V& value, rebind_t<int, deduced-vec-t<V>>* exp);
```

Let `Ret` be *`deduced-vec-t`*`<V>`. Let *`frexp-vec`* denote:

``` cpp
template<class V>
pair<Ret, rebind_t<int, Ret>> frexp-vec(const V& x) {
  int r1[Ret::size()];
  Ret r0([&](simd-size-type i) {
    return frexp(make-compatible-simd-t<Ret, V>(x)[i], &r1[i]);
  });
  return {r0, rebind_t<int, Ret>(r1)};
}
```

Let `ret` be a value of type `pair<Ret, rebind_t<int, Ret>>` that is the
same value as the result of calling *`frexp-vec`*`(x)`.

*Effects:* Sets `*exp` to `ret.second`.

*Returns:* `ret.first`.

``` cpp
template<class V0, class V1>
  constexpr math-common-simd-t<V0, V1> remquo(const V0& x, const V1& y,
                                              rebind_t<int, math-common-simd-t<V0, V1>>* quo);
```

Let `Ret` be *`math-common-simd-t`*`<V0, V1>`. Let *`remquo-vec`*
denote:

``` cpp
template<class V0, class V1>
pair<Ret, rebind_t<int, Ret>> remquo-vec(const V0& x, const V1& y) {
  int r1[Ret::size()];
  Ret r0([&](simd-size-type i) {
    return remquo(make-compatible-simd-t<Ret, V0>(x)[i],
                  make-compatible-simd-t<Ret, V1>(y)[i], &r1[i]);
  });
  return {r0, rebind_t<int, Ret>(r1)};
}
```

Let `ret` be a value of type `pair<Ret, rebind_t<int, Ret>>` that is the
same value as the result of calling *`remquo-vec`*`(x, y)`. If in an
invocation of a scalar overload of `remquo` for index `i` in
*`remquo-vec`* a domain, pole, or range error would occur, the value of
`ret[i]` is unspecified.

*Effects:* Sets `*quo` to `ret.second`.

*Returns:* `ret.first`.

*Remarks:* It is unspecified whether `errno`[[errno]] is accessed.

``` cpp
template<class T, class Abi>
  constexpr basic_vec<T, Abi> modf(const type_identity_t<basic_vec<T, Abi>>& value,
                                   basic_vec<T, Abi>* iptr);
```

Let `V` be `basic_vec<T, Abi>`. Let *`modf-vec`* denote:

``` cpp
pair<V, V> modf-vec(const V& x) {
  T r1[Ret::size()];
  V r0([&](simd-size-type i) {
    return modf(V(x)[i], &r1[i]);
  });
  return {r0, V(r1)};
}
```

Let `ret` be a value of type `pair<V, V>` that is the same value as the
result of calling *`modf-vec`*`(value)`.

*Effects:* Sets `*iptr` to `ret.second`.

*Returns:* `ret.first`.

#### Bit manipulation <a id="simd.bit">[[simd.bit]]</a>

``` cpp
template<simd-vec-type V> constexpr V byteswap(const V& v) noexcept;
```

*Constraints:* The type `V::value_type` models `integral`.

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of `std::byteswap(v[`i`])` for all i in the range \[`0`,
`V::size()`).

``` cpp
template<simd-vec-type V> constexpr V bit_ceil(const V& v) noexcept;
```

*Constraints:* The type `V::value_type` is an unsigned integer
type [[basic.fundamental]].

*Preconditions:* For every i in the range \[`0`, `V::size()`), the
smallest power of 2 greater than or equal to `v[`i`]` is representable
as a value of type `V::value_type`.

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of `std::bit_ceil(v[`i`])` for all i in the range \[`0`,
`V::size()`).

*Remarks:* A function call expression that violates the precondition in
the *Preconditions:* element is not a core constant
expression [[expr.const]].

``` cpp
template<simd-vec-type V> constexpr V bit_floor(const V& v) noexcept;
```

*Constraints:* The type `V::value_type` is an unsigned integer
type [[basic.fundamental]].

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of `std::bit_floor(v[`i`])` for all i in the range \[`0`,
`V::size()`).

``` cpp
template<simd-vec-type V>
  constexpr typename V::mask_type has_single_bit(const V& v) noexcept;
```

*Constraints:* The type `V::value_type` is an unsigned integer
type [[basic.fundamental]].

*Returns:* A `basic_mask` object where the iᵗʰ element is initialized to
the result of `std::has_single_bit(v[`i`])` for all i in the range
\[`0`, `V::size()`).

``` cpp
template<simd-vec-type V0, simd-vec-type V1>
  constexpr V0 rotl(const V0& v0, const V1& v1) noexcept;
template<simd-vec-type V0, simd-vec-type V1>
  constexpr V0 rotr(const V0& v0, const V1& v1) noexcept;
```

*Constraints:*

- The type `V0::value_type` is an unsigned integer
  type [[basic.fundamental]],
- the type `V1::value_type` models `integral`,
- `V0::size() == V1::size()` is `true`, and
- `sizeof(typename V0::value_type) == sizeof(typename V1::value_type)`
  is `true`.

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of *`bit-func`*`(v0[`i`], static_cast<int>(v1[`i`]))` for all
i in the range \[`0`, `V0::size()`), where *`bit-func`* is the
corresponding scalar function from `<bit>`.

``` cpp
template<simd-vec-type V> constexpr V rotl(const V& v, int s) noexcept;
template<simd-vec-type V> constexpr V rotr(const V& v, int s) noexcept;
```

*Constraints:* The type `V::value_type` is an unsigned integer
type [[basic.fundamental]].

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of *`bit-func`*`(v[`i`], s)` for all i in the range \[`0`,
`V::size()`), where *`bit-func`* is the corresponding scalar function
from `<bit>`.

``` cpp
template<simd-vec-type V>
  constexpr rebind_t<make_signed_t<typename V::value_type>, V> bit_width(const V& v) noexcept;
template<simd-vec-type V>
  constexpr rebind_t<make_signed_t<typename V::value_type>, V> countl_zero(const V& v) noexcept;
template<simd-vec-type V>
  constexpr rebind_t<make_signed_t<typename V::value_type>, V> countl_one(const V& v) noexcept;
template<simd-vec-type V>
  constexpr rebind_t<make_signed_t<typename V::value_type>, V> countr_zero(const V& v) noexcept;
template<simd-vec-type V>
  constexpr rebind_t<make_signed_t<typename V::value_type>, V> countr_one(const V& v) noexcept;
template<simd-vec-type V>
  constexpr rebind_t<make_signed_t<typename V::value_type>, V> popcount(const V& v) noexcept;
```

*Constraints:* The type `V::value_type` is an unsigned integer
type [[basic.fundamental]].

*Returns:* A `basic_vec` object where the iᵗʰ element is initialized to
the result of *`bit-func`*`(v[`i`])` for all i in the range \[`0`,
`V::size()`), where *`bit-func`* is the corresponding scalar function
from `<bit>`.

#### Complex math <a id="simd.complex.math">[[simd.complex.math]]</a>

``` cpp
template<simd-complex V>
  constexpr rebind_t<simd-complex-value-type<V>, V> real(const V&) noexcept;
template<simd-complex V>
  constexpr rebind_t<simd-complex-value-type<V>, V> imag(const V&) noexcept;

template<simd-complex V>
  constexpr rebind_t<simd-complex-value-type<V>, V> abs(const V&);
template<simd-complex V>
  constexpr rebind_t<simd-complex-value-type<V>, V> arg(const V&);
template<simd-complex V>
  constexpr rebind_t<simd-complex-value-type<V>, V> norm(const V&);
template<simd-complex V> constexpr V conj(const V&);
template<simd-complex V> constexpr V proj(const V&);

template<simd-complex V> constexpr V exp(const V& v);
template<simd-complex V> constexpr V log(const V& v);
template<simd-complex V> constexpr V log10(const V& v);

template<simd-complex V> constexpr V sqrt(const V& v);
template<simd-complex V> constexpr V sin(const V& v);
template<simd-complex V> constexpr V asin(const V& v);
template<simd-complex V> constexpr V cos(const V& v);
template<simd-complex V> constexpr V acos(const V& v);
template<simd-complex V> constexpr V tan(const V& v);
template<simd-complex V> constexpr V atan(const V& v);
template<simd-complex V> constexpr V sinh(const V& v);
template<simd-complex V> constexpr V asinh(const V& v);
template<simd-complex V> constexpr V cosh(const V& v);
template<simd-complex V> constexpr V acosh(const V& v);
template<simd-complex V> constexpr V tanh(const V& v);
template<simd-complex V> constexpr V atanh(const V& v);
```

*Returns:* A `basic_vec` object `ret` where the iᵗʰ element is
initialized to the result of *`cmplx-func`*`(v[`i`])` for all i in the
range \[`0`, `V::size()`), where *`cmplx-func`* is the corresponding
function from `<complex>`. If in an invocation of *`cmplx-func`* for
index i a domain, pole, or range error would occur, the value of
`ret[`i`]` is unspecified.

*Remarks:* It is unspecified whether `errno`[[errno]] is accessed.

``` cpp
template<simd-floating-point V>
  rebind_t<complex<typename V::value_type>, V> polar(const V& x, const V& y = {});

template<simd-complex V> constexpr V pow(const V& x, const V& y);
```

*Returns:* A `basic_vec` object `ret` where the iᵗʰ element is
initialized to the result of *`cmplx-func`*`(x[`i`], y[`i`])` for all i
in the range \[`0`, `V::size()`), where *`cmplx-func`* is the
corresponding function from `<complex>`. If in an invocation of
*`cmplx-func`* for index i a domain, pole, or range error would occur,
the value of `ret[`i`]` is unspecified.

*Remarks:* It is unspecified whether `errno`[[errno]] is accessed.

### Class template `basic_mask` <a id="simd.mask.class">[[simd.mask.class]]</a>

#### Overview <a id="simd.mask.overview">[[simd.mask.overview]]</a>

``` cpp
namespace std::simd {
  template<size_t Bytes, class Abi> class basic_mask {
  public:
    using value_type = bool;
    using abi_type = Abi;
    using iterator = simd-iterator<basic_mask>;
    using const_iterator = simd-iterator<const basic_mask>;

    constexpr iterator begin() noexcept { return {*this, 0}; }
    constexpr const_iterator begin() const noexcept { return {*this, 0}; }
    constexpr const_iterator cbegin() const noexcept { return {*this, 0}; }
    constexpr default_sentinel_t end() const noexcept { return {}; }
    constexpr default_sentinel_t cend() const noexcept { return {}; }

    static constexpr integral_constant<simd-size-type, simd-size-v<integer-from<Bytes>, Abi>>
      size {};

    constexpr basic_mask() noexcept = default;

    // [simd.mask.ctor], basic_mask constructors
    constexpr explicit basic_mask(value_type) noexcept;
    template<size_t UBytes, class UAbi>
      constexpr explicit basic_mask(const basic_mask<UBytes, UAbi>&) noexcept;
    template<class G>
      constexpr explicit basic_mask(G&& gen);
    constexpr basic_mask(const bitset<size()>& b) noexcept;
    constexpr explicit basic_mask(unsigned_integral auto val) noexcept;

    // [simd.mask.subscr], basic_mask subscript operators
    constexpr value_type operator[](simd-size-type) const;
    template<simd-integral I>
      constexpr resize_t<I::size(), basic_mask> operator[](const I& indices) const;

    // [simd.mask.unary], basic_mask unary operators
    constexpr basic_mask operator!() const noexcept;
    constexpr basic_vec<integer-from<Bytes>, Abi> operator+() const noexcept;
    constexpr basic_vec<integer-from<Bytes>, Abi> operator-() const noexcept;
    constexpr basic_vec<integer-from<Bytes>, Abi> operator~() const noexcept;

    // [simd.mask.conv], basic_mask conversions
    template<class U, class A>
      constexpr explicit(sizeof(U) != Bytes) operator basic_vec<U, A>() const noexcept;
    constexpr bitset<size()> to_bitset() const noexcept;
    constexpr unsigned long long to_ullong() const;

    // [simd.mask.binary], basic_mask binary operators
    friend constexpr basic_mask
      operator&&(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator||(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator&(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator|(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator^(const basic_mask&, const basic_mask&) noexcept;

    // [simd.mask.cassign], basic_mask compound assignment
    friend constexpr basic_mask&
      operator&=(basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask&
      operator|=(basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask&
      operator^=(basic_mask&, const basic_mask&) noexcept;

    // [simd.mask.comparison], basic_mask comparisons
    friend constexpr basic_mask
      operator==(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator!=(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator>=(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator<=(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator>(const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask
      operator<(const basic_mask&, const basic_mask&) noexcept;

    // [simd.mask.cond], basic_mask exposition only conditional operators
    friend constexpr basic_mask simd-select-impl( // exposition only
      const basic_mask&, const basic_mask&, const basic_mask&) noexcept;
    friend constexpr basic_mask simd-select-impl( // exposition only
      const basic_mask&, same_as<bool> auto, same_as<bool> auto) noexcept;
    template<class T0, class T1>
      friend constexpr vec<see below, size()>
        simd-select-impl(const basic_mask&, const T0&, const T1&) noexcept; // exposition only
  };
}
```

Every specialization of `basic_mask` is a complete type. The
specialization of `basic_mask<Bytes, Abi>` is:

- disabled, if there is no vectorizable type `T` such that `Bytes` is
  equal to `sizeof(T)`,
- otherwise, enabled, if there exists a vectorizable type `T` and a
  value `N` in the range \[`1`, `64`\] such that `Bytes` is equal to
  `sizeof(T)` and `Abi` is `deduce-abi-t<T,
     N>`,
- otherwise, it is *implementation-defined* if such a specialization is
  enabled.

If `basic_mask<Bytes, Abi>` is disabled, the specialization has a
deleted default constructor, deleted destructor, deleted copy
constructor, and deleted copy assignment. In addition only the
`value_type` and `abi_type` members are present.

If `basic_mask<Bytes, Abi>` is enabled, `basic_mask<Bytes, Abi>` is
trivially copyable.

*Recommended practice:* Implementations should support implicit
conversions between specializations of `basic_mask` and appropriate
*implementation-defined* types.

[*Note 1*: Appropriate types are non-standard vector types which are
available in the implementation. — *end note*]

#### Constructors <a id="simd.mask.ctor">[[simd.mask.ctor]]</a>

``` cpp
constexpr explicit basic_mask(value_type x) noexcept;
```

*Effects:* Initializes each element with `x`.

``` cpp
template<size_t UBytes, class UAbi>
  constexpr explicit basic_mask(const basic_mask<UBytes, UAbi>& x) noexcept;
```

*Constraints:* `basic_mask<UBytes, UAbi>::size() == size()` is `true`.

*Effects:* Initializes the iᵗʰ element with `x[`i`]` for all i in the
range of \[`0`, `size()`).

``` cpp
template<class G> constexpr explicit basic_mask(G&& gen);
```

*Constraints:* The expression
`gen(integral_constant<`*`simd-size-type`*`, i>())` is well-formed and
its type is `bool` for all i in the range of \[`0`, `size()`).

*Effects:* Initializes the iᵗʰ element with
`gen(integral_constant<`*`simd-size-type`*`, i>())` for all i in the
range of \[`0`, `size()`).

*Remarks:* `gen` is invoked exactly once for each i, in increasing order
of i.

``` cpp
constexpr basic_mask(const bitset<size()>& b) noexcept;
```

*Effects:* Initializes the iᵗʰ element with `b[`i`]` for all i in the
range \[`0`, `size()`).

``` cpp
constexpr explicit basic_mask(unsigned_integral auto val) noexcept;
```

*Effects:* Initializes the first M elements to the corresponding bit
values in `val`, where M is the smaller of `size()` and the number of
bits in the value representation [[basic.types.general]] of the type of
`val`. If M is less than `size()`, the remaining elements are
initialized to zero.

#### Subscript operator <a id="simd.mask.subscr">[[simd.mask.subscr]]</a>

``` cpp
constexpr value_type operator[](simd-size-type i) const;
```

*Preconditions:* `i >= 0 && i < size()` is `true`.

*Returns:* The value of the iᵗʰ element.

*Throws:* Nothing.

``` cpp
template<simd-integral I>
  constexpr resize_t<I::size(), basic_mask> operator[](const I& indices) const;
```

*Effects:* Equivalent to: `return permute(*this, indices);`

#### Unary operators <a id="simd.mask.unary">[[simd.mask.unary]]</a>

``` cpp
constexpr basic_mask operator!() const noexcept;
constexpr basic_vec<integer-from<Bytes>, Abi> operator+() const noexcept;
constexpr basic_vec<integer-from<Bytes>, Abi> operator-() const noexcept;
constexpr basic_vec<integer-from<Bytes>, Abi> operator~() const noexcept;
```

Let *op* be the operator.

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to the results of applying *op* to `operator[](`i`)` for all i in the
range of \[`0`, `size()`).

#### Conversions <a id="simd.mask.conv">[[simd.mask.conv]]</a>

``` cpp
template<class U, class A>
  constexpr explicit(sizeof(U) != Bytes) operator basic_vec<U, A>() const noexcept;
```

*Constraints:* *`simd-size-v`*`<U, A> == `*`simd-size-v`*`<T, Abi>`.

*Returns:* A data-parallel object where the iᵗʰ element is initialized
to `static_cast<U>(operator[](`i`))`.

``` cpp
constexpr bitset<size()> to_bitset() const noexcept;
```

*Returns:* A `bitset<size()>` object where the iᵗʰ element is
initialized to `operator[](`i`)` for all i in the range \[`0`,
`size()`).

``` cpp
constexpr unsigned long long to_ullong() const;
```

Let N be the width of `unsigned long long`.

*Preconditions:*

- `size() <= `N is `true`, or
- for all i in the range \[N, `size()`), `operator[](`i`)` returns
  `false`.

*Returns:* The integral value corresponding to the bits in `*this`.

*Throws:* Nothing.

### `basic_mask` non-member operations <a id="simd.mask.nonmembers">[[simd.mask.nonmembers]]</a>

#### Binary operators <a id="simd.mask.binary">[[simd.mask.binary]]</a>

``` cpp
friend constexpr basic_mask
  operator&&(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator||(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator& (const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator| (const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator^ (const basic_mask& lhs, const basic_mask& rhs) noexcept;
```

Let *op* be the operator.

*Returns:* A `basic_mask` object initialized with the results of
applying *op* to `lhs` and `rhs` as a binary element-wise operation.

#### Compound assignment <a id="simd.mask.cassign">[[simd.mask.cassign]]</a>

``` cpp
friend constexpr basic_mask&
  operator&=(basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask&
  operator|=(basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask&
  operator^=(basic_mask& lhs, const basic_mask& rhs) noexcept;
```

Let *op* be the operator.

*Effects:* These operators apply *op* to `lhs` and `rhs` as a binary
element-wise operation.

*Returns:* `lhs`.

#### Comparisons <a id="simd.mask.comparison">[[simd.mask.comparison]]</a>

``` cpp
friend constexpr basic_mask
  operator==(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator!=(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator>=(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator<=(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator>(const basic_mask& lhs, const basic_mask& rhs) noexcept;
friend constexpr basic_mask
  operator<(const basic_mask& lhs, const basic_mask& rhs) noexcept;
```

Let *op* be the operator.

*Returns:* A `basic_mask` object initialized with the results of
applying *op* to `lhs` and `rhs` as a binary element-wise operation.

#### Exposition-only conditional operators <a id="simd.mask.cond">[[simd.mask.cond]]</a>

``` cpp
friend constexpr basic_mask simd-select-impl(
  const basic_mask& mask, const basic_mask& a, const basic_mask& b) noexcept;
```

*Returns:* A `basic_mask` object where the iᵗʰ element equals
`mask[`i`] ? a[`i`] : b[`i`]` for all i in the range of \[`0`,
`size()`).

``` cpp
friend constexpr basic_mask
simd-select-impl(const basic_mask& mask, same_as<bool> auto a, same_as<bool> auto b) noexcept;
```

*Returns:* A `basic_mask` object where the iᵗʰ element equals
`mask[`i`] ? a : b` for all i in the range of \[`0`, `size()`).

``` cpp
template<class T0, class T1>
  friend constexpr vec<see below, size()>
    simd-select-impl(const basic_mask& mask, const T0& a, const T1& b) noexcept;
```

*Constraints:*

- `same_as<T0, T1>` is `true`,
- `T0` is a vectorizable type, and
- `sizeof(T0) == Bytes`.

*Returns:* A `vec<T0, size()>` object where the iᵗʰ element equals
`mask[`i`] ? a : b` for all i in the range of \[`0`, `size()`).

#### Reductions <a id="simd.mask.reductions">[[simd.mask.reductions]]</a>

``` cpp
template<size_t Bytes, class Abi>
  constexpr bool all_of(const basic_mask<Bytes, Abi>& k) noexcept;
```

*Returns:* `true` if all boolean elements in `k` are `true`, otherwise
`false`.

``` cpp
template<size_t Bytes, class Abi>
  constexpr bool any_of(const basic_mask<Bytes, Abi>& k) noexcept;
```

*Returns:* `true` if at least one boolean element in `k` is `true`,
otherwise `false`.

``` cpp
template<size_t Bytes, class Abi>
  constexpr bool none_of(const basic_mask<Bytes, Abi>& k) noexcept;
```

*Returns:* `!any_of(k)`.

``` cpp
template<size_t Bytes, class Abi>
  constexpr simd-size-type reduce_count(const basic_mask<Bytes, Abi>& k) noexcept;
```

*Returns:* The number of boolean elements in `k` that are `true`.

``` cpp
template<size_t Bytes, class Abi>
  constexpr simd-size-type reduce_min_index(const basic_mask<Bytes, Abi>& k);
```

*Preconditions:* `any_of(k)` is `true`.

*Returns:* The lowest element index i where `k[`i`]` is `true`.

``` cpp
template<size_t Bytes, class Abi>
  constexpr simd-size-type reduce_max_index(const basic_mask<Bytes, Abi>& k);
```

*Preconditions:* `any_of(k)` is `true`.

*Returns:* The greatest element index i where `k[`i`]` is `true`.

``` cpp
constexpr bool all_of(same_as<bool> auto x) noexcept;
constexpr bool any_of(same_as<bool> auto x) noexcept;
constexpr simd-size-type reduce_count(same_as<bool> auto x) noexcept;
```

*Returns:* `x`.

``` cpp
constexpr bool none_of(same_as<bool> auto x) noexcept;
```

*Returns:* `!x`.

``` cpp
constexpr simd-size-type reduce_min_index(same_as<bool> auto x);
constexpr simd-size-type reduce_max_index(same_as<bool> auto x);
```

*Preconditions:* `x` is `true`.

*Returns:* `0`.

## C compatibility <a id="numerics.c">[[numerics.c]]</a>

### Header `<stdckdint.h>` synopsis <a id="stdckdint.h.syn">[[stdckdint.h.syn]]</a>

``` cpp
#define \libmacro{__STDC_VERSION_STDCKDINT_H__} 202311L

template<class type1, class type2, class type3>
  bool ckd_add(type1* result, type2 a, type3 b);
template<class type1, class type2, class type3>
  bool ckd_sub(type1* result, type2 a, type3 b);
template<class type1, class type2, class type3>
  bool ckd_mul(type1* result, type2 a, type3 b);
```

### Checked integer operations <a id="numerics.c.ckdint">[[numerics.c.ckdint]]</a>

``` cpp
template<class type1, class type2, class type3>
  bool ckd_add(type1* result, type2 a, type3 b);
template<class type1, class type2, class type3>
  bool ckd_sub(type1* result, type2 a, type3 b);
template<class type1, class type2, class type3>
  bool ckd_mul(type1* result, type2 a, type3 b);
```

*Mandates:* Each of the types `type1`, `type2`, and `type3` is a
cv-unqualified signed or unsigned integer type [[basic.fundamental]].

*Remarks:* Each function template has the same semantics as the
corresponding type-generic macro with the same name specified in .

<!-- Link reference definitions -->
[algorithms.parallel.defns]: algorithms.md#algorithms.parallel.defns
[bad.alloc]: support.md#bad.alloc
[basic.extended.fp]: basic.md#basic.extended.fp
[basic.fundamental]: basic.md#basic.fundamental
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.stc.thread]: basic.md#basic.stc.thread
[basic.types.general]: basic.md#basic.types.general
[c.math]: #c.math
[c.math.abs]: #c.math.abs
[c.math.fpclass]: #c.math.fpclass
[c.math.hypot3]: #c.math.hypot3
[c.math.lerp]: #c.math.lerp
[c.math.rand]: #c.math.rand
[cfenv]: #cfenv
[cfenv.syn]: #cfenv.syn
[cfenv.thread]: #cfenv.thread
[class.gslice]: #class.gslice
[class.gslice.overview]: #class.gslice.overview
[class.slice]: #class.slice
[class.slice.overview]: #class.slice.overview
[cmath.syn]: #cmath.syn
[cmplx.over]: #cmplx.over
[complex]: #complex
[complex.literals]: #complex.literals
[complex.member.ops]: #complex.member.ops
[complex.members]: #complex.members
[complex.numbers]: #complex.numbers
[complex.numbers.general]: #complex.numbers.general
[complex.ops]: #complex.ops
[complex.syn]: #complex.syn
[complex.transcendentals]: #complex.transcendentals
[complex.tuple]: #complex.tuple
[complex.value.ops]: #complex.value.ops
[cons.slice]: #cons.slice
[contents]: library.md#contents
[conv.prom]: expr.md#conv.prom
[conv.rank]: basic.md#conv.rank
[cpp.pragma]: cpp.md#cpp.pragma
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.equalitycomparable]: #cpp17.equalitycomparable
[dcl.init]: dcl.md#dcl.init
[dcl.init.general]: dcl.md#dcl.init.general
[errno]: diagnostics.md#errno
[execpol.type]: algorithms.md#execpol.type
[expr.const]: expr.md#expr.const
[gslice.access]: #gslice.access
[gslice.array.assign]: #gslice.array.assign
[gslice.array.comp.assign]: #gslice.array.comp.assign
[gslice.array.fill]: #gslice.array.fill
[gslice.cons]: #gslice.cons
[implimits]: #implimits
[indirect.array.assign]: #indirect.array.assign
[indirect.array.comp.assign]: #indirect.array.comp.assign
[indirect.array.fill]: #indirect.array.fill
[input.iterators]: iterators.md#input.iterators
[input.output]: input.md#input.output
[iostate.flags]: input.md#iostate.flags
[istream.formatted]: input.md#istream.formatted
[iterator.concept.contiguous]: iterators.md#iterator.concept.contiguous
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[library.c]: library.md#library.c
[linalg]: #linalg
[linalg.algs.blas1]: #linalg.algs.blas1
[linalg.algs.blas1.add]: #linalg.algs.blas1.add
[linalg.algs.blas1.asum]: #linalg.algs.blas1.asum
[linalg.algs.blas1.complexity]: #linalg.algs.blas1.complexity
[linalg.algs.blas1.copy]: #linalg.algs.blas1.copy
[linalg.algs.blas1.dot]: #linalg.algs.blas1.dot
[linalg.algs.blas1.givens]: #linalg.algs.blas1.givens
[linalg.algs.blas1.givens.lartg]: #linalg.algs.blas1.givens.lartg
[linalg.algs.blas1.givens.rot]: #linalg.algs.blas1.givens.rot
[linalg.algs.blas1.iamax]: #linalg.algs.blas1.iamax
[linalg.algs.blas1.matfrobnorm]: #linalg.algs.blas1.matfrobnorm
[linalg.algs.blas1.matinfnorm]: #linalg.algs.blas1.matinfnorm
[linalg.algs.blas1.matonenorm]: #linalg.algs.blas1.matonenorm
[linalg.algs.blas1.nrm2]: #linalg.algs.blas1.nrm2
[linalg.algs.blas1.scal]: #linalg.algs.blas1.scal
[linalg.algs.blas1.ssq]: #linalg.algs.blas1.ssq
[linalg.algs.blas1.swap]: #linalg.algs.blas1.swap
[linalg.algs.blas2]: #linalg.algs.blas2
[linalg.algs.blas2.gemv]: #linalg.algs.blas2.gemv
[linalg.algs.blas2.hemv]: #linalg.algs.blas2.hemv
[linalg.algs.blas2.rank1]: #linalg.algs.blas2.rank1
[linalg.algs.blas2.rank2]: #linalg.algs.blas2.rank2
[linalg.algs.blas2.symherrank1]: #linalg.algs.blas2.symherrank1
[linalg.algs.blas2.symv]: #linalg.algs.blas2.symv
[linalg.algs.blas2.trmv]: #linalg.algs.blas2.trmv
[linalg.algs.blas2.trsv]: #linalg.algs.blas2.trsv
[linalg.algs.blas3]: #linalg.algs.blas3
[linalg.algs.blas3.gemm]: #linalg.algs.blas3.gemm
[linalg.algs.blas3.inplacetrsm]: #linalg.algs.blas3.inplacetrsm
[linalg.algs.blas3.rank2k]: #linalg.algs.blas3.rank2k
[linalg.algs.blas3.rankk]: #linalg.algs.blas3.rankk
[linalg.algs.blas3.trmm]: #linalg.algs.blas3.trmm
[linalg.algs.blas3.trsm]: #linalg.algs.blas3.trsm
[linalg.algs.blas3.xxmm]: #linalg.algs.blas3.xxmm
[linalg.algs.reqs]: #linalg.algs.reqs
[linalg.conj]: #linalg.conj
[linalg.conj.conjugated]: #linalg.conj.conjugated
[linalg.conj.conjugatedaccessor]: #linalg.conj.conjugatedaccessor
[linalg.conj.intro]: #linalg.conj.intro
[linalg.conjtransposed]: #linalg.conjtransposed
[linalg.general]: #linalg.general
[linalg.helpers]: #linalg.helpers
[linalg.helpers.abs]: #linalg.helpers.abs
[linalg.helpers.concepts]: #linalg.helpers.concepts
[linalg.helpers.conj]: #linalg.helpers.conj
[linalg.helpers.imag]: #linalg.helpers.imag
[linalg.helpers.mandates]: #linalg.helpers.mandates
[linalg.helpers.precond]: #linalg.helpers.precond
[linalg.helpers.real]: #linalg.helpers.real
[linalg.layout.packed]: #linalg.layout.packed
[linalg.layout.packed.cons]: #linalg.layout.packed.cons
[linalg.layout.packed.obs]: #linalg.layout.packed.obs
[linalg.layout.packed.overview]: #linalg.layout.packed.overview
[linalg.overview]: #linalg.overview
[linalg.reqs]: #linalg.reqs
[linalg.reqs.alg]: #linalg.reqs.alg
[linalg.reqs.val]: #linalg.reqs.val
[linalg.scaled]: #linalg.scaled
[linalg.scaled.intro]: #linalg.scaled.intro
[linalg.scaled.scaled]: #linalg.scaled.scaled
[linalg.scaled.scaledaccessor]: #linalg.scaled.scaledaccessor
[linalg.syn]: #linalg.syn
[linalg.tags]: #linalg.tags
[linalg.tags.diagonal]: #linalg.tags.diagonal
[linalg.tags.order]: #linalg.tags.order
[linalg.tags.triangle]: #linalg.tags.triangle
[linalg.transp]: #linalg.transp
[linalg.transp.helpers]: #linalg.transp.helpers
[linalg.transp.intro]: #linalg.transp.intro
[linalg.transp.layout.transpose]: #linalg.transp.layout.transpose
[linalg.transp.transposed]: #linalg.transp.transposed
[mask.array.assign]: #mask.array.assign
[mask.array.comp.assign]: #mask.array.comp.assign
[mask.array.fill]: #mask.array.fill
[math.constants]: #math.constants
[mdspan.accessor.reqmts]: containers.md#mdspan.accessor.reqmts
[mdspan.layout.policy.reqmts]: containers.md#mdspan.layout.policy.reqmts
[mdspan.overview]: containers.md#mdspan.overview
[namespace.std]: library.md#namespace.std
[numarray]: #numarray
[numbers]: #numbers
[numbers.syn]: #numbers.syn
[numeric.requirements]: #numeric.requirements
[numerics]: #numerics
[numerics.c]: #numerics.c
[numerics.c.ckdint]: #numerics.c.ckdint
[numerics.defns]: algorithms.md#numerics.defns
[numerics.general]: #numerics.general
[numerics.summary]: #numerics.summary
[output.iterators]: iterators.md#output.iterators
[over.match.general]: over.md#over.match.general
[rand]: #rand
[rand.adapt]: #rand.adapt
[rand.adapt.disc]: #rand.adapt.disc
[rand.adapt.general]: #rand.adapt.general
[rand.adapt.ibits]: #rand.adapt.ibits
[rand.adapt.shuf]: #rand.adapt.shuf
[rand.device]: #rand.device
[rand.dist]: #rand.dist
[rand.dist.bern]: #rand.dist.bern
[rand.dist.bern.bernoulli]: #rand.dist.bern.bernoulli
[rand.dist.bern.bin]: #rand.dist.bern.bin
[rand.dist.bern.geo]: #rand.dist.bern.geo
[rand.dist.bern.negbin]: #rand.dist.bern.negbin
[rand.dist.general]: #rand.dist.general
[rand.dist.norm]: #rand.dist.norm
[rand.dist.norm.cauchy]: #rand.dist.norm.cauchy
[rand.dist.norm.chisq]: #rand.dist.norm.chisq
[rand.dist.norm.f]: #rand.dist.norm.f
[rand.dist.norm.lognormal]: #rand.dist.norm.lognormal
[rand.dist.norm.normal]: #rand.dist.norm.normal
[rand.dist.norm.t]: #rand.dist.norm.t
[rand.dist.pois]: #rand.dist.pois
[rand.dist.pois.exp]: #rand.dist.pois.exp
[rand.dist.pois.extreme]: #rand.dist.pois.extreme
[rand.dist.pois.gamma]: #rand.dist.pois.gamma
[rand.dist.pois.poisson]: #rand.dist.pois.poisson
[rand.dist.pois.weibull]: #rand.dist.pois.weibull
[rand.dist.samp]: #rand.dist.samp
[rand.dist.samp.discrete]: #rand.dist.samp.discrete
[rand.dist.samp.pconst]: #rand.dist.samp.pconst
[rand.dist.samp.plinear]: #rand.dist.samp.plinear
[rand.dist.uni]: #rand.dist.uni
[rand.dist.uni.int]: #rand.dist.uni.int
[rand.dist.uni.real]: #rand.dist.uni.real
[rand.eng]: #rand.eng
[rand.eng.general]: #rand.eng.general
[rand.eng.lcong]: #rand.eng.lcong
[rand.eng.mers]: #rand.eng.mers
[rand.eng.philox]: #rand.eng.philox
[rand.eng.philox.f]: #rand.eng.philox.f
[rand.eng.sub]: #rand.eng.sub
[rand.general]: #rand.general
[rand.predef]: #rand.predef
[rand.req]: #rand.req
[rand.req.adapt]: #rand.req.adapt
[rand.req.dist]: #rand.req.dist
[rand.req.eng]: #rand.req.eng
[rand.req.genl]: #rand.req.genl
[rand.req.seedseq]: #rand.req.seedseq
[rand.req.urng]: #rand.req.urng
[rand.synopsis]: #rand.synopsis
[rand.util]: #rand.util
[rand.util.canonical]: #rand.util.canonical
[rand.util.seedseq]: #rand.util.seedseq
[random.access.iterators]: iterators.md#random.access.iterators
[res.on.data.races]: library.md#res.on.data.races
[sf.cmath]: #sf.cmath
[sf.cmath.assoc.laguerre]: #sf.cmath.assoc.laguerre
[sf.cmath.assoc.legendre]: #sf.cmath.assoc.legendre
[sf.cmath.beta]: #sf.cmath.beta
[sf.cmath.comp.ellint.1]: #sf.cmath.comp.ellint.1
[sf.cmath.comp.ellint.2]: #sf.cmath.comp.ellint.2
[sf.cmath.comp.ellint.3]: #sf.cmath.comp.ellint.3
[sf.cmath.cyl.bessel.i]: #sf.cmath.cyl.bessel.i
[sf.cmath.cyl.bessel.j]: #sf.cmath.cyl.bessel.j
[sf.cmath.cyl.bessel.k]: #sf.cmath.cyl.bessel.k
[sf.cmath.cyl.neumann]: #sf.cmath.cyl.neumann
[sf.cmath.ellint.1]: #sf.cmath.ellint.1
[sf.cmath.ellint.2]: #sf.cmath.ellint.2
[sf.cmath.ellint.3]: #sf.cmath.ellint.3
[sf.cmath.expint]: #sf.cmath.expint
[sf.cmath.general]: #sf.cmath.general
[sf.cmath.hermite]: #sf.cmath.hermite
[sf.cmath.laguerre]: #sf.cmath.laguerre
[sf.cmath.legendre]: #sf.cmath.legendre
[sf.cmath.riemann.zeta]: #sf.cmath.riemann.zeta
[sf.cmath.sph.bessel]: #sf.cmath.sph.bessel
[sf.cmath.sph.legendre]: #sf.cmath.sph.legendre
[sf.cmath.sph.neumann]: #sf.cmath.sph.neumann
[simd]: #simd
[simd.alg]: #simd.alg
[simd.binary]: #simd.binary
[simd.bit]: #simd.bit
[simd.cassign]: #simd.cassign
[simd.class]: #simd.class
[simd.comparison]: #simd.comparison
[simd.complex.access]: #simd.complex.access
[simd.complex.math]: #simd.complex.math
[simd.cond]: #simd.cond
[simd.creation]: #simd.creation
[simd.ctor]: #simd.ctor
[simd.ctor,simd.loadstore]: #simd.ctor,simd.loadstore
[simd.expos]: #simd.expos
[simd.expos.abi]: #simd.expos.abi
[simd.expos.defn]: #simd.expos.defn
[simd.flags]: #simd.flags
[simd.flags.oper]: #simd.flags.oper
[simd.flags.overview]: #simd.flags.overview
[simd.general]: #simd.general
[simd.iterator]: #simd.iterator
[simd.loadstore]: #simd.loadstore
[simd.mask.binary]: #simd.mask.binary
[simd.mask.cassign]: #simd.mask.cassign
[simd.mask.class]: #simd.mask.class
[simd.mask.comparison]: #simd.mask.comparison
[simd.mask.cond]: #simd.mask.cond
[simd.mask.conv]: #simd.mask.conv
[simd.mask.ctor]: #simd.mask.ctor
[simd.mask.nonmembers]: #simd.mask.nonmembers
[simd.mask.overview]: #simd.mask.overview
[simd.mask.reductions]: #simd.mask.reductions
[simd.mask.subscr]: #simd.mask.subscr
[simd.mask.unary]: #simd.mask.unary
[simd.math]: #simd.math
[simd.nonmembers]: #simd.nonmembers
[simd.overview]: #simd.overview
[simd.permute.dynamic]: #simd.permute.dynamic
[simd.permute.mask]: #simd.permute.mask
[simd.permute.memory]: #simd.permute.memory
[simd.permute.static]: #simd.permute.static
[simd.reductions]: #simd.reductions
[simd.subscr]: #simd.subscr
[simd.syn]: #simd.syn
[simd.traits]: #simd.traits
[simd.unary]: #simd.unary
[slice.access]: #slice.access
[slice.arr.assign]: #slice.arr.assign
[slice.arr.comp.assign]: #slice.arr.comp.assign
[slice.arr.fill]: #slice.arr.fill
[slice.ops]: #slice.ops
[stdckdint.h.syn]: #stdckdint.h.syn
[strings]: strings.md#strings
[template.gslice.array]: #template.gslice.array
[template.gslice.array.overview]: #template.gslice.array.overview
[template.indirect.array]: #template.indirect.array
[template.indirect.array.overview]: #template.indirect.array.overview
[template.mask.array]: #template.mask.array
[template.mask.array.overview]: #template.mask.array.overview
[template.slice.array]: #template.slice.array
[template.slice.array.overview]: #template.slice.array.overview
[template.valarray]: #template.valarray
[template.valarray.overview]: #template.valarray.overview
[term.literal.type]: basic.md#term.literal.type
[thread.jthread.class]: thread.md#thread.jthread.class
[thread.thread.class]: thread.md#thread.thread.class
[utility.arg.requirements]: library.md#utility.arg.requirements
[valarray.access]: #valarray.access
[valarray.assign]: #valarray.assign
[valarray.binary]: #valarray.binary
[valarray.cassign]: #valarray.cassign
[valarray.comparison]: #valarray.comparison
[valarray.cons]: #valarray.cons
[valarray.members]: #valarray.members
[valarray.nonmembers]: #valarray.nonmembers
[valarray.range]: #valarray.range
[valarray.special]: #valarray.special
[valarray.sub]: #valarray.sub
[valarray.syn]: #valarray.syn
[valarray.transcend]: #valarray.transcend
[valarray.unary]: #valarray.unary
[views.multidim]: containers.md#views.multidim

[^1]: In other words, value types. These include arithmetic types,
    pointers, the library class `complex`, and instantiations of
    `valarray` for value types.

[^2]: This constructor (as well as the subsequent corresponding `seed()`
    function) can be particularly useful to applications requiring a
    large number of independent random sequences.

[^3]: The name of this engine refers, in part, to a property of its
    period: For properly-selected values of the parameters, the period
    is closely related to a large Mersenne prime number.

[^4]: The parameter is intended to allow an implementation to
    differentiate between different sources of randomness.

[^5]: If a device has n states whose respective probabilities are
    P₀, …, Pₙ₋₁, the device entropy S is defined as  
    $S = - \sum_{i=0}^{n-1} P_i \cdot \log P_i$.

[^6]: d is introduced to avoid any attempt to produce more bits of
    randomness than can be held in `RealType`.

[^7]: The distribution corresponding to this probability density
    function is also known (with a possible change of variable) as the
    Gumbel Type I, the log-Weibull, or the Fisher-Tippett Type I
    distribution.

[^8]:  [[implimits]] recommends a minimum number of recursively nested
    template instantiations. This requirement thus indirectly suggests a
    minimum allowable complexity for valarray expressions.

[^9]: The intent is to specify an array template that has the minimum
    functionality necessary to address aliasing ambiguities and the
    proliferation of temporary objects. Thus, the `valarray` template is
    neither a matrix class nor a field class. However, it is a very
    useful building block for designing such classes.

[^10]: This default constructor is essential, since arrays of `valarray`
    can be useful. After initialization, the length of an empty array
    can be increased with the `resize` member function.

[^11]: This constructor is the preferred method for converting a C array
    to a `valarray` object.

[^12]: This copy constructor creates a distinct array rather than an
    alias. Implementations in which arrays share storage are permitted,
    but they would need to implement a copy-on-reference mechanism to
    ensure that arrays are conceptually distinct.

[^13]: BLAS stands for *Basic Linear Algebra Subprograms*. C++ programs
    can instantiate this class. See, for example, Dongarra, Du Croz,
    Duff, and Hammerling: *A set of Level 3 Basic Linear Algebra
    Subprograms*; Technical Report MCS-P1-0888, Argonne National
    Laboratory (USA), Mathematics and Computer Science Division, August,
    1988.

[^14]: A mathematical function is mathematically defined for a given set
    of argument values (a) if it is explicitly defined for that set of
    argument values, or (b) if its limiting value exists and does not
    depend on the direction of approach.
