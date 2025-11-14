# Strings library <a id="strings">[[strings]]</a>

## General <a id="strings.general">[[strings.general]]</a>

This Clause describes components for manipulating sequences of any
non-array POD ([[basic.types]]) type. In this Clause such types are
called *char-like types*, and objects of char-like types are called
*char-like objects* or simply *characters*.

The following subclauses describe a character traits class, a string
class, and null-terminated sequence utilities, as summarized in Table 
[[tab:strings.lib.summary]].

**Table: Strings library summary**

| Subclause          |                                    | Header      |
| ------------------ | ---------------------------------- | ----------- |
| [[char.traits]]    | Character traits                   | `<string>`  |
| [[string.classes]] | String classes                     | `<string>`  |
|                    |                                    | `<cctype>`  |
|                    |                                    | `<cwctype>` |
| [[c.strings]]      | Null-terminated sequence utilities | `<cstring>` |
|                    |                                    | `<cwchar>`  |
|                    |                                    | `<cstdlib>` |
|                    |                                    | `<cuchar>`  |


## Character traits <a id="char.traits">[[char.traits]]</a>

This subclause defines requirements on classes representing *character
traits*, and defines a class template `char_traits<charT>`, along with
four specializations, `char_traits<char>`, `char_traits<char16_t>`,  
`char_traits<char32_t>`, and `char_traits<wchar_t>`, that satisfy those
requirements.

Most classes specified in Clauses  [[string.classes]] and 
[[input.output]] need a set of related types and functions to complete
the definition of their semantics. These types and functions are
provided as a set of member typedefs and functions in the template
parameter ‘traits’ used by each such template. This subclause defines
the semantics of these members.

To specialize those templates to generate a string or iostream class to
handle a particular character container type `CharT`, that and its
related character traits class `Traits` are passed as a pair of
parameters to the string or iostream template as parameters `charT` and
`traits`. `Traits::char_type` shall be the same as `CharT`.

This subclause specifies a struct template, `char_traits<charT>`, and
four explicit specializations of it, `char_traits<{}char>`,
`char_traits<char16_t>`, `char_traits<char32_t>`, and
`char_traits<wchar_t>`, all of which appear in the header `<string>` and
satisfy the requirements below.

### Character traits requirements <a id="char.traits.require">[[char.traits.require]]</a>

In Table  [[tab:char.traits.require]], `X` denotes a Traits class
defining types and functions for the character container type `CharT`;
`c` and `d` denote values of type `CharT`; `p` and `q` denote values of
type `const CharT*`; `s` denotes a value of type `CharT*`; `n`, `i` and
`j` denote values of type `std::size_t`; `e` and `f` denote values of
type `X::int_type`; `pos` denotes a value of type `X::pos_type`; `state`
denotes a value of type `X::state_type`; and `r` denotes an lvalue of
type `CharT`. Operations on Traits shall not throw exceptions.

The struct template

``` cpp
template<class charT> struct char_traits;
```

shall be provided in the header `<string>` as a basis for explicit
specializations.

### traits typedefs <a id="char.traits.typedefs">[[char.traits.typedefs]]</a>

``` cpp
typedef CHAR_T char_type;
```

The type `char_type` is used to refer to the character container type in
the implementation of the library classes defined in  [[string.classes]]
and Clause  [[input.output]].

``` cpp
typedef INT_T int_type;
```

*Requires:* For a certain character container type `char_type`, a
related container type `INT_T` shall be a type or class which can
represent all of the valid characters converted from the corresponding
`char_type` values, as well as an end-of-file value, `eof()`. The type
`int_type` represents a character container type which can hold
end-of-file to be used as a return type of the iostream class member
functions.[^1]

``` cpp
typedef implementation-defined off_type;
typedef implementation-defined pos_type;
```

*Requires:* Requirements for `off_type` and `pos_type` are described
in  [[iostreams.limits.pos]] and [[iostream.forward]].

``` cpp
typedef STATE_T state_type;
```

*Requires:* `state_type` shall meet the requirements of `CopyAssignable`
(Table  [[copyassignable]]), `CopyConstructible`
(Table  [[copyconstructible]]), and `DefaultConstructible`
(Table  [[defaultconstructible]]) types.

### `char_traits` specializations <a id="char.traits.specializations">[[char.traits.specializations]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char>;
  template<> struct char_traits<char16_t>;
  template<> struct char_traits<char32_t>;
  template<> struct char_traits<wchar_t>;
}
```

The header `<string>` shall define four specializations of the template
struct `char_traits`: `char_traits<{}char>`, `char_traits<char16_t>`,
`char_traits<char32_t>`, and `char_traits<wchar_t>`.

The requirements for the members of these specializations are given in
Clause  [[char.traits.require]].

#### `struct char_traits<char>` <a id="char.traits.specializations.char">[[char.traits.specializations.char]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char> {
    typedef char        char_type;
    typedef int         int_type;
    typedef streamoff   off_type;
    typedef streampos   pos_type;
    typedef mbstate_t   state_type;

    static void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static int compare(const char_type* s1, const char_type* s2, size_t n);
    static size_t length(const char_type* s);
    static const char_type* find(const char_type* s, size_t n,
                 const char_type& a);
    static char_type* move(char_type* s1, const char_type* s2, size_t n);
    static char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The defined types for `int_type`, `pos_type`, `off_type`, and
`state_type` shall be `int`, `streampos`, `streamoff`, and `mbstate_t`
respectively.

The type `streampos` shall be an *implementation-defined* type that
satisfies the requirements for `pos_type` in  [[iostreams.limits.pos]]
and [[iostream.forward]].

The type `streamoff` shall be an *implementation-defined* type that
satisfies the requirements for `off_type` in  [[iostreams.limits.pos]]
and [[iostream.forward]].

The type `mbstate_t` is defined in `<cwchar>` and can represent any of
the conversion states that can occur in an *implementation-defined* set
of supported multibyte character encoding rules.

The two-argument member `assign` shall be defined identically to the
built-in operator `=`. The two-argument members `eq` and `lt` shall be
defined identically to the built-in operators `==` and `<` for type
`unsigned` `char`.

The member `eof()` shall return `EOF`.

#### `struct char_traits<char16_t>` <a id="char.traits.specializations.char16_t">[[char.traits.specializations.char16_t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char16_t> {
    typedef char16_t        char_type;
    typedef uint_least16_t  int_type;
    typedef streamoff       off_type;
    typedef u16streampos    pos_type;
    typedef mbstate_t       state_type;

    static void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static int compare(const char_type* s1, const char_type* s2, size_t n);
    static size_t length(const char_type* s);
    static const char_type* find(const char_type* s, size_t n,
                                 const char_type& a);
    static char_type* move(char_type* s1, const char_type* s2, size_t n);
    static char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The type `u16streampos` shall be an *implementation-defined* type that
satisfies the requirements for pos_type in  [[iostreams.limits.pos]] and
[[iostream.forward]].

The two-argument members `assign`, `eq`, and `lt` shall be defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` shall return an *implementation-defined* constant
that cannot appear as a valid UTF-16 code unit.

#### `struct char_traits<char32_t>` <a id="char.traits.specializations.char32_t">[[char.traits.specializations.char32_t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char32_t> {
    typedef char32_t        char_type;
    typedef uint_least32_t  int_type;
    typedef streamoff       off_type;
    typedef u32streampos    pos_type;
    typedef mbstate_t       state_type;

    static void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static int compare(const char_type* s1, const char_type* s2, size_t n);
    static size_t length(const char_type* s);
    static const char_type* find(const char_type* s, size_t n,
                 const char_type& a);
    static char_type* move(char_type* s1, const char_type* s2, size_t n);
    static char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The type `u32streampos` shall be an *implementation-defined* type that
satisfies the requirements for pos_type in  [[iostreams.limits.pos]] and
[[iostream.forward]].

The two-argument members `assign`, `eq`, and `lt` shall be defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` shall return an *implementation-defined* constant
that cannot appear as a Unicode code point.

#### `struct char_traits<wchar_t>` <a id="char.traits.specializations.wchar.t">[[char.traits.specializations.wchar.t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<wchar_t> {
    typedef wchar_t      char_type;
    typedef wint_t       int_type;
    typedef streamoff    off_type;
    typedef wstreampos   pos_type;
    typedef mbstate_t    state_type;

    static void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static int compare(const char_type* s1, const char_type* s2, size_t n);
    static size_t length(const char_type* s);
    static const char_type* find(const char_type* s, size_t n,
                 const char_type& a);
    static char_type* move(char_type* s1, const char_type* s2, size_t n);
    static char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The defined types for `int_type`, `pos_type`, and `state_type` shall be
`wint_t`, `wstreampos`, and `mbstate_t` respectively.

The type `wstreampos` shall be an *implementation-defined* type that
satisfies the requirements for pos_type in  [[iostreams.limits.pos]] and
[[iostream.forward]].

The type `mbstate_t` is defined in `<cwchar>` and can represent any of
the conversion states that can occur in an *implementation-defined* set
of supported multibyte character encoding rules.

The two-argument members `assign`, `eq`, and `lt` shall be defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` shall return `WEOF`.

## String classes <a id="string.classes">[[string.classes]]</a>

The header `<string>` defines the `basic_string` class template for
manipulating varying-length sequences of char-like objects and four
typedefs, `string`, `u16string`, `u32string`, and `wstring`, that name
the specializations `basic_string<char>`, `basic_string<char16_t>`,
`basic_string<char32_t>`, and `basic_string<{}wchar_t>`, respectively.

