# Compatibility features (normative) <a id="depr" data-annex="true" data-annex-type="normative">[[depr]]</a>

This Clause describes features of the C++Standard that are specified for
compatibility with existing implementations.

These are deprecated features, where *deprecated* is defined as:
Normative for the current edition of the Standard, but not guaranteed to
be part of the Standard in future revisions.

## Increment operator with `bool` operand <a id="depr.incr.bool">[[depr.incr.bool]]</a>

The use of an operand of type `bool` with the `++` operator is
deprecated (see  [[expr.pre.incr]] and  [[expr.post.incr]]).

## `register` keyword <a id="depr.register">[[depr.register]]</a>

The use of the `register` keyword as a *storage-class-specifier* (
[[dcl.stc]]) is deprecated.

## Implicit declaration of copy functions <a id="depr.impldec">[[depr.impldec]]</a>

The implicit definition of a copy constructor as defaulted is deprecated
if the class has a user-declared copy assignment operator or a
user-declared destructor. The implicit definition of a copy assignment
operator as defaulted is deprecated if the class has a user-declared
copy constructor or a user-declared destructor ([[class.dtor]], 
[[class.copy]]). In a future revision of this International Standard,
these implicit definitions could become deleted ([[dcl.fct.def]]).

## Dynamic exception specifications <a id="depr.except.spec">[[depr.except.spec]]</a>

The use of *dynamic-exception-specification*s is deprecated.

## C standard library headers <a id="depr.c.headers">[[depr.c.headers]]</a>

For compatibility with the C standard library and the C Unicode TR, the
C++standard library provides the 25 *C headers*, as shown in Table 
[[tab:future.c.headers]].

**Table: C headers** <a id="tab:future.c.headers">[tab:future.c.headers]</a>

|               |                |                |              |              |
| ------------- | -------------- | -------------- | ------------ | ------------ |
| `<assert.h>`  | `<inttypes.h>` | `<signal.h>`   | `<stdio.h>`  | `<wchar.h>`  |
| `<complex.h>` | `<iso646.h>`   | `<stdalign.h>` | `<stdlib.h>` | `<wctype.h>` |
| `<ctype.h>`   | `<limits.h>`   | `<stdarg.h>`   | `<string.h>` |              |
| `<errno.h>`   | `<locale.h>`   | `<stdbool.h>`  | `<tgmath.h>` |              |
| `<fenv.h>`    | `<math.h>`     | `<stddef.h>`   | `<time.h>`   |              |
| `<float.h>`   | `<setjmp.h>`   | `<stdint.h>`   | `<uchar.h>`  |              |


Every C header, each of which has a name of the form `name.h`, behaves
as if each name placed in the standard library namespace by the
corresponding `cname` header is placed within the global namespace
scope. It is unspecified whether these names are first declared or
defined within namespace scope ([[basic.scope.namespace]]) of the
namespace `std` and are then injected into the global namespace scope by
explicit *using-declaration*s ([[namespace.udecl]]).

The header `<cstdlib>` assuredly provides its declarations and
definitions within the namespace `std`. It may also provide these names
within the global namespace. The header `<stdlib.h>` assuredly provides
the same declarations and definitions within the global namespace, much
as in the C Standard. It may also provide these names within the
namespace `std`.

## Old iostreams members <a id="depr.ios.members">[[depr.ios.members]]</a>

The following member names are in addition to names specified in Clause 
[[input.output]]:

``` cpp
namespace std {
  class ios_base {
  public:
    typedef T1 io_state;
    typedef T2 open_mode;
    typedef T3 seek_dir;
    typedef implementation-defined streamoff;
    typedef implementation-defined streampos;
    // remainder unchanged
  };
}
```

The type `io_state` is a synonym for an integer type (indicated here as
`T1` ) that permits certain member functions to overload others on
parameters of type `iostate` and provide the same behavior.

The type `open_mode` is a synonym for an integer type (indicated here as
`T2` ) that permits certain member functions to overload others on
parameters of type `openmode` and provide the same behavior.

The type `seek_dir` is a synonym for an integer type (indicated here as
`T3` ) that permits certain member functions to overload others on
parameters of type `seekdir` and provide the same behavior.

The type `streamoff` is an *implementation-defined* type that satisfies
the requirements of off_type in  [[iostreams.limits.pos]].

The type `streampos` is an *implementation-defined* type that satisfies
the requirements of pos_type in  [[iostreams.limits.pos]].

