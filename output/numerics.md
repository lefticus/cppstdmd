---
current_file: numerics
label_index_file: converted/cppstdmd/output/cpp_std_labels.lua
---

# Numerics library <a id="numerics">[numerics]</a>

## General <a id="numerics.general">[numerics.general]</a>

This Clause describes components that C++ programs may use to perform
seminumerical operations.

The following subclauses describe components for complex number types,
random number generation, numeric ( *n*-at-a-time) arrays, generalized
numeric algorithms, and mathematical constants and functions for
floating-point types, as summarized in [numerics.summary].

**Table: Numerics library summary**

| Subclause |  | Header |
| --- | --- | --- |
| [numeric.requirements] | Requirements |
| [cfenv] | Floating-point environment | `<cfenv>` |
| [complex.numbers] | Complex numbers | `<complex>` |
| [rand] | Random number generation | `<random>` |
| [numarray] | Numeric arrays | `<valarray>` |
| [c.math] | Mathematical functions for floating-point types | `<cmath>`, `<cstdlib>` |
| [numbers] | Numbers | `<numbers>` |

## Numeric type requirements <a id="numeric.requirements">[numeric.requirements]</a>

The `complex` and `valarray` components are parameterized by the type of
information they contain and manipulate. A C++ program shall instantiate
these components only with a numeric type. A *numeric type* is a
cv-unqualified object type `T` that meets the
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*,
*Cpp17CopyAssignable*, and *Cpp17Destructible* requirements
[utility.arg.requirements].

If any operation on `T` throws an exception the effects are undefined.

In addition, many member and related functions of `valarray<T>` can be
successfully instantiated and will exhibit well-defined behavior if and
only if `T` meets additional requirements specified for each such member
or related function.

\[*Example 1*: It is valid to instantiate `valarray<complex>`, but
`operator>()` will not be successfully instantiated for
`valarray<complex>` operands, since `complex` does not have any ordering
operators. — *end example*\]

## The floating-point environment <a id="cfenv">[cfenv]</a>

