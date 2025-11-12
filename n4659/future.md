This Clause describes features of the C++Standard that are specified for
compatibility with existing implementations.

These are deprecated features, where *deprecated* is defined as:
Normative for the current edition of this International Standard, but
having been identified as a candidate for removal from future revisions.
An implementation may declare library names and entities described in
this section with the `deprecated` attribute ( [[dcl.attr.deprecated]]).

## Redeclaration of `static constexpr` data members <a id="depr.static_constexpr">[[depr.static_constexpr]]</a>

For compatibility with prior C++ International Standards, a `constexpr`
static data member may be redundantly redeclared outside the class with
no initializer. This usage is deprecated.

[*Example 1*:

``` cpp
struct A {
  static constexpr int n = 5;  // definition (declaration in C++14)
};

constexpr int A::n;  // redundant declaration (definition in C++14)
```

— *end example*\]

## Implicit declaration of copy functions <a id="depr.impldec">[[depr.impldec]]</a>

The implicit definition of a copy constructor as defaulted is deprecated
if the class has a user-declared copy assignment operator or a
user-declared destructor. The implicit definition of a copy assignment
operator as defaulted is deprecated if the class has a user-declared
copy constructor or a user-declared destructor ( [[class.dtor]], 
[[class.copy]]). In a future revision of this International Standard,
these implicit definitions could become deleted ( [[dcl.fct.def]]).

## Deprecated exception specifications <a id="depr.except.spec">[[depr.except.spec]]</a>

The *noexcept-specifier* `throw()` is deprecated.

## C++standard library headers <a id="depr.cpp.headers">[[depr.cpp.headers]]</a>

For compatibility with prior C++International Standards, the C++standard
library provides headers `<ccomplex>` ( [[depr.ccomplex.syn]]),
`<cstdalign>` ( [[depr.cstdalign.syn]]), `<cstdbool>` (
[[depr.cstdbool.syn]]), and `<ctgmath>` ( [[depr.ctgmath.syn]]). The use
of these headers is deprecated.

### Header `<ccomplex>` synopsis <a id="depr.ccomplex.syn">[[depr.ccomplex.syn]]</a>

``` cpp
#include <complex>
```

The header `<ccomplex>` behaves as if it simply includes the header
`<complex>` ( [[complex.syn]]).

### Header `<cstdalign>` synopsis <a id="depr.cstdalign.syn">[[depr.cstdalign.syn]]</a>

``` cpp
#define __alignas_is_defined 1
```

The contents of the header `<cstdalign>` are the same as the C standard
library header `<stdalign.h>`, with the following changes: The header
`<cstdalign>` and the header `<stdalign.h>` shall not define a macro
named `alignas`.

ISO C 7.15.

### Header `<cstdbool>` synopsis <a id="depr.cstdbool.syn">[[depr.cstdbool.syn]]</a>

``` cpp
#define __bool_true_false_are_defined 1
```

The contents of the header `<cstdbool>` are the same as the C standard
library header `<stdbool.h>`, with the following changes: The header
`<cstdbool>` and the header `<stdbool.h>` shall not define macros named
`bool`, `true`, or `false`.

ISO C 7.18.

### Header `<ctgmath>` synopsis <a id="depr.ctgmath.syn">[[depr.ctgmath.syn]]</a>

``` cpp
#include <complex>
#include <cmath>
```

The header `<ctgmath>` simply includes the headers `<complex>` (
[[complex.syn]]) and `<cmath>` ( [[cmath.syn]]).

[*Note 1*: The overloads provided in C by type-generic macros are
already provided in `<complex>` and `<cmath>` by “sufficient” additional
overloads. — *end note*\]

## C standard library headers <a id="depr.c.headers">[[depr.c.headers]]</a>

For compatibility with the C standard library, the C++standard library
provides the *C headers* shown in Table  [[tab:future.c.headers]].

**Table: C headers**

|               |                |                |              |              |
| ------------- | -------------- | -------------- | ------------ | ------------ |
| `<assert.h>`  | `<inttypes.h>` | `<signal.h>`   | `<stdio.h>`  | `<wchar.h>`  |
| `<complex.h>` | `<iso646.h>`   | `<stdalign.h>` | `<stdlib.h>` | `<wctype.h>` |
| `<ctype.h>`   | `<limits.h>`   | `<stdarg.h>`   | `<string.h>` |              |
| `<errno.h>`   | `<locale.h>`   | `<stdbool.h>`  | `<tgmath.h>` |              |
| `<fenv.h>`    | `<math.h>`     | `<stddef.h>`   | `<time.h>`   |              |
| `<float.h>`   | `<setjmp.h>`   | `<stdint.h>`   | `<uchar.h>`  |              |


The header `<complex.h>` behaves as if it simply includes the header
`<ccomplex>`. The header `<tgmath.h>` behaves as if it simply includes
the header `<ctgmath>`.

Every other C header, each of which has a name of the form `name.h`,
behaves as if each name placed in the standard library namespace by the
corresponding `cname` header is placed within the global namespace
scope, except for the functions described in [[sf.cmath]], the
declaration of `std::byte` ( [[cstddef.syn]]), and the functions and
function templates described in [[support.types.byteops]]. It is
unspecified whether these names are first declared or defined within
namespace scope ( [[basic.scope.namespace]]) of the namespace `std` and
are then injected into the global namespace scope by explicit
*using-declaration*s ( [[namespace.udecl]]).

[*Example 1*: The header `<cstdlib>` assuredly provides its
declarations and definitions within the namespace `std`. It may also
provide these names within the global namespace. The header `<stdlib.h>`
assuredly provides the same declarations and definitions within the
global namespace, much as in the C Standard. It may also provide these
names within the namespace `std`. — *end example*\]

## `char*` streams <a id="depr.str.strstreams">[[depr.str.strstreams]]</a>

The header `<strstream>` defines three types that associate stream
buffers with character array objects and assist reading and writing such
objects.

### Class `strstreambuf` <a id="depr.strstreambuf">[[depr.strstreambuf]]</a>

``` cpp
namespace std {
  class strstreambuf : public basic_streambuf<char> {
  public:
    explicit strstreambuf(streamsize alsize_arg = 0);
    strstreambuf(void* (*palloc_arg)(size_t), void (*pfree_arg)(void*));
    strstreambuf(char* gnext_arg, streamsize n, char* pbeg_arg = 0);
    strstreambuf(const char* gnext_arg, streamsize n);

    strstreambuf(signed char* gnext_arg, streamsize n,
                 signed char* pbeg_arg = 0);
    strstreambuf(const signed char* gnext_arg, streamsize n);
    strstreambuf(unsigned char* gnext_arg, streamsize n,
                 unsigned char* pbeg_arg = 0);
    strstreambuf(const unsigned char* gnext_arg, streamsize n);

    virtual ~strstreambuf();

    void  freeze(bool freezefl = true);
    char* str();
    int   pcount();

  protected:
    int_type overflow (int_type c = EOF) override;
    int_type pbackfail(int_type c = EOF) override;
    int_type underflow() override;
    pos_type seekoff(off_type off, ios_base::seekdir way,
                     ios_base::openmode which
                      = ios_base::in | ios_base::out) override;
    pos_type seekpos(pos_type sp,
                     ios_base::openmode which
                      = ios_base::in | ios_base::out) override;
    streambuf* setbuf(char* s, streamsize n) override;

  private:
    using strstate = T1;              // exposition only
    static const strstate allocated;  // exposition only
    static const strstate constant;   // exposition only
    static const strstate dynamic;    // exposition only
    static const strstate frozen;     // exposition only
    strstate strmode;                 // exposition only
    streamsize alsize;                // exposition only
    void* (*palloc)(size_t);          // exposition only
    void (*pfree)(void*);             // exposition only
  };
}
```