An implementation may provide the following additional member function,
which has the effect of calling `sbumpc()` ([[streambuf.pub.get]]):

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT> >
  class basic_streambuf {
  public:
    void stossc();
    // remainder unchanged
  };
}
```

An implementation may provide the following member functions that
overload signatures specified in Clause  [[input.output]]:

``` cpp
namespace std {
  template<class charT, class traits> class basic_ios {
  public:
    void clear(io_state state);
    void setstate(io_state state);
    void exceptions(io_state);
    // remainder unchanged
  };

  class ios_base {
  public:
    // remainder unchanged
  };

  template<class charT, class traits = char_traits<charT> >
  class basic_streambuf {
  public:
    pos_type pubseekoff(off_type off, ios_base::seek_dir way,
              ios_base::open_mode which = ios_base::in | ios_base::out);
    pos_type pubseekpos(pos_type sp,
              ios_base::open_mode which);
    // remainder unchanged
  };

  template <class charT, class traits = char_traits<charT> >
  class basic_filebuf : public basic_streambuf<charT,traits> {
  public:
    basic_filebuf<charT,traits>* open
    (const char* s, ios_base::open_mode mode);
    // remainder unchanged
  };

  template <class charT, class traits = char_traits<charT> >
  class basic_ifstream : public basic_istream<charT,traits> {
  public:
    void open(const char* s, ios_base::open_mode mode);
    // remainder unchanged
  };

  template <class charT, class traits = char_traits<charT> >
  class basic_ofstream : public basic_ostream<charT,traits> {
  public:
    void open(const char* s, ios_base::open_mode mode);
    // remainder unchanged
  };
}
```

The effects of these functions is to call the corresponding member
function specified in Clause  [[input.output]].

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
    virtual int_type overflow (int_type c = EOF);
    virtual int_type pbackfail(int_type c = EOF);
    virtual int_type underflow();
    virtual pos_type seekoff(off_type off, ios_base::seekdir way,
                             ios_base::openmode which
                               = ios_base::in | ios_base::out);
    virtual pos_type seekpos(pos_type sp, ios_base::openmode which
                               = ios_base::in | ios_base::out);
    virtual streambuf* setbuf(char* s, streamsize n);

  private:
    typedef T1 strstate;              // exposition onlyr
    static const strstate allocated;  //  exposition onlyr
    static const strstate constant;   // exposition onlyr
    static const strstate dynamic;    // exposition onlyr
    static const strstate frozen;     // exposition onlyr
    strstate strmode;                 // exposition onlyr
    streamsize alsize;                // exposition onlyr
    void* (*palloc)(size_t);          // exposition onlyr
    void (*pfree)(void*);             // exposition onlyr
  };
}
```

The class `strstreambuf` associates the input sequence, and possibly the
output sequence, with an object of some *character* array type, whose
elements store arbitrary values. The array object has several
attributes.

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

For the sake of exposition, the maintained data is presented here as:

- `strstate strmode`, the attributes of the array object associated with
  the `strstreambuf` object;
- `int alsize`, the suggested minimum size for a dynamic array object;
- `void* (*palloc(size_t)`, points to the function to call to allocate a
  dynamic array object;
- `void (*pfree)(void*)`, points to the function to call to free a
  dynamic array object.

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

**Table: `strstreambuf(streamsize)` effects** <a id="tab:future.strstreambuf.effects">[tab:future.strstreambuf.effects]</a>

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

**Table: `strstreambuf(void* (*)(size_t), void (*)(void*))` effects** <a id="tab:future.strstreambuf1.effects">[tab:future.strstreambuf1.effects]</a>

| Element   | Value                |
| --------- | -------------------- |
| `strmode` | `dynamic`            |
| `alsize`  | an unspecified value |
| `palloc`  | `palloc_arg`         |
| `pfree`   | `pfree_arg`          |

``` cpp
strstreambuf(char* gnext_arg, streamsize n, char *pbeg_arg = 0);
strstreambuf(signed char* gnext_arg, streamsize n,
             signed char *pbeg_arg = 0);
strstreambuf(unsigned char* gnext_arg, streamsize n,
             unsigned char *pbeg_arg = 0);
```

``` cpp
setg(gnext_arg, gnext_arg, gnext_arg + N);
```

``` cpp
virtual ~strstreambuf();
```

*Effects:* Destroys an object of class `strstreambuf`. The function
frees the dynamically allocated array object only if
`strmode & allocated != 0` and
`strmode & frozen == 0`. ([[depr.strstreambuf.virtuals]] describes how
a dynamically allocated array object is freed.)

#### Member functions <a id="depr.strstreambuf.members">[[depr.strstreambuf.members]]</a>

``` cpp
void freeze(bool freezefl = true);
```

