# Input/output library <a id="input.output">[[input.output]]</a>

## General <a id="input.output.general">[[input.output.general]]</a>

This Clause describes components that C++ programs may use to perform
input/output operations.

The following subclauses describe requirements for stream parameters,
and components for forward declarations of iostreams, predefined
iostreams objects, base iostreams classes, stream buffering, stream
formatting and manipulators, string streams, and file streams, as
summarized in [[iostreams.summary]].

**Table: Input/output library summary** <a id="iostreams.summary">[iostreams.summary]</a>

| Subclause                  |                             | Header                                           |
| -------------------------- | --------------------------- | ------------------------------------------------ |
| [[iostreams.requirements]] | Requirements                |                                                  |
| [[iostream.forward]]       | Forward declarations        | `<iosfwd>`                                       |
| [[iostream.objects]]       | Standard iostream objects   | `<iostream>`                                     |
| [[iostreams.base]]         | Iostreams base classes      | `<ios>`                                          |
| [[stream.buffers]]         | Stream buffers              | `<streambuf>`                                    |
| [[iostream.format]]        | Formatting and manipulators | `<istream>`, `<ostream>`, `<iomanip>`, `<print>` |
| [[string.streams]]         | String streams              | `<sstream>`                                      |
| [[span.streams]]           | Span-based streams          | `<spanstream>`                                   |
| [[file.streams]]           | File streams                | `<fstream>`                                      |
| [[syncstream]]             | Synchronized output streams | `<syncstream>`                                   |
| [[filesystems]]            | File systems                | `<filesystem>`                                   |
| [[c.files]]                | C library files             | `<cstdio>`, `<cinttypes>`                        |


## Iostreams requirements <a id="iostreams.requirements">[[iostreams.requirements]]</a>

### Imbue limitations <a id="iostream.limits.imbue">[[iostream.limits.imbue]]</a>

No function described in [[input.output]] except for `ios_base::imbue`
and `basic_filebuf::pubimbue` causes any instance of `basic_ios::imbue`
or `basic_streambuf::imbue` to be called. If any user function called
from a function declared in [[input.output]] or as an overriding virtual
function of any class declared in [[input.output]] calls `imbue`, the
behavior is undefined.

### Types <a id="stream.types">[[stream.types]]</a>

``` cpp
using streamoff = implementation-defined  // type of streamoff;
```

The type `streamoff` is a synonym for one of the signed basic integral
types of sufficient size to represent the maximum possible file size for
the operating system.[^1]

``` cpp
using streamsize = implementation-defined;
```

The type `streamsize` is a synonym for one of the signed basic integral
types. It is used to represent the number of characters transferred in
an I/O operation, or the size of I/O buffers.[^2]

### Positioning type limitations <a id="iostreams.limits.pos">[[iostreams.limits.pos]]</a>

The classes of [[input.output]] with template arguments `charT` and
`traits` behave as described if `traits::pos_type` and
`traits::off_type` are `streampos` and `streamoff` respectively. Except
as noted explicitly below, their behavior when `traits::pos_type` and
`traits::off_type` are other types is *implementation-defined*.

[*Note 1*: For each of the specializations of `char_traits` defined in
[[char.traits.specializations]], `state_type` denotes `mbstate_t`,
`pos_type` denotes `fpos<mbstate_t>`, and `off_type` denotes
`streamoff`. — *end note*]

In the classes of [[input.output]], a template parameter with name
`charT` represents a member of the set of types containing `char`,
`wchar_t`, and any other *implementation-defined* character types that
meet the requirements for a character on which any of the iostream
components can be instantiated.

### Thread safety <a id="iostreams.threadsafety">[[iostreams.threadsafety]]</a>

Concurrent access to a stream object
[[string.streams]], [[file.streams]], stream buffer object
[[stream.buffers]], or C Library stream [[c.files]] by multiple threads
may result in a data race [[intro.multithread]] unless otherwise
specified [[iostream.objects]].

[*Note 1*: Data races result in undefined behavior
[[intro.multithread]]. — *end note*]

If one thread makes a library call *a* that writes a value to a stream
and, as a result, another thread reads this value from the stream
through a library call *b* such that this does not result in a data
race, then *a*’s write synchronizes with *b*’s read.

## Forward declarations <a id="iostream.forward">[[iostream.forward]]</a>

### Header `<iosfwd>` synopsis <a id="iosfwd.syn">[[iosfwd.syn]]</a>

``` cpp
namespace std {
  template<class charT> struct char_traits;
  template<> struct char_traits<char>;
  template<> struct char_traits<char8_t>;
  template<> struct char_traits<char16_t>;
  template<> struct char_traits<char32_t>;
  template<> struct char_traits<wchar_t>;

  template<class T> class allocator;

  template<class charT, class traits = char_traits<charT>>
    class basic_ios;
  template<class charT, class traits = char_traits<charT>>
    class basic_streambuf;
  template<class charT, class traits = char_traits<charT>>
    class basic_istream;
  template<class charT, class traits = char_traits<charT>>
    class basic_ostream;
  template<class charT, class traits = char_traits<charT>>
    class basic_iostream;

  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_stringbuf;
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_istringstream;
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_ostringstream;
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_stringstream;

  template<class charT, class traits = char_traits<charT>>
    class basic_spanbuf;
  template<class charT, class traits = char_traits<charT>>
    class basic_ispanstream;
  template<class charT, class traits = char_traits<charT>>
    class basic_ospanstream;
  template<class charT, class traits = char_traits<charT>>
    class basic_spanstream;

  template<class charT, class traits = char_traits<charT>>
    class basic_filebuf;
  template<class charT, class traits = char_traits<charT>>
    class basic_ifstream;
  template<class charT, class traits = char_traits<charT>>
    class basic_ofstream;
  template<class charT, class traits = char_traits<charT>>
    class basic_fstream;

  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_syncbuf;
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_osyncstream;

  template<class charT, class traits = char_traits<charT>>
    class istreambuf_iterator;
  template<class charT, class traits = char_traits<charT>>
    class ostreambuf_iterator;

  using ios  = basic_ios<char>;
  using wios = basic_ios<wchar_t>;

  using streambuf = basic_streambuf<char>;
  using istream   = basic_istream<char>;
  using ostream   = basic_ostream<char>;
  using iostream  = basic_iostream<char>;

  using stringbuf     = basic_stringbuf<char>;
  using istringstream = basic_istringstream<char>;
  using ostringstream = basic_ostringstream<char>;
  using stringstream  = basic_stringstream<char>;

  using spanbuf     = basic_spanbuf<char>;
  using ispanstream = basic_ispanstream<char>;
  using ospanstream = basic_ospanstream<char>;
  using spanstream  = basic_spanstream<char>;

  using filebuf  = basic_filebuf<char>;
  using ifstream = basic_ifstream<char>;
  using ofstream = basic_ofstream<char>;
  using fstream  = basic_fstream<char>;

  using syncbuf = basic_syncbuf<char>;
  using osyncstream = basic_osyncstream<char>;

  using wstreambuf = basic_streambuf<wchar_t>;
  using wistream   = basic_istream<wchar_t>;
  using wostream   = basic_ostream<wchar_t>;
  using wiostream  = basic_iostream<wchar_t>;

  using wstringbuf     = basic_stringbuf<wchar_t>;
  using wistringstream = basic_istringstream<wchar_t>;
  using wostringstream = basic_ostringstream<wchar_t>;
  using wstringstream  = basic_stringstream<wchar_t>;

  using wspanbuf     = basic_spanbuf<wchar_t>;
  using wispanstream = basic_ispanstream<wchar_t>;
  using wospanstream = basic_ospanstream<wchar_t>;
  using wspanstream  = basic_spanstream<wchar_t>;

  using wfilebuf  = basic_filebuf<wchar_t>;
  using wifstream = basic_ifstream<wchar_t>;
  using wofstream = basic_ofstream<wchar_t>;
  using wfstream  = basic_fstream<wchar_t>;

  using wsyncbuf = basic_syncbuf<wchar_t>;
  using wosyncstream = basic_osyncstream<wchar_t>;

  template<class state> class fpos;
  using streampos  = fpos<char_traits<char>::state_type>;
  using wstreampos = fpos<char_traits<wchar_t>::state_type>;
  using u8streampos = fpos<char_traits<char8_t>::state_type>;
  using u16streampos = fpos<char_traits<char16_t>::state_type>;
  using u32streampos = fpos<char_traits<char32_t>::state_type>;
}
```

Default template arguments are described as appearing both in `<iosfwd>`
and in the synopsis of other headers but it is well-formed to include
both `<iosfwd>` and one or more of the other headers.[^3]

### Overview <a id="iostream.forward.overview">[[iostream.forward.overview]]</a>

The class template specialization `basic_ios<charT, traits>` serves as a
virtual base class for the class templates `basic_istream`,
`basic_ostream`, and class templates derived from them. `basic_iostream`
is a class template derived from both `basic_istream<charT, traits>` and
`basic_ostream<charT, traits>`.

The class template specialization `basic_streambuf<charT, traits>`
serves as a base class for class templates `basic_stringbuf`,
`basic_filebuf`, and `basic_syncbuf`.

The class template specialization `basic_istream<charT, traits>` serves
as a base class for class templates `basic_istringstream` and
`basic_ifstream`.

The class template specialization `basic_ostream<charT, traits>` serves
as a base class for class templates `basic_ostringstream`,
`basic_ofstream`, and `basic_osyncstream`.

The class template specialization `basic_iostream<charT, traits>` serves
as a base class for class templates `basic_stringstream` and
`basic_fstream`.

[*Note 1*: For each of the class templates above, the program is
ill-formed if `traits::char_type` is not the same type as `charT`
[[char.traits]]. — *end note*]

Other *typedef-name*s define instances of class templates specialized
for `char` or `wchar_t` types.

Specializations of the class template `fpos` are used for specifying
file position information.

[*Example 1*: The types `streampos` and `wstreampos` are used for
positioning streams specialized on `char` and `wchar_t`
respectively. — *end example*]

[*Note 2*: This synopsis suggests a circularity between `streampos` and
`char_traits<char>`. An implementation can avoid this circularity by
substituting equivalent types. — *end note*]

## Standard iostream objects <a id="iostream.objects">[[iostream.objects]]</a>

### Header `<iostream>` synopsis <a id="iostream.syn">[[iostream.syn]]</a>

``` cpp
#include <ios>          // see [ios.syn]
#include <streambuf>    // see [streambuf.syn]
#include <istream>      // see [istream.syn]
#include <ostream>      // see [ostream.syn]

namespace std {
  extern istream cin;
  extern ostream cout;
  extern ostream cerr;
  extern ostream clog;

  extern wistream wcin;
  extern wostream wcout;
  extern wostream wcerr;
  extern wostream wclog;
}
```

### Overview <a id="iostream.objects.overview">[[iostream.objects.overview]]</a>

In this Clause, the type name `FILE` refers to the type `FILE` declared
in `<cstdio>`.

The header `<iostream>` declares objects that associate objects with the
standard C streams provided for by the functions declared in `<cstdio>`,
and includes all the headers necessary to use these objects.

The objects are constructed and the associations are established at some
time prior to or during the first time an object of class
`ios_base::Init` is constructed, and in any case before the body of
`main` [[basic.start.main]] begins execution. The objects are not
destroyed during program execution.[^4]

*Recommended practice:* If it is possible for them to do so,
implementations should initialize the objects earlier than required.

The results of including `<iostream>` in a translation unit shall be as
if `<iostream>` defined an instance of `ios_base::Init` with static
storage duration. Each C++ library module [[std.modules]] in a hosted
implementation shall behave as if it contains an interface unit that
defines an unexported `ios_base::Init` variable with ordered
initialization [[basic.start.dynamic]].

[*Note 1*: As a result, the definition of that variable is
appearance-ordered before any declaration following the point of
importation of a C++ library module. Whether such a definition exists is
unobservable by a program that does not reference any of the standard
iostream objects. — *end note*]

Mixing operations on corresponding wide- and narrow-character streams
follows the same semantics as mixing such operations on `FILE`s, as
specified in the C standard library.

Concurrent access to a synchronized [[ios.members.static]] standard
iostream object’s formatted and unformatted input [[istream]] and output
[[ostream]] functions or a standard C stream by multiple threads does
not result in a data race [[intro.multithread]].

[*Note 2*: Unsynchronized concurrent use of these objects and streams
by multiple threads can result in interleaved characters. — *end note*]

See also: ISO C 7.21.2

### Narrow stream objects <a id="narrow.stream.objects">[[narrow.stream.objects]]</a>

``` cpp
istream cin;
```

The object `cin` controls input from a stream buffer associated with the
object `stdin`, declared in `<cstdio>`.

After the object `cin` is initialized, `cin.tie()` returns `&cout`. Its
state is otherwise the same as required for
`basic_ios<char>::init`[[basic.ios.cons]].

``` cpp
ostream cout;
```

The object `cout` controls output to a stream buffer associated with the
object `stdout`, declared in `<cstdio>`.

``` cpp
ostream cerr;
```

The object `cerr` controls output to a stream buffer associated with the
object `stderr`, declared in `<cstdio>`.

After the object `cerr` is initialized, `cerr.flags() & unitbuf` is
nonzero and `cerr.tie()` returns `&cout`. Its state is otherwise the
same as required for `basic_ios<char>::init`[[basic.ios.cons]].

``` cpp
ostream clog;
```

The object `clog` controls output to a stream buffer associated with the
object `stderr`, declared in `<cstdio>`.

### Wide stream objects <a id="wide.stream.objects">[[wide.stream.objects]]</a>

``` cpp
wistream wcin;
```

The object `wcin` controls input from a stream buffer associated with
the object `stdin`, declared in `<cstdio>`.

After the object `wcin` is initialized, `wcin.tie()` returns `&wcout`.
Its state is otherwise the same as required for
`basic_ios<wchar_t>::init`[[basic.ios.cons]].

``` cpp
wostream wcout;
```

The object `wcout` controls output to a stream buffer associated with
the object `stdout`, declared in `<cstdio>`.

``` cpp
wostream wcerr;
```

The object `wcerr` controls output to a stream buffer associated with
the object `stderr`, declared in `<cstdio>`.

After the object `wcerr` is initialized, `wcerr.flags() & unitbuf` is
nonzero and `wcerr.tie()` returns `&wcout`. Its state is otherwise the
same as required for `basic_ios<wchar_t>::init`[[basic.ios.cons]].

``` cpp
wostream wclog;
```

The object `wclog` controls output to a stream buffer associated with
the object `stderr`, declared in `<cstdio>`.

## Iostreams base classes <a id="iostreams.base">[[iostreams.base]]</a>

### Header `<ios>` synopsis <a id="ios.syn">[[ios.syn]]</a>

``` cpp
#include <iosfwd>   // see [iosfwd.syn]

namespace std {
  using streamoff  = implementation-defined;
  using streamsize = implementation-defined;
  template<class stateT> class fpos;

  class ios_base;
  template<class charT, class traits = char_traits<charT>>
    class basic_ios;

  // [std.ios.manip], manipulators
  ios_base& boolalpha  (ios_base& str);
  ios_base& noboolalpha(ios_base& str);

  ios_base& showbase   (ios_base& str);
  ios_base& noshowbase (ios_base& str);

  ios_base& showpoint  (ios_base& str);
  ios_base& noshowpoint(ios_base& str);

  ios_base& showpos    (ios_base& str);
  ios_base& noshowpos  (ios_base& str);

  ios_base& skipws     (ios_base& str);
  ios_base& noskipws   (ios_base& str);

  ios_base& uppercase  (ios_base& str);
  ios_base& nouppercase(ios_base& str);

  ios_base& unitbuf    (ios_base& str);
  ios_base& nounitbuf  (ios_base& str);

  // [adjustfield.manip], adjustfield
  ios_base& internal   (ios_base& str);
  ios_base& left       (ios_base& str);
  ios_base& right      (ios_base& str);

  // [basefield.manip], basefield
  ios_base& dec        (ios_base& str);
  ios_base& hex        (ios_base& str);
  ios_base& oct        (ios_base& str);

  // [floatfield.manip], floatfield
  ios_base& fixed      (ios_base& str);
  ios_base& scientific (ios_base& str);
  ios_base& hexfloat   (ios_base& str);
  ios_base& defaultfloat(ios_base& str);

  // [error.reporting], error reporting
  enum class io_errc {
    stream = 1
  };

  template<> struct is_error_code_enum<io_errc> : public true_type { };
  error_code make_error_code(io_errc e) noexcept;
  error_condition make_error_condition(io_errc e) noexcept;
  const error_category& iostream_category() noexcept;
}
```

### Class `ios_base` <a id="ios.base">[[ios.base]]</a>

#### General <a id="ios.base.general">[[ios.base.general]]</a>

``` cpp
namespace std {
  class ios_base {
  public:
    class failure;              // see below

    // [ios.fmtflags], fmtflags
    using fmtflags = T1;
    static constexpr fmtflags boolalpha = unspecified;
    static constexpr fmtflags dec = unspecified;
    static constexpr fmtflags fixed = unspecified;
    static constexpr fmtflags hex = unspecified;
    static constexpr fmtflags internal = unspecified;
    static constexpr fmtflags left = unspecified;
    static constexpr fmtflags oct = unspecified;
    static constexpr fmtflags right = unspecified;
    static constexpr fmtflags scientific = unspecified;
    static constexpr fmtflags showbase = unspecified;
    static constexpr fmtflags showpoint = unspecified;
    static constexpr fmtflags showpos = unspecified;
    static constexpr fmtflags skipws = unspecified;
    static constexpr fmtflags unitbuf = unspecified;
    static constexpr fmtflags uppercase = unspecified;
    static constexpr fmtflags adjustfield = see below;
    static constexpr fmtflags basefield = see below;
    static constexpr fmtflags floatfield = see below;

    // [ios.iostate], iostate
    using iostate = T2;
    static constexpr iostate badbit = unspecified;
    static constexpr iostate eofbit = unspecified;
    static constexpr iostate failbit = unspecified;
    static constexpr iostate goodbit = see below;

    // [ios.openmode], openmode
    using openmode = T3;
    static constexpr openmode app = unspecified;
    static constexpr openmode ate = unspecified;
    static constexpr openmode binary = unspecified;
    static constexpr openmode in = unspecified;
    static constexpr openmode noreplace = unspecified;
    static constexpr openmode out = unspecified;
    static constexpr openmode trunc = unspecified;

    // [ios.seekdir], seekdir
    using seekdir = T4;
    static constexpr seekdir beg = unspecified;
    static constexpr seekdir cur = unspecified;
    static constexpr seekdir end = unspecified;

    class Init;

    // [fmtflags.state], fmtflags state
    fmtflags flags() const;
    fmtflags flags(fmtflags fmtfl);
    fmtflags setf(fmtflags fmtfl);
    fmtflags setf(fmtflags fmtfl, fmtflags mask);
    void unsetf(fmtflags mask);

    streamsize precision() const;
    streamsize precision(streamsize prec);
    streamsize width() const;
    streamsize width(streamsize wide);

    // [ios.base.locales], locales
    locale imbue(const locale& loc);
    locale getloc() const;

    // [ios.base.storage], storage
    static int xalloc();
    long&  iword(int idx);
    void*& pword(int idx);

    // destructor
    virtual ~ios_base();

    // [ios.base.callback], callbacks
    enum event { erase_event, imbue_event, copyfmt_event };
    using event_callback = void (*)(event, ios_base&, int idx);
    void register_callback(event_callback fn, int idx);

    ios_base(const ios_base&) = delete;
    ios_base& operator=(const ios_base&) = delete;

    static bool sync_with_stdio(bool sync = true);

  protected:
    ios_base();

  private:
    static int index;           // exposition only
    long*  iarray;              // exposition only
    void** parray;              // exposition only
  };
}
```

`ios_base`

defines several member types:

- a type `failure`, defined as either a class derived from
  `system_error` or a synonym for a class derived from `system_error`;
- a class `Init`;
- three bitmask types, `fmtflags`, `iostate`, and `openmode`;
- an enumerated type, `seekdir`.

It maintains several kinds of data:

- state information that reflects the integrity of the stream buffer;
- control information that influences how to interpret (format) input
  sequences and how to generate (format) output sequences;
- additional information that is stored by the program for its private
  use.

[*Note 1*:

For the sake of exposition, the maintained data is presented here as:

- `static int index`, specifies the next available unique index for the
  integer or pointer arrays maintained for the private use of the
  program, initialized to an unspecified value;
- `long* iarray`, points to the first element of an arbitrary-length
  `long` array maintained for the private use of the program;
- `void** parray`, points to the first element of an arbitrary-length
  pointer array maintained for the private use of the program.

— *end note*]

#### Types <a id="ios.types">[[ios.types]]</a>

##### Class `ios_base::failure` <a id="ios.failure">[[ios.failure]]</a>

``` cpp
namespace std {
  class ios_base::failure : public system_error {
  public:
    explicit failure(const string& msg, const error_code& ec = io_errc::stream);
    explicit failure(const char* msg, const error_code& ec = io_errc::stream);
  };
}
```

An implementation is permitted to define `ios_base::failure` as a
synonym for a class with equivalent functionality to class
`ios_base::failure` shown in this subclause.

[*Note 1*: When `ios_base::failure` is a synonym for another type, that
type is required to provide a nested type `failure` to emulate the
injected-class-name. — *end note*]

The class `failure` defines the base class for the types of all objects
thrown as exceptions, by functions in the iostreams library, to report
errors detected during stream buffer operations.

When throwing `ios_base::failure` exceptions, implementations should
provide values of `ec` that identify the specific reason for the
failure.

[*Note 2*: Errors arising from the operating system would typically be
reported as `system_category()` errors with an error value of the error
number reported by the operating system. Errors arising from within the
stream library would typically be reported as
`error_code(io_errc::stream,
iostream_category())`. — *end note*]

``` cpp
explicit failure(const string& msg, const error_code& ec = io_errc::stream);
```

*Effects:* Constructs the base class with `msg` and `ec`.

``` cpp
explicit failure(const char* msg, const error_code& ec = io_errc::stream);
```

*Effects:* Constructs the base class with `msg` and `ec`.

##### Type `ios_base::fmtflags` <a id="ios.fmtflags">[[ios.fmtflags]]</a>

``` cpp
using fmtflags = T1;
```

The type `fmtflags` is a bitmask type [[bitmask.types]]. Setting its
elements has the effects indicated in [[ios.fmtflags]].

**Table: `fmtflags` effects** <a id="ios.fmtflags">[ios.fmtflags]</a>

| Element      | Effect(s) if set                                                                                                                        |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `boolalpha`  | insert and extract `bool` type in alphabetic format                                                                                     |
| `dec`        | converts integer input or generates integer output in decimal base                                                                      |
| `fixed`      | generate floating-point output in fixed-point notation                                                                                  |
| `hex`        | converts integer input or generates integer output in hexadecimal base                                                                  |
| `internal`   | adds fill characters at a designated internal point in certain generated output, or identical to `right` if no such point is designated |
| `left`       | adds fill characters on the right (final positions) of certain generated output                                                         |
| `oct`        | converts integer input or generates integer output in octal base                                                                        |
| `right`      | adds fill characters on the left (initial positions) of certain generated output                                                        |
| `scientific` | generates floating-point output in scientific notation                                                                                  |
| `showbase`   | generates a prefix indicating the numeric base of generated integer output                                                              |
| `showpoint`  | generates a decimal-point character unconditionally in generated floating-point output                                                  |
| `showpos`    | generates a `+` sign in non-negative generated numeric output                                                                           |
| `skipws`     | skips leading whitespace before certain input operations                                                                                |
| `unitbuf`    | flushes output after each output operation                                                                                              |
| `uppercase`  | replaces certain lowercase letters with their uppercase equivalents in generated output                                                 |


Type `fmtflags` also defines the constants indicated in
[[ios.fmtflags.const]].

**Table: `fmtflags` constants** <a id="ios.fmtflags.const">[ios.fmtflags.const]</a>

| Constant      | Allowable values          |
| ------------- | ------------------------- |
| `adjustfield` | `left | right | internal` |
| `basefield`   | `dec | oct | hex`         |
| `floatfield`  | `scientific | fixed`      |


##### Type `ios_base::iostate` <a id="ios.iostate">[[ios.iostate]]</a>

``` cpp
using iostate = T2;
```

The type `iostate` is a bitmask type [[bitmask.types]] that contains the
elements indicated in [[ios.iostate]].

**Table: `iostate` effects** <a id="ios.iostate">[ios.iostate]</a>

| Element   | Effect(s) if set                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `badbit`  | indicates a loss of integrity in an input or output sequence (such as an irrecoverable read error from a file);                                  |
| `eofbit`  | indicates that an input operation reached the end of an input sequence;                                                                          |
| `failbit` | indicates that an input operation failed to read the expected characters, or that an output operation failed to generate the desired characters. |


Type `iostate` also defines the constant:

- `goodbit`, the value zero.

##### Type `ios_base::openmode` <a id="ios.openmode">[[ios.openmode]]</a>

``` cpp
using openmode = T3;
```

The type `openmode` is a bitmask type [[bitmask.types]]. It contains the
elements indicated in [[ios.openmode]].

**Table: `openmode` effects** <a id="ios.openmode">[ios.openmode]</a>

| Element     | Effect(s) if set                                                  |
| ----------- | ----------------------------------------------------------------- |
| `app`       | seek to end before each write                                     |
| `ate`       | open and seek to end immediately after opening                    |
| `binary`    | perform input and output in binary mode (as opposed to text mode) |
| `in`        | open for input                                                    |
| `noreplace` | open in exclusive mode                                            |
| `out`       | open for output                                                   |
| `trunc`     | truncate an existing stream when opening                          |


##### Type `ios_base::seekdir` <a id="ios.seekdir">[[ios.seekdir]]</a>

``` cpp
using seekdir = T4;
```

The type `seekdir` is an enumerated type [[enumerated.types]] that
contains the elements indicated in [[ios.seekdir]].

**Table: `seekdir` effects** <a id="ios.seekdir">[ios.seekdir]</a>

| Element | Meaning                                                                                 |
| ------- | --------------------------------------------------------------------------------------- |
| `beg`   | request a seek (for subsequent input or output) relative to the beginning of the stream |
| `cur`   | request a seek relative to the current position within the sequence                     |
| `end`   | request a seek relative to the current end of the sequence                              |


##### Class `ios_base::Init` <a id="ios.init">[[ios.init]]</a>

``` cpp
namespace std {
  class ios_base::Init {
  public:
    Init();
    Init(const Init&) = default;
    ~Init();
    Init& operator=(const Init&) = default;

  private:
    static int init_cnt;        // exposition only
  };
}
```

The class `Init` describes an object whose construction ensures the
construction of the eight objects declared in `<iostream>`
[[iostream.objects]] that associate file stream buffers with the
standard C streams provided for by the functions declared in `<cstdio>`.

For the sake of exposition, the maintained data is presented here as:

- `static int init_cnt`, counts the number of constructor and destructor
  calls for class `Init`, initialized to zero.

``` cpp
Init();
```

*Effects:* Constructs and initializes the objects `cin`, `cout`, `cerr`,
`clog`, `wcin`, `wcout`, `wcerr`, and `wclog` if they have not already
been constructed and initialized.

``` cpp
~Init();
```

*Effects:* If there are no other instances of the class still in
existence, calls `cout.flush()`, `cerr.flush()`, `clog.flush()`,
`wcout.flush()`, `wcerr.flush()`, `wclog.flush()`.

#### State functions <a id="fmtflags.state">[[fmtflags.state]]</a>

``` cpp
fmtflags flags() const;
```

*Returns:* The format control information for both input and output.

``` cpp
fmtflags flags(fmtflags fmtfl);
```

*Ensures:* `fmtfl == flags()`.

*Returns:* The previous value of `flags()`.

``` cpp
fmtflags setf(fmtflags fmtfl);
```

*Effects:* Sets `fmtfl` in `flags()`.

*Returns:* The previous value of `flags()`.

``` cpp
fmtflags setf(fmtflags fmtfl, fmtflags mask);
```

*Effects:* Clears `mask` in `flags()`, sets `fmtfl & mask` in `flags()`.

*Returns:* The previous value of `flags()`.

``` cpp
void unsetf(fmtflags mask);
```

*Effects:* Clears `mask` in `flags()`.

``` cpp
streamsize precision() const;
```

*Returns:* The precision to generate on certain output conversions.

``` cpp
streamsize precision(streamsize prec);
```

*Ensures:* `prec == precision()`.

*Returns:* The previous value of `precision()`.

``` cpp
streamsize width() const;
```

*Returns:* The minimum field width (number of characters) to generate on
certain output conversions.

``` cpp
streamsize width(streamsize wide);
```

*Ensures:* `wide == width()`.

*Returns:* The previous value of `width()`.

#### Functions <a id="ios.base.locales">[[ios.base.locales]]</a>

``` cpp
locale imbue(const locale& loc);
```

*Effects:* Calls each registered callback pair
`(fn, idx)`[[ios.base.callback]] as `(*fn)(imbue_event, *this, idx)` at
such a time that a call to `ios_base::getloc()` from within `fn` returns
the new locale value `loc`.

*Ensures:* `loc == getloc()`.

*Returns:* The previous value of `getloc()`.

``` cpp
locale getloc() const;
```

*Returns:* If no locale has been imbued, a copy of the global C++
locale, `locale()`, in effect at the time of construction. Otherwise,
returns the imbued locale, to be used to perform locale-dependent input
and output operations.

#### Static members <a id="ios.members.static">[[ios.members.static]]</a>

``` cpp
static bool sync_with_stdio(bool sync = true);
```

*Effects:* If any input or output operation has occurred using the
standard streams prior to the call, the effect is
*implementation-defined*. Otherwise, called with a `false` argument, it
allows the standard streams to operate independently of the standard C
streams.

*Returns:* `true` if the previous state of the standard iostream
objects [[iostream.objects]] was synchronized and otherwise returns
`false`. The first time it is called, the function returns `true`.

*Remarks:* When a standard iostream object `str` is *synchronized* with
a standard stdio stream `f`, the effect of inserting a character `c` by

``` cpp
fputc(f, c);
```

is the same as the effect of

``` cpp
str.rdbuf()->sputc(c);
```

for any sequences of characters; the effect of extracting a character
`c` by

``` cpp
c = fgetc(f);
```

is the same as the effect of

``` cpp
c = str.rdbuf()->sbumpc();
```

for any sequences of characters; and the effect of pushing back a
character `c` by

``` cpp
ungetc(c, f);
```

is the same as the effect of

``` cpp
str.rdbuf()->sputbackc(c);
```

for any sequence of characters.[^5]

#### Storage functions <a id="ios.base.storage">[[ios.base.storage]]</a>

``` cpp
static int xalloc();
```

*Returns:* `index` `++`.

*Remarks:* Concurrent access to this function by multiple threads does
not result in a data race [[intro.multithread]].

``` cpp
long& iword(int idx);
```

*Preconditions:* `idx` is a value obtained by a call to `xalloc`.

*Effects:* If `iarray` is a null pointer, allocates an array of `long`
of unspecified size and stores a pointer to its first element in
`iarray`. The function then extends the array pointed at by `iarray` as
necessary to include the element `iarray[idx]`. Each newly allocated
element of the array is initialized to zero. The reference returned is
invalid after any other operation on the object.[^6]

However, the value of the storage referred to is retained, so that until
the next call to `copyfmt`, calling `iword` with the same index yields
another reference to the same value. If the function fails[^7]

and `*this` is a base class subobject of a `basic_ios<>` object or
subobject, the effect is equivalent to calling
`basic_ios<>::setstate(badbit)` on the derived object (which may throw
`failure`).

*Returns:* On success `iarray[idx]`. On failure, a valid `long&`
initialized to 0.

``` cpp
void*& pword(int idx);
```

*Preconditions:* `idx` is a value obtained by a call to `xalloc`.

*Effects:* If `parray` is a null pointer, allocates an array of pointers
to `void` of unspecified size and stores a pointer to its first element
in `parray`. The function then extends the array pointed at by `parray`
as necessary to include the element `parray[idx]`. Each newly allocated
element of the array is initialized to a null pointer. The reference
returned is invalid after any other operation on the object. However,
the value of the storage referred to is retained, so that until the next
call to `copyfmt`, calling `pword` with the same index yields another
reference to the same value. If the function fails[^8]

and `*this` is a base class subobject of a `basic_ios<>` object or
subobject, the effect is equivalent to calling
`basic_ios<>::setstate(badbit)` on the derived object (which may throw
`failure`).

*Returns:* On success `parray[idx]`. On failure a valid `void*&`
initialized to 0.

*Remarks:* After a subsequent call to `pword(int)` for the same object,
the earlier return value may no longer be valid.

#### Callbacks <a id="ios.base.callback">[[ios.base.callback]]</a>

``` cpp
void register_callback(event_callback fn, int idx);
```

*Preconditions:* The function `fn` does not throw exceptions.

*Effects:* Registers the pair `(fn, idx)` such that during calls to
`imbue()`[[ios.base.locales]], `copyfmt()`, or
`~ios_base()`[[ios.base.cons]], the function `fn` is called with
argument `idx`. Functions registered are called when an event occurs, in
opposite order of registration. Functions registered while a callback
function is active are not called until the next event.

*Remarks:* Identical pairs are not merged. A function registered twice
will be called twice.

#### Constructors and destructor <a id="ios.base.cons">[[ios.base.cons]]</a>

``` cpp
ios_base();
```

*Effects:* Each `ios_base` member has an indeterminate value after
construction. The object’s members shall be initialized by calling
`basic_ios::init` before the object’s first use or before it is
destroyed, whichever comes first; otherwise the behavior is undefined.

``` cpp
~ios_base();
```

*Effects:* Calls each registered callback pair
`(fn, idx)`[[ios.base.callback]] as `(*fn)(erase_event, *this, idx)` at
such time that any `ios_base` member function called from within `fn`
has well-defined results. Then, any memory obtained is deallocated.

### Class template `fpos` <a id="fpos">[[fpos]]</a>

``` cpp
namespace std {
  template<class stateT> class fpos {
  public:
    // [fpos.members], members
    stateT state() const;
    void state(stateT);

  private:
    stateT st;                  // exposition only
  };
}
```

#### Members <a id="fpos.members">[[fpos.members]]</a>

``` cpp
void state(stateT s);
```

*Effects:* Assigns `s` to `st`.

``` cpp
stateT state() const;
```

*Returns:* Current value of `st`.

#### Requirements <a id="fpos.operations">[[fpos.operations]]</a>

An `fpos` type specifies file position information. It holds a state
object whose type is equal to the template parameter `stateT`. Type
`stateT` shall meet the *Cpp17DefaultConstructible* (
[[cpp17.defaultconstructible]]), *Cpp17CopyConstructible* (
[[cpp17.copyconstructible]]), *Cpp17CopyAssignable* (
[[cpp17.copyassignable]]), and *Cpp17Destructible* (
[[cpp17.destructible]]) requirements. If
`is_trivially_copy_constructible_v<stateT>` is `true`, then
`fpos<stateT>` has a trivial copy constructor. If
`is_trivially_copy_assignable_v<stateT>` is `true`, then `fpos<stateT>`
has a trivial copy assignment operator. If
`is_trivially_destructible_v<stateT>` is `true`, then `fpos<stateT>` has
a trivial destructor. All specializations of `fpos` meet the
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*,
*Cpp17CopyAssignable*, *Cpp17Destructible*, and
*Cpp17EqualityComparable* ([[cpp17.equalitycomparable]]) requirements.
In addition, the expressions shown in [[fpos.operations]] are valid and
have the indicated semantics. In that table,

- `P` refers to a specialization of `fpos`,
- `p` and `q` refer to values of type `P` or `const P`,
- `pl` and `ql` refer to modifiable lvalues of type `P`,
- `O` refers to type `streamoff`, and
- `o` and `o2` refer to values of type `streamoff` or `const streamoff`.

Stream operations that return a value of type `traits::pos_type` return
`P(O(-1))` as an invalid value to signal an error. If this value is used
as an argument to any `istream`, `ostream`, or `streambuf` member that
accepts a value of type `traits::pos_type` then the behavior of that
function is undefined.

### Class template `basic_ios` <a id="ios">[[ios]]</a>

#### Overview <a id="ios.overview">[[ios.overview]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_ios : public ios_base {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [iostate.flags], flags functions
    explicit operator bool() const;
    bool operator!() const;
    iostate rdstate() const;
    void clear(iostate state = goodbit);
    void setstate(iostate state);
    bool good() const;
    bool eof()  const;
    bool fail() const;
    bool bad()  const;

    iostate exceptions() const;
    void exceptions(iostate except);

    // [basic.ios.cons], constructor/destructor
    explicit basic_ios(basic_streambuf<charT, traits>* sb);
    virtual ~basic_ios();

    // [basic.ios.members], members
    basic_ostream<charT, traits>* tie() const;
    basic_ostream<charT, traits>* tie(basic_ostream<charT, traits>* tiestr);

    basic_streambuf<charT, traits>* rdbuf() const;
    basic_streambuf<charT, traits>* rdbuf(basic_streambuf<charT, traits>* sb);

    basic_ios& copyfmt(const basic_ios& rhs);

    char_type fill() const;
    char_type fill(char_type ch);

    locale imbue(const locale& loc);

    char      narrow(char_type c, char dfault) const;
    char_type widen(char c) const;

    basic_ios(const basic_ios&) = delete;
    basic_ios& operator=(const basic_ios&) = delete;

  protected:
    basic_ios();
    void init(basic_streambuf<charT, traits>* sb);
    void move(basic_ios& rhs);
    void move(basic_ios&& rhs);
    void swap(basic_ios& rhs) noexcept;
    void set_rdbuf(basic_streambuf<charT, traits>* sb);
  };
}
```

#### Constructors <a id="basic.ios.cons">[[basic.ios.cons]]</a>

``` cpp
explicit basic_ios(basic_streambuf<charT, traits>* sb);
```

*Effects:* Assigns initial values to its member objects by calling
`init(sb)`.

``` cpp
basic_ios();
```

*Effects:* Leaves its member objects uninitialized. The object shall be
initialized by calling `basic_ios::init` before its first use or before
it is destroyed, whichever comes first; otherwise the behavior is
undefined.

``` cpp
~basic_ios();
```

*Remarks:* The destructor does not destroy `rdbuf()`.

``` cpp
void init(basic_streambuf<charT, traits>* sb);
```

*Ensures:* The postconditions of this function are indicated in
[[basic.ios.cons]].

**Table: `basic_ios::init()` effects** <a id="basic.ios.cons">[basic.ios.cons]</a>

| Element        | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| `rdbuf()`      | `sb`                                                         |
| `tie()`        | `0`                                                          |
| `rdstate()`    | `goodbit` if `sb` is not a null pointer, otherwise `badbit`. |
| `exceptions()` | `goodbit`                                                    |
| `flags()`      | `skipws | dec`                                               |
| `width()`      | `0`                                                          |
| `precision()`  | `6`                                                          |
| `fill()`       | `widen(' ')`                                                 |
| `getloc()`     | a copy of the value returned by `locale()`                   |
| `iarray`       | a null pointer                                               |
| `parray`       | a null pointer                                               |


#### Member functions <a id="basic.ios.members">[[basic.ios.members]]</a>

``` cpp
basic_ostream<charT, traits>* tie() const;
```

*Returns:* An output sequence that is *tied* to (synchronized with) the
sequence controlled by the stream buffer.

``` cpp
basic_ostream<charT, traits>* tie(basic_ostream<charT, traits>* tiestr);
```

*Preconditions:* If `tiestr` is not null, `tiestr` is not reachable by
traversing the linked list of tied stream objects starting from
`tiestr->tie()`.

*Ensures:* `tiestr == tie()`.

*Returns:* The previous value of `tie()`.

``` cpp
basic_streambuf<charT, traits>* rdbuf() const;
```

*Returns:* A pointer to the `streambuf` associated with the stream.

``` cpp
basic_streambuf<charT, traits>* rdbuf(basic_streambuf<charT, traits>* sb);
```

*Effects:* Calls `clear()`.

*Ensures:* `sb == rdbuf()`.

*Returns:* The previous value of `rdbuf()`.

``` cpp
locale imbue(const locale& loc);
```

*Effects:* Calls `ios_base::imbue(loc)`[[ios.base.locales]] and if
`rdbuf() != 0` then `rdbuf()->pubimbue(loc)`[[streambuf.locales]].

*Returns:* The prior value of `ios_base::imbue()`.

``` cpp
char narrow(char_type c, char dfault) const;
```

*Returns:* `use_facet<ctype<char_type>>(getloc()).narrow(c, dfault)`

``` cpp
char_type widen(char c) const;
```

*Returns:* `use_facet<ctype<char_type>>(getloc()).widen(c)`

``` cpp
char_type fill() const;
```

*Returns:* The character used to pad (fill) an output conversion to the
specified field width.

``` cpp
char_type fill(char_type fillch);
```

*Ensures:* `traits::eq(fillch, fill())`.

*Returns:* The previous value of `fill()`.

``` cpp
basic_ios& copyfmt(const basic_ios& rhs);
```

*Effects:* If `(this == addressof(rhs))` is `true` does nothing.
Otherwise assigns to the member objects of `*this` the corresponding
member objects of `rhs` as follows:

- calls each registered callback pair `(fn, idx)` as
  `(*fn)(erase_event, *this, idx)`;
- then, assigns to the member objects of `*this` the corresponding
  member objects of `rhs`, except that
  - `rdstate()`, `rdbuf()`, and `exceptions()` are left unchanged;
  - the contents of arrays pointed at by `pword` and `iword` are copied,
    not the pointers themselves;[^9] and
  - if any newly stored pointer values in `*this` point at objects
    stored outside the object `rhs` and those objects are destroyed when
    `rhs` is destroyed, the newly stored pointer values are altered to
    point at newly constructed copies of the objects;
- then, calls each callback pair that was copied from `rhs` as
  `(*fn)(copyfmt_event, *this, idx)`;
- then, calls `exceptions(rhs.exceptions())`.

[*Note 1*: The second pass through the callback pairs permits a copied
`pword` value to be zeroed, or to have its referent deep copied or
reference counted, or to have other special action taken. — *end note*]

*Ensures:* The postconditions of this function are indicated in
[[basic.ios.copyfmt]].

**Table: `basic_ios::copyfmt()` effects** <a id="basic.ios.copyfmt">[basic.ios.copyfmt]</a>

| Element        | Value              |
| -------------- | ------------------ |
| `rdbuf()`      | unchanged          |
| `tie()`        | `rhs.tie()`        |
| `rdstate()`    | unchanged          |
| `exceptions()` | `rhs.exceptions()` |
| `flags()`      | `rhs.flags()`      |
| `width()`      | `rhs.width()`      |
| `precision()`  | `rhs.precision()`  |
| `fill()`       | `rhs.fill()`       |
| `getloc()`     | `rhs.getloc()`     |


*Returns:* `*this`.

``` cpp
void move(basic_ios& rhs);
void move(basic_ios&& rhs);
```

*Ensures:* `*this` has the state that `rhs` had before the function
call, except that `rdbuf()` returns `nullptr`. `rhs` is in a valid but
unspecified state, except that `rhs.rdbuf()` returns the same value as
it returned before the function call, and `rhs.tie()` returns `nullptr`.

``` cpp
void swap(basic_ios& rhs) noexcept;
```

*Effects:* The states of `*this` and `rhs` are exchanged, except that
`rdbuf()` returns the same value as it returned before the function
call, and `rhs.rdbuf()` returns the same value as it returned before the
function call.

``` cpp
void set_rdbuf(basic_streambuf<charT, traits>* sb);
```

*Preconditions:* `sb != nullptr` is `true`.

*Effects:* Associates the `basic_streambuf` object pointed to by `sb`
with this stream without calling `clear()`.

*Ensures:* `rdbuf() == sb` is `true`.

*Throws:* Nothing.

#### Flags functions <a id="iostate.flags">[[iostate.flags]]</a>

``` cpp
explicit operator bool() const;
```

*Returns:* `!fail()`.

``` cpp
bool operator!() const;
```

*Returns:* `fail()`.

``` cpp
iostate rdstate() const;
```

*Returns:* The error state of the stream buffer.

``` cpp
void clear(iostate state = goodbit);
```

*Effects:* If
`((state | (rdbuf() ? goodbit : badbit)) & exceptions()) == 0`, returns.
Otherwise, the function throws an object of class
`ios_base::failure`[[ios.failure]], constructed with
*implementation-defined* argument values.

*Ensures:* If `rdbuf() != 0` then `state == rdstate()`; otherwise
`rdstate() == (state | ios_base::badbit)`.

``` cpp
void setstate(iostate state);
```

*Effects:* Calls `clear(rdstate() | state)` (which may throw
`ios_base::failure`[[ios.failure]]).

``` cpp
bool good() const;
```

*Returns:* `rdstate() == 0`

``` cpp
bool eof() const;
```

*Returns:* `true` if `eofbit` is set in `rdstate()`.

``` cpp
bool fail() const;
```

*Returns:* `true` if `failbit` or `badbit` is set in `rdstate()`.[^10]

``` cpp
bool bad() const;
```

*Returns:* `true` if `badbit` is set in `rdstate()`.

``` cpp
iostate exceptions() const;
```

*Returns:* A mask that determines what elements set in `rdstate()` cause
exceptions to be thrown.

``` cpp
void exceptions(iostate except);
```

*Effects:* Calls `clear(rdstate())`.

*Ensures:* `except == exceptions()`.

### `ios_base` manipulators <a id="std.ios.manip">[[std.ios.manip]]</a>

#### `fmtflags` manipulators <a id="fmtflags.manip">[[fmtflags.manip]]</a>

Each function specified in this subclause is a designated addressable
function [[namespace.std]].

``` cpp
ios_base& boolalpha(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::boolalpha)`.

*Returns:* `str`.

``` cpp
ios_base& noboolalpha(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::boolalpha)`.

*Returns:* `str`.

``` cpp
ios_base& showbase(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::showbase)`.

*Returns:* `str`.

``` cpp
ios_base& noshowbase(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::showbase)`.

*Returns:* `str`.

``` cpp
ios_base& showpoint(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::showpoint)`.

*Returns:* `str`.

``` cpp
ios_base& noshowpoint(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::showpoint)`.

*Returns:* `str`.

``` cpp
ios_base& showpos(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::showpos)`.

*Returns:* `str`.

``` cpp
ios_base& noshowpos(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::showpos)`.

*Returns:* `str`.

``` cpp
ios_base& skipws(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::skipws)`.

*Returns:* `str`.

``` cpp
ios_base& noskipws(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::skipws)`.

*Returns:* `str`.

``` cpp
ios_base& uppercase(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::uppercase)`.

*Returns:* `str`.

``` cpp
ios_base& nouppercase(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::uppercase)`.

*Returns:* `str`.

``` cpp
ios_base& unitbuf(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::unitbuf)`.

*Returns:* `str`.

``` cpp
ios_base& nounitbuf(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::unitbuf)`.

*Returns:* `str`.

#### `adjustfield` manipulators <a id="adjustfield.manip">[[adjustfield.manip]]</a>

Each function specified in this subclause is a designated addressable
function [[namespace.std]].

``` cpp
ios_base& internal(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::internal, ios_base::adjustfield)`.

*Returns:* `str`.

``` cpp
ios_base& left(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::left, ios_base::adjustfield)`.

*Returns:* `str`.

``` cpp
ios_base& right(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::right, ios_base::adjustfield)`.

*Returns:* `str`.

#### `basefield` manipulators <a id="basefield.manip">[[basefield.manip]]</a>

Each function specified in this subclause is a designated addressable
function [[namespace.std]].

``` cpp
ios_base& dec(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::dec, ios_base::basefield)`.

*Returns:* `str`.[^11]

``` cpp
ios_base& hex(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::hex, ios_base::basefield)`.

*Returns:* `str`.

``` cpp
ios_base& oct(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::oct, ios_base::basefield)`.

*Returns:* `str`.

#### `floatfield` manipulators <a id="floatfield.manip">[[floatfield.manip]]</a>

Each function specified in this subclause is a designated addressable
function [[namespace.std]].

``` cpp
ios_base& fixed(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::fixed, ios_base::floatfield)`.

*Returns:* `str`.

``` cpp
ios_base& scientific(ios_base& str);
```

*Effects:* Calls `str.setf(ios_base::scientific, ios_base::floatfield)`.

*Returns:* `str`.

``` cpp
ios_base& hexfloat(ios_base& str);
```

*Effects:* Calls
`str.setf(ios_base::fixed | ios_base::scientific, ios_base::floatfield)`.

*Returns:* `str`.

[*Note 1*: `ios_base::hex` cannot be used to specify a hexadecimal
floating-point format, because it is not part of `ios_base::floatfield`
([[ios.fmtflags.const]]). — *end note*]

``` cpp
ios_base& defaultfloat(ios_base& str);
```

*Effects:* Calls `str.unsetf(ios_base::floatfield)`.

*Returns:* `str`.

### Error reporting <a id="error.reporting">[[error.reporting]]</a>

``` cpp
error_code make_error_code(io_errc e) noexcept;
```

*Returns:* `error_code(static_cast<int>(e), iostream_category())`.

``` cpp
error_condition make_error_condition(io_errc e) noexcept;
```

*Returns:* `error_condition(static_cast<int>(e), iostream_category())`.

``` cpp
const error_category& iostream_category() noexcept;
```

*Returns:* A reference to an object of a type derived from class
`error_category`.

The object’s `default_error_condition` and `equivalent` virtual
functions shall behave as specified for the class `error_category`. The
object’s `name` virtual function shall return a pointer to the string
`"iostream"`.

## Stream buffers <a id="stream.buffers">[[stream.buffers]]</a>

### Header `<streambuf>` synopsis <a id="streambuf.syn">[[streambuf.syn]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
    class basic_streambuf;
  using streambuf  = basic_streambuf<char>;
  using wstreambuf = basic_streambuf<wchar_t>;
}
```

The header `<streambuf>` defines types that control input from and
output to *character* sequences.

### Stream buffer requirements <a id="streambuf.reqts">[[streambuf.reqts]]</a>

Stream buffers can impose various constraints on the sequences they
control. Some constraints are:

- The controlled input sequence can be not readable.
- The controlled output sequence can be not writable.
- The controlled sequences can be associated with the contents of other
  representations for character sequences, such as external files.
- The controlled sequences can support operations *directly* to or from
  associated sequences.
- The controlled sequences can impose limitations on how the program can
  read characters from a sequence, write characters to a sequence, put
  characters back into an input sequence, or alter the stream position.

Each sequence is characterized by three pointers which, if non-null, all
point into the same `charT` array object. The array object represents,
at any moment, a (sub)sequence of characters from the sequence.
Operations performed on a sequence alter the values stored in these
pointers, perform reads and writes directly to or from associated
sequences, and alter “the stream position” and conversion state as
needed to maintain this subsequence relationship. The three pointers
are:

- the *beginning pointer*, or lowest element address in the array
  (called `xbeg` here);
- the *next pointer*, or next element address that is a current
  candidate for reading or writing (called `xnext` here);
- the *end pointer*, or first element address beyond the end of the
  array (called `xend` here).

The following semantic constraints shall always apply for any set of
three pointers for a sequence, using the pointer names given immediately
above:

- If `xnext` is not a null pointer, then `xbeg` and `xend` shall also be
  non-null pointers into the same `charT` array, as described above;
  otherwise, `xbeg` and `xend` shall also be null.
- If `xnext` is not a null pointer and `xnext < xend` for an output
  sequence, then a *write position* is available. In this case, `*xnext`
  shall be assignable as the next element to write (to put, or to store
  a character value, into the sequence).
- If `xnext` is not a null pointer and `xbeg < xnext` for an input
  sequence, then a *putback position* is available. In this case,
  `xnext[-1]` shall have a defined value and is the next (preceding)
  element to store a character that is put back into the input sequence.
- If `xnext` is not a null pointer and `xnext < xend` for an input
  sequence, then a *read position* is available. In this case, `*xnext`
  shall have a defined value and is the next element to read (to get, or
  to obtain a character value, from the sequence).

### Class template `basic_streambuf` <a id="streambuf">[[streambuf]]</a>

#### General <a id="streambuf.general">[[streambuf.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_streambuf {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    virtual ~basic_streambuf();

    // [streambuf.locales], locales
    locale   pubimbue(const locale& loc);
    locale   getloc() const;

    // [streambuf.buffer], buffer and positioning
    basic_streambuf* pubsetbuf(char_type* s, streamsize n);
    pos_type pubseekoff(off_type off, ios_base::seekdir way,
                        ios_base::openmode which
                          = ios_base::in | ios_base::out);
    pos_type pubseekpos(pos_type sp,
                        ios_base::openmode which
                          = ios_base::in | ios_base::out);
    int      pubsync();

    // get and put areas
    // [streambuf.pub.get], get area
    streamsize in_avail();
    int_type snextc();
    int_type sbumpc();
    int_type sgetc();
    streamsize sgetn(char_type* s, streamsize n);

    // [streambuf.pub.pback], putback
    int_type sputbackc(char_type c);
    int_type sungetc();

    // [streambuf.pub.put], put area
    int_type   sputc(char_type c);
    streamsize sputn(const char_type* s, streamsize n);

  protected:
    basic_streambuf();
    basic_streambuf(const basic_streambuf& rhs);
    basic_streambuf& operator=(const basic_streambuf& rhs);

    void swap(basic_streambuf& rhs);

    // [streambuf.get.area], get area access
    char_type* eback() const;
    char_type* gptr()  const;
    char_type* egptr() const;
    void       gbump(int n);
    void       setg(char_type* gbeg, char_type* gnext, char_type* gend);

    // [streambuf.put.area], put area access
    char_type* pbase() const;
    char_type* pptr() const;
    char_type* epptr() const;
    void       pbump(int n);
    void       setp(char_type* pbeg, char_type* pend);

    // [streambuf.virtuals], virtual functions
    // [streambuf.virt.locales], locales
    virtual void imbue(const locale& loc);

    // [streambuf.virt.buffer], buffer management and positioning
    virtual basic_streambuf* setbuf(char_type* s, streamsize n);
    virtual pos_type seekoff(off_type off, ios_base::seekdir way,
                             ios_base::openmode which
                               = ios_base::in | ios_base::out);
    virtual pos_type seekpos(pos_type sp,
                             ios_base::openmode which
                               = ios_base::in | ios_base::out);
    virtual int      sync();

    // [streambuf.virt.get], get area
    virtual streamsize showmanyc();
    virtual streamsize xsgetn(char_type* s, streamsize n);
    virtual int_type   underflow();
    virtual int_type   uflow();

    // [streambuf.virt.pback], putback
    virtual int_type   pbackfail(int_type c = traits::eof());

    // [streambuf.virt.put], put area
    virtual streamsize xsputn(const char_type* s, streamsize n);
    virtual int_type   overflow(int_type c = traits::eof());
  };
}
```

The class template `basic_streambuf` serves as an abstract base class
for deriving various *stream buffers* whose objects each control two
*character sequences*:

- a character *input sequence*;
- a character *output sequence*.

#### Constructors <a id="streambuf.cons">[[streambuf.cons]]</a>

``` cpp
basic_streambuf();
```

*Effects:* Initializes:[^12]

- all pointer member objects to null pointers,
- the `getloc()` member to a copy of the global locale, `locale()`, at
  the time of construction.

*Remarks:* Once the `getloc()` member is initialized, results of calling
locale member functions, and of members of facets so obtained, can
safely be cached until the next time the member `imbue` is called.

``` cpp
basic_streambuf(const basic_streambuf& rhs);
```

*Ensures:*

- `eback() == rhs.eback()`
- `gptr() == rhs.gptr()`
- `egptr() == rhs.egptr()`
- `pbase() == rhs.pbase()`
- `pptr() == rhs.pptr()`
- `epptr() == rhs.epptr()`
- `getloc() == rhs.getloc()`

``` cpp
~basic_streambuf();
```

*Effects:* None.

#### Public member functions <a id="streambuf.members">[[streambuf.members]]</a>

##### Locales <a id="streambuf.locales">[[streambuf.locales]]</a>

``` cpp
locale pubimbue(const locale& loc);
```

*Effects:* Calls `imbue(loc)`.

*Ensures:* `loc == getloc()`.

*Returns:* Previous value of `getloc()`.

``` cpp
locale getloc() const;
```

*Returns:* If `pubimbue()` has ever been called, then the last value of
`loc` supplied, otherwise the current global locale, `locale()`, in
effect at the time of construction. If called after `pubimbue()` has
been called but before `pubimbue` has returned (i.e., from within the
call of `imbue()`) then it returns the previous value.

##### Buffer management and positioning <a id="streambuf.buffer">[[streambuf.buffer]]</a>

``` cpp
basic_streambuf* pubsetbuf(char_type* s, streamsize n);
```

*Returns:* `setbuf(s, n)`.

``` cpp
pos_type pubseekoff(off_type off, ios_base::seekdir way,
                    ios_base::openmode which
                      = ios_base::in | ios_base::out);
```

*Returns:* `seekoff(off, way, which)`.

``` cpp
pos_type pubseekpos(pos_type sp,
                    ios_base::openmode which
                      = ios_base::in | ios_base::out);
```

*Returns:* `seekpos(sp, which)`.

``` cpp
int pubsync();
```

*Returns:* `sync()`.

##### Get area <a id="streambuf.pub.get">[[streambuf.pub.get]]</a>

``` cpp
streamsize in_avail();
```

*Returns:* If a read position is available, returns `egptr() - gptr()`.
Otherwise returns `showmanyc()`[[streambuf.virt.get]].

``` cpp
int_type snextc();
```

*Effects:* Calls `sbumpc()`.

*Returns:* If that function returns `traits::eof()`, returns
`traits::eof()`. Otherwise, returns `sgetc()`.

``` cpp
int_type sbumpc();
```

*Effects:* If the input sequence read position is not available, returns
`uflow()`. Otherwise, returns `traits::to_int_type(*gptr())` and
increments the next pointer for the input sequence.

``` cpp
int_type sgetc();
```

*Returns:* If the input sequence read position is not available, returns
`underflow()`. Otherwise, returns `traits::to_int_type(*gptr())`.

``` cpp
streamsize sgetn(char_type* s, streamsize n);
```

*Returns:* `xsgetn(s, n)`.

##### Putback <a id="streambuf.pub.pback">[[streambuf.pub.pback]]</a>

``` cpp
int_type sputbackc(char_type c);
```

*Effects:* If the input sequence putback position is not available, or
if `traits::eq(c, gptr()[-1])` is `false`, returns
`pbackfail(traits::to_int_type(c))`. Otherwise, decrements the next
pointer for the input sequence and returns
`traits::to_int_type(*gptr())`.

``` cpp
int_type sungetc();
```

*Effects:* If the input sequence putback position is not available,
returns `pbackfail()`. Otherwise, decrements the next pointer for the
input sequence and returns `traits::to_int_type(*gptr())`.

##### Put area <a id="streambuf.pub.put">[[streambuf.pub.put]]</a>

``` cpp
int_type sputc(char_type c);
```

*Effects:* If the output sequence write position is not available,
returns `overflow(traits::to_int_type(c))`. Otherwise, stores `c` at the
next pointer for the output sequence, increments the pointer, and
returns `traits::to_int_type(c)`.

``` cpp
streamsize sputn(const char_type* s, streamsize n);
```

*Returns:* `xsputn(s, n)`.

#### Protected member functions <a id="streambuf.protected">[[streambuf.protected]]</a>

##### Assignment <a id="streambuf.assign">[[streambuf.assign]]</a>

``` cpp
basic_streambuf& operator=(const basic_streambuf& rhs);
```

*Ensures:*

- `eback() == rhs.eback()`
- `gptr() == rhs.gptr()`
- `egptr() == rhs.egptr()`
- `pbase() == rhs.pbase()`
- `pptr() == rhs.pptr()`
- `epptr() == rhs.epptr()`
- `getloc() == rhs.getloc()`

*Returns:* `*this`.

``` cpp
void swap(basic_streambuf& rhs);
```

*Effects:* Swaps the data members of `rhs` and `*this`.

##### Get area access <a id="streambuf.get.area">[[streambuf.get.area]]</a>

``` cpp
char_type* eback() const;
```

*Returns:* The beginning pointer for the input sequence.

``` cpp
char_type* gptr() const;
```

*Returns:* The next pointer for the input sequence.

``` cpp
char_type* egptr() const;
```

*Returns:* The end pointer for the input sequence.

``` cpp
void gbump(int n);
```

*Effects:* Adds `n` to the next pointer for the input sequence.

``` cpp
void setg(char_type* gbeg, char_type* gnext, char_type* gend);
```

*Ensures:* `gbeg == eback()`, `gnext == gptr()`, and `gend == egptr()`
are all `true`.

##### Put area access <a id="streambuf.put.area">[[streambuf.put.area]]</a>

``` cpp
char_type* pbase() const;
```

*Returns:* The beginning pointer for the output sequence.

``` cpp
char_type* pptr() const;
```

*Returns:* The next pointer for the output sequence.

``` cpp
char_type* epptr() const;
```

*Returns:* The end pointer for the output sequence.

``` cpp
void pbump(int n);
```

*Effects:* Adds `n` to the next pointer for the output sequence.

``` cpp
void setp(char_type* pbeg, char_type* pend);
```

*Ensures:* `pbeg == pbase()`, `pbeg == pptr()`, and `pend == epptr()`
are all `true`.

#### Virtual functions <a id="streambuf.virtuals">[[streambuf.virtuals]]</a>

##### Locales <a id="streambuf.virt.locales">[[streambuf.virt.locales]]</a>

``` cpp
void imbue(const locale&);
```

*Effects:* Change any translations based on locale.

*Remarks:* Allows the derived class to be informed of changes in locale
at the time they occur. Between invocations of this function a class
derived from streambuf can safely cache results of calls to locale
functions and to members of facets so obtained.

*Default behavior:* Does nothing.

##### Buffer management and positioning <a id="streambuf.virt.buffer">[[streambuf.virt.buffer]]</a>

``` cpp
basic_streambuf* setbuf(char_type* s, streamsize n);
```

*Effects:* Influences stream buffering in a way that is defined
separately for each class derived from `basic_streambuf` in this
Clause [[stringbuf.virtuals,filebuf.virtuals]].

*Default behavior:* Does nothing. Returns `this`.

``` cpp
pos_type seekoff(off_type off, ios_base::seekdir way,
                 ios_base::openmode which
                  = ios_base::in | ios_base::out);
```

*Effects:* Alters the stream positions within one or more of the
controlled sequences in a way that is defined separately for each class
derived from `basic_streambuf` in this
Clause [[stringbuf.virtuals,filebuf.virtuals]].

*Default behavior:* Returns `pos_type(off_type(-1))`.

``` cpp
pos_type seekpos(pos_type sp,
                 ios_base::openmode which
                  = ios_base::in | ios_base::out);
```

*Effects:* Alters the stream positions within one or more of the
controlled sequences in a way that is defined separately for each class
derived from `basic_streambuf` in this Clause [[stringbuf,filebuf]].

*Default behavior:* Returns `pos_type(off_type(-1))`.

``` cpp
int sync();
```

*Effects:* Synchronizes the controlled sequences with the arrays. That
is, if `pbase()` is non-null the characters between `pbase()` and
`pptr()` are written to the controlled sequence. The pointers may then
be reset as appropriate.

*Returns:* `-1` on failure. What constitutes failure is determined by
each derived class [[filebuf.virtuals]].

*Default behavior:* Returns zero.

##### Get area <a id="streambuf.virt.get">[[streambuf.virt.get]]</a>

``` cpp
streamsize showmanyc();
```

[^13]

*Returns:* An estimate of the number of characters available in the
sequence, or -1. If it returns a positive value, then successive calls
to `underflow()` will not return `traits::eof()` until at least that
number of characters have been extracted from the stream. If
`showmanyc()` returns -1, then calls to `underflow()` or `uflow()` will
fail.[^14]

*Default behavior:* Returns zero.

*Remarks:* Uses `traits::eof()`.

``` cpp
streamsize xsgetn(char_type* s, streamsize n);
```

*Effects:* Assigns up to `n` characters to successive elements of the
array whose first element is designated by `s`. The characters assigned
are read from the input sequence as if by repeated calls to `sbumpc()`.
Assigning stops when either `n` characters have been assigned or a call
to `sbumpc()` would return `traits::eof()`.

*Returns:* The number of characters assigned.[^15]

*Remarks:* Uses `traits::eof()`.

``` cpp
int_type underflow();
```

The *pending sequence* of characters is defined as the concatenation of

- the empty sequence if `gptr()` is null, otherwise the characters in
  \[`gptr()`, `egptr()`), followed by
- some (possibly empty) sequence of characters read from the input
  sequence.

The *result character* is the first character of the pending sequence if
it is non-empty, otherwise the next character that would be read from
the input sequence.

The *backup sequence* is the empty sequence if `eback()` is null,
otherwise the characters in \[`eback()`, `gptr()`).

*Effects:* The function sets up the `gptr()` and `egptr()` such that if
the pending sequence is non-empty, then `egptr()` is non-null and the
characters in \[`gptr()`, `egptr()`) are the characters in the pending
sequence, otherwise either `gptr()` is null or `gptr() == egptr()`.

If `eback()` and `gptr()` are non-null then the function is not
constrained as to their contents, but the “usual backup condition” is
that either

- the backup sequence contains at least `gptr() - eback()` characters,
  in which case the characters in \[`eback()`, `gptr()`) agree with the
  last `gptr() - eback()` characters of the backup sequence, or
- the characters in \[`gptr() - n`, `gptr()`) agree with the backup
  sequence (where `n` is the length of the backup sequence).

*Returns:* `traits::to_int_type(c)`, where `c` is the first *character*
of the *pending sequence*, without moving the input sequence position
past it. If the pending sequence is null then the function returns
`traits::eof()` to indicate failure.

*Default behavior:* Returns `traits::eof()`.

*Remarks:* The public members of `basic_streambuf` call this virtual
function only if `gptr()` is null or `gptr() >= egptr()`.

``` cpp
int_type uflow();
```

*Preconditions:* The constraints are the same as for `underflow()`,
except that the result character is transferred from the pending
sequence to the backup sequence, and the pending sequence is not empty
before the transfer.

*Default behavior:* Calls `underflow()`. If `underflow()` returns
`traits::eof()`, returns `traits::eof()`. Otherwise, returns the value
of `traits::to_int_type(*gptr())` and increments the value of the next
pointer for the input sequence.

*Returns:* `traits::eof()` to indicate failure.

##### Putback <a id="streambuf.virt.pback">[[streambuf.virt.pback]]</a>

``` cpp
int_type pbackfail(int_type c = traits::eof());
```

The *pending sequence* is defined as for `underflow()`, with the
modifications that

- If `traits::eq_int_type(c, traits::eof())` returns `true`, then the
  input sequence is backed up one character before the pending sequence
  is determined.
- If `traits::eq_int_type(c, traits::eof())` returns `false`, then `c`
  is prepended. Whether the input sequence is backed up or modified in
  any other way is unspecified.

*Ensures:* On return, the constraints of `gptr()`, `eback()`, and
`pptr()` are the same as for `underflow()`.

*Returns:* `traits::eof()` to indicate failure. Failure may occur
because the input sequence could not be backed up, or if for some other
reason the pointers cannot be set consistent with the constraints.
`pbackfail()` is called only when put back has really failed.

Returns some value other than `traits::eof()` to indicate success.

*Default behavior:* Returns `traits::eof()`.

*Remarks:* The public functions of `basic_streambuf` call this virtual
function only when `gptr()` is null, `gptr() == eback()`, or
`traits::eq(traits::to_char_type(c), gptr()[-1])` returns `false`. Other
calls shall also satisfy that constraint.

##### Put area <a id="streambuf.virt.put">[[streambuf.virt.put]]</a>

``` cpp
streamsize xsputn(const char_type* s, streamsize n);
```

*Effects:* Writes up to `n` characters to the output sequence as if by
repeated calls to `sputc(c)`. The characters written are obtained from
successive elements of the array whose first element is designated by
`s`. Writing stops when either `n` characters have been written or a
call to `sputc(c)` would return `traits::eof()`. It is unspecified
whether the function calls `overflow()` when `pptr() == epptr()` becomes
`true` or whether it achieves the same effects by other means.

*Returns:* The number of characters written.

``` cpp
int_type overflow(int_type c = traits::eof());
```

*Effects:* Consumes some initial subsequence of the characters of the
*pending sequence*. The pending sequence is defined as the concatenation
of

- the empty sequence if `pbase()` is null, otherwise the
  `pptr() - pbase()` characters beginning at `pbase()`, followed by
- the empty sequence if `traits::eq_int_type(c, traits::eof())` returns
  `true`, otherwise the sequence consisting of `c`.

*Preconditions:* Every overriding definition of this virtual function
obeys the following constraints:

- The effect of consuming a character on the associated output sequence
  is specified.[^16]
- Let `r` be the number of characters in the pending sequence not
  consumed. If `r` is nonzero then `pbase()` and `pptr()` are set so
  that: `pptr() - pbase() == r` and the `r` characters starting at
  `pbase()` are the associated output stream. In case `r` is zero (all
  characters of the pending sequence have been consumed) then either
  `pbase()` is set to `nullptr`, or `pbase()` and `pptr()` are both set
  to the same non-null value.
- The function may fail if either appending some character to the
  associated output stream fails or if it is unable to establish
  `pbase()` and `pptr()` according to the above rules.

*Returns:* `traits::eof()` or throws an exception if the function fails.

Otherwise, returns some value other than `traits::eof()` to indicate
success.[^17]

*Default behavior:* Returns `traits::eof()`.

*Remarks:* The member functions `sputc()` and `sputn()` call this
function in case that no room can be found in the put buffer enough to
accommodate the argument character sequence.

## Formatting and manipulators <a id="iostream.format">[[iostream.format]]</a>

### Header `<istream>` synopsis <a id="istream.syn">[[istream.syn]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
    class basic_istream;

  using istream  = basic_istream<char>;
  using wistream = basic_istream<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_iostream;

  using iostream  = basic_iostream<char>;
  using wiostream = basic_iostream<wchar_t>;

  template<class charT, class traits>
    basic_istream<charT, traits>& ws(basic_istream<charT, traits>& is);

  template<class Istream, class T>
    Istream&& operator>>(Istream&& is, T&& x);
}
```

### Header `<ostream>` synopsis <a id="ostream.syn">[[ostream.syn]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
    class basic_ostream;

  using ostream  = basic_ostream<char>;
  using wostream = basic_ostream<wchar_t>;

  template<class charT, class traits>
    basic_ostream<charT, traits>& endl(basic_ostream<charT, traits>& os);
  template<class charT, class traits>
    basic_ostream<charT, traits>& ends(basic_ostream<charT, traits>& os);
  template<class charT, class traits>
    basic_ostream<charT, traits>& flush(basic_ostream<charT, traits>& os);

  template<class charT, class traits>
    basic_ostream<charT, traits>& emit_on_flush(basic_ostream<charT, traits>& os);
  template<class charT, class traits>
    basic_ostream<charT, traits>& noemit_on_flush(basic_ostream<charT, traits>& os);
  template<class charT, class traits>
    basic_ostream<charT, traits>& flush_emit(basic_ostream<charT, traits>& os);

  template<class Ostream, class T>
    Ostream&& operator<<(Ostream&& os, const T& x);

  // [ostream.formatted.print], print functions
  template<class... Args>
    void print(ostream& os, format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    void println(ostream& os, format_string<Args...> fmt, Args&&... args);

  void vprint_unicode(ostream& os, string_view fmt, format_args args);
  void vprint_nonunicode(ostream& os, string_view fmt, format_args args);
}
```

### Header `<iomanip>` synopsis <a id="iomanip.syn">[[iomanip.syn]]</a>

``` cpp
namespace std {
  unspecified resetiosflags(ios_base::fmtflags mask);
  unspecified setiosflags  (ios_base::fmtflags mask);
  unspecified setbase(int base);
  template<class charT> unspecified setfill(charT c);
  unspecified setprecision(int n);
  unspecified setw(int n);
  template<class moneyT> unspecified get_money(moneyT& mon, bool intl = false);
  template<class moneyT> unspecified put_money(const moneyT& mon, bool intl = false);
  template<class charT> unspecified get_time(tm* tmb, const charT* fmt);
  template<class charT> unspecified put_time(const tm* tmb, const charT* fmt);

  template<class charT>
    unspecified quoted(const charT* s, charT delim = charT('"'), charT escape = charT('\\'));

  template<class charT, class traits, class Allocator>
    unspecified quoted(const basic_string<charT, traits, Allocator>& s,
    \itcorr                   charT delim = charT('"'), charT escape = charT('\\'));

  template<class charT, class traits, class Allocator>
    unspecified quoted(basic_string<charT, traits, Allocator>& s,
    \itcorr                   charT delim = charT('"'), charT escape = charT('\\'));

  template<class charT, class traits>
    unspecified quoted(basic_string_view<charT, traits> s,
    \itcorr                   charT delim = charT('"'), charT escape = charT('\\'));
}
```

### Header `<print>` synopsis <a id="print.syn">[[print.syn]]</a>

``` cpp
namespace std {
  // [print.fun], print functions
  template<class... Args>
    void print(format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    void print(FILE* stream, format_string<Args...> fmt, Args&&... args);

  template<class... Args>
    void println(format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    void println(FILE* stream, format_string<Args...> fmt, Args&&... args);

  void vprint_unicode(string_view fmt, format_args args);
  void vprint_unicode(FILE* stream, string_view fmt, format_args args);

  void vprint_nonunicode(string_view fmt, format_args args);
  void vprint_nonunicode(FILE* stream, string_view fmt, format_args args);
}
```

### Input streams <a id="input.streams">[[input.streams]]</a>

#### General <a id="input.streams.general">[[input.streams.general]]</a>

The header `<istream>` defines two class templates and a function
template that control input from a stream buffer, along with a function
template that extracts from stream rvalues.

#### Class template `basic_istream` <a id="istream">[[istream]]</a>

##### General <a id="istream.general">[[istream.general]]</a>

When a function is specified with a type placeholder of
`extended-floating-point-type`, the implementation provides overloads
for all cv-unqualified extended floating-point types
[[basic.fundamental]] in lieu of `extended-floating-{point-type}`.

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_istream : virtual public basic_ios<charT, traits> {
  public:
    // types (inherited from basic_ios[ios])
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [istream.cons], constructor/destructor
    explicit basic_istream(basic_streambuf<charT, traits>* sb);
    virtual ~basic_istream();

    // [istream.sentry], prefix/suffix
    class sentry;

    // [istream.formatted], formatted input
    basic_istream& operator>>(basic_istream& (*pf)(basic_istream&));
    basic_istream& operator>>(basic_ios<charT, traits>& (*pf)(basic_ios<charT, traits>&));
    basic_istream& operator>>(ios_base& (*pf)(ios_base&));

    basic_istream& operator>>(bool& n);
    basic_istream& operator>>(short& n);
    basic_istream& operator>>(unsigned short& n);
    basic_istream& operator>>(int& n);
    basic_istream& operator>>(unsigned int& n);
    basic_istream& operator>>(long& n);
    basic_istream& operator>>(unsigned long& n);
    basic_istream& operator>>(long long& n);
    basic_istream& operator>>(unsigned long long& n);
    basic_istream& operator>>(float& f);
    basic_istream& operator>>(double& f);
    basic_istream& operator>>(long double& f);
    basic_istream& operator>>(extended-floating-point-type& f);

    basic_istream& operator>>(void*& p);
    basic_istream& operator>>(basic_streambuf<char_type, traits>* sb);

    // [istream.unformatted], unformatted input
    streamsize gcount() const;
    int_type get();
    basic_istream& get(char_type& c);
    basic_istream& get(char_type* s, streamsize n);
    basic_istream& get(char_type* s, streamsize n, char_type delim);
    basic_istream& get(basic_streambuf<char_type, traits>& sb);
    basic_istream& get(basic_streambuf<char_type, traits>& sb, char_type delim);

    basic_istream& getline(char_type* s, streamsize n);
    basic_istream& getline(char_type* s, streamsize n, char_type delim);

    basic_istream& ignore(streamsize n = 1, int_type delim = traits::eof());
    int_type       peek();
    basic_istream& read    (char_type* s, streamsize n);
    streamsize     readsome(char_type* s, streamsize n);

    basic_istream& putback(char_type c);
    basic_istream& unget();
    int sync();

    pos_type tellg();
    basic_istream& seekg(pos_type);
    basic_istream& seekg(off_type, ios_base::seekdir);

  protected:
    // [istream.cons], copy/move constructor
    basic_istream(const basic_istream&) = delete;
    basic_istream(basic_istream&& rhs);

    // [istream.assign], assignment and swap
    basic_istream& operator=(const basic_istream&) = delete;
    basic_istream& operator=(basic_istream&& rhs);
    void swap(basic_istream& rhs);
  };

  // [istream.extractors], character extraction templates
  template<class charT, class traits>
    basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>&, charT&);
  template<class traits>
    basic_istream<char, traits>& operator>>(basic_istream<char, traits>&, unsigned char&);
  template<class traits>
    basic_istream<char, traits>& operator>>(basic_istream<char, traits>&, signed char&);

  template<class charT, class traits, size_t N>
    basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>&, charT(&)[N]);
  template<class traits, size_t N>
    basic_istream<char, traits>& operator>>(basic_istream<char, traits>&, unsigned char(&)[N]);
  template<class traits, size_t N>
    basic_istream<char, traits>& operator>>(basic_istream<char, traits>&, signed char(&)[N]);
}
```

The class template `basic_istream` defines a number of member function
signatures that assist in reading and interpreting input from sequences
controlled by a stream buffer.

Two groups of member function signatures share common properties: the
*formatted input functions* (or *extractors*) and the *unformatted input
functions.* Both groups of input functions are described as if they
obtain (or *extract*) input *characters* by calling `rdbuf()->sbumpc()`
or `rdbuf()->sgetc()`. They may use other public members of `istream`.

##### Constructors <a id="istream.cons">[[istream.cons]]</a>

``` cpp
explicit basic_istream(basic_streambuf<charT, traits>* sb);
```

*Effects:* Initializes the base class subobject with
`basic_ios::init(sb)`[[basic.ios.cons]].

*Ensures:* `gcount() == 0`.

``` cpp
basic_istream(basic_istream&& rhs);
```

*Effects:* Default constructs the base class, copies the `gcount()` from
`rhs`, calls `basic_ios<charT, traits>::move(rhs)` to initialize the
base class, and sets the `gcount()` for `rhs` to 0.

``` cpp
virtual ~basic_istream();
```

*Remarks:* Does not perform any operations of `rdbuf()`.

##### Assignment and swap <a id="istream.assign">[[istream.assign]]</a>

``` cpp
basic_istream& operator=(basic_istream&& rhs);
```

*Effects:* Equivalent to: `swap(rhs)`.

*Returns:* `*this`.

``` cpp
void swap(basic_istream& rhs);
```

*Effects:* Calls `basic_ios<charT, traits>::swap(rhs)`. Exchanges the
values returned by `gcount()` and `rhs.gcount()`.

##### Class `basic_istream::sentry` <a id="istream.sentry">[[istream.sentry]]</a>

``` cpp
namespace std {
  template<class charT, class traits>
  class basic_istream<charT, traits>::sentry {
    bool ok_;                   // exposition only

  public:
    explicit sentry(basic_istream& is, bool noskipws = false);
    ~sentry();
    explicit operator bool() const { return ok_; }
    sentry(const sentry&) = delete;
    sentry& operator=(const sentry&) = delete;
  };
}
```

The class `sentry` defines a class that is responsible for doing
exception safe prefix and suffix operations.

``` cpp
explicit sentry(basic_istream& is, bool noskipws = false);
```

*Effects:* If `is.good()` is `false`, calls `is.setstate(failbit)`.
Otherwise, prepares for formatted or unformatted input. First, if
`is.tie()` is not a null pointer, the function calls `is.tie()->flush()`
to synchronize the output sequence with any associated external C
stream. Except that this call can be suppressed if the put area of
`is.tie()` is empty. Further an implementation is allowed to defer the
call to `flush` until a call of `is.rdbuf()->underflow()` occurs. If no
such call occurs before the `sentry` object is destroyed, the call to
`flush` may be eliminated entirely.[^18]

If `noskipws` is zero and `is.flags() & ios_base::skipws` is nonzero,
the function extracts and discards each character as long as the next
available input character `c` is a whitespace character. If
`is.rdbuf()->sbumpc()` or `is.rdbuf()->sgetc()` returns `traits::eof()`,
the function calls `setstate(failbit | eofbit)` (which may throw
`ios_base::failure`).

*Remarks:* The constructor

``` cpp
explicit sentry(basic_istream& is, bool noskipws = false)
```

uses the currently imbued locale in `is`, to determine whether the next
input character is whitespace or not.

To decide if the character `c` is a whitespace character, the
constructor performs as if it executes the following code fragment:

``` cpp
const ctype<charT>& ctype = use_facet<ctype<charT>>(is.getloc());
if (ctype.is(ctype.space, c) != 0)
  // c is a whitespace character.
```

If, after any preparation is completed, `is.good()` is `true`,
`ok_ != false` otherwise, `ok_ == false`. During preparation, the
constructor may call `setstate(failbit)` (which may throw
`ios_base::failure`[[iostate.flags]]).[^19]

``` cpp
~sentry();
```

*Effects:* None.

``` cpp
explicit operator bool() const;
```

*Returns:* `ok_`.

#### Formatted input functions <a id="istream.formatted">[[istream.formatted]]</a>

##### Common requirements <a id="istream.formatted.reqmts">[[istream.formatted.reqmts]]</a>

Each formatted input function begins execution by constructing an object
of type `ios_base::iostate`, termed the local error state, and
initializing it to `ios_base::goodbit`. It then creates an object of
class `sentry` with the `noskipws` (second) argument `false`. If the
`sentry` object returns `true`, when converted to a value of type
`bool`, the function endeavors to obtain the requested input. Otherwise,
if the `sentry` constructor exits by throwing an exception or if the
`sentry` object produces `false` when converted to a value of type
`bool`, the function returns without attempting to obtain any input. If
`rdbuf()->sbumpc()` or `rdbuf()->sgetc()` returns `traits::eof()`, then
`ios_base::eofbit` is set in the local error state and the input
function stops trying to obtain the requested input. If an exception is
thrown during input then `ios_base::badbit` is set in the local error
state, `*this`’s error state is set to the local error state, and the
exception is rethrown if `(exceptions() & badbit) != 0`. After
extraction is done, the input function calls `setstate`, which sets
`*this`’s error state to the local error state, and may throw an
exception. In any case, the formatted input function destroys the
`sentry` object. If no exception has been thrown, it returns `*this`.

##### Arithmetic extractors <a id="istream.formatted.arithmetic">[[istream.formatted.arithmetic]]</a>

``` cpp
basic_istream& operator>>(unsigned short& val);
basic_istream& operator>>(unsigned int& val);
basic_istream& operator>>(long& val);
basic_istream& operator>>(unsigned long& val);
basic_istream& operator>>(long long& val);
basic_istream& operator>>(unsigned long long& val);
basic_istream& operator>>(float& val);
basic_istream& operator>>(double& val);
basic_istream& operator>>(long double& val);
basic_istream& operator>>(bool& val);
basic_istream& operator>>(void*& val);
```

As in the case of the inserters, these extractors depend on the locale’s
`num_get<>`[[locale.num.get]] object to perform parsing the input stream
data. These extractors behave as formatted input functions (as described
in  [[istream.formatted.reqmts]]). After a `sentry` object is
constructed, the conversion occurs as if performed by the following code
fragment, where `state` represents the input function’s local error
state:

``` cpp
using numget = num_get<charT, istreambuf_iterator<charT, traits>>;
use_facet<numget>(loc).get(*this, 0, *this, state, val);
```

In the above fragment, `loc` stands for the private member of the
`basic_ios` class.

[*Note 1*: The first argument provides an object of the
`istreambuf_iterator` class which is an iterator pointed to an input
stream. It bypasses istreams and uses streambufs
directly. — *end note*]

Class `locale` relies on this type as its interface to `istream`, so
that it does not need to depend directly on `istream`.

``` cpp
basic_istream& operator>>(short& val);
```

The conversion occurs as if performed by the following code fragment
(using the same notation as for the preceding code fragment):

``` cpp
using numget = num_get<charT, istreambuf_iterator<charT, traits>>;
long lval;
use_facet<numget>(loc).get(*this, 0, *this, state, lval);
if (lval < numeric_limits<short>::min()) {
  state |= ios_base::failbit;
  val = numeric_limits<short>::min();
} else if (numeric_limits<short>::max() < lval) {
  state |= ios_base::failbit;
  val = numeric_limits<short>::max();
}  else
  val = static_cast<short>(lval);
```

``` cpp
basic_istream& operator>>(int& val);
```

The conversion occurs as if performed by the following code fragment
(using the same notation as for the preceding code fragment):

``` cpp
using numget = num_get<charT, istreambuf_iterator<charT, traits>>;
long lval;
use_facet<numget>(loc).get(*this, 0, *this, state, lval);
if (lval < numeric_limits<int>::min()) {
  state |= ios_base::failbit;
  val = numeric_limits<int>::min();
} else if (numeric_limits<int>::max() < lval) {
  state |= ios_base::failbit;
  val = numeric_limits<int>::max();
}  else
  val = static_cast<int>(lval);
```

``` cpp
basic_istream& operator>>(extended-floating-point-type& val);
```

If the floating-point conversion rank of
*`extended-floating-point-type`* is not less than or equal to that of
`long double`, then an invocation of the operator function is
conditionally supported with *implementation-defined* semantics.

Otherwise, let `FP` be a standard floating-point type:

- if the floating-point conversion rank of
  *`extended-floating-point-type`* is less than or equal to that of
  `float`, then `FP` is `float`,
- otherwise, if the floating-point conversion rank of
  *`extended-floating-point-type`* is less than or equal to that of
  `double`, then `FP` is `double`,
- otherwise, `FP` is `long double`.

The conversion occurs as if performed by the following code fragment
(using the same notation as for the preceding code fragment):

``` cpp
using numget = num_get<charT, istreambuf_iterator<charT, traits>>;
FP fval;
use_facet<numget>(loc).get(*this, 0, *this, state, fval);
if (fval < -numeric_limits<extended-floating-point-type>::max()) {
  state |= ios_base::failbit;
  val = -numeric_limits<extended-floating-point-type>::max();
} else if (numeric_limits<extended-floating-point-type>::max() < fval) {
  state |= ios_base::failbit;
  val = numeric_limits<extended-floating-point-type>::max();
} else {
  val = static_cast<extended-floating-point-type>(fval);
}
```

[*Note 2*: When the extended floating-point type has a floating-point
conversion rank that is not equal to the rank of any standard
floating-point type, then double rounding during the conversion can
result in inaccurate results. `from_chars` can be used in situations
where maximum accuracy is important. — *end note*]

##### `basic_istream::operator>>` <a id="istream.extractors">[[istream.extractors]]</a>

``` cpp
basic_istream& operator>>(basic_istream& (*pf)(basic_istream&));
```

*Effects:* None. This extractor does not behave as a formatted input
function (as described in  [[istream.formatted.reqmts]]).

*Returns:* `pf(*this)`. [^20]

``` cpp
basic_istream& operator>>(basic_ios<charT, traits>& (*pf)(basic_ios<charT, traits>&));
```

*Effects:* Calls `pf(*this)`. This extractor does not behave as a
formatted input function (as described
in  [[istream.formatted.reqmts]]).

*Returns:* `*this`.

``` cpp
basic_istream& operator>>(ios_base& (*pf)(ios_base&));
```

*Effects:* Calls `pf(*this)`.[^21]

This extractor does not behave as a formatted input function (as
described in  [[istream.formatted.reqmts]]).

*Returns:* `*this`.

``` cpp
template<class charT, class traits, size_t N>
  basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>& in, charT (&s)[N]);
template<class traits, size_t N>
  basic_istream<char, traits>& operator>>(basic_istream<char, traits>& in, unsigned char (&s)[N]);
template<class traits, size_t N>
  basic_istream<char, traits>& operator>>(basic_istream<char, traits>& in, signed char (&s)[N]);
```

*Effects:* Behaves like a formatted input member (as described
in  [[istream.formatted.reqmts]]) of `in`. After a `sentry` object is
constructed, `operator>>` extracts characters and stores them into `s`.
If `width()` is greater than zero, `n` is `min(size_t(width()), N)`.
Otherwise `n` is `N`. `n` is the maximum number of characters stored.

Characters are extracted and stored until any of the following occurs:

- `n-1` characters are stored;
- end of file occurs on the input sequence;
- letting `ct` be `use_facet<ctype<charT>>(in.getloc())`,
  `ct.is(ct.space, c)` is `true`.

`operator>>` then stores a null byte (`charT()`) in the next position,
which may be the first position if no characters were extracted.
`operator>>` then calls `width(0)`.

If the function extracted no characters, `ios_base::failbit` is set in
the input function’s local error state before `setstate` is called.

*Returns:* `in`.

``` cpp
template<class charT, class traits>
  basic_istream<charT, traits>& operator>>(basic_istream<charT, traits>& in, charT& c);
template<class traits>
  basic_istream<char, traits>& operator>>(basic_istream<char, traits>& in, unsigned char& c);
template<class traits>
  basic_istream<char, traits>& operator>>(basic_istream<char, traits>& in, signed char& c);
```

*Effects:* Behaves like a formatted input member (as described
in  [[istream.formatted.reqmts]]) of `in`. A character is extracted from
`in`, if one is available, and stored in `c`. Otherwise,
`ios_base::failbit` is set in the input function’s local error state
before `setstate` is called.

*Returns:* `in`.

``` cpp
basic_istream& operator>>(basic_streambuf<charT, traits>* sb);
```

*Effects:* Behaves as an unformatted input
function [[istream.unformatted]]. If `sb` is null, calls
`setstate(failbit)`, which may throw
`ios_base::failure`[[iostate.flags]]. After a `sentry` object is
constructed, extracts characters from `*this` and inserts them in the
output sequence controlled by `sb`. Characters are extracted and
inserted until any of the following occurs:

- end-of-file occurs on the input sequence;
- inserting in the output sequence fails (in which case the character to
  be inserted is not extracted);
- an exception occurs (in which case the exception is caught).

If the function inserts no characters, `ios_base::failbit` is set in the
input function’s local error state before `setstate` is called.

*Returns:* `*this`.

#### Unformatted input functions <a id="istream.unformatted">[[istream.unformatted]]</a>

Each unformatted input function begins execution by constructing an
object of type `ios_base::iostate`, termed the local error state, and
initializing it to `ios_base::goodbit`. It then creates an object of
class `sentry` with the default argument `noskipws` (second) argument
`true`. If the `sentry` object returns `true`, when converted to a value
of type `bool`, the function endeavors to obtain the requested input.
Otherwise, if the `sentry` constructor exits by throwing an exception or
if the `sentry` object produces `false`, when converted to a value of
type `bool`, the function returns without attempting to obtain any
input. In either case the number of extracted characters is set to 0;
unformatted input functions taking a character array of nonzero size as
an argument shall also store a null character (using `charT()`) in the
first location of the array. If `rdbuf()->sbumpc()` or
`rdbuf()->sgetc()` returns `traits::eof()`, then `ios_base::eofbit` is
set in the local error state and the input function stops trying to
obtain the requested input. If an exception is thrown during input then
`ios_base::badbit` is set in the local error state, `*this`’s error
state is set to the local error state, and the exception is rethrown if
`(exceptions() & badbit) != 0`. If no exception has been thrown it
stores the number of characters extracted in a member object. After
extraction is done, the input function calls `setstate`, which sets
`*this`’s error state to the local error state, and may throw an
exception. In any event the `sentry` object is destroyed before leaving
the unformatted input function.

``` cpp
streamsize gcount() const;
```

*Effects:* None. This member function does not behave as an unformatted
input function (as described above).

*Returns:* The number of characters extracted by the last unformatted
input member function called for the object. If the number cannot be
represented, returns `numeric_limits<streamsize>::max()`.

``` cpp
int_type get();
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, extracts a character `c`,
if one is available. Otherwise, `ios_base::failbit` is set in the input
function’s local error state before `setstate` is called.

*Returns:* `c` if available, otherwise `traits::eof()`.

``` cpp
basic_istream& get(char_type& c);
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, extracts a character, if
one is available, and assigns it to `c`.[^22]

Otherwise, `ios_base::failbit` is set in the input function’s local
error state before `setstate` is called.

*Returns:* `*this`.

``` cpp
basic_istream& get(char_type* s, streamsize n, char_type delim);
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, extracts characters and
stores them into successive locations of an array whose first element is
designated by `s`.[^23]

Characters are extracted and stored until any of the following occurs:

- `n` is less than one or `n - 1` characters are stored;
- end-of-file occurs on the input sequence;
- `traits::eq(c, delim)` for the next available input character `c` (in
  which case `c` is not extracted).

If the function stores no characters, `ios_base::failbit` is set in the
input function’s local error state before `setstate` is called. In any
case, if `n` is greater than zero it then stores a null character into
the next successive location of the array.

*Returns:* `*this`.

``` cpp
basic_istream& get(char_type* s, streamsize n);
```

*Effects:* Calls `get(s, n, widen(’\n’))`.

*Returns:* Value returned by the call.

``` cpp
basic_istream& get(basic_streambuf<char_type, traits>& sb, char_type delim);
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, extracts characters and
inserts them in the output sequence controlled by `sb`. Characters are
extracted and inserted until any of the following occurs:

- end-of-file occurs on the input sequence;
- inserting in the output sequence fails (in which case the character to
  be inserted is not extracted);
- `traits::eq(c, delim)` for the next available input character `c` (in
  which case `c` is not extracted);
- an exception occurs (in which case, the exception is caught but not
  rethrown).

If the function inserts no characters, `ios_base::failbit` is set in the
input function’s local error state before `setstate` is called.

*Returns:* `*this`.

``` cpp
basic_istream& get(basic_streambuf<char_type, traits>& sb);
```

*Effects:* Calls `get(sb, widen(’\n’))`.

*Returns:* Value returned by the call.

``` cpp
basic_istream& getline(char_type* s, streamsize n, char_type delim);
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, extracts characters and
stores them into successive locations of an array whose first element is
designated by `s`.[^24]

Characters are extracted and stored until one of the following occurs:

1.  end-of-file occurs on the input sequence;
2.  `traits::eq(c, delim)` for the next available input character `c`
    (in which case the input character is extracted but not
    stored);[^25]
3.  `n` is less than one or `n - 1` characters are stored (in which case
    the function calls `setstate(failbit)`).

These conditions are tested in the order shown.[^26]

If the function extracts no characters, `ios_base::failbit` is set in
the input function’s local error state before `setstate` is called.[^27]

In any case, if `n` is greater than zero, it then stores a null
character (using `charT()`) into the next successive location of the
array.

*Returns:* `*this`.

[*Example 1*:

``` cpp
#include <iostream>

int main() {
  using namespace std;
  const int line_buffer_size = 100;

  char buffer[line_buffer_size];
  int line_number = 0;
  while (cin.getline(buffer, line_buffer_size, '\n') || cin.gcount()) {
    int count = cin.gcount();
    if (cin.eof())
      cout << "Partial final line";     // cin.fail() is false
    else if (cin.fail()) {
      cout << "Partial long line";
      cin.clear(cin.rdstate() & ~ios_base::failbit);
    } else {
      count--;                          // Don't include newline in count
      cout << "Line " << ++line_number;
    }
    cout << " (" << count << " chars): " << buffer << endl;
  }
}
```

— *end example*]

``` cpp
basic_istream& getline(char_type* s, streamsize n);
```

*Returns:* `getline(s, n, widen(’\n’))`

``` cpp
basic_istream& ignore(streamsize n = 1, int_type delim = traits::eof());
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, extracts characters and
discards them. Characters are extracted until any of the following
occurs:

- `n != numeric_limits<streamsize>::max()`[[numeric.limits]] and `n`
  characters have been extracted so far
- end-of-file occurs on the input sequence (in which case the function
  calls `setstate(eofbit)`, which may throw
  `ios_base::failure`[[iostate.flags]]);
- `traits::eq_int_type(traits::to_int_type(c), delim)` for the next
  available input character `c` (in which case `c` is extracted).

[*Note 1*: The last condition will never occur if
`traits::eq_int_type(delim, traits::eof())`. — *end note*]

*Returns:* `*this`.

``` cpp
int_type peek();
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, reads but does not extract
the current input character.

*Returns:* `traits::eof()` if `good()` is `false`. Otherwise, returns
`rdbuf()->sgetc()`.

``` cpp
basic_istream& read(char_type* s, streamsize n);
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, if `!good()` calls
`setstate(failbit)` which may throw an exception, and return. Otherwise
extracts characters and stores them into successive locations of an
array whose first element is designated by `s`.[^28]

Characters are extracted and stored until either of the following
occurs:

- `n` characters are stored;
- end-of-file occurs on the input sequence (in which case the function
  calls `setstate(failbit | eofbit)`, which may throw
  `ios_base::failure`[[iostate.flags]]).

*Returns:* `*this`.

``` cpp
streamsize readsome(char_type* s, streamsize n);
```

*Effects:* Behaves as an unformatted input function (as described
above). After constructing a `sentry` object, if `!good()` calls
`setstate(failbit)` which may throw an exception, and return. Otherwise
extracts characters and stores them into successive locations of an
array whose first element is designated by `s`. If
`rdbuf()->in_avail() == -1`, calls `setstate(eofbit)` (which may throw
`ios_base::failure`[[iostate.flags]]), and extracts no characters;

- If `rdbuf()->in_avail() == 0`, extracts no characters
- If `rdbuf()->in_avail() > 0`, extracts `min(rdbuf()->in_avail(), n))`.

*Returns:* The number of characters extracted.

``` cpp
basic_istream& putback(char_type c);
```

*Effects:* Behaves as an unformatted input function (as described
above), except that the function first clears `eofbit`. After
constructing a `sentry` object, if `!good()` calls `setstate(failbit)`
which may throw an exception, and return. If `rdbuf()` is not null,
calls `rdbuf()->sputbackc(c)`. If `rdbuf()` is null, or if `sputbackc`
returns `traits::eof()`, calls `setstate(badbit)` (which may throw
`ios_base::failure`[[iostate.flags]]).

[*Note 2*: This function extracts no characters, so the value returned
by the next call to `gcount()` is 0. — *end note*]

*Returns:* `*this`.

``` cpp
basic_istream& unget();
```

*Effects:* Behaves as an unformatted input function (as described
above), except that the function first clears `eofbit`. After
constructing a `sentry` object, if `!good()` calls `setstate(failbit)`
which may throw an exception, and return. If `rdbuf()` is not null,
calls `rdbuf()->sungetc()`. If `rdbuf()` is null, or if `sungetc`
returns `traits::eof()`, calls `setstate(badbit)` (which may throw
`ios_base::failure`[[iostate.flags]]).

[*Note 3*: This function extracts no characters, so the value returned
by the next call to `gcount()` is 0. — *end note*]

*Returns:* `*this`.

``` cpp
int sync();
```

*Effects:* Behaves as an unformatted input function (as described
above), except that it does not count the number of characters extracted
and does not affect the value returned by subsequent calls to
`gcount()`. After constructing a `sentry` object, if `rdbuf()` is a null
pointer, returns `-1`. Otherwise, calls `rdbuf()->pubsync()` and, if
that function returns `-1` calls `setstate(badbit)` (which may throw
`ios_base::failure`[[iostate.flags]], and returns `-1`. Otherwise,
returns zero.

``` cpp
pos_type tellg();
```

*Effects:* Behaves as an unformatted input function (as described
above), except that it does not count the number of characters extracted
and does not affect the value returned by subsequent calls to
`gcount()`.

*Returns:* After constructing a `sentry` object, if `fail() != false`,
returns `pos_type(-1)` to indicate failure. Otherwise, returns
`rdbuf()->pubseekoff(0, cur, in)`.

``` cpp
basic_istream& seekg(pos_type pos);
```

*Effects:* Behaves as an unformatted input function (as described
above), except that the function first clears `eofbit`, it does not
count the number of characters extracted, and it does not affect the
value returned by subsequent calls to `gcount()`. After constructing a
`sentry` object, if `fail() != true`, executes
`rdbuf()->pubseekpos(pos, ios_base::in)`. In case of failure, the
function calls `setstate(failbit)` (which may throw
`ios_base::failure`).

*Returns:* `*this`.

``` cpp
basic_istream& seekg(off_type off, ios_base::seekdir dir);
```

*Effects:* Behaves as an unformatted input function (as described
above), except that the function first clears `eofbit`, does not count
the number of characters extracted, and does not affect the value
returned by subsequent calls to `gcount()`. After constructing a
`sentry` object, if `fail() != true`, executes
`rdbuf()->pubseekoff(off, dir, ios_base::in)`. In case of failure, the
function calls `setstate(failbit)` (which may throw
`ios_base::failure`).

*Returns:* `*this`.

#### Standard `basic_istream` manipulators <a id="istream.manip">[[istream.manip]]</a>

Each instantiation of the function template specified in this subclause
is a designated addressable function [[namespace.std]].

``` cpp
template<class charT, class traits>
  basic_istream<charT, traits>& ws(basic_istream<charT, traits>& is);
```

*Effects:* Behaves as an unformatted input
function [[istream.unformatted]], except that it does not count the
number of characters extracted and does not affect the value returned by
subsequent calls to `is.gcount()`. After constructing a `sentry` object
extracts characters as long as the next available character `c` is
whitespace or until there are no more characters in the sequence.
Whitespace characters are distinguished with the same criterion as used
by `sentry::sentry`[[istream.sentry]]. If `ws` stops extracting
characters because there are no more available it sets `eofbit`, but not
`failbit`.

*Returns:* `is`.

#### Rvalue stream extraction <a id="istream.rvalue">[[istream.rvalue]]</a>

``` cpp
template<class Istream, class T>
  Istream&& operator>>(Istream&& is, T&& x);
```

*Constraints:* The expression `is >> std::forward<T>(x)` is well-formed
when treated as an unevaluated operand [[term.unevaluated.operand]] and
`Istream` is publicly and unambiguously derived from `ios_base`.

*Effects:* Equivalent to:

``` cpp
is >> std::forward<T>(x);
return std::move(is);
```

#### Class template `basic_iostream` <a id="iostreamclass">[[iostreamclass]]</a>

##### General <a id="iostreamclass.general">[[iostreamclass.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_iostream
    : public basic_istream<charT, traits>,
      public basic_ostream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [iostream.cons], constructor
    explicit basic_iostream(basic_streambuf<charT, traits>* sb);

    // [iostream.dest], destructor
    virtual ~basic_iostream();

  protected:
    // [iostream.cons], constructor
    basic_iostream(const basic_iostream&) = delete;
    basic_iostream(basic_iostream&& rhs);

    // [iostream.assign], assignment and swap
    basic_iostream& operator=(const basic_iostream&) = delete;
    basic_iostream& operator=(basic_iostream&& rhs);
    void swap(basic_iostream& rhs);
  };
}
```

The class template `basic_iostream` inherits a number of functions that
allow reading input and writing output to sequences controlled by a
stream buffer.

##### Constructors <a id="iostream.cons">[[iostream.cons]]</a>

``` cpp
explicit basic_iostream(basic_streambuf<charT, traits>* sb);
```

*Effects:* Initializes the base class subobjects with
`basic_istream<charT, traits>(sb)`[[istream]] and
`basic_ostream<charT, traits>(sb)`[[ostream]].

*Ensures:* `rdbuf() == sb` and `gcount() == 0`.

``` cpp
basic_iostream(basic_iostream&& rhs);
```

*Effects:* Move constructs from the rvalue `rhs` by constructing the
`basic_istream` base class with `std::move(rhs)`.

##### Destructor <a id="iostream.dest">[[iostream.dest]]</a>

``` cpp
virtual ~basic_iostream();
```

*Remarks:* Does not perform any operations on `rdbuf()`.

##### Assignment and swap <a id="iostream.assign">[[iostream.assign]]</a>

``` cpp
basic_iostream& operator=(basic_iostream&& rhs);
```

*Effects:* Equivalent to: `swap(rhs)`.

``` cpp
void swap(basic_iostream& rhs);
```

*Effects:* Calls `basic_istream<charT, traits>::swap(rhs)`.

### Output streams <a id="output.streams">[[output.streams]]</a>

#### General <a id="output.streams.general">[[output.streams.general]]</a>

The header `<ostream>` defines a class template and several function
templates that control output to a stream buffer, along with a function
template that inserts into stream rvalues.

#### Class template `basic_ostream` <a id="ostream">[[ostream]]</a>

##### General <a id="ostream.general">[[ostream.general]]</a>

When a function has a parameter type `extended-floating-point-type`, the
implementation provides overloads for all cv-unqualified extended
floating-point types [[basic.fundamental]].

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_ostream : virtual public basic_ios<charT, traits> {
  public:
    // types (inherited from basic_ios[ios])
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [ostream.cons], constructor/destructor
    explicit basic_ostream(basic_streambuf<char_type, traits>* sb);
    virtual ~basic_ostream();

    // [ostream.sentry], prefix/suffix
    class sentry;

    // [ostream.formatted], formatted output
    basic_ostream& operator<<(basic_ostream& (*pf)(basic_ostream&));
    basic_ostream& operator<<(basic_ios<charT, traits>& (*pf)(basic_ios<charT, traits>&));
    basic_ostream& operator<<(ios_base& (*pf)(ios_base&));

    basic_ostream& operator<<(bool n);
    basic_ostream& operator<<(short n);
    basic_ostream& operator<<(unsigned short n);
    basic_ostream& operator<<(int n);
    basic_ostream& operator<<(unsigned int n);
    basic_ostream& operator<<(long n);
    basic_ostream& operator<<(unsigned long n);
    basic_ostream& operator<<(long long n);
    basic_ostream& operator<<(unsigned long long n);
    basic_ostream& operator<<(float f);
    basic_ostream& operator<<(double f);
    basic_ostream& operator<<(long double f);
    basic_ostream& operator<<(extended-floating-point-type f);

    basic_ostream& operator<<(const void* p);
    basic_ostream& operator<<(const volatile void* p);
    basic_ostream& operator<<(nullptr_t);
    basic_ostream& operator<<(basic_streambuf<char_type, traits>* sb);

    // [ostream.unformatted], unformatted output
    basic_ostream& put(char_type c);
    basic_ostream& write(const char_type* s, streamsize n);

    basic_ostream& flush();

    // [ostream.seeks], seeks
    pos_type tellp();
    basic_ostream& seekp(pos_type);
    basic_ostream& seekp(off_type, ios_base::seekdir);

  protected:
    // [ostream.cons], copy/move constructor
    basic_ostream(const basic_ostream&) = delete;
    basic_ostream(basic_ostream&& rhs);

    // [ostream.assign], assignment and swap
    basic_ostream& operator=(const basic_ostream&) = delete;
    basic_ostream& operator=(basic_ostream&& rhs);
    void swap(basic_ostream& rhs);
  };

  // [ostream.inserters.character], character inserters
  template<class charT, class traits>
    basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>&, charT);
  template<class charT, class traits>
    basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>&, char);
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, char);

  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, signed char);
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, unsigned char);

  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, wchar_t) = delete;
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, char8_t) = delete;
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, char16_t) = delete;
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, char32_t) = delete;
  template<class traits>
    basic_ostream<wchar_t, traits>&
      operator<<(basic_ostream<wchar_t, traits>&, char8_t) = delete;
  template<class traits>
    basic_ostream<wchar_t, traits>&
      operator<<(basic_ostream<wchar_t, traits>&, char16_t) = delete;
  template<class traits>
    basic_ostream<wchar_t, traits>&
      operator<<(basic_ostream<wchar_t, traits>&, char32_t) = delete;

  template<class charT, class traits>
    basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>&, const charT*);
  template<class charT, class traits>
    basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>&, const char*);
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, const char*);

  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, const signed char*);
  template<class traits>
    basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>&, const unsigned char*);

  template<class traits>
    basic_ostream<char, traits>&
      operator<<(basic_ostream<char, traits>&, const wchar_t*) = delete;
  template<class traits>
    basic_ostream<char, traits>&
      operator<<(basic_ostream<char, traits>&, const char8_t*) = delete;
  template<class traits>
    basic_ostream<char, traits>&
      operator<<(basic_ostream<char, traits>&, const char16_t*) = delete;
  template<class traits>
    basic_ostream<char, traits>&
      operator<<(basic_ostream<char, traits>&, const char32_t*) = delete;
  template<class traits>
    basic_ostream<wchar_t, traits>&
      operator<<(basic_ostream<wchar_t, traits>&, const char8_t*) = delete;
  template<class traits>
    basic_ostream<wchar_t, traits>&
      operator<<(basic_ostream<wchar_t, traits>&, const char16_t*) = delete;
  template<class traits>
    basic_ostream<wchar_t, traits>&
      operator<<(basic_ostream<wchar_t, traits>&, const char32_t*) = delete;
}
```

The class template `basic_ostream` defines a number of member function
signatures that assist in formatting and writing output to output
sequences controlled by a stream buffer.

Two groups of member function signatures share common properties: the
*formatted output functions* (or *inserters*) and the *unformatted
output functions.* Both groups of output functions generate (or
*insert*) output *characters* by actions equivalent to calling
`rdbuf()->sputc(int_type)`. They may use other public members of
`basic_ostream` except that they shall not invoke any virtual members of
`rdbuf()` except `overflow()`, `xsputn()`, and `sync()`.

If one of these called functions throws an exception, then unless
explicitly noted otherwise the output function sets `badbit` in the
error state. If `badbit` is set in `exceptions()`, the output function
rethrows the exception without completing its actions, otherwise it does
not throw anything and proceeds as if the called function had returned a
failure indication.

[*Note 1*: The deleted overloads of `operator<<` prevent formatting
characters as integers and strings as pointers. — *end note*]

##### Constructors <a id="ostream.cons">[[ostream.cons]]</a>

``` cpp
explicit basic_ostream(basic_streambuf<charT, traits>* sb);
```

*Effects:* Initializes the base class subobject with
`basic_ios<charT, traits>::init(sb)`[[basic.ios.cons]].

*Ensures:* `rdbuf() == sb`.

``` cpp
basic_ostream(basic_ostream&& rhs);
```

*Effects:* Move constructs from the rvalue `rhs`. This is accomplished
by default constructing the base class and calling
`basic_ios<charT, traits>::move(rhs)` to initialize the base class.

``` cpp
virtual ~basic_ostream();
```

*Remarks:* Does not perform any operations on `rdbuf()`.

##### Assignment and swap <a id="ostream.assign">[[ostream.assign]]</a>

``` cpp
basic_ostream& operator=(basic_ostream&& rhs);
```

*Effects:* Equivalent to: `swap(rhs)`.

*Returns:* `*this`.

``` cpp
void swap(basic_ostream& rhs);
```

*Effects:* Calls `basic_ios<charT, traits>::swap(rhs)`.

##### Class `basic_ostream::sentry` <a id="ostream.sentry">[[ostream.sentry]]</a>

``` cpp
namespace std {
  template<class charT, class traits>
  class basic_ostream<charT, traits>::sentry {
    bool ok_;       // exposition only

  public:
    explicit sentry(basic_ostream& os);
    ~sentry();
    explicit operator bool() const { return ok_; }

    sentry(const sentry&) = delete;
    sentry& operator=(const sentry&) = delete;
  };
}
```

The class `sentry` defines a class that is responsible for doing
exception safe prefix and suffix operations.

``` cpp
explicit sentry(basic_ostream& os);
```

If `os.good()` is nonzero, prepares for formatted or unformatted output.
If `os.tie()` is not a null pointer, calls `os.tie()->flush()`.[^29]

If, after any preparation is completed, `os.good()` is `true`,
`ok_ == true` otherwise, `ok_ == false`. During preparation, the
constructor may call `setstate(failbit)` (which may throw
`ios_base::failure`[[iostate.flags]]).[^30]

``` cpp
~sentry();
```

If
`(os.flags() & ios_base::unitbuf) && !uncaught_exceptions() && os.good()`
is `true`, calls `os.rdbuf()->pubsync()`. If that function returns -1,
sets `badbit` in `os.rdstate()` without propagating an exception.

``` cpp
explicit operator bool() const;
```

*Effects:* Returns `ok_`.

##### Seek members <a id="ostream.seeks">[[ostream.seeks]]</a>

Each seek member function begins execution by constructing an object of
class `sentry`. It returns by destroying the `sentry` object.

``` cpp
pos_type tellp();
```

*Returns:* If `fail() != false`, returns `pos_type(-1)` to indicate
failure. Otherwise, returns `rdbuf()->pubseekoff(0, cur, out)`.

``` cpp
basic_ostream& seekp(pos_type pos);
```

*Effects:* If `fail() != true`, executes
`rdbuf()->pubseekpos(pos, ios_base::out)`. In case of failure, the
function calls `setstate(failbit)` (which may throw
`ios_base::failure`).

*Returns:* `*this`.

``` cpp
basic_ostream& seekp(off_type off, ios_base::seekdir dir);
```

*Effects:* If `fail() != true`, executes
`rdbuf()->pubseekoff(off, dir, ios_base::out)`. In case of failure, the
function calls `setstate(failbit)` (which may throw
`ios_base::failure`).

*Returns:* `*this`.

#### Formatted output functions <a id="ostream.formatted">[[ostream.formatted]]</a>

##### Common requirements <a id="ostream.formatted.reqmts">[[ostream.formatted.reqmts]]</a>

Each formatted output function begins execution by constructing an
object of class `sentry`. If that object returns `true` when converted
to a value of type `bool`, the function endeavors to generate the
requested output. If the generation fails, then the formatted output
function does `setstate(ios_base::failbit)`, which can throw an
exception. If an exception is thrown during output, then
`ios_base::badbit` is set[^31]

in `*this`’s error state. If `(exceptions()&badbit) != 0` then the
exception is rethrown. Whether or not an exception is thrown, the
`sentry` object is destroyed before leaving the formatted output
function. If no exception is thrown, the result of the formatted output
function is `*this`.

The descriptions of the individual formatted output functions describe
how they perform output and do not mention the `sentry` object.

If a formatted output function of a stream `os` determines padding, it
does so as follows. Given a `charT` character sequence `seq` where
`charT` is the character type of the stream, if the length of `seq` is
less than `os.width()`, then enough copies of `os.fill()` are added to
this sequence as necessary to pad to a width of `os.width()` characters.
If `(os.flags() & ios_base::adjustfield) == ios_base::left` is `true`,
the fill characters are placed after the character sequence; otherwise,
they are placed before the character sequence.

##### Arithmetic inserters <a id="ostream.inserters.arithmetic">[[ostream.inserters.arithmetic]]</a>

``` cpp
basic_ostream& operator<<(bool val);
basic_ostream& operator<<(short val);
basic_ostream& operator<<(unsigned short val);
basic_ostream& operator<<(int val);
basic_ostream& operator<<(unsigned int val);
basic_ostream& operator<<(long val);
basic_ostream& operator<<(unsigned long val);
basic_ostream& operator<<(long long val);
basic_ostream& operator<<(unsigned long long val);
basic_ostream& operator<<(float val);
basic_ostream& operator<<(double val);
basic_ostream& operator<<(long double val);
basic_ostream& operator<<(const void* val);
```

*Effects:* The classes `num_get<>` and `num_put<>` handle
locale-dependent numeric formatting and parsing. These inserter
functions use the imbued `locale` value to perform numeric formatting.
When `val` is of type `bool`, `long`, `unsigned long`, `long long`,
`unsigned long long`, `double`, `long double`, or `const void*`, the
formatting conversion occurs as if it performed the following code
fragment:

``` cpp
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(), val).failed();
```

When `val` is of type `short` the formatting conversion occurs as if it
performed the following code fragment:

``` cpp
ios_base::fmtflags baseflags = ios_base::flags() & ios_base::basefield;
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(),
    baseflags == ios_base::oct || baseflags == ios_base::hex
      ? static_cast<long>(static_cast<unsigned short>(val))
      : static_cast<long>(val)).failed();
```

When `val` is of type `int` the formatting conversion occurs as if it
performed the following code fragment:

``` cpp
ios_base::fmtflags baseflags = ios_base::flags() & ios_base::basefield;
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(),
    baseflags == ios_base::oct || baseflags == ios_base::hex
      ? static_cast<long>(static_cast<unsigned int>(val))
      : static_cast<long>(val)).failed();
```

When `val` is of type `unsigned short` or `unsigned int` the formatting
conversion occurs as if it performed the following code fragment:

``` cpp
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(),
      static_cast<unsigned long>(val)).failed();
```

When `val` is of type `float` the formatting conversion occurs as if it
performed the following code fragment:

``` cpp
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(),
      static_cast<double>(val)).failed();
```

The first argument provides an object of the `ostreambuf_iterator<>`
class which is an iterator for class `basic_ostream<>`. It bypasses
`ostream`s and uses `streambuf`s directly. Class `locale` relies on
these types as its interface to iostreams, since for flexibility it has
been abstracted away from direct dependence on `ostream`. The second
parameter is a reference to the base class subobject of type `ios_base`.
It provides formatting specifications such as field width, and a locale
from which to obtain other facets. If `failed` is `true` then does
`setstate(badbit)`, which may throw an exception, and returns.

*Returns:* `*this`.

``` cpp
basic_ostream& operator<<(const volatile void* p);
```

*Effects:* Equivalent to:
`return operator<<(const_cast<const void*>(p));`

``` cpp
basic_ostream& operator<<(extended-floating-point-type val);
```

*Effects:* If the floating-point conversion rank of
*`extended-floating-point-type`* is less than or equal to that of
`double`, the formatting conversion occurs as if it performed the
following code fragment:

``` cpp
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(),
      static_cast<double>(val)).failed();
```

Otherwise, if the floating-point conversion rank of
*`extended-floating-point-type`* is less than or equal to that of
`long double`, the formatting conversion occurs as if it performed the
following code fragment:

``` cpp
bool failed = use_facet<
  num_put<charT, ostreambuf_iterator<charT, traits>>
    >(getloc()).put(*this, *this, fill(),
      static_cast<long double>(val)).failed();
```

Otherwise, an invocation of the operator function is conditionally
supported with *implementation-defined* semantics.

If `failed` is `true` then does `setstate(badbit)`, which may throw an
exception, and returns.

*Returns:* `*this`.

##### `basic_ostream::operator<<` <a id="ostream.inserters">[[ostream.inserters]]</a>

``` cpp
basic_ostream& operator<<(basic_ostream& (*pf)(basic_ostream&));
```

*Effects:* None. Does not behave as a formatted output function (as
described in  [[ostream.formatted.reqmts]]).

*Returns:* `pf(*this)`.[^32]

``` cpp
basic_ostream& operator<<(basic_ios<charT, traits>& (*pf)(basic_ios<charT, traits>&));
```

*Effects:* Calls `pf(*this)`. This inserter does not behave as a
formatted output function (as described
in  [[ostream.formatted.reqmts]]).

*Returns:* `*this`.[^33]

``` cpp
basic_ostream& operator<<(ios_base& (*pf)(ios_base&));
```

*Effects:* Calls `pf(*this)`. This inserter does not behave as a
formatted output function (as described
in  [[ostream.formatted.reqmts]]).

*Returns:* `*this`.

``` cpp
basic_ostream& operator<<(basic_streambuf<charT, traits>* sb);
```

*Effects:* Behaves as an unformatted output
function [[ostream.unformatted]]. After the `sentry` object is
constructed, if `sb` is null calls `setstate(badbit)` (which may throw
`ios_base::failure`).

Gets characters from `sb` and inserts them in `*this`. Characters are
read from `sb` and inserted until any of the following occurs:

- end-of-file occurs on the input sequence;
- inserting in the output sequence fails (in which case the character to
  be inserted is not extracted);
- an exception occurs while getting a character from `sb`.

If the function inserts no characters, it calls `setstate(failbit)`
(which may throw `ios_base::failure`[[iostate.flags]]). If an exception
was thrown while extracting a character, the function sets `failbit` in
the error state, and if `failbit` is set in `exceptions()` the caught
exception is rethrown.

*Returns:* `*this`.

``` cpp
basic_ostream& operator<<(nullptr_t);
```

*Effects:* Equivalent to:

``` cpp
return *this << s;
```

where `s` is an *implementation-defined* NTCTS [[defns.ntcts]].

##### Character inserter function templates <a id="ostream.inserters.character">[[ostream.inserters.character]]</a>

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& out, charT c);
template<class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& out, char c);
// specialization
template<class traits>
  basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>& out, char c);
// signed and unsigned
template<class traits>
  basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>& out, signed char c);
template<class traits>
  basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>& out, unsigned char c);
```

*Effects:* Behaves as a formatted output
function [[ostream.formatted.reqmts]] of `out`. Constructs a character
sequence `seq`. If `c` has type `char` and the character type of the
stream is not `char`, then `seq` consists of `out.widen(c)`; otherwise
`seq` consists of `c`. Determines padding for `seq` as described
in  [[ostream.formatted.reqmts]]. Inserts `seq` into `out`. Calls
`os.width(0)`.

*Returns:* `out`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& out, const charT* s);
template<class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& out, const char* s);
template<class traits>
  basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>& out, const char* s);
template<class traits>
  basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>& out, const signed char* s);
template<class traits>
  basic_ostream<char, traits>& operator<<(basic_ostream<char, traits>& out,
                                          const unsigned char* s);
```

*Preconditions:* `s` is not a null pointer.

*Effects:* Behaves like a formatted inserter (as described
in  [[ostream.formatted.reqmts]]) of `out`. Creates a character sequence
`seq` of `n` characters starting at `s`, each widened using
`out.widen()`[[basic.ios.members]], where `n` is the number that would
be computed as if by:

- `traits::length(s)` for the overload where the first argument is of
  type `basic_ostream<charT, traits>&` and the second is of type
  `const charT*`, and also for the overload where the first argument is
  of type `basic_ostream<char, traits>&` and the second is of type
  `const char*`,
- `char_traits<char>::length(s)` for the overload where the first
  argument is of type `basic_ostream<charT, traits>&` and the second is
  of type `const char*`,
- `traits::length(reinterpret_cast<const char*>(s))` for the other two
  overloads.

Determines padding for `seq` as described
in  [[ostream.formatted.reqmts]]. Inserts `seq` into `out`. Calls
`width(0)`.

*Returns:* `out`.

##### Print <a id="ostream.formatted.print">[[ostream.formatted.print]]</a>

``` cpp
template<class... Args>
  void print(ostream& os, format_string<Args...> fmt, Args&&... args);
```

*Effects:* If the ordinary literal encoding [[lex.charset]] is UTF-8,
equivalent to:

``` cpp
vprint_unicode(os, fmt.str, make_format_args(std::forward<Args>(args)...));
```

Otherwise, equivalent to:

``` cpp
vprint_nonunicode(os, fmt.str, make_format_args(std::forward<Args>(args)...));
```

``` cpp
template<class... Args>
  void println(ostream& os, format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
print(os, "{}\n", format(fmt, std::forward<Args>(args)...));
```

``` cpp
void vprint_unicode(ostream& os, string_view fmt, format_args args);
void vprint_nonunicode(ostream& os, string_view fmt, format_args args);
```

*Effects:* Behaves as a formatted output
function [[ostream.formatted.reqmts]] of `os`, except that:

- failure to generate output is reported as specified below, and
- any exception thrown by the call to `vformat` is propagated without
  regard to the value of `os.exceptions()` and without turning on
  `ios_base::badbit` in the error state of `os`.

After constructing a `sentry` object, the function initializes an
automatic variable via

``` cpp
string out = vformat(os.getloc(), fmt, args);
```

If the function is `vprint_unicode` and `os` is a stream that refers to
a terminal capable of displaying Unicode which is determined in an
implementation-defined manner, writes `out` to the terminal using the
native Unicode API; if `out` contains invalid code units, the behavior
is undefined and implementations are encouraged to diagnose it. If the
native Unicode API is used, the function flushes `os` before writing
`out`. Otherwise (if `os` is not such a stream or the function is
`vprint_nonunicode`), inserts the character sequence \[`out.begin()`,
`out.end()`) into `os`. If writing to the terminal or inserting into
`os` fails, calls `os.setstate(ios_base::badbit)` (which may throw
`ios_base::failure`).

*Recommended practice:* For `vprint_unicode`, if invoking the native
Unicode API requires transcoding, implementations should substitute
invalid code units with U+fffd (replacement character) per the Unicode
Standard, Chapter 3.9 ‘U+fffd‘ Substitution in Conversion.

#### Unformatted output functions <a id="ostream.unformatted">[[ostream.unformatted]]</a>

Each unformatted output function begins execution by constructing an
object of class `sentry`. If that object returns `true`, while
converting to a value of type `bool`, the function endeavors to generate
the requested output. If an exception is thrown during output, then
`ios_base::badbit` is set[^34]

in `*this`’s error state. If `(exceptions() & badbit) != 0` then the
exception is rethrown. In any case, the unformatted output function ends
by destroying the `sentry` object, then, if no exception was thrown,
returning the value specified for the unformatted output function.

``` cpp
basic_ostream& put(char_type c);
```

*Effects:* Behaves as an unformatted output function (as described
above). After constructing a `sentry` object, inserts the character `c`,
if possible.[^35]

Otherwise, calls `setstate(badbit)` (which may throw
`ios_base::failure`[[iostate.flags]]).

*Returns:* `*this`.

``` cpp
basic_ostream& write(const char_type* s, streamsize n);
```

*Effects:* Behaves as an unformatted output function (as described
above). After constructing a `sentry` object, obtains characters to
insert from successive locations of an array whose first element is
designated by `s`.[^36]

Characters are inserted until either of the following occurs:

- `n` characters are inserted;
- inserting in the output sequence fails (in which case the function
  calls `setstate(badbit)`, which may throw
  `ios_base::failure`[[iostate.flags]]).

*Returns:* `*this`.

``` cpp
basic_ostream& flush();
```

*Effects:* Behaves as an unformatted output function (as described
above). If `rdbuf()` is not a null pointer, constructs a `sentry`
object. If that object returns `true` when converted to a value of type
`bool` the function calls `rdbuf()->pubsync()`. If that function returns
-1 calls `setstate(badbit)` (which may throw
`ios_base::failure`[[iostate.flags]]). Otherwise, if the `sentry` object
returns `false`, does nothing.

*Returns:* `*this`.

#### Standard manipulators <a id="ostream.manip">[[ostream.manip]]</a>

Each instantiation of any of the function templates specified in this
subclause is a designated addressable function [[namespace.std]].

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& endl(basic_ostream<charT, traits>& os);
```

*Effects:* Calls `os.put(os.widen(’\n’))`, then `os.flush()`.

*Returns:* `os`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& ends(basic_ostream<charT, traits>& os);
```

*Effects:* Inserts a null character into the output sequence: calls
`os.put(charT())`.

*Returns:* `os`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& flush(basic_ostream<charT, traits>& os);
```

*Effects:* Calls `os.flush()`.

*Returns:* `os`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& emit_on_flush(basic_ostream<charT, traits>& os);
```

*Effects:* If `os.rdbuf()` is a
`basic_syncbuf<charT, traits, Allocator>*`, called `buf` for the purpose
of exposition, calls `buf->set_emit_on_sync(true)`. Otherwise this
manipulator has no effect.

[*Note 1*: To work around the issue that the `Allocator` template
argument cannot be deduced, implementations can introduce an
intermediate base class to `basic_syncbuf` that manages its
`emit_on_sync` flag. — *end note*]

*Returns:* `os`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& noemit_on_flush(basic_ostream<charT, traits>& os);
```

*Effects:* If `os.rdbuf()` is a
`basic_syncbuf<charT, traits, Allocator>*`, called `buf` for the purpose
of exposition, calls `buf->set_emit_on_sync(false)`. Otherwise this
manipulator has no effect.

*Returns:* `os`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& flush_emit(basic_ostream<charT, traits>& os);
```

*Effects:* Calls `os.flush()`. Then, if `os.rdbuf()` is a
`basic_syncbuf<charT, traits, Allocator>*`, called `buf` for the purpose
of exposition, behaves as an unformatted output
function [[ostream.unformatted]] of `os`. After constructing a `sentry`
object, calls `buf->emit()`. If that call returns `false`, calls
`os.setstate(ios_base::badbit)`.

*Returns:* `os`.

#### Rvalue stream insertion <a id="ostream.rvalue">[[ostream.rvalue]]</a>

``` cpp
template<class Ostream, class T>
  Ostream&& operator<<(Ostream&& os, const T& x);
```

*Constraints:* The expression `os << x` is well-formed when treated as
an unevaluated operand and `Ostream` is publicly and unambiguously
derived from `ios_base`.

*Effects:* As if by: `os << x;`

*Returns:* `std::move(os)`.

### Standard manipulators <a id="std.manip">[[std.manip]]</a>

The header `<iomanip>` defines several functions that support extractors
and inserters that alter information maintained by class `ios_base` and
its derived classes.

``` cpp
unspecified resetiosflags(ios_base::fmtflags mask);
```

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` then the expression
`out << resetiosflags(mask)` behaves as if it called `f(out, mask)`, or
if `in` is an object of type `basic_istream<charT, traits>` then the
expression `in >> resetiosflags(mask)` behaves as if it called
`f(in, mask)`, where the function `f` is defined as:[^37]

``` cpp
void f(ios_base& str, ios_base::fmtflags mask) {
  // reset specified flags
  str.setf(ios_base::fmtflags(0), mask);
}
```

The expression `out << resetiosflags(mask)` has type
`basic_ostream<charT, traits>&` and value `out`. The expression
`in >> resetiosflags(mask)` has type `basic_istream<charT, traits>&` and
value `in`.

``` cpp
unspecified setiosflags(ios_base::fmtflags mask);
```

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` then the expression
`out << setiosflags(mask)` behaves as if it called `f(out, mask)`, or if
`in` is an object of type `basic_istream<charT, traits>` then the
expression `in >> setiosflags(mask)` behaves as if it called
`f(in, mask)`, where the function `f` is defined as:

``` cpp
void f(ios_base& str, ios_base::fmtflags mask) {
  // set specified flags
  str.setf(mask);
}
```

The expression `out << setiosflags(mask)` has type
`basic_ostream<charT, traits>&` and value `out`. The expression
`in >> setiosflags(mask)` has type `basic_istream<charT, traits>&` and
value `in`.

``` cpp
unspecified setbase(int base);
```

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` then the expression
`out << setbase(base)` behaves as if it called `f(out, base)`, or if
`in` is an object of type `basic_istream<charT, traits>` then the
expression `in >> setbase(base)` behaves as if it called `f(in, base)`,
where the function `f` is defined as:

``` cpp
void f(ios_base& str, int base) {
  // set basefield
  str.setf(base ==  8 ? ios_base::oct :
      base == 10 ? ios_base::dec :
      base == 16 ? ios_base::hex :
      ios_base::fmtflags(0), ios_base::basefield);
}
```

The expression `out << setbase(base)` has type
`basic_ostream<charT, traits>&` and value `out`. The expression
`in >> setbase(base)` has type `basic_istream<charT, traits>&` and value
`in`.

``` cpp
unspecified setfill(char_type c);
```

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` and `c` has type `charT` then the
expression `out << setfill(c)` behaves as if it called `f(out, c)`,
where the function `f` is defined as:

``` cpp
template<class charT, class traits>
void f(basic_ios<charT, traits>& str, charT c) {
  // set fill character
  str.fill(c);
}
```

The expression `out << setfill(c)` has type
`basic_ostream<charT, traits>&` and value `out`.

``` cpp
unspecified setprecision(int n);
```

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` then the expression
`out << setprecision(n)` behaves as if it called `f(out, n)`, or if `in`
is an object of type `basic_istream<charT, traits>` then the expression
`in >> setprecision(n)` behaves as if it called `f(in, n)`, where the
function `f` is defined as:

``` cpp
void f(ios_base& str, int n) {
  // set precision
  str.precision(n);
}
```

The expression `out << setprecision(n)` has type
`basic_ostream<charT, traits>&` and value `out`. The expression
`in >> setprecision(n)` has type `basic_istream<charT, traits>&` and
value `in`.

``` cpp
unspecified setw(int n);
```

*Returns:* An object of unspecified type such that if `out` is an
instance of `basic_ostream<charT, traits>` then the expression
`out << setw(n)` behaves as if it called `f(out, n)`, or if `in` is an
object of type `basic_istream<charT, traits>` then the expression
`in >> setw(n)` behaves as if it called `f(in, n)`, where the function
`f` is defined as:

``` cpp
void f(ios_base& str, int n) {
  // set width
  str.width(n);
}
```

The expression `out << setw(n)` has type `basic_ostream<charT, traits>&`
and value `out`. The expression `in >> setw(n)` has type
`basic_istream<charT, traits>&` and value `in`.

### Extended manipulators <a id="ext.manip">[[ext.manip]]</a>

The header `<iomanip>` defines several functions that support extractors
and inserters that allow for the parsing and formatting of sequences and
values for money and time.

``` cpp
template<class moneyT> unspecified get_money(moneyT& mon, bool intl = false);
```

*Mandates:* The type `moneyT` is either `long double` or a
specialization of the `basic_string` template [[strings]].

*Effects:* The expression `in >> get_money(mon, intl)` described below
behaves as a formatted input function [[istream.formatted.reqmts]].

*Returns:* An object of unspecified type such that if `in` is an object
of type `basic_istream<charT, traits>` then the expression
`in >> get_money(mon, intl)` behaves as if it called `f(in, mon, intl)`,
where the function `f` is defined as:

``` cpp
template<class charT, class traits, class moneyT>
void f(basic_ios<charT, traits>& str, moneyT& mon, bool intl) {
  using Iter     = istreambuf_iterator<charT, traits>;
  using MoneyGet = money_get<charT, Iter>;

  ios_base::iostate err = ios_base::goodbit;
  const MoneyGet& mg = use_facet<MoneyGet>(str.getloc());

  mg.get(Iter(str.rdbuf()), Iter(), intl, str, err, mon);

  if (ios_base::goodbit != err)
    str.setstate(err);
}
```

The expression `in >> get_money(mon, intl)` has type
`basic_istream<charT, traits>&` and value `in`.

``` cpp
template<class moneyT> unspecified put_money(const moneyT& mon, bool intl = false);
```

*Mandates:* The type `moneyT` is either `long double` or a
specialization of the `basic_string` template [[strings]].

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` then the expression
`out << put_money(mon, intl)` behaves as a formatted output
function [[ostream.formatted.reqmts]] that calls `f(out, mon, intl)`,
where the function `f` is defined as:

``` cpp
template<class charT, class traits, class moneyT>
void f(basic_ios<charT, traits>& str, const moneyT& mon, bool intl) {
  using Iter     = ostreambuf_iterator<charT, traits>;
  using MoneyPut = money_put<charT, Iter>;

  const MoneyPut& mp = use_facet<MoneyPut>(str.getloc());
  const Iter end = mp.put(Iter(str.rdbuf()), intl, str, str.fill(), mon);

  if (end.failed())
    str.setstate(ios_base::badbit);
}
```

The expression `out << put_money(mon, intl)` has type
`basic_ostream<charT, traits>&` and value `out`.

``` cpp
template<class charT> unspecified get_time(tm* tmb, const charT* fmt);
```

*Preconditions:* The argument `tmb` is a valid pointer to an object of
type `tm`, and \[`fmt`, `fmt + char_traits<charT>::length(fmt)`) is a
valid range.

*Returns:* An object of unspecified type such that if `in` is an object
of type `basic_istream<charT, traits>` then the expression
`in >> get_time(tmb, fmt)` behaves as if it called `f(in, tmb, fmt)`,
where the function `f` is defined as:

``` cpp
template<class charT, class traits>
void f(basic_ios<charT, traits>& str, tm* tmb, const charT* fmt) {
  using Iter    = istreambuf_iterator<charT, traits>;
  using TimeGet = time_get<charT, Iter>;

  ios_base::iostate err = ios_base::goodbit;
  const TimeGet& tg = use_facet<TimeGet>(str.getloc());

  tg.get(Iter(str.rdbuf()), Iter(), str, err, tmb,
    fmt, fmt + traits::length(fmt));

  if (err != ios_base::goodbit)
    str.setstate(err);
}
```

The expression `in >> get_time(tmb, fmt)` has type
`basic_istream<charT, traits>&` and value `in`.

``` cpp
template<class charT> unspecified put_time(const tm* tmb, const charT* fmt);
```

*Preconditions:* The argument `tmb` is a valid pointer to an object of
type `tm`, and \[`fmt`, `fmt + char_traits<charT>::length(fmt)`) is a
valid range.

*Returns:* An object of unspecified type such that if `out` is an object
of type `basic_ostream<charT, traits>` then the expression
`out << put_time(tmb, fmt)` behaves as if it called `f(out, tmb, fmt)`,
where the function `f` is defined as:

``` cpp
template<class charT, class traits>
void f(basic_ios<charT, traits>& str, const tm* tmb, const charT* fmt) {
  using Iter    = ostreambuf_iterator<charT, traits>;
  using TimePut = time_put<charT, Iter>;

  const TimePut& tp = use_facet<TimePut>(str.getloc());
  const Iter end = tp.put(Iter(str.rdbuf()), str, str.fill(), tmb,
    fmt, fmt + traits::length(fmt));

  if (end.failed())
    str.setstate(ios_base::badbit);
}
```

The expression `out << put_time(tmb, fmt)` has type
`basic_ostream<charT, traits>&` and value `out`.

### Quoted manipulators <a id="quoted.manip">[[quoted.manip]]</a>

[*Note 1*: Quoted manipulators provide string insertion and extraction
of quoted strings (for example, XML and CSV formats). Quoted
manipulators are useful in ensuring that the content of a string with
embedded spaces remains unchanged if inserted and then extracted via
stream I/O. — *end note*]

``` cpp
template<class charT>
  unspecified quoted(const charT* s, charT delim = charT('"'), charT escape = charT('\\'));
template<class charT, class traits, class Allocator>
  unspecified quoted(const basic_string<charT, traits, Allocator>& s,
  \itcorr                   charT delim = charT('"'), charT escape = charT('\\'));
template<class charT, class traits>
  unspecified quoted(basic_string_view<charT, traits> s,
  \itcorr                   charT delim = charT('"'), charT escape = charT('\\'));
```

*Returns:* An object of unspecified type such that if `out` is an
instance of `basic_ostream` with member type `char_type` the same as
`charT` and with member type `traits_type`, which in the second and
third forms is the same as `traits`, then the expression
`out << quoted(s, delim, escape)` behaves as a formatted output
function [[ostream.formatted.reqmts]] of `out`. This forms a character
sequence `seq`, initially consisting of the following elements:

- `delim`.
- Each character in `s`. If the character to be output is equal to
  `escape` or `delim`, as determined by `traits_type::eq`, first output
  `escape`.
- `delim`.

Let `x` be the number of elements initially in `seq`. Then padding is
determined for `seq` as described in  [[ostream.formatted.reqmts]],
`seq` is inserted as if by calling `out.rdbuf()->sputn(seq, n)`, where
`n` is the larger of `out.width()` and `x`, and `out.width(0)` is
called. The expression `out << quoted(s, delim, escape)` has type
`basic_ostream<charT, traits>&` and value `out`.

``` cpp
template<class charT, class traits, class Allocator>
  unspecified quoted(basic_string<charT, traits, Allocator>& s,
  \itcorr                   charT delim = charT('"'), charT escape = charT('\\'));
```

*Returns:* An object of unspecified type such that:

- If `in` is an instance of `basic_istream` with member types
  `char_type` and `traits_type` the same as `charT` and `traits`,
  respectively, then the expression `in >> quoted(s, delim, escape)`
  behaves as if it extracts the following characters from `in` using
  `operator>>(basic_istream<charT, traits>&, charT&)`[[istream.extractors]]
  which may throw `ios_base::failure`[[ios.failure]]:
  - If the first character extracted is equal to `delim`, as determined
    by `traits_type::eq`, then:
    - Turn off the `skipws` flag.
    - `s.clear()`
    - Until an unescaped `delim` character is reached or `!in`, extract
      characters from `in` and append them to `s`, except that if an
      `escape` is reached, ignore it and append the next character to
      `s`.
    - Discard the final `delim` character.
    - Restore the `skipws` flag to its original value.
  - Otherwise, `in >> s`.
- If `out` is an instance of `basic_ostream` with member types
  `char_type` and `traits_type` the same as `charT` and `traits`,
  respectively, then the expression `out << quoted(s, delim, escape)`
  behaves as specified for the
  `const basic_string<charT, traits, Allocator>&` overload of the
  `quoted` function.
- The expression `in >> quoted(s, delim, escape)` has type
  `basic_istream<charT, traits>&` and value `in`.
- The expression `out << quoted(s, delim, escape)` has type
  `basic_ostream<charT, traits>&` and value `out`.

### Print functions <a id="print.fun">[[print.fun]]</a>

``` cpp
template<class... Args>
  void print(format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
print(stdout, fmt, std::forward<Args>(args)...);
```

``` cpp
template<class... Args>
  void print(FILE* stream, format_string<Args...> fmt, Args&&... args);
```

*Effects:* If the ordinary literal encoding [[lex.charset]] is UTF-8,
equivalent to:

``` cpp
vprint_unicode(stream, fmt.str, make_format_args(std::forward<Args>(args)...));
```

Otherwise, equivalent to:

``` cpp
vprint_nonunicode(stream, fmt.str, make_format_args(std::forward<Args>(args)...));
```

``` cpp
template<class... Args>
  void println(format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
println(stdout, fmt, std::forward<Args>(args)...);
```

``` cpp
template<class... Args>
  void println(FILE* stream, format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
print(stream, "{}\n", format(fmt, std::forward<Args>(args)...));
```

``` cpp
void vprint_unicode(string_view fmt, format_args args);
```

*Effects:* Equivalent to:

``` cpp
vprint_unicode(stdout, fmt, args);
```

``` cpp
void vprint_unicode(FILE* stream, string_view fmt, format_args args);
```

*Preconditions:* `stream` is a valid pointer to an output C stream.

*Effects:* The function initializes an automatic variable via

``` cpp
string out = vformat(fmt, args);
```

If `stream` refers to a terminal capable of displaying Unicode, writes
`out` to the terminal using the native Unicode API; if `out` contains
invalid code units, the behavior is undefined and implementations are
encouraged to diagnose it. Otherwise writes `out` to `stream` unchanged.
If the native Unicode API is used, the function flushes `stream` before
writing `out`.

[*Note 1*: On POSIX and Windows, `stream` referring to a terminal means
that, respectively, `isatty(fileno(stream))` and
`GetConsoleMode(_get_osfhandle(_fileno(stream)), ...)` return
nonzero. — *end note*]

[*Note 2*: On Windows, the native Unicode API is
`WriteConsoleW`. — *end note*]

*Throws:* Any exception thrown by the call to
`vformat`[[format.err.report]]. `system_error` if writing to the
terminal or `stream` fails. May throw `bad_alloc`.

*Recommended practice:* If invoking the native Unicode API requires
transcoding, implementations should substitute invalid code units with
U+fffd (replacement character) per the Unicode Standard, Chapter 3.9
‘U+fffd‘ Substitution in Conversion.

``` cpp
void vprint_nonunicode(string_view fmt, format_args args);
```

*Effects:* Equivalent to:

``` cpp
vprint_nonunicode(stdout, fmt, args);
```

``` cpp
void vprint_nonunicode(FILE* stream, string_view fmt, format_args args);
```

*Preconditions:* `stream` is a valid pointer to an output C stream.

*Effects:* Writes the result of `vformat(fmt, args)` to `stream`.

*Throws:* Any exception thrown by the call to
`vformat`[[format.err.report]]. `system_error` if writing to `stream`
fails. May throw `bad_alloc`.

## String-based streams <a id="string.streams">[[string.streams]]</a>

### Header `<sstream>` synopsis <a id="sstream.syn">[[sstream.syn]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_stringbuf;

  template<class charT, class traits, class Allocator>
    void swap(basic_stringbuf<charT, traits, Allocator>& x,
              basic_stringbuf<charT, traits, Allocator>& y) noexcept(noexcept(x.swap(y)));

  using stringbuf  = basic_stringbuf<char>;
  using wstringbuf = basic_stringbuf<wchar_t>;

  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_istringstream;

  template<class charT, class traits, class Allocator>
    void swap(basic_istringstream<charT, traits, Allocator>& x,
              basic_istringstream<charT, traits, Allocator>& y);

  using istringstream  = basic_istringstream<char>;
  using wistringstream = basic_istringstream<wchar_t>;

  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_ostringstream;

  template<class charT, class traits, class Allocator>
    void swap(basic_ostringstream<charT, traits, Allocator>& x,
              basic_ostringstream<charT, traits, Allocator>& y);

  using ostringstream  = basic_ostringstream<char>;
  using wostringstream = basic_ostringstream<wchar_t>;

  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
    class basic_stringstream;

  template<class charT, class traits, class Allocator>
    void swap(basic_stringstream<charT, traits, Allocator>& x,
              basic_stringstream<charT, traits, Allocator>& y);

  using stringstream  = basic_stringstream<char>;
  using wstringstream = basic_stringstream<wchar_t>;
}
```

The header `<sstream>` defines four class templates and eight types that
associate stream buffers with objects of class `basic_string`, as
described in  [[string.classes]].

### Class template `basic_stringbuf` <a id="stringbuf">[[stringbuf]]</a>

#### General <a id="stringbuf.general">[[stringbuf.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_stringbuf : public basic_streambuf<charT, traits> {
  public:
    using char_type      = charT;
    using int_type       = typename traits::int_type;
    using pos_type       = typename traits::pos_type;
    using off_type       = typename traits::off_type;
    using traits_type    = traits;
    using allocator_type = Allocator;

    // [stringbuf.cons], constructors
    basic_stringbuf() : basic_stringbuf(ios_base::in | ios_base::out) {}
    explicit basic_stringbuf(ios_base::openmode which);
    explicit basic_stringbuf(
      const basic_string<charT, traits, Allocator>& s,
      ios_base::openmode which = ios_base::in | ios_base::out);
    explicit basic_stringbuf(const Allocator& a)
      : basic_stringbuf(ios_base::in | ios_base::out, a) {}
    basic_stringbuf(ios_base::openmode which, const Allocator& a);
    explicit basic_stringbuf(
      basic_string<charT, traits, Allocator>&& s,
      ios_base::openmode which = ios_base::in | ios_base::out);
    template<class SAlloc>
      basic_stringbuf(
        const basic_string<charT, traits, SAlloc>& s, const Allocator& a)
        : basic_stringbuf(s, ios_base::in | ios_base::out, a) {}
    template<class SAlloc>
      basic_stringbuf(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which, const Allocator& a);
    template<class SAlloc>
      explicit basic_stringbuf(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which = ios_base::in | ios_base::out);
    basic_stringbuf(const basic_stringbuf&) = delete;
    basic_stringbuf(basic_stringbuf&& rhs);
    basic_stringbuf(basic_stringbuf&& rhs, const Allocator& a);

    // [stringbuf.assign], assignment and swap
    basic_stringbuf& operator=(const basic_stringbuf&) = delete;
    basic_stringbuf& operator=(basic_stringbuf&& rhs);
    void swap(basic_stringbuf& rhs) noexcept(see below);

    // [stringbuf.members], getters and setters
    allocator_type get_allocator() const noexcept;

    basic_string<charT, traits, Allocator> str() const &;
    template<class SAlloc>
      basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
    basic_string<charT, traits, Allocator> str() &&;
    basic_string_view<charT, traits> view() const noexcept;

    void str(const basic_string<charT, traits, Allocator>& s);
    template<class SAlloc>
      void str(const basic_string<charT, traits, SAlloc>& s);
    void str(basic_string<charT, traits, Allocator>&& s);

  protected:
    // [stringbuf.virtuals], overridden virtual functions
    int_type underflow() override;
    int_type pbackfail(int_type c = traits::eof()) override;
    int_type overflow (int_type c = traits::eof()) override;
    basic_streambuf<charT, traits>* setbuf(charT*, streamsize) override;

    pos_type seekoff(off_type off, ios_base::seekdir way,
                     ios_base::openmode which
                      = ios_base::in | ios_base::out) override;
    pos_type seekpos(pos_type sp,
                     ios_base::openmode which
                      = ios_base::in | ios_base::out) override;

  private:
    ios_base::openmode mode;                        // exposition only
    basic_string<charT, traits, Allocator> buf;     // exposition only
    void init_buf_ptrs();                           // exposition only
  };
}
```

The class `basic_stringbuf` is derived from `basic_streambuf` to
associate possibly the input sequence and possibly the output sequence
with a sequence of arbitrary *characters*. The sequence can be
initialized from, or made available as, an object of class
`basic_string`.

For the sake of exposition, the maintained data and internal pointer
initialization is presented here as:

- `ios_base::openmode mode`, has `in` set if the input sequence can be
  read, and `out` set if the output sequence can be written.
- `basic_string<charT, traits, Allocator> buf` contains the underlying
  character sequence.
- `init_buf_ptrs()` sets the base class’ get area [[streambuf.get.area]]
  and put area [[streambuf.put.area]] pointers after initializing,
  moving from, or assigning to `buf` accordingly.

#### Constructors <a id="stringbuf.cons">[[stringbuf.cons]]</a>

``` cpp
explicit basic_stringbuf(ios_base::openmode which);
```

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], and `mode` with `which`. It is
*implementation-defined* whether the sequence pointers (`eback()`,
`gptr()`, `egptr()`, `pbase()`, `pptr()`, `epptr()`) are initialized to
null pointers.

*Ensures:* `str().empty()` is `true`.

``` cpp
explicit basic_stringbuf(
  const basic_string<charT, traits, Allocator>& s,
  ios_base::openmode which = ios_base::in | ios_base::out);
```

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], `mode` with `which`, and `buf`
with `s`, then calls `init_buf_ptrs()`.

``` cpp
basic_stringbuf(ios_base::openmode which, const Allocator &a);
```

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], `mode` with `which`, and `buf`
with `a`, then calls `init_buf_ptrs()`.

*Ensures:* `str().empty()` is `true`.

``` cpp
explicit basic_stringbuf(
  basic_string<charT, traits, Allocator>&& s,
  ios_base::openmode which = ios_base::in | ios_base::out);
```

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], `mode` with `which`, and `buf`
with `std::move(s)`, then calls `init_buf_ptrs()`.

``` cpp
template<class SAlloc>
  basic_stringbuf(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which, const Allocator &a);
```

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], `mode` with `which`, and `buf`
with `{s,a}`, then calls `init_buf_ptrs()`.

``` cpp
template<class SAlloc>
  explicit basic_stringbuf(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which = ios_base::in | ios_base::out);
```

*Constraints:* `is_same_v<SAlloc, Allocator>` is `false`.

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], `mode` with `which`, and `buf`
with `s`, then calls `init_buf_ptrs()`.

``` cpp
basic_stringbuf(basic_stringbuf&& rhs);
basic_stringbuf(basic_stringbuf&& rhs, const Allocator& a);
```

*Effects:* Copy constructs the base class from `rhs` and initializes
`mode` with `rhs.mode`. In the first form `buf` is initialized from
`std::move(rhs).str()`. In the second form `buf` is initialized from
`{std::move(rhs).str(), a}`. It is *implementation-defined* whether the
sequence pointers in `*this` (`eback()`, `gptr()`, `egptr()`, `pbase()`,
`pptr()`, `epptr()`) obtain the values which `rhs` had.

*Ensures:* Let `rhs_p` refer to the state of `rhs` just prior to this
construction and let `rhs_a` refer to the state of `rhs` just after this
construction.

- `str() == rhs_p.str()`
- `gptr() - eback() == rhs_p.gptr() - rhs_p.eback()`
- `egptr() - eback() == rhs_p.egptr() - rhs_p.eback()`
- `pptr() - pbase() == rhs_p.pptr() - rhs_p.pbase()`
- `epptr() - pbase() == rhs_p.epptr() - rhs_p.pbase()`
- `if (eback()) eback() != rhs_a.eback()`
- `if (gptr()) gptr() != rhs_a.gptr()`
- `if (egptr()) egptr() != rhs_a.egptr()`
- `if (pbase()) pbase() != rhs_a.pbase()`
- `if (pptr()) pptr() != rhs_a.pptr()`
- `if (epptr()) epptr() != rhs_a.epptr()`
- `getloc() == rhs_p.getloc()`
- `rhs` is empty but usable, as if `std::move(rhs).str()` was called.

#### Assignment and swap <a id="stringbuf.assign">[[stringbuf.assign]]</a>

``` cpp
basic_stringbuf& operator=(basic_stringbuf&& rhs);
```

*Effects:* After the move assignment `*this` has the observable state it
would have had if it had been move constructed from `rhs`
(see  [[stringbuf.cons]]).

*Returns:* `*this`.

``` cpp
void swap(basic_stringbuf& rhs) noexcept(see below);
```

*Preconditions:*
`allocator_traits<Allocator>::propagate_on_container_swap::value` is
`true` or `get_allocator() == rhs.get_allocator()` is `true`.

*Effects:* Exchanges the state of `*this` and `rhs`.

*Remarks:* The exception specification is equivalent to:  
`allocator_traits<Allocator>::propagate_on_container_swap::value ||`  
`allocator_traits<Allocator>::is_always_equal::value`.

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_stringbuf<charT, traits, Allocator>& x,
            basic_stringbuf<charT, traits, Allocator>& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="stringbuf.members">[[stringbuf.members]]</a>

The member functions getting the underlying character sequence all refer
to a `high_mark` value, where `high_mark` represents the position one
past the highest initialized character in the buffer. Characters can be
initialized by writing to the stream, by constructing the
`basic_stringbuf` passing a `basic_string` argument, or by calling one
of the `str` member functions passing a `basic_string` as an argument.
In the latter case, all characters initialized prior to the call are now
considered uninitialized (except for those characters re-initialized by
the new `basic_string`).

``` cpp
void init_buf_ptrs(); // exposition only
```

*Effects:* Initializes the input and output sequences from `buf`
according to `mode`.

*Ensures:*

- If `ios_base::out` is set in `mode`, `pbase()` points to `buf.front()`
  and `epptr() >= pbase() + buf.size()` is `true`;
  - in addition, if `ios_base::ate` is set in `mode`,
    `pptr() == pbase() + buf.size()` is `true`,
  - otherwise `pptr() == pbase()` is `true`.
- If `ios_base::in` is set in `mode`, `eback()` points to `buf.front()`,
  and `(gptr() == eback() && egptr() == eback() + buf.size())` is
  `true`.

[*Note 1*: For efficiency reasons, stream buffer operations can violate
invariants of `buf` while it is held encapsulated in the
`basic_stringbuf`, e.g., by writing to characters in the range
\[`buf.data() + buf.size()`, `buf.data() + buf.capacity()`). All
operations retrieving a `basic_string` from `buf` ensure that the
`basic_string` invariants hold on the returned value. — *end note*]

``` cpp
allocator_type get_allocator() const noexcept;
```

*Returns:* `buf.get_allocator()`.

``` cpp
basic_string<charT, traits, Allocator> str() const &;
```

*Effects:* Equivalent to:

``` cpp
return basic_string<charT, traits, Allocator>(view(), get_allocator());
```

``` cpp
template<class SAlloc>
  basic_string<charT, traits, SAlloc> str(const SAlloc& sa) const;
```

*Constraints:* `SAlloc` is a type that qualifies as an
allocator [[container.requirements.general]].

*Effects:* Equivalent to:

``` cpp
return basic_string<charT, traits, SAlloc>(view(), sa);
```

``` cpp
basic_string<charT, traits, Allocator> str() &&;
```

*Ensures:* The underlying character sequence `buf` is empty and
`pbase()`, `pptr()`, `epptr()`, `eback()`, `gptr()`, and `egptr()` are
initialized as if by calling `init_buf_ptrs()` with an empty `buf`.

*Returns:* A `basic_string<charT, traits, Allocator>` object move
constructed from the `basic_stringbuf`’s underlying character sequence
in `buf`. This can be achieved by first adjusting `buf` to have the same
content as `view()`.

``` cpp
basic_string_view<charT, traits> view() const noexcept;
```

Let `sv` be `basic_string_view<charT, traits>`.

*Returns:* A `sv` object referring to the `basic_stringbuf`’s underlying
character sequence in `buf`:

- If `ios_base::out` is set in `mode`, then
  `sv(pbase(), high_mark-pbase())` is returned.
- Otherwise, if `ios_base::in` is set in `mode`, then
  `sv(eback(), egptr()-eback())` is returned.
- Otherwise, `sv()` is returned.

[*Note 2*: Using the returned `sv` object after destruction or
invalidation of the character sequence underlying `*this` is undefined
behavior, unless `sv.empty()` is `true`. — *end note*]

``` cpp
void str(const basic_string<charT, traits, Allocator>& s);
```

*Effects:* Equivalent to:

``` cpp
buf = s;
init_buf_ptrs();
```

``` cpp
template<class SAlloc>
  void str(const basic_string<charT, traits, SAlloc>& s);
```

*Constraints:* `is_same_v<SAlloc,Allocator>` is `false`.

*Effects:* Equivalent to:

``` cpp
buf = s;
init_buf_ptrs();
```

``` cpp
void str(basic_string<charT, traits, Allocator>&& s);
```

*Effects:* Equivalent to:

``` cpp
buf = std::move(s);
init_buf_ptrs();
```

#### Overridden virtual functions <a id="stringbuf.virtuals">[[stringbuf.virtuals]]</a>

``` cpp
int_type underflow() override;
```

*Returns:* If the input sequence has a read position available, returns
`traits::to_int_type(*gptr())`. Otherwise, returns `traits::eof()`. Any
character in the underlying buffer which has been initialized is
considered to be part of the input sequence.

``` cpp
int_type pbackfail(int_type c = traits::eof()) override;
```

*Effects:* Puts back the character designated by `c` to the input
sequence, if possible, in one of three ways:

- If `traits::eq_int_type(c, traits::eof())` returns `false` and if the
  input sequence has a putback position available, and if
  `traits::eq(to_char_type(c), gptr()[-1])` returns `true`, assigns
  `gptr() - 1` to `gptr()`. Returns: `c`.
- If `traits::eq_int_type(c, traits::eof())` returns `false` and if the
  input sequence has a putback position available, and if `mode` `&`
  `ios_base::out` is nonzero, assigns `c` to `*–gptr()`. Returns: `c`.
- If `traits::eq_int_type(c, traits::eof())` returns `true` and if the
  input sequence has a putback position available, assigns `gptr() - 1`
  to `gptr()`. Returns: `traits::not_eof(c)`.

*Returns:* As specified above, or `traits::eof()` to indicate failure.

*Remarks:* If the function can succeed in more than one of these ways,
it is unspecified which way is chosen.

``` cpp
int_type overflow(int_type c = traits::eof()) override;
```

*Effects:* Appends the character designated by `c` to the output
sequence, if possible, in one of two ways:

- If `traits::eq_int_type(c, traits::eof())` returns `false` and if
  either the output sequence has a write position available or the
  function makes a write position available (as described below), the
  function calls `sputc(c)`. Signals success by returning `c`.
- If `traits::eq_int_type(c, traits::eof())` returns `true`, there is no
  character to append. Signals success by returning a value other than
  `traits::eof()`.

*Returns:* As specified above, or `traits::eof()` to indicate failure.

*Remarks:* The function can alter the number of write positions
available as a result of any call.

The function can make a write position available only if `ios_base::out`
is set in `mode`. To make a write position available, the function
reallocates (or initially allocates) an array object with a sufficient
number of elements to hold the current array object (if any), plus at
least one additional write position. If `ios_base::in` is set in `mode`,
the function alters the read end pointer `egptr()` to point just past
the new write position.

``` cpp
pos_type seekoff(off_type off, ios_base::seekdir way,
                 ios_base::openmode which
                   = ios_base::in | ios_base::out) override;
```

*Effects:* Alters the stream position within one of the controlled
sequences, if possible, as indicated in [[stringbuf.seekoff.pos]].

**Table: `seekoff` positioning** <a id="stringbuf.seekoff.pos">[stringbuf.seekoff.pos]</a>

| Conditions                                                                                                                     | Result                                            |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `ios_base::in` is set in `which`                                                                                               | positions the input sequence                      |
| `ios_base::out` is set in `which`                                                                                              | positions the output sequence                     |
| both `ios_base::in` and `ios_base::out` are set in `which` and either<br> `way == ios_base::beg` or<br> `way == ios_base::end` | positions both the input and the output sequences |
| Otherwise                                                                                                                      | the positioning operation fails.                  |


For a sequence to be positioned, the function determines `newoff` as
indicated in [[stringbuf.seekoff.newoff]]. If the sequence’s next
pointer (either `gptr()` or `pptr()`) is a null pointer and `newoff` is
nonzero, the positioning operation fails.

**Table: `newoff` values** <a id="stringbuf.seekoff.newoff">[stringbuf.seekoff.newoff]</a>

| Condition              | `newoff` Value                                                          |
| ---------------------- | ----------------------------------------------------------------------- |
| `way == ios_base::beg` | 0                                                                       |
| `way == ios_base::cur` | the next pointer minus the beginning pointer (`xnext - xbeg`).          |
| `way == ios_base::end` | the high mark pointer minus the beginning pointer (`high_mark - xbeg`). |


If `(newoff + off) < 0`, or if `newoff + off` refers to an uninitialized
character [[stringbuf.members]], the positioning operation fails.
Otherwise, the function assigns `xbeg + newoff + off` to the next
pointer `xnext`.

*Returns:* `pos_type(newoff)`, constructed from the resultant offset
`newoff` (of type `off_type`), that stores the resultant stream
position, if possible. If the positioning operation fails, or if the
constructed object cannot represent the resultant stream position, the
return value is `pos_type(off_type(-1))`.

``` cpp
pos_type seekpos(pos_type sp,
                 ios_base::openmode which
                   = ios_base::in | ios_base::out) override;
```

*Effects:* Equivalent to `seekoff(off_type(sp), ios_base::beg, which)`.

*Returns:* `sp` to indicate success, or `pos_type(off_type(-1))` to
indicate failure.

``` cpp
basic_streambuf<charT, traits>* setbuf(charT* s, streamsize n) override;
```

*Effects:* *implementation-defined*, except that `setbuf(0, 0)` has no
effect.

*Returns:* `this`.

### Class template `basic_istringstream` <a id="istringstream">[[istringstream]]</a>

#### General <a id="istringstream.general">[[istringstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_istringstream : public basic_istream<charT, traits> {
  public:
    using char_type      = charT;
    using int_type       = typename traits::int_type;
    using pos_type       = typename traits::pos_type;
    using off_type       = typename traits::off_type;
    using traits_type    = traits;
    using allocator_type = Allocator;

    // [istringstream.cons], constructors
    basic_istringstream() : basic_istringstream(ios_base::in) {}
    explicit basic_istringstream(ios_base::openmode which);
    explicit basic_istringstream(
      const basic_string<charT, traits, Allocator>& s,
      ios_base::openmode which = ios_base::in);
    basic_istringstream(ios_base::openmode which, const Allocator& a);
    explicit basic_istringstream(
      basic_string<charT, traits, Allocator>&& s,
      ios_base::openmode which = ios_base::in);
    template<class SAlloc>
      basic_istringstream(
        const basic_string<charT, traits, SAlloc>& s, const Allocator& a)
        : basic_istringstream(s, ios_base::in, a) {}
    template<class SAlloc>
      basic_istringstream(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which, const Allocator& a);
    template<class SAlloc>
      explicit basic_istringstream(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which = ios_base::in);
    basic_istringstream(const basic_istringstream&) = delete;
    basic_istringstream(basic_istringstream&& rhs);

    basic_istringstream& operator=(const basic_istringstream&) = delete;
    basic_istringstream& operator=(basic_istringstream&& rhs);

    // [istringstream.swap], swap
    void swap(basic_istringstream& rhs);

    // [istringstream.members], members
    basic_stringbuf<charT, traits, Allocator>* rdbuf() const;
    basic_string<charT, traits, Allocator> str() const &;
    template<class SAlloc>
      basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
    basic_string<charT, traits, Allocator> str() &&;
    basic_string_view<charT, traits> view() const noexcept;

    void str(const basic_string<charT, traits, Allocator>& s);
    template<class SAlloc>
      void str(const basic_string<charT, traits, SAlloc>& s);
    void str(basic_string<charT, traits, Allocator>&& s);

  private:
    basic_stringbuf<charT, traits, Allocator> sb;   // exposition only
  };
}
```

The class `basic_istringstream<charT, traits, Allocator>` supports
reading objects of class `basic_string<{}charT, traits, Allocator>`. It
uses a `basic_stringbuf<charT, traits, Allocator>` object to control the
associated storage. For the sake of exposition, the maintained data is
presented here as:

- `sb`, the `stringbuf` object.

#### Constructors <a id="istringstream.cons">[[istringstream.cons]]</a>

``` cpp
explicit basic_istringstream(ios_base::openmode which);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(which | ios_base::in)`[[stringbuf.cons]].

``` cpp
explicit basic_istringstream(
  const basic_string<charT, traits, Allocator>& s,
  ios_base::openmode which = ios_base::in);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(s, which | ios_base::in)`[[stringbuf.cons]].

``` cpp
basic_istringstream(ios_base::openmode which, const Allocator& a);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(which | ios_base::in, a)`[[stringbuf.cons]].

``` cpp
explicit basic_istringstream(
  basic_string<charT, traits, Allocator>&& s,
  ios_base::openmode which = ios_base::in);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(std::move(s), which | ios_base::in)`[[stringbuf.cons]].

``` cpp
template<class SAlloc>
  basic_istringstream(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which, const Allocator& a);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(s, which | ios_base::in, a)`[[stringbuf.cons]].

``` cpp
template<class SAlloc>
  explicit basic_istringstream(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which = ios_base::in);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(s, which | ios_base::in)`[[stringbuf.cons]].

``` cpp
basic_istringstream(basic_istringstream&& rhs);
```

*Effects:* Move constructs from the rvalue `rhs`. This is accomplished
by move constructing the base class, and the contained
`basic_stringbuf`. Then calls
`basic_istream<charT, traits>::set_rdbuf(addressof(sb))` to install the
contained `basic_stringbuf`.

#### Swap <a id="istringstream.swap">[[istringstream.swap]]</a>

``` cpp
void swap(basic_istringstream& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_istream<charT, traits>::swap(rhs);
sb.swap(rhs.sb);
```

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_istringstream<charT, traits, Allocator>& x,
            basic_istringstream<charT, traits, Allocator>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="istringstream.members">[[istringstream.members]]</a>

``` cpp
basic_stringbuf<charT, traits, Allocator>* rdbuf() const;
```

*Returns:*
`const_cast<basic_stringbuf<charT, traits, Allocator>*>(addressof(sb))`.

``` cpp
basic_string<charT, traits, Allocator> str() const &;
```

*Effects:* Equivalent to: `return rdbuf()->str();`

``` cpp
template<class SAlloc>
  basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
```

*Effects:* Equivalent to: `return rdbuf()->str(sa);`

``` cpp
basic_string<charT,traits,Allocator> str() &&;
```

*Effects:* Equivalent to: `return std::move(*rdbuf()).str();`

``` cpp
basic_string_view<charT, traits> view() const noexcept;
```

*Effects:* Equivalent to: `return rdbuf()->view();`

``` cpp
void str(const basic_string<charT, traits, Allocator>& s);
```

*Effects:* Equivalent to: `rdbuf()->str(s);`

``` cpp
template<class SAlloc>
  void str(const basic_string<charT, traits, SAlloc>& s);
```

*Effects:* Equivalent to: `rdbuf()->str(s);`

``` cpp
void str(basic_string<charT, traits, Allocator>&& s);
```

*Effects:* Equivalent to: `rdbuf()->str(std::move(s));`

### Class template `basic_ostringstream` <a id="ostringstream">[[ostringstream]]</a>

#### General <a id="ostringstream.general">[[ostringstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_ostringstream : public basic_ostream<charT, traits> {
  public:
    using char_type      = charT;
    using int_type       = typename traits::int_type;
    using pos_type       = typename traits::pos_type;
    using off_type       = typename traits::off_type;
    using traits_type    = traits;
    using allocator_type = Allocator;

    // [ostringstream.cons], constructors
    basic_ostringstream() : basic_ostringstream(ios_base::out) {}
    explicit basic_ostringstream(ios_base::openmode which);
    explicit basic_ostringstream(
      const basic_string<charT, traits, Allocator>& s,
      ios_base::openmode which = ios_base::out);
    basic_ostringstream(ios_base::openmode which, const Allocator& a);
    explicit basic_ostringstream(
      basic_string<charT, traits, Allocator>&& s,
      ios_base::openmode which = ios_base::out);
    template<class SAlloc>
      basic_ostringstream(
        const basic_string<charT, traits, SAlloc>& s, const Allocator& a)
        : basic_ostringstream(s, ios_base::out, a) {}
    template<class SAlloc>
      basic_ostringstream(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which, const Allocator& a);
    template<class SAlloc>
      explicit basic_ostringstream(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which = ios_base::out);
    basic_ostringstream(const basic_ostringstream&) = delete;
    basic_ostringstream(basic_ostringstream&& rhs);

    basic_ostringstream& operator=(const basic_ostringstream&) = delete;
    basic_ostringstream& operator=(basic_ostringstream&& rhs);

    // [ostringstream.swap], swap
    void swap(basic_ostringstream& rhs);

    // [ostringstream.members], members
    basic_stringbuf<charT, traits, Allocator>* rdbuf() const;

    basic_string<charT, traits, Allocator> str() const &;
    template<class SAlloc>
      basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
    basic_string<charT, traits, Allocator> str() &&;
    basic_string_view<charT, traits> view() const noexcept;

    void str(const basic_string<charT, traits, Allocator>& s);
    template<class SAlloc>
      void str(const basic_string<charT, traits, SAlloc>& s);
    void str(basic_string<charT, traits, Allocator>&& s);

   private:
    basic_stringbuf<charT, traits, Allocator> sb;   // exposition only
  };
}
```

The class `basic_ostringstream<charT, traits, Allocator>` supports
writing objects of class `basic_string<{}charT, traits, Allocator>`. It
uses a `basic_stringbuf` object to control the associated storage. For
the sake of exposition, the maintained data is presented here as:

- `sb`, the `stringbuf` object.

#### Constructors <a id="ostringstream.cons">[[ostringstream.cons]]</a>

``` cpp
explicit basic_ostringstream(ios_base::openmode which);
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(which | ios_base::out)`[[stringbuf.cons]].

``` cpp
explicit basic_ostringstream(
  const basic_string<charT, traits, Allocator>& s,
  ios_base::openmode which = ios_base::out);
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(s, which | ios_base::out)`[[stringbuf.cons]].

``` cpp
basic_ostringstream(ios_base::openmode which, const Allocator& a);
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(which | ios_base::out, a)`[[stringbuf.cons]].

``` cpp
explicit basic_ostringstream(
  basic_string<charT, traits, Allocator>&& s,
  ios_base::openmode which = ios_base::out);
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(std::move(s), which | ios_base::out)`[[stringbuf.cons]].

``` cpp
template<class SAlloc>
  basic_ostringstream(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which, const Allocator& a);
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(s, which | ios_base::out, a)`[[stringbuf.cons]].

``` cpp
template<class SAlloc>
  explicit basic_ostringstream(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which = ios_base::out);
```

*Constraints:* `is_same_v<SAlloc,Allocator>` is `false`.

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream]] and `sb` with
`basic_stringbuf<charT, traits, Allocator>(s, which | ios_base::out)`[[stringbuf.cons]].

``` cpp
basic_ostringstream(basic_ostringstream&& rhs);
```

*Effects:* Move constructs from the rvalue `rhs`. This is accomplished
by move constructing the base class, and the contained
`basic_stringbuf`. Then calls
`basic_ostream<charT, traits>::set_rdbuf(addressof(sb))` to install the
contained `basic_stringbuf`.

#### Swap <a id="ostringstream.swap">[[ostringstream.swap]]</a>

``` cpp
void swap(basic_ostringstream& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_ostream<charT, traits>::swap(rhs);
sb.swap(rhs.sb);
```

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_ostringstream<charT, traits, Allocator>& x,
            basic_ostringstream<charT, traits, Allocator>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="ostringstream.members">[[ostringstream.members]]</a>

``` cpp
basic_stringbuf<charT, traits, Allocator>* rdbuf() const;
```

*Returns:*
`const_cast<basic_stringbuf<charT, traits, Allocator>*>(addressof(sb))`.

``` cpp
basic_string<charT, traits, Allocator> str() const &;
```

*Effects:* Equivalent to: `return rdbuf()->str();`

``` cpp
template<class SAlloc>
  basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
```

*Effects:* Equivalent to: `return rdbuf()->str(sa);`

``` cpp
basic_string<charT,traits,Allocator> str() &&;
```

*Effects:* Equivalent to: `return std::move(*rdbuf()).str();`

``` cpp
basic_string_view<charT, traits> view() const noexcept;
```

*Effects:* Equivalent to: `return rdbuf()->view();`

``` cpp
void str(const basic_string<charT, traits, Allocator>& s);
```

*Effects:* Equivalent to: `rdbuf()->str(s);`

``` cpp
template<class SAlloc>
  void str(const basic_string<charT, traits, SAlloc>& s);
```

*Effects:* Equivalent to: `rdbuf()->str(s);`

``` cpp
void str(basic_string<charT, traits, Allocator>&& s);
```

*Effects:* Equivalent to: `rdbuf()->str(std::move(s));`

### Class template `basic_stringstream` <a id="stringstream">[[stringstream]]</a>

#### General <a id="stringstream.general">[[stringstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_stringstream : public basic_iostream<charT, traits> {
  public:
    using char_type      = charT;
    using int_type       = typename traits::int_type;
    using pos_type       = typename traits::pos_type;
    using off_type       = typename traits::off_type;
    using traits_type    = traits;
    using allocator_type = Allocator;

    // [stringstream.cons], constructors
    basic_stringstream() : basic_stringstream(ios_base::out | ios_base::in) {}
    explicit basic_stringstream(ios_base::openmode which);
    explicit basic_stringstream(
      const basic_string<charT, traits, Allocator>& s,
      ios_base::openmode which = ios_base::out | ios_base::in);
    basic_stringstream(ios_base::openmode which, const Allocator& a);
    explicit basic_stringstream(
      basic_string<charT, traits, Allocator>&& s,
      ios_base::openmode which = ios_base::out | ios_base::in);
    template<class SAlloc>
      basic_stringstream(
        const basic_string<charT, traits, SAlloc>& s, const Allocator& a)
        : basic_stringstream(s, ios_base::out | ios_base::in, a) {}
    template<class SAlloc>
      basic_stringstream(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which, const Allocator& a);
    template<class SAlloc>
      explicit basic_stringstream(
        const basic_string<charT, traits, SAlloc>& s,
        ios_base::openmode which = ios_base::out | ios_base::in);
    basic_stringstream(const basic_stringstream&) = delete;
    basic_stringstream(basic_stringstream&& rhs);

    basic_stringstream& operator=(const basic_stringstream&) = delete;
    basic_stringstream& operator=(basic_stringstream&& rhs);

    // [stringstream.swap], swap
    void swap(basic_stringstream& rhs);

    // [stringstream.members], members
    basic_stringbuf<charT, traits, Allocator>* rdbuf() const;

    basic_string<charT, traits, Allocator> str() const &;
    template<class SAlloc>
      basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
    basic_string<charT, traits, Allocator> str() &&;
    basic_string_view<charT, traits> view() const noexcept;

    void str(const basic_string<charT, traits, Allocator>& s);
    template<class SAlloc>
      void str(const basic_string<charT, traits, SAlloc>& s);
    void str(basic_string<charT, traits, Allocator>&& s);

  private:
    basic_stringbuf<charT, traits> sb;  // exposition only
  };
}
```

The class template `basic_stringstream<charT, traits>` supports reading
and writing from objects of class
`basic_string<charT, traits, Allocator>`. It uses a
`basic_stringbuf<charT, traits, Allocator>` object to control the
associated sequence. For the sake of exposition, the maintained data is
presented here as

- `sb`, the `stringbuf` object.

#### Constructors <a id="stringstream.cons">[[stringstream.cons]]</a>

``` cpp
explicit basic_stringstream(ios_base::openmode which);
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with `basic_stringbuf<charT, traits, Allocator>(which)`.

``` cpp
explicit basic_stringstream(
  const basic_string<charT, traits, Allocator>& s,
  ios_base::openmode which = ios_base::out | ios_base::in);
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with `basic_stringbuf<charT, traits, Allocator>(s, which)`.

``` cpp
basic_stringstream(ios_base::openmode which, const Allocator& a);
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with
`basic_stringbuf<charT, traits, Allocator>(which, a)`[[stringbuf.cons]].

``` cpp
explicit basic_stringstream(
  basic_string<charT, traits, Allocator>&& s,
  ios_base::openmode which = ios_base::out | ios_base::in);
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with
`basic_stringbuf<charT, traits, Allocator>(std::move(s), which)`[[stringbuf.cons]].

``` cpp
template<class SAlloc>
  basic_stringstream(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which, const Allocator& a);
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with
`basic_stringbuf<charT, traits, Allocator>(s, which, a)`[[stringbuf.cons]].

``` cpp
template<class SAlloc>
  explicit basic_stringstream(
    const basic_string<charT, traits, SAlloc>& s,
    ios_base::openmode which = ios_base::out | ios_base::in);
```

*Constraints:* `is_same_v<SAlloc,Allocator>` is `false`.

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with
`basic_stringbuf<charT, traits, Allocator>(s, which)`[[stringbuf.cons]].

``` cpp
basic_stringstream(basic_stringstream&& rhs);
```

*Effects:* Move constructs from the rvalue `rhs`. This is accomplished
by move constructing the base class, and the contained
`basic_stringbuf`. Then calls
`basic_istream<charT, traits>::set_rdbuf(addressof(sb))` to install the
contained `basic_stringbuf`.

#### Swap <a id="stringstream.swap">[[stringstream.swap]]</a>

``` cpp
void swap(basic_stringstream& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_iostream<charT,traits>::swap(rhs);
sb.swap(rhs.sb);
```

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_stringstream<charT, traits, Allocator>& x,
            basic_stringstream<charT, traits, Allocator>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="stringstream.members">[[stringstream.members]]</a>

``` cpp
basic_stringbuf<charT, traits, Allocator>* rdbuf() const;
```

*Returns:*
`const_cast<basic_stringbuf<charT, traits, Allocator>*>(addressof(sb))`.

``` cpp
basic_string<charT, traits, Allocator> str() const &;
```

*Effects:* Equivalent to: `return rdbuf()->str();`

``` cpp
template<class SAlloc>
  basic_string<charT,traits,SAlloc> str(const SAlloc& sa) const;
```

*Effects:* Equivalent to: `return rdbuf()->str(sa);`

``` cpp
basic_string<charT,traits,Allocator> str() &&;
```

*Effects:* Equivalent to: `return std::move(*rdbuf()).str();`

``` cpp
basic_string_view<charT, traits> view() const noexcept;
```

*Effects:* Equivalent to: `return rdbuf()->view();`

``` cpp
void str(const basic_string<charT, traits, Allocator>& s);
```

*Effects:* Equivalent to: `rdbuf()->str(s);`

``` cpp
template<class SAlloc>
  void str(const basic_string<charT, traits, SAlloc>& s);
```

*Effects:* Equivalent to: `rdbuf()->str(s);`

``` cpp
void str(basic_string<charT, traits, Allocator>&& s);
```

*Effects:* Equivalent to: `rdbuf()->str(std::move(s));`

## Span-based streams <a id="span.streams">[[span.streams]]</a>

### Overview <a id="span.streams.overview">[[span.streams.overview]]</a>

The header `<spanstream>` defines class templates and types that
associate stream buffers with objects whose types are specializations of
`span` as described in [[views.span]].

[*Note 1*: A user of these classes is responsible for ensuring that the
character sequence represented by the given `span` outlives the use of
the sequence by objects of the classes in subclause [[span.streams]].
Using multiple `basic_spanbuf` objects referring to overlapping
underlying sequences from different threads, where at least one
`basic_spanbuf` object is used for writing to the sequence, results in a
data race. — *end note*]

### Header `<spanstream>` synopsis <a id="spanstream.syn">[[spanstream.syn]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
    class basic_spanbuf;

  template<class charT, class traits>
    void swap(basic_spanbuf<charT, traits>& x, basic_spanbuf<charT, traits>& y);

  using spanbuf = basic_spanbuf<char>;
  using wspanbuf = basic_spanbuf<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_ispanstream;

  template<class charT, class traits>
    void swap(basic_ispanstream<charT, traits>& x, basic_ispanstream<charT, traits>& y);

  using ispanstream = basic_ispanstream<char>;
  using wispanstream = basic_ispanstream<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_ospanstream;

  template<class charT, class traits>
    void swap(basic_ospanstream<charT, traits>& x, basic_ospanstream<charT, traits>& y);

  using ospanstream = basic_ospanstream<char>;
  using wospanstream = basic_ospanstream<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_spanstream;

  template<class charT, class traits>
    void swap(basic_spanstream<charT, traits>& x, basic_spanstream<charT, traits>& y);

  using spanstream = basic_spanstream<char>;
  using wspanstream = basic_spanstream<wchar_t>;
}
```

### Class template `basic_spanbuf` <a id="spanbuf">[[spanbuf]]</a>

#### General <a id="spanbuf.general">[[spanbuf.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_spanbuf
    : public basic_streambuf<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [spanbuf.cons], constructors
    basic_spanbuf() : basic_spanbuf(ios_base::in | ios_base::out) {}
    explicit basic_spanbuf(ios_base::openmode which)
      : basic_spanbuf(std::span<charT>(), which) {}
    explicit basic_spanbuf(std::span<charT> s,
                           ios_base::openmode which = ios_base::in | ios_base::out);
    basic_spanbuf(const basic_spanbuf&) = delete;
    basic_spanbuf(basic_spanbuf&& rhs);

    // [spanbuf.assign], assignment and swap
    basic_spanbuf& operator=(const basic_spanbuf&) = delete;
    basic_spanbuf& operator=(basic_spanbuf&& rhs);
    void swap(basic_spanbuf& rhs);

    // [spanbuf.members], member functions
    std::span<charT> span() const noexcept;
    void span(std::span<charT> s) noexcept;

  protected:
    // [spanbuf.virtuals], overridden virtual functions
    basic_streambuf<charT, traits>* setbuf(charT*, streamsize) override;
    pos_type seekoff(off_type off, ios_base::seekdir way,
                     ios_base::openmode which = ios_base::in | ios_base::out) override;
    pos_type seekpos(pos_type sp,
                     ios_base::openmode which = ios_base::in | ios_base::out) override;

  private:
    ios_base::openmode mode;            // exposition only
    std::span<charT> buf;               // exposition only
};
}
```

The class template `basic_spanbuf` is derived from `basic_streambuf` to
associate possibly the input sequence and possibly the output sequence
with a sequence of arbitrary characters. The sequence is provided by an
object of class `span<charT>`.

For the sake of exposition, the maintained data is presented here as:

- `ios_base::openmode mode`, has `in` set if the input sequence can be
  read, and `out` set if the output sequence can be written.
- `std::span<charT> buf` is the view to the underlying character
  sequence.

#### Constructors <a id="spanbuf.cons">[[spanbuf.cons]]</a>

``` cpp
explicit basic_spanbuf(std::span<charT> s,
                       ios_base::openmode which = ios_base::in | ios_base::out);
```

*Effects:* Initializes the base class with
`basic_streambuf()`[[streambuf.cons]], and *mode* with `which`.
Initializes the internal pointers as if calling `span(s)`.

``` cpp
basic_spanbuf(basic_spanbuf&& rhs);
```

*Effects:* Initializes the base class with `std::move(rhs)` and *mode*
with `std::move(rhs.`*`mode`*`)` and *buf* with
`std::move(rhs.`*`buf`*`)`. The sequence pointers in `*this` (`eback()`,
`gptr()`, `egptr()`, `pbase()`, `pptr()`, `epptr()`) obtain the values
which `rhs` had. It is *implementation-defined* whether
`rhs.`*`buf`*`.empty()` returns `true` after the move.

*Ensures:* Let `rhs_p` refer to the state of `rhs` just prior to this
construction.

- `span().data() == rhs_p.span().data()`
- `span().size() == rhs_p.span().size()`
- `eback() == rhs_p.eback()`
- `gptr() == rhs_p.gptr()`
- `egptr() == rhs_p.egptr()`
- `pbase() == rhs_p.pbase()`
- `pptr() == rhs_p.pptr()`
- `epptr() == rhs_p.epptr()`
- `getloc() == rhs_p.getloc()`

#### Assignment and swap <a id="spanbuf.assign">[[spanbuf.assign]]</a>

``` cpp
basic_spanbuf& operator=(basic_spanbuf&& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_spanbuf tmp{std::move(rhs)};
this->swap(tmp);
return *this;
```

``` cpp
void swap(basic_spanbuf& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_streambuf<charT, traits>::swap(rhs);
std::swap(mode, rhs.mode);
std::swap(buf, rhs.buf);
```

``` cpp
template<class charT, class traits>
  void swap(basic_spanbuf<charT, traits>& x, basic_spanbuf<charT, traits>& y);
```

*Effects:* Equivalent to `x.swap(y)`.

#### Member functions <a id="spanbuf.members">[[spanbuf.members]]</a>

``` cpp
std::span<charT> span() const noexcept;
```

*Returns:* If `ios_base::out` is set in *mode*, returns
`std::span<charT>(pbase(), pptr())`, otherwise returns *buf*.

[*Note 1*: In contrast to `basic_stringbuf`, the underlying sequence
never grows and is not owned. An owning copy can be obtained by
converting the result to `basic_string<charT>`. — *end note*]

``` cpp
void span(std::span<charT> s) noexcept;
```

*Effects:* *`buf`*` = s`. Initializes the input and output sequences
according to *mode*.

*Ensures:*

- If `ios_base::out` is set in *mode*,
  `pbase() == s.data() && epptr() == pbase() + s.size()` is `true`;
  - in addition, if `ios_base::ate` is set in *mode*,
    `pptr() == pbase() + s.size()` is `true`,
  - otherwise `pptr() == pbase()` is `true`.
- If `ios_base::in` is set in *mode*,
  `eback() == s.data() && gptr() == eback() && egptr() == eback() + s.size()`
  is `true`.

#### Overridden virtual functions <a id="spanbuf.virtuals">[[spanbuf.virtuals]]</a>

[*Note 1*: Because the underlying buffer is of fixed size, neither
`overflow`, `underflow`, nor `pbackfail` can provide useful
behavior. — *end note*]

``` cpp
pos_type seekoff(off_type off, ios_base::seekdir way,
                 ios_base::openmode which = ios_base::in | ios_base::out) override;
```

*Effects:* Alters the stream position within one or both of the
controlled sequences, if possible, as follows:

- If `ios_base::in` is set in `which`, positions the input sequence;
  `xnext` is `gptr()`, `xbeg` is `eback()`.
- If `ios_base::out` is set in `which`, positions the output sequence;
  `xnext` is `pptr()`, `xbeg` is `pbase()`.

If both `ios_base::in` and `ios_base::out` are set in `which` and `way`
is `ios_base::cur`, the positioning operation fails.

For a sequence to be positioned, if its next pointer `xnext` (either
`gptr()` or `pptr()`) is a null pointer and the new offset `newoff` as
computed below is nonzero, the positioning operation fails. Otherwise,
the function determines `baseoff` as a value of type `off_type` as
follows:

- `0` when `way` is `ios_base::beg`;
- `(pptr() - pbase())` for the output sequence, or `(gptr() - eback())`
  for the input sequence when `way` is `ios_base::cur`;
- when `way` is `ios_base::end` :
  - `(pptr() - pbase())` if `ios_base::out` is set in *mode* and
    `ios_base::in` is not set in *mode*,
  - `buf.size()` otherwise.

If `baseoff` + `off` would overflow, or if `baseoff` + `off` is less
than zero, or if `baseoff` + `off` is greater than *`buf`*`.size()`, the
positioning operation fails. Otherwise, the function computes

``` cpp
off_type newoff = baseoff + off;
```

and assigns `xbeg + newoff` to the next pointer `xnext`.

*Returns:* `pos_type(off_type(-1))` if the positioning operation fails;
`pos_type(newoff)` otherwise.

``` cpp
pos_type seekpos(pos_type sp, ios_base::openmode which = ios_base::in | ios_base::out) override;
```

*Effects:* Equivalent to:

``` cpp
return seekoff(off_type(sp), ios_base::beg, which);
```

``` cpp
basic_streambuf<charT, traits>* setbuf(charT* s, streamsize n) override;
```

*Effects:* Equivalent to:

``` cpp
this->span(std::span<charT>(s, n));
return this;
```

### Class template `basic_ispanstream` <a id="ispanstream">[[ispanstream]]</a>

#### General <a id="ispanstream.general">[[ispanstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_ispanstream
    : public basic_istream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [ispanstream.cons], constructors
    explicit basic_ispanstream(std::span<charT> s,
                               ios_base::openmode which = ios_base::in);
    basic_ispanstream(const basic_ispanstream&) = delete;
    basic_ispanstream(basic_ispanstream&& rhs);
    template<class ROS> explicit basic_ispanstream(ROS&& s);

    basic_ispanstream& operator=(const basic_ispanstream&) = delete;
    basic_ispanstream& operator=(basic_ispanstream&& rhs);

    // [ispanstream.swap], swap
    void swap(basic_ispanstream& rhs);

    // [ispanstream.members], member functions
    basic_spanbuf<charT, traits>* rdbuf() const noexcept;

    std::span<const charT> span() const noexcept;
    void span(std::span<charT> s) noexcept;
    template<class ROS> void span(ROS&& s) noexcept;

  private:
    basic_spanbuf<charT, traits> sb;    // exposition only
  };
}
```

[*Note 1*: Constructing an `ispanstream` from a *string-literal*
includes the termination character `'\0'` in the underlying
`spanbuf`. — *end note*]

#### Constructors <a id="ispanstream.cons">[[ispanstream.cons]]</a>

``` cpp
explicit basic_ispanstream(std::span<charT> s, ios_base::openmode which = ios_base::in);
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))` and `sb` with
`basic_spanbuf<charT, traits>(s, which | ios_base::in)`[[spanbuf.cons]].

``` cpp
basic_ispanstream(basic_ispanstream&& rhs);
```

*Effects:* Initializes the base class with `std::move(rhs)` and `sb`
with `std::move(rhs.sb)`. Next,
`basic_istream<charT, traits>::set_rdbuf(addressof(sb))` is called to
install the contained `basic_spanbuf`.

``` cpp
template<class ROS> explicit basic_ispanstream(ROS&& s)
```

*Constraints:* `ROS` models `ranges::borrowed_range`.
`!convertible_to<ROS, std::span<charT>> && convertible_to<ROS, std::span<charT const>>`
is `true`.

*Effects:* Let `sp` be `std::span<const charT>(std::forward<ROS>(s))`.
Equivalent to

``` cpp
basic_ispanstream(std::span<charT>(const_cast<charT*>(sp.data()), sp.size()))
```

#### Swap <a id="ispanstream.swap">[[ispanstream.swap]]</a>

``` cpp
void swap(basic_ispanstream& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_istream<charT, traits>::swap(rhs);
sb.swap(rhs.sb);
```

``` cpp
template<class charT, class traits>
  void swap(basic_ispanstream<charT, traits>& x, basic_ispanstream<charT, traits>& y);
```

*Effects:* Equivalent to `x.swap(y)`.

#### Member functions <a id="ispanstream.members">[[ispanstream.members]]</a>

``` cpp
basic_spanbuf<charT, traits>* rdbuf() const noexcept;
```

*Effects:* Equivalent to:

``` cpp
return const_cast<basic_spanbuf<charT, traits>*>(addressof(sb));
```

``` cpp
std::span<const charT> span() const noexcept;
```

*Effects:* Equivalent to: `return rdbuf()->span();`

``` cpp
void span(std::span<charT> s) noexcept;
```

*Effects:* Equivalent to `rdbuf()->span(s)`.

``` cpp
template<class ROS> void span(ROS&& s) noexcept;
```

*Constraints:* `ROS` models `ranges::borrowed_range`.
`(!convertible_to<ROS, std::span<charT>>) && convertible_to<ROS, std::span<const charT>>`
is `true`.

*Effects:* Let `sp` be `std::span<const charT>(std::forward<ROS>(s))`.
Equivalent to:

``` cpp
this->span(std::span<charT>(const_cast<charT*>(sp.data()), sp.size()))
```

### Class template `basic_ospanstream` <a id="ospanstream">[[ospanstream]]</a>

#### General <a id="ospanstream.general">[[ospanstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_ospanstream
    : public basic_ostream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [ospanstream.cons], constructors
    explicit basic_ospanstream(std::span<charT> s,
                               ios_base::openmode which = ios_base::out);
    basic_ospanstream(const basic_ospanstream&) = delete;
    basic_ospanstream(basic_ospanstream&& rhs);

    basic_ospanstream& operator=(const basic_ospanstream&) = delete;
    basic_ospanstream& operator=(basic_ospanstream&& rhs);

    // [ospanstream.swap], swap
    void swap(basic_ospanstream& rhs);

    // [ospanstream.members], member functions
    basic_spanbuf<charT, traits>* rdbuf() const noexcept;

    std::span<charT> span() const noexcept;
    void span(std::span<charT> s) noexcept;

  private:
    basic_spanbuf<charT, traits> sb;    // exposition only
  };
}
```

#### Constructors <a id="ospanstream.cons">[[ospanstream.cons]]</a>

``` cpp
explicit basic_ospanstream(std::span<charT> s,
                           ios_base::openmode which = ios_base::out);
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))` and `sb` with
`basic_spanbuf<charT, traits>(s, which | ios_base::out)`[[spanbuf.cons]].

``` cpp
basic_ospanstream(basic_ospanstream&& rhs) noexcept;
```

*Effects:* Initializes the base class with `std::move(rhs)` and `sb`
with `std::move(rhs.sb)`. Next,
`basic_ostream<charT, traits>::set_rdbuf(addressof(sb))` is called to
install the contained `basic_spanbuf`.

#### Swap <a id="ospanstream.swap">[[ospanstream.swap]]</a>

``` cpp
void swap(basic_ospanstream& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_ostream<charT, traits>::swap(rhs);
sb.swap(rhs.sb);
```

``` cpp
template<class charT, class traits>
  void swap(basic_ospanstream<charT, traits>& x, basic_ospanstream<charT, traits>& y);
```

*Effects:* Equivalent to `x.swap(y)`.

#### Member functions <a id="ospanstream.members">[[ospanstream.members]]</a>

``` cpp
basic_spanbuf<charT, traits>* rdbuf() const noexcept;
```

*Effects:* Equivalent to:

``` cpp
return const_cast<basic_spanbuf<charT, traits>*>(addressof(sb));
```

``` cpp
std::span<charT> span() const noexcept;
```

*Effects:* Equivalent to: `return rdbuf()->span();`

``` cpp
void span(std::span<charT> s) noexcept;
```

*Effects:* Equivalent to `rdbuf()->span(s)`.

### Class template `basic_spanstream` <a id="spanstream">[[spanstream]]</a>

#### General <a id="spanstream.general">[[spanstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_spanstream
    : public basic_iostream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [spanstream.cons], constructors
    explicit basic_spanstream(std::span<charT> s,
                              ios_base::openmode which = ios_base::out | ios_base::in);
    basic_spanstream(const basic_spanstream&) = delete;
    basic_spanstream(basic_spanstream&& rhs);

    basic_spanstream& operator=(const basic_spanstream&) = delete;
    basic_spanstream& operator=(basic_spanstream&& rhs);

    // [spanstream.swap], swap
    void swap(basic_spanstream& rhs);

    // [spanstream.members], members
    basic_spanbuf<charT, traits>* rdbuf() const noexcept;

    std::span<charT> span() const noexcept;
    void span(std::span<charT> s) noexcept;

  private:
    basic_spanbuf<charT, traits> sb;    // exposition only
  };
}
```

#### Constructors <a id="spanstream.cons">[[spanstream.cons]]</a>

``` cpp
explicit basic_spanstream(std::span<charT> s,
                          ios_base::openmode which = ios_base::out | ios_bas::in);
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))` and `sb` with
`basic_spanbuf<charT, traits>(s, which)`[[spanbuf.cons]].

``` cpp
basic_spanstream(basic_spanstream&& rhs);
```

*Effects:* Initializes the base class with `std::move(rhs)` and `sb`
with `std::move(rhs.sb)`. Next,
`basic_iostream<charT, traits>::set_rdbuf(addressof(sb))` is called to
install the contained `basic_spanbuf`.

#### Swap <a id="spanstream.swap">[[spanstream.swap]]</a>

``` cpp
void swap(basic_spanstream& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_iostream<charT, traits>::swap(rhs);
sb.swap(rhs.sb);
```

``` cpp
template<class charT, class traits>
  void swap(basic_spanstream<charT, traits>& x, basic_spanstream<charT, traits>& y);
```

*Effects:* Equivalent to `x.swap(y)`.

#### Member functions <a id="spanstream.members">[[spanstream.members]]</a>

``` cpp
basic_spanbuf<charT, traits>* rdbuf() const noexcept;
```

*Effects:* Equivalent to:

``` cpp
return const_cast<basic_spanbuf<charT, traits>*>(addressof(sb));
```

``` cpp
std::span<charT> span() const noexcept;
```

*Effects:* Equivalent to: `return rdbuf()->span();`

``` cpp
void span(std::span<charT> s) noexcept;
```

*Effects:* Equivalent to `rdbuf()->span(s)`.

## File-based streams <a id="file.streams">[[file.streams]]</a>

### Header `<fstream>` synopsis <a id="fstream.syn">[[fstream.syn]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
    class basic_filebuf;

  template<class charT, class traits>
    void swap(basic_filebuf<charT, traits>& x, basic_filebuf<charT, traits>& y);

  using filebuf  = basic_filebuf<char>;
  using wfilebuf = basic_filebuf<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_ifstream;

  template<class charT, class traits>
    void swap(basic_ifstream<charT, traits>& x, basic_ifstream<charT, traits>& y);

  using ifstream  = basic_ifstream<char>;
  using wifstream = basic_ifstream<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_ofstream;

  template<class charT, class traits>
    void swap(basic_ofstream<charT, traits>& x, basic_ofstream<charT, traits>& y);

  using ofstream  = basic_ofstream<char>;
  using wofstream = basic_ofstream<wchar_t>;

  template<class charT, class traits = char_traits<charT>>
    class basic_fstream;

  template<class charT, class traits>
    void swap(basic_fstream<charT, traits>& x, basic_fstream<charT, traits>& y);

  using fstream  = basic_fstream<char>;
  using wfstream = basic_fstream<wchar_t>;
}
```

The header `<fstream>` defines four class templates and eight types that
associate stream buffers with files and assist reading and writing
files.

[*Note 1*: The class template `basic_filebuf` treats a file as a source
or sink of bytes. In an environment that uses a large character set, the
file typically holds multibyte character sequences and the
`basic_filebuf` object converts those multibyte sequences into wide
character sequences. — *end note*]

In subclause  [[file.streams]], member functions taking arguments of
`const filesystem::path::value_type*` are only provided on systems where
`filesystem::path::value_type` [[fs.class.path]] is not `char`.

[*Note 2*: These functions enable class `path` support for systems with
a wide native path character type, such as `wchar_t`. — *end note*]

### Class template `basic_filebuf` <a id="filebuf">[[filebuf]]</a>

#### General <a id="filebuf.general">[[filebuf.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_filebuf : public basic_streambuf<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [filebuf.cons], constructors/destructor
    basic_filebuf();
    basic_filebuf(const basic_filebuf&) = delete;
    basic_filebuf(basic_filebuf&& rhs);
    virtual ~basic_filebuf();

    // [filebuf.assign], assignment and swap
    basic_filebuf& operator=(const basic_filebuf&) = delete;
    basic_filebuf& operator=(basic_filebuf&& rhs);
    void swap(basic_filebuf& rhs);

    // [filebuf.members], members
    bool is_open() const;
    basic_filebuf* open(const char* s, ios_base::openmode mode);
    basic_filebuf* open(const filesystem::path::value_type* s,
                        ios_base::openmode mode);   // wide systems only; see [fstream.syn]
    basic_filebuf* open(const string& s,
                        ios_base::openmode mode);
    basic_filebuf* open(const filesystem::path& s,
                        ios_base::openmode mode);
    basic_filebuf* close();

  protected:
    // [filebuf.virtuals], overridden virtual functions
    streamsize showmanyc() override;
    int_type underflow() override;
    int_type uflow() override;
    int_type pbackfail(int_type c = traits::eof()) override;
    int_type overflow (int_type c = traits::eof()) override;

    basic_streambuf<charT, traits>* setbuf(char_type* s,
                                           streamsize n) override;
    pos_type seekoff(off_type off, ios_base::seekdir way,
                     ios_base::openmode which
                      = ios_base::in | ios_base::out) override;
    pos_type seekpos(pos_type sp,
                     ios_base::openmode which
                      = ios_base::in | ios_base::out) override;
    int      sync() override;
    void     imbue(const locale& loc) override;
  };
}
```

The class `basic_filebuf<charT, traits>` associates both the input
sequence and the output sequence with a file.

The restrictions on reading and writing a sequence controlled by an
object of class `basic_filebuf<charT, traits>` are the same as for
reading and writing with the C standard library `FILE`s.

In particular:

- If the file is not open for reading the input sequence cannot be read.
- If the file is not open for writing the output sequence cannot be
  written.
- A joint file position is maintained for both the input sequence and
  the output sequence.

An instance of `basic_filebuf` behaves as described in  [[filebuf]]
provided `traits::pos_type` is `fpos<traits::{}state_type>`. Otherwise
the behavior is undefined.

In order to support file I/O and multibyte/wide character conversion,
conversions are performed using members of a facet, referred to as
`a_codecvt` in following subclauses, obtained as if by

``` cpp
const codecvt<charT, char, typename traits::state_type>& a_codecvt =
  use_facet<codecvt<charT, char, typename traits::state_type>>(getloc());
```

#### Constructors <a id="filebuf.cons">[[filebuf.cons]]</a>

``` cpp
basic_filebuf();
```

*Effects:* Initializes the base class with
`basic_streambuf<charT, traits>()`[[streambuf.cons]].

*Ensures:* `is_open() == false`.

``` cpp
basic_filebuf(basic_filebuf&& rhs);
```

*Effects:* It is *implementation-defined* whether the sequence pointers
in `*this` (`eback()`, `gptr()`, `egptr()`, `pbase()`, `pptr()`,
`epptr()`) obtain the values which `rhs` had. Whether they do or not,
`*this` and `rhs` reference separate buffers (if any at all) after the
construction. Additionally `*this` references the file which `rhs` did
before the construction, and `rhs` references no file after the
construction. The openmode, locale and any other state of `rhs` is also
copied.

*Ensures:* Let `rhs_p` refer to the state of `rhs` just prior to this
construction and let `rhs_a` refer to the state of `rhs` just after this
construction.

- `is_open() == rhs_p.is_open()`
- `rhs_a.is_open() == false`
- `gptr() - eback() == rhs_p.gptr() - rhs_p.eback()`
- `egptr() - eback() == rhs_p.egptr() - rhs_p.eback()`
- `pptr() - pbase() == rhs_p.pptr() - rhs_p.pbase()`
- `epptr() - pbase() == rhs_p.epptr() - rhs_p.pbase()`
- `if (eback()) eback() != rhs_a.eback()`
- `if (gptr()) gptr() != rhs_a.gptr()`
- `if (egptr()) egptr() != rhs_a.egptr()`
- `if (pbase()) pbase() != rhs_a.pbase()`
- `if (pptr()) pptr() != rhs_a.pptr()`
- `if (epptr()) epptr() != rhs_a.epptr()`

``` cpp
virtual ~basic_filebuf();
```

*Effects:* Calls `close()`. If an exception occurs during the
destruction of the object, including the call to `close()`, the
exception is caught but not rethrown
(see  [[res.on.exception.handling]]).

#### Assignment and swap <a id="filebuf.assign">[[filebuf.assign]]</a>

``` cpp
basic_filebuf& operator=(basic_filebuf&& rhs);
```

*Effects:* Calls `close()` then move assigns from `rhs`. After the move
assignment `*this` has the observable state it would have had if it had
been move constructed from `rhs` (see  [[filebuf.cons]]).

*Returns:* `*this`.

``` cpp
void swap(basic_filebuf& rhs);
```

*Effects:* Exchanges the state of `*this` and `rhs`.

``` cpp
template<class charT, class traits>
  void swap(basic_filebuf<charT, traits>& x, basic_filebuf<charT, traits>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="filebuf.members">[[filebuf.members]]</a>

``` cpp
bool is_open() const;
```

*Returns:* `true` if a previous call to `open` succeeded (returned a
non-null value) and there has been no intervening call to close.

``` cpp
basic_filebuf* open(const char* s, ios_base::openmode mode);
basic_filebuf* open(const filesystem::path::value_type* s,
                    ios_base::openmode mode);  // wide systems only; see [fstream.syn]
```

*Preconditions:* `s` points to a NTCTS [[defns.ntcts]].

*Effects:* If `is_open() != false`, returns a null pointer. Otherwise,
initializes the `filebuf` as required. It then opens the file to which
`s` resolves, if possible, as if by a call to `fopen` with the second
argument determined from `mode & ~ios_base::ate` as indicated in
[[filebuf.open.modes]]. If `mode` is not some combination of flags shown
in the table then the open fails.

**Table: File open modes** <a id="filebuf.open.modes">[filebuf.open.modes]</a>

| `binary` | `in` | `out` | `trunc` | `app` | `noreplace` | `stdio` equivalent |
| -------- | ---- | ----- | ------- | ----- | ----------- | ------------------ |
|          |      | +     |         |       |             | `"w"`              |
|          |      | +     |         |       | +           | `"wx"`             |
|          |      | +     | +       |       |             | `"w"`              |
|          |      | +     | +       |       | +           | `"wx"`             |
|          |      | +     |         | +     |             | `"a"`              |
|          |      |       |         | +     |             | `"a"`              |
|          | +    |       |         |       |             | `"r"`              |
|          | +    | +     |         |       |             | `"r+"`             |
|          | +    | +     | +       |       |             | `"w+"`             |
|          | +    | +     | +       |       | +           | `"w+x"`            |
|          | +    | +     |         | +     |             | `"a+"`             |
|          | +    |       |         | +     |             | `"a+"`             |
| +        |      | +     |         |       |             | `"wb"`             |
| +        |      | +     |         |       | +           | `"wbx"`            |
| +        |      | +     | +       |       |             | `"wb"`             |
| +        |      | +     | +       |       | +           | `"wbx"`            |
| +        |      | +     |         | +     |             | `"ab"`             |
| +        |      |       |         | +     |             | `"ab"`             |
| +        | +    |       |         |       |             | `"rb"`             |
| +        | +    | +     |         |       |             | `"r+b"`            |
| +        | +    | +     | +       |       |             | `"w+b"`            |
| +        | +    | +     | +       |       | +           | `"w+bx"`           |
| +        | +    | +     |         | +     |             | `"a+b"`            |
| +        | +    |       |         | +     |             | `"a+b"`            |


If the open operation succeeds and `ios_base::ate` is set in `mode`,
positions the file to the end (as if by calling
`fseek(file, 0, SEEK_END)`, where `file` is the pointer returned by
calling `fopen`).[^38]

If the repositioning operation fails, calls `close()` and returns a null
pointer to indicate failure.

*Returns:* `this` if successful, a null pointer otherwise.

``` cpp
basic_filebuf* open(const string& s, ios_base::openmode mode);
basic_filebuf* open(const filesystem::path& s, ios_base::openmode mode);
```

*Returns:* `open(s.c_str(), mode);`

``` cpp
basic_filebuf* close();
```

*Effects:* If `is_open() == false`, returns a null pointer. If a put
area exists, calls `overflow(traits::eof())` to flush characters. If the
last virtual member function called on `*this` (between `underflow`,
`overflow`, `seekoff`, and `seekpos`) was `overflow` then calls
`a_codecvt.unshift` (possibly several times) to determine a termination
sequence, inserts those characters and calls `overflow(traits::eof())`
again. Finally, regardless of whether any of the preceding calls fails
or throws an exception, the function closes the file (as if by calling
`fclose(file)`). If any of the calls made by the function, including
`fclose`, fails, `close` fails by returning a null pointer. If one of
these calls throws an exception, the exception is caught and rethrown
after closing the file.

*Ensures:* `is_open() == false`.

*Returns:* `this` on success, a null pointer otherwise.

#### Overridden virtual functions <a id="filebuf.virtuals">[[filebuf.virtuals]]</a>

``` cpp
streamsize showmanyc() override;
```

*Effects:* Behaves the same as
`basic_streambuf::showmanyc()`[[streambuf.virtuals]].

*Remarks:* An implementation may provide an overriding definition for
this function signature if it can determine whether more characters can
be read from the input sequence.

``` cpp
int_type underflow() override;
```

*Effects:* Behaves according to the description of
`basic_streambuf<charT, traits>::underflow()`, with the specialization
that a sequence of characters is read from the input sequence as if by
reading from the associated file into an internal buffer (`extern_buf`)
and then as if by doing:

``` cpp
char   extern_buf[XSIZE];
char*  extern_end;
charT  intern_buf[ISIZE];
charT* intern_end;
codecvt_base::result r =
  a_codecvt.in(state, extern_buf, extern_buf+XSIZE, extern_end,
               intern_buf, intern_buf+ISIZE, intern_end);
```

This shall be done in such a way that the class can recover the position
(`fpos_t`) corresponding to each character between `intern_buf` and
`intern_end`. If the value of `r` indicates that `a_codecvt.in()` ran
out of space in `intern_buf`, retry with a larger `intern_buf`.

``` cpp
int_type uflow() override;
```

*Effects:* Behaves according to the description of
`basic_streambuf<charT, traits>::uflow()`, with the specialization that
a sequence of characters is read from the input with the same method as
used by `underflow`.

``` cpp
int_type pbackfail(int_type c = traits::eof()) override;
```

*Effects:* Puts back the character designated by `c` to the input
sequence, if possible, in one of three ways:

- If `traits::eq_int_type(c, traits::eof())` returns `false` and if the
  function makes a putback position available and if
  `traits::eq(to_char_type(c), gptr()[-1])` returns `true`, decrements
  the next pointer for the input sequence, `gptr()`. Returns: `c`.
- If `traits::eq_int_type(c, traits::eof())` returns `false` and if the
  function makes a putback position available and if the function is
  permitted to assign to the putback position, decrements the next
  pointer for the input sequence, and stores `c` there. Returns: `c`.
- If `traits::eq_int_type(c, traits::eof())` returns `true`, and if
  either the input sequence has a putback position available or the
  function makes a putback position available, decrements the next
  pointer for the input sequence, `gptr()`. Returns:
  `traits::not_eof(c)`.

*Returns:* As specified above, or `traits::eof()` to indicate failure.

*Remarks:* If `is_open() == false`, the function always fails.

The function does not put back a character directly to the input
sequence.

If the function can succeed in more than one of these ways, it is
unspecified which way is chosen. The function can alter the number of
putback positions available as a result of any call.

``` cpp
int_type overflow(int_type c = traits::eof()) override;
```

*Effects:* Behaves according to the description of
`basic_streambuf<charT, traits>::overflow(c)`, except that the behavior
of “consuming characters” is performed by first converting as if by:

``` cpp
charT* b = pbase();
charT* p = pptr();
charT* end;
char   xbuf[XSIZE];
char*  xbuf_end;
codecvt_base::result r =
  a_codecvt.out(state, b, p, end, xbuf, xbuf+XSIZE, xbuf_end);
```

and then

- If `r == codecvt_base::error` then fail.
- If `r == codecvt_base::noconv` then output characters from `b` up to
  (and not including) `p`.
- If `r == codecvt_base::partial` then output to the file characters
  from `xbuf` up to `xbuf_end`, and repeat using characters from `end`
  to `p`. If output fails, fail (without repeating).
- Otherwise output from `xbuf` to `xbuf_end`, and fail if output fails.
  At this point if `b != p` and `b == end` (`xbuf` isn’t large enough)
  then increase `XSIZE` and repeat from the beginning.

*Returns:* `traits::not_eof(c)` to indicate success, and `traits::eof()`
to indicate failure. If `is_open() == false`, the function always fails.

``` cpp
basic_streambuf* setbuf(char_type* s, streamsize n) override;
```

*Effects:* If `setbuf(0, 0)` is called on a stream before any I/O has
occurred on that stream, the stream becomes unbuffered. Otherwise the
results are *implementation-defined*. “Unbuffered” means that `pbase()`
and `pptr()` always return null and output to the file should appear as
soon as possible.

``` cpp
pos_type seekoff(off_type off, ios_base::seekdir way,
                 ios_base::openmode which
                   = ios_base::in | ios_base::out) override;
```

*Effects:* Let `width` denote `a_codecvt.encoding()`. If
`is_open() == false`, or `off != 0 && width <= 0`, then the positioning
operation fails. Otherwise, if `way != basic_ios::cur` or `off != 0`,
and if the last operation was output, then update the output sequence
and write any unshift sequence. Next, seek to the new position: if
`width > 0`, call `fseek(file, width * off, whence)`, otherwise call
`fseek(file, 0, whence)`.

*Returns:* A newly constructed `pos_type` object that stores the
resultant stream position, if possible. If the positioning operation
fails, or if the object cannot represent the resultant stream position,
returns `pos_type(off_type(-1))`.

*Remarks:* “The last operation was output” means either the last virtual
operation was overflow or the put buffer is non-empty. “Write any
unshift sequence” means, if `width` if less than zero then call
`a_codecvt.unshift(state, xbuf, xbuf+XSIZE, xbuf_end)` and output the
resulting unshift sequence. The function determines one of three values
for the argument `whence`, of type `int`, as indicated in
[[filebuf.seekoff]].

**Table: `seekoff` effects** <a id="filebuf.seekoff">[filebuf.seekoff]</a>

| `way` Value      | `stdio` Equivalent |
| ---------------- | ------------------ |
| `basic_ios::beg` | `SEEK_SET`         |
| `basic_ios::cur` | `SEEK_CUR`         |
| `basic_ios::end` | `SEEK_END`         |

``` cpp
pos_type seekpos(pos_type sp,
                 ios_base::openmode which
                   = ios_base::in | ios_base::out) override;
```

Alters the file position, if possible, to correspond to the position
stored in `sp` (as described below). Altering the file position performs
as follows:

1.  if `(om & ios_base::out) != 0`, then update the output sequence and
    write any unshift sequence;
2.  set the file position to `sp` as if by a call to `fsetpos`;
3.  if `(om & ios_base::in) != 0`, then update the input sequence;

where `om` is the open mode passed to the last call to `open()`. The
operation fails if `is_open()` returns `false`.

If `sp` is an invalid stream position, or if the function positions
neither sequence, the positioning operation fails. If `sp` has not been
obtained by a previous successful call to one of the positioning
functions (`seekoff` or `seekpos`) on the same file the effects are
undefined.

*Returns:* `sp` on success. Otherwise returns `pos_type(off_type(-1))`.

``` cpp
int sync() override;
```

*Effects:* If a put area exists, calls `filebuf::overflow` to write the
characters to the file, then flushes the file as if by calling
`fflush(file)`. If a get area exists, the effect is
*implementation-defined*.

``` cpp
void imbue(const locale& loc) override;
```

*Preconditions:* If the file is not positioned at its beginning and the
encoding of the current locale as determined by `a_codecvt.encoding()`
is state-dependent [[locale.codecvt.virtuals]] then that facet is the
same as the corresponding facet of `loc`.

*Effects:* Causes characters inserted or extracted after this call to be
converted according to `loc` until another call of `imbue`.

*Remarks:* This may require reconversion of previously converted
characters. This in turn may require the implementation to be able to
reconstruct the original contents of the file.

### Class template `basic_ifstream` <a id="ifstream">[[ifstream]]</a>

#### General <a id="ifstream.general">[[ifstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_ifstream : public basic_istream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [ifstream.cons], constructors
    basic_ifstream();
    explicit basic_ifstream(const char* s,
                            ios_base::openmode mode = ios_base::in);
    explicit basic_ifstream(const filesystem::path::value_type* s,
                            ios_base::openmode mode = ios_base::in);// wide systems only; see [fstream.syn]
    explicit basic_ifstream(const string& s,
                            ios_base::openmode mode = ios_base::in);
    template<class T>
      explicit basic_ifstream(const T& s, ios_base::openmode mode = ios_base::in);
    basic_ifstream(const basic_ifstream&) = delete;
    basic_ifstream(basic_ifstream&& rhs);

    basic_ifstream& operator=(const basic_ifstream&) = delete;
    basic_ifstream& operator=(basic_ifstream&& rhs);

    // [ifstream.swap], swap
    void swap(basic_ifstream& rhs);

    // [ifstream.members], members
    basic_filebuf<charT, traits>* rdbuf() const;

    bool is_open() const;
    void open(const char* s, ios_base::openmode mode = ios_base::in);
    void open(const filesystem::path::value_type* s,
              ios_base::openmode mode = ios_base::in);  // wide systems only; see [fstream.syn]
    void open(const string& s, ios_base::openmode mode = ios_base::in);
    void open(const filesystem::path& s, ios_base::openmode mode = ios_base::in);
    void close();

  private:
    basic_filebuf<charT, traits> sb;    // exposition only
  };
}
```

The class `basic_ifstream<charT, traits>` supports reading from named
files. It uses a `basic_filebuf<{}charT, traits>` object to control the
associated sequence. For the sake of exposition, the maintained data is
presented here as:

- `sb`, the `filebuf` object.

#### Constructors <a id="ifstream.cons">[[ifstream.cons]]</a>

``` cpp
basic_ifstream();
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream.cons]] and `sb`
with `basic_filebuf<charT, traits>()`[[filebuf.cons]].

``` cpp
explicit basic_ifstream(const char* s,
                        ios_base::openmode mode = ios_base::in);
explicit basic_ifstream(const filesystem::path::value_type* s,
                        ios_base::openmode mode = ios_base::in);  // wide systems only; see [fstream.syn]
```

*Effects:* Initializes the base class with
`basic_istream<charT, traits>(addressof(sb))`[[istream.cons]] and `sb`
with `basic_filebuf<charT, traits>()`[[filebuf.cons]], then calls
`rdbuf()->open(s, mode | ios_base::in)`. If that function returns a null
pointer, calls `setstate(failbit)`.

``` cpp
explicit basic_ifstream(const string& s,
                        ios_base::openmode mode = ios_base::in);
```

*Effects:* Equivalent to: `basic_ifstream(s.c_str(), mode)`.

``` cpp
template<class T>
  explicit basic_ifstream(const T& s, ios_base::openmode mode = ios_base::in);
```

*Constraints:* `is_same_v<T, filesystem::path>` is `true`.

*Effects:* Equivalent to: `basic_ifstream(s.c_str(), mode)`.

``` cpp
basic_ifstream(basic_ifstream&& rhs);
```

*Effects:* Move constructs the base class, and the contained
`basic_filebuf`. Then calls
`basic_istream<charT, traits>::set_rdbuf(addressof(sb))` to install the
contained `basic_filebuf`.

#### Swap <a id="ifstream.swap">[[ifstream.swap]]</a>

``` cpp
void swap(basic_ifstream& rhs);
```

*Effects:* Exchanges the state of `*this` and `rhs` by calling
`basic_istream<charT, traits>::swap(rhs)` and `sb.swap(rhs.sb)`.

``` cpp
template<class charT, class traits>
  void swap(basic_ifstream<charT, traits>& x, basic_ifstream<charT, traits>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="ifstream.members">[[ifstream.members]]</a>

``` cpp
basic_filebuf<charT, traits>* rdbuf() const;
```

*Returns:* `const_cast<basic_filebuf<charT, traits>*>(addressof(sb))`.

``` cpp
bool is_open() const;
```

*Returns:* `rdbuf()->is_open()`.

``` cpp
void open(const char* s, ios_base::openmode mode = ios_base::in);
void open(const filesystem::path::value_type* s,
          ios_base::openmode mode = ios_base::in);  // wide systems only; see [fstream.syn]
```

*Effects:* Calls `rdbuf()->open(s, mode | ios_base::in)`. If that
function does not return a null pointer calls `clear()`, otherwise calls
`setstate(failbit)` (which may throw
`ios_base::failure`) [[iostate.flags]].

``` cpp
void open(const string& s, ios_base::openmode mode = ios_base::in);
void open(const filesystem::path& s, ios_base::openmode mode = ios_base::in);
```

*Effects:* Calls `open(s.c_str(), mode)`.

``` cpp
void close();
```

*Effects:* Calls `rdbuf()->close()` and, if that function returns a null
pointer, calls `setstate(failbit)` (which may throw
`ios_base::failure`) [[iostate.flags]].

### Class template `basic_ofstream` <a id="ofstream">[[ofstream]]</a>

#### General <a id="ofstream.general">[[ofstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_ofstream : public basic_ostream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [ofstream.cons], constructors
    basic_ofstream();
    explicit basic_ofstream(const char* s,
                            ios_base::openmode mode = ios_base::out);
    explicit basic_ofstream(const filesystem::path::value_type* s,  // wide systems only; see [fstream.syn]
                            ios_base::openmode mode = ios_base::out);
    explicit basic_ofstream(const string& s,
                            ios_base::openmode mode = ios_base::out);
    template<class T>
      explicit basic_ofstream(const T& s, ios_base::openmode mode = ios_base::out);
    basic_ofstream(const basic_ofstream&) = delete;
    basic_ofstream(basic_ofstream&& rhs);

    basic_ofstream& operator=(const basic_ofstream&) = delete;
    basic_ofstream& operator=(basic_ofstream&& rhs);

    // [ofstream.swap], swap
    void swap(basic_ofstream& rhs);

    // [ofstream.members], members
    basic_filebuf<charT, traits>* rdbuf() const;

    bool is_open() const;
    void open(const char* s, ios_base::openmode mode = ios_base::out);
    void open(const filesystem::path::value_type* s,
              ios_base::openmode mode = ios_base::out);     // wide systems only; see [fstream.syn]
    void open(const string& s, ios_base::openmode mode = ios_base::out);
    void open(const filesystem::path& s, ios_base::openmode mode = ios_base::out);
    void close();

  private:
    basic_filebuf<charT, traits> sb;    // exposition only
  };
}
```

The class `basic_ofstream<charT, traits>` supports writing to named
files. It uses a `basic_filebuf<{}charT, traits>` object to control the
associated sequence. For the sake of exposition, the maintained data is
presented here as:

- `sb`, the `filebuf` object.

#### Constructors <a id="ofstream.cons">[[ofstream.cons]]</a>

``` cpp
basic_ofstream();
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream.cons]] and `sb`
with `basic_filebuf<charT, traits>()`[[filebuf.cons]].

``` cpp
explicit basic_ofstream(const char* s,
                        ios_base::openmode mode = ios_base::out);
explicit basic_ofstream(const filesystem::path::value_type* s,
                        ios_base::openmode mode = ios_base::out); // wide systems only; see [fstream.syn]
```

*Effects:* Initializes the base class with
`basic_ostream<charT, traits>(addressof(sb))`[[ostream.cons]] and `sb`
with `basic_filebuf<charT, traits>()`[[filebuf.cons]], then calls
`rdbuf()->open(s, mode | ios_base::out)`. If that function returns a
null pointer, calls `setstate(failbit)`.

``` cpp
explicit basic_ofstream(const string& s,
                        ios_base::openmode mode = ios_base::out);
```

*Effects:* Equivalent to: `basic_ofstream(s.c_str(), mode)`.

``` cpp
template<class T>
  explicit basic_ofstream(const T& s, ios_base::openmode mode = ios_base::out);
```

*Constraints:* `is_same_v<T, filesystem::path>` is `true`.

*Effects:* Equivalent to: `basic_ofstream(s.c_str(), mode)`.

``` cpp
basic_ofstream(basic_ofstream&& rhs);
```

*Effects:* Move constructs the base class, and the contained
`basic_filebuf`. Then calls
`basic_ostream<charT, traits>::set_rdbuf(addressof(sb))` to install the
contained `basic_filebuf`.

#### Swap <a id="ofstream.swap">[[ofstream.swap]]</a>

``` cpp
void swap(basic_ofstream& rhs);
```

*Effects:* Exchanges the state of `*this` and `rhs` by calling
`basic_ostream<charT, traits>::swap(rhs)` and `sb.swap(rhs.sb)`.

``` cpp
template<class charT, class traits>
  void swap(basic_ofstream<charT, traits>& x, basic_ofstream<charT, traits>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="ofstream.members">[[ofstream.members]]</a>

``` cpp
basic_filebuf<charT, traits>* rdbuf() const;
```

*Returns:* `const_cast<basic_filebuf<charT, traits>*>(addressof(sb))`.

``` cpp
bool is_open() const;
```

*Returns:* `rdbuf()->is_open()`.

``` cpp
void open(const char* s, ios_base::openmode mode = ios_base::out);
void open(const filesystem::path::value_type* s,
          ios_base::openmode mode = ios_base::out);             // wide systems only; see [fstream.syn]
```

*Effects:* Calls `rdbuf()->open(s, mode | ios_base::out)`. If that
function does not return a null pointer calls `clear()`, otherwise calls
`setstate(failbit)` (which may throw
`ios_base::failure`) [[iostate.flags]].

``` cpp
void close();
```

*Effects:* Calls `rdbuf()->close()` and, if that function fails (returns
a null pointer), calls `setstate(failbit)` (which may throw
`ios_base::failure`) [[iostate.flags]].

``` cpp
void open(const string& s, ios_base::openmode mode = ios_base::out);
void open(const filesystem::path& s, ios_base::openmode mode = ios_base::out);
```

*Effects:* Calls `open(s.c_str(), mode)`.

### Class template `basic_fstream` <a id="fstream">[[fstream]]</a>

#### General <a id="fstream.general">[[fstream.general]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class basic_fstream : public basic_iostream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    // [fstream.cons], constructors
    basic_fstream();
    explicit basic_fstream(
      const char* s,
      ios_base::openmode mode = ios_base::in | ios_base::out);
    explicit basic_fstream(
      const filesystem::path::value_type* s,
      ios_base::openmode mode = ios_base::in|ios_base::out);    // wide systems only; see [fstream.syn]
    explicit basic_fstream(
      const string& s,
      ios_base::openmode mode = ios_base::in | ios_base::out);
    template<class T>
      explicit basic_fstream(const T& s, ios_base::openmode mode = ios_base::in | ios_base::out);
    basic_fstream(const basic_fstream&) = delete;
    basic_fstream(basic_fstream&& rhs);

    basic_fstream& operator=(const basic_fstream&) = delete;
    basic_fstream& operator=(basic_fstream&& rhs);

    // [fstream.swap], swap
    void swap(basic_fstream& rhs);

    // [fstream.members], members
    basic_filebuf<charT, traits>* rdbuf() const;
    bool is_open() const;
    void open(
      const char* s,
      ios_base::openmode mode = ios_base::in | ios_base::out);
    void open(
      const filesystem::path::value_type* s,
      ios_base::openmode mode = ios_base::in|ios_base::out);    // wide systems only; see [fstream.syn]
    void open(
      const string& s,
      ios_base::openmode mode = ios_base::in | ios_base::out);
    void open(
      const filesystem::path& s,
      ios_base::openmode mode = ios_base::in | ios_base::out);
    void close();

  private:
    basic_filebuf<charT, traits> sb;    // exposition only
  };
}
```

The class template `basic_fstream<charT, traits>` supports reading and
writing from named files. It uses a `basic_filebuf<charT, traits>`
object to control the associated sequences. For the sake of exposition,
the maintained data is presented here as:

- `sb`, the `basic_filebuf` object.

#### Constructors <a id="fstream.cons">[[fstream.cons]]</a>

``` cpp
basic_fstream();
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with `basic_filebuf<charT, traits>()`.

``` cpp
explicit basic_fstream(
  const char* s,
  ios_base::openmode mode = ios_base::in | ios_base::out);
explicit basic_fstream(
  const filesystem::path::value_type* s,
  ios_base::openmode mode = ios_base::in | ios_base::out);  // wide systems only; see [fstream.syn]
```

*Effects:* Initializes the base class with
`basic_iostream<charT, traits>(addressof(sb))`[[iostream.cons]] and `sb`
with `basic_filebuf<charT, traits>()`. Then calls
`rdbuf()->open(s, mode)`. If that function returns a null pointer, calls
`setstate(failbit)`.

``` cpp
explicit basic_fstream(
  const string& s,
  ios_base::openmode mode = ios_base::in | ios_base::out);
```

*Effects:* Equivalent to: `basic_fstream(s.c_str(), mode)`.

``` cpp
template<class T>
  explicit basic_fstream(const T& s, ios_base::openmode mode = ios_base::in | ios_base::out);
```

*Constraints:* `is_same_v<T, filesystem::path>` is `true`.

*Effects:* Equivalent to: `basic_fstream(s.c_str(), mode)`.

``` cpp
basic_fstream(basic_fstream&& rhs);
```

*Effects:* Move constructs the base class, and the contained
`basic_filebuf`. Then calls
`basic_istream<charT, traits>::set_rdbuf(addressof(sb))` to install the
contained `basic_filebuf`.

#### Swap <a id="fstream.swap">[[fstream.swap]]</a>

``` cpp
void swap(basic_fstream& rhs);
```

*Effects:* Exchanges the state of `*this` and `rhs` by calling
`basic_iostream<charT,traits>::swap(rhs)` and `sb.swap(rhs.sb)`.

``` cpp
template<class charT, class traits>
  void swap(basic_fstream<charT, traits>& x,
            basic_fstream<charT, traits>& y);
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Member functions <a id="fstream.members">[[fstream.members]]</a>

``` cpp
basic_filebuf<charT, traits>* rdbuf() const;
```

*Returns:* `const_cast<basic_filebuf<charT, traits>*>(addressof(sb))`.

``` cpp
bool is_open() const;
```

*Returns:* `rdbuf()->is_open()`.

``` cpp
void open(
  const char* s,
  ios_base::openmode mode = ios_base::in | ios_base::out);
void open(
  const filesystem::path::value_type* s,
  ios_base::openmode mode = ios_base::in | ios_base::out);  // wide systems only; see [fstream.syn]
```

*Effects:* Calls `rdbuf()->open(s, mode)`. If that function does not
return a null pointer calls `clear()`, otherwise calls
`setstate(failbit)` (which may throw
`ios_base::failure`) [[iostate.flags]].

``` cpp
void open(
  const string& s,
  ios_base::openmode mode = ios_base::in | ios_base::out);
void open(
  const filesystem::path& s,
  ios_base::openmode mode = ios_base::in | ios_base::out);
```

*Effects:* Calls `open(s.c_str(), mode)`.

``` cpp
void close();
```

*Effects:* Calls `rdbuf()->close()` and, if that function returns a null
pointer, calls `setstate(failbit)` (which may throw
`ios_base::failure`) [[iostate.flags]].

## Synchronized output streams <a id="syncstream">[[syncstream]]</a>

### Header `<syncstream>` synopsis <a id="syncstream.syn">[[syncstream.syn]]</a>

``` cpp
#include <ostream>  // see [ostream.syn]

namespace std {
  template<class charT, class traits = char_traits<charT>, class Allocator = allocator<charT>>
    class basic_syncbuf;

  // [syncstream.syncbuf.special], specialized algorithms
  template<class charT, class traits, class Allocator>
    void swap(basic_syncbuf<charT, traits, Allocator>&,
              basic_syncbuf<charT, traits, Allocator>&);

  using syncbuf = basic_syncbuf<char>;
  using wsyncbuf = basic_syncbuf<wchar_t>;

  template<class charT, class traits = char_traits<charT>, class Allocator = allocator<charT>>
    class basic_osyncstream;

  using osyncstream = basic_osyncstream<char>;
  using wosyncstream = basic_osyncstream<wchar_t>;
}
```

The header `<syncstream>` provides a mechanism to synchronize execution
agents writing to the same stream.

### Class template `basic_syncbuf` <a id="syncstream.syncbuf">[[syncstream.syncbuf]]</a>

#### Overview <a id="syncstream.syncbuf.overview">[[syncstream.syncbuf.overview]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>, class Allocator = allocator<charT>>
  class basic_syncbuf : public basic_streambuf<charT, traits> {
  public:
    using char_type      = charT;
    using int_type       = typename traits::int_type;
    using pos_type       = typename traits::pos_type;
    using off_type       = typename traits::off_type;
    using traits_type    = traits;
    using allocator_type = Allocator;

    using streambuf_type = basic_streambuf<charT, traits>;

    // [syncstream.syncbuf.cons], construction and destruction
    basic_syncbuf()
      : basic_syncbuf(nullptr) {}
    explicit basic_syncbuf(streambuf_type* obuf)
      : basic_syncbuf(obuf, Allocator()) {}
    basic_syncbuf(streambuf_type*, const Allocator&);
    basic_syncbuf(basic_syncbuf&&);
    ~basic_syncbuf();

    // [syncstream.syncbuf.assign], assignment and swap
    basic_syncbuf& operator=(basic_syncbuf&&);
    void swap(basic_syncbuf&);

    // [syncstream.syncbuf.members], member functions
    bool emit();
    streambuf_type* get_wrapped() const noexcept;
    allocator_type get_allocator() const noexcept;
    void set_emit_on_sync(bool) noexcept;

  protected:
    // [syncstream.syncbuf.virtuals], overridden virtual functions
    int sync() override;

  private:
    streambuf_type* wrapped;    // exposition only
    bool emit_on_sync{};        // exposition only
  };
}
```

Class template `basic_syncbuf` stores character data written to it,
known as the associated output, into internal buffers allocated using
the object’s allocator. The associated output is transferred to the
wrapped stream buffer object `*wrapped` when `emit()` is called or when
the `basic_syncbuf` object is destroyed. Such transfers are atomic with
respect to transfers by other `basic_syncbuf` objects with the same
wrapped stream buffer object.

#### Construction and destruction <a id="syncstream.syncbuf.cons">[[syncstream.syncbuf.cons]]</a>

``` cpp
basic_syncbuf(streambuf_type* obuf, const Allocator& allocator);
```

*Effects:* Sets `wrapped` to `obuf`.

*Ensures:* `get_wrapped() == obuf` and `get_allocator() == allocator`
are `true`.

*Throws:* Nothing unless an exception is thrown by the construction of a
mutex or by memory allocation.

*Remarks:* A copy of `allocator` is used to allocate memory for internal
buffers holding the associated output.

``` cpp
basic_syncbuf(basic_syncbuf&& other);
```

*Ensures:* The value returned by `this->get_wrapped()` is the value
returned by `other.get_wrapped()` prior to calling this constructor.
Output stored in `other` prior to calling this constructor will be
stored in `*this` afterwards. `other.pbase() == other.pptr()` and
`other.get_wrapped() == nullptr` are `true`.

*Remarks:* This constructor disassociates `other` from its wrapped
stream buffer, ensuring destruction of `other` produces no output.

``` cpp
~basic_syncbuf();
```

*Effects:* Calls `emit()`.

*Throws:* Nothing. If an exception is thrown from `emit()`, the
destructor catches and ignores that exception.

#### Assignment and swap <a id="syncstream.syncbuf.assign">[[syncstream.syncbuf.assign]]</a>

``` cpp
basic_syncbuf& operator=(basic_syncbuf&& rhs);
```

*Effects:* Calls `emit()` then move assigns from `rhs`. After the move
assignment `*this` has the observable state it would have had if it had
been move constructed from `rhs`[[syncstream.syncbuf.cons]].

*Ensures:*

- `rhs.get_wrapped() == nullptr` is `true`.
- `this->get_allocator() == rhs.get_allocator()` is `true` when
  ``` cpp
  allocator_traits<Allocator>::propagate_on_container_move_assignment::value
  ```

  is `true`; otherwise, the allocator is unchanged.

*Returns:* `*this`.

*Remarks:* This assignment operator disassociates `rhs` from its wrapped
stream buffer, ensuring destruction of `rhs` produces no output.

``` cpp
void swap(basic_syncbuf& other);
```

*Preconditions:* Either
`allocator_traits<Allocator>::propagate_on_container_swap::value` is
`true` or `this->get_allocator() == other.get_allocator()` is `true`.

*Effects:* Exchanges the state of `*this` and `other`.

#### Member functions <a id="syncstream.syncbuf.members">[[syncstream.syncbuf.members]]</a>

``` cpp
bool emit();
```

*Effects:* Atomically transfers the associated output of `*this` to the
stream buffer `*wrapped`, so that it appears in the output stream as a
contiguous sequence of characters. `wrapped->pubsync()` is called if and
only if a call was made to `sync()` since the most recent call to
`emit()`, if any.

*Synchronization:* All `emit()` calls transferring characters to the
same stream buffer object appear to execute in a total order consistent
with the “happens before” relation [[intro.races]], where each `emit()`
call synchronizes with subsequent `emit()` calls in that total order.

*Ensures:* On success, the associated output is empty.

*Returns:* `true` if all of the following conditions hold; otherwise
`false`:

- `wrapped == nullptr` is `false`.
- All of the characters in the associated output were successfully
  transferred.
- The call to `wrapped->pubsync()` (if any) succeeded.

*Remarks:* May call member functions of `wrapped` while holding a lock
uniquely associated with `wrapped`.

``` cpp
streambuf_type* get_wrapped() const noexcept;
```

*Returns:* `wrapped`.

``` cpp
allocator_type get_allocator() const noexcept;
```

*Returns:* A copy of the allocator that was set in the constructor or
assignment operator.

``` cpp
void set_emit_on_sync(bool b) noexcept;
```

*Effects:* `emit_on_sync = b`.

#### Overridden virtual functions <a id="syncstream.syncbuf.virtuals">[[syncstream.syncbuf.virtuals]]</a>

``` cpp
int sync() override;
```

*Effects:* Records that the wrapped stream buffer is to be flushed.
Then, if `emit_on_sync` is `true`, calls `emit()`.

[*Note 1*: If `emit_on_sync` is `false`, the actual flush is delayed
until a call to `emit()`. — *end note*]

*Returns:* If `emit()` was called and returned `false`, returns `-1`;
otherwise `0`.

#### Specialized algorithms <a id="syncstream.syncbuf.special">[[syncstream.syncbuf.special]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_syncbuf<charT, traits, Allocator>& a,
            basic_syncbuf<charT, traits, Allocator>& b);
```

*Effects:* Equivalent to `a.swap(b)`.

### Class template `basic_osyncstream` <a id="syncstream.osyncstream">[[syncstream.osyncstream]]</a>

#### Overview <a id="syncstream.osyncstream.overview">[[syncstream.osyncstream.overview]]</a>

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>, class Allocator = allocator<charT>>
  class basic_osyncstream : public basic_ostream<charT, traits> {
  public:
    using char_type   = charT;
    using int_type    = typename traits::int_type;
    using pos_type    = typename traits::pos_type;
    using off_type    = typename traits::off_type;
    using traits_type = traits;

    using allocator_type = Allocator;
    using streambuf_type = basic_streambuf<charT, traits>;
    using syncbuf_type   = basic_syncbuf<charT, traits, Allocator>;

    // [syncstream.osyncstream.cons], construction and destruction
    basic_osyncstream(streambuf_type*, const Allocator&);
    explicit basic_osyncstream(streambuf_type* obuf)
      : basic_osyncstream(obuf, Allocator()) {}
    basic_osyncstream(basic_ostream<charT, traits>& os, const Allocator& allocator)
      : basic_osyncstream(os.rdbuf(), allocator) {}
    explicit basic_osyncstream(basic_ostream<charT, traits>& os)
      : basic_osyncstream(os, Allocator()) {}
    basic_osyncstream(basic_osyncstream&&) noexcept;
    ~basic_osyncstream();

    // assignment
    basic_osyncstream& operator=(basic_osyncstream&&);

    // [syncstream.osyncstream.members], member functions
    void emit();
    streambuf_type* get_wrapped() const noexcept;
    syncbuf_type* rdbuf() const noexcept { return const_cast<syncbuf_type*>(addressof(sb)); }

  private:
    syncbuf_type sb;    // exposition only
  };
}
```

`Allocator` shall meet the *Cpp17Allocator* requirements
[[allocator.requirements.general]].

[*Example 1*:

A named variable can be used within a block statement for streaming.

``` cpp
{
  osyncstream bout(cout);
  bout << "Hello, ";
  bout << "World!";
  bout << endl; // flush is noted
  bout << "and more!\n";
}   // characters are transferred and cout is flushed
```

— *end example*]

[*Example 2*:

A temporary object can be used for streaming within a single statement.

``` cpp
osyncstream(cout) << "Hello, " << "World!" << '\n';
```

In this example, `cout` is not flushed.

— *end example*]

#### Construction and destruction <a id="syncstream.osyncstream.cons">[[syncstream.osyncstream.cons]]</a>

``` cpp
basic_osyncstream(streambuf_type* buf, const Allocator& allocator);
```

*Effects:* Initializes `sb` from `buf` and `allocator`. Initializes the
base class with `basic_ostream<charT, traits>(addressof(sb))`.

[*Note 1*: The member functions of the provided stream buffer can be
called from `emit()` while a lock is held, which might result in a
deadlock if used incautiously. — *end note*]

*Ensures:* `get_wrapped() == buf` is `true`.

``` cpp
basic_osyncstream(basic_osyncstream&& other) noexcept;
```

*Effects:* Move constructs the base class and `sb` from the
corresponding subobjects of `other`, and calls
`basic_ostream<charT, traits>::set_rdbuf(addressof(sb))`.

*Ensures:* The value returned by `get_wrapped()` is the value returned
by `other.get_wrapped()` prior to calling this constructor.
`nullptr == other.get_wrapped()` is `true`.

#### Member functions <a id="syncstream.osyncstream.members">[[syncstream.osyncstream.members]]</a>

``` cpp
void emit();
```

*Effects:* Behaves as an unformatted output
function [[ostream.unformatted]]. After constructing a `sentry` object,
calls `sb.emit()`. If that call returns `false`, calls
`setstate(ios_base::badbit)`.

[*Example 1*:

A flush on a `basic_osyncstream` does not flush immediately:

``` cpp
{
  osyncstream bout(cout);
  bout << "Hello," << '\n';     // no flush
  bout.emit();                  // characters transferred; cout not flushed
  bout << "World!" << endl;     // flush noted; cout not flushed
  bout.emit();                  // characters transferred; cout flushed
  bout << "Greetings." << '\n'; // no flush
}   // characters transferred; cout not flushed
```

— *end example*]

[*Example 2*:

The function `emit()` can be used to handle exceptions from operations
on the underlying stream.

``` cpp
{
  osyncstream bout(cout);
  bout << "Hello, " << "World!" << '\n';
  try {
    bout.emit();
  } catch (...) {
    // handle exception
  }
}
```

— *end example*]

``` cpp
streambuf_type* get_wrapped() const noexcept;
```

*Returns:* `sb.get_wrapped()`.

[*Example 3*:

Obtaining the wrapped stream buffer with `get_wrapped()` allows wrapping
it again with an `osyncstream`. For example,

``` cpp
{
  osyncstream bout1(cout);
  bout1 << "Hello, ";
  {
    osyncstream(bout1.get_wrapped()) << "Goodbye, " << "Planet!" << '\n';
  }
  bout1 << "World!" << '\n';
}
```

produces the *uninterleaved* output

``` text
Goodbye, Planet!
Hello, World!
```

— *end example*]

## File systems <a id="filesystems">[[filesystems]]</a>

### General <a id="fs.general">[[fs.general]]</a>

Subclause  [[filesystems]] describes operations on file systems and
their components, such as paths, regular files, and directories.

A *file system* is a collection of files and their attributes.

A *file* is an object within a file system that holds user or system
data. Files can be written to, or read from, or both. A file has certain
attributes, including type. File types include regular files and
directories. Other types of files, such as symbolic links, may be
supported by the implementation.

A *directory* is a file within a file system that acts as a container of
directory entries that contain information about other files, possibly
including other directory files. The *parent directory* of a directory
is the directory that both contains a directory entry for the given
directory and is represented by the dot-dot filename [[fs.path.generic]]
in the given directory. The *parent directory* of other types of files
is a directory containing a directory entry for the file under
discussion.

A *link* is an object that associates a filename with a file. Several
links can associate names with the same file. A *hard link* is a link to
an existing file. Some file systems support multiple hard links to a
file. If the last hard link to a file is removed, the file itself is
removed.

[*Note 1*: A hard link can be thought of as a shared-ownership smart
pointer to a file. — *end note*]

A *symbolic link* is a type of file with the property that when the file
is encountered during pathname resolution [[fs.class.path]], a string
stored by the file is used to modify the pathname resolution.

[*Note 2*: Symbolic links are often called symlinks. A symbolic link
can be thought of as a raw pointer to a file. If the file pointed to
does not exist, the symbolic link is said to be a “dangling” symbolic
link. — *end note*]

### Conformance <a id="fs.conformance">[[fs.conformance]]</a>

#### General <a id="fs.conformance.general">[[fs.conformance.general]]</a>

Conformance is specified in terms of behavior. Ideal behavior is not
always implementable, so the conformance subclauses take that into
account.

#### POSIX conformance <a id="fs.conform.9945">[[fs.conform.9945]]</a>

Some behavior is specified by reference to POSIX. How such behavior is
actually implemented is unspecified.

[*Note 1*: This constitutes an “as if” rule allowing implementations to
call native operating system or other APIs. — *end note*]

Implementations should provide such behavior as it is defined by POSIX.
Implementations shall document any behavior that differs from the
behavior defined by POSIX. Implementations that do not support exact
POSIX behavior should provide behavior as close to POSIX behavior as is
reasonable given the limitations of actual operating systems and file
systems. If an implementation cannot provide any reasonable behavior,
the implementation shall report an error as specified in 
[[fs.err.report]].

[*Note 2*: This allows users to rely on an exception being thrown or an
error code being set when an implementation cannot provide any
reasonable behavior. — *end note*]

Implementations are not required to provide behavior that is not
supported by a particular file system.

[*Example 1*: The FAT file system used by some memory cards, camera
memory, and floppy disks does not support hard links, symlinks, and many
other features of more capable file systems, so implementations are not
required to support those features on the FAT file system but instead
are required to report an error as described above. — *end example*]

#### Operating system dependent behavior conformance <a id="fs.conform.os">[[fs.conform.os]]</a>

Behavior that is specified as being *operating system dependent* is
dependent upon the behavior and characteristics of an operating system.
The operating system an implementation is dependent upon is
*implementation-defined*.

It is permissible for an implementation to be dependent upon an
operating system emulator rather than the actual underlying operating
system.

#### File system race behavior <a id="fs.race.behavior">[[fs.race.behavior]]</a>

A *file system race* is the condition that occurs when multiple threads,
processes, or computers interleave access and modification of the same
object within a file system. Behavior is undefined if calls to functions
provided by subclause  [[filesystems]] introduce a file system race.

If the possibility of a file system race would make it unreliable for a
program to test for a precondition before calling a function described
herein, *Preconditions:* is not specified for the function.

[*Note 1*: As a design practice, preconditions are not specified when
it is unreasonable for a program to detect them prior to calling the
function. — *end note*]

### Requirements <a id="fs.req">[[fs.req]]</a>

Throughout subclause  [[filesystems]], `char`, `wchar_t`, `char8_t`,
`char16_t`, and `char32_t` are collectively called *encoded character
types*.

Functions with template parameters named `EcharT` shall not participate
in overload resolution unless `EcharT` is one of the encoded character
types.

Template parameters named `InputIterator` shall meet the
*Cpp17InputIterator* requirements [[input.iterators]] and shall have a
value type that is one of the encoded character types.

[*Note 1*: Use of an encoded character type implies an associated
character set and encoding. Since `signed char` and `unsigned char` have
no implied character set and encoding, they are not included as
permitted types. — *end note*]

Template parameters named `Allocator` shall meet the *Cpp17Allocator*
requirements [[allocator.requirements.general]].

### Header `<filesystem>` synopsis <a id="fs.filesystem.syn">[[fs.filesystem.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std::filesystem {
  // [fs.class.path], paths
  class path;

  // [fs.path.nonmember], path non-member functions
  void swap(path& lhs, path& rhs) noexcept;
  size_t hash_value(const path& p) noexcept;

  // [fs.class.filesystem.error], filesystem errors
  class filesystem_error;

  // [fs.class.directory.entry], directory entries
  class directory_entry;

  // [fs.class.directory.iterator], directory iterators
  class directory_iterator;

  // [fs.dir.itr.nonmembers], range access for directory iterators
  directory_iterator begin(directory_iterator iter) noexcept;
  directory_iterator end(directory_iterator) noexcept;

  // [fs.class.rec.dir.itr], recursive directory iterators
  class recursive_directory_iterator;

  // [fs.rec.dir.itr.nonmembers], range access for recursive directory iterators
  recursive_directory_iterator begin(recursive_directory_iterator iter) noexcept;
  recursive_directory_iterator end(recursive_directory_iterator) noexcept;

  // [fs.class.file.status], file status
  class file_status;

  struct space_info {
    uintmax_t capacity;
    uintmax_t free;
    uintmax_t available;

    friend bool operator==(const space_info&, const space_info&) = default;
  };

  // [fs.enum], enumerations
  enum class file_type;
  enum class perms;
  enum class perm_options;
  enum class copy_options;
  enum class directory_options;

  using file_time_type = chrono::time_point<chrono::file_clock>;

  // [fs.op.funcs], filesystem operations
  path absolute(const path& p);
  path absolute(const path& p, error_code& ec);

  path canonical(const path& p);
  path canonical(const path& p, error_code& ec);

  void copy(const path& from, const path& to);
  void copy(const path& from, const path& to, error_code& ec);
  void copy(const path& from, const path& to, copy_options options);
  void copy(const path& from, const path& to, copy_options options,
            error_code& ec);

  bool copy_file(const path& from, const path& to);
  bool copy_file(const path& from, const path& to, error_code& ec);
  bool copy_file(const path& from, const path& to, copy_options option);
  bool copy_file(const path& from, const path& to, copy_options option,
                 error_code& ec);

  void copy_symlink(const path& existing_symlink, const path& new_symlink);
  void copy_symlink(const path& existing_symlink, const path& new_symlink,
                    error_code& ec) noexcept;

  bool create_directories(const path& p);
  bool create_directories(const path& p, error_code& ec);

  bool create_directory(const path& p);
  bool create_directory(const path& p, error_code& ec) noexcept;

  bool create_directory(const path& p, const path& attributes);
  bool create_directory(const path& p, const path& attributes,
                        error_code& ec) noexcept;

  void create_directory_symlink(const path& to, const path& new_symlink);
  void create_directory_symlink(const path& to, const path& new_symlink,
                                error_code& ec) noexcept;

  void create_hard_link(const path& to, const path& new_hard_link);
  void create_hard_link(const path& to, const path& new_hard_link,
                        error_code& ec) noexcept;

  void create_symlink(const path& to, const path& new_symlink);
  void create_symlink(const path& to, const path& new_symlink,
                      error_code& ec) noexcept;

  path current_path();
  path current_path(error_code& ec);
  void current_path(const path& p);
  void current_path(const path& p, error_code& ec) noexcept;

  bool equivalent(const path& p1, const path& p2);
  bool equivalent(const path& p1, const path& p2, error_code& ec) noexcept;

  bool exists(file_status s) noexcept;
  bool exists(const path& p);
  bool exists(const path& p, error_code& ec) noexcept;

  uintmax_t file_size(const path& p);
  uintmax_t file_size(const path& p, error_code& ec) noexcept;

  uintmax_t hard_link_count(const path& p);
  uintmax_t hard_link_count(const path& p, error_code& ec) noexcept;

  bool is_block_file(file_status s) noexcept;
  bool is_block_file(const path& p);
  bool is_block_file(const path& p, error_code& ec) noexcept;

  bool is_character_file(file_status s) noexcept;
  bool is_character_file(const path& p);
  bool is_character_file(const path& p, error_code& ec) noexcept;

  bool is_directory(file_status s) noexcept;
  bool is_directory(const path& p);
  bool is_directory(const path& p, error_code& ec) noexcept;

  bool is_empty(const path& p);
  bool is_empty(const path& p, error_code& ec);

  bool is_fifo(file_status s) noexcept;
  bool is_fifo(const path& p);
  bool is_fifo(const path& p, error_code& ec) noexcept;

  bool is_other(file_status s) noexcept;
  bool is_other(const path& p);
  bool is_other(const path& p, error_code& ec) noexcept;

  bool is_regular_file(file_status s) noexcept;
  bool is_regular_file(const path& p);
  bool is_regular_file(const path& p, error_code& ec) noexcept;

  bool is_socket(file_status s) noexcept;
  bool is_socket(const path& p);
  bool is_socket(const path& p, error_code& ec) noexcept;

  bool is_symlink(file_status s) noexcept;
  bool is_symlink(const path& p);
  bool is_symlink(const path& p, error_code& ec) noexcept;

  file_time_type last_write_time(const path& p);
  file_time_type last_write_time(const path& p, error_code& ec) noexcept;
  void last_write_time(const path& p, file_time_type new_time);
  void last_write_time(const path& p, file_time_type new_time,
                       error_code& ec) noexcept;

  void permissions(const path& p, perms prms, perm_options opts=perm_options::replace);
  void permissions(const path& p, perms prms, error_code& ec) noexcept;
  void permissions(const path& p, perms prms, perm_options opts, error_code& ec);

  path proximate(const path& p, error_code& ec);
  path proximate(const path& p, const path& base = current_path());
  path proximate(const path& p, const path& base, error_code& ec);

  path read_symlink(const path& p);
  path read_symlink(const path& p, error_code& ec);

  path relative(const path& p, error_code& ec);
  path relative(const path& p, const path& base = current_path());
  path relative(const path& p, const path& base, error_code& ec);

  bool remove(const path& p);
  bool remove(const path& p, error_code& ec) noexcept;

  uintmax_t remove_all(const path& p);
  uintmax_t remove_all(const path& p, error_code& ec);

  void rename(const path& from, const path& to);
  void rename(const path& from, const path& to, error_code& ec) noexcept;

  void resize_file(const path& p, uintmax_t size);
  void resize_file(const path& p, uintmax_t size, error_code& ec) noexcept;

  space_info space(const path& p);
  space_info space(const path& p, error_code& ec) noexcept;

  file_status status(const path& p);
  file_status status(const path& p, error_code& ec) noexcept;

  bool status_known(file_status s) noexcept;

  file_status symlink_status(const path& p);
  file_status symlink_status(const path& p, error_code& ec) noexcept;

  path temp_directory_path();
  path temp_directory_path(error_code& ec);

  path weakly_canonical(const path& p);
  path weakly_canonical(const path& p, error_code& ec);
}

// [fs.path.hash], hash support
namespace std {
  template<class T> struct hash;
  template<> struct hash<filesystem::path>;
}

namespace std::ranges {
  template<>
    inline constexpr bool enable_borrowed_range<filesystem::directory_iterator> = true;
  template<>
    inline constexpr bool enable_borrowed_range<filesystem::recursive_directory_iterator> = true;

  template<>
    inline constexpr bool enable_view<filesystem::directory_iterator> = true;
  template<>
    inline constexpr bool enable_view<filesystem::recursive_directory_iterator> = true;
}
```

Implementations should ensure that the resolution and range of
`file_time_type` reflect the operating system dependent resolution and
range of file time values.

### Error reporting <a id="fs.err.report">[[fs.err.report]]</a>

Filesystem library functions often provide two overloads, one that
throws an exception to report file system errors, and another that sets
an `error_code`.

[*Note 1*:

This supports two common use cases:

- Uses where file system errors are truly exceptional and indicate a
  serious failure. Throwing an exception is an appropriate response.
- Uses where file system errors are routine and do not necessarily
  represent failure. Returning an error code is the most appropriate
  response. This allows application specific error handling, including
  simply ignoring the error.

— *end note*]

Functions not having an argument of type `error_code&` handle errors as
follows, unless otherwise specified:

- When a call by the implementation to an operating system or other
  underlying API results in an error that prevents the function from
  meeting its specifications, an exception of type `filesystem_error`
  shall be thrown. For functions with a single path argument, that
  argument shall be passed to the `filesystem_error` constructor with a
  single path argument. For functions with two path arguments, the first
  of these arguments shall be passed to the `filesystem_error`
  constructor as the `path1` argument, and the second shall be passed as
  the `path2` argument. The `filesystem_error` constructor’s
  `error_code` argument is set as appropriate for the specific operating
  system dependent error.
- Failure to allocate storage is reported by throwing an exception as
  described in  [[res.on.exception.handling]].
- Destructors throw nothing.

Functions having an argument of type `error_code&` handle errors as
follows, unless otherwise specified:

- If a call by the implementation to an operating system or other
  underlying API results in an error that prevents the function from
  meeting its specifications, the `error_code&` argument is set as
  appropriate for the specific operating system dependent error.
  Otherwise, `clear()` is called on the `error_code&` argument.

### Class `path` <a id="fs.class.path">[[fs.class.path]]</a>

#### General <a id="fs.class.path.general">[[fs.class.path.general]]</a>

An object of class `path` represents a path and contains a pathname.
Such an object is concerned only with the lexical and syntactic aspects
of a path. The path does not necessarily exist in external storage, and
the pathname is not necessarily valid for the current operating system
or for a particular file system.

[*Note 1*: Class `path` is used to support the differences between the
string types used by different operating systems to represent pathnames,
and to perform conversions between encodings when
necessary. — *end note*]

A *path* is a sequence of elements that identify the location of a file
within a filesystem. The elements are the *root-name*ₒₚₜ ,
*root-directory*ₒₚₜ , and an optional sequence of *filename*s
[[fs.path.generic]]. The maximum number of elements in the sequence is
operating system dependent [[fs.conform.os]].

An *absolute path* is a path that unambiguously identifies the location
of a file without reference to an additional starting location. The
elements of a path that determine if it is absolute are operating system
dependent. A *relative path* is a path that is not absolute, and as
such, only unambiguously identifies the location of a file when resolved
relative to an implied starting location. The elements of a path that
determine if it is relative are operating system dependent.

[*Note 2*: Pathnames “.” and “..” are relative paths. — *end note*]

A *pathname* is a character string that represents the name of a path.
Pathnames are formatted according to the generic pathname format grammar
[[fs.path.generic]] or according to an operating system dependent
*native pathname format* accepted by the host operating system.

*Pathname resolution* is the operating system dependent mechanism for
resolving a pathname to a particular file in a file hierarchy. There may
be multiple pathnames that resolve to the same file.

[*Example 1*: POSIX specifies the mechanism in section 4.12, Pathname
resolution. — *end example*]

``` cpp
namespace std::filesystem {
  class path {
  public:
    using value_type  = see below;
    using string_type = basic_string<value_type>;
    static constexpr value_type preferred_separator = see below;

    // [fs.enum.path.format], enumeration format
    enum format;

    // [fs.path.construct], constructors and destructor
    path() noexcept;
    path(const path& p);
    path(path&& p) noexcept;
    path(string_type&& source, format fmt = auto_format);
    template<class Source>
      path(const Source& source, format fmt = auto_format);
    template<class InputIterator>
      path(InputIterator first, InputIterator last, format fmt = auto_format);
    template<class Source>
      path(const Source& source, const locale& loc, format fmt = auto_format);
    template<class InputIterator>
      path(InputIterator first, InputIterator last, const locale& loc, format fmt = auto_format);
    ~path();

    // [fs.path.assign], assignments
    path& operator=(const path& p);
    path& operator=(path&& p) noexcept;
    path& operator=(string_type&& source);
    path& assign(string_type&& source);
    template<class Source>
      path& operator=(const Source& source);
    template<class Source>
      path& assign(const Source& source);
    template<class InputIterator>
      path& assign(InputIterator first, InputIterator last);

    // [fs.path.append], appends
    path& operator/=(const path& p);
    template<class Source>
      path& operator/=(const Source& source);
    template<class Source>
      path& append(const Source& source);
    template<class InputIterator>
      path& append(InputIterator first, InputIterator last);

    // [fs.path.concat], concatenation
    path& operator+=(const path& x);
    path& operator+=(const string_type& x);
    path& operator+=(basic_string_view<value_type> x);
    path& operator+=(const value_type* x);
    path& operator+=(value_type x);
    template<class Source>
      path& operator+=(const Source& x);
    template<class EcharT>
      path& operator+=(EcharT x);
    template<class Source>
      path& concat(const Source& x);
    template<class InputIterator>
      path& concat(InputIterator first, InputIterator last);

    // [fs.path.modifiers], modifiers
    void  clear() noexcept;
    path& make_preferred();
    path& remove_filename();
    path& replace_filename(const path& replacement);
    path& replace_extension(const path& replacement = path());
    void  swap(path& rhs) noexcept;

    // [fs.path.nonmember], non-member operators
    friend bool operator==(const path& lhs, const path& rhs) noexcept;
    friend strong_ordering operator<=>(const path& lhs, const path& rhs) noexcept;

    friend path operator/(const path& lhs, const path& rhs);

    // [fs.path.native.obs], native format observers
    const string_type& native() const noexcept;
    const value_type*  c_str() const noexcept;
    operator string_type() const;

    template<class EcharT, class traits = char_traits<EcharT>,
             class Allocator = allocator<EcharT>>
      basic_string<EcharT, traits, Allocator>
        string(const Allocator& a = Allocator()) const;
    std::string    string() const;
    std::wstring   wstring() const;
    std::u8string  u8string() const;
    std::u16string u16string() const;
    std::u32string u32string() const;

    // [fs.path.generic.obs], generic format observers
    template<class EcharT, class traits = char_traits<EcharT>,
             class Allocator = allocator<EcharT>>
      basic_string<EcharT, traits, Allocator>
        generic_string(const Allocator& a = Allocator()) const;
    std::string    generic_string() const;
    std::wstring   generic_wstring() const;
    std::u8string  generic_u8string() const;
    std::u16string generic_u16string() const;
    std::u32string generic_u32string() const;

    // [fs.path.compare], compare
    int compare(const path& p) const noexcept;
    int compare(const string_type& s) const;
    int compare(basic_string_view<value_type> s) const;
    int compare(const value_type* s) const;

    // [fs.path.decompose], decomposition
    path root_name() const;
    path root_directory() const;
    path root_path() const;
    path relative_path() const;
    path parent_path() const;
    path filename() const;
    path stem() const;
    path extension() const;

    // [fs.path.query], query
    [[nodiscard]] bool empty() const noexcept;
    bool has_root_name() const;
    bool has_root_directory() const;
    bool has_root_path() const;
    bool has_relative_path() const;
    bool has_parent_path() const;
    bool has_filename() const;
    bool has_stem() const;
    bool has_extension() const;
    bool is_absolute() const;
    bool is_relative() const;

    // [fs.path.gen], generation
    path lexically_normal() const;
    path lexically_relative(const path& base) const;
    path lexically_proximate(const path& base) const;

    // [fs.path.itr], iterators
    class iterator;
    using const_iterator = iterator;

    iterator begin() const;
    iterator end() const;

    // [fs.path.io], path inserter and extractor
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const path& p);
    template<class charT, class traits>
      friend basic_istream<charT, traits>&
        operator>>(basic_istream<charT, traits>& is, path& p);
  };
}
```

`value_type` is a `typedef` for the operating system dependent encoded
character type used to represent pathnames.

The value of the `preferred_separator` member is the operating system
dependent *preferred-separator* character [[fs.path.generic]].

[*Example 2*: For POSIX-based operating systems, `value_type` is `char`
and `preferred_separator` is the slash character (`'/'`). For
Windows-based operating systems, `value_type` is `wchar_t` and
`preferred_separator` is the backslash character
(`L'\\'`). — *end example*]

#### Generic pathname format <a id="fs.path.generic">[[fs.path.generic]]</a>

``` bnf
pathname:
    root-nameₒₚₜ root-directoryₒₚₜ relative-path
```

``` bnf
root-name:
    operating system dependent sequences of characters
    implementation-defined sequences of characters
```

``` bnf
root-directory:
    directory-separator
```

``` bnf
relative-path:
    filename
    filename directory-separator relative-path
    an empty path
```

``` bnf
filename:
    non-empty sequence of characters other than *directory-separator* characters
```

``` bnf
directory-separator:
    preferred-separator directory-separatorₒₚₜ 
    fallback-separator directory-separatorₒₚₜ
```

``` bnf
preferred-separator:
    operating system dependent directory separator character
```

``` bnf
fallback-separator:
    /, if *preferred-separator* is not /
```

A *filename* is the name of a file. The *dot* and *dot-dot* filenames,
consisting solely of one and two period characters respectively, have
special meaning. The following characteristics of filenames are
operating system dependent:

- The permitted characters. \[*Example 1*: Some operating systems
  prohibit the ASCII control characters (0x00 – 0x1F) in
  filenames. — *end example*] \[*Note 1*: Wider portability can be
  achieved by limiting *filename* characters to the POSIX Portable
  Filename Character Set:  
  `A B C D E F G H I J K L M N O P Q R S T U V W X Y Z`  
  `a b c d e f g h i j k l m n o p q r s t u v w x y z`  
  `0 1 2 3 4 5 6 7 8 9 . _ -` — *end note*]
- The maximum permitted length.
- Filenames that are not permitted.
- Filenames that have special meaning.
- Case awareness and sensitivity during path resolution.
- Special rules that may apply to file types other than regular files,
  such as directories.

Except in a *root-name*, multiple successive *directory-separator*
characters are considered to be the same as one *directory-separator*
character.

The dot filename is treated as a reference to the current directory. The
dot-dot filename is treated as a reference to the parent directory. What
the dot-dot filename refers to relative to *root-directory* is
*implementation-defined*. Specific filenames may have special meanings
for a particular operating system.

A *root-name* identifies the starting location for pathname resolution
[[fs.class.path]]. If there are no operating system dependent
*root-name*s, at least one *implementation-defined* *root-name* is
required.

[*Note 2*: Many operating systems define a name beginning with two
*directory-separator* characters as a *root-name* that identifies
network or other resource locations. Some operating systems define a
single letter followed by a colon as a drive specifier — a *root-name*
identifying a specific device such as a disk drive. — *end note*]

If a *root-name* is otherwise ambiguous, the possibility with the
longest sequence of characters is chosen.

[*Note 3*: On a POSIX-like operating system, it is impossible to have a
*root-name* and a *relative-path* without an intervening
*root-directory* element. — *end note*]

*Normalization* of a generic format pathname means:

1.  If the path is empty, stop.
2.  Replace each slash character in the *root-name* with a
    *preferred-separator*.
3.  Replace each *directory-separator* with a *preferred-separator*.
    \[*Note 4*: The generic pathname grammar defines
    *directory-separator* as one or more slashes and
    *preferred-separator*s. — *end note*]
4.  Remove each dot filename and any immediately following
    *directory-separator*.
5.  As long as any appear, remove a non-dot-dot filename immediately
    followed by a *directory-separator* and a dot-dot filename, along
    with any immediately following *directory-separator*.
6.  If there is a *root-directory*, remove all dot-dot filenames and any
    *directory-separator*s immediately following them. \[*Note 5*: These
    dot-dot filenames attempt to refer to nonexistent parent
    directories. — *end note*]
7.  If the last filename is dot-dot, remove any trailing
    *directory-separator*.
8.  If the path is empty, add a dot.

The result of normalization is a path in *normal form*, which is said to
be *normalized*.

#### Conversions <a id="fs.path.cvt">[[fs.path.cvt]]</a>

##### Argument format conversions <a id="fs.path.fmt.cvt">[[fs.path.fmt.cvt]]</a>

[*Note 1*:

The format conversions described in this subclause are not applied on
POSIX-based operating systems because on these systems:

- The generic format is acceptable as a native path.
- There is no need to distinguish between native format and generic
  format in function arguments.
- Paths for regular files and paths for directories share the same
  syntax.

— *end note*]

Several functions are defined to accept *detected-format* arguments,
which are character sequences. A detected-format argument represents a
path using either a pathname in the generic format [[fs.path.generic]]
or a pathname in the native format [[fs.class.path]]. Such an argument
is taken to be in the generic format if and only if it matches the
generic format and is not acceptable to the operating system as a native
path.

[*Note 2*: Some operating systems have no unambiguous way to
distinguish between native format and generic format arguments. This is
by design as it simplifies use for operating systems that do not require
disambiguation. An implementation for an operating system where
disambiguation is required is permitted to distinguish between the
formats. — *end note*]

Pathnames are converted as needed between the generic and native formats
in an operating-system-dependent manner. Let *G(n)* and *N(g)* in a
mathematical sense be the implementation’s functions that convert
native-to-generic and generic-to-native formats respectively. If
*g=G(n)* for some *n*, then *G(N(g))=g*; if *n=N(g)* for some *g*, then
*N(G(n))=n*.

[*Note 3*: Neither *G* nor *N* need be invertible. — *end note*]

If the native format requires paths for regular files to be formatted
differently from paths for directories, the path shall be treated as a
directory path if its last element is a *directory-separator*, otherwise
it shall be treated as a path to a regular file.

[*Note 4*: A path stores a native format pathname
[[fs.path.native.obs]] and acts as if it also stores a generic format
pathname, related as given below. The implementation can generate the
generic format pathname based on the native format pathname (and
possibly other information) when requested. — *end note*]

When a path is constructed from or is assigned a single representation
separate from any path, the other representation is selected by the
appropriate conversion function (*G* or *N*).

When the (new) value *p* of one representation of a path is derived from
the representation of that or another path, a value *q* is chosen for
the other representation. The value *q* converts to *p* (by *G* or *N*
as appropriate) if any such value does so; *q* is otherwise unspecified.

[*Note 5*: If *q* is the result of converting any path at all, it is
the result of converting *p*. — *end note*]

##### Type and encoding conversions <a id="fs.path.type.cvt">[[fs.path.type.cvt]]</a>

The *native encoding* of an ordinary character string is the operating
system dependent current encoding for pathnames [[fs.class.path]]. The
*native encoding* for wide character strings is the
implementation-defined execution wide-character set encoding
[[character.seq]].

For member function arguments that take character sequences representing
paths and for member functions returning strings, value type and
encoding conversion is performed if the value type of the argument or
return value differs from `path::value_type`. For the argument or return
value, the method of conversion and the encoding to be converted to is
determined by its value type:

- `char`: The encoding is the native ordinary encoding. The method of
  conversion, if any, is operating system dependent. \[*Note 6*: For
  POSIX-based operating systems `path::value_type` is `char` so no
  conversion from `char` value type arguments or to `char` value type
  return values is performed. For Windows-based operating systems, the
  native ordinary encoding is determined by calling a Windows API
  function. — *end note*] \[*Note 7*: This results in behavior
  identical to other C and C++ standard library functions that perform
  file operations using ordinary character strings to identify paths.
  Changing this behavior would be surprising and
  error-prone. — *end note*]
- `wchar_t`: The encoding is the native wide encoding. The method of
  conversion is unspecified. \[*Note 8*: For Windows-based operating
  systems `path::value_type` is `wchar_t` so no conversion from
  `wchar_t` value type arguments or to `wchar_t` value type return
  values is performed. — *end note*]
- `char8_t`: The encoding is UTF-8. The method of conversion is
  unspecified.
- `char16_t`: The encoding is UTF-16. The method of conversion is
  unspecified.
- `char32_t`: The encoding is UTF-32. The method of conversion is
  unspecified.

If the encoding being converted to has no representation for source
characters, the resulting converted characters, if any, are unspecified.
Implementations should not modify member function arguments if already
of type `path::value_type`.

#### Requirements <a id="fs.path.req">[[fs.path.req]]</a>

In addition to the requirements [[fs.req]], function template parameters
named `Source` shall be one of:

- `basic_string<EcharT, traits, Allocator>`. A function argument
  `const Source&` `source` shall have an effective range
  \[`source.begin()`, `source.end()`).
- `basic_string_view<EcharT, traits>`. A function argument
  `const Source&` `source` shall have an effective range
  \[`source.begin()`, `source.end()`).
- A type meeting the *Cpp17InputIterator* requirements that iterates
  over a NTCTS. The value type shall be an encoded character type. A
  function argument `const Source&` `source` shall have an effective
  range \[`source`, `end`) where `end` is the first iterator value with
  an element value equal to `iterator_traits<Source>::value_type()`.
- A character array that after array-to-pointer decay results in a
  pointer to the start of a NTCTS. The value type shall be an encoded
  character type. A function argument `const Source&` `source` shall
  have an effective range \[`source`, `end`) where `end` is the first
  iterator value with an element value equal to
  `iterator_traits<decay_t<Source>>::value_type()`.

Functions taking template parameters named `Source` shall not
participate in overload resolution unless `Source` denotes a type other
than `path`, and either

- `Source` is a specialization of `basic_string` or `basic_string_view`,
  or
- the *qualified-id* `iterator_traits<decay_t<Source>>::value_type` is
  valid and denotes a possibly const encoded character type
  [[temp.deduct]].

[*Note 1*: See path conversions [[fs.path.cvt]] for how the value types
above and their encodings convert to `path::value_type` and its
encoding. — *end note*]

Arguments of type `Source` shall not be null pointers.

#### Members <a id="fs.path.member">[[fs.path.member]]</a>

##### Constructors <a id="fs.path.construct">[[fs.path.construct]]</a>

``` cpp
path() noexcept;
```

*Ensures:* `empty() == true`.

``` cpp
path(const path& p);
path(path&& p) noexcept;
```

*Effects:* Constructs an object of class `path` having the same pathname
in the native and generic formats, respectively, as the original value
of `p`. In the second form, `p` is left in a valid but unspecified
state.

``` cpp
path(string_type&& source, format fmt = auto_format);
```

*Effects:* Constructs an object of class `path` for which the pathname
in the detected-format of `source` has the original value of
`source`[[fs.path.fmt.cvt]], converting format if
required [[fs.path.fmt.cvt]]. `source` is left in a valid but
unspecified state.

``` cpp
template<class Source>
  path(const Source& source, format fmt = auto_format);
template<class InputIterator>
  path(InputIterator first, InputIterator last, format fmt = auto_format);
```

*Effects:* Let `s` be the effective range of `source`[[fs.path.req]] or
the range \[`first`, `last`), with the encoding converted if
required [[fs.path.cvt]]. Finds the detected-format of
`s`[[fs.path.fmt.cvt]] and constructs an object of class `path` for
which the pathname in that format is `s`.

``` cpp
template<class Source>
  path(const Source& source, const locale& loc, format fmt = auto_format);
template<class InputIterator>
  path(InputIterator first, InputIterator last, const locale& loc, format fmt = auto_format);
```

*Mandates:* The value type of `Source` and `InputIterator` is `char`.

*Effects:* Let `s` be the effective range of `source` or the range
\[`first`, `last`), after converting the encoding as follows:

- If `value_type` is `wchar_t`, converts to the native wide
  encoding [[fs.path.type.cvt]] using the
  `codecvt<wchar_t, char, mbstate_t>` facet of `loc`.
- Otherwise a conversion is performed using the
  `codecvt<wchar_t, char, mbstate_t>` facet of `loc`, and then a second
  conversion to the current ordinary encoding.

Finds the detected-format of `s`[[fs.path.fmt.cvt]] and constructs an
object of class `path` for which the pathname in that format is `s`.

[*Example 1*:

A string is to be read from a database that is encoded in ISO/IEC
8859-1, and used to create a directory:

``` cpp
namespace fs = std::filesystem;
std::string latin1_string = read_latin1_data();
codecvt_8859_1<wchar_t> latin1_facet;
std::locale latin1_locale(std::locale(), latin1_facet);
fs::create_directory(fs::path(latin1_string, latin1_locale));
```

For POSIX-based operating systems, the path is constructed by first
using `latin1_facet` to convert ISO/IEC 8859-1 encoded `latin1_string`
to a wide character string in the native wide
encoding [[fs.path.type.cvt]]. The resulting wide string is then
converted to an ordinary character pathname string in the current native
ordinary encoding. If the native wide encoding is UTF-16 or UTF-32, and
the current native ordinary encoding is UTF-8, all of the characters in
the ISO/IEC 8859-1 character set will be converted to their Unicode
representation, but for other native ordinary encodings some characters
may have no representation.

For Windows-based operating systems, the path is constructed by using
`latin1_facet` to convert ISO/IEC 8859-1 encoded `latin1_string` to a
UTF-16 encoded wide character pathname string. All of the characters in
the ISO/IEC 8859-1 character set will be converted to their Unicode
representation.

— *end example*]

##### Assignments <a id="fs.path.assign">[[fs.path.assign]]</a>

``` cpp
path& operator=(const path& p);
```

*Effects:* If `*this` and `p` are the same object, has no effect.
Otherwise, sets both respective pathnames of `*this` to the respective
pathnames of `p`.

*Returns:* `*this`.

``` cpp
path& operator=(path&& p) noexcept;
```

*Effects:* If `*this` and `p` are the same object, has no effect.
Otherwise, sets both respective pathnames of `*this` to the respective
pathnames of `p`. `p` is left in a valid but unspecified state.

[*Note 1*: A valid implementation is `swap(p)`. — *end note*]

*Returns:* `*this`.

``` cpp
path& operator=(string_type&& source);
path& assign(string_type&& source);
```

*Effects:* Sets the pathname in the detected-format of `source` to the
original value of `source`. `source` is left in a valid but unspecified
state.

*Returns:* `*this`.

``` cpp
template<class Source>
  path& operator=(const Source& source);
template<class Source>
  path& assign(const Source& source);
template<class InputIterator>
  path& assign(InputIterator first, InputIterator last);
```

*Effects:* Let `s` be the effective range of `source`[[fs.path.req]] or
the range \[`first`, `last`), with the encoding converted if
required [[fs.path.cvt]]. Finds the detected-format of
`s`[[fs.path.fmt.cvt]] and sets the pathname in that format to `s`.

*Returns:* `*this`.

##### Appends <a id="fs.path.append">[[fs.path.append]]</a>

The append operations use `operator/=` to denote their semantic effect
of appending *preferred-separator* when needed.

``` cpp
path& operator/=(const path& p);
```

*Effects:* If
`p.is_absolute() || (p.has_root_name() && p.root_name() != root_name())`,
then `operator=(p)`.

Otherwise, modifies `*this` as if by these steps:

- If `p.has_root_directory()`, then removes any root directory and
  relative path from the generic format pathname. Otherwise, if
  `!has_root_directory() && is_absolute()` is `true` or if
  `has_filename()` is `true`, then appends `path::preferred_separator`
  to the generic format pathname.
- Then appends the native format pathname of `p`, omitting any
  *root-name* from its generic format pathname, to the native format
  pathname.

[*Example 2*:

Even if `//host` is interpreted as a *root-name*, both of the paths
`path("//host")/"foo"` and `path("//host/")/"foo"` equal `"//host/foo"`
(although the former might use backslash as the preferred separator).

Expression examples:

``` cpp
// On POSIX,
path("foo") /= path("");        // yields path("foo/")
path("foo") /= path("/bar");    // yields path("/bar")

// On Windows,
path("foo") /= path("");        // yields path("foo\{")}
path("foo") /= path("/bar");    // yields path("/bar")
path("foo") /= path("c:/bar");  // yields path("c:/bar")
path("foo") /= path("c:");      // yields path("c:")
path("c:") /= path("");         // yields path("c:")
path("c:foo") /= path("/bar");  // yields path("c:/bar")
path("c:foo") /= path("c:bar"); // yields path("c:foo\{bar")}
```

— *end example*]

*Returns:* `*this`.

``` cpp
template<class Source>
  path& operator/=(const Source& source);
template<class Source>
  path& append(const Source& source);
```

*Effects:* Equivalent to: `return operator/=(path(source));`

``` cpp
template<class InputIterator>
  path& append(InputIterator first, InputIterator last);
```

*Effects:* Equivalent to: `return operator/=(path(first, last));`

##### Concatenation <a id="fs.path.concat">[[fs.path.concat]]</a>

``` cpp
path& operator+=(const path& x);
path& operator+=(const string_type& x);
path& operator+=(basic_string_view<value_type> x);
path& operator+=(const value_type* x);
template<class Source>
  path& operator+=(const Source& x);
template<class Source>
  path& concat(const Source& x);
```

*Effects:* Appends `path(x).native()` to the pathname in the native
format.

[*Note 2*: This directly manipulates the value of `native()`, which is
not necessarily portable between operating systems. — *end note*]

*Returns:* `*this`.

``` cpp
path& operator+=(value_type x);
template<class EcharT>
  path& operator+=(EcharT x);
```

*Effects:* Equivalent to: `return *this += basic_string_view(&x, 1);`

``` cpp
template<class InputIterator>
  path& concat(InputIterator first, InputIterator last);
```

*Effects:* Equivalent to: `return *this += path(first, last);`

##### Modifiers <a id="fs.path.modifiers">[[fs.path.modifiers]]</a>

``` cpp
void clear() noexcept;
```

*Ensures:* `empty() == true`.

``` cpp
path& make_preferred();
```

*Effects:* Each *directory-separator* of the pathname in the generic
format is converted to *preferred-separator*.

*Returns:* `*this`.

[*Example 3*:

``` cpp
path p("foo/bar");
std::cout << p << '\n';
p.make_preferred();
std::cout << p << '\n';
```

On an operating system where *preferred-separator* is a slash, the
output is:

``` cpp
"foo/bar"
"foo/bar"
```

On an operating system where *preferred-separator* is a backslash, the
output is:

``` cpp
"foo/bar"
"foo\bar"
```

— *end example*]

``` cpp
path& remove_filename();
```

*Effects:* Remove the generic format pathname of `filename()` from the
generic format pathname.

*Ensures:* `!has_filename()`.

*Returns:* `*this`.

[*Example 4*:

``` cpp
path("foo/bar").remove_filename();      // yields "foo/"
path("foo/").remove_filename();         // yields "foo/"
path("/foo").remove_filename();         // yields "/"
path("/").remove_filename();            // yields "/"
```

— *end example*]

``` cpp
path& replace_filename(const path& replacement);
```

*Effects:* Equivalent to:

``` cpp
remove_filename();
operator/=(replacement);
```

*Returns:* `*this`.

[*Example 5*:

``` cpp
path("/foo").replace_filename("bar");   // yields "/bar" on POSIX
path("/").replace_filename("bar");      // yields "/bar" on POSIX
```

— *end example*]

``` cpp
path& replace_extension(const path& replacement = path());
```

*Effects:*

- Any existing `extension()`[[fs.path.decompose]] is removed from the
  pathname in the generic format, then
- If `replacement` is not empty and does not begin with a dot character,
  a dot character is appended to the pathname in the generic format,
  then
- `operator+=(replacement);`.

*Returns:* `*this`.

``` cpp
void swap(path& rhs) noexcept;
```

*Effects:* Swaps the contents (in all formats) of the two paths.

*Complexity:* Constant time.

##### Native format observers <a id="fs.path.native.obs">[[fs.path.native.obs]]</a>

The string returned by all native format observers is in the native
pathname format [[fs.class.path]].

``` cpp
const string_type& native() const noexcept;
```

*Returns:* The pathname in the native format.

``` cpp
const value_type* c_str() const noexcept;
```

*Effects:* Equivalent to: `return native().c_str();`

``` cpp
operator string_type() const;
```

*Returns:* `native()`.

``` cpp
template<class EcharT, class traits = char_traits<EcharT>,
         class Allocator = allocator<EcharT>>
  basic_string<EcharT, traits, Allocator>
    string(const Allocator& a = Allocator()) const;
```

*Returns:* `native()`.

*Remarks:* All memory allocation, including for the return value, shall
be performed by `a`. Conversion, if any, is specified by
[[fs.path.cvt]].

``` cpp
std::string string() const;
std::wstring wstring() const;
std::u8string u8string() const;
std::u16string u16string() const;
std::u32string u32string() const;
```

*Returns:* `native()`.

*Remarks:* Conversion, if any, is performed as specified by
[[fs.path.cvt]].

##### Generic format observers <a id="fs.path.generic.obs">[[fs.path.generic.obs]]</a>

Generic format observer functions return strings formatted according to
the generic pathname format [[fs.path.generic]]. A single slash (`'/'`)
character is used as the *directory-separator*.

[*Example 1*:

On an operating system that uses backslash as its *preferred-separator*,

``` cpp
path("foo\\bar").generic_string()
```

returns `"foo/bar"`.

— *end example*]

``` cpp
template<class EcharT, class traits = char_traits<EcharT>,
         class Allocator = allocator<EcharT>>
  basic_string<EcharT, traits, Allocator>
    generic_string(const Allocator& a = Allocator()) const;
```

*Returns:* The pathname in the generic format.

*Remarks:* All memory allocation, including for the return value, shall
be performed by `a`. Conversion, if any, is specified by
[[fs.path.cvt]].

``` cpp
std::string generic_string() const;
std::wstring generic_wstring() const;
std::u8string generic_u8string() const;
std::u16string generic_u16string() const;
std::u32string generic_u32string() const;
```

*Returns:* The pathname in the generic format.

*Remarks:* Conversion, if any, is specified by  [[fs.path.cvt]].

##### Compare <a id="fs.path.compare">[[fs.path.compare]]</a>

``` cpp
int compare(const path& p) const noexcept;
```

*Returns:*

- Let `rootNameComparison` be the result of
  `this->root_name().native().compare(p.root_name().native())`. If
  `rootNameComparison` is not `0`, `rootNameComparison`.
- Otherwise, if `!this->has_root_directory()` and
  `p.has_root_directory()`, a value less than `0`.
- Otherwise, if `this->has_root_directory()` and
  `!p.has_root_directory()`, a value greater than `0`.
- Otherwise, if `native()` for the elements of `this->relative_path()`
  are lexicographically less than `native()` for the elements of
  `p.relative_path()`, a value less than `0`.
- Otherwise, if `native()` for the elements of `this->relative_path()`
  are lexicographically greater than `native()` for the elements of
  `p.relative_path()`, a value greater than `0`.
- Otherwise, `0`.

``` cpp
int compare(const string_type& s) const;
int compare(basic_string_view<value_type> s) const;
int compare(const value_type* s) const;
```

*Effects:* Equivalent to: `return compare(path(s));`

##### Decomposition <a id="fs.path.decompose">[[fs.path.decompose]]</a>

``` cpp
path root_name() const;
```

*Returns:* *root-name*, if the pathname in the generic format includes
*root-name*, otherwise `path()`.

``` cpp
path root_directory() const;
```

*Returns:* *root-directory*, if the pathname in the generic format
includes *root-directory*, otherwise `path()`.

``` cpp
path root_path() const;
```

*Returns:* `root_name() / root_directory()`.

``` cpp
path relative_path() const;
```

*Returns:* A `path` composed from the pathname in the generic format, if
`empty()` is `false`, beginning with the first *filename* after
`root_path()`. Otherwise, `path()`.

``` cpp
path parent_path() const;
```

*Returns:* `*this` if `has_relative_path()` is `false`, otherwise a path
whose generic format pathname is the longest prefix of the generic
format pathname of `*this` that produces one fewer element in its
iteration.

``` cpp
path filename() const;
```

*Returns:* `relative_path().empty() ? path() : *–end()`.

[*Example 6*:

``` cpp
path("/foo/bar.txt").filename();        // yields "bar.txt"
path("/foo/bar").filename();            // yields "bar"
path("/foo/bar/").filename();           // yields ""
path("/").filename();                   // yields ""
path("//host").filename();              // yields ""
path(".").filename();                   // yields "."
path("..").filename();                  // yields ".."
```

— *end example*]

``` cpp
path stem() const;
```

*Returns:* Let `f` be the generic format pathname of `filename()`.
Returns a path whose pathname in the generic format is

- `f`, if it contains no periods other than a leading period or consists
  solely of one or two periods;
- otherwise, the prefix of `f` ending before its last period.

[*Example 7*:

``` cpp
std::cout << path("/foo/bar.txt").stem();       // outputs "bar"
path p = "foo.bar.baz.tar";
for (; !p.extension().empty(); p = p.stem())
  std::cout << p.extension() << '\n';
  // outputs: .tar
  //          .baz
  //          .bar
```

— *end example*]

``` cpp
path extension() const;
```

*Returns:* A path whose pathname in the generic format is the suffix of
`filename()` not included in `stem()`.

[*Example 8*:

``` cpp
path("/foo/bar.txt").extension();       // yields ".txt" and stem() is "bar"
path("/foo/bar").extension();           // yields "" and stem() is "bar"
path("/foo/.profile").extension();      // yields "" and stem() is ".profile"
path(".bar").extension();               // yields "" and stem() is ".bar"
path("..bar").extension();              // yields ".bar" and stem() is "."
```

— *end example*]

[*Note 3*: The period is included in the return value so that it is
possible to distinguish between no extension and an empty
extension. — *end note*]

[*Note 4*: On non-POSIX operating systems, for a path `p`, it is
possible that `p.stem() + p.extension() == p.filename()` is `false`,
even though the generic format pathnames are the same. — *end note*]

##### Query <a id="fs.path.query">[[fs.path.query]]</a>

``` cpp
[[nodiscard]] bool empty() const noexcept;
```

*Returns:* `true` if the pathname in the generic format is empty,
otherwise `false`.

``` cpp
bool has_root_path() const;
```

*Returns:* `!root_path().empty()`.

``` cpp
bool has_root_name() const;
```

*Returns:* `!root_name().empty()`.

``` cpp
bool has_root_directory() const;
```

*Returns:* `!root_directory().empty()`.

``` cpp
bool has_relative_path() const;
```

*Returns:* `!relative_path().empty()`.

``` cpp
bool has_parent_path() const;
```

*Returns:* `!parent_path().empty()`.

``` cpp
bool has_filename() const;
```

*Returns:* `!filename().empty()`.

``` cpp
bool has_stem() const;
```

*Returns:* `!stem().empty()`.

``` cpp
bool has_extension() const;
```

*Returns:* `!extension().empty()`.

``` cpp
bool is_absolute() const;
```

*Returns:* `true` if the pathname in the native format contains an
absolute path [[fs.class.path]], otherwise `false`.

[*Example 9*: `path("/").is_absolute()` is `true` for POSIX-based
operating systems, and `false` for Windows-based operating
systems. — *end example*]

``` cpp
bool is_relative() const;
```

*Returns:* `!is_absolute()`.

##### Generation <a id="fs.path.gen">[[fs.path.gen]]</a>

``` cpp
path lexically_normal() const;
```

*Returns:* A path whose pathname in the generic format is the normal
form [[fs.path.generic]] of the pathname in the generic format of
`*this`.

[*Example 10*:

``` cpp
assert(path("foo/./bar/..").lexically_normal() == "foo/");
assert(path("foo/.///bar/../").lexically_normal() == "foo/");
```

The above assertions will succeed. On Windows, the returned path’s
*directory-separator* characters will be backslashes rather than
slashes, but that does not affect `path` equality.

— *end example*]

``` cpp
path lexically_relative(const path& base) const;
```

*Effects:* If:

- `root_name() != base.root_name()` is `true`, or
- `is_absolute() != base.is_absolute()` is `true`, or
- `!has_root_directory() && base.has_root_directory()` is `true`, or
- any *filename* in `relative_path()` or `base.relative_path()` can be
  interpreted as a *root-name*,

returns `path()`.

[*Note 5*: On a POSIX implementation, no *filename* in a
*relative-path* is acceptable as a *root-name*. — *end note*]

Determines the first mismatched element of `*this` and `base` as if by:

``` cpp
auto [a, b] = mismatch(begin(), end(), base.begin(), base.end());
```

Then,

- if `a == end()` and `b == base.end()`, returns `path(".")`; otherwise
- let `n` be the number of *filename* elements in \[`b`, `base.end()`)
  that are not dot or dot-dot or empty, minus the number that are
  dot-dot. If `n<0,` returns `path()`; otherwise
- if `n == 0` and `(a == end() || a->empty())`, returns `path(".")`;
  otherwise
- returns an object of class `path` that is default-constructed,
  followed by
  - application of `operator/=(path(".."))` `n` times, and then
  - application of `operator/=` for each element in \[`a`, `end()`).

*Returns:* `*this` made relative to `base`. Does not
resolve [[fs.class.path]] symlinks. Does not first
normalize [[fs.path.generic]] `*this` or `base`.

[*Example 11*:

``` cpp
assert(path("/a/d").lexically_relative("/a/b/c") == "../../d");
assert(path("/a/b/c").lexically_relative("/a/d") == "../b/c");
assert(path("a/b/c").lexically_relative("a") == "b/c");
assert(path("a/b/c").lexically_relative("a/b/c/x/y") == "../..");
assert(path("a/b/c").lexically_relative("a/b/c") == ".");
assert(path("a/b").lexically_relative("c/d") == "../../a/b");
```

The above assertions will succeed. On Windows, the returned path’s
*directory-separator* characters will be backslashes rather than
slashes, but that does not affect `path` equality.

— *end example*]

[*Note 6*: If symlink following semantics are desired, use the
operational function `relative()`. — *end note*]

[*Note 7*: If normalization [[fs.path.generic]] is needed to ensure
consistent matching of elements, apply `lexically_normal()` to `*this`,
`base`, or both. — *end note*]

``` cpp
path lexically_proximate(const path& base) const;
```

*Returns:* If the value of `lexically_relative(base)` is not an empty
path, return it. Otherwise return `*this`.

[*Note 8*: If symlink following semantics are desired, use the
operational function `proximate()`. — *end note*]

[*Note 9*: If normalization [[fs.path.generic]] is needed to ensure
consistent matching of elements, apply `lexically_normal()` to `*this`,
`base`, or both. — *end note*]

#### Iterators <a id="fs.path.itr">[[fs.path.itr]]</a>

Path iterators iterate over the elements of the pathname in the generic
format [[fs.path.generic]].

A `path::iterator` is a constant iterator meeting all the requirements
of a bidirectional iterator [[bidirectional.iterators]] except that, for
dereferenceable iterators `a` and `b` of type `path::iterator` with
`a == b`, there is no requirement that `*a` and `*b` are bound to the
same object. Its `value_type` is `path`.

Calling any non-const member function of a `path` object invalidates all
iterators referring to elements of that object.

For the elements of the pathname in the generic format, the forward
traversal order is as follows:

- The *root-name* element, if present.
- The *root-directory* element, if present. \[*Note 1*: The generic
  format is required to ensure lexicographical comparison works
  correctly. — *end note*]
- Each successive *filename* element, if present.
- An empty element, if a trailing non-root *directory-separator* is
  present.

The backward traversal order is the reverse of forward traversal.

``` cpp
iterator begin() const;
```

*Returns:* An iterator for the first present element in the traversal
list above. If no elements are present, the end iterator.

``` cpp
iterator end() const;
```

*Returns:* The end iterator.

#### Inserter and extractor <a id="fs.path.io">[[fs.path.io]]</a>

``` cpp
template<class charT, class traits>
  friend basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const path& p);
```

*Effects:* Equivalent to `os << quoted(p.string<charT, traits>())`.

[*Note 1*: The `quoted` function is described
in  [[quoted.manip]]. — *end note*]

*Returns:* `os`.

``` cpp
template<class charT, class traits>
  friend basic_istream<charT, traits>&
    operator>>(basic_istream<charT, traits>& is, path& p);
```

*Effects:* Equivalent to:

``` cpp
basic_string<charT, traits> tmp;
is >> quoted(tmp);
p = tmp;
```

*Returns:* `is`.

#### Non-member functions <a id="fs.path.nonmember">[[fs.path.nonmember]]</a>

``` cpp
void swap(path& lhs, path& rhs) noexcept;
```

*Effects:* Equivalent to `lhs.swap(rhs)`.

``` cpp
size_t hash_value(const path& p) noexcept;
```

*Returns:* A hash value for the path `p`. If for two paths, `p1 == p2`
then `hash_value(p1) == hash_value(p2)`.

``` cpp
friend bool operator==(const path& lhs, const path& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) == 0`.

[*Note 1*:

Path equality and path equivalence have different semantics.

- Equality is determined by the `path` non-member `operator==`, which
  considers the two paths’ lexical representations only.
  \[*Example 1*: `path("foo") == "bar"` is never
  `true`. — *end example*]
- Equivalence is determined by the `equivalent()` non-member function,
  which determines if two paths resolve [[fs.class.path]] to the same
  file system entity. \[*Example 2*: `equivalent("foo", "bar")` will be
  `true` when both paths resolve to the same file. — *end example*]

— *end note*]

``` cpp
friend strong_ordering operator<=>(const path& lhs, const path& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) <=> 0`.

``` cpp
friend path operator/(const path& lhs, const path& rhs);
```

*Effects:* Equivalent to: `return path(lhs) /= rhs;`

#### Hash support <a id="fs.path.hash">[[fs.path.hash]]</a>

``` cpp
template<> struct hash<filesystem::path>;
```

For an object `p` of type `filesystem::path`,
`hash<filesystem::path>()(p)` evaluates to the same result as
`filesystem::hash_value(p)`.

### Class `filesystem_error` <a id="fs.class.filesystem.error">[[fs.class.filesystem.error]]</a>

#### General <a id="fs.class.filesystem.error.general">[[fs.class.filesystem.error.general]]</a>

``` cpp
namespace std::filesystem {
  class filesystem_error : public system_error {
  public:
    filesystem_error(const string& what_arg, error_code ec);
    filesystem_error(const string& what_arg,
                     const path& p1, error_code ec);
    filesystem_error(const string& what_arg,
                     const path& p1, const path& p2, error_code ec);

    const path& path1() const noexcept;
    const path& path2() const noexcept;
    const char* what() const noexcept override;
  };
}
```

The class `filesystem_error` defines the type of objects thrown as
exceptions to report file system errors from functions described in
subclause  [[filesystems]].

#### Members <a id="fs.filesystem.error.members">[[fs.filesystem.error.members]]</a>

Constructors are provided that store zero, one, or two paths associated
with an error.

``` cpp
filesystem_error(const string& what_arg, error_code ec);
```

*Ensures:*

- `code() == ec`,
- `path1().empty() == true`,
- `path2().empty() == true`, and
- `string_view(what()).find(what_arg.c_str())` `!= string_view::npos`.

``` cpp
filesystem_error(const string& what_arg, const path& p1, error_code ec);
```

*Ensures:*

- `code() == ec`,
- `path1()` returns a reference to the stored copy of `p1`,
- `path2().empty() == true`, and
- `string_view(what()).find(what_arg.c_str())` `!= string_view::npos`.

``` cpp
filesystem_error(const string& what_arg, const path& p1, const path& p2, error_code ec);
```

*Ensures:*

- `code() == ec`,
- `path1()` returns a reference to the stored copy of `p1`,
- `path2()` returns a reference to the stored copy of `p2`, and
- `string_view(what()).find(what_arg.c_str())` `!= string_view::npos`.

``` cpp
const path& path1() const noexcept;
```

*Returns:* A reference to the copy of `p1` stored by the constructor,
or, if none, an empty path.

``` cpp
const path& path2() const noexcept;
```

*Returns:* A reference to the copy of `p2` stored by the constructor,
or, if none, an empty path.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An NTBS that incorporates the `what_arg` argument supplied to
the constructor. The exact format is unspecified. Implementations should
include the `system_error::what()` string and the pathnames of `path1`
and `path2` in the native format in the returned string.

### Enumerations <a id="fs.enum">[[fs.enum]]</a>

#### Enum `path::format` <a id="fs.enum.path.format">[[fs.enum.path.format]]</a>

This enum specifies constants used to identify the format of the
character sequence, with the meanings listed in [[fs.enum.path.format]].

**Table: Enum `path::format`** <a id="fs.enum.path.format">[fs.enum.path.format]</a>

| Name             | Meaning                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `native_format`  | The native pathname format.                                                                                                                                                                                                                                                                                                                           |
| `generic_format` | The generic pathname format.                                                                                                                                                                                                                                                                                                                          |
| `auto_format`    | The interpretation of the format of the character sequence is implementation-defined. The implementation may inspect the content of the character sequence to determine the format. Recommended practice: For POSIX-based systems, native and generic formats are equivalent and the character sequence should always be interpreted in the same way. |


#### Enum class `file_type` <a id="fs.enum.file.type">[[fs.enum.file.type]]</a>

This enum class specifies constants used to identify file types, with
the meanings listed in [[fs.enum.file.type]]. The values of the
constants are distinct.

**Table: Enum class `file_type`** <a id="fs.enum.file.type">[fs.enum.file.type]</a>

| Constant                 | Meaning                                                                                                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `none`                   | The type of the file has not been determined or an error occurred while trying to determine the type.                                                                                                                       |
| `not_found`              | Pseudo-type indicating the file was not found. *The file not being found is not considered an error while determining the type of a file.*                                                                                  |
| `regular`                | Regular file                                                                                                                                                                                                                |
| `directory`              | Directory file                                                                                                                                                                                                              |
| `symlink`                | Symbolic link file                                                                                                                                                                                                          |
| `block`                  | Block special file                                                                                                                                                                                                          |
| `character`              | Character special file                                                                                                                                                                                                      |
| `fifo`                   | FIFO or pipe file                                                                                                                                                                                                           |
| `socket`                 | Socket file                                                                                                                                                                                                                 |
| `implementation-defined` | Implementations that support file systems having file types in addition to the above `file_type` types shall supply implementation-defined `file_type` constants to separately identify each of those additional file types |
| `unknown`                | The file exists but the type cannot be determined                                                                                                                                                                           |


#### Enum class `copy_options` <a id="fs.enum.copy.opts">[[fs.enum.copy.opts]]</a>

The `enum class` type `copy_options` is a bitmask type [[bitmask.types]]
that specifies bitmask constants used to control the semantics of copy
operations. The constants are specified in option groups with the
meanings listed in [[fs.enum.copy.opts]]. The constant `none` represents
the empty bitmask, and is shown in each option group for purposes of
exposition; implementations shall provide only a single definition.
Every other constant in the table represents a distinct bitmask element.

**Table: Enum class `copy_options`** <a id="fs.enum.copy.opts">[fs.enum.copy.opts]</a>

| Constant             | Meaning                                                                                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `none`               | (Default) Error; file already exists.                                                                                                                |
| `skip_existing`      | Do not overwrite existing file, do not report an error.                                                                                              |
| `overwrite_existing` | Overwrite the existing file.                                                                                                                         |
| `update_existing`    | Overwrite the existing file if it is older than the replacement file. \ohdrx{2}{Option group controlling `copy` function effects for subdirectories} |
| `recursive`          | Recursively copy subdirectories and their contents. \ohdrx{2}{Option group controlling `copy` function effects for symbolic links}                   |
| `copy_symlinks`      | Copy symbolic links as symbolic links rather than copying the files that they point to.                                                              |
| `skip_symlinks`      | Ignore symbolic links. \ohdrx{2}{Option group controlling `copy` function effects for choosing the form of copying}                                  |
| `directories_only`   | Copy directory structure only, do not copy non-directory files.                                                                                      |
| `create_symlinks`    | Make symbolic links instead of copies of files. The source path shall be an absolute path unless the destination path is in the current directory.   |
| `create_hard_links`  | Make hard links instead of copies of files.                                                                                                          |


#### Enum class `perms` <a id="fs.enum.perms">[[fs.enum.perms]]</a>

The `enum class` type `perms` is a bitmask type [[bitmask.types]] that
specifies bitmask constants used to identify file permissions, with the
meanings listed in [[fs.enum.perms]].

**Table: Enum class `perms`** <a id="fs.enum.perms">[fs.enum.perms]</a>

| Name | Value | POSIX | Definition or notes | (octal) | macro |
| ---- | ----- | ----- | ------------------- | ------- | ----- |
| `none` | `0`   |       | There are no permissions set for the file. |
| `owner_read` | `0400` | `S_IRUSR` | Read permission, owner |
| `owner_write` | `0200` | `S_IWUSR` | Write permission, owner |
| `owner_exec` | `0100` | `S_IXUSR` | Execute/search permission, owner |
| `owner_all` | `0700` | `S_IRWXU` | Read, write, execute/search by owner;<br> `owner_read | owner_write | owner_exec` |
| `group_read` | `040` | `S_IRGRP` | Read permission, group |
| `group_write` | `020` | `S_IWGRP` | Write permission, group |
| `group_exec` | `010` | `S_IXGRP` | Execute/search permission, group |
| `group_all` | `070` | `S_IRWXG` | Read, write, execute/search by group;<br> `group_read | group_write | group_exec` |
| `others_read` | `04`  | `S_IROTH` | Read permission, others |
| `others_write` | `02`  | `S_IWOTH` | Write permission, others |
| `others_exec` | `01`  | `S_IXOTH` | Execute/search permission, others |
| `others_all` | `07`  | `S_IRWXO` | Read, write, execute/search by others;<br> `others_read | others_write | others_exec` |
| `all` | `0777` |       | `owner_all | group_all | others_all` |
| `set_uid` | `04000` | `S_ISUID` | Set-user-ID on execution |
| `set_gid` | `02000` | `S_ISGID` | Set-group-ID on execution |
| `sticky_bit` | `01000` | `S_ISVTX` | Operating system dependent. |
| `mask` | `07777` |       | `all | set_uid | set_gid | sticky_bit` |
| `unknown` | `0xFFFF` |       | The permissions are not known, such as when a `file_status` object is created without specifying the permissions |


#### Enum class `perm_options` <a id="fs.enum.perm.opts">[[fs.enum.perm.opts]]</a>

The `enum class` type `perm_options` is a bitmask type [[bitmask.types]]
that specifies bitmask constants used to control the semantics of
permissions operations, with the meanings listed in
[[fs.enum.perm.opts]]. The bitmask constants are bitmask elements. In
[[fs.enum.perm.opts]] `perm` denotes a value of type `perms` passed to
`permissions`.

**Table: Enum class `perm_options`** <a id="fs.enum.perm.opts">[fs.enum.perm.opts]</a>

| Name       | Meaning                                                                                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `replace`  | `permissions` shall replace the file's permission bits with `perm`                                                                                      |
| `add`      | `permissions` shall replace the file's permission bits with the bitwise \logop{or} of `perm` and the file's current permission bits.                    |
| `remove`   | `permissions` shall replace the file's permission bits with the bitwise \logop{and} of the complement of `perm` and the file's current permission bits. |
| `nofollow` | `permissions` shall change the permissions of a symbolic link itself rather than the permissions of the file the link resolves to.                      |


#### Enum class `directory_options` <a id="fs.enum.dir.opts">[[fs.enum.dir.opts]]</a>

The `enum class` type `directory_options` is a bitmask type
[[bitmask.types]] that specifies bitmask constants used to identify
directory traversal options, with the meanings listed in
[[fs.enum.dir.opts]]. The constant `none` represents the empty bitmask;
every other constant in the table represents a distinct bitmask element.

**Table: Enum class `directory_options`** <a id="fs.enum.dir.opts">[fs.enum.dir.opts]</a>

| Name                       | Meaning                                                            |
| -------------------------- | ------------------------------------------------------------------ |
| `none`                     | (Default) Skip directory symlinks, permission denied is an error.  |
| `follow_directory_symlink` | Follow rather than skip directory symlinks.                        |
| `skip_permission_denied`   | Skip directories that would otherwise result in permission denied. |


### Class `file_status` <a id="fs.class.file.status">[[fs.class.file.status]]</a>

#### General <a id="fs.class.file.status.general">[[fs.class.file.status.general]]</a>

``` cpp
namespace std::filesystem {
  class file_status {
  public:
    // [fs.file.status.cons], constructors and destructor
    file_status() noexcept : file_status(file_type::none) {}
    explicit file_status(file_type ft,
                         perms prms = perms::unknown) noexcept;
    file_status(const file_status&) noexcept = default;
    file_status(file_status&&) noexcept = default;
    ~file_status();

    // assignments
    file_status& operator=(const file_status&) noexcept = default;
    file_status& operator=(file_status&&) noexcept = default;

    // [fs.file.status.mods], modifiers
    void       type(file_type ft) noexcept;
    void       permissions(perms prms) noexcept;

    // [fs.file.status.obs], observers
    file_type  type() const noexcept;
    perms      permissions() const noexcept;

    friend bool operator==(const file_status& lhs, const file_status& rhs) noexcept
      { return lhs.type() == rhs.type() && lhs.permissions() == rhs.permissions(); }
  };
}
```

#### Constructors <a id="fs.file.status.cons">[[fs.file.status.cons]]</a>

``` cpp
explicit file_status(file_type ft, perms prms = perms::unknown) noexcept;
```

*Ensures:* `type() == ft` and `permissions() == prms`.

#### Observers <a id="fs.file.status.obs">[[fs.file.status.obs]]</a>

``` cpp
file_type type() const noexcept;
```

*Returns:* The value of `type()` specified by the postconditions of the
most recent call to a constructor, `operator=`, or `type(file_type)`
function.

``` cpp
perms permissions() const noexcept;
```

*Returns:* The value of `permissions()` specified by the postconditions
of the most recent call to a constructor, `operator=`, or
`permissions(perms)` function.

#### Modifiers <a id="fs.file.status.mods">[[fs.file.status.mods]]</a>

``` cpp
void type(file_type ft) noexcept;
```

*Ensures:* `type() == ft`.

``` cpp
void permissions(perms prms) noexcept;
```

*Ensures:* `permissions() == prms`.

### Class `directory_entry` <a id="fs.class.directory.entry">[[fs.class.directory.entry]]</a>

#### General <a id="fs.class.directory.entry.general">[[fs.class.directory.entry.general]]</a>

``` cpp
namespace std::filesystem {
  class directory_entry {
  public:
    // [fs.dir.entry.cons], constructors and destructor
    directory_entry() noexcept = default;
    directory_entry(const directory_entry&) = default;
    directory_entry(directory_entry&&) noexcept = default;
    explicit directory_entry(const filesystem::path& p);
    directory_entry(const filesystem::path& p, error_code& ec);
    ~directory_entry();

    // assignments
    directory_entry& operator=(const directory_entry&) = default;
    directory_entry& operator=(directory_entry&&) noexcept = default;

    // [fs.dir.entry.mods], modifiers
    void assign(const filesystem::path& p);
    void assign(const filesystem::path& p, error_code& ec);
    void replace_filename(const filesystem::path& p);
    void replace_filename(const filesystem::path& p, error_code& ec);
    void refresh();
    void refresh(error_code& ec) noexcept;

    // [fs.dir.entry.obs], observers
    const filesystem::path& path() const noexcept;
    operator const filesystem::path&() const noexcept;
    bool exists() const;
    bool exists(error_code& ec) const noexcept;
    bool is_block_file() const;
    bool is_block_file(error_code& ec) const noexcept;
    bool is_character_file() const;
    bool is_character_file(error_code& ec) const noexcept;
    bool is_directory() const;
    bool is_directory(error_code& ec) const noexcept;
    bool is_fifo() const;
    bool is_fifo(error_code& ec) const noexcept;
    bool is_other() const;
    bool is_other(error_code& ec) const noexcept;
    bool is_regular_file() const;
    bool is_regular_file(error_code& ec) const noexcept;
    bool is_socket() const;
    bool is_socket(error_code& ec) const noexcept;
    bool is_symlink() const;
    bool is_symlink(error_code& ec) const noexcept;
    uintmax_t file_size() const;
    uintmax_t file_size(error_code& ec) const noexcept;
    uintmax_t hard_link_count() const;
    uintmax_t hard_link_count(error_code& ec) const noexcept;
    file_time_type last_write_time() const;
    file_time_type last_write_time(error_code& ec) const noexcept;
    file_status status() const;
    file_status status(error_code& ec) const noexcept;
    file_status symlink_status() const;
    file_status symlink_status(error_code& ec) const noexcept;

    bool operator==(const directory_entry& rhs) const noexcept;
    strong_ordering operator<=>(const directory_entry& rhs) const noexcept;

    // [fs.dir.entry.io], inserter
    template<class charT, class traits>
      friend basic_ostream<charT, traits>&
        operator<<(basic_ostream<charT, traits>& os, const directory_entry& d);

  private:
    filesystem::path pathobject;        // exposition only
    friend class directory_iterator;    // exposition only
  };
}
```

A `directory_entry` object stores a `path` object and may store
additional objects for file attributes such as hard link count, status,
symlink status, file size, and last write time.

Implementations should store such additional file attributes during
directory iteration if their values are available and storing the values
would allow the implementation to eliminate file system accesses by
`directory_entry` observer functions [[fs.op.funcs]]. Such stored file
attribute values are said to be *cached*.

[*Note 1*: For purposes of exposition, class `directory_iterator`
[[fs.class.directory.iterator]] is shown above as a friend of class
`directory_entry`. Friendship allows the `directory_iterator`
implementation to cache already available attribute values directly into
a `directory_entry` object without the cost of an unneeded call to
`refresh()`. — *end note*]

[*Example 1*:

``` cpp
using namespace std::filesystem;

// use possibly cached last write time to minimize disk accesses
for (auto&& x : directory_iterator("."))
{
  std::cout << x.path() << " " << x.last_write_time() << std::endl;
}

// call refresh() to refresh a stale cache
for (auto&& x : directory_iterator("."))
{
  lengthy_function(x.path());   // cache becomes stale
  x.refresh();
  std::cout << x.path() << " " << x.last_write_time() << std::endl;
}
```

On implementations that do not cache the last write time, both loops
will result in a potentially expensive call to the
`std::filesystem::last_write_time` function. On implementations that do
cache the last write time, the first loop will use the cached value and
so will not result in a potentially expensive call to the
`std::filesystem::last_write_time` function. The code is portable to any
implementation, regardless of whether or not it employs caching.

— *end example*]

#### Constructors <a id="fs.dir.entry.cons">[[fs.dir.entry.cons]]</a>

``` cpp
explicit directory_entry(const filesystem::path& p);
directory_entry(const filesystem::path& p, error_code& ec);
```

*Effects:* Calls `refresh()` or `refresh(ec)`, respectively.

*Ensures:* `path() == p` if no error occurs, otherwise
`path() == filesystem::path()`.

*Throws:* As specified in  [[fs.err.report]].

#### Modifiers <a id="fs.dir.entry.mods">[[fs.dir.entry.mods]]</a>

``` cpp
void assign(const filesystem::path& p);
void assign(const filesystem::path& p, error_code& ec);
```

*Effects:* Equivalent to `pathobject = p`, then `refresh()` or
`refresh(ec)`, respectively. If an error occurs, the values of any
cached attributes are unspecified.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
void replace_filename(const filesystem::path& p);
void replace_filename(const filesystem::path& p, error_code& ec);
```

*Effects:* Equivalent to `pathobject.replace_filename(p)`, then
`refresh()` or `refresh(ec)`, respectively. If an error occurs, the
values of any cached attributes are unspecified.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
void refresh();
void refresh(error_code& ec) noexcept;
```

*Effects:* Stores the current values of any cached attributes of the
file `p` resolves to. If an error occurs, an error is
reported [[fs.err.report]] and the values of any cached attributes are
unspecified.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: Implementations of
`directory_iterator`[[fs.class.directory.iterator]] are prohibited from
directly or indirectly calling the `refresh` function as described in
[[fs.class.directory.iterator.general]]. — *end note*]

#### Observers <a id="fs.dir.entry.obs">[[fs.dir.entry.obs]]</a>

Unqualified function names in the *Returns:* elements of the
`directory_entry` observers described below refer to members of the
`std::filesystem` namespace.

``` cpp
const filesystem::path& path() const noexcept;
operator const filesystem::path&() const noexcept;
```

*Returns:* `pathobject`.

``` cpp
bool exists() const;
bool exists(error_code& ec) const noexcept;
```

*Returns:* `exists(this->status())` or `exists(this->status(ec))`,
respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_block_file() const;
bool is_block_file(error_code& ec) const noexcept;
```

*Returns:* `is_block_file(this->status())` or
`is_block_file(this->status(ec))`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_character_file() const;
bool is_character_file(error_code& ec) const noexcept;
```

*Returns:* `is_character_file(this->status())` or
`is_character_file(this->status(ec))`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_directory() const;
bool is_directory(error_code& ec) const noexcept;
```

*Returns:* `is_directory(this->status())` or
`is_directory(this->status(ec))`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_fifo() const;
bool is_fifo(error_code& ec) const noexcept;
```

*Returns:* `is_fifo(this->status())` or `is_fifo(this->status(ec))`,
respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_other() const;
bool is_other(error_code& ec) const noexcept;
```

*Returns:* `is_other(this->status())` or `is_other(this->status(ec))`,
respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_regular_file() const;
bool is_regular_file(error_code& ec) const noexcept;
```

*Returns:* `is_regular_file(this->status())` or
`is_regular_file(this->status(ec))`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_socket() const;
bool is_socket(error_code& ec) const noexcept;
```

*Returns:* `is_socket(this->status())` or `is_socket(this->status(ec))`,
respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool is_symlink() const;
bool is_symlink(error_code& ec) const noexcept;
```

*Returns:* `is_symlink(this->symlink_status())` or
`is_symlink(this->symlink_status(ec))`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
uintmax_t file_size() const;
uintmax_t file_size(error_code& ec) const noexcept;
```

*Returns:* If cached, the file size attribute value. Otherwise,
`file_size(path())` or `file_size(path(), ec)`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
uintmax_t hard_link_count() const;
uintmax_t hard_link_count(error_code& ec) const noexcept;
```

*Returns:* If cached, the hard link count attribute value. Otherwise,
`hard_link_count(path())` or `hard_link_count(path(), ec)`,
respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
file_time_type last_write_time() const;
file_time_type last_write_time(error_code& ec) const noexcept;
```

*Returns:* If cached, the last write time attribute value. Otherwise,
`last_write_time(path())` or `last_write_time(path(), ec)`,
respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
file_status status() const;
file_status status(error_code& ec) const noexcept;
```

*Returns:* If cached, the status attribute value. Otherwise,
`status(path())` or `status(path(), ec)`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
file_status symlink_status() const;
file_status symlink_status(error_code& ec) const noexcept;
```

*Returns:* If cached, the symlink status attribute value. Otherwise,
`symlink_status(path())` or `symlink_status(path(), ec)`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool operator==(const directory_entry& rhs) const noexcept;
```

*Returns:* `pathobject == rhs.pathobject`.

``` cpp
strong_ordering operator<=>(const directory_entry& rhs) const noexcept;
```

*Returns:* `pathobject <=> rhs.pathobject`.

#### Inserter <a id="fs.dir.entry.io">[[fs.dir.entry.io]]</a>

``` cpp
template<class charT, class traits>
  friend basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const directory_entry& d);
```

*Effects:* Equivalent to: `return os << d.path();`

### Class `directory_iterator` <a id="fs.class.directory.iterator">[[fs.class.directory.iterator]]</a>

#### General <a id="fs.class.directory.iterator.general">[[fs.class.directory.iterator.general]]</a>

An object of type `directory_iterator` provides an iterator for a
sequence of `directory_entry` elements representing the path and any
cached attribute values [[fs.class.directory.entry]] for each file in a
directory or in an *implementation-defined* directory-like file type.

[*Note 1*: For iteration into subdirectories, see class
`recursive_directory_iterator` [[fs.class.rec.dir.itr]]. — *end note*]

``` cpp
namespace std::filesystem {
  class directory_iterator {
  public:
    using iterator_category = input_iterator_tag;
    using value_type        = directory_entry;
    using difference_type   = ptrdiff_t;
    using pointer           = const directory_entry*;
    using reference         = const directory_entry&;

    // [fs.dir.itr.members], member functions
    directory_iterator() noexcept;
    explicit directory_iterator(const path& p);
    directory_iterator(const path& p, directory_options options);
    directory_iterator(const path& p, error_code& ec);
    directory_iterator(const path& p, directory_options options,
                       error_code& ec);
    directory_iterator(const directory_iterator& rhs);
    directory_iterator(directory_iterator&& rhs) noexcept;
    ~directory_iterator();

    directory_iterator& operator=(const directory_iterator& rhs);
    directory_iterator& operator=(directory_iterator&& rhs) noexcept;

    const directory_entry& operator*() const;
    const directory_entry* operator->() const;
    directory_iterator&    operator++();
    directory_iterator&    increment(error_code& ec);

    bool operator==(default_sentinel_t) const noexcept {
      return *this == directory_iterator();
    }

    // other members as required by [input.iterators], input iterators
  };
}
```

`directory_iterator` meets the *Cpp17InputIterator* requirements
[[input.iterators]].

If an iterator of type `directory_iterator` reports an error or is
advanced past the last directory element, that iterator shall become
equal to the end iterator value. The `directory_iterator` default
constructor shall create an iterator equal to the end iterator value,
and this shall be the only valid iterator for the end condition.

The end iterator is not dereferenceable.

Two end iterators are always equal. An end iterator shall not be equal
to a non-end iterator.

The result of calling the `path()` member of the `directory_entry`
object obtained by dereferencing a `directory_iterator` is a reference
to a `path` object composed of the directory argument from which the
iterator was constructed with the filename of the directory entry
appended as if by `operator/=`.

Directory iteration shall not yield directory entries for the current
(dot) and parent (dot-dot) directories.

The order of directory entries obtained by dereferencing successive
increments of a `directory_iterator` is unspecified.

Constructors and non-const `directory_iterator` member functions store
the values of any cached attributes [[fs.class.directory.entry]] in the
`directory_entry` element returned by `operator*()`.
`directory_iterator` member functions shall not directly or indirectly
call any `directory_entry` `refresh` function.

[*Note 2*: The exact mechanism for storing cached attribute values is
not exposed to users. For exposition, class `directory_iterator` is
shown in [[fs.class.directory.entry]] as a friend of class
`directory_entry`. — *end note*]

[*Note 3*: A path obtained by dereferencing a directory iterator might
not actually exist; it could be a symbolic link to a non-existent file.
Recursively walking directory trees for purposes of removing and
renaming entries might invalidate symbolic links that are being
followed. — *end note*]

[*Note 4*: If a file is removed from or added to a directory after the
construction of a `directory_iterator` for the directory, it is
unspecified whether or not subsequently incrementing the iterator will
ever result in an iterator referencing the removed or added directory
entry. See POSIX `readdir`. — *end note*]

#### Members <a id="fs.dir.itr.members">[[fs.dir.itr.members]]</a>

``` cpp
directory_iterator() noexcept;
```

*Effects:* Constructs the end iterator.

``` cpp
explicit directory_iterator(const path& p);
directory_iterator(const path& p, directory_options options);
directory_iterator(const path& p, error_code& ec);
directory_iterator(const path& p, directory_options options, error_code& ec);
```

*Effects:* For the directory that `p` resolves to, constructs an
iterator for the first element in a sequence of `directory_entry`
elements representing the files in the directory, if any; otherwise the
end iterator. However, if

``` cpp
(options & directory_options::skip_permission_denied) != directory_options::none
```

and construction encounters an error indicating that permission to
access `p` is denied, constructs the end iterator and does not report an
error.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: To iterate over the current directory, use
`directory_iterator(".")` rather than
`directory_iterator("")`. — *end note*]

``` cpp
directory_iterator(const directory_iterator& rhs);
directory_iterator(directory_iterator&& rhs) noexcept;
```

*Ensures:* `*this` has the original value of `rhs`.

``` cpp
directory_iterator& operator=(const directory_iterator& rhs);
directory_iterator& operator=(directory_iterator&& rhs) noexcept;
```

*Effects:* If `*this` and `rhs` are the same object, the member has no
effect.

*Ensures:* `*this` has the original value of `rhs`.

*Returns:* `*this`.

``` cpp
directory_iterator& operator++();
directory_iterator& increment(error_code& ec);
```

*Effects:* As specified for the prefix increment operation of Input
iterators [[input.iterators]].

*Returns:* `*this`.

*Throws:* As specified in  [[fs.err.report]].

#### Non-member functions <a id="fs.dir.itr.nonmembers">[[fs.dir.itr.nonmembers]]</a>

These functions enable range access for `directory_iterator`.

``` cpp
directory_iterator begin(directory_iterator iter) noexcept;
```

*Returns:* `iter`.

``` cpp
directory_iterator end(directory_iterator) noexcept;
```

*Returns:* `directory_iterator()`.

### Class `recursive_directory_iterator` <a id="fs.class.rec.dir.itr">[[fs.class.rec.dir.itr]]</a>

#### General <a id="fs.class.rec.dir.itr.general">[[fs.class.rec.dir.itr.general]]</a>

An object of type `recursive_directory_iterator` provides an iterator
for a sequence of `directory_entry` elements representing the files in a
directory or in an *implementation-defined* directory-like file type,
and its subdirectories.

``` cpp
namespace std::filesystem {
  class recursive_directory_iterator {
  public:
    using iterator_category = input_iterator_tag;
    using value_type        = directory_entry;
    using difference_type   = ptrdiff_t;
    using pointer           = const directory_entry*;
    using reference         = const directory_entry&;

    // [fs.rec.dir.itr.members], constructors and destructor
    recursive_directory_iterator() noexcept;
    explicit recursive_directory_iterator(const path& p);
    recursive_directory_iterator(const path& p, directory_options options);
    recursive_directory_iterator(const path& p, directory_options options,
                                 error_code& ec);
    recursive_directory_iterator(const path& p, error_code& ec);
    recursive_directory_iterator(const recursive_directory_iterator& rhs);
    recursive_directory_iterator(recursive_directory_iterator&& rhs) noexcept;
    ~recursive_directory_iterator();

    // [fs.rec.dir.itr.members], observers
    directory_options  options() const;
    int                depth() const;
    bool               recursion_pending() const;

    const directory_entry& operator*() const;
    const directory_entry* operator->() const;

    // [fs.rec.dir.itr.members], modifiers
    recursive_directory_iterator&
      operator=(const recursive_directory_iterator& rhs);
    recursive_directory_iterator&
      operator=(recursive_directory_iterator&& rhs) noexcept;

    recursive_directory_iterator& operator++();
    recursive_directory_iterator& increment(error_code& ec);

    void pop();
    void pop(error_code& ec);
    void disable_recursion_pending();

    bool operator==(default_sentinel_t) const noexcept {
      return *this == recursive_directory_iterator();
    }

    // other members as required by [input.iterators], input iterators
  };
}
```

Calling `options`, `depth`, `recursion_pending`, `pop` or
`disable_recursion_pending` on an iterator that is not dereferenceable
results in undefined behavior.

The behavior of a `recursive_directory_iterator` is the same as a
`directory_iterator` unless otherwise specified.

[*Note 1*: If the directory structure being iterated over contains
cycles then it is possible that the end iterator is
unreachable. — *end note*]

#### Members <a id="fs.rec.dir.itr.members">[[fs.rec.dir.itr.members]]</a>

``` cpp
recursive_directory_iterator() noexcept;
```

*Effects:* Constructs the end iterator.

``` cpp
explicit recursive_directory_iterator(const path& p);
recursive_directory_iterator(const path& p, directory_options options);
recursive_directory_iterator(const path& p, directory_options options, error_code& ec);
recursive_directory_iterator(const path& p, error_code& ec);
```

*Effects:* Constructs an iterator representing the first entry in the
directory to which `p` resolves, if any; otherwise, the end iterator.
However, if

``` cpp
(options & directory_options::skip_permission_denied) != directory_options::none
```

and construction encounters an error indicating that permission to
access `p` is denied, constructs the end iterator and does not report an
error.

*Ensures:* `options() == options` for the signatures with a
`directory_options` argument, otherwise
`options() == directory_options::none`.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: Use `recursive_directory_iterator(".")` rather than
`recursive_directory_iterator("")` to iterate over the current
directory. — *end note*]

[*Note 2*: By default, `recursive_directory_iterator` does not follow
directory symlinks. To follow directory symlinks, specify `options` as
`directory_options::follow_directory_symlink`. — *end note*]

``` cpp
recursive_directory_iterator(const recursive_directory_iterator& rhs);
```

*Ensures:*

- `options() == rhs.options()`
- `depth() == rhs.depth()`
- `recursion_pending() == rhs.recursion_pending()`

``` cpp
recursive_directory_iterator(recursive_directory_iterator&& rhs) noexcept;
```

*Ensures:* `options()`, `depth()`, and `recursion_pending()` have the
values that `rhs.options()`, `rhs.depth()`, and
`rhs.recursion_pending()`, respectively, had before the function call.

``` cpp
recursive_directory_iterator& operator=(const recursive_directory_iterator& rhs);
```

*Effects:* If `*this` and `rhs` are the same object, the member has no
effect.

*Ensures:*

- `options() == rhs.options()`
- `depth() == rhs.depth()`
- `recursion_pending() == rhs.recursion_pending()`

*Returns:* `*this`.

``` cpp
recursive_directory_iterator& operator=(recursive_directory_iterator&& rhs) noexcept;
```

*Effects:* If `*this` and `rhs` are the same object, the member has no
effect.

*Ensures:* `options()`, `depth()`, and `recursion_pending()` have the
values that `rhs.options()`, `rhs.depth()`, and
`rhs.recursion_pending()`, respectively, had before the function call.

*Returns:* `*this`.

``` cpp
directory_options options() const;
```

*Returns:* The value of the argument passed to the constructor for the
`options` parameter, if present, otherwise `directory_options::none`.

*Throws:* Nothing.

``` cpp
int depth() const;
```

*Returns:* The current depth of the directory tree being traversed.

[*Note 3*: The initial directory is depth `0`, its immediate
subdirectories are depth `1`, and so forth. — *end note*]

*Throws:* Nothing.

``` cpp
bool recursion_pending() const;
```

*Returns:* `true` if `disable_recursion_pending()` has not been called
subsequent to the prior construction or increment operation, otherwise
`false`.

*Throws:* Nothing.

``` cpp
recursive_directory_iterator& operator++();
recursive_directory_iterator& increment(error_code& ec);
```

*Effects:* As specified for the prefix increment operation of Input
iterators [[input.iterators]], except that:

- If there are no more entries at the current depth, then if
  `depth() != 0` iteration over the parent directory resumes; otherwise
  `*this = recursive_directory_iterator()`.
- Otherwise if
  ``` cpp
  recursion_pending() && is_directory((*this)->status()) &&
  (!is_symlink((*this)->symlink_status()) ||
   (options() & directory_options::follow_directory_symlink) != directory_options::none)
  ```

  then either directory `(*this)->path()` is recursively iterated into
  or, if
  ``` cpp
  (options() & directory_options::skip_permission_denied) != directory_options::none
  ```

  and an error occurs indicating that permission to access directory
  `(*this)->path()` is denied, then directory `(*this)->path()` is
  treated as an empty directory and no error is reported.

*Returns:* `*this`.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
void pop();
void pop(error_code& ec);
```

*Effects:* If `depth() == 0`, set `*this` to
`recursive_directory_iterator()`. Otherwise, cease iteration of the
directory currently being iterated over, and continue iteration over the
parent directory.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* Any copies of the previous value of `*this` are no longer
required to be dereferenceable nor to be in the domain of `==`.

``` cpp
void disable_recursion_pending();
```

*Ensures:* `recursion_pending() == false`.

[*Note 4*: `disable_recursion_pending``()` is used to prevent unwanted
recursion into a directory. — *end note*]

#### Non-member functions <a id="fs.rec.dir.itr.nonmembers">[[fs.rec.dir.itr.nonmembers]]</a>

These functions enable use of `recursive_directory_iterator` with
range-based `for` statements.

``` cpp
recursive_directory_iterator begin(recursive_directory_iterator iter) noexcept;
```

*Returns:* `iter`.

``` cpp
recursive_directory_iterator end(recursive_directory_iterator) noexcept;
```

*Returns:* `recursive_directory_iterator()`.

### Filesystem operation functions <a id="fs.op.funcs">[[fs.op.funcs]]</a>

#### General <a id="fs.op.funcs.general">[[fs.op.funcs.general]]</a>

Filesystem operation functions query or modify files, including
directories, in external storage.

[*Note 1*: Because hardware failures, network failures, file system
races [[fs.race.behavior]], and many other kinds of errors occur
frequently in file system operations, any filesystem operation function,
no matter how apparently innocuous, can encounter an error; see 
[[fs.err.report]]. — *end note*]

#### Absolute <a id="fs.op.absolute">[[fs.op.absolute]]</a>

``` cpp
path filesystem::absolute(const path& p);
path filesystem::absolute(const path& p, error_code& ec);
```

*Effects:* Composes an absolute path referencing the same file system
location as `p` according to the operating system [[fs.conform.os]].

*Returns:* The composed path. The signature with argument `ec` returns
`path()` if an error occurs.

[*Note 1*: For the returned path, `rp`, `rp.is_absolute()` is `true`
unless an error occurs. — *end note*]

*Throws:* As specified in  [[fs.err.report]].

[*Note 2*: To resolve symlinks or perform other sanitization that can
involve queries to secondary storage, such as hard disks, consider
`canonical`[[fs.op.canonical]]. — *end note*]

[*Note 3*: Implementations are strongly encouraged to not query
secondary storage, and not consider `!exists(p)` an
error. — *end note*]

[*Example 1*: For POSIX-based operating systems, `absolute(p)` is
simply `current_path()/p`. For Windows-based operating systems,
`absolute` might have the same semantics as
`GetFullPathNameW`. — *end example*]

#### Canonical <a id="fs.op.canonical">[[fs.op.canonical]]</a>

``` cpp
path filesystem::canonical(const path& p);
path filesystem::canonical(const path& p, error_code& ec);
```

*Effects:* Converts `p` to an absolute path that has no symbolic link,
dot, or dot-dot elements in its pathname in the generic format.

*Returns:* A path that refers to the same file system object as
`absolute(p)`. The signature with argument `ec` returns `path()` if an
error occurs.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* `!exists(p)` is an error.

#### Copy <a id="fs.op.copy">[[fs.op.copy]]</a>

``` cpp
void filesystem::copy(const path& from, const path& to);
```

*Effects:* Equivalent to `copy(from, to, copy_options::none)`.

``` cpp
void filesystem::copy(const path& from, const path& to, error_code& ec);
```

*Effects:* Equivalent to `copy(from, to, copy_options::none, ec)`.

``` cpp
void filesystem::copy(const path& from, const path& to, copy_options options);
void filesystem::copy(const path& from, const path& to, copy_options options,
          error_code& ec);
```

*Preconditions:* At most one element from each option
group [[fs.enum.copy.opts]] is set in `options`.

*Effects:* Before the first use of `f` and `t`:

- If
  ``` cpp
  (options & copy_options::create_symlinks) != copy_options::none ||
  (options & copy_options::skip_symlinks) != copy_options::none
  ```

  then `auto f = symlink_status(from)` and if needed
  `auto t = symlink_status(to)`.
- Otherwise, if
  ``` cpp
  (options & copy_options::copy_symlinks) != copy_options::none
  ```

  then `auto f = symlink_status(from)` and if needed
  `auto t = status(to)`.
- Otherwise, `auto f = status(from)` and if needed
  `auto t = status(to)`.

Effects are then as follows:

- If `f.type()` or `t.type()` is an implementation-defined file
  type [[fs.enum.file.type]], then the effects are
  *implementation-defined*.
- Otherwise, an error is reported as specified in  [[fs.err.report]] if:
  - `exists(f)` is `false`, or
  - `equivalent(from, to)` is `true`, or
  - `is_other(f) || is_other(t)` is `true`, or
  - `is_directory(f) && is_regular_file(t)` is `true`.
- Otherwise, if `is_symlink(f)`, then:
  - If `(options & copy_options::skip_symlinks) != copy_options::none`
    then return.
  - Otherwise if
    ``` cpp
    !exists(t) && (options & copy_options::copy_symlinks) != copy_options::none
    ```

    then `copy_symlink(from, to)`.
  - Otherwise report an error as specified in  [[fs.err.report]].
- Otherwise, if `is_regular_file(f)`, then:
  - If
    `(options & copy_options::directories_only) != copy_options::none`,
    then return.
  - Otherwise, if
    `(options & copy_options::create_symlinks) `` != copy_options::none`,
    then create a symbolic link to the source file.
  - Otherwise, if
    `(options & copy_options::create_hard_links) != copy_options::none`,
    then create a hard link to the source file.
  - Otherwise, if `is_directory(t)`, then
    `copy_file(from, to/from.filename(), options)`.
  - Otherwise, `copy_file(from, to, options)`.
- Otherwise, if
  ``` cpp
  is_directory(f) &&
  (options & copy_options::create_symlinks) != copy_options::none
  ```

  then report an error with an `error_code` argument equal to
  `make_error_code(errc::is_a_directory)`.
- Otherwise, if
  ``` cpp
  is_directory(f) &&
  ((options & copy_options::recursive) != copy_options::none ||
   options == copy_options::none)
  ```

  then:
  - If `exists(t)` is `false`, then `create_directory(to, from)`.
  - Then, iterate over the files in `from`, as if by
    ``` cpp
    for (const directory_entry& x : directory_iterator(from))
      copy(x.path(), to/x.path().filename(),
           options | copy_options::in-recursive-copy);
    ```

    where *`in-recursive-copy`* is a bitmask element of `copy_options`
    that is not one of the elements in  [[fs.enum.copy.opts]].
- Otherwise, for the signature with argument `ec`, `ec.clear()`.
- Otherwise, no effects.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* For the signature with argument `ec`, any library functions
called by the implementation shall have an `error_code` argument if
applicable.

[*Example 1*:

Given this directory structure:

``` cpp
/dir1
  file1
  file2
  dir2
    file3
```

Calling `copy("/dir1", "/dir3")` would result in:

``` cpp
/dir1
  file1
  file2
  dir2
    file3
/dir3
  file1
  file2
```

Alternatively, calling `copy("/dir1", "/dir3", copy_options::recursive)`
would result in:

``` cpp
/dir1
  file1
  file2
  dir2
    file3
/dir3
  file1
  file2
  dir2
    file3
```

— *end example*]

#### Copy file <a id="fs.op.copy.file">[[fs.op.copy.file]]</a>

``` cpp
bool filesystem::copy_file(const path& from, const path& to);
bool filesystem::copy_file(const path& from, const path& to, error_code& ec);
```

*Returns:* `copy_file(from, to, copy_options::none)` or  
`copy_file(from, to, copy_options::none, ec)`, respectively.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool filesystem::copy_file(const path& from, const path& to, copy_options options);
bool filesystem::copy_file(const path& from, const path& to, copy_options options,
               error_code& ec);
```

*Preconditions:* At most one element from each option
group [[fs.enum.copy.opts]] is set in `options`.

*Effects:* As follows:

- Report an error as specified in  [[fs.err.report]] if:
  - `is_regular_file(from)` is `false`, or
  - `exists(to)` is `true` and `is_regular_file(to)` is `false`, or
  - `exists(to)` is `true` and `equivalent(from, to)` is `true`, or
  - `exists(to)` is `true` and
    ``` cpp
    (options & (copy_options::skip_existing |
                copy_options::overwrite_existing |
                copy_options::update_existing)) == copy_options::none
    ```
- Otherwise, copy the contents and attributes of the file `from`
  resolves to, to the file `to` resolves to, if:
  - `exists(to)` is `false`, or
  - `(options & copy_options::overwrite_existing) != copy_options::none`,
    or
  - `(options & copy_options::update_existing) `` `` != copy_options::none`
    and `from` is more recent than `to`, determined as if by use of the
    `last_write_time` function [[fs.op.last.write.time]].
- Otherwise, no effects.

*Returns:* `true` if the `from` file was copied, otherwise `false`. The
signature with argument `ec` returns `false` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

*Complexity:* At most one direct or indirect invocation of `status(to)`.

#### Copy symlink <a id="fs.op.copy.symlink">[[fs.op.copy.symlink]]</a>

``` cpp
void filesystem::copy_symlink(const path& existing_symlink, const path& new_symlink);
void filesystem::copy_symlink(const path& existing_symlink, const path& new_symlink,
                  error_code& ec) noexcept;
```

*Effects:* Equivalent to
*`function`*`(read_symlink(existing_symlink), new_symlink)` or  
*`function`*`(read_symlink(existing_symlink, ec), new_symlink, ec)`,
respectively, where in each case *`function`* is `create_symlink` or
`create_directory_symlink` as appropriate.

*Throws:* As specified in  [[fs.err.report]].

#### Create directories <a id="fs.op.create.directories">[[fs.op.create.directories]]</a>

``` cpp
bool filesystem::create_directories(const path& p);
bool filesystem::create_directories(const path& p, error_code& ec);
```

*Effects:* Calls `create_directory()` for each element of `p` that does
not exist.

*Returns:* `true` if a new directory was created for the directory `p`
resolves to, otherwise `false`.

*Throws:* As specified in  [[fs.err.report]].

*Complexity:* 𝑂(n) where *n* is the number of elements of `p`.

#### Create directory <a id="fs.op.create.directory">[[fs.op.create.directory]]</a>

``` cpp
bool filesystem::create_directory(const path& p);
bool filesystem::create_directory(const path& p, error_code& ec) noexcept;
```

*Effects:* Creates the directory `p` resolves to, as if by POSIX `mkdir`
with a second argument of `static_cast<int>(perms::all)`. If `mkdir`
fails because `p` resolves to an existing directory, no error is
reported. Otherwise on failure an error is reported.

*Returns:* `true` if a new directory was created, otherwise `false`.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
bool filesystem::create_directory(const path& p, const path& existing_p);
bool filesystem::create_directory(const path& p, const path& existing_p, error_code& ec) noexcept;
```

*Effects:* Creates the directory `p` resolves to, with attributes copied
from directory `existing_p`. The set of attributes copied is operating
system dependent. If `mkdir` fails because `p` resolves to an existing
directory, no error is reported. Otherwise on failure an error is
reported.

[*Note 1*: For POSIX-based operating systems, the attributes are those
copied by native API `stat(existing_p.c_str(), &attributes_stat)`
followed by `mkdir(p.c_str(), attributes_stat.st_mode)`. For
Windows-based operating systems, the attributes are those copied by
native API
`CreateDirectoryExW(existing_p.c_str(), p.c_str(), 0)`. — *end note*]

*Returns:* `true` if a new directory was created with attributes copied
from directory `existing_p`, otherwise `false`.

*Throws:* As specified in  [[fs.err.report]].

#### Create directory symlink <a id="fs.op.create.dir.symlk">[[fs.op.create.dir.symlk]]</a>

``` cpp
void filesystem::create_directory_symlink(const path& to, const path& new_symlink);
void filesystem::create_directory_symlink(const path& to, const path& new_symlink,
                              error_code& ec) noexcept;
```

*Effects:* Establishes the postcondition, as if by POSIX `symlink()`.

*Ensures:* `new_symlink` resolves to a symbolic link file that contains
an unspecified representation of `to`.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: Some operating systems require symlink creation to identify
that the link is to a directory. Thus, `create_symlink()` (instead of
`create_directory_symlink()`) cannot be used reliably to create
directory symlinks. — *end note*]

[*Note 2*: Some operating systems do not support symbolic links at all
or support them only for regular files. Some file systems (such as the
FAT file system) do not support symbolic links regardless of the
operating system. — *end note*]

#### Create hard link <a id="fs.op.create.hard.lk">[[fs.op.create.hard.lk]]</a>

``` cpp
void filesystem::create_hard_link(const path& to, const path& new_hard_link);
void filesystem::create_hard_link(const path& to, const path& new_hard_link,
                                      error_code& ec) noexcept;
```

*Effects:* Establishes the postcondition, as if by POSIX `link()`.

*Ensures:*

- `exists(to) && exists(new_hard_link) && equivalent(to, new_hard_link)`
- The contents of the file or directory `to` resolves to are unchanged.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: Some operating systems do not support hard links at all or
support them only for regular files. Some file systems (such as the FAT
file system) do not support hard links regardless of the operating
system. Some file systems limit the number of links per
file. — *end note*]

#### Create symlink <a id="fs.op.create.symlink">[[fs.op.create.symlink]]</a>

``` cpp
void filesystem::create_symlink(const path& to, const path& new_symlink);
void filesystem::create_symlink(const path& to, const path& new_symlink,
                    error_code& ec) noexcept;
```

*Effects:* Establishes the postcondition, as if by POSIX `symlink()`.

*Ensures:* `new_symlink` resolves to a symbolic link file that contains
an unspecified representation of `to`.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: Some operating systems do not support symbolic links at all
or support them only for regular files. Some file systems (such as the
FAT file system) do not support symbolic links regardless of the
operating system. — *end note*]

#### Current path <a id="fs.op.current.path">[[fs.op.current.path]]</a>

``` cpp
path filesystem::current_path();
path filesystem::current_path(error_code& ec);
```

*Returns:* The absolute path of the current working directory, whose
pathname in the native format is obtained as if by POSIX `getcwd()`. The
signature with argument `ec` returns `path()` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* The current working directory is the directory, associated
with the process, that is used as the starting location in pathname
resolution for relative paths.

[*Note 1*: The `current_path()` name was chosen to emphasize that the
returned value is a path, not just a single directory
name. — *end note*]

[*Note 2*: The current path as returned by many operating systems is a
dangerous global variable and can be changed unexpectedly by third-party
or system library functions, or by another thread. — *end note*]

``` cpp
void filesystem::current_path(const path& p);
void filesystem::current_path(const path& p, error_code& ec) noexcept;
```

*Effects:* Establishes the postcondition, as if by POSIX `chdir()`.

*Ensures:* `equivalent(p, current_path())`.

*Throws:* As specified in  [[fs.err.report]].

[*Note 3*: The current path for many operating systems is a dangerous
global state and can be changed unexpectedly by third-party or system
library functions, or by another thread. — *end note*]

#### Equivalent <a id="fs.op.equivalent">[[fs.op.equivalent]]</a>

``` cpp
bool filesystem::equivalent(const path& p1, const path& p2);
bool filesystem::equivalent(const path& p1, const path& p2, error_code& ec) noexcept;
```

Two paths are considered to resolve to the same file system entity if
two candidate entities reside on the same device at the same location.

[*Note 1*: On POSIX platforms, this is determined as if by the values
of the POSIX `stat` class, obtained as if by `stat()` for the two paths,
having equal `st_dev` values and equal `st_ino` values. — *end note*]

*Returns:* `true`, if `p1` and `p2` resolve to the same file system
entity, otherwise `false`. The signature with argument `ec` returns
`false` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* `!exists(p1) || !exists(p2)` is an error.

#### Exists <a id="fs.op.exists">[[fs.op.exists]]</a>

``` cpp
bool filesystem::exists(file_status s) noexcept;
```

*Returns:* `status_known(s) && s.type() != file_type::not_found`.

``` cpp
bool filesystem::exists(const path& p);
bool filesystem::exists(const path& p, error_code& ec) noexcept;
```

Let `s` be a `file_status`, determined as if by `status(p)` or
`status(p, ec)`, respectively.

*Effects:* The signature with argument `ec` calls `ec.clear()` if
`status_known(s)`.

*Returns:* `exists(s)`.

*Throws:* As specified in  [[fs.err.report]].

#### File size <a id="fs.op.file.size">[[fs.op.file.size]]</a>

``` cpp
uintmax_t filesystem::file_size(const path& p);
uintmax_t filesystem::file_size(const path& p, error_code& ec) noexcept;
```

*Effects:* If `exists(p)` is `false`, an error is
reported [[fs.err.report]].

*Returns:*

- If `is_regular_file(p)`, the size in bytes of the file `p` resolves
  to, determined as if by the value of the POSIX `stat` class member
  `st_size` obtained as if by POSIX `stat()`.
- Otherwise, the result is *implementation-defined*.

The signature with argument `ec` returns `static_cast<uintmax_t>(-1)` if
an error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Hard link count <a id="fs.op.hard.lk.ct">[[fs.op.hard.lk.ct]]</a>

``` cpp
uintmax_t filesystem::hard_link_count(const path& p);
uintmax_t filesystem::hard_link_count(const path& p, error_code& ec) noexcept;
```

*Returns:* The number of hard links for `p`. The signature with argument
`ec` returns `static_cast<uintmax_t>(-1)` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is block file <a id="fs.op.is.block.file">[[fs.op.is.block.file]]</a>

``` cpp
bool filesystem::is_block_file(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::block`.

``` cpp
bool filesystem::is_block_file(const path& p);
bool filesystem::is_block_file(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_block_file(status(p))` or `is_block_file(status(p, ec))`,
respectively. The signature with argument `ec` returns `false` if an
error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is character file <a id="fs.op.is.char.file">[[fs.op.is.char.file]]</a>

``` cpp
bool filesystem::is_character_file(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::character`.

``` cpp
bool filesystem::is_character_file(const path& p);
bool filesystem::is_character_file(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_character_file(status(p))` or
`is_character_file(status(p, ec))`, respectively.  
The signature with argument `ec` returns `false` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is directory <a id="fs.op.is.directory">[[fs.op.is.directory]]</a>

``` cpp
bool filesystem::is_directory(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::directory`.

``` cpp
bool filesystem::is_directory(const path& p);
bool filesystem::is_directory(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_directory(status(p))` or `is_directory(status(p, ec))`,
respectively. The signature with argument `ec` returns `false` if an
error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is empty <a id="fs.op.is.empty">[[fs.op.is.empty]]</a>

``` cpp
bool filesystem::is_empty(const path& p);
bool filesystem::is_empty(const path& p, error_code& ec);
```

*Effects:*

- Determine `file_status s`, as if by `status(p)` or `status(p, ec)`,
  respectively.
- For the signature with argument `ec`, return `false` if an error
  occurred.
- Otherwise, if `is_directory(s)`:
  - Create a variable `itr`, as if by `directory_iterator itr(p)` or
    `directory_iterator itr(p, ec)`, respectively.
  - For the signature with argument `ec`, return `false` if an error
    occurred.
  - Otherwise, return `itr == directory_iterator()`.
- Otherwise:
  - Determine `uintmax_t sz`, as if by `file_size(p)` or
    `file_size(p, ec)`, respectively.
  - For the signature with argument `ec`, return `false` if an error
    occurred.
  - Otherwise, return `sz == 0`.

*Throws:* As specified in  [[fs.err.report]].

#### Is fifo <a id="fs.op.is.fifo">[[fs.op.is.fifo]]</a>

``` cpp
bool filesystem::is_fifo(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::fifo`.

``` cpp
bool filesystem::is_fifo(const path& p);
bool filesystem::is_fifo(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_fifo(status(p))` or `is_fifo(status(p, ec))`,
respectively. The signature with argument `ec` returns `false` if an
error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is other <a id="fs.op.is.other">[[fs.op.is.other]]</a>

``` cpp
bool filesystem::is_other(file_status s) noexcept;
```

*Returns:*
`exists(s) && !is_regular_file(s) && !is_directory(s) && !is_symlink(s)`.

``` cpp
bool filesystem::is_other(const path& p);
bool filesystem::is_other(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_other(status(p))` or `is_other(status(p, ec))`,
respectively. The signature with argument `ec` returns `false` if an
error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is regular file <a id="fs.op.is.regular.file">[[fs.op.is.regular.file]]</a>

``` cpp
bool filesystem::is_regular_file(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::regular`.

``` cpp
bool filesystem::is_regular_file(const path& p);
```

*Returns:* `is_regular_file(status(p))`.

*Throws:* `filesystem_error` if `status(p)` would throw
`filesystem_error`.

``` cpp
bool filesystem::is_regular_file(const path& p, error_code& ec) noexcept;
```

*Effects:* Sets `ec` as if by `status(p, ec)`.

[*Note 1*: `file_type::none`, `file_type::not_found` and
`file_type::unknown` cases set `ec` to error values. To distinguish
between cases, call the `status` function directly. — *end note*]

*Returns:* `is_regular_file(status(p, ec))`. Returns `false` if an error
occurs.

#### Is socket <a id="fs.op.is.socket">[[fs.op.is.socket]]</a>

``` cpp
bool filesystem::is_socket(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::socket`.

``` cpp
bool filesystem::is_socket(const path& p);
bool filesystem::is_socket(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_socket(status(p))` or `is_socket(status(p, ec))`,
respectively. The signature with argument `ec` returns `false` if an
error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Is symlink <a id="fs.op.is.symlink">[[fs.op.is.symlink]]</a>

``` cpp
bool filesystem::is_symlink(file_status s) noexcept;
```

*Returns:* `s.type() == file_type::symlink`.

``` cpp
bool filesystem::is_symlink(const path& p);
bool filesystem::is_symlink(const path& p, error_code& ec) noexcept;
```

*Returns:* `is_symlink(symlink_status(p))` or
`is_symlink(symlink_status(p, ec))`, respectively. The signature with
argument `ec` returns `false` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Last write time <a id="fs.op.last.write.time">[[fs.op.last.write.time]]</a>

``` cpp
file_time_type filesystem::last_write_time(const path& p);
file_time_type filesystem::last_write_time(const path& p, error_code& ec) noexcept;
```

*Returns:* The time of last data modification of `p`, determined as if
by the value of the POSIX `stat` class member `st_mtime` obtained as if
by POSIX `stat()`. The signature with argument `ec` returns
`file_time_type::min()` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
void filesystem::last_write_time(const path& p, file_time_type new_time);
void filesystem::last_write_time(const path& p, file_time_type new_time,
                     error_code& ec) noexcept;
```

*Effects:* Sets the time of last data modification of the file resolved
to by `p` to `new_time`, as if by POSIX `futimens()`.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: A postcondition of `last_write_time(p) == new_time` is not
specified because it does not necessarily hold for file systems with
coarse time granularity. — *end note*]

#### Permissions <a id="fs.op.permissions">[[fs.op.permissions]]</a>

``` cpp
void filesystem::permissions(const path& p, perms prms, perm_options opts=perm_options::replace);
void filesystem::permissions(const path& p, perms prms, error_code& ec) noexcept;
void filesystem::permissions(const path& p, perms prms, perm_options opts, error_code& ec);
```

*Preconditions:* Exactly one of the `perm_options` constants `replace`,
`add`, or `remove` is present in `opts`.

*Effects:* Applies the action specified by `opts` to the file `p`
resolves to, or to file `p` itself if `p` is a symbolic link and
`perm_options::nofollow` is set in `opts`. The action is applied as if
by POSIX `fchmodat()`.

[*Note 1*: Conceptually permissions are viewed as bits, but the actual
implementation can use some other mechanism. — *end note*]

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* The second signature behaves as if it had an additional
parameter `perm_options` `opts` with an argument of
`perm_options::replace`.

#### Proximate <a id="fs.op.proximate">[[fs.op.proximate]]</a>

``` cpp
path filesystem::proximate(const path& p, error_code& ec);
```

*Returns:* `proximate(p, current_path(), ec)`.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
path filesystem::proximate(const path& p, const path& base = current_path());
path filesystem::proximate(const path& p, const path& base, error_code& ec);
```

*Returns:* For the first form:

``` cpp
weakly_canonical(p).lexically_proximate(weakly_canonical(base));
```

For the second form:

``` cpp
weakly_canonical(p, ec).lexically_proximate(weakly_canonical(base, ec));
```

or `path()` at the first error occurrence, if any.

*Throws:* As specified in  [[fs.err.report]].

#### Read symlink <a id="fs.op.read.symlink">[[fs.op.read.symlink]]</a>

``` cpp
path filesystem::read_symlink(const path& p);
path filesystem::read_symlink(const path& p, error_code& ec);
```

*Returns:* If `p` resolves to a symbolic link, a `path` object
containing the contents of that symbolic link. The signature with
argument `ec` returns `path()` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

[*Note 1*: It is an error if `p` does not resolve to a symbolic
link. — *end note*]

#### Relative <a id="fs.op.relative">[[fs.op.relative]]</a>

``` cpp
path filesystem::relative(const path& p, error_code& ec);
```

*Returns:* `relative(p, current_path(), ec)`.

*Throws:* As specified in  [[fs.err.report]].

``` cpp
path filesystem::relative(const path& p, const path& base = current_path());
path filesystem::relative(const path& p, const path& base, error_code& ec);
```

*Returns:* For the first form:

``` cpp
weakly_canonical(p).lexically_relative(weakly_canonical(base));
```

For the second form:

``` cpp
weakly_canonical(p, ec).lexically_relative(weakly_canonical(base, ec));
```

or `path()` at the first error occurrence, if any.

*Throws:* As specified in  [[fs.err.report]].

#### Remove <a id="fs.op.remove">[[fs.op.remove]]</a>

``` cpp
bool filesystem::remove(const path& p);
bool filesystem::remove(const path& p, error_code& ec) noexcept;
```

*Effects:* If `exists(symlink_status(p, ec))`, the file `p` is removed
as if by POSIX `remove()`.

[*Note 1*: A symbolic link is itself removed, rather than the file it
resolves to. — *end note*]

*Ensures:* `exists(symlink_status(p))` is `false`.

*Returns:* `false` if `p` did not exist, otherwise `true`. The signature
with argument `ec` returns `false` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Remove all <a id="fs.op.remove.all">[[fs.op.remove.all]]</a>

``` cpp
uintmax_t filesystem::remove_all(const path& p);
uintmax_t filesystem::remove_all(const path& p, error_code& ec);
```

*Effects:* Recursively deletes the contents of `p` if it exists, then
deletes file `p` itself, as if by POSIX `remove()`.

[*Note 1*: A symbolic link is itself removed, rather than the file it
resolves to. — *end note*]

*Ensures:* `exists(symlink_status(p))` is `false`.

*Returns:* The number of files removed. The signature with argument `ec`
returns `static_cast< uintmax_t>(-1)` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

#### Rename <a id="fs.op.rename">[[fs.op.rename]]</a>

``` cpp
void filesystem::rename(const path& old_p, const path& new_p);
void filesystem::rename(const path& old_p, const path& new_p, error_code& ec) noexcept;
```

*Effects:* Renames `old_p` to `new_p`, as if by POSIX `rename()`.

[*Note 1*:

- If `old_p` and `new_p` resolve to the same existing file, no action is
  taken.
- Otherwise, the rename can include the following effects:
  - if `new_p` resolves to an existing non-directory file, `new_p` is
    removed; otherwise,
  - if `new_p` resolves to an existing directory, `new_p` is removed if
    empty on POSIX compliant operating systems but might be an error on
    other operating systems.

A symbolic link is itself renamed, rather than the file it resolves to.

— *end note*]

*Throws:* As specified in  [[fs.err.report]].

#### Resize file <a id="fs.op.resize.file">[[fs.op.resize.file]]</a>

``` cpp
void filesystem::resize_file(const path& p, uintmax_t new_size);
void filesystem::resize_file(const path& p, uintmax_t new_size, error_code& ec) noexcept;
```

*Effects:* Causes the size that would be returned by `file_size(p)` to
be equal to `new_size`, as if by POSIX `truncate()`.

*Throws:* As specified in  [[fs.err.report]].

#### Space <a id="fs.op.space">[[fs.op.space]]</a>

``` cpp
space_info filesystem::space(const path& p);
space_info filesystem::space(const path& p, error_code& ec) noexcept;
```

*Returns:* An object of type `space_info`. The value of the `space_info`
object is determined as if by using POSIX `statvfs` to obtain a POSIX
`struct statvfs`, and then multiplying its `f_blocks`, `f_bfree`, and
`f_bavail` members by its `f_frsize` member, and assigning the results
to the `capacity`, `free`, and `available` members respectively. Any
members for which the value cannot be determined shall be set to
`static_cast<uintmax_t>(-1)`. For the signature with argument `ec`, all
members are set to `static_cast<uintmax_t>(-1)` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* The value of member `space_info::available` is operating
system dependent.

[*Note 1*: `available` might be less than `free`. — *end note*]

#### Status <a id="fs.op.status">[[fs.op.status]]</a>

``` cpp
file_status filesystem::status(const path& p);
```

*Effects:* As if:

``` cpp
error_code ec;
file_status result = status(p, ec);
if (result.type() == file_type::none)
  throw filesystem_error(implementation-supplied-message, p, ec);
return result;
```

*Returns:* See above.

*Throws:* `filesystem_error`.

[*Note 1*: `result` values of `file_status(file_type::not_found)` and
`file_status(file_type::unknown)` are not considered failures and do not
cause an exception to be thrown. — *end note*]

``` cpp
file_status filesystem::status(const path& p, error_code& ec) noexcept;
```

*Effects:* If possible, determines the attributes of the file `p`
resolves to, as if by using POSIX `stat()` to obtain a POSIX
`struct stat`. If, during attribute determination, the underlying file
system API reports an error, sets `ec` to indicate the specific error
reported. Otherwise, `ec.clear()`.

[*Note 2*: This allows users to inspect the specifics of underlying API
errors even when the value returned by `status()` is not
`file_status(file_type::none)`. — *end note*]

Let `prms` denote the result of `(m & perms::mask)`, where `m` is
determined as if by converting the `st_mode` member of the obtained
`struct stat` to the type `perms`.

*Returns:*

- If `ec != error_code()`:
  - If the specific error indicates that `p` cannot be resolved because
    some element of the path does not exist, returns
    `file_status(file_type::not_found)`.
  - Otherwise, if the specific error indicates that `p` can be resolved
    but the attributes cannot be determined, returns
    `file_status(file_type::unknown)`.
  - Otherwise, returns `file_status(file_type::none)`.

  \[*Note 1*: These semantics distinguish between `p` being known not to
  exist, `p` existing but not being able to determine its attributes,
  and there being an error that prevents even knowing if `p` exists.
  These distinctions are important to some use cases. — *end note*]
- Otherwise,
  - If the attributes indicate a regular file, as if by POSIX `S_ISREG`,
    returns `file_status(file_type::regular, prms)`.
    \[*Note 2*: `file_type::regular` implies appropriate `<fstream>`
    operations would succeed, assuming no hardware, permission, access,
    or file system race errors. Lack of `file_type::regular` does not
    necessarily imply `<fstream>` operations would fail on a
    directory. — *end note*]
  - Otherwise, if the attributes indicate a directory, as if by POSIX
    `S_ISDIR`, returns `file_status(file_type::directory, prms)`.
    \[*Note 3*: `file_type::directory` implies that calling
    `directory_iterator(p)` would succeed. — *end note*]
  - Otherwise, if the attributes indicate a block special file, as if by
    POSIX `S_ISBLK`, returns `file_status(file_type::block, prms)`.
  - Otherwise, if the attributes indicate a character special file, as
    if by POSIX `S_ISCHR`, returns
    `file_status(file_type::character, prms)`.
  - Otherwise, if the attributes indicate a fifo or pipe file, as if by
    POSIX `S_ISFIFO`, returns `file_status(file_type::fifo, prms)`.
  - Otherwise, if the attributes indicate a socket, as if by POSIX
    `S_ISSOCK`, returns `file_status(file_type::socket, prms)`.
  - Otherwise, if the attributes indicate an implementation-defined file
    type [[fs.enum.file.type]], returns
    `file_status(file_type::`*`A`*`, prms)`, where *A* is the constant
    for the *implementation-defined* file type.
  - Otherwise, returns `file_status(file_type::unknown, prms)`.

*Remarks:* If a symbolic link is encountered during pathname resolution,
pathname resolution continues using the contents of the symbolic link.

#### Status known <a id="fs.op.status.known">[[fs.op.status.known]]</a>

``` cpp
bool filesystem::status_known(file_status s) noexcept;
```

*Returns:* `s.type() != file_type::none`.

#### Symlink status <a id="fs.op.symlink.status">[[fs.op.symlink.status]]</a>

``` cpp
file_status filesystem::symlink_status(const path& p);
file_status filesystem::symlink_status(const path& p, error_code& ec) noexcept;
```

*Effects:* Same as `status()`, above, except that the attributes of `p`
are determined as if by using POSIX `lstat()` to obtain a POSIX
`struct stat`.

Let `prms` denote the result of `(m & perms::mask)`, where `m` is
determined as if by converting the `st_mode` member of the obtained
`struct stat` to the type `perms`.

*Returns:* Same as `status()`, above, except that if the attributes
indicate a symbolic link, as if by POSIX `S_ISLNK`, returns
`file_status(file_type::symlink, prms)`. The signature with argument
`ec` returns `file_status(file_type::none)` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

*Remarks:* Pathname resolution terminates if `p` names a symbolic link.

#### Temporary directory path <a id="fs.op.temp.dir.path">[[fs.op.temp.dir.path]]</a>

``` cpp
path filesystem::temp_directory_path();
path filesystem::temp_directory_path(error_code& ec);
```

Let `p` be an unspecified directory path suitable for temporary files.

*Effects:* If `exists(p)` is `false` or `is_directory(p)` is `false`, an
error is reported [[fs.err.report]].

*Returns:* The path `p`. The signature with argument `ec` returns
`path()` if an error occurs.

*Throws:* As specified in  [[fs.err.report]].

[*Example 1*: For POSIX-based operating systems, an implementation
might return the path supplied by the first environment variable found
in the list TMPDIR, TMP, TEMP, TEMPDIR, or if none of these are found,
`"/tmp"`. For Windows-based operating systems, an implementation might
return the path reported by the Windows `GetTempPath` API
function. — *end example*]

#### Weakly canonical <a id="fs.op.weakly.canonical">[[fs.op.weakly.canonical]]</a>

``` cpp
path filesystem::weakly_canonical(const path& p);
path filesystem::weakly_canonical(const path& p, error_code& ec);
```

*Effects:* Using `status(p)` or `status(p, ec)`, respectively, to
determine existence, return a path composed by `operator/=` from the
result of calling `canonical()` with a path argument composed of the
leading elements of `p` that exist, if any, followed by the elements of
`p` that do not exist, if any. For the first form, `canonical()` is
called without an `error_code` argument. For the second form,
`canonical()` is called with `ec` as an `error_code` argument, and
`path()` is returned at the first error occurrence, if any.

*Ensures:* The returned path is in normal form [[fs.path.generic]].

*Returns:* `p` with symlinks resolved and the result
normalized [[fs.path.generic]].

*Throws:* As specified in  [[fs.err.report]].

## C library files <a id="c.files">[[c.files]]</a>

### Header `<cstdio>` synopsis <a id="cstdio.syn">[[cstdio.syn]]</a>

``` cpp
namespace std {
  using size_t = see [support.types.layout];
  using FILE = see below;
  using fpos_t = see below;
}

#define NULL see [support.types.nullptr]
#define _IOFBF see below
#define _IOLBF see below
#define _IONBF see below
#define BUFSIZ see below
#define EOF see below
#define FOPEN_MAX see below
#define FILENAME_MAX see below
#define L_tmpnam see below
#define SEEK_CUR see below
#define SEEK_END see below
#define SEEK_SET see below
#define TMP_MAX see below
#define stderr see below
#define stdin see below
#define stdout see below

namespace std {
  int remove(const char* filename);
  int rename(const char* old_p, const char* new_p);
  FILE* tmpfile();
  char* tmpnam(char* s);
  int fclose(FILE* stream);
  int fflush(FILE* stream);
  FILE* fopen(const char* filename, const char* mode);
  FILE* freopen(const char* filename, const char* mode, FILE* stream);
  void setbuf(FILE* stream, char* buf);
  int setvbuf(FILE* stream, char* buf, int mode, size_t size);
  int fprintf(FILE* stream, const char* format, ...);
  int fscanf(FILE* stream, const char* format, ...);
  int printf(const char* format, ...);
  int scanf(const char* format, ...);
  int snprintf(char* s, size_t n, const char* format, ...);
  int sprintf(char* s, const char* format, ...);
  int sscanf(const char* s, const char* format, ...);
  int vfprintf(FILE* stream, const char* format, va_list arg);
  int vfscanf(FILE* stream, const char* format, va_list arg);
  int vprintf(const char* format, va_list arg);
  int vscanf(const char* format, va_list arg);
  int vsnprintf(char* s, size_t n, const char* format, va_list arg);
  int vsprintf(char* s, const char* format, va_list arg);
  int vsscanf(const char* s, const char* format, va_list arg);
  int fgetc(FILE* stream);
  char* fgets(char* s, int n, FILE* stream);
  int fputc(int c, FILE* stream);
  int fputs(const char* s, FILE* stream);
  int getc(FILE* stream);
  int getchar();
  int putc(int c, FILE* stream);
  int putchar(int c);
  int puts(const char* s);
  int ungetc(int c, FILE* stream);
  size_t fread(void* ptr, size_t size, size_t nmemb, FILE* stream);
  size_t fwrite(const void* ptr, size_t size, size_t nmemb, FILE* stream);
  int fgetpos(FILE* stream, fpos_t* pos);
  int fseek(FILE* stream, long int offset, int whence);
  int fsetpos(FILE* stream, const fpos_t* pos);
  long int ftell(FILE* stream);
  void rewind(FILE* stream);
  void clearerr(FILE* stream);
  int feof(FILE* stream);
  int ferror(FILE* stream);
  void perror(const char* s);
}
```

The contents and meaning of the header `<cstdio>` are the same as the C
standard library header `<stdio.h>`.

Calls to the function `tmpnam` with an argument that is a null pointer
value may introduce a data race [[res.on.data.races]] with other calls
to `tmpnam` with an argument that is a null pointer value.

See also: ISO C 7.21

### Header `<cinttypes>` synopsis <a id="cinttypes.syn">[[cinttypes.syn]]</a>

``` cpp
#include <cstdint>  // see [cstdint.syn]

namespace std {
  using imaxdiv_t = see below;

  constexpr intmax_t imaxabs(intmax_t j);
  constexpr imaxdiv_t imaxdiv(intmax_t numer, intmax_t denom);
  intmax_t strtoimax(const char* nptr, char** endptr, int base);
  uintmax_t strtoumax(const char* nptr, char** endptr, int base);
  intmax_t wcstoimax(const wchar_t* nptr, wchar_t** endptr, int base);
  uintmax_t wcstoumax(const wchar_t* nptr, wchar_t** endptr, int base);

  constexpr intmax_t abs(intmax_t);             // optional, see below
  constexpr imaxdiv_t div(intmax_t, intmax_t);  // optional, see below
}

#define PRIdN see below
#define PRIiN see below
#define PRIoN see below
#define PRIuN see below
#define PRIxN see below
#define PRIXN see below
#define SCNdN see below
#define SCNiN see below
#define SCNoN see below
#define SCNuN see below
#define SCNxN see below
#define PRIdLEASTN see below
#define PRIiLEASTN see below
#define PRIoLEASTN see below
#define PRIuLEASTN see below
#define PRIxLEASTN see below
#define PRIXLEASTN see below
#define SCNdLEASTN see below
#define SCNiLEASTN see below
#define SCNoLEASTN see below
#define SCNuLEASTN see below
#define SCNxLEASTN see below
#define PRIdFASTN see below
#define PRIiFASTN see below
#define PRIoFASTN see below
#define PRIuFASTN see below
#define PRIxFASTN see below
#define PRIXFASTN see below
#define SCNdFASTN see below
#define SCNiFASTN see below
#define SCNoFASTN see below
#define SCNuFASTN see below
#define SCNxFASTN see below
#define PRIdMAX see below
#define PRIiMAX see below
#define PRIoMAX see below
#define PRIuMAX see below
#define PRIxMAX see below
#define PRIXMAX see below
#define SCNdMAX see below
#define SCNiMAX see below
#define SCNoMAX see below
#define SCNuMAX see below
#define SCNxMAX see below
#define PRIdPTR see below
#define PRIiPTR see below
#define PRIoPTR see below
#define PRIuPTR see below
#define PRIxPTR see below
#define PRIXPTR see below
#define SCNdPTR see below
#define SCNiPTR see below
#define SCNoPTR see below
#define SCNuPTR see below
#define SCNxPTR see below
```

The contents and meaning of the header `<cinttypes>` are the same as the
C standard library header `<inttypes.h>`, with the following changes:

- The header `<cinttypes>` includes the header `<cstdint>` instead of
  `<stdint.h>`, and
- `intmax_t` and `uintmax_t` are not required to be able to represent
  all values of extended integer types wider than `long long` and
  `unsigned long long`, respectively, and
- if and only if the type `intmax_t` designates an extended integer type
  [[basic.fundamental]], the following function signatures are added:
  ``` cpp
  constexpr intmax_t abs(intmax_t);
  constexpr imaxdiv_t div(intmax_t, intmax_t);
  ```

  which shall have the same semantics as the function signatures
  `constexpr intmax_t imaxabs(intmax_t)` and
  `constexpr imaxdiv_t imaxdiv(intmax_t, intmax_t)`, respectively.

See also: ISO C 7.8

Each of the `PRI` macros listed in this subclause is defined if and only
if the implementation defines the corresponding *typedef-name* in 
[[cstdint.syn]]. Each of the `SCN` macros listed in this subclause is
defined if and only if the implementation defines the corresponding
*typedef-name* in  [[cstdint.syn]] and has a suitable `fscanf` length
modifier for the type.

<!-- Link reference definitions -->
[adjustfield.manip]: #adjustfield.manip
[allocator.requirements.general]: library.md#allocator.requirements.general
[basefield.manip]: #basefield.manip
[basic.fundamental]: basic.md#basic.fundamental
[basic.ios.cons]: #basic.ios.cons
[basic.ios.copyfmt]: #basic.ios.copyfmt
[basic.ios.members]: #basic.ios.members
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.main]: basic.md#basic.start.main
[bidirectional.iterators]: iterators.md#bidirectional.iterators
[bitmask.types]: library.md#bitmask.types
[c.files]: #c.files
[char.traits]: strings.md#char.traits
[char.traits.specializations]: strings.md#char.traits.specializations
[character.seq]: library.md#character.seq
[cinttypes.syn]: #cinttypes.syn
[container.requirements.general]: containers.md#container.requirements.general
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[cpp17.equalitycomparable]: #cpp17.equalitycomparable
[cstdint.syn]: support.md#cstdint.syn
[cstdio.syn]: #cstdio.syn
[defns.ntcts]: intro.md#defns.ntcts
[enumerated.types]: library.md#enumerated.types
[error.reporting]: #error.reporting
[ext.manip]: #ext.manip
[file.streams]: #file.streams
[filebuf]: #filebuf
[filebuf.assign]: #filebuf.assign
[filebuf.cons]: #filebuf.cons
[filebuf.general]: #filebuf.general
[filebuf.members]: #filebuf.members
[filebuf.open.modes]: #filebuf.open.modes
[filebuf.seekoff]: #filebuf.seekoff
[filebuf.virtuals]: #filebuf.virtuals
[filesystems]: #filesystems
[floatfield.manip]: #floatfield.manip
[fmtflags.manip]: #fmtflags.manip
[fmtflags.state]: #fmtflags.state
[format.err.report]: utilities.md#format.err.report
[fpos]: #fpos
[fpos.members]: #fpos.members
[fpos.operations]: #fpos.operations
[fs.class.directory.entry]: #fs.class.directory.entry
[fs.class.directory.entry.general]: #fs.class.directory.entry.general
[fs.class.directory.iterator]: #fs.class.directory.iterator
[fs.class.directory.iterator.general]: #fs.class.directory.iterator.general
[fs.class.file.status]: #fs.class.file.status
[fs.class.file.status.general]: #fs.class.file.status.general
[fs.class.filesystem.error]: #fs.class.filesystem.error
[fs.class.filesystem.error.general]: #fs.class.filesystem.error.general
[fs.class.path]: #fs.class.path
[fs.class.path.general]: #fs.class.path.general
[fs.class.rec.dir.itr]: #fs.class.rec.dir.itr
[fs.class.rec.dir.itr.general]: #fs.class.rec.dir.itr.general
[fs.conform.9945]: #fs.conform.9945
[fs.conform.os]: #fs.conform.os
[fs.conformance]: #fs.conformance
[fs.conformance.general]: #fs.conformance.general
[fs.dir.entry.cons]: #fs.dir.entry.cons
[fs.dir.entry.io]: #fs.dir.entry.io
[fs.dir.entry.mods]: #fs.dir.entry.mods
[fs.dir.entry.obs]: #fs.dir.entry.obs
[fs.dir.itr.members]: #fs.dir.itr.members
[fs.dir.itr.nonmembers]: #fs.dir.itr.nonmembers
[fs.enum]: #fs.enum
[fs.enum.copy.opts]: #fs.enum.copy.opts
[fs.enum.dir.opts]: #fs.enum.dir.opts
[fs.enum.file.type]: #fs.enum.file.type
[fs.enum.path.format]: #fs.enum.path.format
[fs.enum.perm.opts]: #fs.enum.perm.opts
[fs.enum.perms]: #fs.enum.perms
[fs.err.report]: #fs.err.report
[fs.file.status.cons]: #fs.file.status.cons
[fs.file.status.mods]: #fs.file.status.mods
[fs.file.status.obs]: #fs.file.status.obs
[fs.filesystem.error.members]: #fs.filesystem.error.members
[fs.filesystem.syn]: #fs.filesystem.syn
[fs.general]: #fs.general
[fs.op.absolute]: #fs.op.absolute
[fs.op.canonical]: #fs.op.canonical
[fs.op.copy]: #fs.op.copy
[fs.op.copy.file]: #fs.op.copy.file
[fs.op.copy.symlink]: #fs.op.copy.symlink
[fs.op.create.dir.symlk]: #fs.op.create.dir.symlk
[fs.op.create.directories]: #fs.op.create.directories
[fs.op.create.directory]: #fs.op.create.directory
[fs.op.create.hard.lk]: #fs.op.create.hard.lk
[fs.op.create.symlink]: #fs.op.create.symlink
[fs.op.current.path]: #fs.op.current.path
[fs.op.equivalent]: #fs.op.equivalent
[fs.op.exists]: #fs.op.exists
[fs.op.file.size]: #fs.op.file.size
[fs.op.funcs]: #fs.op.funcs
[fs.op.funcs.general]: #fs.op.funcs.general
[fs.op.hard.lk.ct]: #fs.op.hard.lk.ct
[fs.op.is.block.file]: #fs.op.is.block.file
[fs.op.is.char.file]: #fs.op.is.char.file
[fs.op.is.directory]: #fs.op.is.directory
[fs.op.is.empty]: #fs.op.is.empty
[fs.op.is.fifo]: #fs.op.is.fifo
[fs.op.is.other]: #fs.op.is.other
[fs.op.is.regular.file]: #fs.op.is.regular.file
[fs.op.is.socket]: #fs.op.is.socket
[fs.op.is.symlink]: #fs.op.is.symlink
[fs.op.last.write.time]: #fs.op.last.write.time
[fs.op.permissions]: #fs.op.permissions
[fs.op.proximate]: #fs.op.proximate
[fs.op.read.symlink]: #fs.op.read.symlink
[fs.op.relative]: #fs.op.relative
[fs.op.remove]: #fs.op.remove
[fs.op.remove.all]: #fs.op.remove.all
[fs.op.rename]: #fs.op.rename
[fs.op.resize.file]: #fs.op.resize.file
[fs.op.space]: #fs.op.space
[fs.op.status]: #fs.op.status
[fs.op.status.known]: #fs.op.status.known
[fs.op.symlink.status]: #fs.op.symlink.status
[fs.op.temp.dir.path]: #fs.op.temp.dir.path
[fs.op.weakly.canonical]: #fs.op.weakly.canonical
[fs.path.append]: #fs.path.append
[fs.path.assign]: #fs.path.assign
[fs.path.compare]: #fs.path.compare
[fs.path.concat]: #fs.path.concat
[fs.path.construct]: #fs.path.construct
[fs.path.cvt]: #fs.path.cvt
[fs.path.decompose]: #fs.path.decompose
[fs.path.fmt.cvt]: #fs.path.fmt.cvt
[fs.path.gen]: #fs.path.gen
[fs.path.generic]: #fs.path.generic
[fs.path.generic.obs]: #fs.path.generic.obs
[fs.path.hash]: #fs.path.hash
[fs.path.io]: #fs.path.io
[fs.path.itr]: #fs.path.itr
[fs.path.member]: #fs.path.member
[fs.path.modifiers]: #fs.path.modifiers
[fs.path.native.obs]: #fs.path.native.obs
[fs.path.nonmember]: #fs.path.nonmember
[fs.path.query]: #fs.path.query
[fs.path.req]: #fs.path.req
[fs.path.type.cvt]: #fs.path.type.cvt
[fs.race.behavior]: #fs.race.behavior
[fs.rec.dir.itr.members]: #fs.rec.dir.itr.members
[fs.rec.dir.itr.nonmembers]: #fs.rec.dir.itr.nonmembers
[fs.req]: #fs.req
[fstream]: #fstream
[fstream.cons]: #fstream.cons
[fstream.general]: #fstream.general
[fstream.members]: #fstream.members
[fstream.swap]: #fstream.swap
[fstream.syn]: #fstream.syn
[ifstream]: #ifstream
[ifstream.cons]: #ifstream.cons
[ifstream.general]: #ifstream.general
[ifstream.members]: #ifstream.members
[ifstream.swap]: #ifstream.swap
[input.iterators]: iterators.md#input.iterators
[input.output]: #input.output
[input.output.general]: #input.output.general
[input.streams]: #input.streams
[input.streams.general]: #input.streams.general
[intro.multithread]: basic.md#intro.multithread
[intro.races]: basic.md#intro.races
[iomanip.syn]: #iomanip.syn
[ios]: #ios
[ios.base]: #ios.base
[ios.base.callback]: #ios.base.callback
[ios.base.cons]: #ios.base.cons
[ios.base.general]: #ios.base.general
[ios.base.locales]: #ios.base.locales
[ios.base.storage]: #ios.base.storage
[ios.failure]: #ios.failure
[ios.fmtflags]: #ios.fmtflags
[ios.fmtflags.const]: #ios.fmtflags.const
[ios.init]: #ios.init
[ios.iostate]: #ios.iostate
[ios.members.static]: #ios.members.static
[ios.openmode]: #ios.openmode
[ios.overview]: #ios.overview
[ios.seekdir]: #ios.seekdir
[ios.syn]: #ios.syn
[ios.types]: #ios.types
[iosfwd.syn]: #iosfwd.syn
[iostate.flags]: #iostate.flags
[iostream.assign]: #iostream.assign
[iostream.cons]: #iostream.cons
[iostream.dest]: #iostream.dest
[iostream.format]: #iostream.format
[iostream.forward]: #iostream.forward
[iostream.forward.overview]: #iostream.forward.overview
[iostream.limits.imbue]: #iostream.limits.imbue
[iostream.objects]: #iostream.objects
[iostream.objects.overview]: #iostream.objects.overview
[iostream.syn]: #iostream.syn
[iostreamclass]: #iostreamclass
[iostreamclass.general]: #iostreamclass.general
[iostreams.base]: #iostreams.base
[iostreams.limits.pos]: #iostreams.limits.pos
[iostreams.requirements]: #iostreams.requirements
[iostreams.summary]: #iostreams.summary
[iostreams.threadsafety]: #iostreams.threadsafety
[ispanstream]: #ispanstream
[ispanstream.cons]: #ispanstream.cons
[ispanstream.general]: #ispanstream.general
[ispanstream.members]: #ispanstream.members
[ispanstream.swap]: #ispanstream.swap
[istream]: #istream
[istream.assign]: #istream.assign
[istream.cons]: #istream.cons
[istream.extractors]: #istream.extractors
[istream.formatted]: #istream.formatted
[istream.formatted.arithmetic]: #istream.formatted.arithmetic
[istream.formatted.reqmts]: #istream.formatted.reqmts
[istream.general]: #istream.general
[istream.manip]: #istream.manip
[istream.rvalue]: #istream.rvalue
[istream.sentry]: #istream.sentry
[istream.syn]: #istream.syn
[istream.unformatted]: #istream.unformatted
[istringstream]: #istringstream
[istringstream.cons]: #istringstream.cons
[istringstream.general]: #istringstream.general
[istringstream.members]: #istringstream.members
[istringstream.swap]: #istringstream.swap
[lex.charset]: lex.md#lex.charset
[locale.codecvt.virtuals]: localization.md#locale.codecvt.virtuals
[locale.num.get]: localization.md#locale.num.get
[namespace.std]: library.md#namespace.std
[narrow.stream.objects]: #narrow.stream.objects
[numeric.limits]: support.md#numeric.limits
[ofstream]: #ofstream
[ofstream.cons]: #ofstream.cons
[ofstream.general]: #ofstream.general
[ofstream.members]: #ofstream.members
[ofstream.swap]: #ofstream.swap
[ospanstream]: #ospanstream
[ospanstream.cons]: #ospanstream.cons
[ospanstream.general]: #ospanstream.general
[ospanstream.members]: #ospanstream.members
[ospanstream.swap]: #ospanstream.swap
[ostream]: #ostream
[ostream.assign]: #ostream.assign
[ostream.cons]: #ostream.cons
[ostream.formatted]: #ostream.formatted
[ostream.formatted.print]: #ostream.formatted.print
[ostream.formatted.reqmts]: #ostream.formatted.reqmts
[ostream.general]: #ostream.general
[ostream.inserters]: #ostream.inserters
[ostream.inserters.arithmetic]: #ostream.inserters.arithmetic
[ostream.inserters.character]: #ostream.inserters.character
[ostream.manip]: #ostream.manip
[ostream.rvalue]: #ostream.rvalue
[ostream.seeks]: #ostream.seeks
[ostream.sentry]: #ostream.sentry
[ostream.syn]: #ostream.syn
[ostream.unformatted]: #ostream.unformatted
[ostringstream]: #ostringstream
[ostringstream.cons]: #ostringstream.cons
[ostringstream.general]: #ostringstream.general
[ostringstream.members]: #ostringstream.members
[ostringstream.swap]: #ostringstream.swap
[output.streams]: #output.streams
[output.streams.general]: #output.streams.general
[print.fun]: #print.fun
[print.syn]: #print.syn
[quoted.manip]: #quoted.manip
[res.on.data.races]: library.md#res.on.data.races
[res.on.exception.handling]: library.md#res.on.exception.handling
[span.streams]: #span.streams
[span.streams.overview]: #span.streams.overview
[spanbuf]: #spanbuf
[spanbuf.assign]: #spanbuf.assign
[spanbuf.cons]: #spanbuf.cons
[spanbuf.general]: #spanbuf.general
[spanbuf.members]: #spanbuf.members
[spanbuf.virtuals]: #spanbuf.virtuals
[spanstream]: #spanstream
[spanstream.cons]: #spanstream.cons
[spanstream.general]: #spanstream.general
[spanstream.members]: #spanstream.members
[spanstream.swap]: #spanstream.swap
[spanstream.syn]: #spanstream.syn
[sstream.syn]: #sstream.syn
[std.ios.manip]: #std.ios.manip
[std.manip]: #std.manip
[std.modules]: library.md#std.modules
[stream.buffers]: #stream.buffers
[stream.types]: #stream.types
[streambuf]: #streambuf
[streambuf.assign]: #streambuf.assign
[streambuf.buffer]: #streambuf.buffer
[streambuf.cons]: #streambuf.cons
[streambuf.general]: #streambuf.general
[streambuf.get.area]: #streambuf.get.area
[streambuf.locales]: #streambuf.locales
[streambuf.members]: #streambuf.members
[streambuf.protected]: #streambuf.protected
[streambuf.pub.get]: #streambuf.pub.get
[streambuf.pub.pback]: #streambuf.pub.pback
[streambuf.pub.put]: #streambuf.pub.put
[streambuf.put.area]: #streambuf.put.area
[streambuf.reqts]: #streambuf.reqts
[streambuf.syn]: #streambuf.syn
[streambuf.virt.buffer]: #streambuf.virt.buffer
[streambuf.virt.get]: #streambuf.virt.get
[streambuf.virt.locales]: #streambuf.virt.locales
[streambuf.virt.pback]: #streambuf.virt.pback
[streambuf.virt.put]: #streambuf.virt.put
[streambuf.virtuals]: #streambuf.virtuals
[string.classes]: strings.md#string.classes
[string.streams]: #string.streams
[stringbuf]: #stringbuf
[stringbuf,filebuf]: #stringbuf,filebuf
[stringbuf.assign]: #stringbuf.assign
[stringbuf.cons]: #stringbuf.cons
[stringbuf.general]: #stringbuf.general
[stringbuf.members]: #stringbuf.members
[stringbuf.seekoff.newoff]: #stringbuf.seekoff.newoff
[stringbuf.seekoff.pos]: #stringbuf.seekoff.pos
[stringbuf.virtuals]: #stringbuf.virtuals
[stringbuf.virtuals,filebuf.virtuals]: #stringbuf.virtuals,filebuf.virtuals
[strings]: strings.md#strings
[stringstream]: #stringstream
[stringstream.cons]: #stringstream.cons
[stringstream.general]: #stringstream.general
[stringstream.members]: #stringstream.members
[stringstream.swap]: #stringstream.swap
[syncstream]: #syncstream
[syncstream.osyncstream]: #syncstream.osyncstream
[syncstream.osyncstream.cons]: #syncstream.osyncstream.cons
[syncstream.osyncstream.members]: #syncstream.osyncstream.members
[syncstream.osyncstream.overview]: #syncstream.osyncstream.overview
[syncstream.syn]: #syncstream.syn
[syncstream.syncbuf]: #syncstream.syncbuf
[syncstream.syncbuf.assign]: #syncstream.syncbuf.assign
[syncstream.syncbuf.cons]: #syncstream.syncbuf.cons
[syncstream.syncbuf.members]: #syncstream.syncbuf.members
[syncstream.syncbuf.overview]: #syncstream.syncbuf.overview
[syncstream.syncbuf.special]: #syncstream.syncbuf.special
[syncstream.syncbuf.virtuals]: #syncstream.syncbuf.virtuals
[temp.deduct]: temp.md#temp.deduct
[term.unevaluated.operand]: expr.md#term.unevaluated.operand
[views.span]: containers.md#views.span
[wide.stream.objects]: #wide.stream.objects

[^1]: Typically `long long`.

[^2]: Most places where `streamsize` is used would use `size_t` in ISO
    C, or `ssize_t` in POSIX.

[^3]: It is the implementation’s responsibility to implement headers so
    that including `<iosfwd>` and other headers does not violate the
    rules about multiple occurrences of default arguments.

[^4]: Constructors and destructors for objects with static storage
    duration can access these objects to read input from `stdin` or
    write output to `stdout` or `stderr`.

[^5]: This implies that operations on a standard iostream object can be
    mixed arbitrarily with operations on the corresponding stdio stream.
    In practical terms, synchronization usually means that a standard
    iostream object and a standard stdio object share a buffer.

[^6]: An implementation is free to implement both the integer array
    pointed at by `iarray` and the pointer array pointed at by `parray`
    as sparse data structures, possibly with a one-element cache for
    each.

[^7]: For example, because it cannot allocate space.

[^8]: For example, because it cannot allocate space.

[^9]: This suggests an infinite amount of copying, but the
    implementation can keep track of the maximum element of the arrays
    that is nonzero.

[^10]: Checking `badbit` also for `fail()` is historical practice.

[^11]: The function signature `dec(ios_base&)` can be called by the
    function signature
    `basic_ostream& stream::operator<<(ios_base& (*)(ios_base&))` to
    permit expressions of the form `cout << dec` to change the format
    flags stored in `cout`.

[^12]: The default constructor is protected for class `basic_streambuf`
    to assure that only objects for classes derived from this class can
    be constructed.

[^13]: The morphemes of `showmanyc` are “es-how-many-see”, not
    “show-manic”.

[^14]: `underflow` or `uflow` can fail by throwing an exception
    prematurely. The intention is not only that the calls will not
    return `eof()` but that they will return “immediately”.

[^15]: Classes derived from `basic_streambuf` can provide more efficient
    ways to implement `xsgetn()` and `xsputn()` by overriding these
    definitions from the base class.

[^16]: That is, for each class derived from a specialization of
    `basic_streambuf` in this Clause@@REF:stringbuf,filebuf@@, a
    specification of how consuming a character effects the associated
    output sequence is given. There is no requirement on a
    program-defined class.

[^17]: Typically, `overflow` returns `c` to indicate success, except
    when `traits::eq_int_type(c, traits::eof())` returns `true`, in
    which case it returns `traits::not_eof(c)`.

[^18]: This will be possible only in functions that are part of the
    library. The semantics of the constructor used in user code is as
    specified.

[^19]: The `sentry` constructor and destructor can also perform
    additional implementation-dependent operations.

[^20]: See, for example, the function signature
    `ws(basic_istream&)`@@REF:istream.manip@@.

[^21]: See, for example, the function signature
    `dec(ios_base&)`@@REF:basefield.manip@@.

[^22]: Note that this function is not overloaded on types `signed char`
    and `unsigned char`.

[^23]: Note that this function is not overloaded on types `signed char`
    and `unsigned char`.

[^24]: Note that this function is not overloaded on types `signed char`
    and `unsigned char`.

[^25]: Since the final input character is “extracted”, it is counted in
    the `gcount()`, even though it is not stored.

[^26]: This allows an input line which exactly fills the buffer, without
    setting `failbit`. This is different behavior than the historical
    AT&T implementation.

[^27]: This implies an empty input line will not cause `failbit` to be
    set.

[^28]: Note that this function is not overloaded on types `signed char`
    and `unsigned char`.

[^29]: The call `os.tie()->flush()` does not necessarily occur if the
    function can determine that no synchronization is necessary.

[^30]: The `sentry` constructor and destructor can also perform
    additional implementation-dependent operations.

[^31]: This is done without causing an `ios_base::failure` to be thrown.

[^32]: See, for example, the function signature
    `endl(basic_ostream&)`@@REF:ostream.manip@@.

[^33]: See, for example, the function signature
    `dec(ios_base&)`@@REF:basefield.manip@@.

[^34]: This is done without causing an `ios_base::failure` to be thrown.

[^35]: Note that this function is not overloaded on types `signed char`
    and `unsigned char`.

[^36]: Note that this function is not overloaded on types `signed char`
    and `unsigned char`.

[^37]: The expression `cin >> resetiosflags(ios_base::skipws)` clears
    `ios_base::skipws` in the format flags stored in the
    `basic_istream<charT, traits>` object `cin` (the same as
    `cin >> noskipws`), and the expression
    `cout << resetiosflags(ios_base::showbase)` clears
    `ios_base::showbase` in the format flags stored in the
    `basic_ostream<charT, traits>` object `cout` (the same as
    `cout << noshowbase`).

[^38]: The macro `SEEK_END` is defined, and the function signatures
    `fopen(const char*, const char*)` and `fseek(FILE*, long, int)` are
    declared, in `<cstdio>`.