The class `strstreambuf` associates the input sequence, and possibly the
output sequence, with an object of some *character* array type, whose
elements store arbitrary values. The array object has several
attributes.

[*Note 1*:

For the sake of exposition, these are represented as elements of a
bitmask type (indicated here as `T1`) called `strstate`. The elements
are:

- `allocated`, set when a dynamic array object has been allocated, and
  hence should be freed by the destructor for the `strstreambuf` object;
- `constant`, set when the array object has `const` elements, so the
  output sequence cannot be written;
- `dynamic`, set when the array object is allocated (or reallocated) as
  necessary to hold a character sequence that can change in length;
- `frozen`, set when the program has requested that the array object not
  be altered, reallocated, or freed.

— *end note*\]

[*Note 2*:

For the sake of exposition, the maintained data is presented here as:

- `strstate strmode`, the attributes of the array object associated with
  the `strstreambuf` object;
- `int alsize`, the suggested minimum size for a dynamic array object;
- `void* (*palloc)(size_t)`, points to the function to call to allocate
  a dynamic array object;
- `void (*pfree)(void*)`, points to the function to call to free a
  dynamic array object.

— *end note*\]

Each object of class `strstreambuf` has a *seekable area*, delimited by
the pointers `seeklow` and `seekhigh`. If `gnext` is a null pointer, the
seekable area is undefined. Otherwise, `seeklow` equals `gbeg` and
`seekhigh` is either `pend`, if `pend` is not a null pointer, or `gend`.

#### `strstreambuf` constructors <a id="depr.strstreambuf.cons">[[depr.strstreambuf.cons]]</a>

``` cpp
explicit strstreambuf(streamsize alsize_arg = 0);
```

*Effects:* Constructs an object of class `strstreambuf`, initializing
the base class with `streambuf()`. The postconditions of this function
are indicated in Table  [[tab:future.strstreambuf.effects]].

**Table: `strstreambuf(streamsize)` effects**

| Element   | Value          |
| --------- | -------------- |
| `strmode` | `dynamic`      |
| `alsize`  | `alsize_arg`   |
| `palloc`  | a null pointer |
| `pfree`   | a null pointer |

``` cpp
strstreambuf(void* (*palloc_arg)(size_t), void (*pfree_arg)(void*));
```

*Effects:* Constructs an object of class `strstreambuf`, initializing
the base class with `streambuf()`. The postconditions of this function
are indicated in Table  [[tab:future.strstreambuf1.effects]].

**Table: `strstreambuf(void* (*)(size_t), void (*)(void*))` effects**

| Element   | Value                |
| --------- | -------------------- |
| `strmode` | `dynamic`            |
| `alsize`  | an unspecified value |
| `palloc`  | `palloc_arg`         |
| `pfree`   | `pfree_arg`          |

``` cpp
strstreambuf(char* gnext_arg, streamsize n, char* pbeg_arg = 0);
strstreambuf(signed char* gnext_arg, streamsize n,
             signed char* pbeg_arg = 0);
strstreambuf(unsigned char* gnext_arg, streamsize n,
             unsigned char* pbeg_arg = 0);
```

*Effects:* Constructs an object of class `strstreambuf`, initializing
the base class with `streambuf()`. The postconditions of this function
are indicated in Table  [[tab:future.strstreambuf2.effects]].

**Table: `strstreambuf(charT*, streamsize, charT*)` effects**

| Element   | Value                |
| --------- | -------------------- |
| `strmode` | 0                    |
| `alsize`  | an unspecified value |
| `palloc`  | a null pointer       |
| `pfree`   | a null pointer       |


`gnext_arg` shall point to the first element of an array object whose
number of elements `N` is determined as follows:

- If `n > 0`, `N` is `n`.
- If `n == 0`, `N` is `std::strlen(gnext_arg)`.
- If `n < 0`, `N` is `INT_MAX`.[^1]

If `pbeg_arg` is a null pointer, the function executes:

``` cpp
setg(gnext_arg, gnext_arg, gnext_arg + N);
```

Otherwise, the function executes:

``` cpp
setg(gnext_arg, gnext_arg, pbeg_arg);
setp(pbeg_arg,  pbeg_arg + N);
```

``` cpp
strstreambuf(const char* gnext_arg, streamsize n);
strstreambuf(const signed char* gnext_arg, streamsize n);
strstreambuf(const unsigned char* gnext_arg, streamsize n);
```

*Effects:* Behaves the same as `strstreambuf((char*)gnext_arg,n)`,
except that the constructor also sets `constant` in `strmode`.

``` cpp
virtual ~strstreambuf();
```

*Effects:* Destroys an object of class `strstreambuf`. The function
frees the dynamically allocated array object only if
`(strmode & allocated) != 0` and
`(strmode & frozen) == 0`. ( [[depr.strstreambuf.virtuals]] describes
how a dynamically allocated array object is freed.)

#### Member functions <a id="depr.strstreambuf.members">[[depr.strstreambuf.members]]</a>

``` cpp
void freeze(bool freezefl = true);
```

*Effects:* If `strmode & dynamic` is nonzero, alters the freeze status
of the dynamic array object as follows:

- If `freezefl` is `true`, the function sets `frozen` in `strmode`.
- Otherwise, it clears `frozen` in `strmode`.

``` cpp
char* str();
```

*Effects:* Calls `freeze()`, then returns the beginning pointer for the
input sequence, `gbeg`.

*Remarks:* The return value can be a null pointer.

``` cpp
int pcount() const;
```

*Effects:* If the next pointer for the output sequence, `pnext`, is a
null pointer, returns zero. Otherwise, returns the current effective
length of the array object as the next pointer minus the beginning
pointer for the output sequence, `pnext - pbeg`.

#### `strstreambuf` overridden virtual functions <a id="depr.strstreambuf.virtuals">[[depr.strstreambuf.virtuals]]</a>

``` cpp
int_type overflow(int_type c = EOF) override;
```

*Effects:* Appends the character designated by `c` to the output
sequence, if possible, in one of two ways:

- If `c != EOF` and if either the output sequence has a write position
  available or the function makes a write position available (as
  described below), assigns `c` to `*pnext++`. Returns
  `(unsigned char)c`.
- If `c == EOF`, there is no character to append. Returns a value other
  than `EOF`.

Returns `EOF` to indicate failure.

*Remarks:* The function can alter the number of write positions
available as a result of any call.

To make a write position available, the function reallocates (or
initially allocates) an array object with a sufficient number of
elements `n` to hold the current array object (if any), plus at least
one additional write position. How many additional write positions are
made available is otherwise unspecified. [^2] If `palloc` is not a null
pointer, the function calls `(*palloc)(n)` to allocate the new dynamic
array object. Otherwise, it evaluates the expression `new charT[n]`. In
either case, if the allocation fails, the function returns `EOF`.
Otherwise, it sets `allocated` in `strmode`.

To free a previously existing dynamic array object whose first element
address is `p`: If `pfree` is not a null pointer, the function calls
`(*pfree)(p)`. Otherwise, it evaluates the expression `delete[]p`.

If `(strmode & dynamic) == 0`, or if `(strmode & frozen) != 0`, the
function cannot extend the array (reallocate it with greater length) to
make a write position available.

``` cpp
int_type pbackfail(int_type c = EOF) override;
```

Puts back the character designated by `c` to the input sequence, if
possible, in one of three ways:

- If `c != EOF`, if the input sequence has a putback position available,
  and if `(char)c == gnext[-1]`, assigns `gnext - 1` to `gnext`. Returns
  `c`.
- If `c != EOF`, if the input sequence has a putback position available,
  and if `strmode & constant` is zero, assigns `c` to `*`\dcr`gnext`.
  Returns `c`.
