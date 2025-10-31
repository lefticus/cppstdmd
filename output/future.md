## General <a id="depr.general">[depr.general]</a>

This Annex describes features of the C++ Standard that are specified for
compatibility with existing implementations.

These are deprecated features, where *deprecated* is defined as:
Normative for the current revision of C++, but having been identified as
a candidate for removal from future revisions. An implementation may
declare library names and entities described in this Clause with the
`deprecated` attribute [dcl.attr.deprecated].

## Arithmetic conversion on enumerations <a id="depr.arith.conv.enum">[depr.arith.conv.enum]</a>

The ability to apply the usual arithmetic conversions [expr.arith.conv]
on operands where one is of enumeration type and the other is of a
different enumeration type or a floating-point type is deprecated.

\[*Note 1*: Three-way comparisons [expr.spaceship] between such operands
are ill-formed. — *end note*\]

\[*Example 1*:

``` cpp
enum E1 { e };
enum E2 { f };
bool b = e <= 3.7;              // deprecated
int k = f - e;                  // deprecated
auto cmp = e <=> f;             // error
```

— *end example*\]

## Implicit capture of `*this` by reference <a id="depr.capture.this">[depr.capture.this]</a>

For compatibility with prior revisions of C++, a *lambda-expression*
with *capture-default* `=` [expr.prim.lambda.capture] may implicitly
capture `*this` by reference.

\[*Example 1*:

``` cpp
struct X {
  int x;
  void foo(int n) {
    auto f = [=]() { x = n; };          // deprecated: x means this->x, not a copy thereof
    auto g = [=, this]() { x = n; };    // recommended replacement
  }
};
```

— *end example*\]

## Array comparisons <a id="depr.array.comp">[depr.array.comp]</a>

Equality and relational comparisons [expr.eq,expr.rel] between two
operands of array type are deprecated.

\[*Note 1*: Three-way comparisons [expr.spaceship] between such operands
are ill-formed. — *end note*\]

\[*Example 1*:

``` cpp
int arr1[5];
int arr2[5];
bool same = arr1 == arr2;       // deprecated, same as \&arr1[0] == \&arr2[0],
                                // does not compare array contents
auto cmp = arr1 <=> arr2;       // error
```

— *end example*\]

## Deprecated `volatile` types <a id="depr.volatile.type">[depr.volatile.type]</a>

Postfix `++` and `--` expressions [expr.post.incr] and prefix `++` and
`--` expressions [expr.pre.incr] of volatile-qualified arithmetic and
pointer types are deprecated.

\[*Example 1*:

``` cpp
volatile int velociraptor;
++velociraptor;                     // deprecated
```

— *end example*\]

Certain assignments where the left operand is a volatile-qualified
non-class type are deprecated; see  [expr.ass].

\[*Example 2*:

``` cpp
int neck, tail;
volatile int brachiosaur;
brachiosaur = neck;                 // OK
tail = brachiosaur;                 // OK
tail = brachiosaur = neck;          // deprecated
brachiosaur += neck;                // OK
```

— *end example*\]

A function type [dcl.fct] with a parameter with volatile-qualified type
or with a volatile-qualified return type is deprecated.

\[*Example 3*:

``` cpp
volatile struct amber jurassic();                               // deprecated
void trex(volatile short left_arm, volatile short right_arm);   // deprecated
void fly(volatile struct pterosaur* pteranodon);                // OK
```

— *end example*\]

A structured binding [dcl.struct.bind] of a volatile-qualified type is
deprecated.

\[*Example 4*:

``` cpp
struct linhenykus { short forelimb; };
void park(linhenykus alvarezsauroid) {
  volatile auto [what_is_this] = alvarezsauroid;                // deprecated
  // ...
}
```

— *end example*\]

## Redeclaration of `static constexpr` data members <a id="depr.static.constexpr">[depr.static.constexpr]</a>

For compatibility with prior revisions of C++, a `constexpr` static data
member may be redundantly redeclared outside the class with no
initializer. This usage is deprecated.

\[*Example 1*:

``` cpp
struct A {
  static constexpr int n = 5;   // definition (declaration in C++14)
};

constexpr int A::n;             // redundant declaration (definition in C++14)
```

— *end example*\]

## Non-local use of TU-local entities <a id="depr.local">[depr.local]</a>

A declaration of a non-TU-local entity that is an exposure [basic.link]
is deprecated.

\[*Note 1*: Such a declaration in an importable module unit is
ill-formed. — *end note*\]

\[*Example 1*:

``` cpp
namespace {
  struct A {
    void f() {}
  };
}
A h();                          // deprecated: not internal linkage
inline void g() {A().f();}      // deprecated: inline and not internal linkage
```

— *end example*\]

## Implicit declaration of copy functions <a id="depr.impldec">[depr.impldec]</a>

The implicit definition of a copy constructor [class.copy.ctor] as
defaulted is deprecated if the class has a user-declared copy assignment
operator or a user-declared destructor [class.dtor]. The implicit
definition of a copy assignment operator [class.copy.assign] as
defaulted is deprecated if the class has a user-declared copy
constructor or a user-declared destructor. It is possible that future
versions of C++ will specify that these implicit definitions are deleted
[dcl.fct.def.delete].

## Literal operator function declarations using an identifier <a id="depr.lit">[depr.lit]</a>

A *literal-operator-id* [over.literal] of the form

``` cpp
operator string-literal identifier
```

is deprecated.

## `template` keyword before qualified names <a id="depr.template.template">[depr.template.template]</a>

The use of the keyword `template` before the qualified name of a class
or alias template without a template argument list is deprecated
[temp.names].

## Requires paragraph <a id="depr.res.on.required">[depr.res.on.required]</a>

In addition to the elements specified in [structure.specifications],
descriptions of function semantics may also contain a element to denote
the preconditions for calling a function.

Violation of any preconditions specified in a function’s element results
in undefined behavior unless the function’s element specifies throwing
an exception when the precondition is violated.

## `has_denorm` members in `numeric_limits` <a id="depr.numeric.limits.has.denorm">[depr.numeric.limits.has.denorm]</a>

The following type is defined in addition to those specified in :

``` cpp
namespace std {
  enum float_denorm_style {
    denorm_indeterminate = -1,
    denorm_absent = 0,
    denorm_present = 1
  };
}
```

The following members are defined in addition to those specified in
[numeric.limits.general]:

``` cpp
static constexpr float_denorm_style has_denorm = denorm_absent;
static constexpr bool has_denorm_loss = false;
```

The values of `has_denorm` and `has_denorm_loss` of specializations of
`numeric_limits` are unspecified.

The following members of the specialization `numeric_limits<bool>` are
defined in addition to those specified in [numeric.special]:

``` cpp
static constexpr float_denorm_style has_denorm = denorm_absent;
static constexpr bool has_denorm_loss = false;
```

## Deprecated C macros <a id="depr.c.macros">[depr.c.macros]</a>

The header `<stdalign.h>` has the following macro:

``` cpp
#define \xname{alignas_is_defined} 1
```

The header `<stdbool.h>` has the following macro:

``` cpp
#define \xname{bool_true_false_are_defined} 1
```

## Relational operators <a id="depr.relops">[depr.relops]</a>

The header has the following additions:

``` cpp
namespace std::rel_ops {
  template<class T> bool operator!=(const T&, const T&);
  template<class T> bool operator> (const T&, const T&);
  template<class T> bool operator<=(const T&, const T&);
  template<class T> bool operator>=(const T&, const T&);
}
```

To avoid redundant definitions of `operator!=` out of `operator==` and
operators `>`, `<=`, and `>=` out of `operator<`, the library provides
the following:

``` cpp
template<class T> bool operator!=(const T& x, const T& y);
```

Type `T` is *Cpp17EqualityComparable* (\[cpp17.equalitycomparable\]).

***Returns:***

`!(x == y)`.

``` cpp
template<class T> bool operator>(const T& x, const T& y);
```

Type `T` is *Cpp17LessThanComparable* (\[cpp17.lessthancomparable\]).

***Returns:***

`y < x`.

``` cpp
template<class T> bool operator<=(const T& x, const T& y);
```

Type `T` is *Cpp17LessThanComparable* (\[cpp17.lessthancomparable\]).

***Returns:***

`!(y < x)`.

``` cpp
template<class T> bool operator>=(const T& x, const T& y);
```

Type `T` is *Cpp17LessThanComparable* (\[cpp17.lessthancomparable\]).

***Returns:***

`!(x < y)`.

## `char*` streams <a id="depr.str.strstreams">[depr.str.strstreams]</a>

### Header `<strstream>` synopsis <a id="depr.strstream.syn">[depr.strstream.syn]</a>

The header `<strstream>` defines types that associate stream buffers
with character array objects and assist reading and writing such
objects.

``` cpp
namespace std {
  class strstreambuf;
  class istrstream;
  class ostrstream;
  class strstream;
}
```

### Class `strstreambuf` <a id="depr.strstreambuf">[depr.strstreambuf]</a>

#### General <a id="depr.strstreambuf.general">[depr.strstreambuf.general]</a>

``` cpp
namespace std {
  class strstreambuf : public basic_streambuf<char> {
  public:
    strstreambuf() : strstreambuf(0) {}
    explicit strstreambuf(streamsize alsize_arg);
    strstreambuf(void* (*palloc_arg)(size_t), void (*pfree_arg)(void*));
    strstreambuf(char* gnext_arg, streamsize n, char* pbeg_arg = nullptr);
    strstreambuf(const char* gnext_arg, streamsize n);

    strstreambuf(signed char* gnext_arg, streamsize n,
                 signed char* pbeg_arg = nullptr);
    strstreambuf(const signed char* gnext_arg, streamsize n);
    strstreambuf(unsigned char* gnext_arg, streamsize n,
                 unsigned char* pbeg_arg = nullptr);
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
                     ios_base::openmode which = ios_base::in | ios_base::out) override;
    pos_type seekpos(pos_type sp,
                     ios_base::openmode which = ios_base::in | ios_base::out) override;
    streambuf* setbuf(char* s, streamsize n) override;

  private:
    using strstate = T1;                // exposition only
    static const strstate allocated;    // exposition only
    static const strstate constant;     // exposition only
    static const strstate dynamic;      // exposition only
    static const strstate frozen;       // exposition only
    strstate strmode;                   // exposition only
    streamsize alsize;                  // exposition only
    void* (*palloc)(size_t);            // exposition only
    void (*pfree)(void*);               // exposition only
  };
}
```

The class `strstreambuf` associates the input sequence, and possibly the
output sequence, with an object of some *character* array type, whose
elements store arbitrary values. The array object has several
attributes.

\[*Note 1*:

For the sake of exposition, these are represented as elements of a
bitmask type (indicated here as `T1`) called `strstate`. The elements
are:

- `allocated`, set when a dynamic array object has been allocated, and
  hence will be freed by the destructor for the `strstreambuf` object;

- `constant`, set when the array object has `const` elements, so the
  output sequence cannot be written;

- `dynamic`, set when the array object is allocated (or reallocated) as
  necessary to hold a character sequence that can change in length;

- `frozen`, set when the program has requested that the array object not
  be altered, reallocated, or freed.

— *end note*\]