``` cpp
#include <initializer_list>

namespace std {

  // [char.traits], character traits:
  template<class charT> struct char_traits;
  template <> struct char_traits<char>;
  template <> struct char_traits<char16_t>;
  template <> struct char_traits<char32_t>;
  template <> struct char_traits<wchar_t>;

  // [basic.string], basic_string:
  template<class charT, class traits = char_traits<charT>,
    class Allocator = allocator<charT> >
      class basic_string;

  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(const basic_string<charT,traits,Allocator>& lhs,
                const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(basic_string<charT,traits,Allocator>&& lhs,
                const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(const basic_string<charT,traits,Allocator>& lhs,
                basic_string<charT,traits,Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(basic_string<charT,traits,Allocator>&& lhs,
                basic_string<charT,traits,Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(const charT* lhs,
                const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(const charT* lhs,
                basic_string<charT,traits,Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(charT lhs, const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(charT lhs, basic_string<charT,traits,Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(const basic_string<charT,traits,Allocator>& lhs,
                const charT* rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(basic_string<charT,traits,Allocator>&& lhs,
                const charT* rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(const basic_string<charT,traits,Allocator>& lhs, charT rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT,traits,Allocator>
      operator+(basic_string<charT,traits,Allocator>&& lhs, charT rhs);

  template<class charT, class traits, class Allocator>
    bool operator==(const basic_string<charT,traits,Allocator>& lhs,
                    const basic_string<charT,traits,Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator==(const charT* lhs,
                    const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator==(const basic_string<charT,traits,Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator!=(const basic_string<charT,traits,Allocator>& lhs,
                    const basic_string<charT,traits,Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator!=(const charT* lhs,
                    const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator!=(const basic_string<charT,traits,Allocator>& lhs,
                    const charT* rhs);

  template<class charT, class traits, class Allocator>
    bool operator< (const basic_string<charT,traits,Allocator>& lhs,
                    const basic_string<charT,traits,Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator< (const basic_string<charT,traits,Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator< (const charT* lhs,
                    const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator> (const basic_string<charT,traits,Allocator>& lhs,
                    const basic_string<charT,traits,Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator> (const basic_string<charT,traits,Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator> (const charT* lhs,
                    const basic_string<charT,traits,Allocator>& rhs);

  template<class charT, class traits, class Allocator>
    bool operator<=(const basic_string<charT,traits,Allocator>& lhs,
                    const basic_string<charT,traits,Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator<=(const basic_string<charT,traits,Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator<=(const charT* lhs,
                    const basic_string<charT,traits,Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator>=(const basic_string<charT,traits,Allocator>& lhs,
                    const basic_string<charT,traits,Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator>=(const basic_string<charT,traits,Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator>=(const charT* lhs,
                    const basic_string<charT,traits,Allocator>& rhs);

  // [string.special], swap:
  template<class charT, class traits, class Allocator>
    void swap(basic_string<charT,traits,Allocator>& lhs,
      basic_string<charT,traits,Allocator>& rhs);

  // [string.io], inserters and extractors:
  template<class charT, class traits, class Allocator>
    basic_istream<charT,traits>&
      operator>>(basic_istream<charT,traits>& is,
                 basic_string<charT,traits,Allocator>& str);
  template<class charT, class traits, class Allocator>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os,
                 const basic_string<charT,traits,Allocator>& str);
  template<class charT, class traits, class Allocator>
    basic_istream<charT,traits>&
      getline(basic_istream<charT,traits>& is,
              basic_string<charT,traits,Allocator>& str,
              charT delim);
  template<class charT, class traits, class Allocator>
    basic_istream<charT,traits>&
      getline(basic_istream<charT,traits>&& is,
              basic_string<charT,traits,Allocator>& str,
              charT delim);
  template<class charT, class traits, class Allocator>
    basic_istream<charT,traits>&
      getline(basic_istream<charT,traits>& is,
              basic_string<charT,traits,Allocator>& str);
  template<class charT, class traits, class Allocator>
    basic_istream<charT,traits>&
      getline(basic_istream<charT,traits>&& is,
              basic_string<charT,traits,Allocator>& str);

  // basic_string typedef names
  typedef basic_string<char> string;
  typedef basic_string<char16_t> u16string;
  typedef basic_string<char32_t> u32string;
  typedef basic_string<wchar_t> wstring;

  // [string.conversions], numeric conversions:
  int stoi(const string& str, size_t* idx = 0, int base = 10);
  long stol(const string& str, size_t* idx = 0, int base = 10);
  unsigned long stoul(const string& str, size_t* idx = 0, int base = 10);
  long long stoll(const string& str, size_t* idx = 0, int base = 10);
  unsigned long long stoull(const string& str, size_t* idx = 0, int base = 10);
  float stof(const string& str, size_t* idx = 0);
  double stod(const string& str, size_t* idx = 0);
  long double stold(const string& str, size_t* idx = 0);
  string to_string(int val);
  string to_string(unsigned val);
  string to_string(long val);
  string to_string(unsigned long val);
  string to_string(long long val);
  string to_string(unsigned long long val);
  string to_string(float val);
  string to_string(double val);
  string to_string(long double val);

  int stoi(const wstring& str, size_t* idx = 0, int base = 10);
  long stol(const wstring& str, size_t* idx = 0, int base = 10);
  unsigned long stoul(const wstring& str, size_t* idx = 0, int base = 10);
  long long stoll(const wstring& str, size_t* idx = 0, int base = 10);
  unsigned long long stoull(const wstring& str, size_t* idx = 0, int base = 10);
  float stof(const wstring& str, size_t* idx = 0);
  double stod(const wstring& str, size_t* idx = 0);
  long double stold(const wstring& str, size_t* idx = 0);
  wstring to_wstring(int val);
  wstring to_wstring(unsigned val);
  wstring to_wstring(long val);
  wstring to_wstring(unsigned long val);
  wstring to_wstring(long long val);
  wstring to_wstring(unsigned long long val);
  wstring to_wstring(float val);
  wstring to_wstring(double val);
  wstring to_wstring(long double val);

  // [basic.string.hash], hash support:
  template <class T> struct hash;
  template <> struct hash<string>;
  template <> struct hash<u16string>;
  template <> struct hash<u32string>;
  template <> struct hash<wstring>;

inline namespace literals {
inline namespace string_literals {

  // [basic.string.literals], suffix for basic_string literals:
  string    operator "" s(const char* str, size_t len);
  u16string operator "" s(const char16_t* str, size_t len);
  u32string operator "" s(const char32_t* str, size_t len);
  wstring   operator "" s(const wchar_t* str, size_t len);

}
}
}
```

## Class template `basic_string` <a id="basic.string">[[basic.string]]</a>

The class template `basic_string` describes objects that can store a
sequence consisting of a varying number of arbitrary char-like objects
with the first element of the sequence at position zero. Such a sequence
is also called a “string” if the type of the char-like objects that it
holds is clear from context. In the rest of this Clause, the type of the
char-like objects held in a `basic_string` object is designated by
`charT`.

The member functions of `basic_string` use an object of the `Allocator`
class passed as a template parameter to allocate and free storage for
the contained char-like objects.[^2]

The iterators supported by `basic_string` are random access iterators (
[[random.access.iterators]]).

In all cases, `size() <= capacity()`.

The functions described in this Clause can report two kinds of errors,
each associated with an exception type:

- a *length* error is associated with exceptions of type
  `length_error` ([[length.error]]);