- If `c == EOF` and if the input sequence has a putback position
  available, assigns `gnext - 1` to `gnext`. Returns a value other than
  `EOF`.

Returns `EOF` to indicate failure.

*Remarks:* If the function can succeed in more than one of these ways,
it is unspecified which way is chosen. The function can alter the number
of putback positions available as a result of any call.

``` cpp
int_type underflow() override;
```

*Effects:* Reads a character from the *input sequence*, if possible,
without moving the stream position past it, as follows:

- If the input sequence has a read position available, the function
  signals success by returning `(unsigned char)*gnext`.
- Otherwise, if the current write next pointer `pnext` is not a null
  pointer and is greater than the current read end pointer `gend`, makes
  a *read position* available by assigning to `gend` a value greater
  than `gnext` and no greater than `pnext`. Returns
  `(unsigned char)*gnext`.

Returns `EOF` to indicate failure.

*Remarks:* The function can alter the number of read positions available
as a result of any call.

``` cpp
pos_type seekoff(off_type off, seekdir way, openmode which = in | out) override;
```

*Effects:* Alters the stream position within one of the controlled
sequences, if possible, as indicated in
Table  [[tab:future.seekoff.positioning]].

**Table: `seekoff` positioning**

| Conditions                                                                                                                     | Result                                            |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `(which & ios::in) != 0`                                                                                                       | positions the input sequence                      |
| `(which & ios::out) != 0`                                                                                                      | positions the output sequence                     |
| `(which & (ios::in |`<br> `ios::out)) == (ios::in |`<br> `ios::out))` and<br> `way ==` either<br> `ios::beg` or<br> `ios::end` | positions both the input and the output sequences |
| Otherwise                                                                                                                      | the positioning operation fails.                  |


For a sequence to be positioned, if its next pointer is a null pointer,
the positioning operation fails. Otherwise, the function determines
`newoff` as indicated in Table  [[tab:future.newoff.values]].

**Table: `newoff` values**

| Condition         | `newoff` Value                                                 |
| ----------------- | -------------------------------------------------------------- |
| `way == ios::beg` | 0                                                              |
| `way == ios::cur` | the next pointer minus the beginning pointer (`xnext - xbeg`). |
| `way == ios::end` | `seekhigh` minus the beginning pointer (`seekhigh - xbeg`).    |


If `(newoff + off) < (seeklow - xbeg)` or
`(seekhigh - xbeg) < (newoff + off)`, the positioning operation fails.
Otherwise, the function assigns `xbeg + newoff + off` to the next
pointer `xnext`.

*Returns:* `pos_type(newoff)`, constructed from the resultant offset
`newoff` (of type `off_type`), that stores the resultant stream
position, if possible. If the positioning operation fails, or if the
constructed object cannot represent the resultant stream position, the
return value is `pos_type(off_type(-1))`.

``` cpp
pos_type seekpos(pos_type sp, ios_base::openmode which
                  = ios_base::in | ios_base::out) override;
```

*Effects:* Alters the stream position within one of the controlled
sequences, if possible, to correspond to the stream position stored in
`sp` (as described below).

- If `(which & ios::in) != 0`, positions the input sequence.
- If `(which & ios::out) != 0`, positions the output sequence.
- If the function positions neither sequence, the positioning operation
  fails.

For a sequence to be positioned, if its next pointer is a null pointer,
the positioning operation fails. Otherwise, the function determines
`newoff` from `sp.offset()`:

- If `newoff` is an invalid stream position, has a negative value, or
  has a value greater than (`seekhigh - seeklow`), the positioning
  operation fails
- Otherwise, the function adds `newoff` to the beginning pointer `xbeg`
  and stores the result in the next pointer `xnext`.

*Returns:* `pos_type(newoff)`, constructed from the resultant offset
`newoff` (of type `off_type`), that stores the resultant stream
position, if possible. If the positioning operation fails, or if the
constructed object cannot represent the resultant stream position, the
return value is `pos_type(off_type(-1))`.

``` cpp
streambuf<char>* setbuf(char* s, streamsize n) override;
```

*Effects:* Implementation defined, except that `setbuf(0, 0)` has no
effect.

### Class `istrstream` <a id="depr.istrstream">[[depr.istrstream]]</a>

``` cpp
namespace std {
  class istrstream : public basic_istream<char> {
  public:
    explicit istrstream(const char* s);
    explicit istrstream(char* s);
    istrstream(const char* s, streamsize n);
    istrstream(char* s, streamsize n);
    virtual ~istrstream();

    strstreambuf* rdbuf() const;
    char* str();
  private:
    strstreambuf sb;  // exposition only
  };
}
```

The class `istrstream` supports the reading of objects of class
`strstreambuf`. It supplies a `strstreambuf` object to control the
associated array object. For the sake of exposition, the maintained data
is presented here as:

- `sb`, the `strstreambuf` object.

#### `istrstream` constructors <a id="depr.istrstream.cons">[[depr.istrstream.cons]]</a>

``` cpp
explicit istrstream(const char* s);
explicit istrstream(char* s);
```

*Effects:* Constructs an object of class `istrstream`, initializing the
base class with `istream(&sb)` and initializing `sb` with
`strstreambuf(s,0)`. `s` shall designate the first element of an NTBS.

``` cpp
istrstream(const char* s, streamsize n);
istrstream(char* s, streamsize n);
```

*Effects:* Constructs an object of class `istrstream`, initializing the
base class with `istream(&sb)` and initializing `sb` with
`strstreambuf(s,n)`. `s` shall designate the first element of an array
whose length is `n` elements, and `n` shall be greater than zero.

#### Member functions <a id="depr.istrstream.members">[[depr.istrstream.members]]</a>

``` cpp
strstreambuf* rdbuf() const;
```

*Returns:* `const_cast<strstreambuf*>(&sb)`.

``` cpp
char* str();
```

*Returns:* `rdbuf()->str()`.

### Class `ostrstream` <a id="depr.ostrstream">[[depr.ostrstream]]</a>

``` cpp
namespace std {
  class ostrstream : public basic_ostream<char> {
  public:
    ostrstream();
    ostrstream(char* s, int n, ios_base::openmode mode = ios_base::out);
    virtual ~ostrstream();

    strstreambuf* rdbuf() const;
    void freeze(bool freezefl = true);
    char* str();
    int pcount() const;
  private:
    strstreambuf sb;  // exposition only
  };
}
```

The class `ostrstream` supports the writing of objects of class
`strstreambuf`. It supplies a `strstreambuf` object to control the
associated array object. For the sake of exposition, the maintained data
is presented here as:

- `sb`, the `strstreambuf` object.

#### `ostrstream` constructors <a id="depr.ostrstream.cons">[[depr.ostrstream.cons]]</a>

``` cpp
ostrstream();
```

*Effects:* Constructs an object of class `ostrstream`, initializing the
base class with `ostream(&sb)` and initializing `sb` with
`strstreambuf()`.

``` cpp
ostrstream(char* s, int n, ios_base::openmode mode = ios_base::out);
```

*Effects:* Constructs an object of class `ostrstream`, initializing the
base class with `ostream(&sb)`, and initializing `sb` with one of two
constructors:

- If `(mode & app) == 0`, then `s` shall designate the first element of
  an array of `n` elements. The constructor is `strstreambuf(s, n, s)`.
- If `(mode & app) != 0`, then `s` shall designate the first element of
  an array of `n` elements that contains an NTBSwhose first element is
  designated by `s`. The constructor is
  `strstreambuf(s, n, s + std::strlen(s))`.[^3]

#### Member functions <a id="depr.ostrstream.members">[[depr.ostrstream.members]]</a>

``` cpp
strstreambuf* rdbuf() const;
```

*Returns:* `(strstreambuf*)&sb`.

``` cpp
void freeze(bool freezefl = true);
```