\[*Note 2*:

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

#### `strstreambuf` constructors <a id="depr.strstreambuf.cons">[depr.strstreambuf.cons]</a>

``` cpp
explicit strstreambuf(streamsize alsize_arg);
```

***Effects:***

Initializes the base class with `streambuf()`. The postconditions of
this function are indicated in \[depr.strstreambuf.cons.sz\].

``` cpp
strstreambuf(void* (*palloc_arg)(size_t), void (*pfree_arg)(void*));
```

***Effects:***

Initializes the base class with `streambuf()`. The postconditions of
this function are indicated in \[depr.strstreambuf.cons.alloc\].

<div class="libtab2">

`strstreambuf(void* (*)(size_t), void (*)(void*))` effects
depr.strstreambuf.cons.alloc ll ElementValue `strmode` & `dynamic`  
`alsize` & an unspecified value  
`palloc` & `palloc_arg`  
`pfree` & `pfree_arg`  

</div>

``` cpp
strstreambuf(char* gnext_arg, streamsize n, char* pbeg_arg = nullptr);
strstreambuf(signed char* gnext_arg, streamsize n,
             signed char* pbeg_arg = nullptr);
strstreambuf(unsigned char* gnext_arg, streamsize n,
             unsigned char* pbeg_arg = nullptr);
```

***Effects:***

Initializes the base class with `streambuf()`. The postconditions of
this function are indicated in \[depr.strstreambuf.cons.ptr\].

<div class="libtab2">

`strstreambuf(charT*, streamsize, charT*)` effects
depr.strstreambuf.cons.ptr ll ElementValue `strmode` & 0  
`alsize` & an unspecified value  
`palloc` & a null pointer  
`pfree` & a null pointer  

</div>

`gnext_arg` shall point to the first element of an array object whose
number of elements `N` is determined as follows:

- If `n > 0`, `N` is `n`.

- If `n == 0`, `N` is `std::strlen(gnext_arg)`.

- If `n < 0`, `N` is `INT_MAX`.

  The function signature `strlen(const char*)` is declared in . The
  macro `INT_MAX` is defined in .

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

***Effects:***

Behaves the same as `strstreambuf((char*)gnext_arg,n)`, except that the
constructor also sets `constant` in `strmode`.

``` cpp
virtual ~strstreambuf();
```

***Effects:***

Destroys an object of class `strstreambuf`. The function frees the
dynamically allocated array object only if `(strmode & allocated) != 0`
and `(strmode & frozen) == 0`. (\[depr.strstreambuf.virtuals\] describes
how a dynamically allocated array object is freed.)

#### Member functions <a id="depr.strstreambuf.members">[depr.strstreambuf.members]</a>

``` cpp
void freeze(bool freezefl = true);
```

***Effects:***

If `strmode & dynamic` is nonzero, alters the freeze status of the
dynamic array object as follows:

- If `freezefl` is `true`, the function sets `frozen` in `strmode`.

- Otherwise, it clears `frozen` in `strmode`.

``` cpp
char* str();
```

***Effects:***

Calls `freeze()`, then returns the beginning pointer for the input
sequence, `gbeg`.

***Remarks:***

The return value can be a null pointer.

``` cpp
int pcount() const;
```

***Effects:***

If the next pointer for the output sequence, `pnext`, is a null pointer,
returns zero. Otherwise, returns the current effective length of the
array object as the next pointer minus the beginning pointer for the
output sequence, `pnext - pbeg`.

#### `strstreambuf` overridden virtual functions <a id="depr.strstreambuf.virtuals">[depr.strstreambuf.virtuals]</a>

``` cpp
int_type overflow(int_type c = EOF) override;
```

***Effects:***

Appends the character designated by `c` to the output sequence, if
possible, in one of two ways:

- If `c != EOF` and if either the output sequence has a write position
  available or the function makes a write position available (as
  described below), assigns `c` to `*pnext++`.

  Returns `(unsigned char)c`.

- If `c == EOF`, there is no character to append.

  Returns a value other than `EOF`.

Returns `EOF` to indicate failure.

***Remarks:***

The function can alter the number of write positions available as a
result of any call.

To make a write position available, the function reallocates (or
initially allocates) an array object with a sufficient number of
elements `n` to hold the current array object (if any), plus at least
one additional write position. How many additional write positions are
made available is otherwise unspecified. If `palloc` is not a null
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

An implementation should consider `alsize` in making the decision how
many additional write positions to make available.

``` cpp
int_type pbackfail(int_type c = EOF) override;
```

Puts back the character designated by `c` to the input sequence, if
possible, in one of three ways:

- If `c != EOF`, if the input sequence has a putback position available,
  and if `(char)c == gnext[-1]`, assigns `gnext - 1` to `gnext`.

  Returns `c`.

- If `c != EOF`, if the input sequence has a putback position available,
  and if `strmode & constant` is zero, assigns `c` to `*–gnext`.

  Returns `c`.

- If `c == EOF` and if the input sequence has a putback position
  available, assigns `gnext - 1` to `gnext`.

  Returns a value other than `EOF`.

Returns `EOF` to indicate failure.

***Remarks:***

If the function can succeed in more than one of these ways, it is
unspecified which way is chosen. The function can alter the number of
putback positions available as a result of any call.

``` cpp
int_type underflow() override;
```

***Effects:***

Reads a character from the , if possible, without moving the stream
position past it, as follows:

- If the input sequence has a read position available, the function
  signals success by returning `(unsigned char)gnext`.

- Otherwise, if the current write next pointer `pnext` is not a null
  pointer and is greater than the current read end pointer `gend`, makes
  a available by assigning to `gend` a value greater than `gnext` and no
  greater than `pnext`.

  Returns `(unsigned char)*gnext`.

Returns `EOF` to indicate failure.

***Remarks:***

The function can alter the number of read positions available as a
result of any call.

``` cpp
pos_type seekoff(off_type off, seekdir way, openmode which = in | out) override;
```

***Effects:***

Alters the stream position within one of the controlled sequences, if
possible, as indicated in \[depr.strstreambuf.seekoff.pos\].

<div class="libtab2">

`seekoff` positioningdepr.strstreambuf.seekoff.pos
p2.5inlConditionsResult `(which & ios::in) != 0` & positions the input
sequence  
`(which & ios::out) != 0` & positions the output sequence  
`(which & (ios::in | ios::out)) ==` `(ios::in | ios::out)` and either
`way == ios::beg` or `way == ios::end` & positions both the input and
the output sequences  
Otherwise & the positioning operation fails.  

</div>

For a sequence to be positioned, if its next pointer is a null pointer,
the positioning operation fails. Otherwise, the function determines
`newoff` as indicated in \[depr.strstreambuf.seekoff.newoff\].

<div class="libtab2">

`newoff` valuesdepr.strstreambuf.seekoff.newoff
p2.0inp2.0inCondition`newoff` Value `way == ios::beg` & 0  
`way == ios::cur` & the next pointer minus the beginning pointer
(`xnext - xbeg`).  
`way == ios::end` & `seekhigh` minus the beginning pointer
(`seekhigh - xbeg`).  

</div>

If `(newoff + off) < (seeklow - xbeg)` or
`(seekhigh - xbeg) < (newoff + off)`, the positioning operation fails.
Otherwise, the function assigns `xbeg + newoff + off` to the next
pointer `xnext`.

***Returns:***

`pos_type(newoff)`, constructed from the resultant offset `newoff` (of
type `off_type`), that stores the resultant stream position, if
possible. If the positioning operation fails, or if the constructed
object cannot represent the resultant stream position, the return value
is `pos_type(off_type(-1))`.

``` cpp
pos_type seekpos(pos_type sp, ios_base::openmode which = ios_base::in | ios_base::out) override;
```

***Effects:***

Alters the stream position within one of the controlled sequences, if
possible, to correspond to the stream position stored in `sp` (as
described below).

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

***Returns:***

`pos_type(newoff)`, constructed from the resultant offset `newoff` (of
type `off_type`), that stores the resultant stream position, if
possible. If the positioning operation fails, or if the constructed
object cannot represent the resultant stream position, the return value
is `pos_type(off_type(-1))`.

``` cpp
streambuf<char>* setbuf(char* s, streamsize n) override;
```

***Effects:***

Behavior is *implementation-defined*, except that `setbuf(0, 0)` has no
effect.

### Class `istrstream` <a id="depr.istrstream">[depr.istrstream]</a>

#### General <a id="depr.istrstream.general">[depr.istrstream.general]</a>

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
    strstreambuf sb;            // exposition only
  };
}
```

The class `istrstream` supports the reading of objects of class
`strstreambuf`. It supplies a `strstreambuf` object to control the
associated array object. For the sake of exposition, the maintained data
is presented here as:

- `sb`, the `strstreambuf` object.

#### `istrstream` constructors <a id="depr.istrstream.cons">[depr.istrstream.cons]</a>

``` cpp
explicit istrstream(const char* s);
explicit istrstream(char* s);
```

***Effects:***

Initializes the base class with `istream(&sb)` and `sb` with
`strstreambuf(s, 0)`. `s` shall designate the first element of an NTBS.

``` cpp
istrstream(const char* s, streamsize n);
istrstream(char* s, streamsize n);
```

***Effects:***

Initializes the base class with `istream(&sb)` and `sb` with
`strstreambuf(s, n)`. `s` shall designate the first element of an array
whose length is `n` elements, and `n` shall be greater than zero.

#### Member functions <a id="depr.istrstream.members">[depr.istrstream.members]</a>

``` cpp
strstreambuf* rdbuf() const;
```

***Returns:***

`const_cast<strstreambuf*>(&sb)`.

``` cpp
char* str();
```

***Returns:***

`rdbuf()->str()`.

### Class `ostrstream` <a id="depr.ostrstream">[depr.ostrstream]</a>

#### General <a id="depr.ostrstream.general">[depr.ostrstream.general]</a>

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
    strstreambuf sb;            // exposition only
  };
}
```

