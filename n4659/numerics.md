# Numerics library <a id="numerics">[[numerics]]</a>

## General <a id="numerics.general">[[numerics.general]]</a>

This Clause describes components that C++programs may use to perform
seminumerical operations.

The following subclauses describe components for complex number types,
random number generation, numeric ( *n*-at-a-time) arrays, generalized
numeric algorithms, and mathematical functions for floating-point types,
as summarized in Table  [[tab:numerics.lib.summary]].

**Table: Numerics library summary**

| Subclause                |                                | Header       |
| ------------------------ | ------------------------------ | ------------ |
| [[numerics.defns]]       | Definitions                    |              |
| [[numeric.requirements]] | Requirements                   |              |
| [[cfenv]]                | Floating-point environment     | `<cfenv>`    |
| [[complex.numbers]]      | Complex numbers                | `<complex>`  |
| [[rand]]                 | Random number generation       | `<random>`   |
| [[numarray]]             | Numeric arrays                 | `<valarray>` |
| [[numeric.ops]]          | Generalized numeric operations | `<numeric>`  |
| [[c.math]]               | Mathematical functions for     | `<cmath>`    |
|                          | floating-point types           | `<cstdlib>`  |


## Definitions <a id="numerics.defns">[[numerics.defns]]</a>

Define `GENERALIZED_NONCOMMUTATIVE_SUM(op, a1, ..., aN)` as follows:

- `a1` when `N` is `1`, otherwise
- `op(GENERALIZED_NONCOMMUTATIVE_SUM(op, a1, ..., aK),`  
  `\phantom{op(}GENERALIZED_NONCOMMUTATIVE_SUM(op, aM, ..., aN))` for
  any `K` where 1 < K+1 = M ≤ N.

Define `GENERALIZED_SUM(op, a1, ..., aN)` as
`GENERALIZED_NONCOMMUTATIVE_SUM(op, b1, ..., bN)`, where `b1, ..., bN`
may be any permutation of `a1, ..., aN`.

## Numeric type requirements <a id="numeric.requirements">[[numeric.requirements]]</a>

The `complex` and `valarray` components are parameterized by the type of
information they contain and manipulate. A C++program shall instantiate
these components only with a type `T` that satisfies the following
requirements:[^1]

- `T` is not an abstract class (it has no pure virtual member
  functions);
- `T` is not a reference type;
- `T` is not cv-qualified;
- If `T` is a class, it has a public default constructor;
- If `T` is a class, it has a public copy constructor with the signature
  `T::T(const T&)`
- If `T` is a class, it has a public destructor;
- If `T` is a class, it has a public assignment operator whose signature
  is either `T& T::operator=(const T&)` or `T& T::operator=(T)`
- If `T` is a class, its assignment operator, copy and default
  constructors, and destructor shall correspond to each other in the
  following sense:
  - Initialization of raw storage using the copy constructor on the
    value of `T()`, however obtained, is semantically equivalent to
    value-initialization of the same raw storage.
  - Initialization of raw storage using the default constructor,
    followed by assignment, is semantically equivalent to initialization
    of raw storage using the copy constructor.
  - Destruction of an object, followed by initialization of its raw
    storage using the copy constructor, is semantically equivalent to
    assignment to the original object.

  \[*Note 1*:
  This rule states, in part, that there shall not be any subtle
  differences in the semantics of initialization versus assignment. This
  gives an implementation considerable flexibility in how arrays are
  initialized.
  \[*Example 1*:
  An implementation is allowed to initialize a `valarray` by allocating
  storage using the `new` operator (which implies a call to the default
  constructor for each element) and then assigning each element its
  value. Or the implementation can allocate raw storage and use the copy
  constructor to initialize each element.
  — *end example*]
  If the distinction between initialization and assignment is important
  for a class, or if it fails to satisfy any of the other conditions
  listed above, the programmer should use `vector` ([[vector]]) instead
  of `valarray` for that class.
  — *end note*]
- If `T` is a class, it does not overload unary `operator&`.

If any operation on `T` throws an exception the effects are undefined.

In addition, many member and related functions of `valarray<T>` can be
successfully instantiated and will exhibit well-defined behavior if and
only if `T` satisfies additional requirements specified for each such
member or related function.

[*Example 1*: It is valid to instantiate `valarray<complex>`, but
`operator>()` will not be successfully instantiated for
`valarray<complex>` operands, since `complex` does not have any ordering
operators. — *end example*]

## The floating-point environment <a id="cfenv">[[cfenv]]</a>

### Header `<cfenv>` synopsis <a id="cfenv.syn">[[cfenv.syn]]</a>

``` cpp
#define FE_ALL_EXCEPT see below
#define FE_DIVBYZERO see below
#define FE_INEXACT see below
#define FE_INVALID see below
#define FE_OVERFLOW see below
#define FE_UNDERFLOW see below

#define FE_DOWNWARD see below
#define FE_TONEAREST see below
#define FE_TOWARDZERO see below
#define FE_UPWARD see below

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

[*Note 1*: This International Standard does not require an
implementation to support the `FENV_ACCESS` pragma; it is
*implementation-defined* ([[cpp.pragma]]) whether the pragma is
supported. As a consequence, it is *implementation-defined* whether
these functions can be used to test floating-point status flags, set
floating-point control modes, or run under non-default mode settings. If
the pragma is used to enable control over the floating-point
environment, this International Standard does not specify the effect on
floating-point evaluation in constant expressions. — *end note*]

The floating-point environment has thread storage duration (
[[basic.stc.thread]]). The initial state for a thread’s floating-point
environment is the state of the floating-point environment of the thread
that constructs the corresponding `thread` object (
[[thread.thread.class]]) at the time it constructed the object.

[*Note 2*: That is, the child thread gets the floating-point state of
the parent thread at the time of the child’s creation. — *end note*]

A separate floating-point environment shall be maintained for each
thread. Each function accesses the environment corresponding to its
calling thread.

ISO C 7.6

## Complex numbers <a id="complex.numbers">[[complex.numbers]]</a>

The header `<complex>` defines a class template, and numerous functions
for representing and manipulating complex numbers.

The effect of instantiating the template `complex` for any type other
than `float`, `double`, or `long double` is unspecified. The
specializations `complex<float>`, `complex<double>`, and
`complex<long double>` are literal types ([[basic.types]]).

If the result of a function is not mathematically defined or not in the
range of representable values for its type, the behavior is undefined.

If `z` is an lvalue expression of type cv `complex<T>` then:

- the expression `reinterpret_cast<cv{} T(&)[2]>(z)` shall be
  well-formed,
- `reinterpret_cast<cv{} T(&)[2]>(z)[0]` shall designate the real part
  of `z`, and
- `reinterpret_cast<cv{} T(&)[2]>(z)[1]` shall designate the imaginary
  part of `z`.

Moreover, if `a` is an expression of type cv `complex<T>*` and the
expression `a[i]` is well-defined for an integer expression `i`, then:

- `reinterpret_cast<cv{} T*>(a)[2*i]` shall designate the real part of
  `a[i]`, and
- `reinterpret_cast<cv{} T*>(a)[2*i + 1]` shall designate the imaginary
  part of `a[i]`.

### Header `<complex>` synopsis <a id="complex.syn">[[complex.syn]]</a>

``` cpp
namespace std {
  template<class T> class complex;
  template<> class complex<float>;
  template<> class complex<double>;
  template<> class complex<long double>;

  // [complex.ops], operators
  template<class T>
    complex<T> operator+(const complex<T>&, const complex<T>&);
  template<class T> complex<T> operator+(const complex<T>&, const T&);
  template<class T> complex<T> operator+(const T&, const complex<T>&);

  template<class T> complex<T> operator-(
    const complex<T>&, const complex<T>&);
  template<class T> complex<T> operator-(const complex<T>&, const T&);
  template<class T> complex<T> operator-(const T&, const complex<T>&);

  template<class T> complex<T> operator*(
    const complex<T>&, const complex<T>&);
  template<class T> complex<T> operator*(const complex<T>&, const T&);
  template<class T> complex<T> operator*(const T&, const complex<T>&);

  template<class T> complex<T> operator/(
    const complex<T>&, const complex<T>&);
  template<class T> complex<T> operator/(const complex<T>&, const T&);
  template<class T> complex<T> operator/(const T&, const complex<T>&);

  template<class T> complex<T> operator+(const complex<T>&);
  template<class T> complex<T> operator-(const complex<T>&);

  template<class T> constexpr bool operator==(
    const complex<T>&, const complex<T>&);
  template<class T> constexpr bool operator==(const complex<T>&, const T&);
  template<class T> constexpr bool operator==(const T&, const complex<T>&);

  template<class T> constexpr bool operator!=(const complex<T>&, const complex<T>&);
  template<class T> constexpr bool operator!=(const complex<T>&, const T&);
  template<class T> constexpr bool operator!=(const T&, const complex<T>&);

  template<class T, class charT, class traits>
  basic_istream<charT, traits>&
  operator>>(basic_istream<charT, traits>&, complex<T>&);

  template<class T, class charT, class traits>
  basic_ostream<charT, traits>&
  operator<<(basic_ostream<charT, traits>&, const complex<T>&);

  // [complex.value.ops], values
  template<class T> constexpr T real(const complex<T>&);
  template<class T> constexpr T imag(const complex<T>&);

  template<class T> T abs(const complex<T>&);
  template<class T> T arg(const complex<T>&);
  template<class T> T norm(const complex<T>&);

  template<class T> complex<T> conj(const complex<T>&);
  template<class T> complex<T> proj(const complex<T>&);
  template<class T> complex<T> polar(const T&, const T& = 0);

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

### Class template `complex` <a id="complex">[[complex]]</a>

``` cpp
namespace std {
  template<class T>
  class complex {
  public:
    using value_type = T;

    constexpr complex(const T& re = T(), const T& im = T());
    constexpr complex(const complex&);
    template<class X> constexpr complex(const complex<X>&);

    constexpr T real() const;
    void real(T);
    constexpr T imag() const;
    void imag(T);

    complex<T>& operator= (const T&);
    complex<T>& operator+=(const T&);
    complex<T>& operator-=(const T&);
    complex<T>& operator*=(const T&);
    complex<T>& operator/=(const T&);

    complex& operator=(const complex&);
    template<class X> complex<T>& operator= (const complex<X>&);
    template<class X> complex<T>& operator+=(const complex<X>&);
    template<class X> complex<T>& operator-=(const complex<X>&);
    template<class X> complex<T>& operator*=(const complex<X>&);
    template<class X> complex<T>& operator/=(const complex<X>&);
  };
}
```

The class `complex` describes an object that can store the Cartesian
components, `real()` and `imag()`, of a complex number.

### `complex` specializations <a id="complex.special">[[complex.special]]</a>

``` cpp
namespace std {
  template<> class complex<float> {
  public:
    using value_type = float;

    constexpr complex(float re = 0.0f, float im = 0.0f);
    constexpr explicit complex(const complex<double>&);
    constexpr explicit complex(const complex<long double>&);

    constexpr float real() const;
    void real(float);
    constexpr float imag() const;
    void imag(float);

    complex<float>& operator= (float);
    complex<float>& operator+=(float);
    complex<float>& operator-=(float);
    complex<float>& operator*=(float);
    complex<float>& operator/=(float);

    complex<float>& operator=(const complex<float>&);
    template<class X> complex<float>& operator= (const complex<X>&);
    template<class X> complex<float>& operator+=(const complex<X>&);
    template<class X> complex<float>& operator-=(const complex<X>&);
    template<class X> complex<float>& operator*=(const complex<X>&);
    template<class X> complex<float>& operator/=(const complex<X>&);
  };

  template<> class complex<double> {
  public:
    using value_type = double;

    constexpr complex(double re = 0.0, double im = 0.0);
    constexpr complex(const complex<float>&);
    constexpr explicit complex(const complex<long double>&);

    constexpr double real() const;
    void real(double);
    constexpr double imag() const;
    void imag(double);

    complex<double>& operator= (double);
    complex<double>& operator+=(double);
    complex<double>& operator-=(double);
    complex<double>& operator*=(double);
    complex<double>& operator/=(double);

    complex<double>& operator=(const complex<double>&);
    template<class X> complex<double>& operator= (const complex<X>&);
    template<class X> complex<double>& operator+=(const complex<X>&);
    template<class X> complex<double>& operator-=(const complex<X>&);
    template<class X> complex<double>& operator*=(const complex<X>&);
    template<class X> complex<double>& operator/=(const complex<X>&);
  };

  template<> class complex<long double> {
  public:
    using value_type = long double;

    constexpr complex(long double re = 0.0L, long double im = 0.0L);
    constexpr complex(const complex<float>&);
    constexpr complex(const complex<double>&);

    constexpr long double real() const;
    void real(long double);
    constexpr long double imag() const;
    void imag(long double);

    complex<long double>& operator=(const complex<long double>&);
    complex<long double>& operator= (long double);
    complex<long double>& operator+=(long double);
    complex<long double>& operator-=(long double);
    complex<long double>& operator*=(long double);
    complex<long double>& operator/=(long double);

    template<class X> complex<long double>& operator= (const complex<X>&);
    template<class X> complex<long double>& operator+=(const complex<X>&);
    template<class X> complex<long double>& operator-=(const complex<X>&);
    template<class X> complex<long double>& operator*=(const complex<X>&);
    template<class X> complex<long double>& operator/=(const complex<X>&);
  };
}
```

### `complex` member functions <a id="complex.members">[[complex.members]]</a>

``` cpp
template<class T> constexpr complex(const T& re = T(), const T& im = T());
```

*Effects:* Constructs an object of class `complex`.

*Postconditions:* `real() == re && imag() == im`.

``` cpp
constexpr T real() const;
```

*Returns:* The value of the real component.

``` cpp
void real(T val);
```

*Effects:* Assigns `val` to the real component.

``` cpp
constexpr T imag() const;
```

*Returns:* The value of the imaginary component.

``` cpp
void imag(T val);
```

*Effects:* Assigns `val` to the imaginary component.

### `complex` member operators <a id="complex.member.ops">[[complex.member.ops]]</a>

``` cpp
complex<T>& operator+=(const T& rhs);
```

*Effects:* Adds the scalar value `rhs` to the real part of the complex
value `*this` and stores the result in the real part of `*this`, leaving
the imaginary part unchanged.

*Returns:* `*this`.

``` cpp
complex<T>& operator-=(const T& rhs);
```

*Effects:* Subtracts the scalar value `rhs` from the real part of the
complex value `*this` and stores the result in the real part of `*this`,
leaving the imaginary part unchanged.

*Returns:* `*this`.

``` cpp
complex<T>& operator*=(const T& rhs);
```

*Effects:* Multiplies the scalar value `rhs` by the complex value
`*this` and stores the result in `*this`.

*Returns:* `*this`.

``` cpp
complex<T>& operator/=(const T& rhs);
```

*Effects:* Divides the scalar value `rhs` into the complex value `*this`
and stores the result in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> complex<T>& operator+=(const complex<X>& rhs);
```

*Effects:* Adds the complex value `rhs` to the complex value `*this` and
stores the sum in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> complex<T>& operator-=(const complex<X>& rhs);
```

*Effects:* Subtracts the complex value `rhs` from the complex value
`*this` and stores the difference in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> complex<T>& operator*=(const complex<X>& rhs);
```

*Effects:* Multiplies the complex value `rhs` by the complex value
`*this` and stores the product in `*this`.

*Returns:* `*this`.

``` cpp
template<class X> complex<T>& operator/=(const complex<X>& rhs);
```

*Effects:* Divides the complex value `rhs` into the complex value
`*this` and stores the quotient in `*this`.

*Returns:* `*this`.

### `complex` non-member operations <a id="complex.ops">[[complex.ops]]</a>

``` cpp
template<class T> complex<T> operator+(const complex<T>& lhs);
```

*Returns:* `complex<T>(lhs)`.

*Remarks:* unary operator.

``` cpp
template<class T> complex<T> operator+(const complex<T>& lhs, const complex<T>& rhs);
template<class T> complex<T> operator+(const complex<T>& lhs, const T& rhs);
template<class T> complex<T> operator+(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) += rhs`.

``` cpp
template<class T> complex<T> operator-(const complex<T>& lhs);
```

*Returns:* `complex<T>(-lhs.real(),-lhs.imag())`.

*Remarks:* unary operator.

``` cpp
template<class T> complex<T> operator-(const complex<T>& lhs, const complex<T>& rhs);
template<class T> complex<T> operator-(const complex<T>& lhs, const T& rhs);
template<class T> complex<T> operator-(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) -= rhs`.

``` cpp
template<class T> complex<T> operator*(const complex<T>& lhs, const complex<T>& rhs);
template<class T> complex<T> operator*(const complex<T>& lhs, const T& rhs);
template<class T> complex<T> operator*(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) *= rhs`.

``` cpp
template<class T> complex<T> operator/(const complex<T>& lhs, const complex<T>& rhs);
template<class T> complex<T> operator/(const complex<T>& lhs, const T& rhs);
template<class T> complex<T> operator/(const T& lhs, const complex<T>& rhs);
```

*Returns:* `complex<T>(lhs) /= rhs`.

``` cpp
template<class T> constexpr bool operator==(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr bool operator==(const complex<T>& lhs, const T& rhs);
template<class T> constexpr bool operator==(const T& lhs, const complex<T>& rhs);
```

*Returns:* `lhs.real() == rhs.real() && lhs.imag() == rhs.imag()`.

*Remarks:* The imaginary part is assumed to be `T()`, or 0.0, for the
`T` arguments.

``` cpp
template<class T> constexpr bool operator!=(const complex<T>& lhs, const complex<T>& rhs);
template<class T> constexpr bool operator!=(const complex<T>& lhs, const T& rhs);
template<class T> constexpr bool operator!=(const T& lhs, const complex<T>& rhs);
```

*Returns:* `rhs.real() != lhs.real() || rhs.imag() != lhs.imag()`.

``` cpp
template<class T, class charT, class traits>
basic_istream<charT, traits>&
operator>>(basic_istream<charT, traits>& is, complex<T>& x);
```

*Requires:* The input values shall be convertible to `T`.

*Effects:* Extracts a complex number `x` of the form: `u`, `(u)`, or
`(u,v)`, where `u` is the real part and `v` is the imaginary
part ([[istream.formatted]]).

If bad input is encountered, calls `is.setstate(ios_base::failbit)`
(which may throw `ios::failure` ([[iostate.flags]])).

*Returns:* `is`.

*Remarks:* This extraction is performed as a series of simpler
extractions. Therefore, the skipping of whitespace is specified to be
the same for each of the simpler extractions.

``` cpp
template<class T, class charT, class traits>
basic_ostream<charT, traits>&
operator<<(basic_ostream<charT, traits>& o, const complex<T>& x);
```

*Effects:* Inserts the complex number `x` onto the stream `o` as if it
were implemented as follows:

``` cpp
basic_ostringstream<charT, traits> s;
s.flags(o.flags());
s.imbue(o.getloc());
s.precision(o.precision());
s << '(' << x.real() << "," << x.imag() << ')';
return o << s.str();
```

[*Note 1*: In a locale in which comma is used as a decimal point
character, the use of comma as a field separator can be ambiguous.
Inserting `showpoint` into the output stream forces all outputs to show
an explicit decimal point character; as a result, all inserted sequences
of complex numbers can be extracted unambiguously. — *end note*]

### `complex` value operations <a id="complex.value.ops">[[complex.value.ops]]</a>

``` cpp
template<class T> constexpr T real(const complex<T>& x);
```

*Returns:* `x.real()`.

``` cpp
template<class T> constexpr T imag(const complex<T>& x);
```

*Returns:* `x.imag()`.

``` cpp
template<class T> T abs(const complex<T>& x);
```

*Returns:* The magnitude of `x`.

``` cpp
template<class T> T arg(const complex<T>& x);
```

*Returns:* The phase angle of `x`, or `atan2(imag(x), real(x))`.

``` cpp
template<class T> T norm(const complex<T>& x);
```

*Returns:* The squared magnitude of `x`.

``` cpp
template<class T> complex<T> conj(const complex<T>& x);
```

*Returns:* The complex conjugate of `x`.

``` cpp
template<class T> complex<T> proj(const complex<T>& x);
```

*Returns:* The projection of `x` onto the Riemann sphere.

*Remarks:* Behaves the same as the C function `cproj`, defined in
7.3.9.4.

``` cpp
template<class T> complex<T> polar(const T& rho, const T& theta = 0);
```

*Requires:* `rho` shall be non-negative and non-NaN. `theta` shall be
finite.

*Returns:* The `complex` value corresponding to a complex number whose
magnitude is `rho` and whose phase angle is `theta`.

### `complex` transcendentals <a id="complex.transcendentals">[[complex.transcendentals]]</a>

``` cpp
template<class T> complex<T> acos(const complex<T>& x);
```

*Returns:* The complex arc cosine of `x`.

*Remarks:* Behaves the same as C function `cacos`, defined in 7.3.5.1.

``` cpp
template<class T> complex<T> asin(const complex<T>& x);
```

*Returns:* The complex arc sine of `x`.

*Remarks:* Behaves the same as C function `casin`, defined in 7.3.5.2.

``` cpp
template<class T> complex<T> atan(const complex<T>& x);
```

*Returns:* The complex arc tangent of `x`.

*Remarks:* Behaves the same as C function `catan`, defined in 7.3.5.3.

``` cpp
template<class T> complex<T> acosh(const complex<T>& x);
```

*Returns:* The complex arc hyperbolic cosine of `x`.

*Remarks:* Behaves the same as C function `cacosh`, defined in 7.3.6.1.

``` cpp
template<class T> complex<T> asinh(const complex<T>& x);
```

*Returns:* The complex arc hyperbolic sine of `x`.

*Remarks:* Behaves the same as C function `casinh`, defined in 7.3.6.2.

``` cpp
template<class T> complex<T> atanh(const complex<T>& x);
```

*Returns:* The complex arc hyperbolic tangent of `x`.

*Remarks:* Behaves the same as C function `catanh`, defined in 7.3.6.3.

``` cpp
template<class T> complex<T> cos(const complex<T>& x);
```

*Returns:* The complex cosine of `x`.

``` cpp
template<class T> complex<T> cosh(const complex<T>& x);
```

*Returns:* The complex hyperbolic cosine of `x`.

``` cpp
template<class T> complex<T> exp(const complex<T>& x);
```

*Returns:* The complex base-e exponential of `x`.

``` cpp
template<class T> complex<T> log(const complex<T>& x);
```

*Returns:* The complex natural (base-e) logarithm of `x`. For all `x`,
`imag(log(x))` lies in the interval \[-π, π\], and when `x` is a
negative real number, `imag(log(x))` is π.

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> log10(const complex<T>& x);
```

*Returns:* The complex common (base-10) logarithm of `x`, defined as
`log(x) / log(10)`.

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> pow(const complex<T>& x, const complex<T>& y);
template<class T> complex<T> pow(const complex<T>& x, const T& y);
template<class T> complex<T> pow(const T& x, const complex<T>& y);
```

*Returns:* The complex power of base `x` raised to the `y`ᵗʰ power,
defined as `exp(y * log(x))`. The value returned for `pow(0, 0)` is
*implementation-defined*.

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> sin(const complex<T>& x);
```

*Returns:* The complex sine of `x`.

``` cpp
template<class T> complex<T> sinh(const complex<T>& x);
```

*Returns:* The complex hyperbolic sine of `x`.

``` cpp
template<class T> complex<T> sqrt(const complex<T>& x);
```

*Returns:* The complex square root of `x`, in the range of the right
half-plane. If the argument is a negative real number, the value
returned lies on the positive imaginary axis.

*Remarks:* The branch cuts are along the negative real axis.

``` cpp
template<class T> complex<T> tan(const complex<T>& x);
```

*Returns:* The complex tangent of `x`.

``` cpp
template<class T> complex<T> tanh(const complex<T>& x);
```

*Returns:* The complex hyperbolic tangent of `x`.

### Additional overloads <a id="cmplx.over">[[cmplx.over]]</a>

The following function templates shall have additional overloads:

``` cpp
arg                   norm
conj                  proj
imag                  real
```

The additional overloads shall be sufficient to ensure:

1.  If the argument has type `long double`, then it is effectively cast
    to `complex<long double>`.
2.  Otherwise, if the argument has type `double` or an integer type,
    then it is effectively cast to `complex<{}double>`.
3.  Otherwise, if the argument has type `float`, then it is effectively
    cast to `complex<float>`.

Function template `pow` shall have additional overloads sufficient to
ensure, for a call with at least one argument of type `complex<T>`:

1.  If either argument has type `complex<long double>` or type `long
            double`, then both arguments are effectively cast to
    `complex<long double>`.
2.  Otherwise, if either argument has type `complex<double>`, `double`,
    or an integer type, then both arguments are effectively cast to
    `complex<double>`.
3.  Otherwise, if either argument has type `complex<float>` or `float`,
    then both arguments are effectively cast to `complex<float>`.

### Suffixes for complex number literals <a id="complex.literals">[[complex.literals]]</a>

This section describes literal suffixes for constructing complex number
literals. The suffixes `i`, `il`, and `if` create complex numbers of the
types `complex<double>`, `complex<long double>`, and `complex<float>`
respectively, with their imaginary part denoted by the given literal
number and the real part being zero.

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

This subclause defines a facility for generating (pseudo-)random
numbers.

In addition to a few utilities, four categories of entities are
described: , , , and . These categorizations are applicable to types
that satisfy the corresponding requirements, to objects instantiated
from such types, and to templates producing such types when
instantiated.

[*Note 1*: These entities are specified in such a way as to permit the
binding of any uniform random bit generator object `e` as the argument
to any random number distribution object `d`, thus producing a
zero-argument function object such as given by
`bind(d,e)`. — *end note*]

Each of the entities specified via this subclause has an associated
arithmetic type ([[basic.fundamental]]) identified as `result_type`.
With `T` as the `result_type` thus associated with such an entity, that
entity is characterized:

If integer-valued, an entity may optionally be further characterized as
or , according to `numeric_limits<T>::is_signed`.

Unless otherwise specified, all descriptions of calculations in this
subclause use mathematical real numbers.

Throughout this subclause, the operators , , and denote the respective
conventional bitwise operations. Further:

### Requirements <a id="rand.req">[[rand.req]]</a>

#### General requirements <a id="rand.req.genl">[[rand.req.genl]]</a>

Throughout this subclause [[rand]], the effect of instantiating a
template:

Throughout this subclause [[rand]], phrases of the form “`x` is an
iterator of a specific kind” shall be interpreted as equivalent to the
more formal requirement that “`x` is a value of a type satisfying the
requirements of the specified iterator type”.

Throughout this subclause [[rand]], any constructor that can be called
with a single argument and that satisfies a requirement specified in
this subclause shall be declared `explicit`.

#### Seed sequence requirements <a id="rand.req.seedseq">[[rand.req.seedseq]]</a>

A is an object that consumes a sequence of integer-valued data and
produces a requested number of unsigned integer values i, 0 ≤ i < 2³²,
based on the consumed data.

[*Note 1*: Such an object provides a mechanism to avoid replication of
streams of random variates. This can be useful, for example, in
applications requiring large numbers of random number
engines. — *end note*]

A class `S` satisfies the requirements of a seed sequence if the
expressions shown in Table  [[tab:SeedSequence]] are valid and have the
indicated semantics, and if `S` also satisfies all other requirements of
this section [[rand.req.seedseq]]. In that Table and throughout this
section:

#### Uniform random bit generator requirements <a id="rand.req.urng">[[rand.req.urng]]</a>

A `g` of type `G` is a function object returning unsigned integer values
such that each value in the range of possible results has (ideally)
equal probability of being returned.

[*Note 1*: The degree to which `g`’s results approximate the ideal is
often determined statistically. — *end note*]

A class `G` satisfies the requirements of a if the expressions shown in
Table  [[tab:UniformRandomBitGenerator]] are valid and have the
indicated semantics, and if `G` also satisfies all other requirements of
this section [[rand.req.urng]]. In that Table and throughout this
section:

The following relation shall hold: `G::min() < G::max()`.

#### Random number engine requirements <a id="rand.req.eng">[[rand.req.eng]]</a>

A (commonly shortened to ) `e` of type `E` is a uniform random bit
generator that additionally meets the requirements (e.g., for seeding
and for input/output) specified in this section.

At any given time, `e` has a state for some integer i ≥ 0. Upon
construction, `e` has an initial state . An engine’s state may be
established via a constructor, a `seed` function, assignment, or a
suitable `operator>>`.

`E`’s specification shall define:

A class `E` that satisfies the requirements of a uniform random bit
generator ([[rand.req.urng]]) also satisfies the requirements of a if
the expressions shown in Table  [[tab:RandomEngine]] are valid and have
the indicated semantics, and if `E` also satisfies all other
requirements of this section [[rand.req.eng]]. In that Table and
throughout this section:

where `charT` and `traits` are constrained according to Clause 
[[strings]] and Clause  [[input.output]].

`E` shall meet the requirements of `CopyConstructible` (Table 
[[tab:copyconstructible]]) and `CopyAssignable` (Table 
[[tab:copyassignable]]) types. These operations shall each be of
complexity no worse than .

#### Random number engine adaptor requirements <a id="rand.req.adapt">[[rand.req.adapt]]</a>

A (commonly shortened to ) `a` of type `A` is a random number engine
that takes values produced by some other random number engine, and
applies an algorithm to those values in order to deliver a sequence of
values with different randomness properties. An engine `b` of type `B`
adapted in this way is termed a in this context. The expression
`a.base()` shall be valid and shall return a const reference to `a`’s
base engine.

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

`A` shall also satisfy the following additional requirements:

#### Random number distribution requirements <a id="rand.req.dist">[[rand.req.dist]]</a>

A (commonly shortened to ) `d` of type `D` is a function object
returning values that are distributed according to an associated
mathematical p(z) or according to an associated P(zᵢ). A distribution’s
specification identifies its associated probability function p(z) or
P(zᵢ).

An associated probability function is typically expressed using certain
externally-supplied quantities known as the . Such distribution
parameters are identified in this context by writing, for example,
p(z | a,b) or P(zᵢ | a,b), to name specific parameters, or by writing,
for example, p(z |{`p`}) or P(zᵢ |{`p`}), to denote a distribution’s
parameters `p` taken as a whole.

A class `D` satisfies the requirements of a if the expressions shown in
Table  [[tab:RandomDistribution]] are valid and have the indicated
semantics, and if `D` and its associated types also satisfy all other
requirements of this section [[rand.req.dist]]. In that Table and
throughout this section,

where `charT` and `traits` are constrained according to Clauses 
[[strings]] and [[input.output]].

`D` shall satisfy the requirements of `CopyConstructible` (Table 
[[tab:copyconstructible]]) and `CopyAssignable` (Table 
[[tab:copyassignable]]) types.

The sequence of numbers produced by repeated invocations of `d(g)` shall
be independent of any invocation of `os << d` or of any `const` member
function of `D` between any of the invocations `d(g)`.

If a textual representation is written using `os << x` and that
representation is restored into the same or a different object `y` of
the same type using `is >> y`, repeated invocations of `y(g)` shall
produce the same sequence of numbers as would repeated invocations of
`x(g)`.

It is unspecified whether `D::param_type` is declared as a (nested)
`class` or via a `typedef`. In this subclause [[rand]], declarations of
`D::param_type` are in the form of `typedef`s for convenience of
exposition only.

`P` shall satisfy the requirements of `CopyConstructible` (Table 
[[tab:copyconstructible]]), `CopyAssignable` (Table 
[[tab:copyassignable]]), and `EqualityComparable` (Table 
[[tab:equalitycomparable]]) types.

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

### Header `<random>` synopsis <a id="rand.synopsis">[[rand.synopsis]]</a>

``` cpp
#include <initializer_list>

namespace std {
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

### Random number engine class templates <a id="rand.eng">[[rand.eng]]</a>

Each type instantiated from a class template specified in this section 
[[rand.eng]] satisfies the requirements of a random number engine (
[[rand.req.eng]]) type.

Except where specified otherwise, the complexity of each function
specified in this section  [[rand.eng]] is constant.

Except where specified otherwise, no function described in this section 
[[rand.eng]] throws an exception.

Every function described in this section  [[rand.eng]] that has a
function parameter `q` of type `Sseq&` for a template type parameter
named `Sseq` that is different from type `seed_seq` throws what and when
the invocation of `q.generate` throws.

Descriptions are provided in this section  [[rand.eng]] only for engine
operations that are not described in [[rand.req.eng]] or for operations
where there is additional semantic information. In particular,
declarations for copy constructors, for copy assignment operators, for
streaming operators, and for equality and inequality operators are not
shown in the synopses.

Each template specified in this section  [[rand.eng]] requires one or
more relationships, involving the value(s) of its non-type template
parameter(s), to hold. A program instantiating any of these templates is
ill-formed if any such required relationship fails to hold.

For every random number engine and for every random number engine
adaptor `X` defined in this subclause ([[rand.eng]]) and in subclause 
[[rand.adapt]]:

- if the constructor
  ``` cpp
  template <class Sseq> explicit X(Sseq& q);
  ```

  is called with a type `Sseq` that does not qualify as a seed sequence,
  then this constructor shall not participate in overload resolution;
- if the member function
  ``` cpp
  template <class Sseq> void seed(Sseq& q);
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
    explicit linear_congruential_engine(result_type s = default_seed);
    template<class Sseq> explicit linear_congruential_engine(Sseq& q);
    void seed(result_type s = default_seed);
    template<class Sseq> void seed(Sseq& q);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);
  };