*Effects:* Calls `rdbuf()->freeze(freezefl)`.

``` cpp
char* str();
```

*Returns:* `rdbuf()->str()`.

``` cpp
int pcount() const;
```

*Returns:* `rdbuf()->pcount()`.

### Class `strstream` <a id="depr.strstream">[[depr.strstream]]</a>

``` cpp
namespace std {
  class strstream
    : public basic_iostream<char> {
  public:
    // Types
    using char_type = char;
    using int_type  = char_traits<char>::int_type;
    using pos_type  = char_traits<char>::pos_type;
    using off_type  = char_traits<char>::off_type;

    // constructors/destructor
    strstream();
    strstream(char* s, int n,
              ios_base::openmode mode = ios_base::in|ios_base::out);
    virtual ~strstream();

    // Members:
    strstreambuf* rdbuf() const;
    void freeze(bool freezefl = true);
    int pcount() const;
    char* str();

  private:
  strstreambuf sb;  // exposition only
  };
}
```

The class `strstream` supports reading and writing from objects of class
`strstreambuf`. It supplies a `strstreambuf` object to control the
associated array object. For the sake of exposition, the maintained data
is presented here as:

- `sb`, the `strstreambuf` object.

#### `strstream` constructors <a id="depr.strstream.cons">[[depr.strstream.cons]]</a>

``` cpp
strstream();
```

*Effects:* Constructs an object of class `strstream`, initializing the
base class with `iostream(&sb)`.

``` cpp
strstream(char* s, int n,
          ios_base::openmode mode = ios_base::in|ios_base::out);
```

*Effects:* Constructs an object of class `strstream`, initializing the
base class with `iostream(&sb)` and initializing `sb` with one of the
two constructors:

- If `(mode & app) == 0`, then `s` shall designate the first element of
  an array of `n` elements. The constructor is `strstreambuf(s,n,s)`.
- If `(mode & app) != 0`, then `s` shall designate the first element of
  an array of `n` elements that contains an NTBSwhose first element is
  designated by `s`. The constructor is
  `strstreambuf(s,n,s + std::strlen(s))`.

#### `strstream` destructor <a id="depr.strstream.dest">[[depr.strstream.dest]]</a>

``` cpp
virtual ~strstream();
```

*Effects:* Destroys an object of class `strstream`.

#### `strstream` operations <a id="depr.strstream.oper">[[depr.strstream.oper]]</a>

``` cpp
strstreambuf* rdbuf() const;
```

*Returns:* `&sb`.

``` cpp
void freeze(bool freezefl = true);
```

*Effects:* Calls `rdbuf()->freeze(freezefl)`.

``` cpp
char* str();
```

*Returns:* `rdbuf()->str()`.

``` cpp
int pcount() const;
```

*Returns:* `rdbuf()->pcount()`.

## `uncaught_exception` <a id="depr.uncaught">[[depr.uncaught]]</a>

The header `<exception>` has the following addition:

``` cpp
namespace std {
  bool uncaught_exception() noexcept;
}
```

``` cpp
bool uncaught_exception() noexcept;
```

*Returns:* `uncaught_exceptions() > 0`.

## Old adaptable function bindings <a id="depr.func.adaptor.binding">[[depr.func.adaptor.binding]]</a>

### Weak result types <a id="depr.weak.result_type">[[depr.weak.result_type]]</a>

A call wrapper ( [[func.def]]) may have a *weak result type*. If it
does, the type of its member type `result_type` is based on the type `T`
of the wrapper’s target object:

- if `T` is a pointer to function type, `result_type` shall be a synonym
  for the return type of `T`;
- if `T` is a pointer to member function, `result_type` shall be a
  synonym for the return type of `T`;
- if `T` is a class type and the *qualified-id* `T::result_type` is
  valid and denotes a type ( [[temp.deduct]]), then `result_type` shall
  be a synonym for `T::result_type`;
- otherwise `result_type` shall not be defined.

### Typedefs to support function binders <a id="depr.func.adaptor.typedefs">[[depr.func.adaptor.typedefs]]</a>

To enable old function adaptors to manipulate function objects that take
one or two arguments, many of the function objects in this International
Standard correspondingly provide *typedef-name*s `argument_type` and
`result_type` for function objects that take one argument and
`first_argument_type`, `second_argument_type`, and `result_type` for
function objects that take two arguments.

The following member names are defined in addition to names specified in
Clause  [[function.objects]]:

``` cpp
namespace std {
  template<class T> struct owner_less<shared_ptr<T>> {
    using result_type          = bool;
    using first_argument_type  = shared_ptr<T>;
    using second_argument_type = shared_ptr<T>;
  };

  template<class T> struct owner_less<weak_ptr<T>> {
    using result_type          = bool;
    using first_argument_type  = weak_ptr<T>;
    using second_argument_type = weak_ptr<T>;
  };

  template <class T> class reference_wrapper {
  public :
    using result_type          = see below; // not always defined
    using argument_type        = see below; // not always defined
    using first_argument_type  = see below; // not always defined
    using second_argument_type = see below; // not always defined
  };

  template <class T> struct plus {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct minus {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct multiplies {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct divides {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct modulus {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct negate {
    using argument_type = T;
    using result_type   = T;
  };

  template <class T> struct equal_to {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct not_equal_to {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct greater {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct less {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct greater_equal {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct less_equal {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct logical_and {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct logical_or {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = bool;
  };

  template <class T> struct logical_not {
    using argument_type = T;
    using result_type   = bool;
  };

  template <class T> struct bit_and {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct bit_or {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct bit_xor {
    using first_argument_type  = T;
    using second_argument_type = T;
    using result_type          = T;
  };

  template <class T> struct bit_not {
    using argument_type = T;
    using result_type   = T;
  };

  template<class R, class T1>
  class function<R(T1)> {
  public:
    using argument_type = T1;
  };

  template<class R, class T1, class T2>
  class function<R(T1, T2)> {
  public:
    using first_argument_type  = T1;
    using second_argument_type = T2;
  };
}
```

`reference_wrapper<T>` has a weak result type (
[[depr.weak.result_type]]). If `T` is a function type, `result_type`
shall be a synonym for the return type of `T`.

The template specialization `reference_wrapper<T>` shall define a nested
type named `argument_type` as a synonym for `T1` only if the type `T` is
any of the following:

- a function type or a pointer to function type taking one argument of
  type `T1`
- a pointer to member function `R T0::f()` cv (where cv represents the
  member function’s cv-qualifiers); the type `T1` is cv `T0*`
- a class type where the *qualified-id* `T::argument_type` is valid and
  denotes a type ( [[temp.deduct]]); the type `T1` is
  `T::argument_type`.

The template instantiation `reference_wrapper<T>` shall define two
nested types named `first_argument_type` and `second_argument_type` as
synonyms for `T1` and `T2`, respectively, only if the type `T` is any of
the following:

- a function type or a pointer to function type taking two arguments of
  types `T1` and `T2`
- a pointer to member function `R T0::f(T2)` cv (where cv represents the
  member function’s cv-qualifiers); the type `T1` is cv `T0*`
- a class type where the *qualified-id*s `T::first_argument_type` and
  `T::second_argument_type` are both valid and both denote types (
  [[temp.deduct]]); the type `T1` is `T::first_argument_type` and the
  type `T2` is `T::second_argument_type`.

All enabled specializations `hash<Key>` of `hash` ( [[unord.hash]])
provide two nested types, `result_type` and `argument_type`, which shall
be synonyms for `size_t` and `Key`, respectively.

The forwarding call wrapper `g` returned by a call to
`bind(f, bound_args...)` ( [[func.bind.bind]]) shall have a weak result
type ( [[depr.weak.result_type]]).