The class `ostrstream` supports the writing of objects of class
`strstreambuf`. It supplies a `strstreambuf` object to control the
associated array object. For the sake of exposition, the maintained data
is presented here as:

- `sb`, the `strstreambuf` object.

#### `ostrstream` constructors <a id="depr.ostrstream.cons">[depr.ostrstream.cons]</a>

``` cpp
ostrstream();
```

***Effects:***

Initializes the base class with `ostream(&sb)` and `sb` with
`strstreambuf()`.

``` cpp
ostrstream(char* s, int n, ios_base::openmode mode = ios_base::out);
```

***Effects:***

Initializes the base class with `ostream(&sb)`, and `sb` with one of two
constructors:

- If `(mode & app) == 0`, then `s` shall designate the first element of
  an array of `n` elements.

  The constructor is `strstreambuf(s, n, s)`.

- If `(mode & app) != 0`, then `s` shall designate the first element of
  an array of `n` elements that contains an NTBS whose first element is
  designated by `s`. The constructor is
  `strstreambuf(s, n, s + std::strlen(s))`.

  The function signature `strlen(const char*)` is declared in .

#### Member functions <a id="depr.ostrstream.members">[depr.ostrstream.members]</a>

``` cpp
strstreambuf* rdbuf() const;
```

***Returns:***

`(strstreambuf*)&sb`.

``` cpp
void freeze(bool freezefl = true);
```

***Effects:***

Calls `rdbuf()->freeze(freezefl)`.

``` cpp
char* str();
```

***Returns:***

`rdbuf()->str()`.

``` cpp
int pcount() const;
```

***Returns:***

`rdbuf()->pcount()`.

### Class `strstream` <a id="depr.strstream">[depr.strstream]</a>

#### General <a id="depr.strstream.general">[depr.strstream.general]</a>

``` cpp
namespace std {
  class strstream
    : public basic_iostream<char> {
  public:
    // types
    using char_type = char;
    using int_type  = char_traits<char>::int_type;
    using pos_type  = char_traits<char>::pos_type;
    using off_type  = char_traits<char>::off_type;

    // constructors/destructor
    strstream();
    strstream(char* s, int n,
              ios_base::openmode mode = ios_base::in|ios_base::out);
    virtual ~strstream();

    // members
    strstreambuf* rdbuf() const;
    void freeze(bool freezefl = true);
    int pcount() const;
    char* str();

  private:
    strstreambuf sb;            // exposition only
  };
}
```

The class `strstream` supports reading and writing from objects of class
`strstreambuf`. It supplies a `strstreambuf` object to control the
associated array object. For the sake of exposition, the maintained data
is presented here as:

- `sb`, the `strstreambuf` object.

#### `strstream` constructors <a id="depr.strstream.cons">[depr.strstream.cons]</a>

``` cpp
strstream();
```

***Effects:***

Initializes the base class with `iostream(&sb)`.

``` cpp
strstream(char* s, int n,
          ios_base::openmode mode = ios_base::in|ios_base::out);
```

***Effects:***

Initializes the base class with `iostream(&sb)`, and `sb` with one of
the two constructors:

- If `(mode & app) == 0`, then `s` shall designate the first element of
  an array of `n` elements. The constructor is `strstreambuf(s,n,s)`.

- If `(mode & app) != 0`, then `s` shall designate the first element of
  an array of `n` elements that contains an NTBS whose first element is
  designated by `s`. The constructor is
  `strstreambuf(s,n,s + std::strlen(s))`.

#### `strstream` destructor <a id="depr.strstream.dest">[depr.strstream.dest]</a>

``` cpp
virtual ~strstream();
```

***Effects:***

Destroys an object of class `strstream`.

#### `strstream` operations <a id="depr.strstream.oper">[depr.strstream.oper]</a>

``` cpp
strstreambuf* rdbuf() const;
```

***Returns:***

`const_cast<strstreambuf*>(&sb)`.

``` cpp
void freeze(bool freezefl = true);
```

***Effects:***

Calls `rdbuf()->freeze(freezefl)`.

``` cpp
char* str();
```

***Returns:***

`rdbuf()->str()`.

``` cpp
int pcount() const;
```

***Returns:***

`rdbuf()->pcount()`.

## Deprecated error numbers <a id="depr.cerrno">[depr.cerrno]</a>

The following macros are defined in addition to those specified in
[cerrno.syn]:

``` cpp
#define ENODATA see below
#define ENOSR see below
#define ENOSTR see below
#define ETIME see below
```

The meaning of these macros is defined by the POSIX standard.

The following `enum errc` enumerators are defined in addition to those
specified in [system.error.syn]:

``` cpp
no_message_available,               // ENODATA
no_stream_resources,                // ENOSR
not_a_stream,                       // ENOSTR
stream_timeout,                     // ETIME
```

The value of each `enum errc` enumerator above is the same as the value
of the `<cerrno>` macro shown in the above synopsis.

## The default allocator <a id="depr.default.allocator">[depr.default.allocator]</a>

The following member is defined in addition to those specified in
[default.allocator]:

``` cpp
namespace std {
  template<class T> class allocator {
  public:
    using is_always_equal = true_type;
  };
}
```

## Deprecated `polymorphic_allocator` member function <a id="depr.mem.poly.allocator.mem">[depr.mem.poly.allocator.mem]</a>

The following member is declared in addition to those members specified
in [mem.poly.allocator.mem]:

``` cpp
namespace std::pmr {
  template<class Tp = byte>
  class polymorphic_allocator {
  public:
    template <class T>
      void destroy(T* p);
  };
}
```

``` cpp
template<class T>
  void destroy(T* p);
```

***Effects:***

As if by `p->T̃()`.

## Deprecated type traits <a id="depr.meta.types">[depr.meta.types]</a>

The header has the following addition:

``` cpp
namespace std {
  template<class T> struct is_pod;
  template<class T> constexpr bool is_pod_v = is_pod<T>::value;
  template<size_t Len, size_t Align = default-alignment> // see below
    struct aligned_storage;
  template<size_t Len, size_t Align = default-alignment> // see below
    using \libglobal{aligned_storage_t} = typename aligned_storage<Len, Align>::type;
  template<size_t Len, class... Types>
    struct aligned_union;
  template<size_t Len, class... Types>
    using \libglobal{aligned_union_t} = typename aligned_union<Len, Types...>::type;
}
```

The behavior of a program that adds specializations for any of the
templates defined in this subclause is undefined, unless explicitly
permitted by the specification of the corresponding template.

``` cpp
template<class T> struct is_pod;
```

`remove_all_extents_t<T>` shall be a complete type or .

`is_pod<T>` is a *Cpp17UnaryTypeTrait*\[meta.rqmts\] with a base
characteristic of `true_type` if `T` is a POD type, and `false_type`
otherwise. A POD class is a class that is both a trivial class and a
standard-layout class, and has no non-static data members of type
non-POD class (or array thereof). A POD type is a scalar type, a POD
class, an array of such a type, or a cv-qualified version of one of
these types.

\[*Note 1*: It is unspecified whether a closure
type\[expr.prim.lambda.closure\] is a POD type. — *end note*\]

``` cpp
template<size_t Len, size_t Align = default-alignment>
  struct aligned_storage;
```

The value of *default-alignment* is the most stringent alignment
requirement for any object type whose size is no greater than
`Len`\[basic.types\].

***Mandates:***

`Len` is not zero. `Align` is equal to `alignof(T)` for some type `T` or
to *default-alignment*.

The member typedef `type` denotes a trivial standard-layout type
suitable for use as uninitialized storage for any object whose size is
at most `Len` and whose alignment is a divisor of `Align`.

\[*Note 2*: Uses of `aligned_storage<Len, Align>::type` can be replaced
by an array `std::byte[Len]` declared with
`alignas(Align)`. — *end note*\]

\[*Note 3*:

A typical implementation would define `aligned_storage` as:

    template<size_t Len, size_t Alignment>
    struct aligned_storage {
      typedef struct {
        alignas(Alignment) unsigned char __data[Len];
      } type;
    };

— *end note*\]

``` cpp
template<size_t Len, class... Types>
  struct aligned_union;
```

***Mandates:***

At least one type is provided. Each type in the template parameter pack
`Types` is a complete object type.

The member typedef `type` denotes a trivial standard-layout type
suitable for use as uninitialized storage for any object whose type is
listed in `Types`; its size shall be at least `Len`. The static member
`alignment_value` is an integral constant of type `size_t` whose value
is the strictest alignment of all types listed in `Types`.

## Tuple <a id="depr.tuple">[depr.tuple]</a>

The header has the following additions:

``` cpp
namespace std {
  template<class T> struct tuple_size<volatile T>;
  template<class T> struct tuple_size<const volatile T>;

  template<size_t I, class T> struct tuple_element<I, volatile T>;
  template<size_t I, class T> struct tuple_element<I, const volatile T>;
}
```

``` cpp
template<class T> struct tuple_size<volatile T>;
template<class T> struct tuple_size<const volatile T>;
```

Let `TS` denote `tuple_size<T>` of the cv-unqualified type `T`. If the
expression `TS::value` is well-formed when treated as an unevaluated
operand\[term.unevaluated.operand\], then specializations of each of the
two templates meet the *Cpp17TransformationTrait* requirements with a
base characteristic of `integral_constant<size_t, TS::value>`.
Otherwise, they have no member `value`.

Access checking is performed as if in a context unrelated to `TS` and
`T`. Only the validity of the immediate context of the expression is
considered.

In addition to being available via inclusion of the header, the two
templates are available when any of the headers , , or are included.

``` cpp
template<size_t I, class T> struct tuple_element<I, volatile T>;
template<size_t I, class T> struct tuple_element<I, const volatile T>;
```

Let `TE` denote `tuple_element_t<I, T>` of the cv-unqualified type `T`.
Then specializations of each of the two templates meet the
*Cpp17TransformationTrait* requirements with a member typedef `type`
that names the following type:

- for the first specialization, `add_volatile_t<TE>`, and

- for the second specialization, `add_cv_t<TE>`.

In addition to being available via inclusion of the header, the two
templates are available when any of the headers , , or are included.

## Variant <a id="depr.variant">[depr.variant]</a>

The header has the following additions:

``` cpp
namespace std {
  template<class T> struct variant_size<volatile T>;
  template<class T> struct variant_size<const volatile T>;

  template<size_t I, class T> struct variant_alternative<I, volatile T>;
  template<size_t I, class T> struct variant_alternative<I, const volatile T>;
}
```

``` cpp
template<class T> struct variant_size<volatile T>;
template<class T> struct variant_size<const volatile T>;
```

Let `VS` denote `variant_size<T>` of the cv-unqualified type `T`. Then
specializations of each of the two templates meet the
*Cpp17UnaryTypeTrait* requirements with a base characteristic of
`integral_constant<size_t, VS::value>`.

``` cpp
template<size_t I, class T> struct variant_alternative<I, volatile T>;
template<size_t I, class T> struct variant_alternative<I, const volatile T>;
```

Let `VA` denote `variant_alternative<I, T>` of the cv-unqualified type
`T`. Then specializations of each of the two templates meet the
*Cpp17TransformationTrait* requirements with a member typedef `type`
that names the following type:

- for the first specialization, `add_volatile_t<VA::type>`, and

- for the second specialization, `add_cv_t<VA::type>`.

## Deprecated `iterator` class template <a id="depr.iterator">[depr.iterator]</a>

The header has the following addition:

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

\[*Note 1*: If the new iterator type is a class template, then these
aliases will not be visible from within the iterator class’s template
definition, but only to callers of that class. — *end note*\]

\[*Example 1*:

If a C++ program wants to define a bidirectional iterator for some data
structure containing `double` and such that it works on a large memory
model of the implementation, it can do so with:

``` cpp
class MyIterator :
  public iterator<bidirectional_iterator_tag, double, long, T*, T&> {
  // code implementing ++, etc.
};
```

— *end example*\]