*Effects:* If `strmode` & `dynamic` is non-zero, alters the freeze
status of the dynamic array object as follows:

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
pointer for the output sequence, `pnext` - `pbeg`.

#### `strstreambuf` overridden virtual functions <a id="depr.strstreambuf.virtuals">[[depr.strstreambuf.virtuals]]</a>

``` cpp
int_type overflow(int_type c = EOF);
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
made available is otherwise unspecified. [^1] If `palloc` is not a null
pointer, the function calls `(*palloc)(n)` to allocate the new dynamic
array object. Otherwise, it evaluates the expression `new charT[n]`. In
either case, if the allocation fails, the function returns `EOF`.
Otherwise, it sets `allocated` in `strmode`.

To free a previously existing dynamic array object whose first element
address is `p`: If `pfree` is not a null pointer, the function calls
`(*pfree)(p)`. Otherwise, it evaluates the expression `delete[]p`.

If `strmode & dynamic == 0`, or if `strmode & frozen != 0`, the function
cannot extend the array (reallocate it with greater length) to make a
write position available.

``` cpp
int_type pbackfail(int_type c = EOF);
```

Puts back the character designated by `c` to the input sequence, if
possible, in one of three ways:

- If `c != EOF`, if the input sequence has a putback position available,
  and if `(char)c == gnext[-1]`, assigns `gnext - 1` to `gnext`. Returns
  `c`.
- If `c != EOF`, if the input sequence has a putback position available,
  and if `strmode` & `constant` is zero, assigns `c` to `*`\dcr`gnext`.
  Returns `c`.
- If `c == EOF` and if the input sequence has a putback position
  available, assigns `gnext - 1` to `gnext`. Returns a value other than
  `EOF`.

Returns `EOF` to indicate failure.

*Remarks:* If the function can succeed in more than one of these ways,
it is unspecified which way is chosen. The function can alter the number
of putback positions available as a result of any call.

``` cpp
int_type underflow();
```

*Effects:* Reads a character from the *input sequence*, if possible,
without moving the stream position past it, as follows:

- If the input sequence has a read position available, the function
  signals success by returning `(unsigned char)*gnext`.
- Otherwise, if the current write next pointer `pnext` is not a null
  pointer and is greater than the current read end pointer `gend`, makes
  a *read position* available by assigning to `gend` a value greater
  than `gnext` and no greater than `pnext`. Returns
  `(unsigned char*)gnext`.

Returns `EOF` to indicate failure.

*Remarks:* The function can alter the number of read positions available
as a result of any call.

``` cpp
pos_type seekoff(off_type off, seekdir way, openmode which = in | out);
```

*Effects:* Alters the stream position within one of the controlled
sequences, if possible, as indicated in
Table  [[tab:future.seekoff.positioning]].

**Table: `seekoff` positioning** <a id="tab:future.seekoff.positioning">[tab:future.seekoff.positioning]</a>

| Conditions                                                                                                                     | Result                                            |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `(which & ios::in) != 0`                                                                                                       | positions the input sequence                      |
| `(which & ios::out) != 0`                                                                                                      | positions the output sequence                     |
| `(which & (ios::in |`<br> `ios::out)) == (ios::in |`<br> `ios::out))` and<br> `way ==` either<br> `ios::beg` or<br> `ios::end` | positions both the input and the output sequences |
| Otherwise                                                                                                                      | the positioning operation fails.                  |


For a sequence to be positioned, if its next pointer is a null pointer,
the positioning operation fails. Otherwise, the function determines
`newoff` as indicated in Table  [[tab:future.newoff.values]].

**Table: `newoff` values** <a id="tab:future.newoff.values">[tab:future.newoff.values]</a>

| Condition                                                                                       | `newoff` Value                                                 |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `way == ios::beg`                                                                               | 0                                                              |
| `way == ios::cur`                                                                               | the next pointer minus the beginning pointer (`xnext - xbeg`). |
| `way == ios::end`                                                                               | `seekhigh` minus the beginning pointer (`seekhigh - xbeg`).    |
| If `(newoff + off) <`<br> `(seeklow - xbeg)`,<br> or `(seekhigh - xbeg) <`<br> `(newoff + off)` | the positioning operation fails                                |


Otherwise, the function assigns `xbeg` + `newoff` + `off` to the next
pointer `xnext`.

*Returns:* `pos_type(newoff)`, constructed from the resultant offset
`newoff` (of type `off_type`), that stores the resultant stream
position, if possible. If the positioning operation fails, or if the
constructed object cannot represent the resultant stream position, the
return value is `pos_type(off_type(-1))`.

``` cpp
pos_type seekpos(pos_type sp, ios_base::openmode which
                  = ios_base::in | ios_base::out);