The forwarding call wrapper `g` returned by a call to
`bind<R>(f, bound_args...)` ( [[func.bind.bind]]) shall have a nested
type `result_type` defined as a synonym for `R`.

The simple call wrapper returned from a call to `mem_fn(pm)` shall have
a nested type `result_type` that is a synonym for the return type of
`pm` when `pm` is a pointer to member function.

The simple call wrapper returned from a call to `mem_fn(pm)` shall
define two nested types named `argument_type` and `result_type` as
synonyms for cv `T*` and `Ret`, respectively, when `pm` is a pointer to
member function with cv-qualifier cv and taking no arguments, where
`Ret` is `pm`'s return type.

The simple call wrapper returned from a call to `mem_fn(pm)` shall
define three nested types named `first_argument_type`,
`second_argument_type`, and `result_type` as synonyms for cv `T*`, `T1`,
and `Ret`, respectively, when `pm` is a pointer to member function with
cv-qualifier cv and taking one argument of type `T1`, where `Ret` is
`pm`'s return type.

The following member names are defined in addition to names specified in
Clause  [[containers]]:

``` cpp
namespace std {
  template <class Key, class T, class Compare, class Allocator>
  class map<Key, T, Compare, Allocator>::value_compare {
  public:
    using result_type          = bool;
    using first_argument_type  = value_type;
    using second_argument_type = value_type;
  };

  template <class Key, class T, class Compare, class Allocator>
  class multimap<Key, T, Compare, Allocator>::value_compare {
  public:
    using result_type          = bool;
    using first_argument_type  = value_type;
    using second_argument_type = value_type;
  };
}
```

### Negators <a id="depr.negators">[[depr.negators]]</a>

The header `<functional>` has the following additions:

``` cpp
namespace std {
  template <class Predicate> class unary_negate;
  template <class Predicate>
    constexpr unary_negate<Predicate> not1(const Predicate&);
  template <class Predicate> class binary_negate;
  template <class Predicate>
    constexpr binary_negate<Predicate> not2(const Predicate&);
}
```

Negators `not1` and `not2` take a unary and a binary predicate,
respectively, and return their logical negations ( [[expr.unary.op]]).

``` cpp
template <class Predicate>
class unary_negate {
public:
  constexpr explicit unary_negate(const Predicate& pred);
  constexpr bool operator()(const typename Predicate::argument_type& x) const;
  using argument_type = typename Predicate::argument_type;
  using result_type   = bool;
};
```

``` cpp
constexpr bool operator()(const typename Predicate::argument_type& x) const;
```

*Returns:* `!pred(x)`.

``` cpp
template <class Predicate>
   constexpr unary_negate<Predicate> not1(const Predicate& pred);
```

*Returns:* `unary_negate<Predicate>(pred)`.

``` cpp
template <class Predicate>
class binary_negate {
public:
  constexpr explicit binary_negate(const Predicate& pred);
  constexpr bool operator()(const typename Predicate::first_argument_type& x,
                            const typename Predicate::second_argument_type& y) const;
  using first_argument_type  = typename Predicate::first_argument_type;
  using second_argument_type = typename Predicate::second_argument_type;
  using result_type          = bool;

};
```

``` cpp
constexpr bool operator()(const typename Predicate::first_argument_type& x,
                          const typename Predicate::second_argument_type& y) const;
```

*Returns:* `!pred(x,y)`.

``` cpp
template <class Predicate>
  constexpr binary_negate<Predicate> not2(const Predicate& pred);
```

*Returns:* `binary_negate<Predicate>(pred)`.

## The default allocator <a id="depr.default.allocator">[[depr.default.allocator]]</a>

The following members and explicit class template specialization are
defined in addition to those specified in [[default.allocator]]:

``` cpp
namespace std {
  // specialize for void:
  template <> class allocator<void> {
  public:
    using value_type    = void;
    using pointer       = void*;
    using const_pointer = const void*;
    // reference-to-void members are impossible.

    template <class U> struct rebind { using other = allocator<U>; };
  };

  template <class T> class allocator {
   public:
    using size_type       = size_t;
    using difference_type = ptrdiff_t;
    using pointer         = T*;
    using const_pointer   = const T*;
    using reference       = T&;
    using const_reference = const T&;
    template <class U> struct rebind { using other = allocator<U>; };

    T* address(T& x) const noexcept;
    const T* address(const T& x) const noexcept;

    T* allocate(size_t n, const void* hint);

    template<class U, class... Args>
      void construct(U* p, Args&&... args);
    template <class U>
      void destroy(U* p);

    size_t max_size() const noexcept;
  };
}
```

``` cpp
T* address(T& x) const noexcept;
const T* address(const T& x) const noexcept;
```

*Returns:* `addressof(x)`.

``` cpp
T* allocate(size_t n, const void* hint);
```

*Returns:* A pointer to the initial element of an array of storage of
size `n` `* sizeof(T)`, aligned appropriately for objects of type `T`.
It is *implementation-defined* whether over-aligned types are
supported ( [[basic.align]]).

*Remarks:* The storage is obtained by calling
`::operator new(std::size_t)` ( [[new.delete]]), but it is unspecified
when or how often this function is called.

*Throws:* `bad_alloc` if the storage cannot be obtained.

``` cpp
template <class U, class... Args>
  void construct(U* p, Args&&... args);
```

*Effects:* As if by: `::new((void *)p) U(std::forward<Args>(args)...);`

``` cpp
template <class U>
  void destroy(U* p);
```

*Effects:* As if by `p->~U()`.

``` cpp
size_t max_size() const noexcept;
```

*Returns:* The largest value *N* for which the call `allocate(N, 0)`
might succeed.

## Raw storage iterator <a id="depr.storage.iterator">[[depr.storage.iterator]]</a>

The header `<memory>` has the following addition:

``` cpp
namespace std {
  template <class OutputIterator, class T>
  class raw_storage_iterator {
  public:
    using iterator_category = output_iterator_tag;
    using value_type        = void;
    using difference_type   = void;
    using pointer           = void;
    using reference         = void;

    explicit raw_storage_iterator(OutputIterator x);

    raw_storage_iterator& operator*();
    raw_storage_iterator& operator=(const T& element);
    raw_storage_iterator& operator=(T&& element);
    raw_storage_iterator& operator++();
    raw_storage_iterator  operator++(int);
    OutputIterator base() const;
  };
}
```

`raw_storage_iterator` is provided to enable algorithms to store their
results into uninitialized memory. The template parameter
`OutputIterator` is required to have its `operator*` return an object
for which `operator&` is defined and returns a pointer to `T`, and is
also required to satisfy the requirements of an output iterator (
[[output.iterators]]).

``` cpp
explicit raw_storage_iterator(OutputIterator x);
```

*Effects:* Initializes the iterator to point to the same value to which
`x` points.

``` cpp
raw_storage_iterator& operator*();
```

*Returns:* `*this`

``` cpp
raw_storage_iterator& operator=(const T& element);
```

*Requires:* `T` shall be `CopyConstructible`.

*Effects:* Constructs a value from `element` at the location to which
the iterator points.

*Returns:* A reference to the iterator.

``` cpp
raw_storage_iterator& operator=(T&& element);
```

*Requires:* `T` shall be `MoveConstructible`.

*Effects:* Constructs a value from `std::move(element)` at the location
to which the iterator points.

*Returns:* A reference to the iterator.

``` cpp
raw_storage_iterator& operator++();
```

*Effects:* Pre-increment: advances the iterator and returns a reference
to the updated iterator.

``` cpp
raw_storage_iterator operator++(int);
```

*Effects:* Post-increment: advances the iterator and returns the old
value of the iterator.

``` cpp
OutputIterator base() const;
```

*Returns:* An iterator of type `OutputIterator` that points to the same
value as `*this` points to.