## Deprecated `move_iterator` access <a id="depr.move.iter.elem">[depr.move.iter.elem]</a>

The following member is declared in addition to those members specified
in [move.iter.elem]:

``` cpp
namespace std {
  template<class Iterator>
  class move_iterator {
  public:
    constexpr pointer operator->() const;
  };
}
```

``` cpp
constexpr pointer operator->() const;
```

***Returns:***

`current`.

## Deprecated `shared_ptr` atomic access <a id="depr.util.smartptr.shared.atomic">[depr.util.smartptr.shared.atomic]</a>

The header has the following additions:

``` cpp
namespace std {
  template<class T>
    bool atomic_is_lock_free(const shared_ptr<T>* p);

  template<class T>
    shared_ptr<T> atomic_load(const shared_ptr<T>* p);
  template<class T>
    shared_ptr<T> atomic_load_explicit(const shared_ptr<T>* p, memory_order mo);

  template<class T>
    void atomic_store(shared_ptr<T>* p, shared_ptr<T> r);
  template<class T>
    void atomic_store_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);

  template<class T>
    shared_ptr<T> atomic_exchange(shared_ptr<T>* p, shared_ptr<T> r);
  template<class T>
    shared_ptr<T> atomic_exchange_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);

  template<class T>
    bool atomic_compare_exchange_weak(shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
  template<class T>
    bool atomic_compare_exchange_strong(shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
  template<class T>
    bool atomic_compare_exchange_weak_explicit(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
      memory_order success, memory_order failure);
  template<class T>
    bool atomic_compare_exchange_strong_explicit(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
      memory_order success, memory_order failure);
}
```

Concurrent access to a `shared_ptr` object from multiple threads does
not introduce a data race if the access is done exclusively via the
functions in this subclause and the instance is passed as their first
argument.

The meaning of the arguments of type `memory_order` is explained in 
[atomics.order].

``` cpp
template<class T> bool atomic_is_lock_free(const shared_ptr<T>* p);
```

`p` shall not be null.

***Returns:***

`true` if atomic access to `*p` is lock-free, `false` otherwise.

***Throws:***

Nothing.

``` cpp
template<class T> shared_ptr<T> atomic_load(const shared_ptr<T>* p);
```

`p` shall not be null.

***Returns:***

`atomic_load_explicit(p, memory_order::seq_cst)`.

***Throws:***

Nothing.

``` cpp
template<class T> shared_ptr<T> atomic_load_explicit(const shared_ptr<T>* p, memory_order mo);
```

`p` shall not be null.

`mo` shall not be `memory_order::release` or `memory_order::acq_rel`.

***Returns:***

`*p`.

***Throws:***

Nothing.

``` cpp
template<class T> void atomic_store(shared_ptr<T>* p, shared_ptr<T> r);
```

`p` shall not be null.

***Effects:***

As if by `atomic_store_explicit(p, r, memory_order::seq_cst)`.

***Throws:***

Nothing.

``` cpp
template<class T> void atomic_store_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);
```

`p` shall not be null.

`mo` shall not be `memory_order::acquire` or `memory_order::acq_rel`.

***Effects:***

As if by `p->swap(r)`.

***Throws:***

Nothing.

``` cpp
template<class T> shared_ptr<T> atomic_exchange(shared_ptr<T>* p, shared_ptr<T> r);
```

`p` shall not be null.

***Returns:***

`atomic_exchange_explicit(p, r, memory_order::seq_cst)`.