```

*Effects:* Alters the stream position within one of the controlled
sequences, if possible, to correspond to the stream position stored in
`sp` (as described below).

- If `(which & ios::in) != 0`, positions the input sequence.
- If `(which & ios::out) != 0`, positions the output sequence.
- If the function positions neither sequence, the positioning operation
  fails. For a sequence to be positioned, if its next pointer is a null
  pointer, the positioning operation fails. Otherwise, the function
  determines `newoff` from `sp.offset()`:
- If `newoff` is an invalid stream position, has a negative value, or
  has a value greater than (`seekhigh` - `seeklow`), the positioning
  operation fails
- Otherwise, the function adds `newoff` to the beginning pointer `xbeg`
  and stores the result in the next pointer `xnext`.

*Returns:* `pos_type(newoff)`, constructed from the resultant offset
`newoff` (of type `off_type`), that stores the resultant stream
position, if possible. If the positioning operation fails, or if the
constructed object cannot represent the resultant stream position, the
return value is `pos_type(off_type(-1))`.

``` cpp
streambuf<char>* setbuf(char* s, streamsize n);
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
    char *str();
  private:
    strstreambuf sb;  // exposition onlyr
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
`strstreambuf(s,0))`. `s` shall designate the first element of an NTBS.

``` cpp
istrstream(const char* s, streamsize n);
```

*Effects:* Constructs an object of class `istrstream`, initializing the
base class with `istream(&sb)` and initializing `sb` with
`strstreambuf(s,n))`. `s` shall designate the first element of an array
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
    strstreambuf sb;  // exposition onlyr
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
`strstreambuf())`.

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
  `strstreambuf(s, n, s + std::strlen(s))`.[^2]

#### Member functions <a id="depr.ostrstream.members">[[depr.ostrstream.members]]</a>

``` cpp
strstreambuf* rdbuf() const;
```

*Returns:* `(strstreambuf*)&sb `.

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
    typedef char                                char_type;
    typedef typename char_traits<char>::int_type int_type;
    typedef typename char_traits<char>::pos_type pos_type;
    typedef typename char_traits<char>::off_type off_type;

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
  strstreambuf sb;  // exposition onlyr
  };
}
```

The class `strstream` supports reading and writing from objects of
classs `strstreambuf.` It supplies a `strstreambuf` object to control
the associated array object. For the sake of exposition, the maintained
data is presented here as

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
virtual ~strstream()
```

*Effects:* Destroys an object of class `strstream`.

``` cpp
strstreambuf* rdbuf() const;
```

*Returns:* `&sb`.

#### `strstream` operations <a id="depr.strstream.oper">[[depr.strstream.oper]]</a>

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

## Function objects <a id="depr.function.objects">[[depr.function.objects]]</a>

### Base <a id="depr.base">[[depr.base]]</a>

The class templates `unary_function` and `binary_function` are
deprecated. A program shall not declare specializations of these
templates.

``` cpp
namespace std {
  template <class Arg, class Result>
  struct unary_function {
    typedef Arg    argument_type;
    typedef Result result_type;
  };
}
```

``` cpp
namespace std {
  template <class Arg1, class Arg2, class Result>
  struct binary_function {
    typedef Arg1   first_argument_type;
    typedef Arg2   second_argument_type;
    typedef Result result_type;
  };
}
```

### Function adaptors <a id="depr.adaptors">[[depr.adaptors]]</a>

The adaptors ptr_fun, mem_fun, mem_fun_ref, and their corresponding
return types are deprecated. The function template `bind`  [[func.bind]]
provides a better solution.

#### Adaptors for pointers to functions <a id="depr.function.pointer.adaptors">[[depr.function.pointer.adaptors]]</a>

To allow pointers to (unary and binary) functions to work with function
adaptors the library provides:

``` cpp
template <class Arg, class Result>
class pointer_to_unary_function : public unary_function<Arg, Result> {
public:
  explicit pointer_to_unary_function(Result (*f)(Arg));
  Result operator()(Arg x) const;
};
```

`operator()` returns `f(x)`.

``` cpp
template <class Arg, class Result>
  pointer_to_unary_function<Arg, Result> ptr_fun(Result (*f)(Arg));
```

*Returns:* `pointer_to_unary_function<Arg, Result>(f)`.

``` cpp
template <class Arg1, class Arg2, class Result>
class pointer_to_binary_function :
  public binary_function<Arg1,Arg2,Result> {
public:
  explicit pointer_to_binary_function(Result (*f)(Arg1, Arg2));
  Result operator()(Arg1 x, Arg2 y) const;
};
```

`operator()` returns `f(x,y)`.