## Temporary buffers <a id="depr.temporary.buffer">[[depr.temporary.buffer]]</a>

The header `<memory>` has the following additions:

``` cpp
namespace std {
  template <class T>
    pair<T*, ptrdiff_t> get_temporary_buffer(ptrdiff_t n) noexcept;
  template <class T>
    void return_temporary_buffer(T* p);
}
```

``` cpp
template <class T>
  pair<T*, ptrdiff_t> get_temporary_buffer(ptrdiff_t n) noexcept;
```

*Effects:* Obtains a pointer to uninitialized, contiguous storage for N
adjacent objects of type `T`, for some non-negative number N. It is
*implementation-defined* whether over-aligned types are
supported ( [[basic.align]]).

*Remarks:* Calling `get_temporary_buffer` with a positive number `n` is
a non-binding request to return storage for `n` objects of type `T`. In
this case, an implementation is permitted to return instead storage for
a non-negative number N of such objects, where N` != n` (including
N` == 0`).

[*Note 1*: The request is non-binding to allow latitude for
implementation-specific optimizations of its memory
management. — *end note*\]

*Returns:* If `n <= 0` or if no storage could be obtained, returns a
pair `P` such that `P.first` is a null pointer value and
`P.second == 0`; otherwise returns a pair `P` such that `P.first` refers
to the address of the uninitialized storage and `P.second` refers to its
capacity N (in the units of `sizeof(T)`).

``` cpp
template <class T> void return_temporary_buffer(T* p);
```

*Effects:* Deallocates the storage referenced by `p`.

*Requires:* `p` shall be a pointer value returned by an earlier call to
`get_temporary_buffer` that has not been invalidated by an intervening
call to `return_temporary_buffer(T*)`.

*Throws:* Nothing.

## Deprecated type traits <a id="depr.meta.types">[[depr.meta.types]]</a>

The header `<type_traits>` has the following addition:

``` cpp
namespace std {
  template <class T> struct is_literal_type;

  template <class T> constexpr bool is_literal_type_v = is_literal_type<T>::value;

  template <class> struct result_of; // not defined
  template <class Fn, class... ArgTypes> struct result_of<Fn(ArgTypes...)>;

  template <class T> using result_of_t = typename result_of<T>::type;
}
```

*Requires:* For `is_literal_type`, `remove_all_extents_t<T>` shall be a
complete type or cv `void`. For `result_of<Fn(ArgTypes...)>`, `Fn` and
all types in the parameter pack `ArgTypes` shall be complete types,
cv `void`, or arrays of unknown bound.

`is_literal_type<T>` is a `UnaryTypeTrait` ( [[meta.rqmts]]) with a base
characteristic of `true_type` if `T` is a literal type (
[[basic.types]]), and `false_type` otherwise. The partial specialization
`result_of<Fn(ArgTypes...)>` is a `TransformationTrait` whose member
typedef `type` is defined if and only if
`invoke_result<Fn, ArgTypes...>::type` is defined. If `type` is defined,
it names the same type as `invoke_result_t<Fn, ArgTypes...>`.

The behavior of a program that adds specializations for
`is_literal_type` or `is_literal_type_v` is undefined.

## Deprecated iterator primitives <a id="depr.iterator.primitives">[[depr.iterator.primitives]]</a>

### Basic iterator <a id="depr.iterator.basic">[[depr.iterator.basic]]</a>

The header `<iterator>` has the following addition:

``` cpp
namespace std {
  template<class Category, class T, class Distance = ptrdiff_t,
    class Pointer = T*, class Reference = T&>
  struct iterator {
    using iterator_category = Category;
    using value_type        = T;
    using difference_type   = Distance;
    using pointer           = Pointer;
    using reference         = Reference;
  };
}
```

The `iterator` template may be used as a base class to ease the
definition of required types for new iterators.

[*Note 1*: If the new iterator type is a class template, then these
aliases will not be visible from within the iterator class’s template
definition, but only to callers of that class. — *end note*\]

[*Example 1*:

If a C++program wants to define a bidirectional iterator for some data
structure containing `double` and such that it works on a large memory
model of the implementation, it can do so with:

``` cpp
class MyIterator :
  public iterator<bidirectional_iterator_tag, double, long, T*, T&> {
  // code implementing ++, etc.
};
```

— *end example*\]

## Deprecated `shared_ptr` observers <a id="depr.util.smartptr.shared.obs">[[depr.util.smartptr.shared.obs]]</a>

The following member is defined in addition to those members specified
in [[util.smartptr.shared]]:

``` cpp
namespace std {
  template<class T> class shared_ptr {
  public:
    bool unique() const noexcept;
  };
}
```

``` cpp
bool unique() const noexcept;
```

*Returns:* `use_count() == 1`.

## Deprecated standard code conversion facets <a id="depr.locale.stdcvt">[[depr.locale.stdcvt]]</a>

The header `<codecvt>` provides code conversion facets for various
character encodings.

### Header `<codecvt>` synopsis <a id="depr.codecvt.syn">[[depr.codecvt.syn]]</a>

``` cpp
namespace std {
  enum codecvt_mode {
    consume_header = 4,
    generate_header = 2,
    little_endian = 1
  };

  template <class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = (codecvt_mode)0>
    class codecvt_utf8 : public codecvt<Elem, char, mbstate_t> {
    public:
      explicit codecvt_utf8(size_t refs = 0);
      ~codecvt_utf8();
    };

  template <class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = (codecvt_mode)0>
    class codecvt_utf16 : public codecvt<Elem, char, mbstate_t> {
    public:
      explicit codecvt_utf16(size_t refs = 0);
      ~codecvt_utf16();
    };

  template <class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = (codecvt_mode)0>
    class codecvt_utf8_utf16 : public codecvt<Elem, char, mbstate_t> {
    public:
      explicit codecvt_utf8_utf16(size_t refs = 0);
      ~codecvt_utf8_utf16();
    };
}
```

### Requirements <a id="depr.locale.stdcvt.req">[[depr.locale.stdcvt.req]]</a>

For each of the three code conversion facets `codecvt_utf8`,
`codecvt_utf16`, and `codecvt_utf8_utf16`:

- `Elem` is the wide-character type, such as `wchar_t`, `char16_t`, or
  `char32_t`.
- `Maxcode` is the largest wide-character code that the facet will read
  or write without reporting a conversion error.
- If `(Mode & consume_header)`, the facet shall consume an initial
  header sequence, if present, when reading a multibyte sequence to
  determine the endianness of the subsequent multibyte sequence to be
  read.
- If `(Mode & generate_header)`, the facet shall generate an initial
  header sequence when writing a multibyte sequence to advertise the
  endianness of the subsequent multibyte sequence to be written.
- If `(Mode & little_endian)`, the facet shall generate a multibyte
  sequence in little-endian order, as opposed to the default big-endian
  order.

For the facet `codecvt_utf8`:

- The facet shall convert between UTF-8 multibyte sequences and UCS2 or
  UCS4 (depending on the size of `Elem`) within the program.
- Endianness shall not affect how multibyte sequences are read or
  written.
- The multibyte sequences may be written as either a text or a binary
  file.

For the facet `codecvt_utf16`:

- The facet shall convert between UTF-16 multibyte sequences and UCS2 or
  UCS4 (depending on the size of `Elem`) within the program.
- Multibyte sequences shall be read or written according to the `Mode`
  flag, as set out above.
- The multibyte sequences may be written only as a binary file.
  Attempting to write to a text file produces undefined behavior.

For the facet `codecvt_utf8_utf16`:

- The facet shall convert between UTF-8 multibyte sequences and UTF-16
  (one or two 16-bit codes) within the program.
- Endianness shall not affect how multibyte sequences are read or
  written.
- The multibyte sequences may be written as either a text or a binary
  file.