```

If the template parameter `m` is 0, the modulus m used throughout this
section  [[rand.eng.lcong]] is `numeric_limits<result_type>::max()` plus
1.

[*Note 1*: m need not be representable as a value of type
`result_type`. — *end note*]

If the template parameter `m` is not 0, the following relations shall
hold: `a < m` and `c < m`.

The textual representation consists of the value of .

``` cpp
explicit linear_congruential_engine(result_type s = default_seed);
```

*Effects:* Constructs a `linear_congruential_engine` object. If
c  mod  m is 0 and `s`  mod  m is 0, sets the engine’s state to 1,
otherwise sets the engine’s state to `s`  mod  m.

``` cpp
template<class Sseq> explicit linear_congruential_engine(Sseq& q);
```

*Effects:* Constructs a `linear_congruential_engine` object. With
$k = \left\lceil \frac{\log_2 m}
                        {32}
            \right\rceil$ and a an array (or equivalent) of length
k + 3, invokes `q.generate(`a+0`, `a+k+3`)` and then computes
$S = \left(\sum_{j=0}^{k-1}a_{j+3} \cdot 2^{32j} \right) \bmod m$. If
c  mod  m is 0 and S is 0, sets the engine’s state to 1, else sets the
engine’s state to S.

#### Class template `mersenne_twister_engine` <a id="rand.eng.mers">[[rand.eng.mers]]</a>

A `mersenne_twister_engine` random number engine[^2] produces unsigned
integer random numbers in the closed interval [0,2ʷ-1]. The state of a
`mersenne_twister_engine` object `x` is of size n and consists of a
sequence X of n values of the type delivered by `x`; all subscripts
applied to X are to be taken modulo n.

The transition algorithm employs a twisted generalized feedback shift
register defined by shift values n and m, a twist value r, and a
conditional xor-mask a. To improve the uniformity of the result, the
bits of the raw shift register are additionally (i.e., scrambled)
according to a bit-scrambling matrix defined by values u, d, s, b, t, c,
and ℓ.

The state transition is performed as follows:

The sequence X is initialized with the help of an initialization
multiplier f.

The generation algorithm determines the unsigned integer values
z₁, z₂, z₃, z₄ as follows, then delivers z₄ as its result:

``` cpp
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
    explicit mersenne_twister_engine(result_type value = default_seed);
    template<class Sseq> explicit mersenne_twister_engine(Sseq& q);
    void seed(result_type value = default_seed);
    template<class Sseq> void seed(Sseq& q);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);
  };
```

The following relations shall hold: `0 < m`, `m <= n`, `2u < w`,
`r <= w`, `u <= w`, `s <= w`, `t <= w`, `l <= w`,
`w <= numeric_limits<UIntType>::digits`, `a <= (1u<<w) - 1u`,
`b <= (1u<<w) - 1u`, `c <= (1u<<w) - 1u`, `d <= (1u<<w) - 1u`, and
`f <= (1u<<w) - 1u`.

The textual representation of consists of the values of Xᵢ₋ₙ, …, Xᵢ₋₁,
in that order.

``` cpp
explicit mersenne_twister_engine(result_type value = default_seed);
```

*Effects:* Constructs a `mersenne_twister_engine` object. Sets X₋ₙ to
`value`  mod  2ʷ. Then, iteratively for i = 1-n,…,-1, sets Xᵢ to $$%
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

*Effects:* Constructs a `mersenne_twister_engine` object. With
k = ⌈ w / 32 ⌉ and a an array (or equivalent) of length n ⋅ k, invokes
`q.generate(`a+0`, `a+n ⋅ k`)` and then, iteratively for i = -n,…,-1,
sets Xᵢ to
$\left(\sum_{j=0}^{k-1}a_{k(i+n)+j} \cdot 2^{32j} \right) \bmod 2^w$.
Finally, if the most significant w-r bits of X₋ₙ are zero, and if each
of the other resulting Xᵢ is 0, changes X₋ₙ to 2ʷ⁻¹.

#### Class template `subtract_with_carry_engine` <a id="rand.eng.sub">[[rand.eng.sub]]</a>

A `subtract_with_carry_engine` random number engine produces unsigned
integer random numbers.

The state of a `subtract_with_carry_engine` object `x` is of size , and
consists of a sequence X of r integer values 0 ≤ Xᵢ < m  = 2ʷ; all
subscripts applied to X are to be taken modulo r. The state additionally
consists of an integer c (known as the ) whose value is either 0 or 1.

The state transition is performed as follows:

[*Note 1*: This algorithm corresponds to a modular linear function of
the form $\mathsf{TA}(\state{x}{i}) = (a \cdot \state{x}{i}) \bmod b$,
where b is of the form mʳ - mˢ + 1 and a = b - (b-1) / m. — *end note*]

The generation algorithm is given by $\mathsf{GA}(\state{x}{i}) = y$,
where y is the value produced as a result of advancing the engine’s
state as described above.

``` cpp
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
    static constexpr result_type default_seed = 19780503u;

    // constructors and seeding functions
    explicit subtract_with_carry_engine(result_type value = default_seed);
    template<class Sseq> explicit subtract_with_carry_engine(Sseq& q);
    void seed(result_type value = default_seed);
    template<class Sseq> void seed(Sseq& q);

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);
  };
```

The following relations shall hold: `0u < s`, `s < r`, `0 < w`, and
`w <= numeric_limits<UIntType>::digits`.

The textual representation consists of the values of Xᵢ₋ᵣ, …, Xᵢ₋₁, in
that order, followed by c.

``` cpp
explicit subtract_with_carry_engine(result_type value = default_seed);
```

*Effects:* Constructs a `subtract_with_carry_engine` object. Sets the
values of X₋ᵣ, …, X₋₁, in that order, as specified below. If X₋₁ is then
0, sets c to 1; otherwise sets c to 0.

To set the values Xₖ, first construct `e`, a
`linear_congruential_engine` object, as if by the following definition:

``` cpp
linear_congruential_engine<result_type,
                          40014u,0u,2147483563u> e(value == 0u ? default_seed : value);
```

Then, to set each Xₖ, obtain new values z₀, …, zₙ₋₁ from n = ⌈ w/32 ⌉
successive invocations of `e` taken modulo 2³². Set Xₖ to
$\left( \sum_{j=0}^{n-1} z_j \cdot 2^{32j}\right) \bmod m$.

*Complexity:* Exactly n ⋅ `r` invocations of `e`.

``` cpp
template<class Sseq> explicit subtract_with_carry_engine(Sseq& q);
```

*Effects:* Constructs a `subtract_with_carry_engine` object. With
k = ⌈ w / 32 ⌉ and a an array (or equivalent) of length r ⋅ k, invokes
`q.generate(`a+0`, `a+r ⋅ k`)` and then, iteratively for i = -r, …, -1,
sets Xᵢ to
$\left(\sum_{j=0}^{k-1}a_{k(i+r)+j} \cdot 2^{32j} \right) \bmod m$. If
X₋₁ is then 0, sets c to 1; otherwise sets c to 0.

### Random number engine adaptor class templates <a id="rand.adapt">[[rand.adapt]]</a>

#### In general <a id="rand.adapt.general">[[rand.adapt.general]]</a>

Each type instantiated from a class template specified in this section 
[[rand.adapt]] satisfies the requirements of a random number engine
adaptor ([[rand.req.adapt]]) type.

Except where specified otherwise, the complexity of each function
specified in this section  [[rand.adapt]] is constant.

Except where specified otherwise, no function described in this section 
[[rand.adapt]] throws an exception.

Every function described in this section  [[rand.adapt]] that has a
function parameter `q` of type `Sseq&` for a template type parameter
named `Sseq` that is different from type `seed_seq` throws what and when
the invocation of `q.generate` throws.

Descriptions are provided in this section  [[rand.adapt]] only for
adaptor operations that are not described in section  [[rand.req.adapt]]
or for operations where there is additional semantic information. In
particular, declarations for copy constructors, for copy assignment
operators, for streaming operators, and for equality and inequality
operators are not shown in the synopses.

Each template specified in this section  [[rand.adapt]] requires one or
more relationships, involving the value(s) of its non-type template
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

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // property functions
    const Engine& base() const noexcept { return e; };

  private:
    Engine e;   // exposition only
    int n;      // exposition only
  };
```

The following relations shall hold: `0 < r` and `r <= p`.

The textual representation consists of the textual representation of `e`
followed by the value of `n`.

In addition to its behavior pursuant to section  [[rand.req.adapt]],
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

[*Note 1*: The relation w = n₀ w₀ + (n - n₀)(w₀ + 1) always
holds. — *end note*]

The transition algorithm is carried out by invoking `e()` as often as
needed to obtain n₀ values less than y₀ + `e.min()` and n - n₀ values
less than y₁ + `e.min()` .

The generation algorithm uses the values produced while advancing the
state as described above to yield a quantity S obtained as if by the
following algorithm:

``` cpp
S = 0;
for (k = 0; k \neq n₀; k += 1)  {
 do u = e() - e.min(); while ( u \ge y₀ );
 S =  2^{w₀ \cdot S + u \bmod 2^{w₀ ;
}
for (k = n₀; k \neq n; k += 1)  {
 do u = e() - e.min(); while ( u \ge y₁ );
 S =  2^{w₀ + 1} \cdot S + u \bmod 2^{w₀ + 1} ;
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

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // property functions
    const Engine& base() const noexcept { return e; };

  private:
    Engine e;   // exposition only
  };
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
the state is the size of e’s state plus k+1.

The transition algorithm permutes the values produced by e. The state
transition is performed as follows:

The generation algorithm yields the last value of `Y` produced while
advancing `e`’s state as described above.

``` cpp
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

    // generating functions
    result_type operator()();
    void discard(unsigned long long z);

    // property functions
    const Engine& base() const noexcept { return e; };

  private:
    Engine e;           // exposition only
    result_type V[k];   // exposition only
    result_type Y;      // exposition only
  };
```

The following relation shall hold: `0 < k`.

The textual representation consists of the textual representation of
`e`, followed by the `k` values of V, followed by the value of Y.

In addition to its behavior pursuant to section  [[rand.req.adapt]],
each constructor that is not a copy constructor initializes
`V[0]`, …, `V[k-1]` and Y, in that order, with values returned by
successive invocations of `e()`.

### Engines and engine adaptors with predefined parameters <a id="rand.predef">[[rand.predef]]</a>

``` cpp
using minstd_rand0 =
      linear_congruential_engine<uint_fast32_t, 16807, 0, 2147483647>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `minstd_rand0` shall produce the
value 1043618065.

``` cpp
using minstd_rand =
      linear_congruential_engine<uint_fast32_t, 48271, 0, 2147483647>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `minstd_rand` shall produce the value
399268537.

``` cpp
using mt19937 =
      mersenne_twister_engine<uint_fast32_t,
       32,624,397,31,0x9908b0df,11,0xffffffff,7,0x9d2c5680,15,0xefc60000,18,1812433253>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `mt19937` shall produce the value
4123659995.

``` cpp
using mt19937_64 =
      mersenne_twister_engine<uint_fast64_t,
       64,312,156,31,0xb5026f5aa96619e9,29,
       0x5555555555555555,17,
       0x71d67fffeda60000,37,
       0xfff7eee000000000,43,
       6364136223846793005>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `mt19937_64` shall produce the value
9981545732273789042.

``` cpp
using ranlux24_base =
      subtract_with_carry_engine<uint_fast32_t, 24, 10, 24>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `ranlux24_base` shall produce the