``` cpp
template <class Arg1, class Arg2, class Result>
  pointer_to_binary_function<Arg1,Arg2,Result>
    ptr_fun(Result (*f)(Arg1, Arg2));
```

*Returns:* `pointer_to_binary_function<Arg1,Arg2,Result>(f)`.

``` cpp
int compare(const char*, const char*);
replace_if(v.begin(), v.end(),
  not1(bind2nd(ptr_fun(compare), "abc")), "def");
```

replaces each `abc` with `def` in sequence `v`.

#### Adaptors for pointers to members <a id="depr.member.pointer.adaptors">[[depr.member.pointer.adaptors]]</a>

The purpose of the following is to provide the same facilities for
pointer to members as those provided for pointers to functions in 
[[depr.function.pointer.adaptors]].

``` cpp
template <class S, class T> class mem_fun_t
        : public unary_function<T*, S> {
public:
  explicit mem_fun_t(S (T::*p)());
  S operator()(T* p) const;
};
```

`mem_fun_t` calls the member function it is initialized with given a
pointer argument.

``` cpp
template <class S, class T, class A> class mem_fun1_t
      : public binary_function<T*, A, S> {
public:
  explicit mem_fun1_t(S (T::*p)(A));
  S operator()(T* p, A x) const;
};
```

`mem_fun1_t` calls the member function it is initialized with given a
pointer argument and an additional argument of the appropriate type.

``` cpp
template<class S, class T> mem_fun_t<S,T>
   mem_fun(S (T::*f)());
template<class S, class T, class A> mem_fun1_t<S,T,A>
   mem_fun(S (T::*f)(A));
```

`mem_fun(&X::f)` returns an object through which `X::f` can be called
given a pointer to an `X` followed by the argument required for `f` (if
any).

``` cpp
template <class S, class T> class mem_fun_ref_t
      : public unary_function<T, S> {
public:
  explicit mem_fun_ref_t(S (T::*p)());
  S operator()(T& p) const;
};
```

`mem_fun_ref_t` calls the member function it is initialized with given a
reference argument.

``` cpp
template <class S, class T, class A> class mem_fun1_ref_t
      : public binary_function<T, A, S> {
public:
  explicit mem_fun1_ref_t(S (T::*p)(A));
  S operator()(T& p, A x) const;
};
```

`mem_fun1_ref_t` calls the member function it is initialized with given
a reference argument and an additional argument of the appropriate type.

``` cpp
template<class S, class T> mem_fun_ref_t<S,T>
   mem_fun_ref(S (T::*f)());
template<class S, class T, class A> mem_fun1_ref_t<S,T,A>
   mem_fun_ref(S (T::*f)(A));
```

`mem_fun_ref(&X::f)` returns an object through which `X::f` can be
called given a reference to an `X` followed by the argument required for
`f` (if any).

``` cpp
template <class S, class T> class const_mem_fun_t
      : public unary_function<const T*, S> {
public:
  explicit const_mem_fun_t(S (T::*p)() const);
  S operator()(const T* p) const;
};
```

`const_mem_fun_t` calls the member function it is initialized with given
a pointer argument.

``` cpp
template <class S, class T, class A> class const_mem_fun1_t
      : public binary_function<const T*, A, S> {
public:
  explicit const_mem_fun1_t(S (T::*p)(A) const);
  S operator()(const T* p, A x) const;
};
```

`const_mem_fun1_t` calls the member function it is initialized with
given a pointer argument and an additional argument of the appropriate
type.

``` cpp
template<class S, class T> const_mem_fun_t<S,T>
   mem_fun(S (T::*f)() const);
template<class S, class T, class A> const_mem_fun1_t<S,T,A>
   mem_fun(S (T::*f)(A) const);
```

`mem_fun(&X::f)` returns an object through which `X::f` can be called
given a pointer to an `X` followed by the argument required for `f` (if
any).

``` cpp
template <class S, class T> class const_mem_fun_ref_t
      : public unary_function<T, S> {
public:
  explicit const_mem_fun_ref_t(S (T::*p)() const);
  S operator()(const T& p) const;
};
```

`const_mem_fun_ref_t` calls the member function it is initialized with
given a reference argument.

``` cpp
template <class S, class T, class A> class const_mem_fun1_ref_t
      : public binary_function<T, A, S> {
public:
  explicit const_mem_fun1_ref_t(S (T::*p)(A) const);
  S operator()(const T& p, A x) const;
};
```

`const_mem_fun1_ref_t` calls the member function it is initialized with
given a reference argument and an additional argument of the appropriate
type.