ISO/IEC 10646-1:1993.

## Deprecated convenience conversion interfaces <a id="depr.conversions">[[depr.conversions]]</a>

The header `<locale>` has the following additions:

``` cpp
namespace std {
  template <class Codecvt, class Elem = wchar_t,
            class Wide_alloc = allocator<Elem>,
            class Byte_alloc = allocator<char>>
    class wstring_convert;

  template <class Codecvt, class Elem = wchar_t,
            class Tr = char_traits<Elem>>
    class wbuffer_convert;
}
```

### Class template `wstring_convert` <a id="depr.conversions.string">[[depr.conversions.string]]</a>

Class template `wstring_convert` performs conversions between a wide
string and a byte string. It lets you specify a code conversion facet
(like class template `codecvt`) to perform the conversions, without
affecting any streams or locales.

[*Example 1*:

If you want to use the code conversion facet `codecvt_utf8` to output to
`cout` a UTF-8 multibyte sequence corresponding to a wide string, but
you don’t want to alter the locale for `cout`, you can write something
like:

``` cpp
wstring_convert<std::codecvt_utf8<wchar_t>> myconv;
std::string mbstring = myconv.to_bytes(L"Hello\n");
std::cout << mbstring;
```

— *end example*\]

``` cpp
namespace std {
  template <class Codecvt, class Elem = wchar_t,
            class Wide_alloc = allocator<Elem>,
            class Byte_alloc = allocator<char>>
    class wstring_convert {
    public:
      using byte_string = basic_string<char, char_traits<char>, Byte_alloc>;
      using wide_string = basic_string<Elem, char_traits<Elem>, Wide_alloc>;
      using state_type  = typename Codecvt::state_type;
      using int_type    = typename wide_string::traits_type::int_type;

      explicit wstring_convert(Codecvt* pcvt = new Codecvt);
      wstring_convert(Codecvt* pcvt, state_type state);
      explicit wstring_convert(const byte_string& byte_err,
                               const wide_string& wide_err = wide_string());
      ~wstring_convert();

      wstring_convert(const wstring_convert&) = delete;
      wstring_convert& operator=(const wstring_convert&) = delete;

      wide_string from_bytes(char byte);
      wide_string from_bytes(const char* ptr);
      wide_string from_bytes(const byte_string& str);
      wide_string from_bytes(const char* first, const char* last);

      byte_string to_bytes(Elem wchar);
      byte_string to_bytes(const Elem* wptr);
      byte_string to_bytes(const wide_string& wstr);
      byte_string to_bytes(const Elem* first, const Elem* last);

      size_t converted() const noexcept;
      state_type state() const;

    private:
      byte_string byte_err_string;  // exposition only
      wide_string wide_err_string;  // exposition only
      Codecvt* cvtptr;              // exposition only
      state_type cvtstate;          // exposition only
      size_t cvtcount;              // exposition only
    };
}
```

The class template describes an object that controls conversions between
wide string objects of class `basic_string<Elem, char_traits<Elem>,
Wide_alloc>` and byte string objects of class `basic_string<char,
char_traits<char>, Byte_alloc>`. The class template defines the types
`wide_string` and `byte_string` as synonyms for these two types.
Conversion between a sequence of `Elem` values (stored in a
`wide_string` object) and multibyte sequences (stored in a `byte_string`
object) is performed by an object of class `Codecvt`, which meets the
requirements of the standard code-conversion facet `codecvt<Elem,
char, mbstate_t>`.

An object of this class template stores:

- `byte_err_string` — a byte string to display on errors
- `wide_err_string` — a wide string to display on errors
- `cvtptr` — a pointer to the allocated conversion object (which is
  freed when the `wstring_convert` object is destroyed)
- `cvtstate` — a conversion state object
- `cvtcount` — a conversion count

``` cpp
using byte_string = basic_string<char, char_traits<char>, Byte_alloc>;
```

The type shall be a synonym for
`basic_string<char, char_traits<char>, Byte_alloc>`.

``` cpp
size_t converted() const noexcept;
```

*Returns:* `cvtcount`.

``` cpp
wide_string from_bytes(char byte);
wide_string from_bytes(const char* ptr);
wide_string from_bytes(const byte_string& str);
wide_string from_bytes(const char* first, const char* last);
```

*Effects:* The first member function shall convert the single-element
sequence `byte` to a wide string. The second member function shall
convert the null-terminated sequence beginning at `ptr` to a wide
string. The third member function shall convert the sequence stored in
`str` to a wide string. The fourth member function shall convert the
sequence defined by the range \[`first`, `last`) to a wide string.

In all cases:

- If the `cvtstate` object was not constructed with an explicit value,
  it shall be set to its default value (the initial conversion state)
  before the conversion begins. Otherwise it shall be left unchanged.
- The number of input elements successfully converted shall be stored in
  `cvtcount`.

*Returns:* If no conversion error occurs, the member function shall
return the converted wide string. Otherwise, if the object was
constructed with a wide-error string, the member function shall return
the wide-error string. Otherwise, the member function throws an object
of class `range_error`.

``` cpp
using int_type = typename wide_string::traits_type::int_type;
```

The type shall be a synonym for `wide_string::traits_type::int_type`.

``` cpp
state_type state() const;
```

returns `cvtstate`.

``` cpp
using state_type = typename Codecvt::state_type;
```

The type shall be a synonym for `Codecvt::state_type`.

``` cpp
byte_string to_bytes(Elem wchar);
byte_string to_bytes(const Elem* wptr);
byte_string to_bytes(const wide_string& wstr);
byte_string to_bytes(const Elem* first, const Elem* last);
```

*Effects:* The first member function shall convert the single-element
sequence `wchar` to a byte string. The second member function shall
convert the null-terminated sequence beginning at `wptr` to a byte
string. The third member function shall convert the sequence stored in
`wstr` to a byte string. The fourth member function shall convert the
sequence defined by the range \[`first`, `last`) to a byte string.

In all cases:

- If the `cvtstate` object was not constructed with an explicit value,
  it shall be set to its default value (the initial conversion state)
  before the conversion begins. Otherwise it shall be left unchanged.
- The number of input elements successfully converted shall be stored in
  `cvtcount`.

*Returns:* If no conversion error occurs, the member function shall
return the converted byte string. Otherwise, if the object was
constructed with a byte-error string, the member function shall return
the byte-error string. Otherwise, the member function shall throw an
object of class `range_error`.

``` cpp
using wide_string = basic_string<Elem, char_traits<Elem>, Wide_alloc>;
```

The type shall be a synonym for
`basic_string<Elem, char_traits<Elem>, Wide_alloc>`.

``` cpp
explicit wstring_convert(Codecvt* pcvt = new Codecvt);
wstring_convert(Codecvt* pcvt, state_type state);
explicit wstring_convert(const byte_string& byte_err,
    const wide_string& wide_err = wide_string());
```

*Requires:* For the first and second constructors, `pcvt != nullptr`.

*Effects:* The first constructor shall store `pcvt` in `cvtptr` and
default values in `cvtstate`, `byte_err_string`, and `wide_err_string`.
The second constructor shall store `pcvt` in `cvtptr`, `state` in
`cvtstate`, and default values in `byte_err_string` and
`wide_err_string`; moreover the stored state shall be retained between
calls to `from_bytes` and `to_bytes`. The third constructor shall store
`new Codecvt` in `cvtptr`, `state_type()` in `cvtstate`, `byte_err` in
`byte_err_string`, and `wide_err` in `wide_err_string`.

``` cpp
~wstring_convert();
```

*Effects:* The destructor shall delete `cvtptr`.

### Class template `wbuffer_convert` <a id="depr.conversions.buffer">[[depr.conversions.buffer]]</a>