value 7937952.

``` cpp
using ranlux48_base =
      subtract_with_carry_engine<uint_fast64_t, 48, 5, 12>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `ranlux48_base` shall produce the
value 61839128582725.

``` cpp
using ranlux24 = discard_block_engine<ranlux24_base, 223, 23>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `ranlux24` shall produce the value
9901578.

``` cpp
using ranlux48 = discard_block_engine<ranlux48_base, 389, 11>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `ranlux48` shall produce the value
249142670248501.

``` cpp
using knuth_b = shuffle_order_engine<minstd_rand0,256>;
```

*Required behavior:* The $10000^{\,th}$ consecutive invocation of a
default-constructed object of type `knuth_b` shall produce the value
1112339016.

``` cpp
using default_random_engine = implementation-defined;
```

*Remarks:* The choice of engine type named by this `typedef` is
*implementation-defined*.

[*Note 1*: The implementation may select this type on the basis of
performance, size, quality, or any combination of such factors, so as to
provide at least acceptable engine behavior for relatively casual,
inexpert, and/or lightweight use. Because different implementations may
select different underlying engine types, code that uses this `typedef`
need not generate identical sequences across
implementations. — *end note*]

### Class `random_device` <a id="rand.device">[[rand.device]]</a>

A `random_device` uniform random bit generator produces nondeterministic
random numbers.

If implementation limitations prevent generating nondeterministic random
numbers, the implementation may employ a random number engine.

``` cpp
class random_device {
public:
  // types
  using result_type = unsigned int;

  // generator characteristics
  static constexpr result_type min() { return numeric_limits<result_type>::min(); }
  static constexpr result_type max() { return numeric_limits<result_type>::max(); }

  // constructors
  explicit random_device(const string& token = implementation-defined);

  // generating functions
  result_type operator()();

  // property functions
  double entropy() const noexcept;

  // no copy functions
  random_device(const random_device& ) = delete;
  void operator=(const random_device& ) = delete;
};
```

``` cpp
explicit random_device(const string& token = implementation-defined);
```

*Effects:* Constructs a `random_device` nondeterministic uniform random
bit generator object. The semantics and default value of the `token`
parameter are *implementation-defined*. [^3]

*Throws:* A value of an *implementation-defined* type derived from
`exception` if the `random_device` could not be initialized.

``` cpp
double entropy() const noexcept;
```

*Returns:* If the implementation employs a random number engine, returns
0.0. Otherwise, returns an entropy estimate[^4] for the random numbers
returned by `operator()`, in the range `min()` to log₂( `max()`+1).

``` cpp
result_type operator()();
```

*Returns:* A nondeterministic random value, uniformly distributed
between `min()` and `max()`, inclusive. It is *implementation-defined*
how these values are generated.

*Throws:* A value of an *implementation-defined* type derived from
`exception` if a random number could not be obtained.

### Utilities <a id="rand.util">[[rand.util]]</a>

#### Class `seed_seq` <a id="rand.util.seedseq">[[rand.util.seedseq]]</a>

``` cpp
class seed_seq {
public:
  // types
  using result_type = uint_least32_t;

  // constructors
  seed_seq();
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
  seed_seq(const seed_seq& ) = delete;
  void operator=(const seed_seq& ) = delete;

private:
  vector<result_type> v;   // exposition only
};
```

``` cpp
seed_seq();
```

*Effects:* Constructs a `seed_seq` object as if by default-constructing
its member `v`.

*Throws:* Nothing.

``` cpp
template<class T>
 seed_seq(initializer_list<T> il);
```

*Requires:* `T` shall be an integer type.

*Effects:* Same as `seed_seq(il.begin(), il.end())`.

``` cpp
template<class InputIterator>
  seed_seq(InputIterator begin, InputIterator end);
```

*Requires:* `InputIterator` shall satisfy the requirements of an input
iterator (Table  [[tab:iterator.input.requirements]]) type. Moreover,
`iterator_traits<InputIterator>::value_type` shall denote an integer
type.

*Effects:* Constructs a `seed_seq` object by the following algorithm:

``` cpp
for( InputIterator s = begin; s != end; ++s)
 v.push_back((*s) mod  2³²);
```

``` cpp
template<class RandomAccessIterator>
  void generate(RandomAccessIterator begin, RandomAccessIterator end);
```

*Requires:* `RandomAccessIterator` shall meet the requirements of a
mutable random access iterator ([[random.access.iterators]]). Moreover,
`iterator_traits<RandomAccessIterator>::value_type` shall denote an
unsigned integer type capable of accommodating 32-bit quantities.

*Effects:* Does nothing if `begin == end`. Otherwise, with
s = `v.size()` and n = `end` - `begin`, fills the supplied range
[`begin`,`end`) according to the following algorithm in which each
operation is to be carried out modulo 2³², each indexing operator
applied to `begin` is to be taken modulo n, and T(x) is defined as
$x \, \xor \, (x \, \rightshift \, 27)$:

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

*Requires:* `OutputIterator` shall satisfy the requirements of an output
iterator ([[output.iterators]]). Moreover, the expression `*dest = rt`
shall be valid for a value `rt` of type `result_type`.

*Effects:* Copies the sequence of prepared 32-bit units to the given
destination, as if by executing the following statement:

``` cpp
copy(v.begin(), v.end(), dest);
```

*Throws:* What and when `OutputIterator` operations of `dest` throw.

#### Function template `generate_canonical` <a id="rand.util.canonical">[[rand.util.canonical]]</a>

Each function instantiated from the template described in this section 
[[rand.util.canonical]] maps the result of one or more invocations of a
supplied uniform random bit generator `g` to one member of the specified
`RealType` such that, if the values gᵢ produced by `g` are uniformly
distributed, the instantiation’s results tⱼ, 0 ≤ tⱼ < 1, are distributed
as uniformly as possible as specified below.

[*Note 1*: Obtaining a value in this way can be a useful step in the
process of transforming a value generated by a uniform random bit
generator into a value that can be delivered by a random number
distribution. — *end note*]

``` cpp
template<class RealType, size_t bits, class URBG>
 RealType generate_canonical(URBG& g);
```

*Complexity:* Exactly k = max(1, ⌈ b / log₂ R ⌉) invocations of `g`,
where b[^5] is the lesser of `numeric_limits<RealType>::digits` and
`bits`, and R is the value of `g.max()` - `g.min()` + 1.

*Effects:* Invokes `g()` k times to obtain values g₀, …, gₖ₋₁,
respectively. Calculates a quantity
$$S = \sum_{i=0}^{k-1} (g_i - \texttt{g.min()})
                        \cdot R^i$$ using arithmetic of type `RealType`.

*Returns:* S / Rᵏ.

*Throws:* What and when `g` throws.

### Random number distribution class templates <a id="rand.dist">[[rand.dist]]</a>

#### In general <a id="rand.dist.general">[[rand.dist.general]]</a>

Each type instantiated from a class template specified in this section 
[[rand.dist]] satisfies the requirements of a random number
distribution ([[rand.req.dist]]) type.

Descriptions are provided in this section  [[rand.dist]] only for
distribution operations that are not described in [[rand.req.dist]] or
for operations where there is additional semantic information. In
particular, declarations for copy constructors, for copy assignment
operators, for streaming operators, and for equality and inequality
operators are not shown in the synopses.

The algorithms for producing each of the specified distributions are
*implementation-defined*.

The value of each probability density function p(z) and of each discrete
probability function P(zᵢ) specified in this section is 0 everywhere
outside its stated domain.

#### Uniform distributions <a id="rand.dist.uni">[[rand.dist.uni]]</a>

##### Class template `uniform_int_distribution` <a id="rand.dist.uni.int">[[rand.dist.uni.int]]</a>

A `uniform_int_distribution` random number distribution produces random
integers i, a ≤ i ≤ b, distributed according to the constant discrete
probability function $$%
 P(i\,|\,a,b) = 1 / (b - a + 1)
\; \mbox{.}$$

``` cpp
template<class IntType = int>
  class uniform_int_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit uniform_int_distribution(IntType a = 0, IntType b = numeric_limits<IntType>::max());
    explicit uniform_int_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit uniform_int_distribution(IntType a = 0, IntType b = numeric_limits<IntType>::max());
```

*Requires:* `a` ≤ `b`.

*Effects:* Constructs a `uniform_int_distribution` object; `a` and `b`
correspond to the respective parameters of the distribution.

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
density function $$%
 p(x\,|\,a,b) = 1 / (b - a)
\; \mbox{.}$$

[*Note 1*: This implies that p(x | a,b) is undefined when
`a == b`. — *end note*]

``` cpp
template<class RealType = double>
  class uniform_real_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit uniform_real_distribution(RealType a = 0.0, RealType b = 1.0);
    explicit uniform_real_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit uniform_real_distribution(RealType a = 0.0, RealType b = 1.0);
```

*Requires:* `a` ≤ `b` and `b` - `a` ≤ `numeric_limits<RealType>::max()`.

*Effects:* Constructs a `uniform_real_distribution` object; `a` and `b`
correspond to the respective parameters of the distribution.

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
values b distributed according to the discrete probability function $$%
 P(b\,|\,p)
      = \left\{ \begin{array}{lcl}
          p    &  \mbox{if} & b = \tcode{true} \\
          1-p  &  \mbox{if} & b = \tcode{false}
        \end{array}\right.
\; \mbox{.}$$

``` cpp
class bernoulli_distribution {
public:
  // types
  using result_type = bool;
  using param_type  = unspecified;

  // constructors and reset functions
  explicit bernoulli_distribution(double p = 0.5);
  explicit bernoulli_distribution(const param_type& parm);
  void reset();

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
};
```

``` cpp
explicit bernoulli_distribution(double p = 0.5);
```

*Requires:* 0 ≤ `p` ≤ 1.

*Effects:* Constructs a `bernoulli_distribution` object; `p` corresponds
to the parameter of the distribution.

``` cpp
double p() const;
```

*Returns:* The value of the `p` parameter with which the object was
constructed.

##### Class template `binomial_distribution` <a id="rand.dist.bern.bin">[[rand.dist.bern.bin]]</a>

A `binomial_distribution` random number distribution produces integer
values i ≥ 0 distributed according to the discrete probability function
$$%
 P(i\,|\,t,p)
      = \binom{t}{i} \cdot p^i \cdot (1-p)^{t-i}
\; \mbox{.}$$

``` cpp
template<class IntType = int>
  class binomial_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit binomial_distribution(IntType t = 1, double p = 0.5);
    explicit binomial_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit binomial_distribution(IntType t = 1, double p = 0.5);
```

*Requires:* 0 ≤ `p` ≤ 1 and 0 ≤ `t`.

*Effects:* Constructs a `binomial_distribution` object; `t` and `p`
correspond to the respective parameters of the distribution.

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
$$%
 P(i\,|\,p)
      = p \cdot (1-p)^{i}
\; \mbox{.}$$

``` cpp
template<class IntType = int>
  class geometric_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit geometric_distribution(double p = 0.5);
    explicit geometric_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit geometric_distribution(double p = 0.5);