``` cpp
template<class S, class T> const_mem_fun_ref_t<S,T>
   mem_fun_ref(S (T::*f)() const);
template<class S, class T, class A> const_mem_fun1_ref_t<S,T,A>
    mem_fun_ref(S (T::*f)(A) const);
```

`mem_fun_ref(&X::f)` returns an object through which `X::f` can be
called given a reference to an `X` followed by the argument required for
`f` (if any).

## Binders <a id="depr.lib.binders">[[depr.lib.binders]]</a>

The binders `binder1st`, `bind1st`, `binder2nd`, and `bind2nd` are
deprecated. The function template `bind` ([[bind]]) provides a better
solution.

### Class template `binder1st` <a id="depr.lib.binder.1st">[[depr.lib.binder.1st]]</a>

``` cpp
template <class Fn>
  class binder1st
    : public unary_function<typename Fn::second_argument_type,
                            typename Fn::result_type> {
  protected:
    Fn                      op;
    typename Fn::first_argument_type value;
  public:
    binder1st(const Fn& x,
              const typename Fn::first_argument_type& y);
    typename Fn::result_type
      operator()(const typename Fn::second_argument_type& x) const;
    typename Fn::result_type
      operator()(typename Fn::second_argument_type& x) const;
  };
```

The constructor initializes `op` with `x` and `value` with `y`.

`operator()` returns `op``(value,x)`.

### `bind1st` <a id="depr.lib.bind.1st">[[depr.lib.bind.1st]]</a>

``` cpp
template <class Fn, class T>
  binder1st<Fn> bind1st(const Fn& fn, const T& x);
```

*Returns:* `binder1st<Fn>(fn, typename Fn::first_argument_type(x))`.

### Class template `binder2nd` <a id="depr.lib.binder.2nd">[[depr.lib.binder.2nd]]</a>

``` cpp
template <class Fn>
  class binder2nd
    : public unary_function<typename Fn::first_argument_type,
                            typename Fn::result_type> {
  protected:
    Fn                       op;
    typename Fn::second_argument_type value;
  public:
    binder2nd(const Fn& x,
              const typename Fn::second_argument_type& y);
    typename Fn::result_type
      operator()(const typename Fn::first_argument_type& x) const;
    typename Fn::result_type
      operator()(typename Fn::first_argument_type& x) const;
  };
```

The constructor initializes `op` with `x` and `value` with `y`.

`operator()` returns `op``(x,value)`.

### `bind2nd` <a id="depr.lib.bind.2nd">[[depr.lib.bind.2nd]]</a>

``` cpp
template <class Fn, class T>
  binder2nd<Fn> bind2nd(const Fn& op, const T& x);
```

*Returns:* `binder2nd<Fn>(op, typename Fn::second_argument_type(x))`.

``` cpp
find_if(v.begin(), v.end(), bind2nd(greater<int>(), 5));
```

finds the first integer in vector `v` greater than 5;

``` cpp
find_if(v.begin(), v.end(), bind1st(greater<int>(), 5));
```

finds the first integer in `v` less than 5.

## `auto_ptr` <a id="depr.auto.ptr">[[depr.auto.ptr]]</a>

The class template `auto_ptr` is deprecated. The class template
`unique_ptr` ([[unique.ptr]]) provides a better solution.

### Class template `auto_ptr` <a id="auto.ptr">[[auto.ptr]]</a>

The class template `auto_ptr` stores a pointer to an object obtained via
`new` and deletes that object when it itself is destroyed (such as when
leaving block scope  [[stmt.dcl]]).

The class template `auto_ptr_ref` is for exposition only. An
implementation is permitted to provide equivalent functionality without
providing a template with this name. The template holds a reference to
an `auto_ptr`. It is used by the `auto_ptr` conversions to allow
`auto_ptr` objects to be passed to and returned from functions.

``` cpp
namespace std {
  template <class Y> struct auto_ptr_ref;   // exposition only

  template <class X> class auto_ptr {
  public:
    typedef X element_type;

    // [auto.ptr.cons] construct/copy/destroy:
    explicit auto_ptr(X* p =0) throw();
    auto_ptr(auto_ptr&) throw();
    template<class Y> auto_ptr(auto_ptr<Y>&) throw();
    auto_ptr& operator=(auto_ptr&) throw();
    template<class Y> auto_ptr& operator=(auto_ptr<Y>&) throw();
    auto_ptr& operator=(auto_ptr_ref<X> r) throw();
   ~auto_ptr() throw();

    // [auto.ptr.members] members:
    X& operator*() const throw();
    X* operator->() const throw();
    X* get() const throw();
    X* release() throw();
    void reset(X* p =0) throw();

    // [auto.ptr.conv] conversions:
    auto_ptr(auto_ptr_ref<X>) throw();
    template<class Y> operator auto_ptr_ref<Y>() throw();
    template<class Y> operator auto_ptr<Y>() throw();
  };

  template <> class auto_ptr<void>
  {
  public:
    typedef void element_type;
  };
}
```