***Throws:***

Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_exchange_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);
```

`p` shall not be null.

***Effects:***

As if by `p->swap(r)`.

***Returns:***

The previous value of `*p`.

***Throws:***

Nothing.

``` cpp
template<class T>
  bool atomic_compare_exchange_weak(shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
```

`p` shall not be null and `v` shall not be null.

***Returns:***

``` cpp
atomic_compare_exchange_weak_explicit(p, v, w, memory_order::seq_cst, memory_order::seq_cst)
```

***Throws:***

Nothing.

``` cpp
template<class T>
  bool atomic_compare_exchange_strong(shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
```

***Returns:***

``` cpp
atomic_compare_exchange_strong_explicit(p, v, w, memory_order::seq_cst,
                                        memory_order::seq_cst)
```

``` cpp
template<class T>
  bool atomic_compare_exchange_weak_explicit(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
    memory_order success, memory_order failure);
template<class T>
  bool atomic_compare_exchange_strong_explicit(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
    memory_order success, memory_order failure);
```

`p` shall not be null and `v` shall not be null. The `failure` argument
shall not be `memory_order::release` nor `memory_order::acq_rel`.

***Effects:***

If `*p` is equivalent to `*v`, assigns `w` to `*p` and has
synchronization semantics corresponding to the value of `success`,
otherwise assigns `*p` to `*v` and has synchronization semantics
corresponding to the value of `failure`.

***Returns:***

`true` if `*p` was equivalent to `*v`, `false` otherwise.

***Throws:***

Nothing.

***Remarks:***

Two `shared_ptr` objects are equivalent if they store the same pointer
value and share ownership. The weak form may fail spuriously.
See \[atomics.types.operations\].

## Deprecated `basic_string` capacity <a id="depr.string.capacity">[depr.string.capacity]</a>

The following member is declared in addition to those members specified
in [string.capacity]:

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_string {
  public:
    void reserve();
  };
}
```

``` cpp
void reserve();
```

***Effects:***

After this call, `capacity()` has an unspecified value greater than or
equal to `size()`.

\[*Note 1*: This is a non-binding shrink to fit request. — *end note*\]

## Deprecated standard code conversion facets <a id="depr.locale.stdcvt">[depr.locale.stdcvt]</a>

### General <a id="depr.locale.stdcvt.general">[depr.locale.stdcvt.general]</a>

The header `<codecvt>` provides code conversion facets for various
character encodings.

### Header `<codecvt>` synopsis <a id="depr.codecvt.syn">[depr.codecvt.syn]</a>

``` cpp
namespace std {
  enum codecvt_mode {
    consume_header = 4,
    generate_header = 2,
    little_endian = 1
  };

  template<class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = (codecvt_mode)0>
    class codecvt_utf8 : public codecvt<Elem, char, mbstate_t> {
    public:
      explicit codecvt_utf8(size_t refs = 0);
      ~codecvt_utf8();
    };

  template<class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = (codecvt_mode)0>
    class codecvt_utf16 : public codecvt<Elem, char, mbstate_t> {
    public:
      explicit codecvt_utf16(size_t refs = 0);
      ~codecvt_utf16();
    };

  template<class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = (codecvt_mode)0>
    class codecvt_utf8_utf16 : public codecvt<Elem, char, mbstate_t> {
    public:
      explicit codecvt_utf8_utf16(size_t refs = 0);
      ~codecvt_utf8_utf16();
    };
}
```

### Requirements <a id="depr.locale.stdcvt.req">[depr.locale.stdcvt.req]</a>

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

- UCS-2 is the same encoding as UTF-16, except that it encodes scalar
  values in the range – (Basic Multilingual Plane) only.

For the facet `codecvt_utf8`:

- The facet shall convert between UTF-8 multibyte sequences and UCS-2 or
  UTF-32 (depending on the size of `Elem`).

- Endianness shall not affect how multibyte sequences are read or
  written.

- The multibyte sequences may be written as either a text or a binary
  file.

For the facet `codecvt_utf16`:

- The facet shall convert between UTF-16 multibyte sequences and UCS-2
  or UTF-32 (depending on the size of `Elem`).

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

## Deprecated convenience conversion interfaces <a id="depr.conversions">[depr.conversions]</a>

### General <a id="depr.conversions.general">[depr.conversions.general]</a>

The header has the following additions:

``` cpp
namespace std {
  template<class Codecvt, class Elem = wchar_t,
           class WideAlloc = allocator<Elem>,
           class ByteAlloc = allocator<char>>
    class wstring_convert;

  template<class Codecvt, class Elem = wchar_t,
           class Tr = char_traits<Elem>>
    class wbuffer_convert;
}
```

### Class template `wstring_convert` <a id="depr.conversions.string">[depr.conversions.string]</a>

Class template `wstring_convert` performs conversions between a wide
string and a byte string. It lets you specify a code conversion facet
(like class template `codecvt`) to perform the conversions, without
affecting any streams or locales.

\[*Example 1*:

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
  template<class Codecvt, class Elem = wchar_t,
           class WideAlloc = allocator<Elem>,
           class ByteAlloc = allocator<char>>
    class wstring_convert {
    public:
      using byte_string = basic_string<char, char_traits<char>, ByteAlloc>;
      using wide_string = basic_string<Elem, char_traits<Elem>, WideAlloc>;
      using state_type  = typename Codecvt::state_type;
      using int_type    = typename wide_string::traits_type::int_type;

      wstring_convert() : wstring_convert(new Codecvt) {}
      explicit wstring_convert(Codecvt* pcvt);
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
WideAlloc>` and byte string objects of class `basic_string<char,
char_traits<char>, ByteAlloc>`. The class template defines the types
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
size_t converted() const noexcept;
```

***Returns:***

`cvtcount`.

``` cpp
wide_string from_bytes(char byte);
wide_string from_bytes(const char* ptr);
wide_string from_bytes(const byte_string& str);
wide_string from_bytes(const char* first, const char* last);
```

***Effects:***

The first member function shall convert the single-element sequence
`byte` to a wide string. The second member function shall convert the
null-terminated sequence beginning at `ptr` to a wide string. The third
member function shall convert the sequence stored in `str` to a wide
string. The fourth member function shall convert the sequence defined by
the range \[`first`, `last`) to a wide string.

In all cases:

- If the `cvtstate` object was not constructed with an explicit value,
  it shall be set to its default value (the initial conversion state)
  before the conversion begins. Otherwise it shall be left unchanged.

- The number of input elements successfully converted shall be stored in
  `cvtcount`.

***Returns:***

If no conversion error occurs, the member function shall return the
converted wide string. Otherwise, if the object was constructed with a
wide-error string, the member function shall return the wide-error
string. Otherwise, the member function throws an object of class
`range_error`.

``` cpp
state_type state() const;
```

***Returns:***

`cvtstate`.

``` cpp
byte_string to_bytes(Elem wchar);
byte_string to_bytes(const Elem* wptr);
byte_string to_bytes(const wide_string& wstr);
byte_string to_bytes(const Elem* first, const Elem* last);
```

***Effects:***

The first member function shall convert the single-element sequence
`wchar` to a byte string. The second member function shall convert the
null-terminated sequence beginning at `wptr` to a byte string. The third
member function shall convert the sequence stored in `wstr` to a byte
string. The fourth member function shall convert the sequence defined by
the range \[`first`, `last`) to a byte string.

In all cases:

- If the `cvtstate` object was not constructed with an explicit value,
  it shall be set to its default value (the initial conversion state)
  before the conversion begins. Otherwise it shall be left unchanged.

- The number of input elements successfully converted shall be stored in
  `cvtcount`.

***Returns:***

If no conversion error occurs, the member function shall return the
converted byte string. Otherwise, if the object was constructed with a
byte-error string, the member function shall return the byte-error
string. Otherwise, the member function shall throw an object of class
`range_error`.

``` cpp
explicit wstring_convert(Codecvt* pcvt);
wstring_convert(Codecvt* pcvt, state_type state);
explicit wstring_convert(const byte_string& byte_err,
    const wide_string& wide_err = wide_string());
```

For the first and second constructors, `pcvt != nullptr`.

***Effects:***

The first constructor shall store `pcvt` in `cvtptr` and default values
in `cvtstate`, `byte_err_string`, and `wide_err_string`. The second
constructor shall store `pcvt` in `cvtptr`, `state` in `cvtstate`, and
default values in `byte_err_string` and `wide_err_string`; moreover the
stored state shall be retained between calls to `from_bytes` and
`to_bytes`. The third constructor shall store `new Codecvt` in `cvtptr`,
`state_type()` in `cvtstate`, `byte_err` in `byte_err_string`, and
`wide_err` in `wide_err_string`.

``` cpp
~wstring_convert();
```

***Effects:***

The destructor shall delete `cvtptr`.

### Class template `wbuffer_convert` <a id="depr.conversions.buffer">[depr.conversions.buffer]</a>

Class template `wbuffer_convert` looks like a wide stream buffer, but
performs all its I/O through an underlying byte stream buffer that you
specify when you construct it. Like class template `wstring_convert`, it
lets you specify a code conversion facet to perform the conversions,
without affecting any streams or locales.

``` cpp
namespace std {
  template<class Codecvt, class Elem = wchar_t, class Tr = char_traits<Elem>>
    class wbuffer_convert : public basic_streambuf<Elem, Tr> {
    public:
      using state_type = typename Codecvt::state_type;

      wbuffer_convert() : wbuffer_convert(nullptr) {}
      explicit wbuffer_convert(streambuf* bytebuf,
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

***Returns:***

`cvtstate`.

``` cpp
streambuf* rdbuf() const;
```

***Returns:***

`bufptr`.

``` cpp
streambuf* rdbuf(streambuf* bytebuf);
```

***Effects:***

Stores `bytebuf` in `bufptr`.

***Returns:***

The previous value of `bufptr`.

``` cpp
explicit wbuffer_convert(
    streambuf* bytebuf,
    Codecvt* pcvt = new Codecvt,
    state_type state = state_type());
```

`pcvt != nullptr`.

***Effects:***

The constructor constructs a stream buffer object, initializes `bufptr`
to `bytebuf`, initializes `cvtptr` to `pcvt`, and initializes `cvtstate`
to `state`.

``` cpp
~wbuffer_convert();
```

***Effects:***

The destructor shall delete `cvtptr`.

## Deprecated locale category facets <a id="depr.locale.category">[depr.locale.category]</a>

The `ctype` locale category includes the following facets as if they
were specified in table [locale.category.facets] of [locale.category].

``` cpp
codecvt<char16_t, char, mbstate_t>
codecvt<char32_t, char, mbstate_t>
```

The `ctype` locale category includes the following facets as if they
were specified in table [locale.spec] of [locale.category].

``` cpp
codecvt_byname<char16_t, char, mbstate_t>
codecvt_byname<char32_t, char, mbstate_t>
```

The following class template specializations are required in addition to
those specified in  [locale.codecvt]. The specialization
`codecvt<char16_t, char, mbstate_t>` converts between the UTF-16 and
UTF-8 encoding forms, and the specialization
`codecvt<char32_t, char, mbstate_t>` converts between the UTF-32 and
UTF-8 encoding forms.

## Deprecated filesystem path factory functions <a id="depr.fs.path.factory">[depr.fs.path.factory]</a>

``` cpp
template<class Source>
  path u8path(const Source& source);
template<class InputIterator>
  path u8path(InputIterator first, InputIterator last);
```

The `source` and \[`first`, `last`) sequences are UTF-8 encoded. The
value type of `Source` and `InputIterator` is `char` or . `Source` meets
the requirements specified in \[fs.path.req\].

***Returns:***

- If `value_type` is `char` and the current native narrow
  encoding\[fs.path.type.cvt\] is UTF-8, return `path(source)` or
  `path(first, last)`; otherwise,

- if `value_type` is and the native wide encoding is UTF-16, or if
  `value_type` is or , convert `source` or \[`first`, `last`) to a
  temporary, `tmp`, of type `string_type` and return `path(tmp)`;
  otherwise,

- convert `source` or \[`first`, `last`) to a temporary, `tmp`, of type
  `u32string` and return `path(tmp)`.

***Remarks:***

Argument format conversion\[fs.path.fmt.cvt\] applies to the arguments
for these functions. How Unicode encoding conversions are performed is
unspecified.

\[*Example 1*:

A string is to be read from a database that is encoded in UTF-8, and
used to create a directory using the native encoding for filenames:

    namespace fs = std::filesystem;
    std::string utf8_string = read_utf8_data();
    fs::create_directory(fs::u8path(utf8_string));

For POSIX-based operating systems with the native narrow encoding set to
UTF-8, no encoding or type conversion occurs.

For POSIX-based operating systems with the native narrow encoding not
set to UTF-8, a conversion to UTF-32 occurs, followed by a conversion to
the current native narrow encoding. Some Unicode characters may have no
native character set representation.

For Windows-based operating systems a conversion from UTF-8 to UTF-16
occurs.

— *end example*\]

\[*Note 1*: The example above is representative of a historical use of
`filesystem::u8path`. To indicate a UTF-8 encoding, passing a
`std::u8string` to `path`’s constructor is preferred as it is consistent
with `path`’s handling of other encodings. — *end note*\]

## Deprecated atomic operations <a id="depr.atomics">[depr.atomics]</a>

### General <a id="depr.atomics.general">[depr.atomics.general]</a>

The header has the following additions.

``` cpp
namespace std {
  template<class T>
    void atomic_init(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    void atomic_init(atomic<T>*, typename atomic<T>::value_type) noexcept;

  #define ATOMIC_VAR_INIT(value) see below
}
```

### Volatile access <a id="depr.atomics.volatile">[depr.atomics.volatile]</a>

If an `atomic` [atomics.types.generic] specialization has one of the
following overloads, then that overload participates in overload
resolution even if `atomic<T>::is_always_lock_free` is `false`:

``` cpp
void store(T desired, memory_order order = memory_order::seq_cst) volatile noexcept;
T operator=(T desired) volatile noexcept;
T load(memory_order order = memory_order::seq_cst) const volatile noexcept;
operator T() const volatile noexcept;
T exchange(T desired, memory_order order = memory_order::seq_cst) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order success, memory_order failure) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order success, memory_order failure) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order order = memory_order::seq_cst) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order::seq_cst) volatile noexcept;
T fetch_key(T operand, memory_order order = memory_order::seq_cst) volatile noexcept;
T operator op=(T operand) volatile noexcept;
T* fetch_key(ptrdiff_t operand, memory_order order = memory_order::seq_cst) volatile noexcept;
```

### Non-member functions <a id="depr.atomics.nonmembers">[depr.atomics.nonmembers]</a>

``` cpp
template<class T>
  void atomic_init(volatile atomic<T>* object, typename atomic<T>::value_type desired) noexcept;
template<class T>
  void atomic_init(atomic<T>* object, typename atomic<T>::value_type desired) noexcept;
```

***Effects:***

Equivalent to:
`atomic_store_explicit(object, desired, memory_order::relaxed);`

### Operations on atomic types <a id="depr.atomics.types.operations">[depr.atomics.types.operations]</a>

``` cpp
#define ATOMIC_VAR_INIT(value) see below
```

The macro expands to a token sequence suitable for constant
initialization of an atomic variable of static storage duration of a
type that is initialization-compatible with `value`.

\[*Note 1*: This operation possibly needs to initialize
locks. — *end note*\]

Concurrent access to the variable being initialized, even via an atomic
operation, constitutes a data race.

\[*Example 1*:

    atomic<int> v = ATOMIC_VAR_INIT(5);

— *end example*\]

<!-- Link reference definitions -->
[atomics.order]: thread.md#atomics.order
[cerrno.syn]: diagnostics.md#cerrno.syn
[default.allocator]: mem.md#default.allocator
[expr.ass]: expr.md#expr.ass
[locale.category]: localization.md#locale.category
[locale.codecvt]: localization.md#locale.codecvt
[mem.poly.allocator.mem]: mem.md#mem.poly.allocator.mem
[move.iter.elem]: iterators.md#move.iter.elem
[numeric.limits.general]: support.md#numeric.limits.general
[numeric.special]: support.md#numeric.special
[string.capacity]: strings.md#string.capacity
[structure.specifications]: library.md#structure.specifications
[system.error.syn]: diagnostics.md#system.error.syn