```

*Requires:* 0 < `p` < 1.

*Effects:* Constructs a `geometric_distribution` object; `p` corresponds
to the parameter of the distribution.

``` cpp
double p() const;
```

*Returns:* The value of the `p` parameter with which the object was
constructed.

##### Class template `negative_binomial_distribution` <a id="rand.dist.bern.negbin">[[rand.dist.bern.negbin]]</a>

A `negative_binomial_distribution` random number distribution produces
random integers i ≥ 0 distributed according to the discrete probability
function $$%
 P(i\,|\,k,p)
      = \binom{k+i-1}{i} \cdot p^k \cdot (1-p)^i
\; \mbox{.}$$

[*Note 1*: This implies that P(i | k,p) is undefined when
`p == 1`. — *end note*]

``` cpp
template<class IntType = int>
  class negative_binomial_distribution {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit negative_binomial_distribution(IntType k = 1, double p = 0.5);
    explicit negative_binomial_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit negative_binomial_distribution(IntType k = 1, double p = 0.5);
```

*Requires:* 0 < `p` ≤ 1 and 0 < `k`.

*Effects:* Constructs a `negative_binomial_distribution` object; `k` and
`p` correspond to the respective parameters of the distribution.

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
$$%
 P(i\,|\,\mu)
      = \frac{ e^{-\mu} \mu^{i} }
             { i\,! }
\; \mbox{.}$$ The distribution parameter μ is also known as this
distribution’s .

``` cpp
template<class IntType = int>
  class poisson_distribution
  {
  public:
    // types
    using result_type = IntType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit poisson_distribution(double mean = 1.0);
    explicit poisson_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit poisson_distribution(double mean = 1.0);
```

*Requires:* 0 < `mean`.

*Effects:* Constructs a `poisson_distribution` object; `mean`
corresponds to the parameter of the distribution.

``` cpp
double mean() const;
```

*Returns:* The value of the `mean` parameter with which the object was
constructed.

##### Class template `exponential_distribution` <a id="rand.dist.pois.exp">[[rand.dist.pois.exp]]</a>

An `exponential_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
$$%
 p(x\,|\,\lambda)
      = \lambda e^{-\lambda x}
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class exponential_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit exponential_distribution(RealType lambda = 1.0);
    explicit exponential_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit exponential_distribution(RealType lambda = 1.0);
```

*Requires:* 0 < `lambda`.

*Effects:* Constructs an `exponential_distribution` object; `lambda`
corresponds to the parameter of the distribution.

``` cpp
RealType lambda() const;
```

*Returns:* The value of the `lambda` parameter with which the object was
constructed.

##### Class template `gamma_distribution` <a id="rand.dist.pois.gamma">[[rand.dist.pois.gamma]]</a>

A `gamma_distribution` random number distribution produces random
numbers x > 0 distributed according to the probability density function
$$%
 p(x\,|\,\alpha,\beta)
      = \frac{e^{-x/\beta}}{\beta^{\alpha} \cdot \Gamma(\alpha)}
        \, \cdot \, x^{\, \alpha-1}
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class gamma_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit gamma_distribution(RealType alpha = 1.0, RealType beta = 1.0);
    explicit gamma_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit gamma_distribution(RealType alpha = 1.0, RealType beta = 1.0);
```

*Requires:* 0 < `alpha` and 0 < `beta`.

*Effects:* Constructs a `gamma_distribution` object; `alpha` and `beta`
correspond to the parameters of the distribution.

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
$$%
 p(x\,|\,a,b)
      =       \frac{a}{b}
        \cdot \left(\frac{x}{b}\right)^{a-1}
        \cdot \, \exp\left( -\left(\frac{x}{b}\right)^a\right)
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class weibull_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit weibull_distribution(RealType a = 1.0, RealType b = 1.0);
    explicit weibull_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit weibull_distribution(RealType a = 1.0, RealType b = 1.0);
```

*Requires:* 0 < `a` and 0 < `b`.

*Effects:* Constructs a `weibull_distribution` object; `a` and `b`
correspond to the respective parameters of the distribution.

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
function[^6] $$%
 p(x\,|\,a,b)
      =       \frac{1}{b}
        \cdot \exp\left(  \frac{a-x}{b}
                       \,-\, \exp\left(\frac{a-x}{b}\right)
                  \right)
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class extreme_value_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit extreme_value_distribution(RealType a = 0.0, RealType b = 1.0);
    explicit extreme_value_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit extreme_value_distribution(RealType a = 0.0, RealType b = 1.0);
```

*Requires:* 0 < `b`.

*Effects:* Constructs an `extreme_value_distribution` object; `a` and
`b` correspond to the respective parameters of the distribution.

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
numbers x distributed according to the probability density function $$%
 p(x\,|\,\mu,\sigma)
      = \frac{1}{\sigma \sqrt{2\pi}}
        \cdot
        % e^{-(x-\mu)^2 / (2\sigma^2)}
        \exp{\left(- \, \frac{(x - \mu)^2}
                             {2 \sigma^2}
             \right)
            }
\; \mbox{.}$$ The distribution parameters μ and σ are also known as this
distribution’s and .

``` cpp
template<class RealType = double>
  class normal_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructors and reset functions
    explicit normal_distribution(RealType mean = 0.0, RealType stddev = 1.0);
    explicit normal_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit normal_distribution(RealType mean = 0.0, RealType stddev = 1.0);
```

*Requires:* 0 < `stddev`.

*Effects:* Constructs a `normal_distribution` object; `mean` and
`stddev` correspond to the respective parameters of the distribution.

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
$$%
 p(x\,|\,m,s)
      = \frac{1}
             {s x \sqrt{2 \pi}}
        \cdot
        \exp{\left(- \, \frac{(\ln{x} - m)^2}
                             {2 s^2}
             \right)
            }
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class lognormal_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit lognormal_distribution(RealType m = 0.0, RealType s = 1.0);
    explicit lognormal_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit lognormal_distribution(RealType m = 0.0, RealType s = 1.0);
```

*Requires:* 0 < `s`.

*Effects:* Constructs a `lognormal_distribution` object; `m` and `s`
correspond to the respective parameters of the distribution.

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
numbers x>0 distributed according to the probability density function
$$%
 p(x\,|\,n)
      =  \frac{ x^{(n/2)-1} \cdot e^{-x/2}}
              {\Gamma(n/2) \cdot 2^{n/2}}
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class chi_squared_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit chi_squared_distribution(RealType n = 1);
    explicit chi_squared_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit chi_squared_distribution(RealType n = 1);
```

*Requires:* 0 < `n`.

*Effects:* Constructs a `chi_squared_distribution` object; `n`
corresponds to the parameter of the distribution.

``` cpp
RealType n() const;
```

*Returns:* The value of the `n` parameter with which the object was
constructed.

##### Class template `cauchy_distribution` <a id="rand.dist.norm.cauchy">[[rand.dist.norm.cauchy]]</a>

A `cauchy_distribution` random number distribution produces random
numbers x distributed according to the probability density function $$%
 p(x\,|\,a,b)
      = \left( \pi b \left( 1 + \left( \frac{x-a}{b}  \right)^2 \;\right)\right)^{-1}
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class cauchy_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit cauchy_distribution(RealType a = 0.0, RealType b = 1.0);
    explicit cauchy_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit cauchy_distribution(RealType a = 0.0, RealType b = 1.0);
```

*Requires:* 0 < `b`.

*Effects:* Constructs a `cauchy_distribution` object; `a` and `b`
correspond to the respective parameters of the distribution.

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
numbers x≥0 distributed according to the probability density function
$$%
 p(x\,|\,m,n)
      = \frac{\Gamma\big((m+n)/2\big)}
             {\Gamma(m/2) \; \Gamma(n/2)}
        \cdot
        \left(\frac{m}{n}\right)^{m/2}
        \cdot
        x^{(m/2)-1}
        \cdot
        {\left( 1 + \frac{m x}{n}  \right)}^{-(m+n)/2}
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class fisher_f_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit fisher_f_distribution(RealType m = 1, RealType n = 1);
    explicit fisher_f_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit fisher_f_distribution(RealType m = 1, RealType n = 1);
```

*Requires:* 0 < `m` and 0 < `n`.

*Effects:* Constructs a `fisher_f_distribution` object; `m` and `n`
correspond to the respective parameters of the distribution.

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
numbers x distributed according to the probability density function $$%
 p(x\,|\,n)
      =  \frac{1}
              {\sqrt{n \pi}}
         \cdot \frac{\Gamma\big((n+1)/2\big)}
                    {\Gamma(n/2)}
         \cdot \left( 1+\frac{x^2}{n} \right) ^ {-(n+1)/2}
\; \mbox{.}$$

``` cpp
template<class RealType = double>
  class student_t_distribution {
  public:
    // types
    using result_type = RealType;
    using param_type  = unspecified;

    // constructor and reset functions
    explicit student_t_distribution(RealType n = 1);
    explicit student_t_distribution(const param_type& parm);
    void reset();

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
  };
```

``` cpp
explicit student_t_distribution(RealType n = 1);
```

*Requires:* 0 < `n`.

*Effects:* Constructs a `student_t_distribution` object; `n` corresponds
to the parameter of the distribution.

``` cpp
RealType n() const;
```

*Returns:* The value of the `n` parameter with which the object was
constructed.

#### Sampling distributions <a id="rand.dist.samp">[[rand.dist.samp]]</a>

##### Class template `discrete_distribution` <a id="rand.dist.samp.discrete">[[rand.dist.samp.discrete]]</a>

A `discrete_distribution` random number distribution produces random
integers i, 0 ≤ i < n, distributed according to the discrete probability
function $$%
 P(i\,|\,p_0,\ldots,p_{n-1})
      = p_i
\; \mbox{.}$$

Unless specified otherwise, the distribution parameters are calculated
as: $p_k = {w_k / S} \; \mbox{  for } k = 0, \ldots, n\!-\!1$ , in which
the values wₖ, commonly known as the , shall be non-negative, non-NaN,
and non-infinity. Moreover, the following relation shall hold:
0 < S = w₀ + ⋯ + wₙ₋₁.

``` cpp
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
  };
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

*Requires:* `InputIterator` shall satisfy the requirements of an input
iterator ([[input.iterators]]). Moreover,
`iterator_traits<InputIterator>::value_type` shall denote a type that is
convertible to `double`. If `firstW == lastW`, let n = 1 and w₀ = 1.
Otherwise, [`firstW`, `lastW`) shall form a sequence w of length n > 0.

*Effects:* Constructs a `discrete_distribution` object with
probabilities given by the formula above.

``` cpp
discrete_distribution(initializer_list<double> wl);
```

*Effects:* Same as `discrete_distribution(wl.begin(), wl.end())`.

``` cpp
template<class UnaryOperation>
  discrete_distribution(size_t nw, double xmin, double xmax, UnaryOperation fw);
```

*Requires:* Each instance of type `UnaryOperation` shall be a function
object ([[function.objects]]) whose return type shall be convertible to
`double`. Moreover, `double` shall be convertible to the type of
`UnaryOperation`’s sole parameter. If `nw` = 0, let n = 1, otherwise let
n = `nw`. The relation 0 < δ = (`xmax` - `xmin`) / n shall hold.

*Effects:* Constructs a `discrete_distribution` object with
probabilities given by the formula above, using the following values: If
`nw` = 0, let w₀ = 1. Otherwise, let wₖ = `fw`(`xmin` + k ⋅ δ + δ / 2)
for k = 0, …, n-1.

*Complexity:* The number of invocations of `fw` shall not exceed n.

``` cpp
vector<double> probabilities() const;
```

*Returns:* A `vector<double>` whose `size` member returns n and whose
`operator[]` member returns pₖ when invoked with argument k for
k = 0, …, n-1.

##### Class template `piecewise_constant_distribution` <a id="rand.dist.samp.pconst">[[rand.dist.samp.pconst]]</a>

A `piecewise_constant_distribution` random number distribution produces
random numbers x, b₀ ≤ x < bₙ, uniformly distributed over each
subinterval [ bᵢ, bᵢ₊₁ ) according to the probability density function
$$%
 p(x\,|\,b_0,\ldots,b_n,\;\rho_0,\ldots,\rho_{n-1})
      = \rho_i
\; \mbox{,}
\mbox{ for } b_i \le x < b_{i+1}
\; \mbox{.}$$

The n+1 distribution parameters bᵢ, also known as this distribution’s ,
shall satisfy the relation bᵢ < bᵢ₊₁ for i = 0, …, n-1. Unless specified
otherwise, the remaining n distribution parameters are calculated as:
$$%
 \rho_k = \;
   \frac{w_k}{S \cdot (b_{k+1}-b_k)}
   \; \mbox{ for } k = 0, \ldots, n\!-\!1,$$ in which the values wₖ,
commonly known as the , shall be non-negative, non-NaN, and
non-infinity. Moreover, the following relation shall hold:
0 < S = w₀ + ⋯ + wₙ₋₁.

``` cpp
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
  };
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

*Requires:* `InputIteratorB` and `InputIteratorW` shall each satisfy the
requirements of an input iterator
(Table  [[tab:iterator.input.requirements]]) type. Moreover,
`iterator_traits<InputIteratorB>::value_type` and
`iterator_traits<InputIteratorW>::value_type` shall each denote a type
that is convertible to `double`. If `firstB == lastB` or
`++firstB == lastB`, let n = 1, w₀ = 1, b₀ = 0, and b₁ = 1. Otherwise,
[`firstB`, `lastB`) shall form a sequence b of length n+1, the length of
the sequence w starting from `firstW` shall be at least n, and any wₖ
for k ≥ n shall be ignored by the distribution.

*Effects:* Constructs a `piecewise_constant_distribution` object with
parameters as specified above.

``` cpp
template<class UnaryOperation>
 piecewise_constant_distribution(initializer_list<RealType> bl, UnaryOperation fw);
```

*Requires:* Each instance of type `UnaryOperation` shall be a function
object ([[function.objects]]) whose return type shall be convertible to
`double`. Moreover, `double` shall be convertible to the type of
`UnaryOperation`’s sole parameter.

*Effects:* Constructs a `piecewise_constant_distribution` object with
parameters taken or calculated from the following values: If
`bl.size()` < 2, let n = 1, w₀ = 1, b₀ = 0, and b₁ = 1. Otherwise, let
[`bl.begin()`, `bl.end()`) form a sequence b₀, …, bₙ, and let
wₖ = `fw`((bₖ₊₁ + bₖ) / 2) for k = 0, …, n-1.

*Complexity:* The number of invocations of `fw` shall not exceed n.

``` cpp
template<class UnaryOperation>
 piecewise_constant_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
```

*Requires:* Each instance of type `UnaryOperation` shall be a function
object ([[function.objects]]) whose return type shall be convertible to
`double`. Moreover, `double` shall be convertible to the type of
`UnaryOperation`’s sole parameter. If `nw` = 0, let n = 1, otherwise let
n = `nw`. The relation 0 < δ = (`xmax` - `xmin`) / n shall hold.

*Effects:* Constructs a `piecewise_constant_distribution` object with
parameters taken or calculated from the following values: Let
bₖ = `xmin` + k ⋅ δ for k = 0, …, n, and wₖ = `fw`(bₖ + δ / 2) for
k = 0, …, n-1.

*Complexity:* The number of invocations of `fw` shall not exceed n.

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
k = 0, …, n-1.

##### Class template `piecewise_linear_distribution` <a id="rand.dist.samp.plinear">[[rand.dist.samp.plinear]]</a>

A `piecewise_linear_distribution` random number distribution produces
random numbers x, b₀ ≤ x < bₙ, distributed over each subinterval
[ bᵢ, bᵢ₊₁ ) according to the probability density function $$%
 p(x\,|\,b_0,\ldots,b_n,\;\rho_0,\ldots,\rho_n)
      = \rho_i     \cdot {\frac{b_{i+1} - x}{b_{i+1} - b_i}}
      + \rho_{i+1} \cdot {\frac{x - b_i}{b_{i+1} - b_i}}
\; \mbox{,}
\mbox{ for } b_i \le x < b_{i+1}
\; \mbox{.}$$

The n+1 distribution parameters bᵢ, also known as this distribution’s ,
shall satisfy the relation bᵢ < bᵢ₊₁ for i = 0, …, n-1. Unless specified
otherwise, the remaining n+1 distribution parameters are calculated as
$\rho_k = {w_k / S} \; \mbox{ for } k = 0, \ldots, n$, in which the
values wₖ, commonly known as the , shall be non-negative, non-NaN, and
non-infinity. Moreover, the following relation shall hold: $$%
 0 < S = \frac{1}{2}
       \cdot \sum_{k=0}^{n-1} (w_k + w_{k+1}) \cdot (b_{k+1} - b_k)
\; \mbox{.}$$

``` cpp
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
  };
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

*Requires:* `InputIteratorB` and `InputIteratorW` shall each satisfy the
requirements of an input iterator
(Table  [[tab:iterator.input.requirements]]) type. Moreover,
`iterator_traits<InputIteratorB>::value_type` and
`iterator_traits<InputIteratorW>::value_type` shall each denote a type
that is convertible to `double`. If `firstB == lastB` or
`++firstB == lastB`, let n = 1, ρ₀ = ρ₁ = 1, b₀ = 0, and b₁ = 1.
Otherwise, [`firstB`, `lastB`) shall form a sequence b of length n+1,
the length of the sequence w starting from `firstW` shall be at least
n+1, and any wₖ for k ≥ n+1 shall be ignored by the distribution.

*Effects:* Constructs a `piecewise_linear_distribution` object with
parameters as specified above.

``` cpp
template<class UnaryOperation>
 piecewise_linear_distribution(initializer_list<RealType> bl, UnaryOperation fw);
```

*Requires:* Each instance of type `UnaryOperation` shall be a function
object ([[function.objects]]) whose return type shall be convertible to
`double`. Moreover, `double` shall be convertible to the type of
`UnaryOperation`’s sole parameter.

*Effects:* Constructs a `piecewise_linear_distribution` object with
parameters taken or calculated from the following values: If
`bl.size()` < 2, let n = 1, ρ₀ = ρ₁ = 1, b₀ = 0, and b₁ = 1. Otherwise,
let [`bl.begin(),` `bl.end()`) form a sequence b₀, …, bₙ, and let
wₖ = `fw`(bₖ) for k = 0, …, n.

*Complexity:* The number of invocations of `fw` shall not exceed n+1.

``` cpp
template<class UnaryOperation>
 piecewise_linear_distribution(size_t nw, RealType xmin, RealType xmax, UnaryOperation fw);
```

*Requires:* Each instance of type `UnaryOperation` shall be a function
object ([[function.objects]]) whose return type shall be convertible to
`double`. Moreover, `double` shall be convertible to the type of
`UnaryOperation`’s sole parameter. If `nw` = 0, let n = 1, otherwise let
n = `nw`. The relation 0 < δ = (`xmax` - `xmin`) / n shall hold.

*Effects:* Constructs a `piecewise_linear_distribution` object with
parameters taken or calculated from the following values: Let
bₖ = `xmin` + k ⋅ δ for k = 0, …, n, and wₖ = `fw`(bₖ) for k = 0, …, n.

*Complexity:* The number of invocations of `fw` shall not exceed n+1.

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

[*Note 1*: The header `<cstdlib>` ([[cstdlib.syn]]) declares the
functions described in this subclause. — *end note*]

``` cpp
int rand();
void srand(unsigned int seed);
```

*Effects:* The `rand` and `srand` functions have the semantics specified
in the C standard library.

*Remarks:* The implementation may specify that particular library
functions may call `rand`. It is *implementation-defined* whether the
`rand` function may introduce data races ([[res.on.data.races]]).

[*Note 1*: The other random number generation facilities in this
International Standard ([[rand]]) are often preferable to `rand`,
because `rand`’s underlying algorithm is unspecified. Use of `rand`
therefore continues to be non-portable, with unpredictable and
oft-questionable quality and performance. — *end note*]

ISO C 7.22.2

## Numeric arrays <a id="numarray">[[numarray]]</a>

### Header `<valarray>` synopsis <a id="valarray.syn">[[valarray.syn]]</a>

``` cpp
#include <initializer_list>

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
  template<class T> valarray<T> operator* (const valarray<T>&, const T&);
  template<class T> valarray<T> operator* (const T&, const valarray<T>&);

  template<class T> valarray<T> operator/ (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator/ (const valarray<T>&, const T&);
  template<class T> valarray<T> operator/ (const T&, const valarray<T>&);

  template<class T> valarray<T> operator% (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator% (const valarray<T>&, const T&);
  template<class T> valarray<T> operator% (const T&, const valarray<T>&);

  template<class T> valarray<T> operator+ (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator+ (const valarray<T>&, const T&);
  template<class T> valarray<T> operator+ (const T&, const valarray<T>&);

  template<class T> valarray<T> operator- (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator- (const valarray<T>&, const T&);
  template<class T> valarray<T> operator- (const T&, const valarray<T>&);

  template<class T> valarray<T> operator^ (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator^ (const valarray<T>&, const T&);
  template<class T> valarray<T> operator^ (const T&, const valarray<T>&);

  template<class T> valarray<T> operator& (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator& (const valarray<T>&, const T&);
  template<class T> valarray<T> operator& (const T&, const valarray<T>&);

  template<class T> valarray<T> operator| (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator| (const valarray<T>&, const T&);
  template<class T> valarray<T> operator| (const T&, const valarray<T>&);

  template<class T> valarray<T> operator<<(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator<<(const valarray<T>&, const T&);
  template<class T> valarray<T> operator<<(const T&, const valarray<T>&);

  template<class T> valarray<T> operator>>(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> operator>>(const valarray<T>&, const T&);
  template<class T> valarray<T> operator>>(const T&, const valarray<T>&);

  template<class T> valarray<bool> operator&&(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator&&(const valarray<T>&, const T&);
  template<class T> valarray<bool> operator&&(const T&, const valarray<T>&);

  template<class T> valarray<bool> operator||(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator||(const valarray<T>&, const T&);
  template<class T> valarray<bool> operator||(const T&, const valarray<T>&);

  template<class T>
    valarray<bool> operator==(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator==(const valarray<T>&, const T&);
  template<class T> valarray<bool> operator==(const T&, const valarray<T>&);
  template<class T>
    valarray<bool> operator!=(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator!=(const valarray<T>&, const T&);
  template<class T> valarray<bool> operator!=(const T&, const valarray<T>&);

  template<class T>
    valarray<bool> operator< (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator< (const valarray<T>&, const T&);
  template<class T> valarray<bool> operator< (const T&, const valarray<T>&);
  template<class T>
    valarray<bool> operator> (const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator> (const valarray<T>&, const T&);
  template<class T> valarray<bool> operator> (const T&, const valarray<T>&);
  template<class T>
    valarray<bool> operator<=(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator<=(const valarray<T>&, const T&);
  template<class T> valarray<bool> operator<=(const T&, const valarray<T>&);
  template<class T>
    valarray<bool> operator>=(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<bool> operator>=(const valarray<T>&, const T&);
  template<class T> valarray<bool> operator>=(const T&, const valarray<T>&);

  template<class T> valarray<T> abs  (const valarray<T>&);
  template<class T> valarray<T> acos (const valarray<T>&);
  template<class T> valarray<T> asin (const valarray<T>&);
  template<class T> valarray<T> atan (const valarray<T>&);

  template<class T> valarray<T> atan2(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> atan2(const valarray<T>&, const T&);
  template<class T> valarray<T> atan2(const T&, const valarray<T>&);

  template<class T> valarray<T> cos  (const valarray<T>&);
  template<class T> valarray<T> cosh (const valarray<T>&);
  template<class T> valarray<T> exp  (const valarray<T>&);
  template<class T> valarray<T> log  (const valarray<T>&);
  template<class T> valarray<T> log10(const valarray<T>&);

  template<class T> valarray<T> pow(const valarray<T>&, const valarray<T>&);
  template<class T> valarray<T> pow(const valarray<T>&, const T&);
  template<class T> valarray<T> pow(const T&, const valarray<T>&);

  template<class T> valarray<T> sin  (const valarray<T>&);
  template<class T> valarray<T> sinh (const valarray<T>&);
  template<class T> valarray<T> sqrt (const valarray<T>&);
  template<class T> valarray<T> tan  (const valarray<T>&);
  template<class T> valarray<T> tanh (const valarray<T>&);

  template <class T> unspecified{1} begin(valarray<T>& v);
  template <class T> unspecified{2} begin(const valarray<T>& v);
  template <class T> unspecified{1} end(valarray<T>& v);
  template <class T> unspecified{2} end(const valarray<T>& v);
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
nested argument type.[^7]

Implementations introducing such replacement types shall provide
additional functions and operators as follows:

- for every function taking a `const valarray<T>&` other than `begin`
  and `end` ([[valarray.range]]), identical functions taking the
  replacement types shall be added;
- for every function taking two `const valarray<T>&` arguments,
  identical functions taking every combination of `const valarray<T>&`
  and replacement types shall be added.

In particular, an implementation shall allow a `valarray<T>` to be
constructed from such replacement types and shall allow assignments and
compound assignments of such types to `valarray<T>`, `slice_array<T>`,
`gslice_array<T>`, `mask_array<T>` and `indirect_array<T>` objects.

These library functions are permitted to throw a `bad_alloc` (
[[bad.alloc]]) exception if there are not sufficient resources available
to carry out the operation. Note that the exception is not mandated.

### Class template `valarray` <a id="template.valarray">[[template.valarray]]</a>

#### Class template `valarray` overview <a id="template.valarray.overview">[[template.valarray.overview]]</a>

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
operators.[^8]

An implementation is permitted to qualify any of the functions declared
in `<valarray>` as `inline`.

#### `valarray` constructors <a id="valarray.cons">[[valarray.cons]]</a>

``` cpp
valarray();
```

*Effects:* Constructs a `valarray` that has zero length.[^9]

``` cpp
explicit valarray(size_t n);
```

*Effects:* Constructs a `valarray` that has length `n`. Each element of
the array is value-initialized ([[dcl.init]]).

``` cpp
valarray(const T& v, size_t n);
```

*Effects:* Constructs a `valarray` that has length `n`. Each element of
the array is initialized with `v`.

``` cpp
valarray(const T* p, size_t n);
```

*Requires:* `p` points to an array ([[dcl.array]]) of at least `n`
elements.

*Effects:* Constructs a `valarray` that has length `n`. The values of
the elements of the array are initialized with the first `n` values
pointed to by the first argument.[^10]

``` cpp
valarray(const valarray& v);
```

*Effects:* Constructs a `valarray` that has the same length as `v`. The
elements are initialized with the values of the corresponding elements
of `v`.[^11]

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

#### `valarray` assignment <a id="valarray.assign">[[valarray.assign]]</a>

``` cpp
valarray& operator=(const valarray& v);
```

*Effects:* Each element of the `*this` array is assigned the value of
the corresponding element of `v`. If the length of `v` is not equal to
the length of `*this`, resizes `*this` to make the two arrays the same
length, as if by calling `resize(v.size())`, before performing the
assignment.

*Postconditions:* `size() == v.size()`.

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

*Requires:* The length of the array to which the argument refers equals
`size()`. The value of an element in the left-hand side of a `valarray`
assignment operator does not depend on the value of another element in
that left-hand side.

These operators allow the results of a generalized subscripting
operation to be assigned directly to a `valarray`.

#### `valarray` element access <a id="valarray.access">[[valarray.access]]</a>

``` cpp
const T&  operator[](size_t n) const;
T& operator[](size_t n);
```

*Requires:* `n < size()`.

*Returns:* A reference to the corresponding element of the array.

[*Note 1*: The expression `(a[i] = q, a[i]) == q` evaluates to `true`
for any non-constant `valarray<T> a`, any `T q`, and for any `size_t i`
such that the value of `i` is less than the length of
`a`. — *end note*]

*Remarks:* The expression `&a[i+j] == &a[i] + j` evaluates to `true` for
all `size_t i` and `size_t j` such that `i+j < a.size()`.

The expression `&a[i] != &b[j]` evaluates to `true` for any two arrays
`a` and `b` and for any `size_t i` and `size_t j` such that
`i < a.size()` and `j < b.size()`.

[*Note 2*: This property indicates an absence of aliasing and may be
used to advantage by optimizing compilers. Compilers may take advantage
of inlining, constant propagation, loop fusion, tracking of pointers
obtained from `operator new`, and other techniques to generate efficient
`valarray`s. — *end note*]

The reference returned by the subscript operator for an array shall be
valid until the member function
`resize(size_t, T)` ([[valarray.members]]) is called for that array or
until the lifetime of that array ends, whichever happens first.

#### `valarray` subset operations <a id="valarray.sub">[[valarray.sub]]</a>

The member `operator[]` is overloaded to provide several ways to select
sequences of elements from among those controlled by `*this`. Each of
these operations returns a subset of the array. The const-qualified
versions return this subset as a new `valarray` object. The non-const
versions return a class template object which has reference semantics to
the original array, working in conjunction with various overloads of
`operator=` and other assigning operators to allow selective replacement
(slicing) of the controlled sequence. In each case the selected
element(s) must exist.

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

#### `valarray` unary operators <a id="valarray.unary">[[valarray.unary]]</a>

\indexlibrarymember{operator~}{valarray}

``` cpp
valarray operator+() const;
valarray operator-() const;
valarray operator~() const;
valarray<bool> operator!() const;
```

*Requires:* Each of these operators may only be instantiated for a type
`T` to which the indicated operator can be applied and for which the
indicated operator returns a value which is of type `T` (`bool` for
`operator!`) or which may be unambiguously implicitly converted to type
`T` (`bool` for `operator!`).

*Returns:* A `valarray` whose length is `size()`. Each element of the
returned array is initialized with the result of applying the indicated
operator to the corresponding element of the array.

#### `valarray` compound assignment <a id="valarray.cassign">[[valarray.cassign]]</a>

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

*Requires:* `size() == v.size()`. Each of these operators may only be
instantiated for a type `T` if the indicated operator can be applied to
two operands of type `T`. The value of an element in the left-hand side
of a valarray compound assignment operator does not depend on the value
of another element in that left hand side.

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

*Requires:* Each of these operators may only be instantiated for a type
`T` if the indicated operator can be applied to two operands of type
`T`.

*Effects:* Each of these operators applies the indicated operation to
each element of `*this` and `v`.

*Returns:* `*this`

*Remarks:* The appearance of an array on the left-hand side of a
compound assignment does not invalidate references or pointers to the
elements of the array.

#### `valarray` member functions <a id="valarray.members">[[valarray.members]]</a>

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

*Requires:* `size() > 0`. This function may only be instantiated for a
type `T` to which `operator+=` can be applied.

*Returns:* The sum of all the elements of the array. If the array has
length 1, returns the value of element 0. Otherwise, the returned value
is calculated by applying `operator+=` to a copy of an element of the
array and all other elements of the array in an unspecified order.

``` cpp
T min() const;
```

*Requires:* `size() > 0`

*Returns:* The minimum value contained in `*this`. For an array of
length 1, the value of element 0 is returned. For all other array
lengths, the determination is made using `operator<`.

``` cpp
T max() const;
```

*Requires:* `size() > 0`.

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
of the result will be value-initialized ([[dcl.init]]); the third
element of the result will be assigned the value of the first element of
the argument; etc. — *end example*]

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

#### `valarray` binary operators <a id="valarray.binary">[[valarray.binary]]</a>

\indexlibrarymember{operator^}{valarray}

``` cpp
template<class T> valarray<T> operator*
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator/
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator%
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator+
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator-
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator^
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator&
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator|
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator<<
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> operator>>
    (const valarray<T>&, const valarray<T>&);
```

*Requires:* Each of these operators may only be instantiated for a type
`T` to which the indicated operator can be applied and for which the
indicated operator returns a value which is of type `T` or which can be
unambiguously implicitly converted to type `T`. The argument arrays have
the same length.

*Returns:* A `valarray` whose length is equal to the lengths of the
argument arrays. Each element of the returned array is initialized with
the result of applying the indicated operator to the corresponding
elements of the argument arrays.

\indexlibrarymember{operator^}{valarray}

``` cpp
template<class T> valarray<T> operator* (const valarray<T>&, const T&);
template<class T> valarray<T> operator* (const T&, const valarray<T>&);
template<class T> valarray<T> operator/ (const valarray<T>&, const T&);
template<class T> valarray<T> operator/ (const T&, const valarray<T>&);
template<class T> valarray<T> operator% (const valarray<T>&, const T&);
template<class T> valarray<T> operator% (const T&, const valarray<T>&);
template<class T> valarray<T> operator+ (const valarray<T>&, const T&);
template<class T> valarray<T> operator+ (const T&, const valarray<T>&);
template<class T> valarray<T> operator- (const valarray<T>&, const T&);
template<class T> valarray<T> operator- (const T&, const valarray<T>&);
template<class T> valarray<T> operator^ (const valarray<T>&, const T&);
template<class T> valarray<T> operator^ (const T&, const valarray<T>&);
template<class T> valarray<T> operator& (const valarray<T>&, const T&);
template<class T> valarray<T> operator& (const T&, const valarray<T>&);
template<class T> valarray<T> operator| (const valarray<T>&, const T&);
template<class T> valarray<T> operator| (const T&, const valarray<T>&);
template<class T> valarray<T> operator<<(const valarray<T>&, const T&);
template<class T> valarray<T> operator<<(const T&, const valarray<T>&);
template<class T> valarray<T> operator>>(const valarray<T>&, const T&);
template<class T> valarray<T> operator>>(const T&, const valarray<T>&);
```

*Requires:* Each of these operators may only be instantiated for a type
`T` to which the indicated operator can be applied and for which the
indicated operator returns a value which is of type `T` or which can be
unambiguously implicitly converted to type `T`.

*Returns:* A `valarray` whose length is equal to the length of the array
argument. Each element of the returned array is initialized with the
result of applying the indicated operator to the corresponding element
of the array argument and the non-array argument.

#### `valarray` logical operators <a id="valarray.comparison">[[valarray.comparison]]</a>

``` cpp
template<class T> valarray<bool> operator==
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator!=
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator<
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator>
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator<=
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator>=
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator&&
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<bool> operator||
    (const valarray<T>&, const valarray<T>&);
```

*Requires:* Each of these operators may only be instantiated for a type
`T` to which the indicated operator can be applied and for which the
indicated operator returns a value which is of type `bool` or which can
be unambiguously implicitly converted to type `bool`. The two array
arguments have the same length.

*Returns:* A `valarray<bool>` whose length is equal to the length of the
array arguments. Each element of the returned array is initialized with
the result of applying the indicated operator to the corresponding
elements of the argument arrays.

``` cpp
template<class T> valarray<bool> operator==(const valarray<T>&, const T&);
template<class T> valarray<bool> operator==(const T&, const valarray<T>&);
template<class T> valarray<bool> operator!=(const valarray<T>&, const T&);
template<class T> valarray<bool> operator!=(const T&, const valarray<T>&);
template<class T> valarray<bool> operator< (const valarray<T>&, const T&);
template<class T> valarray<bool> operator< (const T&, const valarray<T>&);
template<class T> valarray<bool> operator> (const valarray<T>&, const T&);
template<class T> valarray<bool> operator> (const T&, const valarray<T>&);
template<class T> valarray<bool> operator<=(const valarray<T>&, const T&);
template<class T> valarray<bool> operator<=(const T&, const valarray<T>&);
template<class T> valarray<bool> operator>=(const valarray<T>&, const T&);
template<class T> valarray<bool> operator>=(const T&, const valarray<T>&);
template<class T> valarray<bool> operator&&(const valarray<T>&, const T&);
template<class T> valarray<bool> operator&&(const T&, const valarray<T>&);
template<class T> valarray<bool> operator||(const valarray<T>&, const T&);
template<class T> valarray<bool> operator||(const T&, const valarray<T>&);
```

*Requires:* Each of these operators may only be instantiated for a type
`T` to which the indicated operator can be applied and for which the
indicated operator returns a value which is of type `bool` or which can
be unambiguously implicitly converted to type `bool`.

*Returns:* A `valarray<bool>` whose length is equal to the length of the
array argument. Each element of the returned array is initialized with
the result of applying the indicated operator to the corresponding
element of the array and the non-array argument.

#### `valarray` transcendentals <a id="valarray.transcend">[[valarray.transcend]]</a>

``` cpp
template<class T> valarray<T> abs  (const valarray<T>&);
template<class T> valarray<T> acos (const valarray<T>&);
template<class T> valarray<T> asin (const valarray<T>&);
template<class T> valarray<T> atan (const valarray<T>&);
template<class T> valarray<T> atan2
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> atan2(const valarray<T>&, const T&);
template<class T> valarray<T> atan2(const T&, const valarray<T>&);
template<class T> valarray<T> cos  (const valarray<T>&);
template<class T> valarray<T> cosh (const valarray<T>&);
template<class T> valarray<T> exp  (const valarray<T>&);
template<class T> valarray<T> log  (const valarray<T>&);
template<class T> valarray<T> log10(const valarray<T>&);
template<class T> valarray<T> pow
    (const valarray<T>&, const valarray<T>&);
template<class T> valarray<T> pow  (const valarray<T>&, const T&);
template<class T> valarray<T> pow  (const T&, const valarray<T>&);
template<class T> valarray<T> sin  (const valarray<T>&);
template<class T> valarray<T> sinh (const valarray<T>&);
template<class T> valarray<T> sqrt (const valarray<T>&);
template<class T> valarray<T> tan  (const valarray<T>&);
template<class T> valarray<T> tanh (const valarray<T>&);
```

*Requires:* Each of these functions may only be instantiated for a type
`T` to which a unique function with the indicated name can be applied
(unqualified). This function shall return a value which is of type `T`
or which can be unambiguously implicitly converted to type `T`.

#### `valarray` specialized algorithms <a id="valarray.special">[[valarray.special]]</a>

``` cpp
template <class T> void swap(valarray<T>& x, valarray<T>& y) noexcept;
```

*Effects:* Equivalent to `x.swap(y)`.

### Class `slice` <a id="class.slice">[[class.slice]]</a>

#### Class `slice` overview <a id="class.slice.overview">[[class.slice.overview]]</a>

``` cpp
namespace std {
  class slice {
  public:
    slice();
    slice(size_t, size_t, size_t);

    size_t start() const;
    size_t size() const;
    size_t stride() const;
  };
}
```

The `slice` class represents a BLAS-like slice from an array. Such a
slice is specified by a starting index, a length, and a stride.[^12]

#### `slice` constructors <a id="cons.slice">[[cons.slice]]</a>

``` cpp
slice();
slice(size_t start, size_t length, size_t stride);
slice(const slice&);
```

The default constructor is equivalent to `slice(0, 0, 0)`. A default
constructor is provided only to permit the declaration of arrays of
slices. The constructor with arguments for a slice takes a start,
length, and stride parameter.

[*Example 1*: `slice(3, 8, 2)` constructs a slice which selects
elements 3, 5, 7, ... 17 from an array. — *end example*]

#### `slice` access functions <a id="slice.access">[[slice.access]]</a>

``` cpp
size_t start() const;
size_t size() const;
size_t stride() const;
```

*Returns:* The start, length, or stride specified by a `slice` object.

*Complexity:* Constant time.

### Class template `slice_array` <a id="template.slice.array">[[template.slice.array]]</a>

#### Class template `slice_array` overview <a id="template.slice.array.overview">[[template.slice.array.overview]]</a>

``` cpp
namespace std {
  template <class T> class slice_array {
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

    slice_array() = delete;       // as implied by declaring copy constructor above
  };
}
```

The `slice_array` template is a helper template used by the `slice`
subscript operator

``` cpp
slice_array<T> valarray<T>::operator[](slice);
```

It has reference semantics to a subset of an array specified by a
`slice` object.

[*Example 1*: The expression `a[slice(1, 5, 3)] = b;` has the effect of
assigning the elements of `b` to a slice of the elements in `a`. For the
slice shown, the elements selected from `a` are 1, 4, ...,
13. — *end example*]

#### `slice_array` assignment <a id="slice.arr.assign">[[slice.arr.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const slice_array& operator=(const slice_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which the `slice_array` object refers.

#### `slice_array` compound assignment <a id="slice.arr.comp.assign">[[slice.arr.comp.assign]]</a>

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

#### `slice_array` fill function <a id="slice.arr.fill">[[slice.arr.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`slice_array` object refers.

### The `gslice` class <a id="class.gslice">[[class.gslice]]</a>

#### The `gslice` class overview <a id="class.gslice.overview">[[class.gslice.overview]]</a>

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

#### `gslice` constructors <a id="gslice.cons">[[gslice.cons]]</a>

``` cpp
gslice();
gslice(size_t start, const valarray<size_t>& lengths,
         const valarray<size_t>& strides);
gslice(const gslice&);
```

The default constructor is equivalent to
`gslice(0, valarray<size_t>(), valarray<size_t>())`. The constructor
with arguments builds a `gslice` based on a specification of start,
lengths, and strides, as explained in the previous section.

#### `gslice` access functions <a id="gslice.access">[[gslice.access]]</a>

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

#### Class template `gslice_array` overview <a id="template.gslice.array.overview">[[template.gslice.array.overview]]</a>

``` cpp
namespace std {
  template <class T> class gslice_array {
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

    gslice_array() = delete;      // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the `slice` subscript
operator

``` cpp
gslice_array<T> valarray<T>::operator[](const gslice&);
```

It has reference semantics to a subset of an array specified by a
`gslice` object.

Thus, the expression `a[gslice(1, length, stride)] = b` has the effect
of assigning the elements of `b` to a generalized slice of the elements
in `a`.

#### `gslice_array` assignment <a id="gslice.array.assign">[[gslice.array.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const gslice_array& operator=(const gslice_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which the `gslice_array` refers.

#### `gslice_array` compound assignment <a id="gslice.array.comp.assign">[[gslice.array.comp.assign]]</a>

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

#### `gslice_array` fill function <a id="gslice.array.fill">[[gslice.array.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`gslice_array` object refers.

### Class template `mask_array` <a id="template.mask.array">[[template.mask.array]]</a>

#### Class template `mask_array` overview <a id="template.mask.array.overview">[[template.mask.array.overview]]</a>

``` cpp
namespace std {
  template <class T> class mask_array {
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

    mask_array() = delete;        // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the mask subscript operator:

``` cpp
mask_array<T> valarray<T>::operator[](const valarray<bool>&).
```

It has reference semantics to a subset of an array specified by a
boolean mask. Thus, the expression `a[mask] = b;` has the effect of
assigning the elements of `b` to the masked elements in `a` (those for
which the corresponding element in `mask` is `true`.)

#### `mask_array` assignment <a id="mask.array.assign">[[mask.array.assign]]</a>

``` cpp
void operator=(const valarray<T>&) const;
const mask_array& operator=(const mask_array&) const;
```

These assignment operators have reference semantics, assigning the
values of the argument array elements to selected elements of the
`valarray<T>` object to which it refers.

#### `mask_array` compound assignment <a id="mask.array.comp.assign">[[mask.array.comp.assign]]</a>

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
elements of the `valarray<T>` object to which the mask object refers.

#### `mask_array` fill function <a id="mask.array.fill">[[mask.array.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`mask_array` object refers.

### Class template `indirect_array` <a id="template.indirect.array">[[template.indirect.array]]</a>

#### Class template `indirect_array` overview <a id="template.indirect.array.overview">[[template.indirect.array.overview]]</a>

``` cpp
namespace std {
  template <class T> class indirect_array {
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

    indirect_array() = delete;        // as implied by declaring copy constructor above
  };
}
```

This template is a helper template used by the indirect subscript
operator

``` cpp
indirect_array<T> valarray<T>::operator[](const valarray<size_t>&).
```

It has reference semantics to a subset of an array specified by an
`indirect_array`. Thus the expression `a[indirect] = b;` has the effect
of assigning the elements of `b` to the elements in `a` whose indices
appear in `indirect`.

#### `indirect_array` assignment <a id="indirect.array.assign">[[indirect.array.assign]]</a>

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

#### `indirect_array` compound assignment <a id="indirect.array.comp.assign">[[indirect.array.comp.assign]]</a>

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

#### `indirect_array` fill function <a id="indirect.array.fill">[[indirect.array.fill]]</a>

``` cpp
void operator=(const T&) const;
```

This function has reference semantics, assigning the value of its
argument to the elements of the `valarray<T>` object to which the
`indirect_array` object refers.

### `valarray` range access <a id="valarray.range">[[valarray.range]]</a>

In the `begin` and `end` function templates that follow, *unspecified*1
is a type that meets the requirements of a mutable random access
iterator ([[random.access.iterators]]) and of a contiguous iterator (
[[iterator.requirements.general]]) whose `value_type` is the template
parameter `T` and whose `reference` type is `T&`. *unspecified*2 is a
type that meets the requirements of a constant random access iterator (
[[random.access.iterators]]) and of a contiguous iterator (
[[iterator.requirements.general]]) whose `value_type` is the template
parameter `T` and whose `reference` type is `const T&`.

The iterators returned by `begin` and `end` for an array are guaranteed
to be valid until the member function `resize(size_t, T)` (
[[valarray.members]]) is called for that array or until the lifetime of
that array ends, whichever happens first.

``` cpp
template <class T> unspecified{1} begin(valarray<T>& v);
template <class T> unspecified{2} begin(const valarray<T>& v);
```

*Returns:* An iterator referencing the first value in the array.

``` cpp
template <class T> unspecified{1} end(valarray<T>& v);
template <class T> unspecified{2} end(const valarray<T>& v);
```

*Returns:* An iterator referencing one past the last value in the array.

## Generalized numeric operations <a id="numeric.ops">[[numeric.ops]]</a>

### Header `<numeric>` synopsis <a id="numeric.ops.overview">[[numeric.ops.overview]]</a>

``` cpp
namespace std {
  // [accumulate], accumulate
  template <class InputIterator, class T>
    T accumulate(InputIterator first, InputIterator last, T init);
  template <class InputIterator, class T, class BinaryOperation>
    T accumulate(InputIterator first, InputIterator last, T init,
                 BinaryOperation binary_op);

  // [reduce], reduce
  template<class InputIterator>
    typename iterator_traits<InputIterator>::value_type
      reduce(InputIterator first, InputIterator last);
  template<class InputIterator, class T>
    T reduce(InputIterator first, InputIterator last, T init);
  template<class InputIterator, class T, class BinaryOperation>
    T reduce(InputIterator first, InputIterator last, T init,
             BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator>
    typename iterator_traits<ForwardIterator>::value_type
      reduce(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
             ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class T>
    T reduce(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
             ForwardIterator first, ForwardIterator last, T init);
  template<class ExecutionPolicy, class ForwardIterator, class T, class BinaryOperation>
    T reduce(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
             ForwardIterator first, ForwardIterator last, T init,
             BinaryOperation binary_op);

  // [inner.product], inner product
  template <class InputIterator1, class InputIterator2, class T>
    T inner_product(InputIterator1 first1, InputIterator1 last1,
                    InputIterator2 first2, T init);
  template <class InputIterator1, class InputIterator2, class T,
            class BinaryOperation1, class BinaryOperation2>
    T inner_product(InputIterator1 first1, InputIterator1 last1,
                    InputIterator2 first2, T init,
                    BinaryOperation1 binary_op1,
                    BinaryOperation2 binary_op2);

  // [transform.reduce], transform reduce
  template<class InputIterator1, class InputIterator2, class T>
    T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2,
                       T init);
  template<class InputIterator1, class InputIterator2, class T,
           class BinaryOperation1, class BinaryOperation2>
    T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2,
                       T init,
                       BinaryOperation1 binary_op1,
                       BinaryOperation2 binary_op2);
  template<class InputIterator, class T,
           class BinaryOperation, class UnaryOperation>
    T transform_reduce(InputIterator first, InputIterator last,
                       T init,
                       BinaryOperation binary_op, UnaryOperation unary_op);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2, class T>
    T transform_reduce(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                       ForwardIterator1 first1, ForwardIterator1 last1,
                       ForwardIterator2 first2,
                       T init);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2, class T,
           class BinaryOperation1, class BinaryOperation2>
    T transform_reduce(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                       ForwardIterator1 first1, ForwardIterator1 last1,
                       ForwardIterator2 first2,
                       T init,
                       BinaryOperation1 binary_op1,
                       BinaryOperation2 binary_op2);
  template<class ExecutionPolicy,
           class ForwardIterator, class T,
           class BinaryOperation, class UnaryOperation>
    T transform_reduce(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                       ForwardIterator first, ForwardIterator last,
                       T init,
                       BinaryOperation binary_op, UnaryOperation unary_op);

  // [partial.sum], partial sum
  template <class InputIterator, class OutputIterator>
    OutputIterator partial_sum(InputIterator first,
                               InputIterator last,
                               OutputIterator result);
  template <class InputIterator, class OutputIterator, class BinaryOperation>
    OutputIterator partial_sum(InputIterator first,
                               InputIterator last,
                               OutputIterator result,
                               BinaryOperation binary_op);

  // [exclusive.scan], exclusive scan
  template<class InputIterator, class OutputIterator, class T>
    OutputIterator exclusive_scan(InputIterator first, InputIterator last,
                                  OutputIterator result,
                                  T init);
  template<class InputIterator, class OutputIterator, class T, class BinaryOperation>
    OutputIterator exclusive_scan(InputIterator first, InputIterator last,
                                  OutputIterator result,
                                  T init, BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T>
    ForwardIterator2 exclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                    ForwardIterator1 first, ForwardIterator1 last,
                                    ForwardIterator2 result,
                                    T init);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T,
           class BinaryOperation>
    ForwardIterator2 exclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                    ForwardIterator1 first, ForwardIterator1 last,
                                    ForwardIterator2 result,
                                    T init, BinaryOperation binary_op);

  // [inclusive.scan], inclusive scan
  template<class InputIterator, class OutputIterator>
    OutputIterator inclusive_scan(InputIterator first, InputIterator last,
                                  OutputIterator result);
  template<class InputIterator, class OutputIterator, class BinaryOperation>
    OutputIterator inclusive_scan(InputIterator first, InputIterator last,
                                  OutputIterator result,
                                  BinaryOperation binary_op);
  template<class InputIterator, class OutputIterator, class BinaryOperation, class T>
    OutputIterator inclusive_scan(InputIterator first, InputIterator last,
                                  OutputIterator result,
                                  BinaryOperation binary_op, T init);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2 inclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                    ForwardIterator1 first, ForwardIterator1 last,
                                    ForwardIterator2 result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation>
    ForwardIterator2 inclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                    ForwardIterator1 first, ForwardIterator1 last,
                                    ForwardIterator2 result,
                                    BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation, class T>
    ForwardIterator2 inclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                    ForwardIterator1 first, ForwardIterator1 last,
                                    ForwardIterator2 result,
                                    BinaryOperation binary_op, T init);

  // [transform.exclusive.scan], transform exclusive scan
  template<class InputIterator, class OutputIterator, class T,
           class BinaryOperation, class UnaryOperation>
    OutputIterator transform_exclusive_scan(InputIterator first, InputIterator last,
                                            OutputIterator result,
                                            T init,
                                            BinaryOperation binary_op,
                                            UnaryOperation unary_op);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2, class T,
           class BinaryOperation, class UnaryOperation>
    ForwardIterator2 transform_exclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                              ForwardIterator1 first, ForwardIterator1 last,
                                              ForwardIterator2 result,
                                              T init,
                                              BinaryOperation binary_op,
                                              UnaryOperation unary_op);

  // [transform.inclusive.scan], transform inclusive scan
  template<class InputIterator, class OutputIterator,
           class BinaryOperation, class UnaryOperation>
    OutputIterator transform_inclusive_scan(InputIterator first, InputIterator last,
                                            OutputIterator result,
                                            BinaryOperation binary_op,
                                            UnaryOperation unary_op);
  template<class InputIterator, class OutputIterator,
           class BinaryOperation, class UnaryOperation, class T>
    OutputIterator transform_inclusive_scan(InputIterator first, InputIterator last,
                                            OutputIterator result,
                                            BinaryOperation binary_op,
                                            UnaryOperation unary_op,
                                            T init);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation, class UnaryOperation>
    ForwardIterator2 transform_inclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                              ForwardIterator1 first, ForwardIterator1 last,
                                              ForwardIterator2 result,
                                              BinaryOperation binary_op,
                                              UnaryOperation unary_op);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation, class UnaryOperation, class T>
    ForwardIterator2 transform_inclusive_scan(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                              ForwardIterator1 first, ForwardIterator1 last,
                                              ForwardIterator2 result,
                                              BinaryOperation binary_op,
                                              UnaryOperation unary_op,
                                              T init);

  // [adjacent.difference], adjacent difference
  template <class InputIterator, class OutputIterator>
    OutputIterator adjacent_difference(InputIterator first,
                                       InputIterator last,
                                       OutputIterator result);
  template <class InputIterator, class OutputIterator, class BinaryOperation>
    OutputIterator adjacent_difference(InputIterator first,
                                       InputIterator last,
                                       OutputIterator result,
                                       BinaryOperation binary_op);
  template <class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2 adjacent_difference(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                         ForwardIterator1 first,
                                         ForwardIterator1 last,
                                         ForwardIterator2 result);
  template <class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
            class BinaryOperation>
    ForwardIterator2 adjacent_difference(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                         ForwardIterator1 first,
                                         ForwardIterator1 last,
                                         ForwardIterator2 result,
                                         BinaryOperation binary_op);

  // [numeric.iota], iota
  template <class ForwardIterator, class T>
    void iota(ForwardIterator first, ForwardIterator last, T value);

  // [numeric.ops.gcd], greatest common divisor
  template <class M, class N>
    constexpr common_type_t<M,N> gcd(M m, N n);

  // [numeric.ops.lcm], least common multiple
  template <class M, class N>
    constexpr common_type_t<M,N> lcm(M m, N n);
}
```

The requirements on the types of algorithms’ arguments that are
described in the introduction to Clause  [[algorithms]] also apply to
the following algorithms.

Throughout this subclause, the parameters `UnaryOperation`,
`BinaryOperation`, `BinaryOperation1`, and `BinaryOperation2` are used
whenever an algorithm expects a function object ([[function.objects]]).

[*Note 1*: The use of closed ranges as well as semi-open ranges to
specify requirements throughout this subclause is
intentional. — *end note*]

### Accumulate <a id="accumulate">[[accumulate]]</a>

``` cpp
template <class InputIterator, class T>
  T accumulate(InputIterator first, InputIterator last, T init);
template <class InputIterator, class T, class BinaryOperation>
  T accumulate(InputIterator first, InputIterator last, T init,
               BinaryOperation binary_op);
```

*Requires:* `T` shall meet the requirements of `CopyConstructible`
(Table  [[tab:copyconstructible]]) and `CopyAssignable`
(Table  [[tab:copyassignable]]) types. In the range \[`first`, `last`\],
`binary_op` shall neither modify elements nor invalidate iterators or
subranges.[^13]

*Effects:* Computes its result by initializing the accumulator `acc`
with the initial value `init` and then modifies it with `acc = acc + *i`
or `acc = binary_op(acc, *i)` for every iterator `i` in the range
\[`first`, `last`) in order.[^14]

### Reduce <a id="reduce">[[reduce]]</a>

``` cpp
template<class InputIterator>
  typename iterator_traits<InputIterator>::value_type
    reduce(InputIterator first, InputIterator last);
```

*Effects:* Equivalent to:

``` cpp
return reduce(first, last,
              typename iterator_traits<InputIterator>::value_type{});
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator>
  typename iterator_traits<ForwardIterator>::value_type
    reduce(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
return reduce(std::forward<ExecutionPolicy>(exec), first, last,
              typename iterator_traits<ForwardIterator>::value_type{});
```

``` cpp
template<class InputIterator, class T>
  T reduce(InputIterator first, InputIterator last, T init);
```

*Effects:* Equivalent to:

``` cpp
return reduce(first, last, init, plus<>());
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator, class T>
  T reduce(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator last, T init);
```

*Effects:* Equivalent to:

``` cpp
return reduce(std::forward<ExecutionPolicy>(exec), first, last, init, plus<>());
```

``` cpp
template<class InputIterator, class T, class BinaryOperation>
  T reduce(InputIterator first, InputIterator last, T init,
           BinaryOperation binary_op);
template<class ExecutionPolicy, class ForwardIterator, class T, class BinaryOperation>
  T reduce(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator last, T init,
           BinaryOperation binary_op);
```

*Requires:*

- `T` shall be `MoveConstructible` (Table  [[tab:moveconstructible]]).
- All of `binary_op(init, *first)`, `binary_op(*first, init)`,
  `binary_op(init, init)`, and `binary_op(*first, *first)` shall be
  convertible to `T`.
- `binary_op` shall neither invalidate iterators or subranges, nor
  modify elements in the range \[`first`, `last`\].

*Returns:* *GENERALIZED_SUM*(binary_op, init, \*i, ...) for every `i` in
\[`first`, `last`).

*Complexity:* 𝑂(`last - first`) applications of `binary_op`.

[*Note 1*: The difference between `reduce` and `accumulate` is that
`reduce` applies `binary_op` in an unspecified order, which yields a
nondeterministic result for non-associative or non-commutative
`binary_op` such as floating-point addition. — *end note*]

### Inner product <a id="inner.product">[[inner.product]]</a>

``` cpp
template <class InputIterator1, class InputIterator2, class T>
  T inner_product(InputIterator1 first1, InputIterator1 last1,
                  InputIterator2 first2, T init);
template <class InputIterator1, class InputIterator2, class T,
          class BinaryOperation1, class BinaryOperation2>
  T inner_product(InputIterator1 first1, InputIterator1 last1,
                  InputIterator2 first2, T init,
                  BinaryOperation1 binary_op1,
                  BinaryOperation2 binary_op2);
```

*Requires:* `T` shall meet the requirements of `CopyConstructible`
(Table  [[tab:copyconstructible]]) and `CopyAssignable`
(Table  [[tab:copyassignable]]) types. In the ranges \[`first1`,
`last1`\] and \[`first2`, `first2 + (last1 - first1)`\] `binary_op1` and
`binary_op2` shall neither modify elements nor invalidate iterators or
subranges.[^15]

*Effects:* Computes its result by initializing the accumulator `acc`
with the initial value `init` and then modifying it with
`acc = acc + (*i1) * (*i2)` or
`acc = binary_op1(acc, binary_op2(*i1, *i2))` for every iterator `i1` in
the range \[`first1`, `last1`) and iterator `i2` in the range
\[`first2`, `first2 + (last1 - first1)`) in order.

### Transform reduce <a id="transform.reduce">[[transform.reduce]]</a>

``` cpp
template <class InputIterator1, class InputIterator2, class T>
  T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2,
                     T init);
template <class ExecutionPolicy,
          class ForwardIterator1, class ForwardIterator2, class T>
  T transform_reduce(ExecutionPolicy&& exec,
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2,
                     T init);
```

*Effects:* Equivalent to:

``` cpp
return transform_reduce(first1, last1, first2, init, plus<>(), multiplies<>());
```

``` cpp
template <class InputIterator1, class InputIterator2, class T,
          class BinaryOperation1, class BinaryOperation2>
  T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2,
                     T init,
                     BinaryOperation1 binary_op1,
                     BinaryOperation2 binary_op2);
template <class ExecutionPolicy,
          class ForwardIterator1, class ForwardIterator2, class T,
          class BinaryOperation1, class BinaryOperation2>
  T transform_reduce(ExecutionPolicy&& exec,
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2,
                     T init,
                     BinaryOperation1 binary_op1,
                     BinaryOperation2 binary_op2);
```

*Requires:*

- `T` shall be `MoveConstructible` (Table  [[tab:moveconstructible]]).
- All of
  - `binary_op1(init, init)`,
  - `binary_op1(init, binary_op2(*first1, *first2))`,
  - `binary_op1(binary_op2(*first1, *first2), init)`, and
  - `binary_op1(binary_op2(*first1, *first2), binary_op2(*first1, *first2))`

  shall be convertible to `T`.
- Neither `binary_op1` nor `binary_op2` shall invalidate subranges, or
  modify elements in the ranges \[`first1`, `last1`\] and \[`first2`,
  `first2 + (last1 - first1)`\].

*Returns:*

``` cpp
GENERALIZED_SUM(binary_op1, init, binary_op2(*i, *(first2 + (i - first1))), ...)
```

for every iterator `i` in \[`first1`, `last1`).

*Complexity:* 𝑂(`last1 - first1`) applications each of `binary_op1` and
`binary_op2`.

``` cpp
template<class InputIterator, class T,
         class BinaryOperation, class UnaryOperation>
  T transform_reduce(InputIterator first, InputIterator last, T init,
                     BinaryOperation binary_op, UnaryOperation unary_op);
template<class ExecutionPolicy,
         class ForwardIterator, class T,
         class BinaryOperation, class UnaryOperation>
  T transform_reduce(ExecutionPolicy&& exec,
                     ForwardIterator first, ForwardIterator last,
                     T init, BinaryOperation binary_op, UnaryOperation unary_op);
```

*Requires:*

- `T` shall be `MoveConstructible` (Table  [[tab:moveconstructible]]).
- All of
  - `binary_op(init, init)`,
  - `binary_op(init, unary_op(*first))`,
  - `binary_op(unary_op(*first), init)`, and
  - `binary_op(unary_op(*first), unary_op(*first))`

  shall be convertible to `T`.
- Neither `unary_op` nor `binary_op` shall invalidate subranges, or
  modify elements in the range \[`first`, `last`\].

*Returns:*

``` cpp
GENERALIZED_SUM(binary_op, init, unary_op(*i), ...)
```

for every iterator `i` in \[`first`, `last`).

*Complexity:* 𝑂(`last - first`) applications each of `unary_op` and
`binary_op`.

[*Note 1*: `transform_reduce` does not apply `unary_op` to
`init`. — *end note*]

### Partial sum <a id="partial.sum">[[partial.sum]]</a>

``` cpp
template <class InputIterator, class OutputIterator>
  OutputIterator partial_sum(
    InputIterator first, InputIterator last,
    OutputIterator result);
template <class InputIterator, class OutputIterator, class BinaryOperation>
  OutputIterator partial_sum(
    InputIterator first, InputIterator last,
    OutputIterator result, BinaryOperation binary_op);
```

*Requires:* `InputIterator`’s value type shall be constructible from the
type of `*first`. The result of the expression `acc + *i` or
`binary_op(acc, *i)` shall be implicitly convertible to
`InputIterator`’s value type. `acc` shall be
writable ([[iterator.requirements.general]]) to the `result` output
iterator. In the ranges \[`first`, `last`\] and \[`result`,
`result + (last - first)`\] `binary_op` shall neither modify elements
nor invalidate iterators or subranges.[^16]

*Effects:* For a non-empty range, the function creates an accumulator
`acc` whose type is `InputIterator`’s value type, initializes it with
`*first`, and assigns the result to `*result`. For every iterator `i` in
\[`first + 1`, `last`) in order, `acc` is then modified by
`acc = acc + *i` or `acc = binary_op(acc, *i)` and the result is
assigned to `*(result + (i - first))`.

*Returns:* `result + (last - first)`.

*Complexity:* Exactly `(last - first) - 1` applications of the binary
operation.

*Remarks:* `result` may be equal to `first`.

### Exclusive scan <a id="exclusive.scan">[[exclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator, class T>
  OutputIterator exclusive_scan(InputIterator first, InputIterator last,
                                OutputIterator result,
                                T init);
```

*Effects:* Equivalent to:

``` cpp
return exclusive_scan(first, last, result, init, plus<>());
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T>
  ForwardIterator2 exclusive_scan(ExecutionPolicy&& exec,
                                  ForwardIterator1 first, ForwardIterator1 last,
                                  ForwardIterator2 result,
                                  T init);
```

*Effects:* Equivalent to:

``` cpp
return exclusive_scan(std::forward<ExecutionPolicy>(exec),
                      first, last, result, init, plus<>());
```

``` cpp
template<class InputIterator, class OutputIterator, class T, class BinaryOperation>
  OutputIterator exclusive_scan(InputIterator first, InputIterator last,
                                OutputIterator result,
                                T init, BinaryOperation binary_op);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class T, class BinaryOperation>
  ForwardIterator2 exclusive_scan(ExecutionPolicy&& exec,
                                  ForwardIterator1 first, ForwardIterator1 last,
                                  ForwardIterator2 result,
                                  T init, BinaryOperation binary_op);
```

*Requires:*

- `T` shall be `MoveConstructible` (Table  [[tab:moveconstructible]]).
- All of `binary_op(init, init)`, `binary_op(init, *first)`, and
  `binary_op(*first, *first)` shall be convertible to `T`.
- `binary_op` shall neither invalidate iterators or subranges, nor
  modify elements in the ranges \[`first`, `last`\] or \[`result`,
  `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of:

``` cpp
GENERALIZED_NONCOMMUTATIVE_SUM(
    binary_op, init, *(first + 0), *(first + 1), ..., *(first + K - 1))
```

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications of `binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `exclusive_scan` and `inclusive_scan`
is that `exclusive_scan` excludes the `i`th input element from the `i`th
sum. If `binary_op` is not mathematically associative, the behavior of
`exclusive_scan` may be nondeterministic. — *end note*]

### Inclusive scan <a id="inclusive.scan">[[inclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  OutputIterator inclusive_scan(InputIterator first, InputIterator last,
                                OutputIterator result);
```

*Effects:* Equivalent to:

``` cpp
return inclusive_scan(first, last, result, plus<>());
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2 inclusive_scan(ExecutionPolicy&& exec,
                                ForwardIterator1 first, ForwardIterator1 last,
                                ForwardIterator2 result);
```

*Effects:* Equivalent to:

``` cpp
return inclusive_scan(std::forward<ExecutionPolicy>(exec), first, last, result, plus<>());
```

``` cpp
template<class InputIterator, class OutputIterator, class BinaryOperation>
  OutputIterator inclusive_scan(InputIterator first, InputIterator last,
                                OutputIterator result,
                                BinaryOperation binary_op);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation>
  ForwardIterator2 inclusive_scan(ExecutionPolicy&& exec,
                                  ForwardIterator1 first, ForwardIterator1 last,
                                  ForwardIterator2 result,
                                  BinaryOperation binary_op);

template<class InputIterator, class OutputIterator, class BinaryOperation, class T>
  OutputIterator inclusive_scan(InputIterator first, InputIterator last,
                                OutputIterator result,
                                BinaryOperation binary_op, T init);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class BinaryOperation, class T>
  ForwardIterator2 inclusive_scan(ExecutionPolicy&& exec,
                                  ForwardIterator1 first, ForwardIterator1 last,
                                  ForwardIterator2 result,
                                  BinaryOperation binary_op, T init);
```

*Requires:*

- If `init` is provided, `T` shall be `MoveConstructible`
  (Table  [[tab:moveconstructible]]); otherwise, `ForwardIterator1`’s
  value type shall be `MoveConstructible`.
- If `init` is provided, all of `binary_op(init, init)`,
  `binary_op(init, *first)`, and `binary_op(*first, *first)` shall be
  convertible to `T`; otherwise, `binary_op(*first, *first)` shall be
  convertible to `ForwardIterator1`’s value type.
- `binary_op` shall neither invalidate iterators or subranges, nor
  modify elements in the ranges \[`first`, `last`\] or \[`result`,
  `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of

- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op, init, \*(first + 0), \*(first + 1), ..., \*(first +
  K))  
  if `init` is provided, or
- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op, \*(first + 0), \*(first + 1), ..., \*(first + K))  
  otherwise.

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications of `binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `exclusive_scan` and `inclusive_scan`
is that `inclusive_scan` includes the `i`th input element in the `i`th
sum. If `binary_op` is not mathematically associative, the behavior of
`inclusive_scan` may be nondeterministic. — *end note*]

### Transform exclusive scan <a id="transform.exclusive.scan">[[transform.exclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator, class T,
         class BinaryOperation, class UnaryOperation>
  OutputIterator transform_exclusive_scan(InputIterator first, InputIterator last,
                                          OutputIterator result,
                                          T init,
                                          BinaryOperation binary_op,
                                          UnaryOperation unary_op);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class T,
         class BinaryOperation, class UnaryOperation>
  ForwardIterator2 transform_exclusive_scan(ExecutionPolicy&& exec,
                                            ForwardIterator1 first, ForwardIterator1 last,
                                            ForwardIterator2 result,
                                            T init,
                                            BinaryOperation binary_op,
                                            UnaryOperation unary_op);
```

*Requires:*

- `T` shall be `MoveConstructible` (Table  [[tab:moveconstructible]]).
- All of
  - `binary_op(init, init)`,
  - `binary_op(init, unary_op(*first))`, and
  - `binary_op(unary_op(*first), unary_op(*first))`

  shall be convertible to `T`.
- Neither `unary_op` nor `binary_op` shall invalidate iterators or
  subranges, or modify elements in the ranges \[`first`, `last`\] or
  \[`result`, `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of:

``` cpp
GENERALIZED_NONCOMMUTATIVE_SUM(
    binary_op, init,
    unary_op(*(first + 0)), unary_op(*(first + 1)), ..., unary_op(*(first + K - 1)))
```

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications each of `unary_op` and
`binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `transform_exclusive_scan` and
`transform_inclusive_scan` is that `transform_exclusive_scan` excludes
the iᵗʰ input element from the iᵗʰ sum. If `binary_op` is not
mathematically associative, the behavior of `transform_exclusive_scan`
may be nondeterministic. `transform_exclusive_scan` does not apply
`unary_op` to `init`. — *end note*]

### Transform inclusive scan <a id="transform.inclusive.scan">[[transform.inclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator,
         class BinaryOperation, class UnaryOperation>
  OutputIterator transform_inclusive_scan(InputIterator first, InputIterator last,
                                          OutputIterator result,
                                          BinaryOperation binary_op,
                                          UnaryOperation unary_op);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation, class UnaryOperation>
  ForwardIterator2 transform_inclusive_scan(ExecutionPolicy&& exec,
                                            ForwardIterator1 first, ForwardIterator1 last,
                                            ForwardIterator2 result,
                                            BinaryOperation binary_op,
                                            UnaryOperation unary_op);
template<class InputIterator, class OutputIterator,
         class BinaryOperation, class UnaryOperation, class T>
  OutputIterator transform_inclusive_scan(InputIterator first, InputIterator last,
                                          OutputIterator result,
                                          BinaryOperation binary_op,
                                          UnaryOperation unary_op,
                                          T init);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation, class UnaryOperation, class T>
  ForwardIterator2 transform_inclusive_scan(ExecutionPolicy&& exec,
                                            ForwardIterator1 first, ForwardIterator1 last,
                                            ForwardIterator2 result,
                                            BinaryOperation binary_op,
                                            UnaryOperation unary_op,
                                            T init);
```

*Requires:*

- If `init` is provided, `T` shall be `MoveConstructible`
  (Table  [[tab:moveconstructible]]); otherwise, `ForwardIterator1`’s
  value type shall be `MoveConstructible`.
- If `init` is provided, all of
  - `binary_op(init, init)`,
  - `binary_op(init, unary_op(*first))`, and
  - `binary_op(unary_op(*first), unary_op(*first))`

  shall be convertible to `T`; otherwise,
  `binary_op(unary_op(*first), unary_op(*first))` shall be convertible
  to `ForwardIterator1`’s value type.
- Neither `unary_op` nor `binary_op` shall invalidate iterators or
  subranges, nor modify elements in the ranges \[`first`, `last`\] or
  \[`result`, `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of

- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op, init,  
      unary_op(\*(first + 0)), unary_op(\*(first + 1)), ...,
  unary_op(\*(first + K)))  
  if `init` is provided, or
- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op,  
      unary_op(\*(first + 0)), unary_op(\*(first + 1)), ...,
  unary_op(\*(first + K)))  
  otherwise.

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications each of `unary_op` and
`binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `transform_exclusive_scan` and
`transform_inclusive_scan` is that `transform_inclusive_scan` includes
the iᵗʰ input element in the iᵗʰ sum. If `binary_op` is not
mathematically associative, the behavior of `transform_inclusive_scan`
may be nondeterministic. `transform_inclusive_scan` does not apply
`unary_op` to `init`. — *end note*]

### Adjacent difference <a id="adjacent.difference">[[adjacent.difference]]</a>

``` cpp
template <class InputIterator, class OutputIterator>
  OutputIterator
    adjacent_difference(InputIterator first, InputIterator last,
                        OutputIterator result);
template <class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    adjacent_difference(ExecutionPolicy&& exec,
                        ForwardIterator1 first, ForwardIterator1 last,
                        ForwardIterator2 result);

template <class InputIterator, class OutputIterator, class BinaryOperation>
  OutputIterator
    adjacent_difference(InputIterator first, InputIterator last,
                        OutputIterator result,
                        BinaryOperation binary_op);
template <class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
          class BinaryOperation>
  ForwardIterator2
    adjacent_difference(ExecutionPolicy&& exec,
                        ForwardIterator1 first, ForwardIterator1 last,
                        ForwardIterator2 result,
                        BinaryOperation binary_op);
```

*Requires:*

- For the overloads with no `ExecutionPolicy`, `InputIterator`’s value
  type shall be `MoveAssignable` (Table  [[tab:moveassignable]]) and
  shall be constructible from the type of `*first`. `acc` (defined
  below) shall be writable ([[iterator.requirements.general]]) to the
  `result` output iterator. The result of the expression `val - acc` or
  `binary_op(val, acc)` shall be writable to the `result` output
  iterator.
- For the overloads with an `ExecutionPolicy`, the value type of
  `ForwardIterator1` shall be `CopyConstructible`
  (Table  [[tab:copyconstructible]]), constructible from the expression
  `*first - *first` or `binary_op(*first, *first)`, and assignable to
  the value type of `ForwardIterator2`.
- For all overloads, in the ranges \[`first`, `last`\] and \[`result`,
  `result + (last - first)`\], `binary_op` shall neither modify elements
  nor invalidate iterators or subranges.[^17]

*Effects:* For the overloads with no `ExecutionPolicy` and a non-empty
range, the function creates an accumulator `acc` whose type is
`InputIterator`’s value type, initializes it with `*first`, and assigns
the result to `*result`. For every iterator `i` in \[`first + 1`,
`last`) in order, creates an object `val` whose type is
`InputIterator`’s value type, initializes it with `*i`, computes
`val - acc` or `binary_op(val, acc)`, assigns the result to
`*(result + (i - first))`, and move assigns from `val` to `acc`.

For the overloads with an `ExecutionPolicy` and a non-empty range, first
the function creates an object whose type is `ForwardIterator1`’s value
type, initializes it with `*first`, and assigns the result to `*result`.
Then for every `d` in \[`1`, `last - first - 1`\], creates an object
`val` whose type is `ForwardIterator1`’s value type, initializes it with
`*(first + d) - *(first + d - 1)` or
`binary_op(*(first + d), *(first + d - 1))`, and assigns the result to
`*(result + d)`.

*Returns:* `result + (last - first)`.

*Complexity:* Exactly `(last - first) - 1` applications of the binary
operation.

*Remarks:* For the overloads with no `ExecutionPolicy`, `result` may be
equal to `first`. For the overloads with an `ExecutionPolicy`, the
ranges \[`first`, `last`) and \[`result`, `result + (last - first)`)
shall not overlap.

### Iota <a id="numeric.iota">[[numeric.iota]]</a>

``` cpp
template <class ForwardIterator, class T>
  void iota(ForwardIterator first, ForwardIterator last, T value);
```

*Requires:* `T` shall be convertible to `ForwardIterator`’s value type.
The expression `++val`, where `val` has type `T`, shall be well formed.

*Effects:* For each element referred to by the iterator `i` in the range
\[`first`, `last`), assigns `*i = value` and increments `value` as if by
`++value`.

*Complexity:* Exactly `last - first` increments and assignments.

### Greatest common divisor <a id="numeric.ops.gcd">[[numeric.ops.gcd]]</a>

``` cpp
template <class M, class N>
  constexpr common_type_t<M,N> gcd(M m, N n);
```

*Requires:* `|m|` and `|n|` shall be representable as a value of
`common_type_t<M, N>`.

[*Note 1*: These requirements ensure, for example, that
`gcd(m, m) = |m|` is representable as a value of type
`M`. — *end note*]

*Remarks:* If either `M` or `N` is not an integer type, or if either is
cv `bool`, the program is ill-formed.

*Returns:* Zero when `m` and `n` are both zero. Otherwise, returns the
greatest common divisor of `|m|` and `|n|`.

*Throws:* Nothing.

### Least common multiple <a id="numeric.ops.lcm">[[numeric.ops.lcm]]</a>

``` cpp
template <class M, class N>
  constexpr common_type_t<M,N> lcm(M m, N n);
```

*Requires:* `|m|` and `|n|` shall be representable as a value of
`common_type_t<M, N>`. The least common multiple of `|m|` and `|n|`
shall be representable as a value of type `common_type_t<M,N>`.

*Remarks:* If either `M` or `N` is not an integer type, or if either is
cv `bool` the program is ill-formed.

*Returns:* Zero when either `m` or `n` is zero. Otherwise, returns the
least common multiple of `|m|` and `|n|`.

*Throws:* Nothing.

## Mathematical functions for floating-point types <a id="c.math">[[c.math]]</a>

### Header `<cmath>` synopsis <a id="cmath.syn">[[cmath.syn]]</a>

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
  float acos(float x);  // see [library.c]
  double acos(double x);
  long double acos(long double x);  // see [library.c]
  float acosf(float x);
  long double acosl(long double x);

  float asin(float x);  // see [library.c]
  double asin(double x);
  long double asin(long double x);  // see [library.c]
  float asinf(float x);
  long double asinl(long double x);

  float atan(float x);  // see [library.c]
  double atan(double x);
  long double atan(long double x);  // see [library.c]
  float atanf(float x);
  long double atanl(long double x);

  float atan2(float y, float x);  // see [library.c]
  double atan2(double y, double x);
  long double atan2(long double y, long double x);  // see [library.c]
  float atan2f(float y, float x);
  long double atan2l(long double y, long double x);

  float cos(float x);  // see [library.c]
  double cos(double x);
  long double cos(long double x);  // see [library.c]
  float cosf(float x);
  long double cosl(long double x);

  float sin(float x);  // see [library.c]
  double sin(double x);
  long double sin(long double x);  // see [library.c]
  float sinf(float x);
  long double sinl(long double x);

  float tan(float x);  // see [library.c]
  double tan(double x);
  long double tan(long double x);  // see [library.c]
  float tanf(float x);
  long double tanl(long double x);

  float acosh(float x);  // see [library.c]
  double acosh(double x);
  long double acosh(long double x);  // see [library.c]
  float acoshf(float x);
  long double acoshl(long double x);

  float asinh(float x);  // see [library.c]
  double asinh(double x);
  long double asinh(long double x);  // see [library.c]
  float asinhf(float x);
  long double asinhl(long double x);

  float atanh(float x);  // see [library.c]
  double atanh(double x);
  long double atanh(long double x);  // see [library.c]
  float atanhf(float x);
  long double atanhl(long double x);

  float cosh(float x);  // see [library.c]
  double cosh(double x);
  long double cosh(long double x);  // see [library.c]
  float coshf(float x);
  long double coshl(long double x);

  float sinh(float x);  // see [library.c]
  double sinh(double x);
  long double sinh(long double x);  // see [library.c]
  float sinhf(float x);
  long double sinhl(long double x);

  float tanh(float x);  // see [library.c]
  double tanh(double x);
  long double tanh(long double x);  // see [library.c]
  float tanhf(float x);
  long double tanhl(long double x);

  float exp(float x);  // see [library.c]
  double exp(double x);
  long double exp(long double x);  // see [library.c]
  float expf(float x);
  long double expl(long double x);

  float exp2(float x);  // see [library.c]
  double exp2(double x);
  long double exp2(long double x);  // see [library.c]
  float exp2f(float x);
  long double exp2l(long double x);

  float expm1(float x);  // see [library.c]
  double expm1(double x);
  long double expm1(long double x);  // see [library.c]
  float expm1f(float x);
  long double expm1l(long double x);

  float frexp(float value, int* exp);  // see [library.c]
  double frexp(double value, int* exp);
  long double frexp(long double value, int* exp);  // see [library.c]
  float frexpf(float value, int* exp);
  long double frexpl(long double value, int* exp);

  int ilogb(float x);  // see [library.c]
  int ilogb(double x);
  int ilogb(long double x);  // see [library.c]
  int ilogbf(float x);
  int ilogbl(long double x);

  float ldexp(float x, int exp);  // see [library.c]
  double ldexp(double x, int exp);
  long double ldexp(long double x, int exp);  // see [library.c]
  float ldexpf(float x, int exp);
  long double ldexpl(long double x, int exp);

  float log(float x);  // see [library.c]
  double log(double x);
  long double log(long double x);  // see [library.c]
  float logf(float x);
  long double logl(long double x);

  float log10(float x);  // see [library.c]
  double log10(double x);
  long double log10(long double x);  // see [library.c]
  float log10f(float x);
  long double log10l(long double x);

  float log1p(float x);  // see [library.c]
  double log1p(double x);
  long double log1p(long double x);  // see [library.c]
  float log1pf(float x);
  long double log1pl(long double x);

  float log2(float x);  // see [library.c]
  double log2(double x);
  long double log2(long double x);  // see [library.c]
  float log2f(float x);
  long double log2l(long double x);

  float logb(float x);  // see [library.c]
  double logb(double x);
  long double logb(long double x);  // see [library.c]
  float logbf(float x);
  long double logbl(long double x);

  float modf(float value, float* iptr);  // see [library.c]
  double modf(double value, double* iptr);
  long double modf(long double value, long double* iptr);  // see [library.c]
  float modff(float value, float* iptr);
  long double modfl(long double value, long double* iptr);

  float scalbn(float x, int n);  // see [library.c]
  double scalbn(double x, int n);
  long double scalbn(long double x, int n);  // see [library.c]
  float scalbnf(float x, int n);
  long double scalbnl(long double x, int n);

  float scalbln(float x, long int n);  // see [library.c]
  double scalbln(double x, long int n);
  long double scalbln(long double x, long int n);  // see [library.c]
  float scalblnf(float x, long int n);
  long double scalblnl(long double x, long int n);

  float cbrt(float x);  // see [library.c]
  double cbrt(double x);
  long double cbrt(long double x);  // see [library.c]
  float cbrtf(float x);
  long double cbrtl(long double x);

  // [c.math.abs], absolute values
  int abs(int j);
  long int abs(long int j);
  long long int abs(long long int j);
  float abs(float j);
  double abs(double j);
  long double abs(long double j);

  float fabs(float x);  // see [library.c]
  double fabs(double x);
  long double fabs(long double x);  // see [library.c]
  float fabsf(float x);
  long double fabsl(long double x);

  float hypot(float x, float y);  // see [library.c]
  double hypot(double x, double y);
  long double hypot(double x, double y);  // see [library.c]
  float hypotf(float x, float y);
  long double hypotl(long double x, long double y);

  // [c.math.hypot3], three-dimensional hypotenuse
  float hypot(float x, float y, float z);
  double hypot(double x, double y, double z);
  long double hypot(long double x, long double y, long double z);

  float pow(float x, float y);  // see [library.c]
  double pow(double x, double y);
  long double pow(long double x, long double y);  // see [library.c]
  float powf(float x, float y);
  long double powl(long double x, long double y);

  float sqrt(float x);  // see [library.c]
  double sqrt(double x);
  long double sqrt(long double x);  // see [library.c]
  float sqrtf(float x);
  long double sqrtl(long double x);

  float erf(float x);  // see [library.c]
  double erf(double x);
  long double erf(long double x);  // see [library.c]
  float erff(float x);
  long double erfl(long double x);

  float erfc(float x);  // see [library.c]
  double erfc(double x);
  long double erfc(long double x);  // see [library.c]
  float erfcf(float x);
  long double erfcl(long double x);

  float lgamma(float x);  // see [library.c]
  double lgamma(double x);
  long double lgamma(long double x);  // see [library.c]
  float lgammaf(float x);
  long double lgammal(long double x);

  float tgamma(float x);  // see [library.c]
  double tgamma(double x);
  long double tgamma(long double x);  // see [library.c]
  float tgammaf(float x);
  long double tgammal(long double x);

  float ceil(float x);  // see [library.c]
  double ceil(double x);
  long double ceil(long double x);  // see [library.c]
  float ceilf(float x);
  long double ceill(long double x);

  float floor(float x);  // see [library.c]
  double floor(double x);
  long double floor(long double x);  // see [library.c]
  float floorf(float x);
  long double floorl(long double x);

  float nearbyint(float x);  // see [library.c]
  double nearbyint(double x);
  long double nearbyint(long double x);  // see [library.c]
  float nearbyintf(float x);
  long double nearbyintl(long double x);

  float rint(float x);  // see [library.c]
  double rint(double x);
  long double rint(long double x);  // see [library.c]
  float rintf(float x);
  long double rintl(long double x);

  long int lrint(float x);  // see [library.c]
  long int lrint(double x);
  long int lrint(long double x);  // see [library.c]
  long int lrintf(float x);
  long int lrintl(long double x);

  long long int llrint(float x);  // see [library.c]
  long long int llrint(double x);
  long long int llrint(long double x);  // see [library.c]
  long long int llrintf(float x);
  long long int llrintl(long double x);

  float round(float x);  // see [library.c]
  double round(double x);
  long double round(long double x);  // see [library.c]
  float roundf(float x);
  long double roundl(long double x);

  long int lround(float x);  // see [library.c]
  long int lround(double x);
  long int lround(long double x);  // see [library.c]
  long int lroundf(float x);
  long int lroundl(long double x);

  long long int llround(float x);  // see [library.c]
  long long int llround(double x);
  long long int llround(long double x);  // see [library.c]
  long long int llroundf(float x);
  long long int llroundl(long double x);

  float trunc(float x);  // see [library.c]
  double trunc(double x);
  long double trunc(long double x);  // see [library.c]
  float truncf(float x);
  long double truncl(long double x);

  float fmod(float x, float y);  // see [library.c]
  double fmod(double x, double y);
  long double fmod(long double x, long double y);  // see [library.c]
  float fmodf(float x, float y);
  long double fmodl(long double x, long double y);

  float remainder(float x, float y);  // see [library.c]
  double remainder(double x, double y);
  long double remainder(long double x, long double y);  // see [library.c]
  float remainderf(float x, float y);
  long double remainderl(long double x, long double y);

  float remquo(float x, float y, int* quo);  // see [library.c]
  double remquo(double x, double y, int* quo);
  long double remquo(long double x, long double y, int* quo);  // see [library.c]
  float remquof(float x, float y, int* quo);
  long double remquol(long double x, long double y, int* quo);

  float copysign(float x, float y);  // see [library.c]
  double copysign(double x, double y);
  long double copysign(long double x, long double y);  // see [library.c]
  float copysignf(float x, float y);
  long double copysignl(long double x, long double y);

  double nan(const char* tagp);
  float nanf(const char* tagp);
  long double nanl(const char* tagp);

  float nextafter(float x, float y);  // see [library.c]
  double nextafter(double x, double y);
  long double nextafter(long double x, long double y);  // see [library.c]
  float nextafterf(float x, float y);
  long double nextafterl(long double x, long double y);

  float nexttoward(float x, long double y);  // see [library.c]
  double nexttoward(double x, long double y);
  long double nexttoward(long double x, long double y);  // see [library.c]
  float nexttowardf(float x, long double y);
  long double nexttowardl(long double x, long double y);

  float fdim(float x, float y);  // see [library.c]
  double fdim(double x, double y);
  long double fdim(long double x, long double y);  // see [library.c]
  float fdimf(float x, float y);
  long double fdiml(long double x, long double y);

  float fmax(float x, float y);  // see [library.c]
  double fmax(double x, double y);
  long double fmax(long double x, long double y);  // see [library.c]
  float fmaxf(float x, float y);
  long double fmaxl(long double x, long double y);

  float fmin(float x, float y);  // see [library.c]
  double fmin(double x, double y);
  long double fmin(long double x, long double y);  // see [library.c]
  float fminf(float x, float y);
  long double fminl(long double x, long double y);

  float fma(float x, float y, float z);  // see [library.c]
  double fma(double x, double y, double z);
  long double fma(long double x, long double y, long double z);  // see [library.c]
  float fmaf(float x, float y, float z);
  long double fmal(long double x, long double y, long double z);

  // [c.math.fpclass], classification / comparison functions
  int fpclassify(float x);
  int fpclassify(double x);
  int fpclassify(long double x);

  int isfinite(float x);
  int isfinite(double x);
  int isfinite(long double x);

  int isinf(float x);
  int isinf(double x);
  int isinf(long double x);

  int isnan(float x);
  int isnan(double x);
  int isnan(long double x);

  int isnormal(float x);
  int isnormal(double x);
  int isnormal(long double x);

  int signbit(float x);
  int signbit(double x);
  int signbit(long double x);

  int isgreater(float x, float y);
  int isgreater(double x, double y);
  int isgreater(long double x, long double y);

  int isgreaterequal(float x, float y);
  int isgreaterequal(double x, double y);
  int isgreaterequal(long double x, long double y);

  int isless(float x, float y);
  int isless(double x, double y);
  int isless(long double x, long double y);

  int islessequal(float x, float y);
  int islessequal(double x, double y);
  int islessequal(long double x, long double y);

  int islessgreater(float x, float y);
  int islessgreater(double x, double y);
  int islessgreater(long double x, long double y);

  int isunordered(float x, float y);
  int isunordered(double x, double y);
  int isunordered(long double x, long double y);

  // [sf.cmath], mathematical special functions

  // [sf.cmath.assoc_laguerre], associated Laguerre polynomials
  double       assoc_laguerre(unsigned n, unsigned m, double x);
  float        assoc_laguerref(unsigned n, unsigned m, float x);
  long double  assoc_laguerrel(unsigned n, unsigned m, long double x);

  // [sf.cmath.assoc_legendre], associated Legendre functions
  double       assoc_legendre(unsigned l, unsigned m, double x);
  float        assoc_legendref(unsigned l, unsigned m, float x);
  long double  assoc_legendrel(unsigned l, unsigned m, long double x);

  // [sf.cmath.beta], beta function
  double       beta(double x, double y);
  float        betaf(float x, float y);
  long double  betal(long double x, long double y);

  // [sf.cmath.comp_ellint_1], complete elliptic integral of the first kind
  double       comp_ellint_1(double k);
  float        comp_ellint_1f(float k);
  long double  comp_ellint_1l(long double k);

  // [sf.cmath.comp_ellint_2], complete elliptic integral of the second kind
  double       comp_ellint_2(double k);
  float        comp_ellint_2f(float k);
  long double  comp_ellint_2l(long double k);

  // [sf.cmath.comp_ellint_3], complete elliptic integral of the third kind
  double       comp_ellint_3(double k, double nu);
  float        comp_ellint_3f(float k, float nu);
  long double  comp_ellint_3l(long double k, long double nu);

  // [sf.cmath.cyl_bessel_i], regular modified cylindrical Bessel functions
  double       cyl_bessel_i(double nu, double x);
  float        cyl_bessel_if(float nu, float x);
  long double  cyl_bessel_il(long double nu, long double x);

  // [sf.cmath.cyl_bessel_j], cylindrical Bessel functions of the first kind
  double       cyl_bessel_j(double nu, double x);
  float        cyl_bessel_jf(float nu, float x);
  long double  cyl_bessel_jl(long double nu, long double x);

  // [sf.cmath.cyl_bessel_k], irregular modified cylindrical Bessel functions
  double       cyl_bessel_k(double nu, double x);
  float        cyl_bessel_kf(float nu, float x);
  long double  cyl_bessel_kl(long double nu, long double x);

  // [sf.cmath.cyl_neumann], cylindrical Neumann functions;
  // cylindrical Bessel functions of the second kind
  double       cyl_neumann(double nu, double x);
  float        cyl_neumannf(float nu, float x);
  long double  cyl_neumannl(long double nu, long double x);

  // [sf.cmath.ellint_1], incomplete elliptic integral of the first kind
  double       ellint_1(double k, double phi);
  float        ellint_1f(float k, float phi);
  long double  ellint_1l(long double k, long double phi);

  // [sf.cmath.ellint_2], incomplete elliptic integral of the second kind
  double       ellint_2(double k, double phi);
  float        ellint_2f(float k, float phi);
  long double  ellint_2l(long double k, long double phi);

  // [sf.cmath.ellint_3], incomplete elliptic integral of the third kind
  double       ellint_3(double k, double nu, double phi);
  float        ellint_3f(float k, float nu, float phi);
  long double  ellint_3l(long double k, long double nu, long double phi);

  // [sf.cmath.expint], exponential integral
  double       expint(double x);
  float        expintf(float x);
  long double  expintl(long double x);

  // [sf.cmath.hermite], Hermite polynomials
  double       hermite(unsigned n, double x);
  float        hermitef(unsigned n, float x);
  long double  hermitel(unsigned n, long double x);

  // [sf.cmath.laguerre], Laguerre polynomials
  double       laguerre(unsigned n, double x);
  float        laguerref(unsigned n, float x);
  long double  laguerrel(unsigned n, long double x);

  // [sf.cmath.legendre], Legendre polynomials
  double       legendre(unsigned l, double x);
  float        legendref(unsigned l, float x);
  long double  legendrel(unsigned l, long double x);

  // [sf.cmath.riemann_zeta], Riemann zeta function
  double       riemann_zeta(double x);
  float        riemann_zetaf(float x);
  long double  riemann_zetal(long double x);

  // [sf.cmath.sph_bessel], spherical Bessel functions of the first kind
  double       sph_bessel(unsigned n, double x);
  float        sph_besself(unsigned n, float x);
  long double  sph_bessell(unsigned n, long double x);

  // [sf.cmath.sph_legendre], spherical associated Legendre functions
  double       sph_legendre(unsigned l, unsigned m, double theta);
  float        sph_legendref(unsigned l, unsigned m, float theta);
  long double  sph_legendrel(unsigned l, unsigned m, long double theta);

  // [sf.cmath.sph_neumann], spherical Neumann functions;
  // spherical Bessel functions of the second kind:
  double       sph_neumann(unsigned n, double x);
  float        sph_neumannf(unsigned n, float x);
  long double  sph_neumannl(unsigned n, long double x);
}
```

The contents and meaning of the header `<cmath>` are the same as the C
standard library header `<math.h>`, with the addition of a
three-dimensional hypotenuse function ([[c.math.hypot3]]) and the
mathematical special functions described in [[sf.cmath]].

[*Note 1*: Several functions have additional overloads in this
International Standard, but they have the same behavior as in the C
standard library ([[library.c]]). — *end note*]

For each set of overloaded functions within `<cmath>`, with the
exception of `abs`, there shall be additional overloads sufficient to
ensure:

1.  If any argument of arithmetic type corresponding to a `double`
    parameter has type `long double`, then all arguments of arithmetic
    type ([[basic.fundamental]]) corresponding to `double` parameters
    are effectively cast to `long double`.
2.  Otherwise, if any argument of arithmetic type corresponding to a
    `double` parameter has type `double` or an integer type, then all
    arguments of arithmetic type corresponding to `double` parameters
    are effectively cast to `double`.
3.  Otherwise, all arguments of arithmetic type corresponding to
    `double` parameters have type `float`.

[*Note 2*: `abs` is exempted from these rules in order to stay
compatible with C. — *end note*]

ISO C 7.12

### Absolute values <a id="c.math.abs">[[c.math.abs]]</a>

[*Note 1*: The headers `<cstdlib>` ([[cstdlib.syn]]) and `<cmath>` (
[[cmath.syn]]) declare the functions described in this
subclause. — *end note*]

``` cpp
int abs(int j);
long int abs(long int j);
long long int abs(long long int j);
float abs(float j);
double abs(double j);
long double abs(long double j);
```

*Effects:* The `abs` functions have the semantics specified in the C
standard library for the functions `abs`, `labs`, `llabs`, `fabsf`,
`fabs`, and `fabsl`.

*Remarks:* If `abs()` is called with an argument of type `X` for which
`is_unsigned_v<X>` is `true` and if `X` cannot be converted to `int` by
integral promotion ([[conv.prom]]), the program is ill-formed.

[*Note 1*: Arguments that can be promoted to `int` are permitted for
compatibility with C. — *end note*]

ISO C 7.12.7.2, 7.22.6.1

### Three-dimensional hypotenuse <a id="c.math.hypot3">[[c.math.hypot3]]</a>

``` cpp
float hypot(float x, float y, float z);
double hypot(double x, double y, double z);
long double hypot(long double x, long double y, long double z);
```

*Returns:* $\sqrt{x^2+y^2+z^2}$.

### Classification / comparison functions <a id="c.math.fpclass">[[c.math.fpclass]]</a>

The classification / comparison functions behave the same as the C
macros with the corresponding names defined in the C standard library.
Each function is overloaded for the three floating-point types.

ISO C 7.12.3, 7.12.4

### Mathematical special functions <a id="sf.cmath">[[sf.cmath]]</a>

If any argument value to any of the functions specified in this
subclause is a NaN (Not a Number), the function shall return a NaN but
it shall not report a domain error. Otherwise, the function shall report
a domain error for just those argument values for which:

- the function description’s *Returns:* clause explicitly specifies a
  domain and those argument values fall outside the specified domain, or
- the corresponding mathematical function value has a nonzero imaginary
  component, or
- the corresponding mathematical function is not mathematically
  defined.[^18]

Unless otherwise specified, each function is defined for all finite
values, for negative infinity, and for positive infinity.

#### Associated Laguerre polynomials <a id="sf.cmath.assoc_laguerre">[[sf.cmath.assoc_laguerre]]</a>

``` cpp
double       assoc_laguerre(unsigned n, unsigned m, double x);
float        assoc_laguerref(unsigned n, unsigned m, float x);
long double  assoc_laguerrel(unsigned n, unsigned m, long double x);
```

*Effects:* These functions compute the associated Laguerre polynomials
of their respective arguments `n`, `m`, and `x`.

*Returns:* $$%
  \mathsf{L}_n^m(x) =
  (-1)^m \frac{\mathsf{d} ^ m}
       {\mathsf{d}x ^ m} \, \mathsf{L}_{n+m}(x),
       \quad \mbox{for $x \ge 0$}$$ where n is `n`, m is `m`, and x is
`x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128` or if `m >= 128`.

#### Associated Legendre functions <a id="sf.cmath.assoc_legendre">[[sf.cmath.assoc_legendre]]</a>

``` cpp
double       assoc_legendre(unsigned l, unsigned m, double x);
float        assoc_legendref(unsigned l, unsigned m, float x);
long double  assoc_legendrel(unsigned l, unsigned m, long double x);
```

*Effects:* These functions compute the associated Legendre functions of
their respective arguments `l`, `m`, and `x`.

*Returns:* $$%
  \mathsf{P}_\ell^m(x) =
  (1 - x^2) ^ {m/2}
  \:
  \frac{ \mathsf{d} ^ m}
       { \mathsf{d}x ^ m} \, \mathsf{P}_\ell(x),
       \quad \mbox{for $|x| \le 1$}$$ where l is `l`, m is `m`, and x is
`x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `l >= 128`.

#### Beta function <a id="sf.cmath.beta">[[sf.cmath.beta]]</a>

``` cpp
double       beta(double x, double y);
float        betaf(float x, float y);
long double  betal(long double x, long double y);
```

*Effects:* These functions compute the beta function of their respective
arguments `x` and `y`.

*Returns:* $$%
  \mathsf{B}(x, y) =
  \frac{ \Gamma(x) \, \Gamma(y) }
       { \Gamma(x+y) },
       \quad \mbox{for $x > 0$,\, $y > 0$}$$ where x is `x` and y is
`y`.

#### Complete elliptic integral of the first kind <a id="sf.cmath.comp_ellint_1">[[sf.cmath.comp_ellint_1]]</a>

``` cpp
double       comp_ellint_1(double k);
float        comp_ellint_1f(float k);
long double  comp_ellint_1l(long double k);
```

*Effects:* These functions compute the complete elliptic integral of the
first kind of their respective arguments `k`.

*Returns:* $$%
  \mathsf{K}(k) =
  \mathsf{F}(k, \pi / 2),
              \quad \mbox{for $|k| \le 1$}$$ where k is `k`.

See also [[sf.cmath.ellint_1]].

#### Complete elliptic integral of the second kind <a id="sf.cmath.comp_ellint_2">[[sf.cmath.comp_ellint_2]]</a>

``` cpp
double       comp_ellint_2(double k);
float        comp_ellint_2f(float k);
long double  comp_ellint_2l(long double k);
```

*Effects:* These functions compute the complete elliptic integral of the
second kind of their respective arguments `k`.

*Returns:* $$%
  \mathsf{E}(k) =
  \mathsf{E}(k, \pi / 2),
\quad \mbox{for $|k| \le 1$}$$ where k is `k`.

See also [[sf.cmath.ellint_2]].

#### Complete elliptic integral of the third kind <a id="sf.cmath.comp_ellint_3">[[sf.cmath.comp_ellint_3]]</a>

``` cpp
double       comp_ellint_3(double k, double nu);
float        comp_ellint_3f(float k, float nu);
long double  comp_ellint_3l(long double k, long double nu);
```

*Effects:* These functions compute the complete elliptic integral of the
third kind of their respective arguments `k` and `nu`.

*Returns:* $$%
  \mathsf{\Pi}(\nu, k) = \mathsf{\Pi}(\nu, k, \pi / 2),
        \quad \mbox{for $|k| \le 1$}$$ where k is `k` and $\nu$ is `nu`.

See also [[sf.cmath.ellint_3]].

#### Regular modified cylindrical Bessel functions <a id="sf.cmath.cyl_bessel_i">[[sf.cmath.cyl_bessel_i]]</a>

``` cpp
double       cyl_bessel_i(double nu, double x);
float        cyl_bessel_if(float nu, float x);
long double  cyl_bessel_il(long double nu, long double x);
```

*Effects:* These functions compute the regular modified cylindrical
Bessel functions of their respective arguments `nu` and `x`.

*Returns:* $$%
  \mathsf{I}_\nu(x) =
  i^{-\nu} \mathsf{J}_\nu(ix)
  =
  \sum_{k=0}^\infty \frac{(x/2)^{\nu+2k}}
             {k! \: \Gamma(\nu+k+1)},
       \quad \mbox{for $x \ge 0$}$$ where $\nu$ is `nu` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

See also [[sf.cmath.cyl_bessel_j]].

#### Cylindrical Bessel functions of the first kind <a id="sf.cmath.cyl_bessel_j">[[sf.cmath.cyl_bessel_j]]</a>

``` cpp
double       cyl_bessel_j(double nu, double x);
float        cyl_bessel_jf(float nu, float x);
long double  cyl_bessel_jl(long double nu, long double x);
```

*Effects:* These functions compute the cylindrical Bessel functions of
the first kind of their respective arguments `nu` and `x`.

*Returns:* $$%
  \mathsf{J}_\nu(x) =
  \sum_{k=0}^\infty \frac{(-1)^k (x/2)^{\nu+2k}}
             {k! \: \Gamma(\nu+k+1)},
       \quad \mbox{for $x \ge 0$}$$ where $\nu$ is `nu` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

#### Irregular modified cylindrical Bessel functions <a id="sf.cmath.cyl_bessel_k">[[sf.cmath.cyl_bessel_k]]</a>

``` cpp
double       cyl_bessel_k(double nu, double x);
float        cyl_bessel_kf(float nu, float x);
long double  cyl_bessel_kl(long double nu, long double x);
```

*Effects:* These functions compute the irregular modified cylindrical
Bessel functions of their respective arguments `nu` and `x`.

*Returns:* $$%
  \mathsf{K}_\nu(x) =
  (\pi/2)i^{\nu+1} (            \mathsf{J}_\nu(ix)
                + i \mathsf{N}_\nu(ix)
                )
  =
  \left\{
  \begin{array}{cl}
  \displaystyle
  \frac{\pi}{2}
  \frac{\mathsf{I}_{-\nu}(x) - \mathsf{I}_{\nu}(x)}
       {\sin \nu\pi },
  & \mbox{for $x \ge 0$ and non-integral $\nu$}
  \\
  \\
  \displaystyle
  \frac{\pi}{2}
  \lim_{\mu \rightarrow \nu} \frac{\mathsf{I}_{-\mu}(x) - \mathsf{I}_{\mu}(x)}
                                  {\sin \mu\pi },
  & \mbox{for $x \ge 0$ and integral $\nu$}
  \end{array}
  \right.$$ where $\nu$ is `nu` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

See also [[sf.cmath.cyl_bessel_i]], [[sf.cmath.cyl_bessel_j]],
[[sf.cmath.cyl_neumann]].

#### Cylindrical Neumann functions <a id="sf.cmath.cyl_neumann">[[sf.cmath.cyl_neumann]]</a>

``` cpp
double       cyl_neumann(double nu, double x);
float        cyl_neumannf(float nu, float x);
long double  cyl_neumannl(long double nu, long double x);
```

*Effects:* These functions compute the cylindrical Neumann functions,
also known as the cylindrical Bessel functions of the second kind, of
their respective arguments `nu` and `x`.

*Returns:* $$%
  \mathsf{N}_\nu(x) =
  \left\{
  \begin{array}{cl}
  \displaystyle
  \frac{\mathsf{J}_\nu(x) \cos \nu\pi - \mathsf{J}_{-\nu}(x)}
       {\sin \nu\pi },
  & \mbox{for $x \ge 0$ and non-integral $\nu$}
  \\
  \\
  \displaystyle
  \lim_{\mu \rightarrow \nu} \frac{\mathsf{J}_\mu(x) \cos \mu\pi - \mathsf{J}_{-\mu}(x)}
                                {\sin \mu\pi },
  & \mbox{for $x \ge 0$ and integral $\nu$}
  \end{array}
  \right.$$ where $\nu$ is `nu` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `nu >= 128`.

See also [[sf.cmath.cyl_bessel_j]].

#### Incomplete elliptic integral of the first kind <a id="sf.cmath.ellint_1">[[sf.cmath.ellint_1]]</a>

``` cpp
double       ellint_1(double k, double phi);
float        ellint_1f(float k, float phi);
long double  ellint_1l(long double k, long double phi);
```

*Effects:* These functions compute the incomplete elliptic integral of
the first kind of their respective arguments `k` and `phi` (`phi`
measured in radians).

*Returns:* $$%
  \mathsf{F}(k, \phi) =
  \int_0^\phi \! \frac{\mathsf{d}\theta}
                      {\sqrt{1 - k^2 \sin^2 \theta}},
       \quad \mbox{for $|k| \le 1$}$$ where k is `k` and φ is `phi`.

#### Incomplete elliptic integral of the second kind <a id="sf.cmath.ellint_2">[[sf.cmath.ellint_2]]</a>

``` cpp
double       ellint_2(double k, double phi);
float        ellint_2f(float k, float phi);
long double  ellint_2l(long double k, long double phi);
```

*Effects:* These functions compute the incomplete elliptic integral of
the second kind of their respective arguments `k` and `phi` (`phi`
measured in radians).

*Returns:* $$%
  \mathsf{E}(k, \phi) =
  \int_0^\phi \! \sqrt{1 - k^2 \sin^2 \theta} \, \mathsf{d}\theta,
       \quad \mbox{for $|k| \le 1$}$$ where k is `k` and φ is `phi`.

#### Incomplete elliptic integral of the third kind <a id="sf.cmath.ellint_3">[[sf.cmath.ellint_3]]</a>

``` cpp
double       ellint_3(double k, double nu, double phi);
float        ellint_3f(float k, float nu, float phi);
long double  ellint_3l(long double k, long double nu, long double phi);
```

*Effects:* These functions compute the incomplete elliptic integral of
the third kind of their respective arguments `k`, `nu`, and `phi` (`phi`
measured in radians).

*Returns:* $$%
  \mathsf{\Pi}(\nu, k, \phi) =
  \int_0^\phi \! \frac{ \mathsf{d}\theta }
                      { (1 - \nu \, \sin^2 \theta) \sqrt{1 - k^2 \sin^2 \theta} },
       \quad \mbox{for $|k| \le 1$}$$ where $\nu$ is `nu`, k is `k`, and
φ is `phi`.

#### Exponential integral <a id="sf.cmath.expint">[[sf.cmath.expint]]</a>

``` cpp
double       expint(double x);
float        expintf(float x);
long double  expintl(long double x);
```

*Effects:* These functions compute the exponential integral of their
respective arguments `x`.

*Returns:* $$%
  \mathsf{Ei}(x) =
  - \int_{-x}^\infty \frac{e^{-t}}
                          {t     } \, \mathsf{d}t
\;$$ where x is `x`.

#### Hermite polynomials <a id="sf.cmath.hermite">[[sf.cmath.hermite]]</a>

``` cpp
double       hermite(unsigned n, double x);
float        hermitef(unsigned n, float x);
long double  hermitel(unsigned n, long double x);
```

*Effects:* These functions compute the Hermite polynomials of their
respective arguments `n` and `x`.

*Returns:* $$%
  \mathsf{H}_n(x) =
  (-1)^n e^{x^2} \frac{ \mathsf{d} ^n}
              { \mathsf{d}x^n} \, e^{-x^2}
\;$$ where n is `n` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

#### Laguerre polynomials <a id="sf.cmath.laguerre">[[sf.cmath.laguerre]]</a>

``` cpp
double       laguerre(unsigned n, double x);
float        laguerref(unsigned n, float x);
long double  laguerrel(unsigned n, long double x);
```

*Effects:* These functions compute the Laguerre polynomials of their
respective arguments `n` and `x`.

*Returns:* $$%
  \mathsf{L}_n(x) =
  \frac{e^x}{n!} \frac{ \mathsf{d} ^ n}
            { \mathsf{d}x ^ n} \, (x^n e^{-x}),
       \quad \mbox{for $x \ge 0$}$$ where n is `n` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

#### Legendre polynomials <a id="sf.cmath.legendre">[[sf.cmath.legendre]]</a>

``` cpp
double       legendre(unsigned l, double x);
float        legendref(unsigned l, float x);
long double  legendrel(unsigned l, long double x);
```

*Effects:* These functions compute the Legendre polynomials of their
respective arguments `l` and `x`.

*Returns:* $$%
  \mathsf{P}_\ell(x) =
  \frac{1}
       {2^\ell \, \ell!}
  \frac{ \mathsf{d} ^ \ell}
       { \mathsf{d}x ^ \ell} \, (x^2 - 1) ^ \ell,
       \quad \mbox{for $|x| \le 1$}$$ where l is `l` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `l >= 128`.

#### Riemann zeta function <a id="sf.cmath.riemann_zeta">[[sf.cmath.riemann_zeta]]</a>

``` cpp
double       riemann_zeta(double x);
float        riemann_zetaf(float x);
long double  riemann_zetal(long double x);
```

*Effects:* These functions compute the Riemann zeta function of their
respective arguments `x`.

*Returns:* $$%
  \mathsf{\zeta}(x) =
  \left\{
  \begin{array}{cl}
  \displaystyle
  \sum_{k=1}^\infty k^{-x},
  & \mbox{for $x > 1$}
  \\
  \\
  \displaystyle
  \frac{1}
    {1 - 2^{1-x}}
  \sum_{k=1}^\infty (-1)^{k-1} k^{-x},
  & \mbox{for $0 \le x \le 1$}
  \\
  \\
  \displaystyle
  2^x \pi^{x-1} \sin(\frac{\pi x}{2}) \, \Gamma(1-x) \, \zeta(1-x),
  & \mbox{for $x < 0$}
  \end{array}
  \right.
\;$$ where x is `x`.

#### Spherical Bessel functions of the first kind <a id="sf.cmath.sph_bessel">[[sf.cmath.sph_bessel]]</a>

``` cpp
double       sph_bessel(unsigned n, double x);
float        sph_besself(unsigned n, float x);
long double  sph_bessell(unsigned n, long double x);
```

*Effects:* These functions compute the spherical Bessel functions of the
first kind of their respective arguments `n` and `x`.

*Returns:* $$%
  \mathsf{j}_n(x) =
  (\pi/2x)^{1\!/\!2} \mathsf{J}_{n + 1\!/\!2}(x),
       \quad \mbox{for $x \ge 0$}$$ where n is `n` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

See also [[sf.cmath.cyl_bessel_j]].

#### Spherical associated Legendre functions <a id="sf.cmath.sph_legendre">[[sf.cmath.sph_legendre]]</a>

``` cpp
double       sph_legendre(unsigned l, unsigned m, double theta);
float        sph_legendref(unsigned l, unsigned m, float theta);
long double  sph_legendrel(unsigned l, unsigned m, long double theta);
```

*Effects:* These functions compute the spherical associated Legendre
functions of their respective arguments `l`, `m`, and `theta` (`theta`
measured in radians).

*Returns:* $$%
  \mathsf{Y}_\ell^m(\theta, 0)
\;$$ where $$%
  \mathsf{Y}_\ell^m(\theta, \phi) =
  (-1)^m \left[ \frac{(2 \ell + 1)}
                     {4 \pi}
            \frac{(\ell - m)!}
                 {(\ell + m)!}
         \right]^{1/2}
     \mathsf{P}_\ell^m
     ( \cos\theta ) e ^ {i m \phi},
       \quad \mbox{for $|m| \le \ell$}$$ and l is `l`, m is `m`, and θ
is `theta`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `l >= 128`.

See also [[sf.cmath.assoc_legendre]].

#### Spherical Neumann functions <a id="sf.cmath.sph_neumann">[[sf.cmath.sph_neumann]]</a>

``` cpp
double       sph_neumann(unsigned n, double x);
float        sph_neumannf(unsigned n, float x);
long double  sph_neumannl(unsigned n, long double x);
```

*Effects:* These functions compute the spherical Neumann functions, also
known as the spherical Bessel functions of the second kind, of their
respective arguments `n` and `x`.

*Returns:* $$%
  \mathsf{n}_n(x) =
  (\pi/2x)^{1\!/\!2} \mathsf{N}_{n + 1\!/\!2}(x),
       \quad \mbox{for $x \ge 0$}$$ where n is `n` and x is `x`.

*Remarks:* The effect of calling each of these functions is
*implementation-defined* if `n >= 128`.

See also [[sf.cmath.cyl_neumann]].

<!-- Link reference definitions -->
[accumulate]: #accumulate
[adjacent.difference]: #adjacent.difference
[algorithms]: algorithms.md#algorithms
[bad.alloc]: language.md#bad.alloc
[basic.fundamental]: basic.md#basic.fundamental
[basic.stc.thread]: basic.md#basic.stc.thread
[basic.types]: basic.md#basic.types
[c.math]: #c.math
[c.math.abs]: #c.math.abs
[c.math.fpclass]: #c.math.fpclass
[c.math.hypot3]: #c.math.hypot3
[c.math.rand]: #c.math.rand
[cfenv]: #cfenv
[cfenv.syn]: #cfenv.syn
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
[complex.ops]: #complex.ops
[complex.special]: #complex.special
[complex.syn]: #complex.syn
[complex.transcendentals]: #complex.transcendentals
[complex.value.ops]: #complex.value.ops
[cons.slice]: #cons.slice
[conv.prom]: conv.md#conv.prom
[cpp.pragma]: cpp.md#cpp.pragma
[cstdlib.syn]: language.md#cstdlib.syn
[dcl.array]: dcl.md#dcl.array
[dcl.init]: dcl.md#dcl.init
[exclusive.scan]: #exclusive.scan
[function.objects]: utilities.md#function.objects
[gslice.access]: #gslice.access
[gslice.array.assign]: #gslice.array.assign
[gslice.array.comp.assign]: #gslice.array.comp.assign
[gslice.array.fill]: #gslice.array.fill
[gslice.cons]: #gslice.cons
[implimits]: #implimits
[inclusive.scan]: #inclusive.scan
[indirect.array.assign]: #indirect.array.assign
[indirect.array.comp.assign]: #indirect.array.comp.assign
[indirect.array.fill]: #indirect.array.fill
[inner.product]: #inner.product
[input.iterators]: iterators.md#input.iterators
[input.output]: input.md#input.output
[iostate.flags]: input.md#iostate.flags
[istream.formatted]: input.md#istream.formatted
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[library.c]: library.md#library.c
[mask.array.assign]: #mask.array.assign
[mask.array.comp.assign]: #mask.array.comp.assign
[mask.array.fill]: #mask.array.fill
[numarray]: #numarray
[numeric.iota]: #numeric.iota
[numeric.ops]: #numeric.ops
[numeric.ops.gcd]: #numeric.ops.gcd
[numeric.ops.lcm]: #numeric.ops.lcm
[numeric.ops.overview]: #numeric.ops.overview
[numeric.requirements]: #numeric.requirements
[numerics]: #numerics
[numerics.defns]: #numerics.defns
[numerics.general]: #numerics.general
[output.iterators]: iterators.md#output.iterators
[partial.sum]: #partial.sum
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
[rand.eng.lcong]: #rand.eng.lcong
[rand.eng.mers]: #rand.eng.mers
[rand.eng.sub]: #rand.eng.sub
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
[reduce]: #reduce
[res.on.data.races]: library.md#res.on.data.races
[sf.cmath]: #sf.cmath
[sf.cmath.assoc_laguerre]: #sf.cmath.assoc_laguerre
[sf.cmath.assoc_legendre]: #sf.cmath.assoc_legendre
[sf.cmath.beta]: #sf.cmath.beta
[sf.cmath.comp_ellint_1]: #sf.cmath.comp_ellint_1
[sf.cmath.comp_ellint_2]: #sf.cmath.comp_ellint_2
[sf.cmath.comp_ellint_3]: #sf.cmath.comp_ellint_3
[sf.cmath.cyl_bessel_i]: #sf.cmath.cyl_bessel_i
[sf.cmath.cyl_bessel_j]: #sf.cmath.cyl_bessel_j
[sf.cmath.cyl_bessel_k]: #sf.cmath.cyl_bessel_k
[sf.cmath.cyl_neumann]: #sf.cmath.cyl_neumann
[sf.cmath.ellint_1]: #sf.cmath.ellint_1
[sf.cmath.ellint_2]: #sf.cmath.ellint_2
[sf.cmath.ellint_3]: #sf.cmath.ellint_3
[sf.cmath.expint]: #sf.cmath.expint
[sf.cmath.hermite]: #sf.cmath.hermite
[sf.cmath.laguerre]: #sf.cmath.laguerre
[sf.cmath.legendre]: #sf.cmath.legendre
[sf.cmath.riemann_zeta]: #sf.cmath.riemann_zeta
[sf.cmath.sph_bessel]: #sf.cmath.sph_bessel
[sf.cmath.sph_legendre]: #sf.cmath.sph_legendre
[sf.cmath.sph_neumann]: #sf.cmath.sph_neumann
[slice.access]: #slice.access
[slice.arr.assign]: #slice.arr.assign
[slice.arr.comp.assign]: #slice.arr.comp.assign
[slice.arr.fill]: #slice.arr.fill
[strings]: strings.md#strings
[tab:RandomDistribution]: #tab:RandomDistribution
[tab:RandomEngine]: #tab:RandomEngine
[tab:SeedSequence]: #tab:SeedSequence
[tab:UniformRandomBitGenerator]: #tab:UniformRandomBitGenerator
[tab:copyassignable]: #tab:copyassignable
[tab:copyconstructible]: #tab:copyconstructible
[tab:equalitycomparable]: #tab:equalitycomparable
[tab:iterator.input.requirements]: #tab:iterator.input.requirements
[tab:moveassignable]: #tab:moveassignable
[tab:moveconstructible]: #tab:moveconstructible
[tab:numerics.lib.summary]: #tab:numerics.lib.summary
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
[thread.thread.class]: thread.md#thread.thread.class
[transform.exclusive.scan]: #transform.exclusive.scan
[transform.inclusive.scan]: #transform.inclusive.scan
[transform.reduce]: #transform.reduce
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
[vector]: containers.md#vector

[^1]: In other words, value types. These include arithmetic types,
    pointers, the library class `complex`, and instantiations of
    `valarray` for value types.

[^2]: The name of this engine refers, in part, to a property of its
    period: For properly-selected values of the parameters, the period
    is closely related to a large Mersenne prime number.

[^3]: The parameter is intended to allow an implementation to
    differentiate between different sources of randomness.

[^4]: If a device has n states whose respective probabilities are
    P₀, …, Pₙ₋₁, the device entropy S is defined as  
    $S = - \sum_{i=0}^{n-1} P_i \cdot \log P_i$.

[^5]: b is introduced to avoid any attempt to produce more bits of
    randomness than can be held in `RealType`.

[^6]: The distribution corresponding to this probability density
    function is also known (with a possible change of variable) as the
    Gumbel Type I, the log-Weibull, or the Fisher-Tippett Type I
    distribution.

[^7]: Annex  [[implimits]] recommends a minimum number of recursively
    nested template instantiations. This requirement thus indirectly
    suggests a minimum allowable complexity for valarray expressions.

[^8]: The intent is to specify an array template that has the minimum
    functionality necessary to address aliasing ambiguities and the
    proliferation of temporaries. Thus, the `valarray` template is
    neither a matrix class nor a field class. However, it is a very
    useful building block for designing such classes.

[^9]: This default constructor is essential, since arrays of `valarray`
    may be useful. After initialization, the length of an empty array
    can be increased with the `resize` member function.

[^10]: This constructor is the preferred method for converting a C array
    to a `valarray` object.

[^11]: This copy constructor creates a distinct array rather than an
    alias. Implementations in which arrays share storage are permitted,
    but they shall implement a copy-on-reference mechanism to ensure
    that arrays are conceptually distinct.

[^12]: BLAS stands for *Basic Linear Algebra Subprograms.* C++programs
    may instantiate this class. See, for example, Dongarra, Du Croz,
    Duff, and Hammerling: *A set of Level 3 Basic Linear Algebra
    Subprograms*; Technical Report MCS-P1-0888, Argonne National
    Laboratory (USA), Mathematics and Computer Science Division, August,
    1988.

[^13]: The use of fully closed ranges is intentional.

[^14]: `accumulate` is similar to the APL reduction operator and Common
    Lisp reduce function, but it avoids the difficulty of defining the
    result of reduction on an empty sequence by always requiring an
    initial value.

[^15]: The use of fully closed ranges is intentional.

[^16]: The use of fully closed ranges is intentional.

[^17]: The use of fully closed ranges is intentional.

[^18]: A mathematical function is mathematically defined for a given set
    of argument values (a) if it is explicitly defined for that set of
    argument values, or (b) if its limiting value exists and does not
    depend on the direction of approach.