Class template `wbuffer_convert` looks like a wide stream buffer, but
performs all its I/O through an underlying byte stream buffer that you
specify when you construct it. Like class template `wstring_convert`, it
lets you specify a code conversion facet to perform the conversions,
without affecting any streams or locales.

``` cpp
namespace std {
  template <class Codecvt, class Elem = wchar_t, class Tr = char_traits<Elem>>
    class wbuffer_convert : public basic_streambuf<Elem, Tr> {
    public:
      using state_type = typename Codecvt::state_type;

      explicit wbuffer_convert(streambuf* bytebuf = 0,
                               Codecvt* pcvt = new Codecvt,
                               state_type state = state_type());

      ~wbuffer_convert();

      wbuffer_convert(const wbuffer_convert&) = delete;
      wbuffer_convert& operator=(const wbuffer_convert&) = delete;

      streambuf* rdbuf() const;
      streambuf* rdbuf(streambuf* bytebuf);

      state_type state() const;

    private:
      streambuf* bufptr;            // exposition only
      Codecvt* cvtptr;              // exposition only
      state_type cvtstate;          // exposition only
  };
}
```

The class template describes a stream buffer that controls the
transmission of elements of type `Elem`, whose character traits are
described by the class `Tr`, to and from a byte stream buffer of type
`streambuf`. Conversion between a sequence of `Elem` values and
multibyte sequences is performed by an object of class `Codecvt`, which
shall meet the requirements of the standard code-conversion facet
`codecvt<Elem, char, mbstate_t>`.

An object of this class template stores:

- `bufptr` — a pointer to its underlying byte stream buffer
- `cvtptr` — a pointer to the allocated conversion object (which is
  freed when the `wbuffer_convert` object is destroyed)
- `cvtstate` — a conversion state object

``` cpp
state_type state() const;
```

*Returns:* `cvtstate`.

``` cpp
streambuf* rdbuf() const;
```

*Returns:* `bufptr`.

``` cpp
streambuf* rdbuf(streambuf* bytebuf);
```

*Effects:* Stores `bytebuf` in `bufptr`.

*Returns:* The previous value of `bufptr`.

``` cpp
using state_type = typename Codecvt::state_type;
```

The type shall be a synonym for `Codecvt::state_type`.

``` cpp
explicit wbuffer_convert(
    streambuf* bytebuf = 0,
    Codecvt* pcvt = new Codecvt,
    state_type state = state_type());
```

*Requires:* `pcvt != nullptr`.

*Effects:* The constructor constructs a stream buffer object,
initializes `bufptr` to `bytebuf`, initializes `cvtptr` to `pcvt`, and
initializes `cvtstate` to `state`.

``` cpp
~wbuffer_convert();
```

*Effects:* The destructor shall delete `cvtptr`.

<!-- Section link definitions -->
[depr.c.headers]: #depr.c.headers
[depr.ccomplex.syn]: #depr.ccomplex.syn
[depr.codecvt.syn]: #depr.codecvt.syn
[depr.conversions]: #depr.conversions
[depr.conversions.buffer]: #depr.conversions.buffer
[depr.conversions.string]: #depr.conversions.string
[depr.cpp.headers]: #depr.cpp.headers
[depr.cstdalign.syn]: #depr.cstdalign.syn
[depr.cstdbool.syn]: #depr.cstdbool.syn
[depr.ctgmath.syn]: #depr.ctgmath.syn
[depr.default.allocator]: #depr.default.allocator
[depr.except.spec]: #depr.except.spec
[depr.func.adaptor.binding]: #depr.func.adaptor.binding
[depr.func.adaptor.typedefs]: #depr.func.adaptor.typedefs
[depr.impldec]: #depr.impldec
[depr.istrstream]: #depr.istrstream
[depr.istrstream.cons]: #depr.istrstream.cons
[depr.istrstream.members]: #depr.istrstream.members
[depr.iterator.basic]: #depr.iterator.basic
[depr.iterator.primitives]: #depr.iterator.primitives
[depr.locale.stdcvt]: #depr.locale.stdcvt
[depr.locale.stdcvt.req]: #depr.locale.stdcvt.req
[depr.meta.types]: #depr.meta.types
[depr.negators]: #depr.negators
[depr.ostrstream]: #depr.ostrstream
[depr.ostrstream.cons]: #depr.ostrstream.cons
[depr.ostrstream.members]: #depr.ostrstream.members
[depr.static_constexpr]: #depr.static_constexpr
[depr.storage.iterator]: #depr.storage.iterator
[depr.str.strstreams]: #depr.str.strstreams
[depr.strstream]: #depr.strstream
[depr.strstream.cons]: #depr.strstream.cons
[depr.strstream.dest]: #depr.strstream.dest
[depr.strstream.oper]: #depr.strstream.oper
[depr.strstreambuf]: #depr.strstreambuf
[depr.strstreambuf.cons]: #depr.strstreambuf.cons
[depr.strstreambuf.members]: #depr.strstreambuf.members
[depr.strstreambuf.virtuals]: #depr.strstreambuf.virtuals
[depr.temporary.buffer]: #depr.temporary.buffer
[depr.uncaught]: #depr.uncaught
[depr.util.smartptr.shared.obs]: #depr.util.smartptr.shared.obs
[depr.weak.result_type]: #depr.weak.result_type

<!-- Link reference definitions -->
[basic.align]: basic.md#basic.align
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.types]: basic.md#basic.types
[class.copy]: special.md#class.copy
[class.dtor]: special.md#class.dtor
[cmath.syn]: numerics.md#cmath.syn
[complex.syn]: numerics.md#complex.syn
[containers]: containers.md#containers
[cstddef.syn]: language.md#cstddef.syn
[dcl.attr.deprecated]: dcl.md#dcl.attr.deprecated
[dcl.fct.def]: dcl.md#dcl.fct.def
[default.allocator]: utilities.md#default.allocator
[depr.ccomplex.syn]: #depr.ccomplex.syn
[depr.cstdalign.syn]: #depr.cstdalign.syn
[depr.cstdbool.syn]: #depr.cstdbool.syn
[depr.ctgmath.syn]: #depr.ctgmath.syn
[depr.strstreambuf.virtuals]: #depr.strstreambuf.virtuals
[depr.weak.result_type]: #depr.weak.result_type
[expr.unary.op]: expr.md#expr.unary.op
[func.bind.bind]: utilities.md#func.bind.bind
[func.def]: utilities.md#func.def
[function.objects]: utilities.md#function.objects
[meta.rqmts]: utilities.md#meta.rqmts
[namespace.udecl]: dcl.md#namespace.udecl
[new.delete]: language.md#new.delete
[output.iterators]: iterators.md#output.iterators
[sf.cmath]: numerics.md#sf.cmath
[support.types.byteops]: language.md#support.types.byteops
[tab:future.c.headers]: #tab:future.c.headers
[tab:future.newoff.values]: #tab:future.newoff.values
[tab:future.seekoff.positioning]: #tab:future.seekoff.positioning
[tab:future.strstreambuf.effects]: #tab:future.strstreambuf.effects
[tab:future.strstreambuf1.effects]: #tab:future.strstreambuf1.effects
[tab:future.strstreambuf2.effects]: #tab:future.strstreambuf2.effects
[temp.deduct]: temp.md#temp.deduct
[unord.hash]: utilities.md#unord.hash
[util.smartptr.shared]: utilities.md#util.smartptr.shared

[^1]: The function signature `strlen(const char*)` is declared in
    `<cstring>` (@@REF:cstring.syn@@). The macro `INT_MAX` is defined in
    `<climits>` (@@REF:climits.syn@@).

[^2]: An implementation should consider `alsize` in making this
    decision.

[^3]: The function signature `strlen(const char*)` is declared in
    `<cstring>` (@@REF:cstring.syn@@).