- an *out-of-range* error is associated with exceptions of type
  `out_of_range` ([[out.of.range]]).

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
    class Allocator = allocator<charT> >
  class basic_string {
  public:
    // types:
    typedef          traits                                         traits_type;
    typedef typename traits::char_type                              value_type;
    typedef          Allocator                                      allocator_type;
    typedef typename allocator_traits<Allocator>::size_type         size_type;
    typedef typename allocator_traits<Allocator>::difference_type   difference_type;

    typedef value_type& reference;
    typedef const value_type&   const_reference;
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;

    typedef implementation-defined              iterator;       // See [container.requirements]
    typedef implementation-defined              const_iterator; // See [container.requirements]
    typedef std::reverse_iterator<iterator> reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
    static const size_type npos = -1;

    // [string.cons], construct/copy/destroy:
    basic_string() : basic_string(Allocator()) { }
    explicit basic_string(const Allocator& a);
    basic_string(const basic_string& str);
    basic_string(basic_string&& str) noexcept;
    basic_string(const basic_string& str, size_type pos, size_type n = npos,
                 const Allocator& a = Allocator());
    basic_string(const charT* s,
                 size_type n, const Allocator& a = Allocator());
    basic_string(const charT* s, const Allocator& a = Allocator());
    basic_string(size_type n, charT c, const Allocator& a = Allocator());
    template<class InputIterator>
      basic_string(InputIterator begin, InputIterator end,
                   const Allocator& a = Allocator());
    basic_string(initializer_list<charT>, const Allocator& = Allocator());
    basic_string(const basic_string&, const Allocator&);
    basic_string(basic_string&&, const Allocator&);

   ~basic_string();
    basic_string& operator=(const basic_string& str);
    basic_string& operator=(basic_string&& str) noexcept;
    basic_string& operator=(const charT* s);
    basic_string& operator=(charT c);
    basic_string& operator=(initializer_list<charT>);

    // [string.iterators], iterators:
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;

    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // [string.capacity], capacity:
    size_type size() const noexcept;
    size_type length() const noexcept;
    size_type max_size() const noexcept;
    void resize(size_type n, charT c);
    void resize(size_type n);
    size_type capacity() const noexcept;
    void reserve(size_type res_arg = 0);
    void shrink_to_fit();
    void clear() noexcept;
    bool empty() const noexcept;

    // [string.access], element access:
    const_reference operator[](size_type pos) const;
    reference       operator[](size_type pos);
    const_reference at(size_type n) const;
    reference       at(size_type n);

    const charT& front() const;
    charT& front();
    const charT& back() const;
    charT& back();

    // [string.modifiers], modifiers:
    basic_string& operator+=(const basic_string& str);
    basic_string& operator+=(const charT* s);
    basic_string& operator+=(charT c);
    basic_string& operator+=(initializer_list<charT>);
    basic_string& append(const basic_string& str);
    basic_string& append(const basic_string& str, size_type pos,
                         size_type n = npos);
    basic_string& append(const charT* s, size_type n);
    basic_string& append(const charT* s);
    basic_string& append(size_type n, charT c);
    template<class InputIterator>
      basic_string& append(InputIterator first, InputIterator last);
    basic_string& append(initializer_list<charT>);
    void push_back(charT c);

    basic_string& assign(const basic_string& str);
    basic_string& assign(basic_string&& str) noexcept;
    basic_string& assign(const basic_string& str, size_type pos,
                         size_type n = npos);
    basic_string& assign(const charT* s, size_type n);
    basic_string& assign(const charT* s);
    basic_string& assign(size_type n, charT c);
    template<class InputIterator>
      basic_string& assign(InputIterator first, InputIterator last);
    basic_string& assign(initializer_list<charT>);

    basic_string& insert(size_type pos1, const basic_string& str);
    basic_string& insert(size_type pos1, const basic_string& str,
                         size_type pos2, size_type n = npos);
    basic_string& insert(size_type pos, const charT* s, size_type n);
    basic_string& insert(size_type pos, const charT* s);
    basic_string& insert(size_type pos, size_type n, charT c);
    iterator insert(const_iterator p, charT c);
    iterator insert(const_iterator p, size_type n, charT c);
    template<class InputIterator>
      iterator insert(const_iterator p, InputIterator first, InputIterator last);
    iterator insert(const_iterator p, initializer_list<charT>);

    basic_string& erase(size_type pos = 0, size_type n = npos);
    iterator erase(const_iterator p);
    iterator erase(const_iterator first, const_iterator last);

    void pop_back();

    basic_string& replace(size_type pos1, size_type n1,
                          const basic_string& str);
    basic_string& replace(size_type pos1, size_type n1,
                          const basic_string& str,
                          size_type pos2, size_type n2 = npos);
    basic_string& replace(size_type pos, size_type n1, const charT* s,
                          size_type n2);
    basic_string& replace(size_type pos, size_type n1, const charT* s);
    basic_string& replace(size_type pos, size_type n1, size_type n2,
                          charT c);

    basic_string& replace(const_iterator i1, const_iterator i2,
              const basic_string& str);
    basic_string& replace(const_iterator i1, const_iterator i2, const charT* s,
                          size_type n);
    basic_string& replace(const_iterator i1, const_iterator i2, const charT* s);
    basic_string& replace(const_iterator i1, const_iterator i2,
                          size_type n, charT c);
    template<class InputIterator>
      basic_string& replace(const_iterator i1, const_iterator i2,
                            InputIterator j1, InputIterator j2);
    basic_string& replace(const_iterator, const_iterator, initializer_list<charT>);

    size_type copy(charT* s, size_type n, size_type pos = 0) const;
    void swap(basic_string& str);

    // [string.ops], string operations:
    const charT* c_str() const noexcept;
    const charT* data() const noexcept;
    allocator_type get_allocator() const noexcept;

    size_type find (const basic_string& str, size_type pos = 0) const noexcept;
    size_type find (const charT* s, size_type pos, size_type n) const;
    size_type find (const charT* s, size_type pos = 0) const;
    size_type find (charT c, size_type pos = 0) const;
    size_type rfind(const basic_string& str, size_type pos = npos) const noexcept;
    size_type rfind(const charT* s, size_type pos, size_type n) const;
    size_type rfind(const charT* s, size_type pos = npos) const;
    size_type rfind(charT c, size_type pos = npos) const;

    size_type find_first_of(const basic_string& str,
                            size_type pos = 0) const noexcept;
    size_type find_first_of(const charT* s,
                            size_type pos, size_type n) const;
    size_type find_first_of(const charT* s, size_type pos = 0) const;
    size_type find_first_of(charT c, size_type pos = 0) const;
    size_type find_last_of (const basic_string& str,
                            size_type pos = npos) const noexcept;
    size_type find_last_of (const charT* s,
                            size_type pos, size_type n) const;
    size_type find_last_of (const charT* s, size_type pos = npos) const;
    size_type find_last_of (charT c, size_type pos = npos) const;

    size_type find_first_not_of(const basic_string& str,
                size_type pos = 0) const noexcept;
    size_type find_first_not_of(const charT* s, size_type pos,
                                size_type n) const;
    size_type find_first_not_of(const charT* s, size_type pos = 0) const;
    size_type find_first_not_of(charT c, size_type pos = 0) const;
    size_type find_last_not_of (const basic_string& str,
                                size_type pos = npos) const noexcept;
    size_type find_last_not_of (const charT* s, size_type pos,
                                size_type n) const;
    size_type find_last_not_of (const charT* s,
                                size_type pos = npos) const;
    size_type find_last_not_of (charT c, size_type pos = npos) const;

    basic_string substr(size_type pos = 0, size_type n = npos) const;
    int compare(const basic_string& str) const noexcept;
    int compare(size_type pos1, size_type n1,
                const basic_string& str) const;
    int compare(size_type pos1, size_type n1,
                const basic_string& str,
                size_type pos2, size_type n2 = npos) const;
    int compare(const charT* s) const;
    int compare(size_type pos1, size_type n1,
                const charT* s) const;
    int compare(size_type pos1, size_type n1,
                const charT* s, size_type n2) const;
  };
}
```

### `basic_string` general requirements <a id="string.require">[[string.require]]</a>

If any operation would cause `size()` to exceed `max_size()`, that
operation shall throw an exception object of type `length_error`.

If any member function or operator of `basic_string` throws an
exception, that function or operator shall have no other effect.

In every specialization `basic_string<charT, traits, Allocator>`, the
type `allocator_traits<Allocator>::value_type` shall name the same type
as `charT`. Every object of type
`basic_string<charT, traits, Allocator>` shall use an object of type
`Allocator` to allocate and free storage for the contained `charT`
objects as needed. The `Allocator` object used shall be obtained as
described in [[container.requirements.general]].

The char-like objects in a `basic_string` object shall be stored
contiguously. That is, for any `basic_string` object `s`, the identity
`&*(s.begin() + n) == &*s.begin() + n` shall hold for all values of `n`
such that `0 <= n < s.size()`.

References, pointers, and iterators referring to the elements of a
`basic_string` sequence may be invalidated by the following uses of that
`basic_string` object:

- as an argument to any standard library function taking a reference to
  non-const `basic_string` as an argument.[^3]
- Calling non-const member functions, except `operator[]`, `at`,
  `front`, `back`, `begin`, `rbegin`, `end`, and `rend`.

### `basic_string` constructors and assignment operators <a id="string.cons">[[string.cons]]</a>

``` cpp
explicit basic_string(const Allocator& a);
```

*Effects:* Constructs an object of class `basic_string`. The
postconditions of this function are indicated in
Table  [[tab:strings.ctr.1]].

**Table: `basic_string(const Allocator&)` effects**

| Element      | Value                                                          |
| ------------ | -------------------------------------------------------------- |
| `data()`     | a non-null pointer that is copyable and can have 0 added to it |
| `size()`     | 0                                                              |
| `capacity()` | an unspecified value                                           |

``` cpp
basic_string(const basic_string& str);
basic_string(basic_string&& str) noexcept;
```

*Effects:* Constructs an object of class `basic_string` as indicated in
Table  [[tab:strings.ctr.cpy]]. In the second form, `str` is left in a
valid state with an unspecified value.

**Table: `basic_string(const basic_string&)` effects**

| Element      | Value                                                                                                           |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| `data()`     | points at the first element of an allocated copy of the array whose first element is pointed at by `str.data()` |
| `size()`     | `str.size()`                                                                                                    |
| `capacity()` | a value at least as large as `size()`                                                                           |

``` cpp
basic_string(const basic_string& str,
             size_type pos, size_type n = npos,
             const Allocator& a = Allocator());
```

*Requires:* `pos <= str.size()`

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Constructs an object of class `basic_string` and determines
the effective length `rlen` of the initial string value as the smaller
of `n` and `str.size() - pos`, as indicated in
Table  [[tab:strings.ctr.2]].

**Table: `basic_string(const basic_string&, size_type, size_type, const Allocator&)` effects**

| Element      | Value                                                                                                                                         |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `data()`     | points at the first element of an allocated copy of `rlen` consecutive elements of the string controlled by `str` beginning at position `pos` |
| `size()`     | `rlen`                                                                                                                                        |
| `capacity()` | a value at least as large as `size()`                                                                                                         |

``` cpp
basic_string(const charT* s, size_type n,
             const Allocator& a = Allocator());
```

*Requires:* `s` points to an array of at least `n` elements of `charT`.

*Effects:* Constructs an object of class `basic_string` and determines
its initial string value from the array of `charT` of length `n` whose
first element is designated by `s`, as indicated in
Table  [[tab:strings.ctr.3]].

**Table: `basic_string(const charT*, size_type, const Allocator&)` effects**

| Element      | Value                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `data()`     | points at the first element of an allocated copy of the array whose first element is pointed at by `s` |
| `size()`     | `n`                                                                                                    |
| `capacity()` | a value at least as large as `size()`                                                                  |

``` cpp
basic_string(const charT* s, const Allocator& a = Allocator());
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Effects:* Constructs an object of class `basic_string` and determines
its initial string value from the array of `charT` of length
`traits::length(s)` whose first element is designated by `s`, as
indicated in Table  [[tab:strings.ctr.4]].

**Table: `basic_string(const charT*, const Allocator&)` effects**

| Element      | Value                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `data()`     | points at the first element of an allocated copy of the array whose first element is pointed at by `s` |
| `size()`     | `traits::length(s)`                                                                                    |
| `capacity()` | a value at least as large as `size()`                                                                  |


Uses `traits::length()`.

``` cpp
basic_string(size_type n, charT c, const Allocator& a = Allocator());
```

*Requires:* `n < npos`

*Effects:* Constructs an object of class `basic_string` and determines
its initial string value by repeating the char-like object `c` for all
`n` elements, as indicated in Table  [[tab:strings.ctr.5]].

**Table: `basic_string(size_t, charT, const Allocator&)` effects**

| Element      | Value                                                                                                 |
| ------------ | ----------------------------------------------------------------------------------------------------- |
| `data()`     | points at the first element of an allocated array of `n` elements, each storing the initial value `c` |
| `size()`     | `n`                                                                                                   |
| `capacity()` | a value at least as large as `size()`                                                                 |

``` cpp
template<class InputIterator>
  basic_string(InputIterator begin, InputIterator end,
               const Allocator& a = Allocator());
```

*Effects:* If `InputIterator` is an integral type, equivalent to

``` cpp
basic_string(static_cast<size_type>(begin), static_cast<value_type>(end), a)
```

Otherwise constructs a string from the values in the range \[`begin`,
`end`), as indicated in the Sequence Requirements table
(see  [[sequence.reqmts]]).

``` cpp
basic_string(initializer_list<charT> il, const Allocator& a = Allocator());
```

*Effects:* Same as `basic_string(il.begin(), il.end(), a)`.

``` cpp
basic_string(const basic_string& str, const Allocator& alloc);
basic_string(basic_string&& str, const Allocator& alloc);
```