The class template `auto_ptr` provides a semantics of strict ownership.
An `auto_ptr` owns the object it holds a pointer to. Copying an
`auto_ptr` copies the pointer and transfers ownership to the
destination. If more than one `auto_ptr` owns the same object at the
same time the behavior of the program is undefined. The uses of
`auto_ptr` include providing temporary exception-safety for dynamically
allocated memory, passing ownership of dynamically allocated memory to a
function, and returning dynamically allocated memory from a function.
Instances of `auto_ptr` meet the requirements of `MoveConstructible` and
`MoveAssignable`, but do not meet the requirements of
`CopyConstructible` and `CopyAssignable`.

#### `auto_ptr` constructors <a id="auto.ptr.cons">[[auto.ptr.cons]]</a>

``` cpp
explicit auto_ptr(X* p =0) throw();
```

*Postconditions:* `*this` holds the pointer `p`.

``` cpp
auto_ptr(auto_ptr& a) throw();
```

*Effects:* Calls `a.release()`.

*Postconditions:* `*this` holds the pointer returned from `a.release()`.

``` cpp
template<class Y> auto_ptr(auto_ptr<Y>& a) throw();
```

*Requires:* `Y*` can be implicitly converted to `X*`.

*Effects:* Calls `a.release()`.

*Postconditions:* `*this` holds the pointer returned from `a.release()`.

``` cpp
auto_ptr& operator=(auto_ptr& a) throw();
```

*Requires:* The expression `delete get()` is well formed.

*Effects:* `reset(a.release())`.

*Returns:* `*this`.

``` cpp
template<class Y> auto_ptr& operator=(auto_ptr<Y>& a) throw();
```

*Requires:* `Y*` can be implicitly converted to `X*`. The expression
`delete get()` is well formed.

*Effects:* `reset(a.release())`.

*Returns:* `*this`.

``` cpp
~auto_ptr() throw();
```

*Requires:* The expression `delete get()` is well formed.

*Effects:* `delete get()`.

#### `auto_ptr` members <a id="auto.ptr.members">[[auto.ptr.members]]</a>

``` cpp
X& operator*() const throw();
```

*Requires:* `get() != 0`

*Returns:* `*get()`

``` cpp
X* operator->() const throw();
```

*Returns:* `get()`

``` cpp
X* get() const throw();
```

*Returns:* The pointer `*this` holds.

``` cpp
X* release() throw();
```

*Returns:* `get()`

`*this` holds the null pointer.

``` cpp
void reset(X* p=0) throw();
```

*Effects:* If `get() != p` then `delete get()`.

*Postconditions:* `*this` holds the pointer `p`.

#### `auto_ptr` conversions <a id="auto.ptr.conv">[[auto.ptr.conv]]</a>

``` cpp
auto_ptr(auto_ptr_ref<X> r) throw();
```

*Effects:* Calls `p.release()` for the `auto_ptr` `p` that `r` holds.

*Postconditions:* `*this` holds the pointer returned from `release()`.

``` cpp
template<class Y> operator auto_ptr_ref<Y>() throw();
```

*Returns:* An `auto_ptr_ref<Y>` that holds `*this`.

``` cpp
template<class Y> operator auto_ptr<Y>() throw();
```

*Effects:* Calls `release()`.

*Returns:* An `auto_ptr<Y>` that holds the pointer returned from
`release()`.

``` cpp
auto_ptr& operator=(auto_ptr_ref<X> r) throw()
```

*Effects:* Calls `reset(p.release())` for the `auto_ptr p` that `r`
holds a reference to.

*Returns:* `*this`

## Violating *exception-specification*s <a id="exception.unexpected">[[exception.unexpected]]</a>

### Type `unexpected_handler` <a id="unexpected.handler">[[unexpected.handler]]</a>

``` cpp
typedef void (*unexpected_handler)();
```

The type of a *handler function* to be called by `unexpected()` when a
function attempts to throw an exception not listed in its
*dynamic-exception-specification*.

*Required behavior:* An `unexpected_handler` shall not return. See
also  [[except.unexpected]].

*Default behavior:* The implementation’s default `unexpected_handler`
calls `std::terminate()`.

### `set_unexpected` <a id="set.unexpected">[[set.unexpected]]</a>

``` cpp
unexpected_handler set_unexpected(unexpected_handler f) noexcept;
```