``` cpp
#define FE_ALL_EXCEPT see below
#define FE_DIVBYZERO see below    // optional
#define FE_INEXACT see below      // optional
#define FE_INVALID see below      // optional
#define FE_OVERFLOW see below     // optional
#define FE_UNDERFLOW see below    // optional

#define FE_DOWNWARD see below     // optional
#define FE_TONEAREST see below    // optional
#define FE_TOWARDZERO see below   // optional
#define FE_UPWARD see below       // optional

#define FE_DFL_ENV see below

namespace std {
  // types
  using fenv_t    = object type;
  using fexcept_t = integer type;

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

The contents and meaning of the header `<cfenv>` are the same as the C
standard library header `<fenv.h>`.

\[*Note 1*: This document does not require an implementation to support
the `FENV_ACCESS` pragma; it is *implementation-defined* [cpp.pragma]
whether the pragma is supported. As a consequence, it is
*implementation-defined* whether these functions can be used to test
floating-point status flags, set floating-point control modes, or run
under non-default mode settings. If the pragma is used to enable control
over the floating-point environment, this document does not specify the
effect on floating-point evaluation in constant
expressions. — *end note*\]

### Threads <a id="cfenv.thread">[cfenv.thread]</a>

The floating-point environment has thread storage duration
[basic.stc.thread]. The initial state for a thread’s floating-point
environment is the state of the floating-point environment of the thread
that constructs the corresponding `thread` object [thread.thread.class]
or `jthread` object [thread.jthread.class] at the time it constructed
the object.

\[*Note 2*: That is, the child thread gets the floating-point state of
the parent thread at the time of the child’s creation. — *end note*\]

A separate floating-point environment is maintained for each thread.
Each function accesses the environment corresponding to its calling
thread.

## Complex numbers <a id="complex.numbers">[complex.numbers]</a>

### General <a id="complex.numbers.general">[complex.numbers.general]</a>

The header `<complex>` defines a class template, and numerous functions
for representing and manipulating complex numbers.

The effect of instantiating the template `complex` for any type that is
not a cv-unqualified floating-point type [basic.fundamental] is
unspecified. Specializations of `complex` for cv-unqualified
floating-point types are trivially-copyable literal types
[term.literal.type].

If the result of a function is not mathematically defined or not in the
range of representable values for its type, the behavior is undefined.

If `z` is an lvalue of type cv `complex<T>` then:

- the expression `reinterpret_cast<\cv{} T(&)[2]>(z)` is well-formed,

- `reinterpret_cast<\cv{} T(&)[2]>(z)[0]` designates the real part of
  `z`, and

- `reinterpret_cast<\cv{} T(&)[2]>(z)[1]` designates the imaginary part
  of `z`.

Moreover, if `a` is an expression of type cv `complex<T>*` and the
expression `a[i]` is well-defined for an integer expression `i`, then:

- `reinterpret_cast<\cv{} T*>(a)[2*i]` designates the real part of
  `a[i]`, and

- `reinterpret_cast<\cv{} T*>(a)[2*i + 1]` designates the imaginary part
  of `a[i]`.

### Header `<complex>` synopsis <a id="complex.syn">[complex.syn]</a>

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

  template<class T> T abs(const complex<T>&);
  template<class T> T arg(const complex<T>&);
  template<class T> constexpr T norm(const complex<T>&);

  template<class T> constexpr complex<T> conj(const complex<T>&);
  template<class T> complex<T> proj(const complex<T>&);
  template<class T> complex<T> polar(const T&, const T& = T());

  // [complex.transcendentals], transcendentals
  template<class T> complex<T> acos(const complex<T>&);
  template<class T> complex<T> asin(const complex<T>&);
  template<class T> complex<T> atan(const complex<T>&);

  template<class T> complex<T> acosh(const complex<T>&);
  template<class T> complex<T> asinh(const complex<T>&);
  template<class T> complex<T> atanh(const complex<T>&);

  template<class T> complex<T> cos  (const complex<T>&);
  template<class T> complex<T> cosh (const complex<T>&);
  template<class T> complex<T> exp  (const complex<T>&);
  template<class T> complex<T> log  (const complex<T>&);
  template<class T> complex<T> log10(const complex<T>&);

  template<class T> complex<T> pow  (const complex<T>&, const T&);
  template<class T> complex<T> pow  (const complex<T>&, const complex<T>&);
  template<class T> complex<T> pow  (const T&, const complex<T>&);

  template<class T> complex<T> sin  (const complex<T>&);
  template<class T> complex<T> sinh (const complex<T>&);
  template<class T> complex<T> sqrt (const complex<T>&);
  template<class T> complex<T> tan  (const complex<T>&);
  template<class T> complex<T> tanh (const complex<T>&);

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

### Class template `complex` <a id="complex">[complex]</a>

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

### Member functions <a id="complex.members">[complex.members]</a>

``` cpp
constexpr complex(const T& re = T(), const T& im = T());
```

> *Ensures:*
>
> `real() == re && imag() == im` is `true`.

``` cpp
template<class X> constexpr explicit(see below) complex(const complex<X>& other);
```

> *Effects:*
>
> Initializes the real part with `other.real()` and the imaginary part
> with `other.imag()`.
>
> *Remarks:*
>
> The expression inside `explicit` evaluates to `false` if and only if
> the floating-point conversion rank of `T` is greater than or equal to
> the floating-point conversion rank of `X`.

``` cpp
constexpr T real() const;
```

> *Returns:*
>
> The value of the real component.

``` cpp
constexpr void real(T val);
```

> *Effects:*
>
> Assigns `val` to the real component.

``` cpp
constexpr T imag() const;
```

> *Returns:*
>
> The value of the imaginary component.

``` cpp
constexpr void imag(T val);
```

> *Effects:*
>
> Assigns `val` to the imaginary component.

### Member operators <a id="complex.member.ops">[complex.member.ops]</a>

``` cpp
constexpr complex& operator+=(const T& rhs);
```

> *Effects:*
>
> Adds the scalar value `rhs` to the real part of the complex value
> `*this` and stores the result in the real part of `*this`, leaving the
> imaginary part unchanged.
>
> *Returns:*
>
> `*this`.

``` cpp
constexpr complex& operator-=(const T& rhs);
```

> *Effects:*
>
> Subtracts the scalar value `rhs` from the real part of the complex
> value `*this` and stores the result in the real part of `*this`,
> leaving the imaginary part unchanged.
>
> *Returns:*
>
> `*this`.

``` cpp
constexpr complex& operator*=(const T& rhs);
```

> *Effects:*
>
> Multiplies the scalar value `rhs` by the complex value `*this` and
> stores the result in `*this`.
>
> *Returns:*
>
> `*this`.

``` cpp
constexpr complex& operator/=(const T& rhs);
```

> *Effects:*
>
> Divides the scalar value `rhs` into the complex value `*this` and
> stores the result in `*this`.
>
> *Returns:*
>
> `*this`.

``` cpp
template<class X> constexpr complex& operator+=(const complex<X>& rhs);
```

> *Effects:*
>
> Adds the complex value `rhs` to the complex value `*this` and stores
> the sum in `*this`.
>
> *Returns:*
>
> `*this`.

``` cpp
template<class X> constexpr complex& operator-=(const complex<X>& rhs);
```

> *Effects:*
>
> Subtracts the complex value `rhs` from the complex value `*this` and
> stores the difference in `*this`.
>
> *Returns:*
>
> `*this`.

``` cpp
template<class X> constexpr complex& operator*=(const complex<X>& rhs);
```

> *Effects:*
>
> Multiplies the complex value `rhs` by the complex value `*this` and
> stores the product in `*this`.
>
> *Returns:*
>
> `*this`.

``` cpp
template<class X> constexpr complex& operator/=(const complex<X>& rhs);
```

> *Effects:*
>
> Divides the complex value `rhs` into the complex value `*this` and
> stores the quotient in `*this`.
>
> *Returns:*
>
> `*this`.

### Non-member operations <a id="complex.ops">[complex.ops]</a>

``` cpp
template<class T> constexpr complex<T> operator+(const complex<T>& lhs);
```

> *Returns:*
>
> `complex<T>(lhs)`.

``` cpp
template<class T> constexpr complex<T> operator+(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator+(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator+(const T& lhs, const complex<T>& rhs);
```

> *Returns:*
>
> `complex<T>(lhs) += rhs`.

``` cpp
template<class T> constexpr complex<T> operator-(const complex<T>& lhs);
```

> *Returns:*
>
> `complex<T>(-lhs.real(),-lhs.imag())`.

``` cpp
template<class T> constexpr complex<T> operator-(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator-(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator-(const T& lhs, const complex<T>& rhs);
```

> *Returns:*
>
> `complex<T>(lhs) -= rhs`.

``` cpp
template<class T> constexpr complex<T> operator*(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator*(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator*(const T& lhs, const complex<T>& rhs);
```

> *Returns:*
>
> `complex<T>(lhs) *= rhs`.

``` cpp
template<class T> constexpr complex<T> operator/(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr complex<T> operator/(const complex<T>& lhs, const T& rhs);
template<class T> constexpr complex<T> operator/(const T& lhs, const complex<T>& rhs);
```

> *Returns:*
>
> `complex<T>(lhs) /= rhs`.

``` cpp
template<class T> constexpr bool operator==(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr bool operator==(const complex<T>& lhs, const T& rhs);
```

> *Returns:*
>
> `lhs.real() == rhs.real() && lhs.imag() == rhs.imag()`.
>
> *Remarks:*
>
> The imaginary part is assumed to be `T()`, or 0.0, for the `T`
> arguments.

``` cpp
template<class T, class charT, class traits>
  basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>& is, complex<T>& x);
```

> *Preconditions:*
>
> The input values are convertible to `T`.
>
> *Effects:*
>
> Extracts a complex number `x` of the form: `u`, `(u)`, or `(u,v)`,
> where `u` is the real part and `v` is the imaginary
> part\[istream.formatted\].
>
> If bad input is encountered, calls `is.setstate(ios_base::failbit)`
> (which may throw `ios_base::failure`\[iostate.flags\]).
>
> *Returns:*
>
> `is`.
>
> *Remarks:*
>
> This extraction is performed as a series of simpler extractions.
> Therefore, the skipping of whitespace is specified to be the same for
> each of the simpler extractions.

``` cpp
template<class T, class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& o, const complex<T>& x);
```

> *Effects:*
>
> Inserts the complex number `x` onto the stream `o` as if it were
> implemented as follows:
>
> ``` cpp
> basic_ostringstream<charT, traits> s;
> s.flags(o.flags());
> s.imbue(o.getloc());
> s.precision(o.precision());
> s << '(' << x.real() << ',' << x.imag() << ')';
> return o << s.str();
> ```
>
> \[*Note 1*: In a locale in which comma is used as a decimal point
> character, the use of comma as a field separator can be ambiguous.
> Inserting `showpoint` into the output stream forces all outputs to
> show an explicit decimal point character; as a result, all inserted
> sequences of complex numbers can be extracted
> unambiguously. — *end note*\]

### Value operations <a id="complex.value.ops">[complex.value.ops]</a>

``` cpp
template<class T> constexpr T real(const complex<T>& x);
```

> *Returns:*
>
> `x.real()`.

``` cpp
template<class T> constexpr T imag(const complex<T>& x);
```

> *Returns:*
>
> `x.imag()`.

``` cpp
template<class T> T abs(const complex<T>& x);
```

> *Returns:*
>
> The magnitude of `x`.

``` cpp
template<class T> T arg(const complex<T>& x);
```

> *Returns:*
>
> The phase angle of `x`, or `atan2(imag(x), real(x))`.

``` cpp
template<class T> constexpr T norm(const complex<T>& x);
```

> *Returns:*
>
> The squared magnitude of `x`.

``` cpp
template<class T> constexpr complex<T> conj(const complex<T>& x);
```

> *Returns:*
>
> The complex conjugate of `x`.

``` cpp
template<class T> complex<T> proj(const complex<T>& x);
```

> *Returns:*
>
> The projection of `x` onto the Riemann sphere.
>
> *Remarks:*
>
> Behaves the same as the C function `cproj`.

``` cpp
template<class T> complex<T> polar(const T& rho, const T& theta = T());
```

> *Preconditions:*
>
> `rho` is non-negative and non-NaN`theta` is finite.
>
> *Returns:*
>
> The `complex` value corresponding to a complex number whose magnitude
> is `rho` and whose phase angle is `theta`.

### Transcendentals <a id="complex.transcendentals">[complex.transcendentals]</a>

``` cpp
template<class T> complex<T> acos(const complex<T>& x);
```

> *Returns:*
>
> The complex arc cosine of `x`.
>
> *Remarks:*
>
> Behaves the same as the C function `cacos`.

``` cpp
template<class T> complex<T> asin(const complex<T>& x);
```

> *Returns:*
>
> The complex arc sine of `x`.
>
> *Remarks:*
>
> Behaves the same as the C function `casin`.

``` cpp
template<class T> complex<T> atan(const complex<T>& x);
```

> *Returns:*
>
> The complex arc tangent of `x`.
>
> *Remarks:*
>
> Behaves the same as the C function `catan`.

``` cpp
template<class T> complex<T> acosh(const complex<T>& x);
```

> *Returns:*
>
> The complex arc hyperbolic cosine of `x`.
>
> *Remarks:*
>
> Behaves the same as the C function `cacosh`.

``` cpp
template<class T> complex<T> asinh(const complex<T>& x);
```

> *Returns:*
>
> The complex arc hyperbolic sine of `x`.
>
> *Remarks:*
>
> Behaves the same as the C function `casinh`.

``` cpp
template<class T> complex<T> atanh(const complex<T>& x);
```

> *Returns:*
>
> The complex arc hyperbolic tangent of `x`.
>
> *Remarks:*
>
> Behaves the same as the C function `catanh`.

``` cpp
template<class T> complex<T> cos(const complex<T>& x);
```

> *Returns:*
>
> The complex cosine of `x`.

``` cpp
template<class T> complex<T> cosh(const complex<T>& x);
```

> *Returns:*
>
> The complex hyperbolic cosine of `x`.

``` cpp
template<class T> complex<T> exp(const complex<T>& x);
```

> *Returns:*
>
> The complex base-e exponential of `x`.

``` cpp
template<class T> complex<T> log(const complex<T>& x);
```

> *Returns:*
>
> The complex natural (base-e) logarithm of `x`. For all `x`,
> `imag(log(x))` lies in the interval \[-π, π\].
>
> \[*Note 2*: The semantics of this function are intended to be the same
> in as they are for `clog` in C. — *end note*\]
>
> *Remarks:*
>
> The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> log10(const complex<T>& x);
```

> *Returns:*
>
> The complex common (base-10) logarithm of `x`, defined as
> `log(x) / log(10)`.
>
> *Remarks:*
>
> The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> pow(const complex<T>& x, const complex<T>& y);
template<class T> complex<T> pow(const complex<T>& x, const T& y);
template<class T> complex<T> pow(const T& x, const complex<T>& y);
```

> *Returns:*
>
> The complex power of base `x` raised to the $\texttt{y}^\text{th}$
> power, defined as `exp(y * log(x))`. The value returned for
> `pow(0, 0)` is *implementation-defined*.
>
> *Remarks:*
>
> The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> sin(const complex<T>& x);
```

> *Returns:*
>
> The complex sine of `x`.

``` cpp
template<class T> complex<T> sinh(const complex<T>& x);
```

> *Returns:*
>
> The complex hyperbolic sine of `x`.

``` cpp
template<class T> complex<T> sqrt(const complex<T>& x);
```

> *Returns:*
>
> The complex square root of `x`, in the range of the right half-plane.
>
> \[*Note 3*: The semantics of this function are intended to be the same
> in as they are for `csqrt` in C. — *end note*\]
>
> *Remarks:*
>
> The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> tan(const complex<T>& x);
```

> *Returns:*
>
> The complex tangent of `x`.

``` cpp
template<class T> complex<T> tanh(const complex<T>& x);
```

> *Returns:*
>
> The complex hyperbolic tangent of `x`.

### Additional overloads <a id="cmplx.over">[cmplx.over]</a>

The following function templates shall have additional overloads:

``` cpp
arg                   norm
conj                  proj
imag                  real
```

where `norm`, `conj`, `imag`, and `real` are `constexpr` overloads.

The additional overloads shall be sufficient to ensure:

- If the argument has a floating-point type `T`, then it is effectively
  cast to `complex<T>`.

- Otherwise, if the argument has integer type, then it is effectively
  cast to `complex<double>`.

Function template `pow` has additional overloads sufficient to ensure,
for a call with one argument of type `complex<T1>` and the other
argument of type `T2` or `complex<T2>`, both arguments are effectively
cast to `complex<common_type_t<T1, T2>>`. If `common_type_t<T1, T2>` is
not well-formed, then the program is ill-formed.

### Suffixes for complex number literals <a id="complex.literals">[complex.literals]</a>

This subclause describes literal suffixes for constructing complex
number literals. The suffixes `i`, `il`, and `if` create complex numbers
of the types `complex<double>`, `complex<long double>`, and
`complex<float>` respectively, with their imaginary part denoted by the
given literal number and the real part being zero.

``` cpp
constexpr complex<long double> operator""il(long double d);
constexpr complex<long double> operator""il(unsigned long long d);
```

> *Returns:*
>
> `complex<long double>{0.0L, static_cast<long double>(d)}`.

``` cpp
constexpr complex<double> operator""i(long double d);
constexpr complex<double> operator""i(unsigned long long d);
```

> *Returns:*
>
> `complex<double>{0.0, static_cast<double>(d)}`.

``` cpp
constexpr complex<float> operator""if(long double d);
constexpr complex<float> operator""if(unsigned long long d);
```

> *Returns:*
>
> `complex<float>{0.0f, static_cast<float>(d)}`.

## Random number generation <a id="rand">[rand]</a>

### General <a id="rand.general">[rand.general]</a>

Subclause [rand] defines a facility for generating (pseudo-)random
numbers.

In addition to a few utilities, four categories of entities are
described: *uniform random bit generators*, *random number engines*,
*random number engine adaptors*, and *random number distributions*.
These categorizations are applicable to types that meet the
corresponding requirements, to objects instantiated from such types, and
to templates producing such types when instantiated.

\[*Note 1*: These entities are specified in such a way as to permit the
binding of any uniform random bit generator object `e` as the argument
to any random number distribution object `d`, thus producing a
zero-argument function object such as given by
`bind(d,e)`. — *end note*\]

Each of the entities specified in [rand] has an associated arithmetic
type [basic.fundamental] identified as `result_type`. With `T` as the
`result_type` thus associated with such an entity, that entity is
characterized:

- as *boolean* or equivalently as *boolean-valued*, if `T` is `bool`;

- otherwise as *integral* or equivalently as *integer-valued*, if
  `numeric_limits<T>::is_integer` is `true`;

- otherwise as *floating-point* or equivalently as *real-valued*.

If integer-valued, an entity may optionally be further characterized as
*signed* or *unsigned*, according to `numeric_limits<T>::is_signed`.

Unless otherwise specified, all descriptions of calculations in [rand]
use mathematical real numbers.

Throughout [rand], the operators , , and denote the respective
conventional bitwise operations. Further:

- the operator denotes a bitwise right shift with zero-valued bits
  appearing in the high bits of the result, and

- the operator denotes a bitwise left shift with zero-valued bits
  appearing in the low bits of the result, and whose result is always
  taken modulo $2^w$.

### Header `<random>` synopsis <a id="rand.synopsis">[rand.synopsis]</a>

``` cpp
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [rand.req.urng], uniform random bit generator requirements
  template<class G>
    concept uniform_random_bit_generator = see below;

  // [rand.eng.lcong], class template linear_congruential_engine
  template<class UIntType, UIntType a, UIntType c, UIntType m>
    class linear_congruential_engine;

  // [rand.eng.mers], class template mersenne_twister_engine
  template<class UIntType, size_t w, size_t n, size_t m, size_t r,
           UIntType a, size_t u, UIntType d, size_t s,
           UIntType b, size_t t,
           UIntType c, size_t l, UIntType f>
    class mersenne_twister_engine;

  // [rand.eng.sub], class template subtract_with_carry_engine
  template<class UIntType, size_t w, size_t s, size_t r>
    class subtract_with_carry_engine;

  // [rand.adapt.disc], class template discard_block_engine
  template<class Engine, size_t p, size_t r>
    class discard_block_engine;

  // [rand.adapt.ibits], class template independent_bits_engine
  template<class Engine, size_t w, class UIntType>
    class independent_bits_engine;

  // [rand.adapt.shuf], class template shuffle_order_engine
  template<class Engine, size_t k>
    class shuffle_order_engine;

  // [rand.predef], engines and engine adaptors with predefined parameters
  using minstd_rand0  = see below;
  using minstd_rand   = see below;
  using mt19937       = see below;
  using mt19937_64    = see below;
  using ranlux24_base = see below;
  using ranlux48_base = see below;
  using ranlux24      = see below;
  using ranlux48      = see below;
  using knuth_b       = see below;

  using default_random_engine = see below;

  // [rand.device], class random_device
  class random_device;

  // [rand.util.seedseq], class seed_seq
  class seed_seq;

  // [rand.util.canonical], function template generate_canonical
  template<class RealType, size_t bits, class URBG>
    RealType generate_canonical(URBG& g);

  // [rand.dist.uni.int], class template uniform_int_distribution
  template<class IntType = int>
    class uniform_int_distribution;

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

### Requirements <a id="rand.req">[rand.req]</a>

#### General requirements <a id="rand.req.genl">[rand.req.genl]</a>

Throughout this subclause [rand], the effect of instantiating a
template:

- that has a template type parameter named `Sseq` is undefined unless
  the corresponding template argument is cv-unqualified and meets the
  requirements of seed sequence [rand.req.seedseq].

- that has a template type parameter named `URBG` is undefined unless
  the corresponding template argument is cv-unqualified and meets the
  requirements of uniform random bit generator [rand.req.urng].

- that has a template type parameter named `Engine` is undefined unless
  the corresponding template argument is cv-unqualified and meets the
  requirements of random number engine [rand.req.eng].

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

Throughout this subclause [rand], phrases of the form “`x` is an
iterator of a specific kind” shall be interpreted as equivalent to the
more formal requirement that “`x` is a value of a type meeting the
requirements of the specified iterator type”.

Throughout this subclause [rand], any constructor that can be called
with a single argument and that meets a requirement specified in this
subclause shall be declared `explicit`.

#### Seed sequence requirements <a id="rand.req.seedseq">[rand.req.seedseq]</a>

A *seed sequence* is an object that consumes a sequence of
integer-valued data and produces a requested number of unsigned integer
values i, $0 \le i < 2^{32}$, based on the consumed data.

\[*Note 2*: Such an object provides a mechanism to avoid replication of
streams of random variates. This can be useful, for example, in
applications requiring large numbers of random number
engines. — *end note*\]

A class `S` meets the requirements of a seed sequence if the expressions
shown in [rand.req.seedseq] are valid and have the indicated semantics,
and if `S` also meets all other requirements of this subclause
[rand.req.seedseq]. In that Table and throughout this subclause:

- `T` is the type named by `S`’s associated `result_type`;

- `q` is a value of type `S` and `r` is a value of type `S` or
  `const S`;

- `ib` and `ie` are input iterators with an unsigned integer
  `value_type` of at least 32 bits;

- `rb` and `re` are mutable random access iterators with an unsigned
  integer `value_type` of at least 32 bits;

- `ob` is an output iterator; and

- `il` is a value of type `initializer_list<T>`.

#### Uniform random bit generator requirements <a id="rand.req.urng">[rand.req.urng]</a>

A *uniform random bit generator* `g` of type `G` is a function object
returning unsigned integer values such that each value in the range of
possible results has (ideally) equal probability of being returned.

\[*Note 3*: The degree to which `g`’s results approximate the ideal is
often determined statistically. — *end note*\]

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
unsigned integer type [basic.fundamental], and `G` provides a nested
*typedef-name* `result_type` that denotes the same type as
`invoke_result_t<G&>`.

#### Random number engine requirements <a id="rand.req.eng">[rand.req.eng]</a>

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

- the *transition algorithm* $\mathsf{TA}$ by which `e`’s state is
  advanced to its *successor state* ; and

- the *generation algorithm* $\mathsf{GA}$ by which an engine’s state is
  mapped to a value of type `result_type`.

A class `E` that meets the requirements of a uniform random bit
generator [rand.req.urng] also meets the requirements of a
*random number engine* if the expressions shown in [rand.req.eng] are
valid and have the indicated semantics, and if `E` also meets all other
requirements of this subclause [rand.req.eng]. In that Table and
throughout this subclause:

- `T` is the type named by `E`’s associated `result_type`;

- `e` is a value of `E`, `v` is an lvalue of `E`, `x` and `y` are
  (possibly const) values of `E`;

- `s` is a value of `T`;

- `q` is an lvalue meeting the requirements of a seed sequence
  [rand.req.seedseq];

- `z` is a value of type `unsigned long long`;

- `os` is an lvalue of the type of some class template specialization
  `basic_ostream<charT,` `traits>`; and

- `is` is an lvalue of the type of some class template specialization
  `basic_istream<charT,` `traits>`;

where `charT` and `traits` are constrained according to [strings] and
[input.output].

`E` shall meet the *Cpp17CopyConstructible* ( [cpp17.copyconstructible])
and *Cpp17CopyAssignable* ( [cpp17.copyassignable]) requirements. These
operations shall each be of complexity no worse than .

#### Random number engine adaptor requirements <a id="rand.req.adapt">[rand.req.adapt]</a>

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

> *Effects:*
>
> The base engine is initialized as if by its default constructor.

``` cpp
bool operator==(const A& a1, const A& a2);
```

> *Returns:*
>
> `true` if `a1`’s base engine is equal to `a2`’s base engine. Otherwise
> returns `false`.

``` cpp
A::A(result_type s);
```

> *Effects:*
>
> The base engine is initialized with `s`.

``` cpp
template<class Sseq> A::A(Sseq& q);
```

> *Effects:*
>
> The base engine is initialized with `q`.

``` cpp
void seed();
```

> *Effects:*
>
> With `b` as the base engine, invokes `b.seed()`.

``` cpp
void seed(result_type s);
```

> *Effects:*
>
> With `b` as the base engine, invokes `b.seed(s)`.

``` cpp
template<class Sseq> void seed(Sseq& q);
```

> *Effects:*
>
> With `b` as the base engine, invokes `b.seed(q)`.

`A` shall also meet the following additional requirements:

- The complexity of each function shall not exceed the complexity of the
  corresponding function applied to the base engine.

- The state of `A` shall include the state of its base engine. The size
  of `A`’s state shall be no less than the size of the base engine.

- Copying `A`’s state (e.g., during copy construction or copy
  assignment) shall include copying the state of the base engine of `A`.

- The textual representation of `A` shall include the textual
  representation of its base engine.

#### Random number distribution requirements <a id="rand.req.dist">[rand.req.dist]</a>

A *random number distribution* (commonly shortened to *distribution*)
`d` of type `D` is a function object returning values that are
distributed according to an associated mathematical
*probability density function* p(z) or according to an associated
*discrete probability function* P(zᵢ). A distribution’s specification
identifies its associated probability function p(z) or P(zᵢ).

An associated probability function is typically expressed using certain
externally-supplied quantities known as the
*parameters of the distribution*. Such distribution parameters are
identified in this context by writing, for example, p(z\,|\,a,b) or
P(zᵢ\,|\,a,b), to name specific parameters, or by writing, for example,
$p(z\,|\left\{\tcode{p}\right\})$ or
$P(z_i\,|\left\{\tcode{p}\right\})$, to denote a distribution’s
parameters `p` taken as a whole.

A class `D` meets the requirements of a *random number distribution* if
the expressions shown in [rand.req.dist] are valid and have the
indicated semantics, and if `D` and its associated types also meet all
other requirements of this subclause [rand.req.dist]. In that Table and
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
  a uniform random bit generator [rand.req.urng];

- `os` is an lvalue of the type of some class template specialization
  `basic_ostream<charT,` `traits>`; and

- `is` is an lvalue of the type of some class template specialization
  `basic_istream<charT,` `traits>`;

where `charT` and `traits` are constrained according to [strings] and
[input.output].

`D` shall meet the *Cpp17CopyConstructible* ( [cpp17.copyconstructible])
and *Cpp17CopyAssignable* ( [cpp17.copyassignable]) requirements.

The sequence of numbers produced by repeated invocations of `d(g)` shall
be independent of any invocation of `os << d` or of any `const` member
function of `D` between any of the invocations of `d(g)`.

If a textual representation is written using `os << x` and that
representation is restored into the same or a different object `y` of
the same type using `is >> y`, repeated invocations of `y(g)` shall
produce the same sequence of numbers as would repeated invocations of
`x(g)`.

It is unspecified whether `D::param_type` is declared as a (nested)
`class` or via a `typedef`. In this subclause [rand], declarations of
`D::param_type` are in the form of `typedef`s for convenience of
exposition only.

`P` shall meet the *Cpp17CopyConstructible* (
[cpp17.copyconstructible]), *Cpp17CopyAssignable* (
[cpp17.copyassignable]), and *Cpp17Equality\\Comp\\arable* (
[cpp17.equalitycomparable]) requirements.

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

### Random number engine class templates <a id="rand.eng">[rand.eng]</a>

#### General <a id="rand.eng.general">[rand.eng.general]</a>

Each type instantiated from a class template specified in [rand.eng]
meets the requirements of a random number engine [rand.req.eng] type.

Except where specified otherwise, the complexity of each function
specified in [rand.eng] is constant.

Except where specified otherwise, no function described in [rand.eng]
throws an exception.

Every function described in [rand.eng] that has a function parameter `q`
of type `Sseq&` for a template type parameter named `Sseq` that is
different from type `seed_seq` throws what and when the invocation of
`q.generate` throws.

Descriptions are provided in [rand.eng] only for engine operations that
are not described in [rand.req.eng] or for operations where there is
additional semantic information. In particular, declarations for copy
constructors, for copy assignment operators, for streaming operators,
and for equality and inequality operators are not shown in the synopses.

Each template specified in [rand.eng] requires one or more
relationships, involving the value(s) of its non-type template
parameter(s), to hold. A program instantiating any of these templates is
ill-formed if any such required relationship fails to hold.

For every random number engine and for every random number engine
adaptor `X` defined in [rand.eng] and in [rand.adapt]:

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

#### Class template `linear_congruential_engine` <a id="rand.eng.lcong">[rand.eng.lcong]</a>

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
        operator<<(basic_ostream<charT, traits>& os, const linear_congruential_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, linear_congruential_engine& x);
  };
}
```

If the template parameter `m` is 0, the modulus m used throughout this
subclause  [rand.eng.lcong] is `numeric_limits<result_type>::max()` plus
1.

\[*Note 4*: m need not be representable as a value of type
`result_type`. — *end note*\]

If the template parameter `m` is not 0, the following relations shall
hold: `a < m` and `c < m`.

The textual representation consists of the value of .

``` cpp
explicit linear_congruential_engine(result_type s);
```

> *Effects:*
>
> If $c \bmod m$ is 0 and $\texttt{s} \bmod m$ is 0, sets the engine’s
> state to 1, otherwise sets the engine’s state to $\texttt{s} \bmod m$.

``` cpp
template<class Sseq> explicit linear_congruential_engine(Sseq& q);
```

> *Effects:*
>
> With $k = \left\lceil \frac{\log_2 m}{32} \right\rceil$ and a an array
> (or equivalent) of length k + 3, invokes
> `q.generate(`a + 0`, `a + k + 3`)` and then computes
> $S = \left(\sum_{j = 0}^{k - 1} a_{j + 3} \cdot 2^{32j} \right) \bmod m$.
> If $c \bmod m$ is 0 and S is 0, sets the engine’s state to 1, else
> sets the engine’s state to S.

#### Class template `mersenne_twister_engine` <a id="rand.eng.mers">[rand.eng.mers]</a>

A `mersenne_twister_engine` random number engine

produces unsigned integer random numbers in the closed interval
$[0,2^w-1]$. The state of a `mersenne_twister_engine` object `x` is of
size n and consists of a sequence X of n values of the type delivered by
`x`; all subscripts applied to X are to be taken modulo n.

The transition algorithm employs a twisted generalized feedback shift
register defined by shift values n and m, a twist value r, and a
conditional xor-mask a. To improve the uniformity of the result, the
bits of the raw shift register are additionally *tempered* (i.e.,
scrambled) according to a bit-scrambling matrix defined by values u, d,
s, b, t, c, and $\ell$.

The state transition is performed as follows:

- Concatenate the upper w-r bits of $X_{i-n}$ with the lower r bits of
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
    static constexpr result_type max() { return  $2^w - 1$; }
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
        operator<<(basic_ostream<charT, traits>& os, const mersenne_twister_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, mersenne_twister_engine& x);
  };
}
```

The following relations shall hold: `0 < m`, `m <= n`, `2u < w`,
`r <= w`, `u <= w`, `s <= w`, `t <= w`, `l <= w`,
`w <= numeric_limits<UIntType>::digits`, `a <= (1u<<w) - 1u`,
`b <= (1u<<w) - 1u`, `c <= (1u<<w) - 1u`, `d <= (1u<<w) - 1u`, and
`f <= (1u<<w) - 1u`.

The textual representation of consists of the values of
$X_{i - n}, \dotsc, X_{i - 1}$, in that order.

``` cpp
explicit mersenne_twister_engine(result_type value);
```

> *Effects:*
>
> Sets $X_{-n}$ to $\texttt{value} \bmod 2^w$. Then, iteratively for
> $i = 1 - n, \dotsc, -1$, sets Xᵢ to $$%
>  \bigl[f \cdot
>        \bigl(X_{i-1} \xor \bigl(X_{i-1} \rightshift (w-2)\bigr)
>        \bigr)
>        + i \bmod n
>  \bigr] \bmod 2^w
> \; \mbox{.}$$
>
> *Complexity:*
>
> 𝑂(n).

``` cpp
template<class Sseq> explicit mersenne_twister_engine(Sseq& q);
```

> *Effects:*
>
> With $k = \left\lceil w / 32 \right\rceil$ and a an array (or
> equivalent) of length n ⋅ k, invokes `q.generate(`a+0`, `a+n ⋅ k`)`
> and then, iteratively for $i = -n,\dotsc,-1$, sets Xᵢ to
> $\left(\sum_{j=0}^{k-1}a_{k(i+n)+j} \cdot 2^{32j} \right) \bmod 2^w$.
> Finally, if the most significant w-r bits of $X_{-n}$ are zero, and if
> each of the other resulting Xᵢ is 0, changes $X_{-n}$ to $2^{w-1}$.

#### Class template `subtract_with_carry_engine` <a id="rand.eng.sub">[rand.eng.sub]</a>

A `subtract_with_carry_engine` random number engine produces unsigned
integer random numbers.

The state of a `subtract_with_carry_engine` object `x` is of size , and
consists of a sequence X of r integer values $0 \leq X_i < m \,= 2^w$;
all subscripts applied to X are to be taken modulo r. The state
additionally consists of an integer c (known as the *carry*) whose value
is either 0 or 1.

The state transition is performed as follows:

- Let $Y = X_{i-s} - X_{i-r} - c$.

- Set Xᵢ to $y = Y \bmod m$. Set c to 1 if Y < 0, otherwise set c to 0.

\[*Note 5*: This algorithm corresponds to a modular linear function of
the form $\mathsf{TA}(\state{x}{i}) = (a \cdot \state{x}{i}) \bmod b$,
where b is of the form $m^r - m^s + 1$ and
a = b - (b - 1) / m. — *end note*\]

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
    static constexpr result_type max() { return $m - 1$; }
    static constexpr result_type default_seed = 19780503u;

    // constructors and seeding functions
    subtract_with_carry_engine() : subtract_with_carry_engine(default_seed) {}
    explicit subtract_with_carry_engine(result_type value);
    template<class Sseq> explicit subtract_with_carry_engine(Sseq& q);
    void seed(result_type value = default_seed);
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
        operator<<(basic_ostream<charT, traits>& os, const subtract_with_carry_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, subtract_with_carry_engine& x);
  };
}
```

The following relations shall hold: `0u < s`, `s < r`, `0 < w`, and
`w <= numeric_limits<UIntType>::digits`.

The textual representation consists of the values of
$X_{i-r}, \dotsc, X_{i-1}$, in that order, followed by c.

``` cpp
explicit subtract_with_carry_engine(result_type value);
```

> *Effects:*
>
> Sets the values of $X_{-r}, \dotsc, X_{-1}$, in that order, as
> specified below. If $X_{-1}$ is then 0, sets c to 1; otherwise sets c
> to 0.
>
> To set the values Xₖ, first construct `e`, a
> `linear_congruential_engine` object, as if by the following
> definition:
>
> ``` cpp
> linear_congruential_engine<result_type,
>                           40014u,0u,2147483563u> e(value == 0u ? default_seed : value);
> ```
>
> Then, to set each Xₖ, obtain new values $z_0, \dotsc, z_{n-1}$ from
> $n = \lceil w/32 \rceil$ successive invocations of `e`. Set Xₖ to
> $\left( \sum_{j=0}^{n-1} z_j \cdot 2^{32j}\right) \bmod m$.
>
> *Complexity:*
>
> Exactly $n \cdot \texttt{r}$ invocations of `e`.

``` cpp
template<class Sseq> explicit subtract_with_carry_engine(Sseq& q);
```

> *Effects:*
>
> With $k = \left\lceil w / 32 \right\rceil$ and a an array (or
> equivalent) of length r ⋅ k, invokes
> `q.generate(`a + 0`, `a + r ⋅ k`)` and then, iteratively for
> $i = -r, \dotsc, -1$, sets Xᵢ to
> $\left(\sum_{j=0}^{k-1}a_{k(i+r)+j} \cdot 2^{32j} \right) \bmod m$. If
> $X_{-1}$ is then 0, sets c to 1; otherwise sets c to 0.

### Random number engine adaptor class templates <a id="rand.adapt">[rand.adapt]</a>

#### In general <a id="rand.adapt.general">[rand.adapt.general]</a>

Each type instantiated from a class template specified in this
subclause  [rand.adapt] meets the requirements of a random number engine
adaptor [rand.req.adapt] type.

Except where specified otherwise, the complexity of each function
specified in this subclause  [rand.adapt] is constant.

Except where specified otherwise, no function described in this
subclause  [rand.adapt] throws an exception.

Every function described in this subclause  [rand.adapt] that has a
function parameter `q` of type `Sseq&` for a template type parameter
named `Sseq` that is different from type `seed_seq` throws what and when
the invocation of `q.generate` throws.

Descriptions are provided in this subclause  [rand.adapt] only for
adaptor operations that are not described in subclause  [rand.req.adapt]
or for operations where there is additional semantic information. In
particular, declarations for copy constructors, for copy assignment
operators, for streaming operators, and for equality and inequality
operators are not shown in the synopses.

Each template specified in this subclause  [rand.adapt] requires one or
more relationships, involving the value(s) of its non-type template
parameter(s), to hold. A program instantiating any of these templates is
ill-formed if any such required relationship fails to hold.

#### Class template `discard_block_engine` <a id="rand.adapt.disc">[rand.adapt.disc]</a>

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
    using result_type = typename Engine::result_type;

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
        operator<<(basic_ostream<charT, traits>& os, const discard_block_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, discard_block_engine& x);

  private:
    Engine e;   // exposition only
    size_t n;   // exposition only
  };
}
```

The following relations shall hold: `0 < r` and `r <= p`.

The textual representation consists of the textual representation of `e`
followed by the value of `n`.

In addition to its behavior pursuant to subclause  [rand.req.adapt],
each constructor that is not a copy constructor sets `n` to 0.

#### Class template `independent_bits_engine` <a id="rand.adapt.ibits">[rand.adapt.ibits]</a>

An `independent_bits_engine` random number engine adaptor combines
random numbers that are produced by some base engine e, so as to produce
random numbers with a specified number of bits w. The state of an
`independent_bits_engine` engine adaptor object `x` consists of the
state of its base engine `e`; the size of the state is the size of e’s
state.

The transition and generation algorithms are described in terms of the
following integral constants:

- Let $R = \tcode{e.max() - e.min() + 1}$ and
  $m = \left\lfloor \log_2 R \right\rfloor$.

- With n as determined below, let
  $w_0 = \left\lfloor w / n \right\rfloor$, $n_0 = n - w \bmod n$,
  $y_0 = 2^{w_0} \left\lfloor R / 2^{w_0} \right\rfloor$, and
  $y_1 = 2^{w_0 + 1} \left\lfloor R / 2^{w_0 + 1} \right\rfloor$.

- Let $n = \left\lceil w / m \right\rceil$ if and only if the relation
  $R - y_0 \leq \left\lfloor y_0 / n \right\rfloor$ holds as a result.
  Otherwise let $n = 1 + \left\lceil w / m \right\rceil$.

\[*Note 6*: The relation w = n₀ w₀ + (n - n₀)(w₀ + 1) always
holds. — *end note*\]

The transition algorithm is carried out by invoking `e()` as often as
needed to obtain n₀ values less than $y_0 + \tcode{e.min()}$ and n - n₀
values less than $y_1 + \tcode{e.min()}$.

The generation algorithm uses the values produced while advancing the
state as described above to yield a quantity S obtained as if by the
following algorithm:

``` cpp
$S$ = 0;
for ($k$ = $0$; $k \neq n_0$; $k$ += $1$)  {
 do $u$ = e() - e.min(); while ($u \ge y_0$);
 $S$ = $2^{w_0} \cdot S + u \bmod 2^{w_0}$;
}
for ($k$ = $n_0$; $k \neq n$; $k$ += $1$)  {
 do $u$ = e() - e.min(); while ($u \ge y_1$);
 $S$ = $2^{w_0 + 1} \cdot S + u \bmod 2^{w_0 + 1}$;
}
```

``` cpp
template<class Engine, size_t w, class UIntType>
  class independent_bits_engine {
  public:
    // types
    using result_type = UIntType;

    // engine characteristics
    static constexpr result_type min() { return 0; }
    static constexpr result_type max() { return $2^w - 1$; }

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
        operator<<(basic_ostream<charT, traits>& os, const independent_bits_engine& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, independent_bits_engine& x);

  private:
    Engine e;   // exposition only
  };
```

The following relations shall hold: `0 < w` and
`w <= numeric_limits<result_type>::digits`.

The textual representation consists of the textual representation of
`e`.

#### Class template `shuffle_order_engine` <a id="rand.adapt.shuf">[rand.adapt.shuf]</a>

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

- Set Y to $V_j$ and then set $V_j$ to $\tcode{e()}$.

The generation algorithm yields the last value of `Y` produced while
advancing `e`’s state as described above.

``` cpp
namespace std {
  template<class Engine, size_t k>
  class shuffle_order_engine {
  public:
    // types
    using result_type = typename Engine::result_type;

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

In addition to its behavior pursuant to subclause  [rand.req.adapt],
each constructor that is not a copy constructor initializes
$\tcode{V[0]}, \dotsc, \tcode{V[k-1]}$ and Y, in that order, with values
returned by successive invocations of `e()`.

### Engines and engine adaptors with predefined parameters <a id="rand.predef">[rand.predef]</a>

``` cpp
using minstd_rand0 =
      linear_congruential_engine<uint_fast32_t, 16'807, 0, 2'147'483'647>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `minstd_rand0` produces the value 1043618065.

``` cpp
using minstd_rand =
      linear_congruential_engine<uint_fast32_t, 48'271, 0, 2'147'483'647>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `minstd_rand` produces the value 399268537.

``` cpp
using mt19937 =
      mersenne_twister_engine<uint_fast32_t, 32, 624, 397, 31,
       0x9908'b0df, 11, 0xffff'ffff, 7, 0x9d2c'5680, 15, 0xefc6'0000, 18, 1'812'433'253>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `mt19937` produces the value 4123659995.

``` cpp
using mt19937_64 =
      mersenne_twister_engine<uint_fast64_t, 64, 312, 156, 31,
       0xb502'6f5a'a966'19e9, 29, 0x5555'5555'5555'5555, 17,
       0x71d6'7fff'eda6'0000, 37, 0xfff7'eee0'0000'0000, 43, 6'364'136'223'846'793'005>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `mt19937_64` produces the value 9981545732273789042.

``` cpp
using ranlux24_base =
      subtract_with_carry_engine<uint_fast32_t, 24, 10, 24>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `ranlux24_base` produces the value 7937952.

``` cpp
using ranlux48_base =
      subtract_with_carry_engine<uint_fast64_t, 48, 5, 12>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `ranlux48_base` produces the value 61839128582725.

``` cpp
using ranlux24 = discard_block_engine<ranlux24_base, 223, 23>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `ranlux24` produces the value 9901578.

``` cpp
using ranlux48 = discard_block_engine<ranlux48_base, 389, 11>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `ranlux48` produces the value 249142670248501.

``` cpp
using knuth_b = shuffle_order_engine<minstd_rand0,256>;
```

> The $10000^\text{th}$ consecutive invocation of a default-constructed
> object of type `knuth_b` produces the value 1112339016.

``` cpp
using default_random_engine = \textit{\impldef{type of default_random_engine}};
```

> *Remarks:*
>
> The choice of engine type named by this is *implementation-defined*.
>
> \[*Note 4*: The implementation can select this type on the basis of
> performance, size, quality, or any combination of such factors, so as
> to provide at least acceptable engine behavior for relatively casual,
> inexpert, and/or lightweight use. Because different implementations
> can select different underlying engine types, code that uses this need
> not generate identical sequences across
> implementations. — *end note*\]

### Class `random_device` <a id="rand.device">[rand.device]</a>

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

> *Throws:*
>
> A value of an *implementation-defined* type derived from `exception`
> if the `random_device` cannot be initialized.
>
> *Remarks:*
>
> The semantics of the `token` parameter and the token value used by the
> default constructor are *implementation-defined*.
>
> The parameter is intended to allow an implementation to differentiate
> between different sources of randomness.

``` cpp
double entropy() const noexcept;
```

> *Returns:*
>
> If the implementation employs a random number engine, returns 0.0.
> Otherwise, returns an entropy estimate
>
> If a device has n states whose respective probabilities are
> $P_0, \dotsc, P_{n-1}$, the device entropy S is defined as  
> $S = - \sum_{i=0}^{n-1} P_i \cdot \log P_i$.
>
> for the random numbers returned by `operator()`, in the range `min()`
> to $\log_2( \texttt{max()}+1)$.

``` cpp
result_type operator()();
```

> *Returns:*
>
> A nondeterministic random value, uniformly distributed between `min()`
> and `max()` (inclusive). It is *implementation-defined* how these
> values are generated.
>
> *Throws:*
>
> A value of an *implementation-defined* type derived from `exception`
> if a random number cannot be obtained.

### Utilities <a id="rand.util">[rand.util]</a>

#### Class `seed_seq` <a id="rand.util.seedseq">[rand.util.seedseq]</a>

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

> *Ensures:*
>
> `v.empty()` is `true`.

``` cpp
template<class T>
  seed_seq(initializer_list<T> il);
```

> `T` is an integer type.
>
> *Effects:*
>
> Same as `seed_seq(il.begin(), il.end())`.

``` cpp
template<class InputIterator>
  seed_seq(InputIterator begin, InputIterator end);
```

> *Mandates:*
>
> `iterator_traits<InputIterator>::value_type` is an integer type.
>
> *Preconditions:*
>
> `InputIterator` meets the *Cpp17InputIterator*
> requirements\[input.iterators\].
>
> *Effects:*
>
> Initializes `v` by the following algorithm:
>
> ``` cpp
> for (InputIterator s = begin; s != end; ++s)
>  v.push_back((*s)$\bmod 2^{32}$);
> ```

``` cpp
template<class RandomAccessIterator>
  void generate(RandomAccessIterator begin, RandomAccessIterator end);
```

> *Mandates:*
>
> `iterator_traits<RandomAccessIterator>::value_type` is an unsigned
> integer type capable of accommodating 32-bit quantities.
>
> *Preconditions:*
>
> `RandomAccessIterator` meets the *Cpp17RandomAccessIterator*
> requirements\[random.access.iterators\] and the requirements of a
> mutable iterator.
>
> *Effects:*
>
> Does nothing if `begin == end`. Otherwise, with
> $s = \texttt{v.size()}$ and $n = \texttt{end} - \texttt{begin}$, fills
> the supplied range $[\texttt{begin},\texttt{end})$ according to the
> following algorithm in which each operation is to be carried out
> modulo $2^{32}$, each indexing operator applied to `begin` is to be
> taken modulo n, and T(x) is defined as $x \xor (x \rightshift 27)$:
>
> - By way of initialization, set each element of the range to the value
>   `0x8b8b8b8b`. Additionally, for use in subsequent steps, let
>   p = (n - t) / 2 and let q = p + t, where $$%
>        t = (n \ge 623) \mbox{ ? } 11 \mbox{ : } (n \ge 68) \mbox{ ? } 7 \mbox{ : } (n \ge 39) \mbox{ ? } 5 \mbox{ : } (n \ge 7) \mbox{ ? } 3 \mbox{ : } (n - 1)/2;$$
>
> - With m as the larger of s + 1 and n, transform the elements of the
>   range: iteratively for $k = 0, \dotsc, m - 1$, calculate values
>   $$\begin{aligned}
>        r_1 & = &
>          1664525 \cdot T(    \texttt{begin[}k\texttt{]}
>                         \xor \texttt{begin[}k+p\texttt{]}
>                         \xor \texttt{begin[}k-1 \texttt{]}
>                         )
>        \\
>        r_2 & = & r_1 + \left\{
>          \begin{array}{cl}
>            s                                  & \mbox{,  } k = 0
>            \\
>            k \bmod n + \texttt{v[}k-1\texttt{]} & \mbox{,  } 0 < k \le s
>            \\
>            k \bmod n                          & \mbox{,  } s < k
>          \end{array}
>        \right.
>      
>   \end{aligned}$$ and, in order, increment `begin[`k+p`]` by r₁,
>   increment `begin[`k+q`]` by r₂, and set `begin[`k`]` to r₂.
>
> - Transform the elements of the range again, beginning where the
>   previous step ended: iteratively for $k = m, \dotsc, m + n - 1$,
>   calculate values $$\begin{aligned}
>        r_3 & = &
>          1566083941 \cdot T( \texttt{begin[}k  \texttt{]}
>                            + \texttt{begin[}k+p\texttt{]}
>                            + \texttt{begin[}k-1\texttt{]}
>                            )
>        \\
>        r_4 & = & r_3 - (k \bmod n)
>      
>   \end{aligned}$$ and, in order, update `begin[`k+p`]` by xoring it
>   with r₃, update `begin[`k+q`]` by xoring it with r₄, and set
>   `begin[`k`]` to r₄.
>
> *Throws:*
>
> What and when `RandomAccessIterator` operations of `begin` and `end`
> throw.

``` cpp
size_t size() const noexcept;
```

> *Returns:*
>
> The number of 32-bit units that would be returned by a call to
> `param()`.
>
> *Complexity:*
>
> Constant time.

``` cpp
template<class OutputIterator>
  void param(OutputIterator dest) const;
```

> *Mandates:*
>
> Values of type `result_type` are
> writable\[iterator.requirements.general\] to `dest`.
>
> *Preconditions:*
>
> `OutputIterator` meets the *Cpp17OutputIterator*
> requirements\[output.iterators\].
>
> *Effects:*
>
> Copies the sequence of prepared 32-bit units to the given destination,
> as if by executing the following statement:
>
> ``` cpp
> copy(v.begin(), v.end(), dest);
> ```
>
> *Throws:*
>
> What and when `OutputIterator` operations of `dest` throw.

#### Function template `generate_canonical` <a id="rand.util.canonical">[rand.util.canonical]</a>

``` cpp
template<class RealType, size_t bits, class URBG>
  RealType generate_canonical(URBG& g);
```

> *Effects:*
>
> Invokes `g()` k times to obtain values $g_0, \dotsc, g_{k-1}$,
> respectively. Calculates a quantity
> $$S = \sum_{i=0}^{k-1} (g_i - \texttt{g.min()})
>                         \cdot R^i$$ using arithmetic of type
> `RealType`.
>
> *Returns:*
>
> $S / R^k$.
>
> \[*Note 5*: $0 \leq S / R^k < 1$. — *end note*\]
>
> *Throws:*
>
> What and when `g` throws.
>
> *Complexity:*
>
> Exactly $k = \max(1, \left\lceil b / \log_2 R \right\rceil)$
> invocations of `g`, where b
>
> b is introduced to avoid any attempt to produce more bits of
> randomness than can be held in `RealType`.
>
> is the lesser of `numeric_limits<RealType>::digits` and `bits`, and R
> is the value of $\texttt{g.max()} - \texttt{g.min()} + 1$.
>
> \[*Note 6*: If the values gᵢ produced by `g` are uniformly
> distributed, the instantiation’s results are distributed as uniformly
> as possible. Obtaining a value in this way can be a useful step in the
> process of transforming a value generated by a uniform random bit
> generator into a value that can be delivered by a random number
> distribution. — *end note*\]

### Random number distribution class templates <a id="rand.dist">[rand.dist]</a>

#### In general <a id="rand.dist.general">[rand.dist.general]</a>

Each type instantiated from a class template specified in this
subclause  [rand.dist] meets the requirements of a random number
distribution [rand.req.dist] type.

Descriptions are provided in this subclause  [rand.dist] only for
distribution operations that are not described in [rand.req.dist] or for
operations where there is additional semantic information. In
particular, declarations for copy constructors, for copy assignment
operators, for streaming operators, and for equality and inequality
operators are not shown in the synopses.

The algorithms for producing each of the specified distributions are
*implementation-defined*.

The value of each probability density function p(z) and of each discrete
probability function P(zᵢ) specified in this subclause is 0 everywhere
outside its stated domain.

#### Uniform distributions <a id="rand.dist.uni">[rand.dist.uni]</a>

##### Class template `uniform_int_distribution` <a id="rand.dist.uni.int">[rand.dist.uni.int]</a>

A `uniform_int_distribution` random number distribution produces random
integers i, a ≤ i ≤ b, distributed according to the constant discrete
probability function $$P(i\,|\,a,b) = 1 / (b - a + 1) \text{ .}$$

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
        operator<<(basic_ostream<charT, traits>& os, const uniform_int_distribution& x);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, uniform_int_distribution& x);
  };
}
```

``` cpp
explicit uniform_int_distribution(IntType a, IntType b = numeric_limits<IntType>::max());
```

> *Preconditions:*
>
> $\texttt{a} \leq \texttt{b}$.
>
> *Remarks:*
>
> `a` and `b` correspond to the respective parameters of the
> distribution.

``` cpp
result_type a() const;
```

> *Returns:*
>
> The value of the `a` parameter with which the object was constructed.

``` cpp
result_type b() const;
```

> *Returns:*
>
> The value of the `b` parameter with which the object was constructed.

##### Class template `uniform_real_distribution` <a id="rand.dist.uni.real">[rand.dist.uni.real]</a>

A `uniform_real_distribution` random number distribution produces random
numbers x, a ≤ x < b, distributed according to the constant probability
density function $$p(x\,|\,a,b) = 1 / (b - a) \text{ .}$$

\[*Note 7*: This implies that p(x\,|\,a,b) is undefined when
`a == b`. — *end note*\]

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

> *Preconditions:*
>
> $\texttt{a} \leq \texttt{b}$ and
> $\texttt{b} - \texttt{a} \leq \texttt{numeric_limits<RealType>::max()}$.
>
> *Remarks:*
>
> `a` and `b` correspond to the respective parameters of the
> distribution.

``` cpp
result_type a() const;
```

> *Returns:*
>
> The value of the `a` parameter with which the object was constructed.

``` cpp
result_type b() const;
```

> *Returns:*
>
> The value of the `b` parameter with which the object was constructed.

#### Bernoulli distributions <a id="rand.dist.bern">[rand.dist.bern]</a>

##### Class `bernoulli_distribution` <a id="rand.dist.bern.bernoulli">[rand.dist.bern.bernoulli]</a>

A `bernoulli_distribution` random number distribution produces `bool`
values b distributed according to the discrete probability function
$$P(b\,|\,p) = \left\{ \begin{array}{ll}
                          p     & \text{ if $b = \tcode{true}$, or} \\
                          1 - p & \text{ if $b = \tcode{false}$.}
                          \end{array}\right.$$

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

> *Preconditions:*
>
> $0 \leq \texttt{p} \leq 1$.
>
> *Remarks:*
>
> `p` corresponds to the parameter of the distribution.

``` cpp
double p() const;
```

> *Returns:*
>
> The value of the `p` parameter with which the object was constructed.

##### Class template `binomial_distribution` <a id="rand.dist.bern.bin">[rand.dist.bern.bin]</a>

A `binomial_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
$$P(i\,|\,t,p) = \binom{t}{i} \cdot p^i \cdot (1-p)^{t-i} \text{ .}$$

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

> *Preconditions:*
>
> $0 \leq \texttt{p} \leq 1$ and $0 \leq \texttt{t}$.
>
> *Remarks:*
>
> `t` and `p` correspond to the respective parameters of the
> distribution.

``` cpp
IntType t() const;
```

> *Returns:*
>
> The value of the `t` parameter with which the object was constructed.

``` cpp
double p() const;
```

> *Returns:*
>
> The value of the `p` parameter with which the object was constructed.

##### Class template `geometric_distribution` <a id="rand.dist.bern.geo">[rand.dist.bern.geo]</a>

A `geometric_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
$$P(i\,|\,p) = p \cdot (1-p)^{i} \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{p} < 1$.
>
> *Remarks:*
>
> `p` corresponds to the parameter of the distribution.

``` cpp
double p() const;
```

> *Returns:*
>
> The value of the `p` parameter with which the object was constructed.

##### Class template `negative_binomial_distribution` <a id="rand.dist.bern.negbin">[rand.dist.bern.negbin]</a>

A `negative_binomial_distribution` random number distribution produces
random integers i ≥ 0 distributed according to the discrete probability
function
$$P(i\,|\,k,p) = \binom{k+i-1}{i} \cdot p^k \cdot (1-p)^i \text{ .}$$

\[*Note 8*: This implies that P(i\,|\,k,p) is undefined when
`p == 1`. — *end note*\]

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

> *Preconditions:*
>
> $0 < \texttt{p} \leq 1$ and $0 < \texttt{k}$.
>
> *Remarks:*
>
> `k` and `p` correspond to the respective parameters of the
> distribution.

``` cpp
IntType k() const;
```

> *Returns:*
>
> The value of the `k` parameter with which the object was constructed.

``` cpp
double p() const;
```

> *Returns:*
>
> The value of the `p` parameter with which the object was constructed.

#### Poisson distributions <a id="rand.dist.pois">[rand.dist.pois]</a>

##### Class template `poisson_distribution` <a id="rand.dist.pois.poisson">[rand.dist.pois.poisson]</a>

A `poisson_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
$$P(i\,|\,\mu) = \frac{e^{-\mu} \mu^{i}}{i\,!} \text{ .}$$ The
distribution parameter μ is also known as this distribution’s *mean* .

``` cpp
template<class IntType = int>
  class poisson_distribution
  {
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
```

``` cpp
explicit poisson_distribution(double mean);
```

> *Preconditions:*
>
> $0 < \texttt{mean}$.
>
> *Remarks:*
>
> `mean` corresponds to the parameter of the distribution.

``` cpp
double mean() const;
```

> *Returns:*
>
> The value of the `mean` parameter with which the object was
> constructed.

##### Class template `exponential_distribution` <a id="rand.dist.pois.exp">[rand.dist.pois.exp]</a>

An `exponential_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
$$p(x\,|\,\lambda) = \lambda e^{-\lambda x} \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{lambda}$.
>
> *Remarks:*
>
> `lambda` corresponds to the parameter of the distribution.

``` cpp
RealType lambda() const;
```

> *Returns:*
>
> The value of the `lambda` parameter with which the object was
> constructed.

##### Class template `gamma_distribution` <a id="rand.dist.pois.gamma">[rand.dist.pois.gamma]</a>

A `gamma_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
$$p(x\,|\,\alpha,\beta) =
     \frac{e^{-x/\beta}}{\beta^{\alpha} \cdot \Gamma(\alpha)} \, \cdot \, x^{\, \alpha-1}
     \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{alpha}$ and $0 < \texttt{beta}$.
>
> *Remarks:*
>
> `alpha` and `beta` correspond to the parameters of the distribution.

``` cpp
RealType alpha() const;
```

> *Returns:*
>
> The value of the `alpha` parameter with which the object was
> constructed.

``` cpp
RealType beta() const;
```

> *Returns:*
>
> The value of the `beta` parameter with which the object was
> constructed.

##### Class template `weibull_distribution` <a id="rand.dist.pois.weibull">[rand.dist.pois.weibull]</a>

A `weibull_distribution` random number distribution produces random
numbers x ≥ 0 distributed according to the probability density function
$$p(x\,|\,a,b) = \frac{a}{b}
     \cdot \left(\frac{x}{b}\right)^{a-1}
     \cdot \, \exp\left( -\left(\frac{x}{b}\right)^a\right)
     \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{a}$ and $0 < \texttt{b}$.
>
> *Remarks:*
>
> `a` and `b` correspond to the respective parameters of the
> distribution.

``` cpp
RealType a() const;
```

> *Returns:*
>
> The value of the `a` parameter with which the object was constructed.

``` cpp
RealType b() const;
```

> *Returns:*
>
> The value of the `b` parameter with which the object was constructed.

##### Class template `extreme_value_distribution` <a id="rand.dist.pois.extreme">[rand.dist.pois.extreme]</a>

An `extreme_value_distribution` random number distribution produces
random numbers x distributed according to the probability density
function

$$p(x\,|\,a,b) = \frac{1}{b}
     \cdot \exp\left(\frac{a-x}{b} - \exp\left(\frac{a-x}{b}\right)\right)
     \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{b}$.
>
> *Remarks:*
>
> `a` and `b` correspond to the respective parameters of the
> distribution.

``` cpp
RealType a() const;
```

> *Returns:*
>
> The value of the `a` parameter with which the object was constructed.

``` cpp
RealType b() const;
```

> *Returns:*
>
> The value of the `b` parameter with which the object was constructed.

#### Normal distributions <a id="rand.dist.norm">[rand.dist.norm]</a>

##### Class template `normal_distribution` <a id="rand.dist.norm.normal">[rand.dist.norm.normal]</a>

A `normal_distribution` random number distribution produces random
numbers x distributed according to the probability density function $$%
 p(x\,|\,\mu,\sigma)
      = \frac{1}{\sigma \sqrt{2\pi}}
        \cdot
        % e^{-(x-\mu)^2 / (2\sigma^2)}
        \exp{\left(- \, \frac{(x - \mu)^2}
                             {2 \sigma^2}
             \right)
            }
 \text{ .}$$ The distribution parameters μ and σ are also known as this
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

> *Preconditions:*
>
> $0 < \texttt{stddev}$.
>
> *Remarks:*
>
> `mean` and `stddev` correspond to the respective parameters of the
> distribution.

``` cpp
RealType mean() const;
```

> *Returns:*
>
> The value of the `mean` parameter with which the object was
> constructed.

``` cpp
RealType stddev() const;
```

> *Returns:*
>
> The value of the `stddev` parameter with which the object was
> constructed.

##### Class template `lognormal_distribution` <a id="rand.dist.norm.lognormal">[rand.dist.norm.lognormal]</a>

A `lognormal_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
$$p(x\,|\,m,s) = \frac{1}{s x \sqrt{2 \pi}}
     \cdot \exp{\left(-\frac{(\ln{x} - m)^2}{2 s^2}\right)}
     \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{s}$.
>
> *Remarks:*
>
> `m` and `s` correspond to the respective parameters of the
> distribution.

``` cpp
RealType m() const;
```

> *Returns:*
>
> The value of the `m` parameter with which the object was constructed.

``` cpp
RealType s() const;
```

> *Returns:*
>
> The value of the `s` parameter with which the object was constructed.

##### Class template `chi_squared_distribution` <a id="rand.dist.norm.chisq">[rand.dist.norm.chisq]</a>

A `chi_squared_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
$$p(x\,|\,n) = \frac{x^{(n/2)-1} \cdot e^{-x/2}}{\Gamma(n/2) \cdot 2^{n/2}} \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{n}$.
>
> *Remarks:*
>
> `n` corresponds to the parameter of the distribution.

``` cpp
RealType n() const;
```

> *Returns:*
>
> The value of the `n` parameter with which the object was constructed.

##### Class template `cauchy_distribution` <a id="rand.dist.norm.cauchy">[rand.dist.norm.cauchy]</a>

A `cauchy_distribution` random number distribution produces random
numbers x distributed according to the probability density function
$$p(x\,|\,a,b) = \left(\pi b \left(1 + \left(\frac{x-a}{b} \right)^2 \, \right)\right)^{-1} \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{b}$.
>
> *Remarks:*
>
> `a` and `b` correspond to the respective parameters of the
> distribution.

``` cpp
RealType a() const;
```

> *Returns:*
>
> The value of the `a` parameter with which the object was constructed.

``` cpp
RealType b() const;
```

> *Returns:*
>
> The value of the `b` parameter with which the object was constructed.

##### Class template `fisher_f_distribution` <a id="rand.dist.norm.f">[rand.dist.norm.f]</a>

A `fisher_f_distribution` random number distribution produces random
numbers $x \ge 0$ distributed according to the probability density
function
$$p(x\,|\,m,n) = \frac{\Gamma\big((m+n)/2\big)}{\Gamma(m/2) \; \Gamma(n/2)}
     \cdot \left(\frac{m}{n}\right)^{m/2}
     \cdot x^{(m/2)-1}
     \cdot \left(1 + \frac{m x}{n}\right)^{-(m + n)/2}
     \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{m}$ and $0 < \texttt{n}$.
>
> *Remarks:*
>
> `m` and `n` correspond to the respective parameters of the
> distribution.

``` cpp
RealType m() const;
```

> *Returns:*
>
> The value of the `m` parameter with which the object was constructed.

``` cpp
RealType n() const;
```

> *Returns:*
>
> The value of the `n` parameter with which the object was constructed.

##### Class template `student_t_distribution` <a id="rand.dist.norm.t">[rand.dist.norm.t]</a>

A `student_t_distribution` random number distribution produces random
numbers x distributed according to the probability density function
$$p(x\,|\,n) = \frac{1}{\sqrt{n \pi}}
     \cdot \frac{\Gamma\big((n+1)/2\big)}{\Gamma(n/2)}
     \cdot \left(1 + \frac{x^2}{n} \right)^{-(n+1)/2}
     \text{ .}$$

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

> *Preconditions:*
>
> $0 < \texttt{n}$.
>
> *Remarks:*
>
> `n` corresponds to the parameter of the distribution.

``` cpp
RealType n() const;
```

> *Returns:*
>
> The value of the `n` parameter with which the object was constructed.

#### Sampling distributions <a id="rand.dist.samp">[rand.dist.samp]</a>

##### Class template `discrete_distribution` <a id="rand.dist.samp.discrete">[rand.dist.samp.discrete]</a>

A `discrete_distribution` random number distribution produces random
integers i, 0 ≤ i < n, distributed according to the discrete probability
function $$P(i \,|\, p_0, \dotsc, p_{n-1}) = p_i \text{ .}$$

Unless specified otherwise, the distribution parameters are calculated
as: pₖ = {wₖ / S} for $k = 0, \dotsc, n - 1$, in which the values wₖ,
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

> *Effects:*
>
> Constructs a `discrete_distribution` object with n = 1 and p₀ = 1.
>
> \[*Note 7*: Such an object will always deliver the value
> 0. — *end note*\]

``` cpp
template<class InputIterator>
  discrete_distribution(InputIterator firstW, InputIterator lastW);
```

> *Mandates:*
>
> `is_convertible_v<iterator_traits<InputIterator>::value_type, double>`
> is `true`.
>
> *Preconditions:*
>
> `InputIterator` meets the *Cpp17InputIterator*
> requirements\[input.iterators\]. If `firstW == lastW`, let n = 1 and
> w₀ = 1. Otherwise, $\bigl[\texttt{firstW}, \texttt{lastW}\bigr)$ forms
> a sequence w of length n > 0.
>
> *Effects:*
>
> Constructs a `discrete_distribution` object with probabilities given
> by the formula above.

``` cpp
discrete_distribution(initializer_list<double> wl);
```

> *Effects:*
>
> Same as `discrete_distribution(wl.begin(), wl.end())`.

``` cpp
template<class UnaryOperation>
  discrete_distribution(size_t nw, double xmin, double xmax, UnaryOperation fw);
```

> *Mandates:*
>
> `is_invocable_r_v<double, UnaryOperation&, double>` is `true`.
>
> *Preconditions:*
>
> If $\texttt{nw} = 0$, let n = 1, otherwise let $n = \texttt{nw}$. The
> relation $0 < \delta = (\texttt{xmax} - \texttt{xmin}) / n$ holds.
>
> *Effects:*
>
> Constructs a `discrete_distribution` object with probabilities given
> by the formula above, using the following values: If
> $\texttt{nw} = 0$, let w₀ = 1. Otherwise, let
> $w_k = \texttt{fw}(\texttt{xmin} + k \cdot \delta + \delta / 2)$ for
> $k = 0, \dotsc, n - 1$.
>
> *Complexity:*
>
> The number of invocations of `fw` does not exceed n.

``` cpp
vector<double> probabilities() const;
```

> *Returns:*
>
> A `vector<double>` whose `size` member returns n and whose
> `operator[]` member returns pₖ when invoked with argument k for
> $k = 0, \dotsc, n - 1$.

##### Class template `piecewise_constant_distribution` <a id="rand.dist.samp.pconst">[rand.dist.samp.pconst]</a>

A `piecewise_constant_distribution` random number distribution produces
random numbers x, b₀ ≤ x < bₙ, uniformly distributed over each
subinterval $[ b_i, b_{i+1} )$ according to the probability density
function
$$p(x \,|\, b_0, \dotsc, b_n, \; \rho_0, \dotsc, \rho_{n-1}) = \rho_i
   \text{ , for $b_i \le x < b_{i+1}$.}$$

The n + 1 distribution parameters bᵢ, also known as this distribution’s
*interval boundaries* , shall satisfy the relation $b_i < b_{i + 1}$ for
$i = 0, \dotsc, n - 1$. Unless specified otherwise, the remaining n
distribution parameters are calculated as:
$$\rho_k = \frac{w_k}{S \cdot (b_{k+1}-b_k)} \text{ for } k = 0, \dotsc, n - 1 \text{ ,}$$
in which the values wₖ, commonly known as the *weights* , shall be
non-negative, non-NaN, and non-infinity. Moreover, the following
relation shall hold: $0 < S = w_0 + \dotsb + w_{n-1}$.

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

> *Effects:*
>
> Constructs a `piecewise_constant_distribution` object with n = 1,
> $\rho_0 = 1$, b₀ = 0, and b₁ = 1.

``` cpp
template<class InputIteratorB, class InputIteratorW>
 piecewise_constant_distribution(InputIteratorB firstB, InputIteratorB lastB,
                                 InputIteratorW firstW);
```

> *Mandates:*
>
> Both of
>
> - `is_convertible_v<iterator_traits<InputIteratorB>::value_type, double>`
>
> - `is_convertible_v<iterator_traits<InputIteratorW>::value_type, double>`
>
> are `true`.
>
> *Preconditions:*
>
> `InputIteratorB` and `InputIteratorW` each meet the
> *Cpp17InputIterator* requirements\[input.iterators\]. If
> `firstB == lastB` or `++firstB == lastB`, let n = 1, w₀ = 1, b₀ = 0,
> and b₁ = 1. Otherwise, $\bigl[\texttt{firstB}, \texttt{lastB}\bigr)$
> forms a sequence b of length n+1, the length of the sequence w
> starting from `firstW` is at least n, and any wₖ for k ≥ n are ignored
> by the distribution.
>
> *Effects:*
>
> Constructs a `piecewise_constant_distribution` object with parameters
> as specified above.

``` cpp
template<class UnaryOperation>
 piecewise_constant_distribution(initializer_list<RealType> bl, UnaryOperation fw);
```

> *Mandates:*
>
> `is_invocable_r_v<double, UnaryOperation&, double>` is `true`.
>
> *Effects:*
>
> Constructs a `piecewise_constant_distribution` object with parameters
> taken or calculated from the following values: If
> $\texttt{bl.size()} < 2$, let n = 1, w₀ = 1, b₀ = 0, and b₁ = 1.
> Otherwise, let $\bigl[\texttt{bl.begin()}, \texttt{bl.end()}\bigr)$
> form a sequence $b_0, \dotsc, b_n$, and let
> $w_k = \texttt{fw}\bigl(\bigl(b_{k+1} + b_k\bigr) / 2\bigr)$ for
> $k = 0, \dotsc, n - 1$.
>
> *Complexity:*
>
> The number of invocations of `fw` does not exceed n.

``` cpp
template<class UnaryOperation>
 piecewise_constant_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
```

> *Mandates:*
>
> `is_invocable_r_v<double, UnaryOperation&, double>` is `true`.
>
> *Preconditions:*
>
> If $\texttt{nw} = 0$, let n = 1, otherwise let $n = \texttt{nw}$. The
> relation $0 < \delta = (\texttt{xmax} - \texttt{xmin}) / n$ holds.
>
> *Effects:*
>
> Constructs a `piecewise_constant_distribution` object with parameters
> taken or calculated from the following values: Let
> $b_k = \texttt{xmin} + k \cdot \delta$ for $k = 0, \dotsc, n$, and
> $w_k = \texttt{fw}(b_k + \delta / 2)$ for $k = 0, \dotsc, n - 1$.
>
> *Complexity:*
>
> The number of invocations of `fw` does not exceed n.

``` cpp
vector<result_type> intervals() const;
```

> *Returns:*
>
> A `vector<result_type>` whose `size` member returns n + 1 and whose
> $\texttt{operator[]}$ member returns bₖ when invoked with argument k
> for $k = 0, \dotsc, n$.

``` cpp
vector<result_type> densities() const;
```

> *Returns:*
>
> A `vector<result_type>` whose `size` member returns n and whose
> $\texttt{operator[]}$ member returns $\rho_k$ when invoked with
> argument k for $k = 0, \dotsc, n - 1$.

##### Class template `piecewise_linear_distribution` <a id="rand.dist.samp.plinear">[rand.dist.samp.plinear]</a>

A `piecewise_linear_distribution` random number distribution produces
random numbers x, b₀ ≤ x < bₙ, distributed over each subinterval
$[b_i, b_{i+1})$ according to the probability density function
$$p(x \,|\, b_0, \dotsc, b_n, \; \rho_0, \dotsc, \rho_n)
     = \rho_{i}   \cdot {\frac{b_{i+1} - x}{b_{i+1} - b_i}}
     + \rho_{i+1} \cdot {\frac{x - b_i}{b_{i+1} - b_i}}
     \text{ , for $b_i \le x < b_{i+1}$.}$$

The n + 1 distribution parameters bᵢ, also known as this distribution’s
*interval boundaries* , shall satisfy the relation $b_i < b_{i+1}$ for
$i = 0, \dotsc, n - 1$. Unless specified otherwise, the remaining n + 1
distribution parameters are calculated as $\rho_k = {w_k / S}$ for
$k = 0, \dotsc, n$, in which the values wₖ, commonly known as the
*weights at boundaries* , shall be non-negative, non-NaN, and
non-infinity. Moreover, the following relation shall hold:
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

> *Effects:*
>
> Constructs a `piecewise_linear_distribution` object with n = 1,
> $\rho_0 = \rho_1 = 1$, b₀ = 0, and b₁ = 1.

``` cpp
template<class InputIteratorB, class InputIteratorW>
 piecewise_linear_distribution(InputIteratorB firstB, InputIteratorB lastB,
                               InputIteratorW firstW);
```

> *Mandates:*
>
> `is_invocable_r_v<double, UnaryOperation&, double>` is `true`.
>
> *Preconditions:*
>
> `InputIteratorB` and `InputIteratorW` each meet the
> *Cpp17InputIterator* requirements\[input.iterators\]. If
> `firstB == lastB` or `++firstB == lastB`, let n = 1,
> $\rho_0 = \rho_1 = 1$, b₀ = 0, and b₁ = 1. Otherwise,
> $\bigl[\texttt{firstB}, \texttt{lastB}\bigr)$ forms a sequence b of
> length n+1, the length of the sequence w starting from `firstW` is at
> least n+1, and any wₖ for k ≥ n + 1 are ignored by the distribution.
>
> *Effects:*
>
> Constructs a `piecewise_linear_distribution` object with parameters as
> specified above.

``` cpp
template<class UnaryOperation>
 piecewise_linear_distribution(initializer_list<RealType> bl, UnaryOperation fw);
```

> *Mandates:*
>
> `is_invocable_r_v<double, UnaryOperation&, double>` is `true`.
>
> *Effects:*
>
> Constructs a `piecewise_linear_distribution` object with parameters
> taken or calculated from the following values: If
> $\texttt{bl.size()} < 2$, let n = 1, $\rho_0 = \rho_1 = 1$, b₀ = 0,
> and b₁ = 1. Otherwise, let
> $\bigl[\texttt{bl.begin(),} \texttt{bl.end()}\bigr)$ form a sequence
> $b_0, \dotsc, b_n$, and let $w_k = \texttt{fw}(b_k)$ for
> $k = 0, \dotsc, n$.
>
> *Complexity:*
>
> The number of invocations of `fw` does not exceed n+1.

``` cpp
template<class UnaryOperation>
 piecewise_linear_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
```

> *Mandates:*
>
> `is_invocable_r_v<double, UnaryOperation&, double>` is `true`.
>
> *Preconditions:*
>
> If $\texttt{nw} = 0$, let n = 1, otherwise let $n = \texttt{nw}$. The
> relation $0 < \delta = (\texttt{xmax} - \texttt{xmin}) / n$ holds.
>
> *Effects:*
>
> Constructs a `piecewise_linear_distribution` object with parameters
> taken or calculated from the following values: Let
> $b_k = \texttt{xmin} + k \cdot \delta$ for $k = 0, \dotsc, n$, and
> $w_k = \texttt{fw}(b_k)$ for $k = 0, \dotsc, n$.
>
> *Complexity:*
>
> The number of invocations of `fw` does not exceed n+1.

``` cpp
vector<result_type> intervals() const;
```

> *Returns:*
>
> A `vector<result_type>` whose `size` member returns n + 1 and whose
> $\texttt{operator[]}$ member returns bₖ when invoked with argument k
> for $k = 0, \dotsc, n$.

``` cpp
vector<result_type> densities() const;
```

> *Returns:*
>
> A `vector<result_type>` whose `size` member returns n and whose
> $\texttt{operator[]}$ member returns $\rho_k$ when invoked with
> argument k for $k = 0, \dotsc, n$.

### Low-quality random number generation <a id="c.math.rand">[c.math.rand]</a>

\[*Note 9*: The header `<cstdlib>` declares the functions described in
this subclause. — *end note*\]

``` cpp
int rand();
void srand(unsigned int seed);
```

> *Effects:*
>
> The `rand` and `srand` functions have the semantics specified in the C
> standard library.
>
> *Remarks:*
>
> The implementation may specify that particular library functions may
> call `rand`. It is *implementation-defined* whether the `rand`
> function may introduce data races\[res.on.data.races\].

## Numeric arrays <a id="numarray">[numarray]</a>

### Header `<valarray>` synopsis <a id="valarray.syn">[valarray.syn]</a>

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
nested argument type.

Implementations introducing such replacement types shall provide
additional functions and operators as follows:

- for every function taking a `const valarray<T>&` other than `begin`
  and `end` [valarray.range], identical functions taking the replacement
  types shall be added;

- for every function taking two `const valarray<T>&` arguments,
  identical functions taking every combination of `const valarray<T>&`
  and replacement types shall be added.

In particular, an implementation shall allow a `valarray<T>` to be
constructed from such replacement types and shall allow assignments and
compound assignments of such types to `valarray<T>`, `slice_array<T>`,
`gslice_array<T>`, `mask_array<T>` and `indirect_array<T>` objects.

These library functions are permitted to throw a `bad_alloc` [bad.alloc]
exception if there are not sufficient resources available to carry out
the operation. Note that the exception is not mandated.

### Class template `valarray` <a id="template.valarray">[template.valarray]</a>

#### Overview <a id="template.valarray.overview">[template.valarray.overview]</a>

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
remainder of  [numarray]. The illusion of higher dimensionality may be
produced by the familiar idiom of computed indices, together with the
powerful subsetting capabilities provided by the generalized subscript
operators.

#### Constructors <a id="valarray.cons">[valarray.cons]</a>

``` cpp
valarray();
```

> *Effects:*
>
> Constructs a `valarray` that has zero length.
>
> This default constructor is essential, since arrays of `valarray` can
> be useful. After initialization, the length of an empty array can be
> increased with the `resize` member function.

``` cpp
explicit valarray(size_t n);
```

> *Effects:*
>
> Constructs a `valarray` that has length `n`. Each element of the array
> is value-initialized\[dcl.init\].

``` cpp
valarray(const T& v, size_t n);
```

> *Effects:*
>
> Constructs a `valarray` that has length `n`. Each element of the array
> is initialized with `v`.

``` cpp
valarray(const T* p, size_t n);
```

> *Preconditions:*
>
> \[`p`, `p + n`) is a valid range.
>
> *Effects:*
>
> Constructs a `valarray` that has length `n`. The values of the
> elements of the array are initialized with the first `n` values
> pointed to by the first argument.
>
> This constructor is the preferred method for converting a C array to a
> `valarray` object.

``` cpp
valarray(const valarray& v);
```

> *Effects:*
>
> Constructs a `valarray` that has the same length as `v`. The elements
> are initialized with the values of the corresponding elements of `v`.
>
> This copy constructor creates a distinct array rather than an alias.
> Implementations in which arrays share storage are permitted, but they
> would need to implement a copy-on-reference mechanism to ensure that
> arrays are conceptually distinct.

``` cpp
valarray(valarray&& v) noexcept;
```

> *Effects:*
>
> Constructs a `valarray` that has the same length as `v`. The elements
> are initialized with the values of the corresponding elements of `v`.
>
> *Complexity:*
>
> Constant.

``` cpp
valarray(initializer_list<T> il);
```

> *Effects:*
>
> Equivalent to `valarray(il.begin(), il.size())`.

``` cpp
valarray(const slice_array<T>&);
valarray(const gslice_array<T>&);
valarray(const mask_array<T>&);
valarray(const indirect_array<T>&);
```

> These conversion constructors convert one of the four reference
> templates to a `valarray`.

``` cpp
~valarray();
```

> *Effects:*
>
> The destructor is applied to every element of `*this`; an
> implementation may return all allocated memory.

#### Assignment <a id="valarray.assign">[valarray.assign]</a>

``` cpp
valarray& operator=(const valarray& v);
```

> *Effects:*
>
> Each element of the `*this` array is assigned the value of the
> corresponding element of `v`. If the length of `v` is not equal to the
> length of `*this`, resizes `*this` to make the two arrays the same
> length, as if by calling `resize(v.size())`, before performing the
> assignment.
>
> *Ensures:*
>
> `size() == v.size()`.
>
> *Returns:*
>
> `*this`.

``` cpp
valarray& operator=(valarray&& v) noexcept;
```

> *Effects:*
>
> `*this` obtains the value of `v`. The value of `v` after the
> assignment is not specified.
>
> *Returns:*
>
> `*this`.
>
> *Complexity:*
>
> Linear.

``` cpp
valarray& operator=(initializer_list<T> il);
```

> *Effects:*
>
> Equivalent to: `return *this = valarray(il);`

``` cpp
valarray& operator=(const T& v);
```

> *Effects:*
>
> Assigns `v` to each element of `*this`.
>
> *Returns:*
>
> `*this`.

``` cpp
valarray& operator=(const slice_array<T>&);
valarray& operator=(const gslice_array<T>&);
valarray& operator=(const mask_array<T>&);
valarray& operator=(const indirect_array<T>&);
```

> *Preconditions:*
>
> The length of the array to which the argument refers equals `size()`.
> The value of an element in the left-hand side of a `valarray`
> assignment operator does not depend on the value of another element in
> that left-hand side.
>
> These operators allow the results of a generalized subscripting
> operation to be assigned directly to a `valarray`.

#### Element access <a id="valarray.access">[valarray.access]</a>

``` cpp
const T&  operator[](size_t n) const;
T& operator[](size_t n);
```

> *Preconditions:*
>
> `n < size()` is `true`.
>
> *Returns:*
>
> A reference to the corresponding element of the array.
>
> \[*Note 8*: The expression `(a[i] = q, a[i]) == q` evaluates to `true`
> for any non-constant `valarray<T> a`, any `T q`, and for any
> `size_t i` such that the value of `i` is less than the length of
> `a`. — *end note*\]
>
> *Remarks:*
>
> The expression `addressof(a[i+j]) == addressof(a[i]) + j` evaluates to
> `true` for all `size_t i` and `size_t j` such that `i+j < a.size()`.
>
> The expression `addressof(a[i]) != addressof(b[j])` evaluates to
> `true` for any two arrays `a` and `b` and for any `size_t i` and
> `size_t j` such that `i < a.size()` and `j < b.size()`.
>
> \[*Note 9*: This property indicates an absence of aliasing and can be
> used to advantage by optimizing compilers. Compilers can take
> advantage of inlining, constant propagation, loop fusion, tracking of
> pointers obtained from `operator new`, and other techniques to
> generate efficient `valarray`s. — *end note*\]
>
> The reference returned by the subscript operator for an array shall be
> valid until the member function
> `resize(size_t, T)`\[valarray.members\] is called for that array or
> until the lifetime of that array ends, whichever happens first.

#### Subset operations <a id="valarray.sub">[valarray.sub]</a>

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

> *Returns:*
>
> A `valarray` containing those elements of the controlled sequence
> designated by `slicearr`.
>
> \[*Example 1*:
>
>     const valarray<char> v0("abcdefghijklmnop", 16);
>     // \texttt{v0[slice(2, 5, 3)]} returns \texttt{valarray<char>("cfilo", 5)}
>
> — *end example*\]

``` cpp
slice_array<T> operator[](slice slicearr);
```

> *Returns:*
>
> An object that holds references to elements of the controlled sequence
> selected by `slicearr`.
>
> \[*Example 2*:
>
>     valarray<char> v0("abcdefghijklmnop", 16);
>     valarray<char> v1("ABCDE", 5);
>     v0[slice(2, 5, 3)] = v1;
>     // \texttt{v0 == valarray<char>("abAdeBghCjkDmnEp", 16);}
>
> — *end example*\]

``` cpp
valarray operator[](const gslice& gslicearr) const;
```

> *Returns:*
>
> A `valarray` containing those elements of the controlled sequence
> designated by `gslicearr`.
>
> \[*Example 3*:
>
>     const valarray<char> v0("abcdefghijklmnop", 16);
>     const size_t lv[] = { 2, 3 };
>     const size_t dv[] = { 7, 2 };
>     const valarray<size_t> len(lv, 2), str(dv, 2);
>     // \texttt{v0[gslice(3, len, str)]} returns
>     // \texttt{valarray<char>("dfhkmo", 6)}
>
> — *end example*\]

``` cpp
gslice_array<T> operator[](const gslice& gslicearr);
```

> *Returns:*
>
> An object that holds references to elements of the controlled sequence
> selected by `gslicearr`.
>
> \[*Example 4*:
>
>     valarray<char> v0("abcdefghijklmnop", 16);
>     valarray<char> v1("ABCDEF", 6);
>     const size_t lv[] = { 2, 3 };
>     const size_t dv[] = { 7, 2 };
>     const valarray<size_t> len(lv, 2), str(dv, 2);
>     v0[gslice(3, len, str)] = v1;
>     // \texttt{v0 == valarray<char>("abcAeBgCijDlEnFp", 16)}
>
> — *end example*\]

``` cpp
valarray operator[](const valarray<bool>& boolarr) const;
```

> *Returns:*
>
> A `valarray` containing those elements of the controlled sequence
> designated by `boolarr`.
>
> \[*Example 5*:
>
>     const valarray<char> v0("abcdefghijklmnop", 16);
>     const bool vb[] = { false, false, true, true, false, true };
>     // \texttt{v0[valarray<bool>(vb, 6)]} returns
>     // \texttt{valarray<char>("cdf", 3)}
>
> — *end example*\]

``` cpp
mask_array<T> operator[](const valarray<bool>& boolarr);
```

> *Returns:*
>
> An object that holds references to elements of the controlled sequence
> selected by `boolarr`.
>
> \[*Example 6*:
>
>     valarray<char> v0("abcdefghijklmnop", 16);
>     valarray<char> v1("ABC", 3);
>     const bool vb[] = { false, false, true, true, false, true };
>     v0[valarray<bool>(vb, 6)] = v1;
>     // \texttt{v0 == valarray<char>("abABeCghijklmnop", 16)}
>
> — *end example*\]

``` cpp
valarray operator[](const valarray<size_t>& indarr) const;
```

> *Returns:*
>
> A `valarray` containing those elements of the controlled sequence
> designated by `indarr`.
>
> \[*Example 7*:
>
>     const valarray<char> v0("abcdefghijklmnop", 16);
>     const size_t vi[] = { 7, 5, 2, 3, 8 };
>     // \texttt{v0[valarray<size_t>(vi, 5)]} returns
>     // \texttt{valarray<char>("hfcdi", 5)}
>
> — *end example*\]

``` cpp
indirect_array<T> operator[](const valarray<size_t>& indarr);
```

> *Returns:*
>
> An object that holds references to elements of the controlled sequence
> selected by `indarr`.
>
> \[*Example 8*:
>
>     valarray<char> v0("abcdefghijklmnop", 16);
>     valarray<char> v1("ABCDE", 5);
>     const size_t vi[] = { 7, 5, 2, 3, 8 };
>     v0[valarray<size_t>(vi, 5)] = v1;
>     // \texttt{v0 == valarray<char>("abCDeBgAEjklmnop", 16)}
>
> — *end example*\]

#### Unary operators <a id="valarray.unary">[valarray.unary]</a>

``` cpp
valarray operator+() const;
valarray operator-() const;
valarray operator~() const;
valarray<bool> operator!() const;
```

> *Mandates:*
>
> The indicated operator can be applied to operands of type `T` and
> returns a value of type `T` (`bool` for `operator!`) or which may be
> unambiguously implicitly converted to type `T` (`bool` for
> `operator!`).
>
> *Returns:*
>
> A `valarray` whose length is `size()`. Each element of the returned
> array is initialized with the result of applying the indicated
> operator to the corresponding element of the array.

#### Compound assignment <a id="valarray.cassign">[valarray.cassign]</a>

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

> *Mandates:*
>
> The indicated operator can be applied to two operands of type `T`.
>
> *Preconditions:*
>
> `size() == v.size()` is `true`.
>
> The value of an element in the left-hand side of a valarray compound
> assignment operator does not depend on the value of another element in
> that left hand side.
>
> *Effects:*
>
> Each of these operators performs the indicated operation on each of
> the elements of `*this` and the corresponding element of `v`.
>
> *Returns:*
>
> `*this`.
>
> *Remarks:*
>
> The appearance of an array on the left-hand side of a compound
> assignment does not invalidate references or pointers.

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

> *Mandates:*
>
> The indicated operator can be applied to two operands of type `T`.
>
> *Effects:*
>
> Each of these operators applies the indicated operation to each
> element of `*this` and `v`.
>
> *Returns:*
>
> `*this`
>
> *Remarks:*
>
> The appearance of an array on the left-hand side of a compound
> assignment does not invalidate references or pointers to the elements
> of the array.

#### Member functions <a id="valarray.members">[valarray.members]</a>

``` cpp
void swap(valarray& v) noexcept;
```

> *Effects:*
>
> `*this` obtains the value of `v`. `v` obtains the value of `*this`.
>
> *Complexity:*
>
> Constant.

``` cpp
size_t size() const;
```

> *Returns:*
>
> The number of elements in the array.
>
> *Complexity:*
>
> Constant time.

``` cpp
T sum() const;
```

> *Mandates:*
>
> `operator+=` can be applied to operands of type `T`.
>
> *Preconditions:*
>
> `size() > 0` is `true`.
>
> *Returns:*
>
> The sum of all the elements of the array. If the array has length 1,
> returns the value of element 0. Otherwise, the returned value is
> calculated by applying `operator+=` to a copy of an element of the
> array and all other elements of the array in an unspecified order.

``` cpp
T min() const;
```

> *Preconditions:*
>
> `size() > 0` is `true`.
>
> *Returns:*
>
> The minimum value contained in `*this`. For an array of length 1, the
> value of element 0 is returned. For all other array lengths, the
> determination is made using `operator<`.

``` cpp
T max() const;
```

> *Preconditions:*
>
> `size() > 0` is `true`.
>
> *Returns:*
>
> The maximum value contained in `*this`. For an array of length 1, the
> value of element 0 is returned. For all other array lengths, the
> determination is made using `operator<`.

``` cpp
valarray shift(int n) const;
```

> *Returns:*
>
> A `valarray` of length `size()`, each of whose elements *I* is
> `(*this)[`*`I`*` + n]` if *`I`*` + n` is non-negative and less than
> `size()`, otherwise `T()`.
>
> \[*Note 10*: If element zero is taken as the leftmost element, a
> positive value of `n` shifts the elements left `n` places, with zero
> fill. — *end note*\]
>
> \[*Example 9*: If the argument has the value -2, the first two
> elements of the result will be value-initialized\[dcl.init\]; the
> third element of the result will be assigned the value of the first
> element of `*this`; etc. — *end example*\]

``` cpp
valarray cshift(int n) const;
```

> *Returns:*
>
> A `valarray` of length `size()` that is a circular shift of `*this`.
> If element zero is taken as the leftmost element, a non-negative value
> of n shifts the elements circularly left n places and a negative value
> of n shifts the elements circularly right -n places.

``` cpp
valarray apply(T func(T)) const;
valarray apply(T func(const T&)) const;
```

> *Returns:*
>
> A `valarray` whose length is `size()`. Each element of the returned
> array is assigned the value returned by applying the argument function
> to the corresponding element of `*this`.

``` cpp
void resize(size_t sz, T c = T());
```

> *Effects:*
>
> Changes the length of the `*this` array to `sz` and then assigns to
> each element the value of the second argument. Resizing invalidates
> all pointers and references to elements in the array.

### `valarray` non-member operations <a id="valarray.nonmembers">[valarray.nonmembers]</a>

#### Binary operators <a id="valarray.binary">[valarray.binary]</a>

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

> *Mandates:*
>
> The indicated operator can be applied to operands of type `T` and
> returns a value of type `T` or which can be unambiguously implicitly
> converted to `T`.
>
> *Preconditions:*
>
> The argument arrays have the same length.
>
> *Returns:*
>
> A `valarray` whose length is equal to the lengths of the argument
> arrays. Each element of the returned array is initialized with the
> result of applying the indicated operator to the corresponding
> elements of the argument arrays.

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

> *Mandates:*
>
> The indicated operator can be applied to operands of type `T` and
> returns a value of type `T` or which can be unambiguously implicitly
> converted to `T`.
>
> *Returns:*
>
> A `valarray` whose length is equal to the length of the array
> argument. Each element of the returned array is initialized with the
> result of applying the indicated operator to the corresponding element
> of the array argument and the non-array argument.

#### Logical operators <a id="valarray.comparison">[valarray.comparison]</a>

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

> *Mandates:*
>
> The indicated operator can be applied to operands of type `T` and
> returns a value of type `bool` or which can be unambiguously
> implicitly converted to `bool`.
>
> *Preconditions:*
>
> The two array arguments have the same length.
>
> *Returns:*
>
> A `valarray<bool>` whose length is equal to the length of the array
> arguments. Each element of the returned array is initialized with the
> result of applying the indicated operator to the corresponding
> elements of the argument arrays.

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

> *Mandates:*
>
> The indicated operator can be applied to operands of type `T` and
> returns a value of type `bool` or which can be unambiguously
> implicitly converted to `bool`.
>
> *Returns:*
>
> A `valarray<bool>` whose length is equal to the length of the array
> argument. Each element of the returned array is initialized with the
> result of applying the indicated operator to the corresponding element
> of the array and the non-array argument.

#### Transcendentals <a id="valarray.transcend">[valarray.transcend]</a>

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

> *Mandates:*
>
> A unique function with the indicated name can be applied (unqualified)
> to an operand of type `T`. This function returns a value of type `T`
> or which can be unambiguously implicitly converted to type `T`.

#### Specialized algorithms <a id="valarray.special">[valarray.special]</a>

``` cpp
template<class T> void swap(valarray<T>& x, valarray<T>& y) noexcept;
```

> *Effects:*
>
> Equivalent to `x.swap(y)`.

### Class `slice` <a id="class.slice">[class.slice]</a>

#### Overview <a id="class.slice.overview">[class.slice.overview]</a>

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
slice is specified by a starting index, a length, and a stride.

#### Constructors <a id="cons.slice">[cons.slice]</a>

``` cpp
slice();
slice(size_t start, size_t length, size_t stride);
```

> The default constructor is equivalent to `slice(0, 0, 0)`. A default
> constructor is provided only to permit the declaration of arrays of
> slices. The constructor with arguments for a slice takes a start,
> length, and stride parameter.
>
> \[*Example 10*: `slice(3, 8, 2)` constructs a slice which selects
> elements $3, 5, 7, \dotsc, 17$ from an array. — *end example*\]

#### Access functions <a id="slice.access">[slice.access]</a>

``` cpp
size_t start() const;
size_t size() const;
size_t stride() const;
```

> *Returns:*
>
> The start, length, or stride specified by a `slice` object.
>
> *Complexity:*
>
> Constant time.

#### Operators <a id="slice.ops">[slice.ops]</a>

``` cpp
friend bool operator==(const slice& x, const slice& y);
```

> *Effects:*
>
> Equivalent to:
>
> ``` cpp
> return x.start() == y.start() && x.size() == y.size() && x.stride() == y.stride();
> ```

### Class template `slice_array` <a id="template.slice.array">[template.slice.array]</a>

#### Overview <a id="template.slice.array.overview">[template.slice.array.overview]</a>

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

\[*Example 1*: The expression `a[slice(1, 5, 3)] = b;` has the effect of
assigning the elements of `b` to a slice of the elements in `a`. For the
slice shown, the elements selected from `a` are
$1, 4, \dotsc, 13$. — *end example*\]

#### Assignment <a id="slice.arr.assign">[slice.arr.assign]</a>

``` cpp
void operator=(const valarray<T>&) const;
const slice_array& operator=(const slice_array&) const;
```

> These assignment operators have reference semantics, assigning the
> values of the argument array elements to selected elements of the
> `valarray<T>` object to which the `slice_array` object refers.

#### Compound assignment <a id="slice.arr.comp.assign">[slice.arr.comp.assign]</a>

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

> These compound assignments have reference semantics, applying the
> indicated operation to the elements of the argument array and selected
> elements of the `valarray<T>` object to which the `slice_array` object
> refers.

#### Fill function <a id="slice.arr.fill">[slice.arr.fill]</a>

``` cpp
void operator=(const T&) const;
```

> This function has reference semantics, assigning the value of its
> argument to the elements of the `valarray<T>` object to which the
> `slice_array` object refers.

### The `gslice` class <a id="class.gslice">[class.gslice]</a>

#### Overview <a id="class.gslice.overview">[class.gslice.overview]</a>

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
defined by a starting offset (s), a set of lengths ($l_j$), and a set of
strides ($d_j$). The number of lengths shall equal the number of
strides.

A `gslice` represents a mapping from a set of indices ($i_j$), equal in
number to the number of strides, to a single index k. It is useful for
building multidimensional array classes using the `valarray` template,
which is one-dimensional. The set of one-dimensional index values
specified by a `gslice` are $$k = s + \sum_j i_j d_j$$ where the
multidimensional indices $i_j$ range in value from 0 to $l_{ij} - 1$.

\[*Example 2*:

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

— *end example*\]

It is possible to have degenerate generalized slices in which an address
is repeated.

\[*Example 3*:

If the stride parameters in the previous example are changed to {1, 1,
1}, the first few elements of the resulting sequence of indices will be

— *end example*\]

If a degenerate slice is used as the argument to the non-`const` version
of `operator[](const gslice&)`, the behavior is undefined.

#### Constructors <a id="gslice.cons">[gslice.cons]</a>

``` cpp
gslice();
gslice(size_t start, const valarray<size_t>& lengths,
       const valarray<size_t>& strides);
```

> The default constructor is equivalent to
> `gslice(0, valarray<size_t>(), valarray<size_t>())`. The constructor
> with arguments builds a `gslice` based on a specification of start,
> lengths, and strides, as explained in the previous subclause.

#### Access functions <a id="gslice.access">[gslice.access]</a>

``` cpp
size_t           start()  const;
valarray<size_t> size() const;
valarray<size_t> stride() const;
```

> *Returns:*
>
> The representation of the start, lengths, or strides specified for the
> `gslice`.
>
> *Complexity:*
>
> `start()` is constant time. `size()` and `stride()` are linear in the
> number of strides.

### Class template `gslice_array` <a id="template.gslice.array">[template.gslice.array]</a>

#### Overview <a id="template.gslice.array.overview">[template.gslice.array.overview]</a>

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

#### Assignment <a id="gslice.array.assign">[gslice.array.assign]</a>

``` cpp
void operator=(const valarray<T>&) const;
const gslice_array& operator=(const gslice_array&) const;
```

> These assignment operators have reference semantics, assigning the
> values of the argument array elements to selected elements of the
> `valarray<T>` object to which the `gslice_array` refers.

#### Compound assignment <a id="gslice.array.comp.assign">[gslice.array.comp.assign]</a>

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

> These compound assignments have reference semantics, applying the
> indicated operation to the elements of the argument array and selected
> elements of the `valarray<T>` object to which the `gslice_array`
> object refers.

#### Fill function <a id="gslice.array.fill">[gslice.array.fill]</a>

``` cpp
void operator=(const T&) const;
```

> This function has reference semantics, assigning the value of its
> argument to the elements of the `valarray<T>` object to which the
> `gslice_array` object refers.

### Class template `mask_array` <a id="template.mask.array">[template.mask.array]</a>

#### Overview <a id="template.mask.array.overview">[template.mask.array.overview]</a>

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

#### Assignment <a id="mask.array.assign">[mask.array.assign]</a>

``` cpp
void operator=(const valarray<T>&) const;
const mask_array& operator=(const mask_array&) const;
```

> These assignment operators have reference semantics, assigning the
> values of the argument array elements to selected elements of the
> `valarray<T>` object to which the `mask_array` object refers.

#### Compound assignment <a id="mask.array.comp.assign">[mask.array.comp.assign]</a>

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

> These compound assignments have reference semantics, applying the
> indicated operation to the elements of the argument array and selected
> elements of the `valarray<T>` object to which the `mask_array` object
> refers.

#### Fill function <a id="mask.array.fill">[mask.array.fill]</a>

``` cpp
void operator=(const T&) const;
```

> This function has reference semantics, assigning the value of its
> argument to the elements of the `valarray<T>` object to which the
> `mask_array` object refers.

### Class template `indirect_array` <a id="template.indirect.array">[template.indirect.array]</a>

#### Overview <a id="template.indirect.array.overview">[template.indirect.array.overview]</a>

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
`indirect_array`. Thus, the expression `a[indirect] = b;` has the effect
of assigning the elements of `b` to the elements in `a` whose indices
appear in `indirect`.

#### Assignment <a id="indirect.array.assign">[indirect.array.assign]</a>

``` cpp
void operator=(const valarray<T>&) const;
const indirect_array& operator=(const indirect_array&) const;
```

> These assignment operators have reference semantics, assigning the
> values of the argument array elements to selected elements of the
> `valarray<T>` object to which it refers.
>
> If the `indirect_array` specifies an element in the `valarray<T>`
> object to which it refers more than once, the behavior is undefined.
>
> \[*Example 11*:
>
>     int addr[] = {2, 3, 1, 4, 4};
>     valarray<size_t> indirect(addr, 5);
>     valarray<double> a(0., 10), b(1., 5);
>     a[indirect] = b;
>
> results in undefined behavior since element 4 is specified twice in
> the indirection.
>
> — *end example*\]

#### Compound assignment <a id="indirect.array.comp.assign">[indirect.array.comp.assign]</a>

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

> These compound assignments have reference semantics, applying the
> indicated operation to the elements of the argument array and selected
> elements of the `valarray<T>` object to which the `indirect_array`
> object refers.
>
> If the `indirect_array` specifies an element in the `valarray<T>`
> object to which it refers more than once, the behavior is undefined.

#### Fill function <a id="indirect.array.fill">[indirect.array.fill]</a>

``` cpp
void operator=(const T&) const;
```

> This function has reference semantics, assigning the value of its
> argument to the elements of the `valarray<T>` object to which the
> `indirect_array` object refers.

### `valarray` range access <a id="valarray.range">[valarray.range]</a>

In the `begin` and `end` function templates that follow, *unspecified*
is a type that meets the requirements of a mutable
*Cpp17RandomAccessIterator* [random.access.iterators] and models
`contiguous_iterator` [iterator.concept.contiguous], whose `value_type`
is the template parameter `T` and whose `reference` type is `T&`.
*unspecified* is a type that meets the requirements of a constant
*Cpp17RandomAccessIterator* and models `contiguous_iterator`, whose
`value_type` is the template parameter `T` and whose `reference` type is
`const T&`.

The iterators returned by `begin` and `end` for an array are guaranteed
to be valid until the member function `resize(size_t, T)`
[valarray.members] is called for that array or until the lifetime of
that array ends, whichever happens first.

``` cpp
template<class T> unspecified{1} begin(valarray<T>& v);
template<class T> unspecified{2} begin(const valarray<T>& v);
```

> *Returns:*
>
> An iterator referencing the first value in the array.

``` cpp
template<class T> unspecified{1} end(valarray<T>& v);
template<class T> unspecified{2} end(const valarray<T>& v);
```

> *Returns:*
>
> An iterator referencing one past the last value in the array.

## Mathematical functions for floating-point types <a id="c.math">[c.math]</a>

### Header `<cmath>` synopsis <a id="cmath.syn">[cmath.syn]</a>

``` cpp
namespace std {
  using float_t = see below;
  using double_t = see below;
}

#define HUGE_VAL see below
#define HUGE_VALF see below
#define HUGE_VALL see below
#define INFINITY see below
#define NAN see below
#define FP_INFINITE see below
#define FP_NAN see below
#define FP_NORMAL see below
#define FP_SUBNORMAL see below
#define FP_ZERO see below
#define FP_FAST_FMA see below
#define FP_FAST_FMAF see below
#define FP_FAST_FMAL see below
#define FP_ILOGB0 see below
#define FP_ILOGBNAN see below
#define MATH_ERRNO see below
#define MATH_ERREXCEPT see below

#define math_errhandling see below

namespace std {
  floating-point-type acos(floating-point-type x);
  float acosf(float x);
  long double acosl(long double x);

  floating-point-type asin(floating-point-type x);
  float asinf(float x);
  long double asinl(long double x);

  floating-point-type atan(floating-point-type x);
  float atanf(float x);
  long double atanl(long double x);

  floating-point-type atan2(floating-point-type y, floating-point-type x);
  float atan2f(float y, float x);
  long double atan2l(long double y, long double x);

  floating-point-type cos(floating-point-type x);
  float cosf(float x);
  long double cosl(long double x);

  floating-point-type sin(floating-point-type x);
  float sinf(float x);
  long double sinl(long double x);

  floating-point-type tan(floating-point-type x);
  float tanf(float x);
  long double tanl(long double x);

  floating-point-type acosh(floating-point-type x);
  float acoshf(float x);
  long double acoshl(long double x);

  floating-point-type asinh(floating-point-type x);
  float asinhf(float x);
  long double asinhl(long double x);

  floating-point-type atanh(floating-point-type x);
  float atanhf(float x);
  long double atanhl(long double x);

  floating-point-type cosh(floating-point-type x);
  float coshf(float x);
  long double coshl(long double x);

  floating-point-type sinh(floating-point-type x);
  float sinhf(float x);
  long double sinhl(long double x);

  floating-point-type tanh(floating-point-type x);
  float tanhf(float x);
  long double tanhl(long double x);

  floating-point-type exp(floating-point-type x);
  float expf(float x);
  long double expl(long double x);

  floating-point-type exp2(floating-point-type x);
  float exp2f(float x);
  long double exp2l(long double x);

  floating-point-type expm1(floating-point-type x);
  float expm1f(float x);
  long double expm1l(long double x);

  constexpr floating-point-type frexp(floating-point-type value, int* exp);
  constexpr float frexpf(float value, int* exp);
  constexpr long double frexpl(long double value, int* exp);

  constexpr int ilogb(floating-point-type x);
  constexpr int ilogbf(float x);
  constexpr int ilogbl(long double x);

  constexpr floating-point-type ldexp(floating-point-type x, int exp);
  constexpr float ldexpf(float x, int exp);
  constexpr long double ldexpl(long double x, int exp);

  floating-point-type log(floating-point-type x);
  float logf(float x);
  long double logl(long double x);

  floating-point-type log10(floating-point-type x);
  float log10f(float x);
  long double log10l(long double x);

  floating-point-type log1p(floating-point-type x);
  float log1pf(float x);
  long double log1pl(long double x);

  floating-point-type log2(floating-point-type x);
  float log2f(float x);
  long double log2l(long double x);

  constexpr floating-point-type logb(floating-point-type x);
  constexpr float logbf(float x);
  constexpr long double logbl(long double x);

  constexpr floating-point-type modf(floating-point-type value, floating-point-type* iptr);
  constexpr float modff(float value, float* iptr);
  constexpr long double modfl(long double value, long double* iptr);

  constexpr floating-point-type scalbn(floating-point-type x, int n);
  constexpr float scalbnf(float x, int n);
  constexpr long double scalbnl(long double x, int n);

  constexpr floating-point-type scalbln(floating-point-type x, long int n);
  constexpr float scalblnf(float x, long int n);
  constexpr long double scalblnl(long double x, long int n);

  floating-point-type cbrt(floating-point-type x);
  float cbrtf(float x);
  long double cbrtl(long double x);

  // [c.math.abs], absolute values
  constexpr int abs(int j);
  constexpr long int abs(long int j);
  constexpr long long int abs(long long int j);
  constexpr floating-point-type abs(floating-point-type j);

  constexpr floating-point-type fabs(floating-point-type x);
  constexpr float fabsf(float x);
  constexpr long double fabsl(long double x);

  floating-point-type hypot(floating-point-type x, floating-point-type y);
  float hypotf(float x, float y);
  long double hypotl(long double x, long double y);

  // [c.math.hypot3], three-dimensional hypotenuse
  floating-point-type hypot(floating-point-type x, floating-point-type y,
                            floating-point-type z);

  floating-point-type pow(floating-point-type x, floating-point-type y);
  float powf(float x, float y);
  long double powl(long double x, long double y);

  floating-point-type sqrt(floating-point-type x);
  float sqrtf(float x);
  long double sqrtl(long double x);

  floating-point-type erf(floating-point-type x);
  float erff(float x);
  long double erfl(long double x);

  floating-point-type erfc(floating-point-type x);
  float erfcf(float x);
  long double erfcl(long double x);

  floating-point-type lgamma(floating-point-type x);
  float lgammaf(float x);
  long double lgammal(long double x);

  floating-point-type tgamma(floating-point-type x);
  float tgammaf(float x);
  long double tgammal(long double x);

  constexpr floating-point-type ceil(floating-point-type x);
  constexpr float ceilf(float x);
  constexpr long double ceill(long double x);

  constexpr floating-point-type floor(floating-point-type x);
  constexpr float floorf(float x);
  constexpr long double floorl(long double x);

  floating-point-type nearbyint(floating-point-type x);
  float nearbyintf(float x);
  long double nearbyintl(long double x);

  floating-point-type rint(floating-point-type x);
  float rintf(float x);
  long double rintl(long double x);

  long int lrint(floating-point-type x);
  long int lrintf(float x);
  long int lrintl(long double x);

  long long int llrint(floating-point-type x);
  long long int llrintf(float x);
  long long int llrintl(long double x);

  constexpr floating-point-type round(floating-point-type x);
  constexpr float roundf(float x);
  constexpr long double roundl(long double x);

  constexpr long int lround(floating-point-type x);
  constexpr long int lroundf(float x);
  constexpr long int lroundl(long double x);

  constexpr long long int llround(floating-point-type x);
  constexpr long long int llroundf(float x);
  constexpr long long int llroundl(long double x);

  constexpr floating-point-type trunc(floating-point-type x);
  constexpr float truncf(float x);
  constexpr long double truncl(long double x);

  constexpr floating-point-type fmod(floating-point-type x, floating-point-type y);
  constexpr float fmodf(float x, float y);
  constexpr long double fmodl(long double x, long double y);

  constexpr floating-point-type remainder(floating-point-type x, floating-point-type y);
  constexpr float remainderf(float x, float y);
  constexpr long double remainderl(long double x, long double y);

  constexpr floating-point-type remquo(floating-point-type x, floating-point-type y, int* quo);
  constexpr float remquof(float x, float y, int* quo);
  constexpr long double remquol(long double x, long double y, int* quo);

  constexpr floating-point-type copysign(floating-point-type x, floating-point-type y);
  constexpr float copysignf(float x, float y);
  constexpr long double copysignl(long double x, long double y);

  double nan(const char* tagp);
  float nanf(const char* tagp);
  long double nanl(const char* tagp);

  constexpr floating-point-type nextafter(floating-point-type x, floating-point-type y);
  constexpr float nextafterf(float x, float y);
  constexpr long double nextafterl(long double x, long double y);

  constexpr floating-point-type nexttoward(floating-point-type x, long double y);
  constexpr float nexttowardf(float x, long double y);
  constexpr long double nexttowardl(long double x, long double y);

  constexpr floating-point-type fdim(floating-point-type x, floating-point-type y);
  constexpr float fdimf(float x, float y);
  constexpr long double fdiml(long double x, long double y);

  constexpr floating-point-type fmax(floating-point-type x, floating-point-type y);
  constexpr float fmaxf(float x, float y);
  constexpr long double fmaxl(long double x, long double y);

  constexpr floating-point-type fmin(floating-point-type x, floating-point-type y);
  constexpr float fminf(float x, float y);
  constexpr long double fminl(long double x, long double y);

  constexpr floating-point-type fma(floating-point-type x, floating-point-type y,
                                  floating-point-type z);
  constexpr float fmaf(float x, float y, float z);
  constexpr long double fmal(long double x, long double y, long double z);

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
  float        assoc_laguerref(unsigned n, unsigned m, float x);
  long double  assoc_laguerrel(unsigned n, unsigned m, long double x);

  // [sf.cmath.assoc.legendre], associated Legendre functions
  floating-point-type assoc_legendre(unsigned l, unsigned m, floating-point-type x);
  float        assoc_legendref(unsigned l, unsigned m, float x);
  long double  assoc_legendrel(unsigned l, unsigned m, long double x);

  // [sf.cmath.beta], beta function
  floating-point-type beta(floating-point-type x, floating-point-type y);
  float        betaf(float x, float y);
  long double  betal(long double x, long double y);

  // [sf.cmath.comp.ellint.1], complete elliptic integral of the first kind
  floating-point-type comp_ellint_1(floating-point-type k);
  float        comp_ellint_1f(float k);
  long double  comp_ellint_1l(long double k);

  // [sf.cmath.comp.ellint.2], complete elliptic integral of the second kind
  floating-point-type comp_ellint_2(floating-point-type k);
  float        comp_ellint_2f(float k);
  long double  comp_ellint_2l(long double k);

  // [sf.cmath.comp.ellint.3], complete elliptic integral of the third kind
  floating-point-type comp_ellint_3(floating-point-type k, floating-point-type nu);
  float        comp_ellint_3f(float k, float nu);
  long double  comp_ellint_3l(long double k, long double nu);

  // [sf.cmath.cyl.bessel.i], regular modified cylindrical Bessel functions
  floating-point-type cyl_bessel_i(floating-point-type nu, floating-point-type x);
  float        cyl_bessel_if(float nu, float x);
  long double  cyl_bessel_il(long double nu, long double x);

  // [sf.cmath.cyl.bessel.j], cylindrical Bessel functions of the first kind
  floating-point-type cyl_bessel_j(floating-point-type nu, floating-point-type x);
  float        cyl_bessel_jf(float nu, float x);
  long double  cyl_bessel_jl(long double nu, long double x);

  // [sf.cmath.cyl.bessel.k], irregular modified cylindrical Bessel functions
  floating-point-type cyl_bessel_k(floating-point-type nu, floating-point-type x);
  float        cyl_bessel_kf(float nu, float x);
  long double  cyl_bessel_kl(long double nu, long double x);

  // [sf.cmath.cyl.neumann], cylindrical Neumann functions
  // cylindrical Bessel functions of the second kind
  floating-point-type       cyl_neumann(floating-point-type nu, floating-point-type x);
  float        cyl_neumannf(float nu, float x);
  long double  cyl_neumannl(long double nu, long double x);

  // [sf.cmath.ellint.1], incomplete elliptic integral of the first kind
  floating-point-type ellint_1(floating-point-type k, floating-point-type phi);
  float        ellint_1f(float k, float phi);
  long double  ellint_1l(long double k, long double phi);

  // [sf.cmath.ellint.2], incomplete elliptic integral of the second kind
  floating-point-type ellint_2(floating-point-type k, floating-point-type phi);
  float        ellint_2f(float k, float phi);
  long double  ellint_2l(long double k, long double phi);

  // [sf.cmath.ellint.3], incomplete elliptic integral of the third kind
  floating-point-type ellint_3(floating-point-type k, floating-point-type nu,
                                 floating-point-type phi);
  float        ellint_3f(float k, float nu, float phi);
  long double  ellint_3l(long double k, long double nu, long double phi);

  // [sf.cmath.expint], exponential integral
  floating-point-type expint(floating-point-type x);
  float        expintf(float x);
  long double  expintl(long double x);

  // [sf.cmath.hermite], Hermite polynomials
  floating-point-type hermite(unsigned n, floating-point-type x);
  float        hermitef(unsigned n, float x);
  long double  hermitel(unsigned n, long double x);

  // [sf.cmath.laguerre], Laguerre polynomials
  floating-point-type laguerre(unsigned n, floating-point-type x);
  float        laguerref(unsigned n, float x);
  long double  laguerrel(unsigned n, long double x);

  // [sf.cmath.legendre], Legendre polynomials
  floating-point-type legendre(unsigned l, floating-point-type x);
  float        legendref(unsigned l, float x);
  long double  legendrel(unsigned l, long double x);

  // [sf.cmath.riemann.zeta], Riemann zeta function
  floating-point-type riemann_zeta(floating-point-type x);
  float        riemann_zetaf(float x);
  long double  riemann_zetal(long double x);

  // [sf.cmath.sph.bessel], spherical Bessel functions of the first kind
  floating-point-type sph_bessel(unsigned n, floating-point-type x);
  float        sph_besself(unsigned n, float x);
  long double  sph_bessell(unsigned n, long double x);

  // [sf.cmath.sph.legendre], spherical associated Legendre functions
  floating-point-type sph_legendre(unsigned l, unsigned m, floating-point-type theta);
  float        sph_legendref(unsigned l, unsigned m, float theta);
  long double  sph_legendrel(unsigned l, unsigned m, long double theta);

  // [sf.cmath.sph.neumann], spherical Neumann functions;
  // spherical Bessel functions of the second kind
  floating-point-type sph_neumann(unsigned n, floating-point-type x);
  float        sph_neumannf(unsigned n, float x);
  long double  sph_neumannl(unsigned n, long double x);
}
```

The contents and meaning of the header `<cmath>` are the same as the C
standard library header `<math.h>`, with the addition of a
three-dimensional hypotenuse function [c.math.hypot3], a linear
interpolation function [c.math.lerp], and the mathematical special
functions described in [sf.cmath].

\[*Note 1*: Several functions have additional overloads in this
document, but they have the same behavior as in the C standard library
[library.c]. — *end note*\]

For each function with at least one parameter of type
*floating-point-type*, the implementation provides an overload for each
cv-unqualified floating-point type [basic.fundamental] where all uses of
*floating-point-type* in the function signature are replaced with that
floating-point type.

For each function with at least one parameter of type
*floating-point-type* other than `abs`, the implementation also provides
additional overloads sufficient to ensure that, if every argument
corresponding to a *floating-point-type* parameter has arithmetic type,
then every such argument is effectively cast to the floating-point type
with the greatest floating-point conversion rank and greatest
floating-point conversion subrank among the types of all such arguments,
where arguments of integer type are considered to have the same
floating-point conversion rank as `double`. If no such floating-point
type with the greatest rank and subrank exists, then overload resolution
does not result in a usable candidate [over.match.general] from the
overloads provided by the implementation.

An invocation of `nexttoward` is ill-formed if the argument
corresponding to the *floating-point-type* parameter has extended
floating-point type.

### Absolute values <a id="c.math.abs">[c.math.abs]</a>

\[*Note 2*: The headers `<cstdlib>` and `<cmath>` declare the functions
described in this subclause. — *end note*\]

``` cpp
constexpr int abs(int j);
constexpr long int abs(long int j);
constexpr long long int abs(long long int j);
```

> *Effects:*
>
> These functions have the semantics specified in the C standard library
> for the functions `abs`, `labs`, and `llabs`, respectively.
>
> *Remarks:*
>
> If `abs` is called with an argument of type `X` for which
> `is_unsigned_v<X>` is `true` and if `X` cannot be converted to `int`
> by integral promotion\[conv.prom\], the program is ill-formed.
>
> \[*Note 11*: Arguments that can be promoted to `int` are permitted for
> compatibility with C. — *end note*\]

``` cpp
constexpr floating-point-type abs(floating-point-type x);
```

> *Returns:*
>
> The absolute value of `x`.

### Three-dimensional hypotenuse <a id="c.math.hypot3">[c.math.hypot3]</a>

``` cpp
floating-point-type hypot(floating-point-type x, floating-point-type y, floating-point-type z);
```

> *Returns:*
>
> $\sqrt{x^2+y^2+z^2}$.

### Linear interpolation <a id="c.math.lerp">[c.math.lerp]</a>

``` cpp
constexpr floating-point-type lerp(floating-point-type a, floating-point-type b,
                                   floating-point-type t) noexcept;
```

> *Returns:*
>
> a+t(b-a).
>
> *Remarks:*
>
> Let `r` be the value returned. If `isfinite(a) && isfinite(b)`, then:
>
> - If `t == 0`, then `r == a`.
>
> - If `t == 1`, then `r == b`.
>
> - If `t >= 0 && t <= 1`, then `isfinite(r)`.
>
> - If `isfinite(t) && a == b`, then `r == a`.
>
> - If `isfinite(t) || !isnan(t) && b-a != 0`, then `!isnan(r)`.
>
> Let *`CMP`*`(x,y)` be `1` if `x > y`, `-1` if `x < y`, and `0`
> otherwise. For any `t1` and `t2`, the product of
> *`CMP`*`(lerp(a, b, t2), lerp(a, b, t1))`, *`CMP`*`(t2, t1)`, and
> *`CMP`*`(b, a)` is non-negative.

### Classification / comparison functions <a id="c.math.fpclass">[c.math.fpclass]</a>

The classification / comparison functions behave the same as the C
macros with the corresponding names defined in the C standard library.

### Mathematical special functions <a id="sf.cmath">[sf.cmath]</a>

#### General <a id="sf.cmath.general">[sf.cmath.general]</a>

If any argument value to any of the functions specified in [sf.cmath] is
a NaN (Not a Number), the function shall return a NaN but it shall not
report a domain error. Otherwise, the function shall report a domain
error for just those argument values for which:

- the function description’s element explicitly specifies a domain and
  those argument values fall outside the specified domain, or

- the corresponding mathematical function value has a nonzero imaginary
  component, or

- the corresponding mathematical function is not mathematically defined.

Unless otherwise specified, each function is defined for all finite
values, for negative infinity, and for positive infinity.

#### Associated Laguerre polynomials <a id="sf.cmath.assoc.laguerre">[sf.cmath.assoc.laguerre]</a>

``` cpp
floating-point-type assoc_laguerre(unsigned n, unsigned m, floating-point-type x);
float        assoc_laguerref(unsigned n, unsigned m, float x);
long double  assoc_laguerrel(unsigned n, unsigned m, long double x);
```

> *Effects:*
>
> These functions compute the associated Laguerre polynomials of their
> respective arguments `n`, `m`, and `x`.
>
> *Returns:*
>
> $$\mathsf{L}_n^m(x) =
>    (-1)^m \frac{\mathsf{d} ^ m}{\mathsf{d}x ^ m} \, \mathsf{L}_{n+m}(x)
>    \text{ ,\quad for $x \ge 0$,}$$ where n is `n`, m is `m`, and x is
> `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `n >= 128` or if `m >= 128`.

#### Associated Legendre functions <a id="sf.cmath.assoc.legendre">[sf.cmath.assoc.legendre]</a>

``` cpp
floating-point-type assoc_legendre(unsigned l, unsigned m, floating-point-type x);
float        assoc_legendref(unsigned l, unsigned m, float x);
long double  assoc_legendrel(unsigned l, unsigned m, long double x);
```

> *Effects:*
>
> These functions compute the associated Legendre functions of their
> respective arguments `l`, `m`, and `x`.
>
> *Returns:*
>
> $$\mathsf{P}_\ell^m(x) = (1 - x^2) ^ {m/2} \:
>    \frac{\mathsf{d} ^ m}{\mathsf{d}x ^ m} \, \mathsf{P}_\ell(x)
>    \text{ ,\quad for $|x| \le 1$,}$$ where l is `l`, m is `m`, and x
> is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `l >= 128`.

#### Beta function <a id="sf.cmath.beta">[sf.cmath.beta]</a>

``` cpp
floating-point-type beta(floating-point-type x, floating-point-type y);
float        betaf(float x, float y);
long double  betal(long double x, long double y);
```

> *Effects:*
>
> These functions compute the beta function of their respective
> arguments `x` and `y`.
>
> *Returns:*
>
> $$\mathsf{B}(x, y) = \frac{\Gamma(x) \, \Gamma(y)}{\Gamma(x + y)}
>    \text{ ,\quad for $x > 0$,\, $y > 0$,}$$ where x is `x` and y is
> `y`.

#### Complete elliptic integral of the first kind <a id="sf.cmath.comp.ellint.1">[sf.cmath.comp.ellint.1]</a>

``` cpp
floating-point-type comp_ellint_1(floating-point-type k);
float        comp_ellint_1f(float k);
long double  comp_ellint_1l(long double k);
```

> *Effects:*
>
> These functions compute the complete elliptic integral of the first
> kind of their respective arguments `k`.
>
> *Returns:*
>
> $$\mathsf{K}(k) = \mathsf{F}(k, \pi / 2) \text{ ,\quad for $|k| \le 1$,}$$
> where k is `k`.
>
> See also \[sf.cmath.ellint.1\].

#### Complete elliptic integral of the second kind <a id="sf.cmath.comp.ellint.2">[sf.cmath.comp.ellint.2]</a>

``` cpp
floating-point-type comp_ellint_2(floating-point-type k);
float        comp_ellint_2f(float k);
long double  comp_ellint_2l(long double k);
```

> *Effects:*
>
> These functions compute the complete elliptic integral of the second
> kind of their respective arguments `k`.
>
> *Returns:*
>
> $$\mathsf{E}(k) = \mathsf{E}(k, \pi / 2) \text{ ,\quad for $|k| \le 1$,}$$
> where k is `k`.
>
> See also \[sf.cmath.ellint.2\].

#### Complete elliptic integral of the third kind <a id="sf.cmath.comp.ellint.3">[sf.cmath.comp.ellint.3]</a>

``` cpp
floating-point-type comp_ellint_3(floating-point-type k, floating-point-type nu);
float        comp_ellint_3f(float k, float nu);
long double  comp_ellint_3l(long double k, long double nu);
```

> *Effects:*
>
> These functions compute the complete elliptic integral of the third
> kind of their respective arguments `k` and `nu`.
>
> *Returns:*
>
> $$\mathsf{\Pi}(\nu, k) = \mathsf{\Pi}(\nu, k, \pi / 2) \text{ ,\quad for $|k| \le 1$,}$$
> where k is `k` and $\nu$ is `nu`.
>
> See also \[sf.cmath.ellint.3\].

#### Regular modified cylindrical Bessel functions <a id="sf.cmath.cyl.bessel.i">[sf.cmath.cyl.bessel.i]</a>

``` cpp
floating-point-type cyl_bessel_i(floating-point-type nu, floating-point-type x);
float        cyl_bessel_if(float nu, float x);
long double  cyl_bessel_il(long double nu, long double x);
```

> *Effects:*
>
> These functions compute the regular modified cylindrical Bessel
> functions of their respective arguments `nu` and `x`.
>
> *Returns:*
>
> $$\mathsf{I}_\nu(x) =
>      \mathrm{i}^{-\nu} \mathsf{J}_\nu(\mathrm{i}x) =
>      \sum_{k=0}^\infty \frac{(x/2)^{\nu+2k}}{k! \: \Gamma(\nu+k+1)}
>      \text{ ,\quad for $x \ge 0$,}$$ where $\nu$ is `nu` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `nu >= 128`.
>
> See also \[sf.cmath.cyl.bessel.j\].

#### Cylindrical Bessel functions of the first kind <a id="sf.cmath.cyl.bessel.j">[sf.cmath.cyl.bessel.j]</a>

``` cpp
floating-point-type cyl_bessel_j(floating-point-type nu, floating-point-type x);
float        cyl_bessel_jf(float nu, float x);
long double  cyl_bessel_jl(long double nu, long double x);
```

> *Effects:*
>
> These functions compute the cylindrical Bessel functions of the first
> kind of their respective arguments `nu` and `x`.
>
> *Returns:*
>
> $$\mathsf{J}_\nu(x) =
>    \sum_{k=0}^\infty \frac{(-1)^k (x/2)^{\nu+2k}}{k! \: \Gamma(\nu+k+1)}
>    \text{ ,\quad for $x \ge 0$,}$$ where $\nu$ is `nu` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `nu >= 128`.

#### Irregular modified cylindrical Bessel functions <a id="sf.cmath.cyl.bessel.k">[sf.cmath.cyl.bessel.k]</a>

``` cpp
floating-point-type cyl_bessel_k(floating-point-type nu, floating-point-type x);
float        cyl_bessel_kf(float nu, float x);
long double  cyl_bessel_kl(long double nu, long double x);
```

> *Effects:*
>
> These functions compute the irregular modified cylindrical Bessel
> functions of their respective arguments `nu` and `x`.
>
> *Returns:*
>
> $$%
>   \mathsf{K}_\nu(x) =
>   (\pi/2)\mathrm{i}^{\nu+1} (            \mathsf{J}_\nu(\mathrm{i}x)
>                 + \mathrm{i} \mathsf{N}_\nu(\mathrm{i}x)
>                 )
>   =
>   \left\{
>   \begin{array}{cl}
>   \displaystyle
>   \frac{\pi}{2}
>   \frac{\mathsf{I}_{-\nu}(x) - \mathsf{I}_{\nu}(x)}
>        {\sin \nu\pi },
>   & \mbox{for $x \ge 0$ and non-integral $\nu$}
>   \\
>   \\
>   \displaystyle
>   \frac{\pi}{2}
>   \lim_{\mu \rightarrow \nu} \frac{\mathsf{I}_{-\mu}(x) - \mathsf{I}_{\mu}(x)}
>                                   {\sin \mu\pi },
>   & \mbox{for $x \ge 0$ and integral $\nu$}
>   \end{array}
>   \right.$$ where $\nu$ is `nu` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `nu >= 128`.
>
> See also \[sf.cmath.cyl.bessel.i\], \[sf.cmath.cyl.bessel.j\],
> \[sf.cmath.cyl.neumann\].

#### Cylindrical Neumann functions <a id="sf.cmath.cyl.neumann">[sf.cmath.cyl.neumann]</a>

``` cpp
floating-point-type cyl_neumann(floating-point-type nu, floating-point-type x);
float        cyl_neumannf(float nu, float x);
long double  cyl_neumannl(long double nu, long double x);
```

> *Effects:*
>
> These functions compute the cylindrical Neumann functions, also known
> as the cylindrical Bessel functions of the second kind, of their
> respective arguments `nu` and `x`.
>
> *Returns:*
>
> $$%
>   \mathsf{N}_\nu(x) =
>   \left\{
>   \begin{array}{cl}
>   \displaystyle
>   \frac{\mathsf{J}_\nu(x) \cos \nu\pi - \mathsf{J}_{-\nu}(x)}
>        {\sin \nu\pi },
>   & \mbox{for $x \ge 0$ and non-integral $\nu$}
>   \\
>   \\
>   \displaystyle
>   \lim_{\mu \rightarrow \nu} \frac{\mathsf{J}_\mu(x) \cos \mu\pi - \mathsf{J}_{-\mu}(x)}
>                                 {\sin \mu\pi },
>   & \mbox{for $x \ge 0$ and integral $\nu$}
>   \end{array}
>   \right.$$ where $\nu$ is `nu` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `nu >= 128`.
>
> See also \[sf.cmath.cyl.bessel.j\].

#### Incomplete elliptic integral of the first kind <a id="sf.cmath.ellint.1">[sf.cmath.ellint.1]</a>

``` cpp
floating-point-type ellint_1(floating-point-type k, floating-point-type phi);
float        ellint_1f(float k, float phi);
long double  ellint_1l(long double k, long double phi);
```

> *Effects:*
>
> These functions compute the incomplete elliptic integral of the first
> kind of their respective arguments `k` and `phi` (`phi` measured in
> radians).
>
> *Returns:*
>
> $$\mathsf{F}(k, \phi) =
>      \int_0^\phi \! \frac{\mathsf{d}\theta}{\sqrt{1 - k^2 \sin^2 \theta}}
>      \text{ ,\quad for $|k| \le 1$,}$$ where k is `k` and $\phi$ is
> `phi`.

#### Incomplete elliptic integral of the second kind <a id="sf.cmath.ellint.2">[sf.cmath.ellint.2]</a>

``` cpp
floating-point-type ellint_2(floating-point-type k, floating-point-type phi);
float        ellint_2f(float k, float phi);
long double  ellint_2l(long double k, long double phi);
```

> *Effects:*
>
> These functions compute the incomplete elliptic integral of the second
> kind of their respective arguments `k` and `phi` (`phi` measured in
> radians).
>
> *Returns:*
>
> $$\mathsf{E}(k, \phi) = \int_0^\phi \! \sqrt{1 - k^2 \sin^2 \theta} \, \mathsf{d}\theta
>    \text{ ,\quad for $|k| \le 1$,}$$ where k is `k` and $\phi$ is
> `phi`.

#### Incomplete elliptic integral of the third kind <a id="sf.cmath.ellint.3">[sf.cmath.ellint.3]</a>

``` cpp
floating-point-type ellint_3(floating-point-type k, floating-point-type nu,
                             floating-point-type phi);
float        ellint_3f(float k, float nu, float phi);
long double  ellint_3l(long double k, long double nu, long double phi);
```

> *Effects:*
>
> These functions compute the incomplete elliptic integral of the third
> kind of their respective arguments `k`, `nu`, and `phi` (`phi`
> measured in radians).
>
> *Returns:*
>
> $$\mathsf{\Pi}(\nu, k, \phi) = \int_0^\phi \!
>    \frac{ \mathsf{d}\theta }{ (1 - \nu \, \sin^2 \theta) \sqrt{1 - k^2 \sin^2 \theta} } \text{ ,\quad for $|k| \le 1$,}$$
> where $\nu$ is `nu`, k is `k`, and $\phi$ is `phi`.

#### Exponential integral <a id="sf.cmath.expint">[sf.cmath.expint]</a>

``` cpp
floating-point-type expint(floating-point-type x);
float        expintf(float x);
long double  expintl(long double x);
```

> *Effects:*
>
> These functions compute the exponential integral of their respective
> arguments `x`.
>
> *Returns:*
>
> $$%
>   \mathsf{Ei}(x) =
>   - \int_{-x}^\infty \frac{e^{-t}}
>                           {t     } \, \mathsf{d}t
> \;$$ where x is `x`.

#### Hermite polynomials <a id="sf.cmath.hermite">[sf.cmath.hermite]</a>

``` cpp
floating-point-type hermite(unsigned n, floating-point-type x);
float        hermitef(unsigned n, float x);
long double  hermitel(unsigned n, long double x);
```

> *Effects:*
>
> These functions compute the Hermite polynomials of their respective
> arguments `n` and `x`.
>
> *Returns:*
>
> $$%
>   \mathsf{H}_n(x) =
>   (-1)^n e^{x^2} \frac{ \mathsf{d} ^n}
>               { \mathsf{d}x^n} \, e^{-x^2}
> \;$$ where n is `n` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `n >= 128`.

#### Laguerre polynomials <a id="sf.cmath.laguerre">[sf.cmath.laguerre]</a>

``` cpp
floating-point-type laguerre(unsigned n, floating-point-type x);
float        laguerref(unsigned n, float x);
long double  laguerrel(unsigned n, long double x);
```

> *Effects:*
>
> These functions compute the Laguerre polynomials of their respective
> arguments `n` and `x`.
>
> *Returns:*
>
> $$\mathsf{L}_n(x) =
>      \frac{e^x}{n!} \frac{\mathsf{d}^n}{\mathsf{d}x^n} \, (x^n e^{-x})
>      \text{ ,\quad for $x \ge 0$,}$$ where n is `n` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `n >= 128`.

#### Legendre polynomials <a id="sf.cmath.legendre">[sf.cmath.legendre]</a>

``` cpp
floating-point-type legendre(unsigned l, floating-point-type x);
float        legendref(unsigned l, float x);
long double  legendrel(unsigned l, long double x);
```

> *Effects:*
>
> These functions compute the Legendre polynomials of their respective
> arguments `l` and `x`.
>
> *Returns:*
>
> $$\mathsf{P}_\ell(x) =
>      \frac{1}{2^\ell \, \ell!}
>      \frac{\mathsf{d}^\ell}{\mathsf{d}x^\ell} \, (x^2 - 1) ^ \ell
>      \text{ ,\quad for $|x| \le 1$,}$$ where l is `l` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `l >= 128`.

#### Riemann zeta function <a id="sf.cmath.riemann.zeta">[sf.cmath.riemann.zeta]</a>

``` cpp
floating-point-type riemann_zeta(floating-point-type x);
float        riemann_zetaf(float x);
long double  riemann_zetal(long double x);
```

> *Effects:*
>
> These functions compute the Riemann zeta function of their respective
> arguments `x`.
>
> *Returns:*
>
> $$%
>   \mathsf{\zeta}(x) =
>   \left\{
>   \begin{array}{cl}
>   \displaystyle
>   \sum_{k=1}^\infty k^{-x},
>   & \mbox{for $x > 1$}
>   \\
>   \\
>   \displaystyle
>   \frac{1}
>     {1 - 2^{1-x}}
>   \sum_{k=1}^\infty (-1)^{k-1} k^{-x},
>   & \mbox{for $0 \le x \le 1$}
>   \\
>   \\
>   \displaystyle
>   2^x \pi^{x-1} \sin(\frac{\pi x}{2}) \, \Gamma(1-x) \, \zeta(1-x),
>   & \mbox{for $x < 0$}
>   \end{array}
>   \right.
> \;$$ where x is `x`.

#### Spherical Bessel functions of the first kind <a id="sf.cmath.sph.bessel">[sf.cmath.sph.bessel]</a>

``` cpp
floating-point-type sph_bessel(unsigned n, floating-point-type x);
float        sph_besself(unsigned n, float x);
long double  sph_bessell(unsigned n, long double x);
```

> *Effects:*
>
> These functions compute the spherical Bessel functions of the first
> kind of their respective arguments `n` and `x`.
>
> *Returns:*
>
> $$\mathsf{j}_n(x) = (\pi/2x)^{1\!/\!2} \mathsf{J}_{n + 1\!/\!2}(x) \text{ ,\quad for $x \ge 0$,}$$
> where n is `n` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `n >= 128`.
>
> See also \[sf.cmath.cyl.bessel.j\].

#### Spherical associated Legendre functions <a id="sf.cmath.sph.legendre">[sf.cmath.sph.legendre]</a>

``` cpp
floating-point-type sph_legendre(unsigned l, unsigned m, floating-point-type theta);
float        sph_legendref(unsigned l, unsigned m, float theta);
long double  sph_legendrel(unsigned l, unsigned m, long double theta);
```

> *Effects:*
>
> These functions compute the spherical associated Legendre functions of
> their respective arguments `l`, `m`, and `theta` (`theta` measured in
> radians).
>
> *Returns:*
>
> $$\mathsf{Y}_\ell^m(\theta, 0)$$ where
> $$\mathsf{Y}_\ell^m(\theta, \phi) =
>      (-1)^m \left[\frac{(2 \ell + 1)}{4 \pi} \frac{(\ell - m)!}{(\ell + m)!}\right]^{1/2}
>      \mathsf{P}_\ell^m (\cos\theta) e^{i m \phi}
>      \text{ ,\quad for $|m| \le \ell$,}$$ and l is `l`, m is `m`, and
> θ is `theta`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `l >= 128`.
>
> See also \[sf.cmath.assoc.legendre\].

#### Spherical Neumann functions <a id="sf.cmath.sph.neumann">[sf.cmath.sph.neumann]</a>

``` cpp
floating-point-type sph_neumann(unsigned n, floating-point-type x);
float        sph_neumannf(unsigned n, float x);
long double  sph_neumannl(unsigned n, long double x);
```

> *Effects:*
>
> These functions compute the spherical Neumann functions, also known as
> the spherical Bessel functions of the second kind, of their respective
> arguments `n` and `x`.
>
> *Returns:*
>
> $$\mathsf{n}_n(x) = (\pi/2x)^{1\!/\!2} \mathsf{N}_{n + 1\!/\!2}(x)
>    \text{ ,\quad for $x \ge 0$,}$$ where n is `n` and x is `x`.
>
> *Remarks:*
>
> The effect of calling each of these functions is
> *implementation-defined* if `n >= 128`.
>
> See also \[sf.cmath.cyl.neumann\].

## Numbers <a id="numbers">[numbers]</a>

### Header `<numbers>` synopsis <a id="numbers.syn">[numbers.syn]</a>

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

### Mathematical constants <a id="math.constants">[math.constants]</a>

The library-defined partial specializations of mathematical constant
variable templates are initialized with the nearest representable values
of e, $\log_{2} \mathrm{e}$, $\log_{10} \mathrm{e}$, π, $\frac{1}{\pi}$,
$\frac{1}{\sqrt{\pi}}$, $\ln 2$, $\ln 10$, $\sqrt{2}$, $\sqrt{3}$,
$\frac{1}{\sqrt{3}}$, the Euler-Mascheroni γ constant, and the golden
ratio $\phi$ constant $\frac{1+\sqrt{5}}{2}$, respectively.

Pursuant to [namespace.std], a program may partially or explicitly
specialize a mathematical constant variable template provided that the
specialization depends on a program-defined type.

A program that instantiates a primary template of a mathematical
constant variable template is ill-formed.

<!-- Link reference definitions -->
[bad.alloc]: support.md#bad.alloc
[basic.fundamental]: basic.md#basic.fundamental
[basic.stc.thread]: basic.md#basic.stc.thread
[c.math.hypot3]: #c.math.hypot3
[c.math.lerp]: #c.math.lerp
[cpp.pragma]: cpp.md#cpp.pragma
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.equalitycomparable]: #cpp17.equalitycomparable
[input.output]: input.md#input.output
[iostate.flags]: input.md#iostate.flags
[iterator.concept.contiguous]: iterators.md#iterator.concept.contiguous
[library.c]: library.md#library.c
[namespace.std]: library.md#namespace.std
[numarray]: #numarray
[numerics.summary]: #numerics.summary
[over.match.general]: over.md#over.match.general
[rand]: #rand
[rand.adapt]: #rand.adapt
[rand.dist]: #rand.dist
[rand.eng]: #rand.eng
[rand.eng.lcong]: #rand.eng.lcong
[rand.req.adapt]: #rand.req.adapt
[rand.req.dist]: #rand.req.dist
[rand.req.eng]: #rand.req.eng
[rand.req.seedseq]: #rand.req.seedseq
[rand.req.urng]: #rand.req.urng
[random.access.iterators]: iterators.md#random.access.iterators
[sf.cmath]: #sf.cmath
[strings]: strings.md#strings
[term.literal.type]: #term.literal.type
[thread.jthread.class]: thread.md#thread.jthread.class
[thread.thread.class]: thread.md#thread.thread.class
[utility.arg.requirements]: library.md#utility.arg.requirements
[valarray.members]: #valarray.members
[valarray.range]: #valarray.range

<!-- Link reference definitions -->
[c.math]: #c.math
[cfenv]: #cfenv
[complex.numbers]: #complex.numbers
[numarray]: #numarray
[numbers]: #numbers
[numeric.requirements]: #numeric.requirements
[rand]: #rand