*Effects:* Constructs an object of class `basic_string` as indicated in
Table  [[tab:strings.ctr.6]]. The stored allocator is constructed from
`alloc`. In the second form, `str` is left in a valid state with an
unspecified value.

**Table: `basic_string(const basic_string&, const Allocator&)` and
`basic_string(basic_string&&, const Allocator&)` effects**

| Element           | Value                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `data()`          | points at the first element of an allocated copy of the array whose first element is pointed at by the original value of `str.data()`. |
| `size()`          | the original value of `str.size()`                                                                                                     |
| `capacity()`      | a value at least as large as `size()`                                                                                                  |
| `get_allocator()` | `alloc`                                                                                                                                |


*Throws:* The second form throws nothing if
`alloc == str.get_allocator()`.

``` cpp
basic_string& operator=(const basic_string& str);
```

*Effects:* If `*this` and `str` are not the same object, modifies
`*this` as shown in Table  [[tab:strings.op=]].

If `*this` and `str` are the same object, the member has no effect.

*Returns:* `*this`

**Table: `operator=(const basic_string&)` effects**

| Element      | Value                                                                                                           |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| `data()`     | points at the first element of an allocated copy of the array whose first element is pointed at by `str.data()` |
| `size()`     | `str.size()`                                                                                                    |
| `capacity()` | a value at least as large as `size()`                                                                           |

``` cpp
basic_string& operator=(basic_string&& str) noexcept;
```

*Effects:* If `*this` and `str` are not the same object, modifies
`*this` as shown in Table  [[tab:strings.op=rv]]. A valid implementation
is `swap(str)`.

If `*this` and `str` are the same object, the member has no effect.

*Returns:* `*this`

**Table: `operator=(basic_string&&)` effects**

| Element      | Value                                                                  |
| ------------ | ---------------------------------------------------------------------- |
| `data()`     | points at the array whose first element was pointed at by `str.data()` |
| `size()`     | previous value of `str.size()`                                         |
| `capacity()` | a value at least as large as `size()`                                  |

``` cpp
basic_string& operator=(const charT* s);
```

*Returns:* `*this = basic_string(s)`.

Uses `traits::length()`.

``` cpp
basic_string& operator=(charT c);
```

*Returns:* `*this = basic_string(1,c)`.

``` cpp
basic_string& operator=(initializer_list<charT> il);
```

*Effects:* `*this = basic_string(il)`.

*Returns:* `*this`.

### `basic_string` iterator support <a id="string.iterators">[[string.iterators]]</a>

``` cpp
iterator       begin() noexcept;
const_iterator begin() const noexcept;
const_iterator cbegin() const noexcept;
```

*Returns:* An iterator referring to the first character in the string.

``` cpp
iterator       end() noexcept;
const_iterator end() const noexcept;
const_iterator cend() const noexcept;
```

*Returns:* An iterator which is the past-the-end value.

``` cpp
reverse_iterator       rbegin() noexcept;
const_reverse_iterator rbegin() const noexcept;
const_reverse_iterator crbegin() const noexcept;
```

*Returns:* An iterator which is semantically equivalent to
`reverse_iterator(end())`.

``` cpp
reverse_iterator       rend() noexcept;
const_reverse_iterator rend() const noexcept;
const_reverse_iterator crend() const noexcept;
```

*Returns:* An iterator which is semantically equivalent to
`reverse_iterator(begin())`.

### `basic_string` capacity <a id="string.capacity">[[string.capacity]]</a>

``` cpp
size_type size() const noexcept;
```

*Returns:* A count of the number of char-like objects currently in the
string.

*Complexity:* Constant time.

``` cpp
size_type length() const noexcept;
```

*Returns:* `size()`.

``` cpp
size_type max_size() const noexcept;
```

*Returns:* The size of the largest possible string.

*Complexity:* Constant time.

``` cpp
void resize(size_type n, charT c);
```

*Requires:* `n <= max_size()`

*Throws:* `length_error` if `n > max_size()`.

*Effects:* Alters the length of the string designated by `*this` as
follows:

- If `n <= size()`, the function replaces the string designated by
  `*this` with a string of length `n` whose elements are a copy of the
  initial elements of the original string designated by `*this`.
- If `n > size()`, the function replaces the string designated by
  `*this` with a string of length `n` whose first `size()` elements are
  a copy of the original string designated by `*this`, and whose
  remaining elements are all initialized to `c`.

``` cpp
void resize(size_type n);
```

*Effects:* `resize(n,charT())`.

``` cpp
size_type capacity() const noexcept;
```

*Returns:* The size of the allocated storage in the string.

``` cpp
void reserve(size_type res_arg=0);
```

The member function `reserve()` is a directive that informs a
`basic_string` object of a planned change in size, so that it can manage
the storage allocation accordingly.

*Effects:* After `reserve()`, `capacity()` is greater or equal to the
argument of `reserve`. Calling `reserve()` with a `res_arg` argument
less than `capacity()` is in effect a non-binding shrink request. A call
with `res_arg <= size()` is in effect a non-binding shrink-to-fit
request.

*Throws:* `length_error` if `res_arg > max_size()`.[^4]

``` cpp
void shrink_to_fit();
```

`shrink_to_fit` is a non-binding request to reduce `capacity()` to
`size()`. The request is non-binding to allow latitude for
implementation-specific optimizations.

``` cpp
void clear() noexcept;
```

*Effects:* Behaves as if the function calls:

``` cpp
erase(begin(), end());
```

``` cpp
bool empty() const noexcept;
```

*Returns:* `size() == 0`.

### `basic_string` element access <a id="string.access">[[string.access]]</a>

``` cpp
const_reference operator[](size_type pos) const;
reference       operator[](size_type pos);
```

*Requires:* `pos <= size()`.

*Returns:* `*(begin() + pos)` if `pos < size()`. Otherwise, returns a
reference to an object of type `charT` with value `charT()`, where
modifying the object leads to undefined behavior.

*Throws:* Nothing.

*Complexity:* Constant time.

``` cpp
const_reference at(size_type pos) const;
reference       at(size_type pos);
```

*Throws:* `out_of_range` if `pos >= size()`.

*Returns:* `operator[](pos)`.

``` cpp
const charT& front() const;
charT& front();
```

*Requires:* `!empty()`

*Effects:* Equivalent to `operator[](0)`.

``` cpp
const charT& back() const;
charT& back();
```

*Requires:* `!empty()`

*Effects:* Equivalent to `operator[](size() - 1)`.

### `basic_string` modifiers <a id="string.modifiers">[[string.modifiers]]</a>

#### `basic_string::operator+=` <a id="string::op+=">[[string::op+=]]</a>

``` cpp
basic_string&
  operator+=(const basic_string& str);
```

*Effects:* Calls `append(str)`.

*Returns:* `*this`.

``` cpp
basic_string& operator+=(const charT* s);
```

*Effects:* Calls `append(s)`.

*Returns:* `*this`.

``` cpp
basic_string& operator+=(charT c);
```

*Effects:* Calls `push_back(c)`;

*Returns:* `*this`.

``` cpp
basic_string& operator+=(initializer_list<charT> il);
```

*Effects:* Calls `append(il)`.

*Returns:* `*this`.

#### `basic_string::append` <a id="string::append">[[string::append]]</a>

``` cpp
basic_string&
  append(const basic_string& str);
```

*Effects:* Calls `append(str.data(), str.size())`.

*Returns:* `*this`.

``` cpp
basic_string&
  append(const basic_string& str, size_type pos, size_type n = npos);
```

*Requires:* `pos <= str.size()`

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to
append as the smaller of `n` and `str``.size() - ``pos` and calls
`append(str.data() + pos, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string&
  append(const charT* s, size_type n);
```

*Requires:* `s` points to an array of at least `n` elements of `charT`.

*Throws:* `length_error` if `size() + n > max_size()`.

*Effects:* The function replaces the string controlled by `*this` with a
string of length `size() + n` whose first `size()` elements are a copy
of the original string controlled by `*this` and whose remaining
elements are a copy of the initial `n` elements of `s`.

*Returns:* `*this`.

``` cpp
basic_string& append(const charT* s);
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Effects:* Calls `append(s, traits::length(s))`.

*Returns:* `*this`.

``` cpp
basic_string& append(size_type n, charT c);
```

*Effects:* Equivalent to `append(basic_string(n, c))`.

*Returns:* `*this`.

``` cpp
template<class InputIterator>
  basic_string& append(InputIterator first, InputIterator last);
```

*Requires:* \[`first`, `last`) is a valid range.

*Effects:* Equivalent to `append(basic_string(first, last))`.

*Returns:* `*this`.

``` cpp
basic_string& append(initializer_list<charT> il);
```

*Effects:* Calls `append(il.begin(), il.size())`.

*Returns:* `*this`.

``` cpp
void push_back(charT c);
```

*Effects:* Equivalent to `append(static_cast<size_type>(1), c)`.

#### `basic_string::assign` <a id="string::assign">[[string::assign]]</a>

``` cpp
basic_string& assign(const basic_string& str);
```

*Effects:* Equivalent to `assign(str, 0, npos)`.

*Returns:* `*this`.

``` cpp
basic_string& assign(basic_string&& str) noexcept;
```

*Effects:* The function replaces the string controlled by `*this` with a
string of length `str.size()` whose elements are a copy of the string
controlled by `str`. A valid implementation is `swap(str)`.

*Returns:* `*this`.

``` cpp
basic_string&
  assign(const basic_string& str, size_type pos,
         size_type n = npos);
```

*Requires:* `pos <= str.size()`

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to
assign as the smaller of `n` and `str``.size() - ``pos` and calls
`assign(str.data() + pos rlen)`.

*Returns:* `*this`.

``` cpp
basic_string& assign(const charT* s, size_type n);
```

*Requires:* `s` points to an array of at least `n` elements of `charT`.

*Throws:* `length_error` if `n > max_size()`.

*Effects:* Replaces the string controlled by `*this` with a string of
length `n` whose elements are a copy of those pointed to by `s`.

*Returns:* `*this`.

``` cpp
basic_string& assign(const charT* s);
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Effects:* Calls `assign(s, traits::length(s))`.

*Returns:* `*this`.

``` cpp
basic_string& assign(initializer_list<charT> il);
```

*Effects:* Calls `assign(il.begin(), il.size())`.

`*this`.

``` cpp
basic_string& assign(size_type n, charT c);
```