*Effects:* Establishes the function designated by `f` as the current
`unexpected_handler`.

It is unspecified whether a null pointer value designates the default
`unexpected_handler`.

*Returns:* The previous `unexpected_handler`.

### `get_unexpected` <a id="get.unexpected">[[get.unexpected]]</a>

``` cpp
unexpected_handler get_unexpected() noexcept;
```

*Returns:* The current `unexpected_handler`. This may be a null pointer
value.

### `unexpected` <a id="unexpected">[[unexpected]]</a>

``` cpp
[[noreturn]] void unexpected();
```

*Remarks:* Called by the implementation when a function exits via an
exception not allowed by its
*exception-specification* ([[except.unexpected]]), in effect after
evaluating the throw-expression ([[unexpected.handler]]). May also be
called directly by the program.

*Effects:* Calls the current `unexpected_handler` function. A default
`unexpected_handler` is always considered a callable handler in this
context.

<!-- Link reference definitions -->
[auto.ptr]: #auto.ptr
[auto.ptr.cons]: #auto.ptr.cons
[auto.ptr.conv]: #auto.ptr.conv
[auto.ptr.members]: #auto.ptr.members
[basic.scope.namespace]: basic.md#basic.scope.namespace
[bind]: utilities.md#bind
[class.copy]: special.md#class.copy
[class.dtor]: special.md#class.dtor
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.stc]: dcl.md#dcl.stc
[depr]: #depr
[depr.adaptors]: #depr.adaptors
[depr.auto.ptr]: #depr.auto.ptr
[depr.base]: #depr.base
[depr.c.headers]: #depr.c.headers
[depr.except.spec]: #depr.except.spec
[depr.function.objects]: #depr.function.objects
[depr.function.pointer.adaptors]: #depr.function.pointer.adaptors
[depr.impldec]: #depr.impldec
[depr.incr.bool]: #depr.incr.bool
[depr.ios.members]: #depr.ios.members
[depr.istrstream]: #depr.istrstream
[depr.istrstream.cons]: #depr.istrstream.cons
[depr.istrstream.members]: #depr.istrstream.members
[depr.lib.bind.1st]: #depr.lib.bind.1st
[depr.lib.bind.2nd]: #depr.lib.bind.2nd
[depr.lib.binder.1st]: #depr.lib.binder.1st
[depr.lib.binder.2nd]: #depr.lib.binder.2nd
[depr.lib.binders]: #depr.lib.binders
[depr.member.pointer.adaptors]: #depr.member.pointer.adaptors
[depr.ostrstream]: #depr.ostrstream
[depr.ostrstream.cons]: #depr.ostrstream.cons
[depr.ostrstream.members]: #depr.ostrstream.members
[depr.register]: #depr.register
[depr.str.strstreams]: #depr.str.strstreams
[depr.strstream]: #depr.strstream
[depr.strstream.cons]: #depr.strstream.cons
[depr.strstream.dest]: #depr.strstream.dest
[depr.strstream.oper]: #depr.strstream.oper
[depr.strstreambuf]: #depr.strstreambuf
[depr.strstreambuf.cons]: #depr.strstreambuf.cons
[depr.strstreambuf.members]: #depr.strstreambuf.members
[depr.strstreambuf.virtuals]: #depr.strstreambuf.virtuals
[except.unexpected]: except.md#except.unexpected
[exception.unexpected]: #exception.unexpected
[expr.post.incr]: expr.md#expr.post.incr
[expr.pre.incr]: expr.md#expr.pre.incr
[func.bind]: utilities.md#func.bind
[get.unexpected]: #get.unexpected
[input.output]: input.md#input.output
[iostreams.limits.pos]: input.md#iostreams.limits.pos
[namespace.udecl]: dcl.md#namespace.udecl
[set.unexpected]: #set.unexpected
[stmt.dcl]: stmt.md#stmt.dcl
[streambuf.pub.get]: input.md#streambuf.pub.get
[tab:future.c.headers]: #tab:future.c.headers
[tab:future.newoff.values]: #tab:future.newoff.values
[tab:future.seekoff.positioning]: #tab:future.seekoff.positioning
[tab:future.strstreambuf.effects]: #tab:future.strstreambuf.effects
[tab:future.strstreambuf1.effects]: #tab:future.strstreambuf1.effects
[unexpected]: #unexpected
[unexpected.handler]: #unexpected.handler
[unique.ptr]: utilities.md#unique.ptr

[^1]: An implementation should consider `alsize` in making this
    decision.

[^2]: The function signature `strlen(const char*)` is declared in
    `<cstring>` (@@REF:c.strings@@).