*Effects:* Equivalent to `assign(basic_string(n, c))`.

*Returns:* `*this`.

``` cpp
template<class InputIterator>
  basic_string& assign(InputIterator first, InputIterator last);
```

*Effects:* Equivalent to `assign(basic_string(first, last))`.

*Returns:* `*this`.

#### `basic_string::insert` <a id="string::insert">[[string::insert]]</a>

``` cpp
basic_string&
  insert(size_type pos1,
         const basic_string& str);
```

*Requires:* `pos <= size()`.

*Throws:* `out_of_range` if `pos > size()`.

*Effects:* Calls `insert(pos, str.data(), str.size())`.

*Returns:* `*this`.

``` cpp
basic_string&
  insert(size_type pos1,
         const basic_string& str,
         size_type pos2, size_type n = npos);
```

*Requires:* `pos1 <= size()` and `pos2 <= str.size()`

*Throws:* `out_of_range` if `pos1 > size()` or `pos2 > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to
insert as the smaller of `n` and `str.size() - pos2` and calls
`insert(pos1, str.data() + pos2, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string&
  insert(size_type pos, const charT* s, size_type n);
```

*Requires:* `s` points to an array of at least `n` elements of `charT`
and `pos <= size()`.

*Throws:* `out_of_range` if `pos > size()` or `length_error` if
`size() + n > max_size()`.

*Effects:* Replaces the string controlled by `*this` with a string of
length `size() + n` whose first `pos` elements are a copy of the initial
elements of the original string controlled by `*this` and whose next `n`
elements are a copy of the elements in `s` and whose remaining elements
are a copy of the remaining elements of the original string controlled
by `*this`.

*Returns:* `*this`.

``` cpp
basic_string&
  insert(size_type pos, const charT* s);
```

*Requires:* `pos <= size()` and `s` points to an array of at least
`traits::length(s) + 1` elements of `charT`.

*Effects:* Equivalent to `insert(pos, s, traits::length(s))`.

*Returns:* `*this`.

``` cpp
basic_string&
  insert(size_type pos, size_type n, charT c);
```

*Effects:* Equivalent to `insert(pos, basic_string(n, c))`.

*Returns:* `*this`.

``` cpp
iterator insert(const_iterator p, charT c);
```

*Requires:* `p` is a valid iterator on `*this`.

*Effects:* inserts a copy of `c` before the character referred to by
`p`.

*Returns:* An iterator which refers to the copy of the inserted
character.

``` cpp
iterator insert(const_iterator p, size_type n, charT c);
```

*Requires:* `p` is a valid iterator on `*this`.

*Effects:* inserts `n` copies of `c` before the character referred to by
`p`.

*Returns:* An iterator which refers to the copy of the first inserted
character, or `p` if `n == 0`.

``` cpp
template<class InputIterator>
  iterator insert(const_iterator p, InputIterator first, InputIterator last);
```

*Requires:* `p` is a valid iterator on `*this`. `[first,last)` is a
valid range.

*Effects:* Equivalent to
`insert(p - begin(), basic_string(first, last))`.

*Returns:* An iterator which refers to the copy of the first inserted
character, or `p` if `first == last`.

``` cpp
iterator insert(const_iterator p, initializer_list<charT> il);
```

*Effects:* `insert(p, il.begin(), il.end())`.

*Returns:* An iterator which refers to the copy of the first inserted
character, or `p` if `i1` is empty.

#### `basic_string::erase` <a id="string::erase">[[string::erase]]</a>

``` cpp
basic_string& erase(size_type pos = 0, size_type n = npos);
```

*Requires:* `pos` ` <= size()`

*Throws:* `out_of_range` if `pos` `> size()`.

*Effects:* Determines the effective length `xlen` of the string to be
removed as the smaller of `n` and `size() - pos`.

The function then replaces the string controlled by `*this` with a
string of length `size() - xlen` whose first `pos` elements are a copy
of the initial elements of the original string controlled by `*this`,
and whose remaining elements are a copy of the elements of the original
string controlled by `*this` beginning at position `pos + xlen`.

*Returns:* `*this`.

``` cpp
iterator erase(const_iterator p);
```

*Throws:* Nothing.

*Effects:* removes the character referred to by `p`.

*Returns:* An iterator which points to the element immediately following
`p` prior to the element being erased. If no such element exists,
`end()` is returned.

``` cpp
iterator erase(const_iterator first, const_iterator last);
```

*Requires:* `first` and `last` are valid iterators on `*this`, defining
a range `[first,last)`.

*Throws:* Nothing.

*Effects:* removes the characters in the range `[first,last)`.

*Returns:* An iterator which points to the element pointed to by `last`
prior to the other elements being erased. If no such element exists,
`end()` is returned.

``` cpp
void pop_back();
```

*Requires:* `!empty()`

*Throws:* Nothing.

*Effects:* Equivalent to `erase(size() - 1, 1)`.

#### `basic_string::replace` <a id="string::replace">[[string::replace]]</a>

``` cpp
basic_string&
  replace(size_type pos1, size_type n1,
          const basic_string& str);
```

*Requires:* `pos1 <= size()`.

*Throws:* `out_of_range` if `pos1 > size()`.

*Effects:* Calls `replace(pos1, n1, str.data(), str.size())`.

*Returns:* `*this`.

``` cpp
basic_string&
  replace(size_type pos1, size_type n1,
          const basic_string& str,
          size_type pos2, size_type n2 = npos);
```

*Requires:* `pos1 <= size()` and `pos2 <= str.size()`.

*Throws:* `out_of_range` if `pos1 > size()` or `pos2 > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to be
inserted as the smaller of `n2` and `str.size() - pos2` and calls
`replace(pos1, n1, str.data() + pos2, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string&
  replace(size_type pos1, size_type n1, const charT* s, size_type n2);
```

*Requires:* `pos1 <= size()` and `s` points to an array of at least `n2`
elements of `charT`.

*Throws:* `out_of_range` if `pos1 > size()` or `length_error` if the
length of the resulting string would exceed `max_size()` (see below).

*Effects:* Determines the effective length `xlen` of the string to be
removed as the smaller of `n1` and `size() - pos1`. If
`size() - xlen >= max_size() - n2` throws `length_error`. Otherwise, the
function replaces the string controlled by \*`this` with a string of
length `size() - xlen + n2` whose first `pos1` elements are a copy of
the initial elements of the original string controlled by `*this`, whose
next `n2` elements are a copy of the initial `n2` elements of `s`, and
whose remaining elements are a copy of the elements of the original
string controlled by `*this` beginning at position `pos + xlen`.

*Returns:* `*this`.

``` cpp
basic_string&
  replace(size_type pos, size_type n, const charT* s);
```

*Requires:* `pos <= size()` and `s` points to an array of at least
`traits::length(s) + 1` elements of `charT`.

*Effects:* Calls `replace(pos, n, s, traits::length(s))`.

*Returns:* `*this`.

``` cpp
basic_string&
  replace(size_type pos1, size_type n1,
          size_type n2, charT c);
```

*Effects:* Equivalent to `replace(pos1, n1, basic_string(n2, c))`.

*Returns:* `*this`.

``` cpp
basic_string& replace(const_iterator i1, const_iterator i2, const basic_string& str);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Calls `replace(i1 - begin(), i2 - i1, str)`.

*Returns:* `*this`.

``` cpp
basic_string&
  replace(const_iterator i1, const_iterator i2, const charT* s, size_type n);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges and
`s` points to an array of at least `n` elements of `charT`.

*Effects:* Calls `replace(i1 - begin(), i2 - i1, s, n)`.

*Returns:* `*this`.

``` cpp
basic_string& replace(const_iterator i1, const_iterator i2, const charT* s);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges and
`s` points to an array of at least `traits::length(s) + 1` elements of
`charT`.

*Effects:* Calls `replace(i1 - begin(), i2 - i1, s, traits::length(s))`.

*Returns:* `*this`.

``` cpp
basic_string& replace(const_iterator i1, const_iterator i2, size_type n,
                      charT c);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Calls `replace(i1 - begin(), i2 - i1, basic_string(n, c))`.

*Returns:* `*this`.

``` cpp
template<class InputIterator>
  basic_string& replace(const_iterator i1, const_iterator i2,
                        InputIterator j1, InputIterator j2);
```

*Requires:* \[`begin()`, `i1`), \[`i1`, `i2`) and \[`j1`, `j2`) are
valid ranges.

*Effects:* Calls `replace(i1 - begin(), i2 - i1, basic_string(j1, j2))`.

*Returns:* `*this`.

``` cpp
basic_string& replace(const_iterator i1, const_iterator i2,
                      initializer_list<charT> il);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Calls
`replace(i1 - begin(), i2 - i1, il.begin(), il.size())`.

*Returns:* `*this`.

#### `basic_string::copy` <a id="string::copy">[[string::copy]]</a>

``` cpp
size_type copy(charT* s, size_type n, size_type pos = 0) const;
```

*Requires:* `pos <= size()`

*Throws:* `out_of_range` if `pos > size()`.

*Effects:* Determines the effective length `rlen` of the string to copy
as the smaller of `n` and `size() - pos`. `s` shall designate an array
of at least `rlen` elements.

The function then replaces the string designated by `s` with a string of
length `rlen` whose elements are a copy of the string controlled by
`*this` beginning at position `pos`.

The function does not append a null object to the string designated by
`s`.

*Returns:* `rlen`.

#### `basic_string::swap` <a id="string::swap">[[string::swap]]</a>

``` cpp
void swap(basic_string& s);
```

`*this` contains the same sequence of characters that was in `s`, `s`
contains the same sequence of characters that was in `*this`.

*Throws:* Nothing.

*Complexity:* Constant time.

### `basic_string` string operations <a id="string.ops">[[string.ops]]</a>

#### `basic_string` accessors <a id="string.accessors">[[string.accessors]]</a>

``` cpp
const charT* c_str() const noexcept;
const charT* data() const noexcept;
```

*Returns:* A pointer `p` such that `p + i == &operator[](i)` for each
`i` in \[`0`, `size()`\].

*Complexity:* Constant time.

*Requires:* The program shall not alter any of the values stored in the
character array.

``` cpp
allocator_type get_allocator() const noexcept;
```

*Returns:* A copy of the `Allocator` object used to construct the string
or, if that allocator has been replaced, a copy of the most recent
replacement.

#### `basic_string::find` <a id="string::find">[[string::find]]</a>

``` cpp
size_type find(const basic_string& str,
               size_type pos = 0) const noexcept;
```

*Effects:* Determines the lowest position `xpos`, if possible, such that
both of the following conditions obtain:

- `pos <= xpos` and `xpos + str.size() <= size()`;
- `traits::eq(at(xpos+I), str.at(I))` for all elements `I` of the string
  controlled by `str`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

Uses `traits::eq()`.

``` cpp
size_type find(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find(basic_string(s,n),pos)`.

``` cpp
size_type find(const charT* s, size_type pos = 0) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find(basic_string(s), pos)`.

``` cpp
size_type find(charT c, size_type pos = 0) const;
```

*Returns:* `find(basic_string(1,c), pos)`.

#### `basic_string::rfind` <a id="string::rfind">[[string::rfind]]</a>

``` cpp
size_type rfind(const basic_string& str,
                size_type pos = npos) const noexcept;
```

*Effects:* Determines the highest position `xpos`, if possible, such
that both of the following conditions obtain:

- `xpos <= pos` and `xpos + str.size() <= size()`;
- `traits::eq(at(xpos+I), str.at(I))` for all elements `I` of the string
  controlled by `str`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

Uses `traits::eq()`.

``` cpp
size_type rfind(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `rfind(basic_string(s, n), pos)`.

``` cpp
size_type rfind(const charT* s, size_type pos = npos) const;
```

*Requires:* s points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `rfind(basic_string(s), pos)`.

``` cpp
size_type rfind(charT c, size_type pos = npos) const;
```

*Returns:* `rfind(basic_string(1,c),pos)`.

#### `basic_string::find_first_of` <a id="string::find.first.of">[[string::find.first.of]]</a>

``` cpp
size_type
  find_first_of(const basic_string& str,
                size_type pos = 0) const noexcept;
```

*Effects:* Determines the lowest position `xpos`, if possible, such that
both of the following conditions obtain:

- `pos <= xpos` and `xpos < size()`;
- `traits::eq(at(xpos), str.at(I))` for some element `I` of the string
  controlled by `str`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

Uses `traits::eq()`.

``` cpp
size_type
  find_first_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find_first_of(basic_string(s, n), pos)`.

``` cpp
size_type find_first_of(const charT* s, size_type pos = 0) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_first_of(basic_string(s), pos)`.

``` cpp
size_type find_first_of(charT c, size_type pos = 0) const;
```

*Returns:* `find_first_of(basic_string(1,c), pos)`.

#### `basic_string::find_last_of` <a id="string::find.last.of">[[string::find.last.of]]</a>

``` cpp
size_type
  find_last_of(const basic_string& str,
               size_type pos = npos) const noexcept;
```

*Effects:* Determines the highest position `xpos`, if possible, such
that both of the following conditions obtain:

- `xpos <= pos` and `xpos < size()`;
- `traits::eq(at(xpos), str.at(I))` for some element `I` of the string
  controlled by `str`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

Uses `traits::eq()`.

``` cpp
size_type find_last_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find_last_of(basic_string(s, n), pos)`.

``` cpp
size_type find_last_of(const charT* s, size_type pos = npos) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_last_of(basic_string(s), pos)`.

``` cpp
size_type find_last_of(charT c, size_type pos = npos) const;
```

*Returns:* `find_last_of(basic_string(1,c),pos)`.

#### `basic_string::find_first_not_of` <a id="string::find.first.not.of">[[string::find.first.not.of]]</a>

``` cpp
size_type
  find_first_not_of(const basic_string& str,
                    size_type pos = 0) const noexcept;
```

*Effects:* Determines the lowest position `xpos`, if possible, such that
both of the following conditions obtain:

- `pos <= xpos` and `xpos < size()`;
- `traits::eq(at(xpos), str.at(I))` for no element `I` of the string
  controlled by `str`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

Uses `traits::eq()`.

``` cpp
size_type
  find_first_not_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find_first_not_of(basic_string(s, n), pos)`.

``` cpp
size_type find_first_not_of(const charT* s, size_type pos = 0) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_first_not_of(basic_string(s), pos)`.

``` cpp
size_type find_first_not_of(charT c, size_type pos = 0) const;
```

*Returns:* `find_first_not_of(basic_string(1, c), pos)`.

#### `basic_string::find_last_not_of` <a id="string::find.last.not.of">[[string::find.last.not.of]]</a>

``` cpp
size_type
  find_last_not_of(const basic_string& str,
                   size_type pos = npos) const noexcept;
```

*Effects:* Determines the highest position `xpos`, if possible, such
that both of the following conditions obtain:

- `xpos <= pos` and `xpos < size()`;
- `traits::eq(at(xpos), str.at(I))` for no element `I` of the string
  controlled by `str`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

Uses `traits::eq()`.

``` cpp
size_type find_last_not_of(const charT* s, size_type pos,
                           size_type n) const;
```

*Returns:* `find_last_not_of(basic_string(s, n), pos)`.

``` cpp
size_type find_last_not_of(const charT* s, size_type pos = npos) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_last_not_of(basic_string(s), pos)`.

``` cpp
size_type find_last_not_of(charT c, size_type pos = npos) const;
```

*Returns:* `find_last_not_of(basic_string(1, c), pos)`.

#### `basic_string::substr` <a id="string::substr">[[string::substr]]</a>

``` cpp
basic_string substr(size_type pos = 0, size_type n = npos) const;
```

*Requires:* `pos <= size()`

*Throws:* `out_of_range` if `pos > size()`.

*Effects:* Determines the effective length `rlen` of the string to copy
as the smaller of `n` and `size() - pos`.

*Returns:* `basic_string(data()+pos,rlen)`.

#### `basic_string::compare` <a id="string::compare">[[string::compare]]</a>

``` cpp
int compare(const basic_string& str) const noexcept;
```

*Effects:* Determines the effective length *rlen* of the strings to
compare as the smallest of `size()` and `str.size()`. The function then
compares the two strings by calling
`traits::compare(data(), str.data(), rlen)`.

*Returns:* The nonzero result if the result of the comparison is
nonzero. Otherwise, returns a value as indicated in
Table  [[tab:strings.compare]].

**Table: `compare()` results**

| Condition               | Return Value |
| ----------------------- | ------------ |
| `size() < \ str.size()` | `< 0`        |
| `size() == str.size()`  | ` \ 0`       |
| `size() > \ str.size()` | `> 0`        |

``` cpp
int compare(size_type pos1, size_type n1,
            const basic_string& str) const;
```

*Returns:* `basic_string(*this,pos1,n1).compare(str)`.

``` cpp
int compare(size_type pos1, size_type n1,
            const basic_string& str,
            size_type pos2, size_type n2 = npos) const;
```

*Returns:*
`basic_string(*this, pos1, n1).compare(basic_string(str, pos2, n2))`.

``` cpp
int compare(const charT* s) const;
```

*Returns:* `compare(basic_string(s))`.

``` cpp
int compare(size_type pos, size_type n1,
            const charT* s) const;
```

*Returns:* `basic_string(*this, pos, n1).compare(basic_string(s))`.

``` cpp
int compare(size_type pos, size_type n1,
            const charT* s, size_type n2) const;
```

*Returns:* `basic_string(*this, pos, n1).compare(basic_string(s, n2))`.

### `basic_string` non-member functions <a id="string.nonmembers">[[string.nonmembers]]</a>

#### `operator+` <a id="string::op+">[[string::op+]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(const basic_string<charT,traits,Allocator>& lhs,
              const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `basic_string<charT,traits,Allocator>(lhs).append(rhs)`

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(basic_string<charT,traits,Allocator>&& lhs,
              const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `std::move(lhs.append(rhs))`

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(const basic_string<charT,traits,Allocator>& lhs,
              basic_string<charT,traits,Allocator>&& rhs);
```

*Returns:* `std::move(rhs.insert(0, lhs))`

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(basic_string<charT,traits,Allocator>&& lhs,
              basic_string<charT,traits,Allocator>&& rhs);
```

*Returns:* `std::move(lhs.append(rhs))` Or equivalently
`std::move(rhs.insert(0, lhs))`

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(const charT* lhs,
              const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `basic_string<charT,traits,Allocator>(lhs) + rhs`.

Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(const charT* lhs,
              basic_string<charT,traits,Allocator>&& rhs);
```

*Returns:* `std::move(rhs.insert(0, lhs))`.

Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(charT lhs,
              const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `basic_string<charT,traits,Allocator>(1,lhs) + rhs`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(charT lhs,
              basic_string<charT,traits,Allocator>&& rhs);
```

*Returns:* `std::move(rhs.insert(0, 1, lhs))`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(const basic_string<charT,traits,Allocator>& lhs,
              const charT* rhs);
```

*Returns:* `lhs + basic_string<charT,traits,Allocator>(rhs)`.

Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(basic_string<charT,traits,Allocator>&& lhs,
              const charT* rhs);
```

*Returns:* `std::move(lhs.append(rhs))`.

Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(const basic_string<charT,traits,Allocator>& lhs,
              charT rhs);
```

*Returns:* `lhs + basic_string<charT,traits,Allocator>(1,rhs)`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT,traits,Allocator>
    operator+(basic_string<charT,traits,Allocator>&& lhs,
              charT rhs);
```

*Returns:* `std::move(lhs.append(1, rhs))`.

#### `operator==` <a id="string::operator==">[[string::operator==]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator==(const basic_string<charT,traits,Allocator>& lhs,
                  const basic_string<charT,traits,Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator==(const charT* lhs,
                  const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `rhs == lhs`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator==(const basic_string<charT,traits,Allocator>& lhs,
                  const charT* rhs);
```

*Requires:* `rhs` points to an array of at least
`traits::length(rhs) + 1` elements of `charT`.

*Returns:* `lhs.compare(rhs) == 0`.

#### `operator!=` <a id="string::op!=">[[string::op!=]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator!=(const basic_string<charT,traits,Allocator>& lhs,
                  const basic_string<charT,traits,Allocator>& rhs) noexcept;
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator!=(const charT* lhs,
                  const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `rhs != lhs`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator!=(const basic_string<charT,traits,Allocator>& lhs,
                  const charT* rhs);
```

*Requires:* `rhs` points to an array of at least
`traits::length(rhs) + 1` elements of `charT`.

*Returns:* `lhs.compare(rhs) != 0`.

#### `operator<` <a id="string::op<">[[string::op<]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator< (const basic_string<charT,traits,Allocator>& lhs,
                  const basic_string<charT,traits,Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) < 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator< (const charT* lhs,
                  const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) > 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator< (const basic_string<charT,traits,Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) < 0`.

#### `operator>` <a id="string::op>">[[string::op>]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator> (const basic_string<charT,traits,Allocator>& lhs,
                  const basic_string<charT,traits,Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) > 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator> (const charT* lhs,
                  const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) < 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator> (const basic_string<charT,traits,Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) > 0`.

#### `operator<=` <a id="string::op<=">[[string::op<=]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator<=(const basic_string<charT,traits,Allocator>& lhs,
                  const basic_string<charT,traits,Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) <= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator<=(const charT* lhs,
                  const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) >= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator<=(const basic_string<charT,traits,Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) <= 0`.

#### `operator>=` <a id="string::op>=">[[string::op>=]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator>=(const basic_string<charT,traits,Allocator>& lhs,
                  const basic_string<charT,traits,Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) >= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator>=(const charT* lhs,
                  const basic_string<charT,traits,Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) <= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator>=(const basic_string<charT,traits,Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) >= 0`.

#### `swap` <a id="string.special">[[string.special]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_string<charT,traits,Allocator>& lhs,
    basic_string<charT,traits,Allocator>& rhs);
```

*Effects:* Equivalent to `lhs.swap(rhs);`

#### Inserters and extractors <a id="string.io">[[string.io]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT,traits>&
    operator>>(basic_istream<charT,traits>& is,
               basic_string<charT,traits,Allocator>& str);
```

*Effects:* Behaves as a formatted input
function ([[istream.formatted.reqmts]]). After constructing a `sentry`
object, if the sentry converts to true, calls `str.erase()` and then
extracts characters from `is` and appends them to `str` as if by calling
`str.append(1,c)`. If `is.width()` is greater than zero, the maximum
number `n` of characters appended is `is.width()`; otherwise `n` is
`str.max_size()`. Characters are extracted and appended until any of the
following occurs:

- *n* characters are stored;
- end-of-file occurs on the input sequence;
- `isspace(c,is.getloc())` is true for the next available input
  character *c*.

After the last character (if any) is extracted, `is.width(0)` is called
and the `sentry` object `k` is destroyed.

If the function extracts no characters, it calls
`is.setstate(ios::failbit)`, which may throw
`ios_base::failure` ([[iostate.flags]]).

*Returns:* `is`

``` cpp
template<class charT, class traits, class Allocator>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os,
               const basic_string<charT,traits,Allocator>& str);
```

*Effects:* Behaves as a formatted output
function ([[ostream.formatted.reqmts]]) of `os`. Forms a character
sequence `seq`, initially consisting of the elements defined by the
range \[`str.begin(), str.end()`). Determines padding for `seq` as
described in  [[ostream.formatted.reqmts]]. Then inserts `seq` as if by
calling `os.rdbuf()->sputn(seq, n)`, where `n` is the larger of
`os.width()` and `str.size()`; then calls `os.width(0)`.

*Returns:* `os`

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT,traits>&
    getline(basic_istream<charT,traits>& is,
            basic_string<charT,traits,Allocator>& str,
            charT delim);
template<class charT, class traits, class Allocator>
  basic_istream<charT,traits>&
    getline(basic_istream<charT,traits>&& is,
            basic_string<charT,traits,Allocator>& str,
            charT delim);
```

*Effects:* Behaves as an unformatted input
function ([[istream.unformatted]]), except that it does not affect the
value returned by subsequent calls to `basic_istream<>::gcount()`. After
constructing a `sentry` object, if the sentry converts to true, calls
`str.erase()` and then extracts characters from `is` and appends them to
`str` as if by calling `str.append(1, c)` until any of the following
occurs:

- end-of-file occurs on the input sequence (in which case, the `getline`
  function calls `is.setstate(ios_base::eofbit)`).
- `traits::eq(c, delim)` for the next available input character *c* (in
  which case, *c* is extracted but not appended) ([[iostate.flags]])
- `str.max_size()` characters are stored (in which case, the function
  calls `is.setstate(ios_base::failbit))` ([[iostate.flags]])

The conditions are tested in the order shown. In any case, after the
last character is extracted, the `sentry` object `k` is destroyed.

If the function extracts no characters, it calls
`is.setstate(ios_base::failbit)` which may throw
`ios_base::failure` ([[iostate.flags]]).

*Returns:* `is`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT,traits>&
    getline(basic_istream<charT,traits>& is,
            basic_string<charT,traits,Allocator>& str);
template<class charT, class traits, class Allocator>
  basic_istream<charT,traits>&
    getline(basic_istream<charT,traits>&& is,
            basic_string<charT,traits,Allocator>& str);
```

*Returns:* `getline(is,str,is.widen(’\n’))`

## Numeric conversions <a id="string.conversions">[[string.conversions]]</a>

``` cpp
int stoi(const string& str, size_t* idx = 0, int base = 10);
long stol(const string& str, size_t* idx = 0, int base = 10);
unsigned long stoul(const string& str, size_t* idx = 0, int base = 10);
long long stoll(const string& str, size_t* idx = 0, int base = 10);
unsigned long long stoull(const string& str, size_t* idx = 0, int base = 10);
```

*Effects:* the first two functions call
`strtol(str.c_str(), ptr, base)`, and the last three functions call
`strtoul(str.c_str(), ptr, base)`, `strtoll(str.c_str(), ptr, base)`,
and `strtoull(str.c_str(), ptr, base)`, respectively. Each function
returns the converted result, if any. The argument `ptr` designates a
pointer to an object internal to the function that is used to determine
what to store at `*idx`. If the function does not throw an exception and
`idx != 0`, the function stores in `*idx` the index of the first
unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `strtol`, `strtoul`, `strtoll`, or
`strtoull` reports that no conversion could be performed. Throws
`out_of_range` if `strtol`, `strtoul`, `strtoll` or `strtoull` sets
`errno` to `ERANGE`, or if the converted value is outside the range of
representable values for the return type.

``` cpp
float stof(const string& str, size_t* idx = 0);
double stod(const string& str, size_t* idx = 0);
long double stold(const string& str, size_t* idx = 0);
```

*Effects:* the first two functions call `strtod(str.c_str(), ptr)` and
the third function calls `strtold(str.c_str(), ptr)`. Each function
returns the converted result, if any. The argument `ptr` designates a
pointer to an object internal to the function that is used to determine
what to store at `*idx`. If the function does not throw an exception and
`idx != 0`, the function stores in `*idx` the index of the first
unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `strtod` or `strtold` reports that no
conversion could be performed. Throws `out_of_range` if `strtod` or
`strtold` sets `errno` to `ERANGE` or if the converted value is outside
the range of representable values for the return type.

``` cpp
string to_string(int val);
string to_string(unsigned val);
string to_string(long val);
string to_string(unsigned long val);
string to_string(long long val);
string to_string(unsigned long long val);
string to_string(float val);
string to_string(double val);
string to_string(long double val);
```

*Returns:* Each function returns a `string` object holding the character
representation of the value of its argument that would be generated by
calling `sprintf(buf, fmt, val)` with a format specifier of `"%d"`,
`"%u"`, `"%ld"`, `"%lu"`, `"%lld"`, `"%llu"`, `"%f"`, `"%f"`, or
`"%Lf"`, respectively, where `buf` designates an internal character
buffer of sufficient size.

``` cpp
int stoi(const wstring& str, size_t* idx = 0, int base = 10);
long stol(const wstring& str, size_t* idx = 0, int base = 10);
unsigned long stoul(const wstring& str, size_t* idx = 0, int base = 10);
long long stoll(const wstring& str, size_t* idx = 0, int base = 10);
unsigned long long stoull(const wstring& str, size_t* idx = 0, int base = 10);
```

*Effects:* the first two functions call
`wcstol(str.c_str(), ptr, base)`, and the last three functions call
`wcstoul(str.c_str(), ptr, base)`, `wcstoll(str.c_str(), ptr, base)`,
and `wcstoull(str.c_str(), ptr, base)`, respectively. Each function
returns the converted result, if any. The argument `ptr` designates a
pointer to an object internal to the function that is used to determine
what to store at `*idx`. If the function does not throw an exception and
`idx != 0`, the function stores in `*idx` the index of the first
unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `wcstol`, `wcstoul`, `wcstoll`, or
`wcstoull` reports that no conversion could be performed. Throws
`out_of_range` if the converted value is outside the range of
representable values for the return type.

``` cpp
float stof(const wstring& str, size_t* idx = 0);
double stod(const wstring& str, size_t* idx = 0);
long double stold(const wstring& str, size_t* idx = 0);
```

*Effects:* the first two functions call `wcstod(str.c_str(), ptr)` and
the third function calls `wcstold(str.c_str(), ptr)`. Each function
returns the converted result, if any. The argument `ptr` designates a
pointer to an object internal to the function that is used to determine
what to store at `*idx`. If the function does not throw an exception and
`idx != 0`, the function stores in `*idx` the index of the first
unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `wcstod` or `wcstold` reports that no
conversion could be performed. Throws `out_of_range` if `wcstod` or
`wcstold` sets `errno` to `ERANGE`.

``` cpp
wstring to_wstring(int val);
wstring to_wstring(unsigned val);
wstring to_wstring(long val);
wstring to_wstring(unsigned long val);
wstring to_wstring(long long val);
wstring to_wstring(unsigned long long val);
wstring to_wstring(float val);
wstring to_wstring(double val);
wstring to_wstring(long double val);
```

*Returns:* Each function returns a `wstring` object holding the
character representation of the value of its argument that would be
generated by calling `swprintf(buf, buffsz, fmt, val)` with a format
specifier of `L"%d"`, `L"%u"`, `L"%ld"`, `L"%lu"`, `L"%lld"`, `L"%llu"`,
`L"%f"`, `L"%f"`, or `L"%Lf"`, respectively, where `buf` designates an
internal character buffer of sufficient size `buffsz`.

## Hash support <a id="basic.string.hash">[[basic.string.hash]]</a>

``` cpp
template <> struct hash<string>;
template <> struct hash<u16string>;
template <> struct hash<u32string>;
template <> struct hash<wstring>;
```

The template specializations shall meet the requirements of class
template `hash` ([[unord.hash]]).

## Suffix for `basic_string` literals <a id="basic.string.literals">[[basic.string.literals]]</a>

``` cpp
string operator "" s(const char* str, size_t len);
```

*Returns:* `string{str,len}`

``` cpp
u16string operator "" s(const char16_t* str, size_t len);
```

*Returns:* `u16string{str,len}`

``` cpp
u32string operator "" s(const char32_t* str, size_t len);
```

*Returns:* `u32string{str,len}`

``` cpp
wstring operator "" s(const wchar_t* str, size_t len);
```

*Returns:* `wstring{str,len}`

The same suffix `s` is used for `chrono::duration` literals denoting
seconds but there is no conflict, since duration suffixes apply to
numbers and string literal suffixes apply to character array literals.

## Null-terminated sequence utilities <a id="c.strings">[[c.strings]]</a>

Tables  [[tab:strings.hdr.cctype]], [[tab:strings.hdr.cwctype]],
[[tab:strings.hdr.cstring]], [[tab:strings.hdr.cwchar]],
[[tab:strings.hdr.cstdlib]], and [[tab:strings.hdr.cuchar]] describe
headers `<cctype>`, `<cwctype>`, `<cstring>`, `<cwchar>`, `<cstdlib>`
(character conversions), and `<cuchar>`, respectively.

The contents of these headers shall be the same as the Standard C
Library headers `<ctype.h>`, `<wctype.h>`, `<string.h>`, `<wchar.h>`,
and `<stdlib.h>` and the C Unicode TR header `<uchar.h>`, respectively,
with the following modifications:

The headers shall not define the types `char16_t`, `char32_t`, and
`wchar_t` ([[lex.key]]).

The function signature `strchr(const char*, int)` shall be replaced by
the two declarations:

``` cpp
const char* strchr(const char* s, int c);
      char* strchr(      char* s, int c);
```

both of which shall have the same behavior as the original declaration.

The function signature `strpbrk(const char*, const char*)` shall be
replaced by the two declarations:

``` cpp
const char* strpbrk(const char* s1, const char* s2);
      char* strpbrk(      char* s1, const char* s2);
```

both of which shall have the same behavior as the original declaration.

The function signature `strrchr(const char*, int)` shall be replaced by
the two declarations:

``` cpp
const char* strrchr(const char* s, int c);
      char* strrchr(      char* s, int c);
```

both of which shall have the same behavior as the original declaration.

The function signature `strstr(const char*, const char*)` shall be
replaced by the two declarations:

``` cpp
const char* strstr(const char* s1, const char* s2);
      char* strstr(      char* s1, const char* s2);
```

both of which shall have the same behavior as the original declaration.

The function signature `memchr(const void*, int, size_t)` shall be
replaced by the two declarations:

``` cpp
const void* memchr(const void* s, int c, size_t n);
      void* memchr(      void* s, int c, size_t n);
```

both of which shall have the same behavior as the original declaration.

The function signature `wcschr(const wchar_t*, wchar_t)` shall be
replaced by the two declarations:

``` cpp
const wchar_t* wcschr(const wchar_t* s, wchar_t c);
      wchar_t* wcschr(      wchar_t* s, wchar_t c);
```

both of which shall have the same behavior as the original declaration.

The function signature `wcspbrk(const wchar_t*, const wchar_t*)` shall
be replaced by the two declarations:

``` cpp
const wchar_t* wcspbrk(const wchar_t* s1, const wchar_t* s2);
      wchar_t* wcspbrk(      wchar_t* s1, const wchar_t* s2);
```

both of which shall have the same behavior as the original declaration.

The function signature `wcsrchr(const wchar_t*, wchar_t)` shall be
replaced by the two declarations:

``` cpp
const wchar_t* wcsrchr(const wchar_t* s, wchar_t c);
      wchar_t* wcsrchr(      wchar_t* s, wchar_t c);
```

both of which shall have the same behavior as the original declaration.

The function signature `wcsstr(const wchar_t*, const wchar_t*)` shall be
replaced by the two declarations:

``` cpp
const wchar_t* wcsstr(const wchar_t* s1, const wchar_t* s2);
      wchar_t* wcsstr(      wchar_t* s1, const wchar_t* s2);
```

both of which shall have the same behavior as the original declaration.

The function signature `wmemchr(const wwchar_t*, int, size_t)` shall be
replaced by the two declarations:

``` cpp
const wchar_t* wmemchr(const wchar_t* s, wchar_t c, size_t n);
      wchar_t* wmemchr(      wchar_t* s, wchar_t c, size_t n);
```

both of which shall have the same behavior as the original declaration.

The functions `strerror` and `strtok` are not required to avoid data
races ([[res.on.data.races]]).

Calling the functions listed in Table  [[tab:mbstate.data.races]] with
an `mbstate_t*` argument of `NULL` may introduce a data race (
[[res.on.data.races]]) with other calls to these functions with an
`mbstate_t*` argument of `NULL`.

**Table: Potential `mbstate_t` data races**

|            |           |            |          |           |
| ---------- | --------- | ---------- | -------- | --------- |
| `mbrlen`   | `mbrtowc` | `mbsrtowc` | `mbtowc` | `wcrtomb` |
| `wcsrtomb` | `wctomb`  |            |          |           |


ISO C 7.3, 7.10.7, 7.10.8, and 7.11. Amendment 1 4.4, 4.5, and 4.6.

<!-- Link reference definitions -->
[basic.string]: #basic.string
[basic.string.hash]: #basic.string.hash
[basic.string.literals]: #basic.string.literals
[basic.types]: basic.md#basic.types
[c.strings]: #c.strings
[char.traits]: #char.traits
[char.traits.require]: #char.traits.require
[char.traits.specializations]: #char.traits.specializations
[char.traits.specializations.char]: #char.traits.specializations.char
[char.traits.specializations.char16_t]: #char.traits.specializations.char16_t
[char.traits.specializations.char32_t]: #char.traits.specializations.char32_t
[char.traits.specializations.wchar.t]: #char.traits.specializations.wchar.t
[char.traits.typedefs]: #char.traits.typedefs
[container.requirements.general]: containers.md#container.requirements.general
[copyassignable]: #copyassignable
[copyconstructible]: #copyconstructible
[defaultconstructible]: #defaultconstructible
[input.output]: input.md#input.output
[iostate.flags]: input.md#iostate.flags
[iostream.forward]: input.md#iostream.forward
[iostreams.limits.pos]: input.md#iostreams.limits.pos
[istream.formatted.reqmts]: input.md#istream.formatted.reqmts
[istream.unformatted]: input.md#istream.unformatted
[length.error]: diagnostics.md#length.error
[lex.key]: lex.md#lex.key
[ostream.formatted.reqmts]: input.md#ostream.formatted.reqmts
[out.of.range]: diagnostics.md#out.of.range
[random.access.iterators]: iterators.md#random.access.iterators
[res.on.data.races]: library.md#res.on.data.races
[sequence.reqmts]: containers.md#sequence.reqmts
[string.access]: #string.access
[string.accessors]: #string.accessors
[string.capacity]: #string.capacity
[string.classes]: #string.classes
[string.cons]: #string.cons
[string.conversions]: #string.conversions
[string.io]: #string.io
[string.iterators]: #string.iterators
[string.modifiers]: #string.modifiers
[string.nonmembers]: #string.nonmembers
[string.ops]: #string.ops
[string.require]: #string.require
[string.special]: #string.special
[string::append]: #string::append
[string::assign]: #string::assign
[string::compare]: #string::compare
[string::copy]: #string::copy
[string::erase]: #string::erase
[string::find]: #string::find
[string::find.first.not.of]: #string::find.first.not.of
[string::find.first.of]: #string::find.first.of
[string::find.last.not.of]: #string::find.last.not.of
[string::find.last.of]: #string::find.last.of
[string::insert]: #string::insert
[string::op!=]: #string::op!=
[string::op+]: #string::op+
[string::op+=]: #string::op+=
[string::op<]: #string::op<
[string::op<=]: #string::op<=
[string::op>]: #string::op>
[string::op>=]: #string::op>=
[string::operator==]: #string::operator==
[string::replace]: #string::replace
[string::rfind]: #string::rfind
[string::substr]: #string::substr
[string::swap]: #string::swap
[strings]: #strings
[strings.general]: #strings.general
[tab:char.traits.require]: #tab:char.traits.require
[tab:mbstate.data.races]: #tab:mbstate.data.races
[tab:strings.compare]: #tab:strings.compare
[tab:strings.ctr.1]: #tab:strings.ctr.1
[tab:strings.ctr.2]: #tab:strings.ctr.2
[tab:strings.ctr.3]: #tab:strings.ctr.3
[tab:strings.ctr.4]: #tab:strings.ctr.4
[tab:strings.ctr.5]: #tab:strings.ctr.5
[tab:strings.ctr.6]: #tab:strings.ctr.6
[tab:strings.ctr.cpy]: #tab:strings.ctr.cpy
[tab:strings.hdr.cctype]: #tab:strings.hdr.cctype
[tab:strings.hdr.cstdlib]: #tab:strings.hdr.cstdlib
[tab:strings.hdr.cstring]: #tab:strings.hdr.cstring
[tab:strings.hdr.cuchar]: #tab:strings.hdr.cuchar
[tab:strings.hdr.cwchar]: #tab:strings.hdr.cwchar
[tab:strings.hdr.cwctype]: #tab:strings.hdr.cwctype
[tab:strings.lib.summary]: #tab:strings.lib.summary
[tab:strings.op=]: #tab:strings.op=
[tab:strings.op=rv]: #tab:strings.op=rv
[unord.hash]: utilities.md#unord.hash

[^1]: If `eof()` can be held in `char_type` then some iostreams
    operations may give surprising results.

[^2]: `Allocator::value_type` must name the same type as `charT` (
    [[string.require]]).

[^3]: For example, as an argument to non-member functions `swap()` (
    [[string.special]]), `operator>{}>()` ([[string.io]]), and
    `getline()` ([[string.io]]), or as an argument to
    `basic_string::swap()`

[^4]: `reserve()` uses `allocator_traits<Allocator>::allocate()` which
    may throw an appropriate exception.
