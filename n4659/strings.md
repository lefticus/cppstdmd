# Strings library <a id="strings">[[strings]]</a>

## General <a id="strings.general">[[strings.general]]</a>

This Clause describes components for manipulating sequences of any
non-array POD ( [[basic.types]]) type. Such types are called *char-like
types*, and objects of char-like types are called *char-like objects* or
simply *characters*.

The following subclauses describe a character traits class, a string
class, and null-terminated sequence utilities, as summarized in Table 
[[tab:strings.lib.summary]].

**Table: Strings library summary**

| Subclause          |                                    | Header          |
| ------------------ | ---------------------------------- | --------------- |
| [[char.traits]]    | Character traits                   | `<string>`      |
| [[string.classes]] | String classes                     | `<string>`      |
| [[string.view]]    | String view classes                | `<string_view>` |
|                    |                                    | `<cctype>`      |
|                    |                                    | `<cwctype>`     |
| [[c.strings]]      | Null-terminated sequence utilities | `<cstring>`     |
|                    |                                    | `<cwchar>`      |
|                    |                                    | `<cstdlib>`     |
|                    |                                    | `<cuchar>`      |


## Character traits <a id="char.traits">[[char.traits]]</a>

This subclause defines requirements on classes representing *character
traits*, and defines a class template `char_traits<charT>`, along with
four specializations, `char_traits<char>`, `char_traits<char16_t>`,  
`char_traits<char32_t>`, and `char_traits<wchar_t>`, that satisfy those
requirements.

Most classes specified in Clauses  [[string.classes]] and 
[[input.output]] need a set of related types and functions to complete
the definition of their semantics. These types and functions are
provided as a set of member *typedef-name*s and functions in the
template parameter `traits` used by each such template. This subclause
defines the semantics of these members.

To specialize those templates to generate a string or iostream class to
handle a particular character container type `CharT`, that and its
related character traits class `Traits` are passed as a pair of
parameters to the string or iostream template as parameters `charT` and
`traits`. `Traits::char_type` shall be the same as `CharT`.

This subclause specifies a class template, `char_traits<charT>`, and
four explicit specializations of it, `char_traits<{}char>`,
`char_traits<char16_t>`, `char_traits<char32_t>`, and
`char_traits<wchar_t>`, all of which appear in the header `<string>` and
satisfy the requirements below.

### Character traits requirements <a id="char.traits.require">[[char.traits.require]]</a>

In Table  [[tab:char.traits.require]], `X` denotes a Traits class
defining types and functions for the character container type `CharT`;
`c` and `d` denote values of type `CharT`; `p` and `q` denote values of
type `const CharT*`; `s` denotes a value of type `CharT*`; `n`, `i` and
`j` denote values of type `size_t`; `e` and `f` denote values of type
`X::int_type`; `pos` denotes a value of type `X::pos_type`; `state`
denotes a value of type `X::state_type`; and `r` denotes an lvalue of
type `CharT`. Operations on Traits shall not throw exceptions.

The class template

``` cpp
template<class charT> struct char_traits;
```

shall be provided in the header `<string>` as a basis for explicit
specializations.

### Traits typedefs <a id="char.traits.typedefs">[[char.traits.typedefs]]</a>

``` cpp
using char_type = CHAR_T;
```

The type `char_type` is used to refer to the character container type in
the implementation of the library classes defined in  [[string.classes]]
and Clause  [[input.output]].

``` cpp
using int_type = INT_T;
```

*Requires:* For a certain character container type `char_type`, a
related container type `INT_T` shall be a type or class which can
represent all of the valid characters converted from the corresponding
`char_type` values, as well as an end-of-file value, `eof()`. The type
`int_type` represents a character container type which can hold
end-of-file to be used as a return type of the iostream class member
functions.[^1]

``` cpp
using off_type = implementation-defined;
using pos_type = implementation-defined;
```

*Requires:* Requirements for `off_type` and `pos_type` are described
in  [[iostreams.limits.pos]] and [[iostream.forward]].

``` cpp
using state_type = STATE_T;
```

*Requires:* `state_type` shall meet the requirements of `CopyAssignable`
(Table  [[tab:copyassignable]]), `CopyConstructible`
(Table  [[tab:copyconstructible]]), and `DefaultConstructible`
(Table  [[tab:defaultconstructible]]) types.

### `char_traits` specializations <a id="char.traits.specializations">[[char.traits.specializations]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char>;
  template<> struct char_traits<char16_t>;
  template<> struct char_traits<char32_t>;
  template<> struct char_traits<wchar_t>;
}
```

The header `<string>` shall define four specializations of the class
template `char_traits`: `char_traits<{}char>`, `char_traits<char16_t>`,
`char_traits<char32_t>`, and `char_traits<wchar_t>`.

The requirements for the members of these specializations are given in
Clause  [[char.traits.require]].

#### `struct char_traits<char>` <a id="char.traits.specializations.char">[[char.traits.specializations.char]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char> {
    using char_type  = char;
    using int_type   = int;
    using off_type   = streamoff;
    using pos_type   = streampos;
    using state_type = mbstate_t;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
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
`unsigned char`.

The member `eof()` shall return `EOF`.

#### `struct char_traits<char16_t>` <a id="char.traits.specializations.char16_t">[[char.traits.specializations.char16_t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char16_t> {
    using char_type  = char16_t;
    using int_type   = uint_least16_t;
    using off_type   = streamoff;
    using pos_type   = u16streampos;
    using state_type = mbstate_t;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
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
satisfies the requirements for `pos_type` in  [[iostreams.limits.pos]]
and [[iostream.forward]].

The two-argument members `assign`, `eq`, and `lt` shall be defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` shall return an *implementation-defined* constant
that cannot appear as a valid UTF-16 code unit.

#### `struct char_traits<char32_t>` <a id="char.traits.specializations.char32_t">[[char.traits.specializations.char32_t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char32_t> {
    using char_type  = char32_t;
    using int_type   = uint_least32_t;
    using off_type   = streamoff;
    using pos_type   = u32streampos;
    using state_type = mbstate_t;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
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
satisfies the requirements for `pos_type` in  [[iostreams.limits.pos]]
and [[iostream.forward]].

The two-argument members `assign`, `eq`, and `lt` shall be defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` shall return an *implementation-defined* constant
that cannot appear as a Unicode code point.

#### `struct char_traits<wchar_t>` <a id="char.traits.specializations.wchar.t">[[char.traits.specializations.wchar.t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<wchar_t> {
    using char_type  = wchar_t;
    using int_type   = wint_t;
    using off_type   = streamoff;
    using pos_type   = wstreampos;
    using state_type = mbstate_t;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
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
satisfies the requirements for `pos_type` in  [[iostreams.limits.pos]]
and [[iostream.forward]].

The type `mbstate_t` is defined in `<cwchar>` and can represent any of
the conversion states that can occur in an *implementation-defined* set
of supported multibyte character encoding rules.

The two-argument members `assign`, `eq`, and `lt` shall be defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` shall return `WEOF`.

## String classes <a id="string.classes">[[string.classes]]</a>

The header `<string>` defines the `basic_string` class template for
manipulating varying-length sequences of char-like objects and four
*typedef-name*s, `string`, `u16string`, `u32string`, and `wstring`, that
name the specializations `basic_string<char>`, `basic_string<char16_t>`,
`basic_string<char32_t>`, and `basic_string<{}wchar_t>`, respectively.

### Header `<string>` synopsis <a id="string.syn">[[string.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {
  // [char.traits], character traits
  template<class charT> struct char_traits;
  template<> struct char_traits<char>;
  template<> struct char_traits<char16_t>;
  template<> struct char_traits<char32_t>;
  template<> struct char_traits<wchar_t>;

  // [basic.string], basic_string
  template<class charT, class traits = char_traits<charT>,
    class Allocator = allocator<charT>>
      class basic_string;

  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(const charT* lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(const charT* lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(charT lhs, const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(charT lhs, basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                const charT* rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                const charT* rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs, charT rhs);
  template<class charT, class traits, class Allocator>
    basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs, charT rhs);

  template<class charT, class traits, class Allocator>
    bool operator==(const basic_string<charT, traits, Allocator>& lhs,
                    const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator==(const charT* lhs,
                    const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator==(const basic_string<charT, traits, Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator!=(const basic_string<charT, traits, Allocator>& lhs,
                    const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator!=(const charT* lhs,
                    const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator!=(const basic_string<charT, traits, Allocator>& lhs,
                    const charT* rhs);

  template<class charT, class traits, class Allocator>
    bool operator< (const basic_string<charT, traits, Allocator>& lhs,
                    const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator< (const basic_string<charT, traits, Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator< (const charT* lhs,
                    const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator> (const basic_string<charT, traits, Allocator>& lhs,
                    const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator> (const basic_string<charT, traits, Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator> (const charT* lhs,
                    const basic_string<charT, traits, Allocator>& rhs);

  template<class charT, class traits, class Allocator>
    bool operator<=(const basic_string<charT, traits, Allocator>& lhs,
                    const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator<=(const basic_string<charT, traits, Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator<=(const charT* lhs,
                    const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    bool operator>=(const basic_string<charT, traits, Allocator>& lhs,
                    const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    bool operator>=(const basic_string<charT, traits, Allocator>& lhs,
                    const charT* rhs);
  template<class charT, class traits, class Allocator>
    bool operator>=(const charT* lhs,
                    const basic_string<charT, traits, Allocator>& rhs);

  // [string.special], swap
  template<class charT, class traits, class Allocator>
    void swap(basic_string<charT, traits, Allocator>& lhs,
              basic_string<charT, traits, Allocator>& rhs)
      noexcept(noexcept(lhs.swap(rhs)));

  // [string.io], inserters and extractors
  template<class charT, class traits, class Allocator>
    basic_istream<charT, traits>&
      operator>>(basic_istream<charT, traits>& is,
                 basic_string<charT, traits, Allocator>& str);
  template<class charT, class traits, class Allocator>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os,
                 const basic_string<charT, traits, Allocator>& str);
  template<class charT, class traits, class Allocator>
    basic_istream<charT, traits>&
      getline(basic_istream<charT, traits>& is,
              basic_string<charT, traits, Allocator>& str,
              charT delim);
  template<class charT, class traits, class Allocator>
    basic_istream<charT, traits>&
      getline(basic_istream<charT, traits>&& is,
              basic_string<charT, traits, Allocator>& str,
              charT delim);
  template<class charT, class traits, class Allocator>
    basic_istream<charT, traits>&
      getline(basic_istream<charT, traits>& is,
              basic_string<charT, traits, Allocator>& str);
  template<class charT, class traits, class Allocator>
    basic_istream<charT, traits>&
      getline(basic_istream<charT, traits>&& is,
              basic_string<charT, traits, Allocator>& str);

  // basic_string typedef names
  using string    = basic_string<char>;
  using u16string = basic_string<char16_t>;
  using u32string = basic_string<char32_t>;
  using wstring   = basic_string<wchar_t>;

  // [string.conversions], numeric conversions
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

  // [basic.string.hash], hash support
  template<class T> struct hash;
  template<> struct hash<string>;
  template<> struct hash<u16string>;
  template<> struct hash<u32string>;
  template<> struct hash<wstring>;

  namespace pmr {
    template <class charT, class traits = char_traits<charT>>
      using basic_string =
        std::basic_string<charT, traits, polymorphic_allocator<charT>>;

    using string    = basic_string<char>;
    using u16string = basic_string<char16_t>;
    using u32string = basic_string<char32_t>;
    using wstring   = basic_string<wchar_t>;
  }

  inline namespace literals {
  inline namespace string_literals {
    // [basic.string.literals], suffix for basic_string literals
    string    operator""s(const char* str, size_t len);
    u16string operator""s(const char16_t* str, size_t len);
    u32string operator""s(const char32_t* str, size_t len);
    wstring   operator""s(const wchar_t* str, size_t len);
  }
  }
}
```

### Class template `basic_string` <a id="basic.string">[[basic.string]]</a>

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

A `basic_string` is a contiguous container (
[[container.requirements.general]]).

In all cases, `size() <= capacity()`.

The functions described in this Clause can report two kinds of errors,
each associated with an exception type:

- a *length* error is associated with exceptions of type
  `length_error` ( [[length.error]]);
- an *out-of-range* error is associated with exceptions of type
  `out_of_range` ( [[out.of.range]]).

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_string {
  public:
    // types:
    using traits_type            = traits;
    using value_type             = charT;
    using allocator_type         = Allocator;
    using size_type              = typename allocator_traits<Allocator>::size_type;
    using difference_type        = typename allocator_traits<Allocator>::difference_type;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;

    using iterator               = implementation-defined  // type of basic_string::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of basic_string::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    static const size_type npos  = -1;

    // [string.cons], construct/copy/destroy
    basic_string() noexcept(noexcept(Allocator())) : basic_string(Allocator()) { }
    explicit basic_string(const Allocator& a) noexcept;
    basic_string(const basic_string& str);
    basic_string(basic_string&& str) noexcept;
    basic_string(const basic_string& str, size_type pos,
                 const Allocator& a = Allocator());
    basic_string(const basic_string& str, size_type pos, size_type n,
                 const Allocator& a = Allocator());
    template<class T>
      basic_string(const T& t, size_type pos, size_type n,
                   const Allocator& a = Allocator());
    explicit basic_string(basic_string_view<charT, traits> sv,
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
    basic_string& operator=(basic_string&& str)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    basic_string& operator=(basic_string_view<charT, traits> sv);
    basic_string& operator=(const charT* s);
    basic_string& operator=(charT c);
    basic_string& operator=(initializer_list<charT>);

    // [string.iterators], iterators
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

    // [string.capacity], capacity
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

    // [string.access], element access
    const_reference operator[](size_type pos) const;
    reference       operator[](size_type pos);
    const_reference at(size_type n) const;
    reference       at(size_type n);

    const charT& front() const;
    charT&       front();
    const charT& back() const;
    charT&       back();

    // [string.modifiers], modifiers
    basic_string& operator+=(const basic_string& str);
    basic_string& operator+=(basic_string_view<charT, traits> sv);
    basic_string& operator+=(const charT* s);
    basic_string& operator+=(charT c);
    basic_string& operator+=(initializer_list<charT>);
    basic_string& append(const basic_string& str);
    basic_string& append(const basic_string& str, size_type pos,
                         size_type n = npos);
    basic_string& append(basic_string_view<charT, traits> sv);
    template<class T>
      basic_string& append(const T& t, size_type pos, size_type n = npos);
    basic_string& append(const charT* s, size_type n);
    basic_string& append(const charT* s);
    basic_string& append(size_type n, charT c);
    template<class InputIterator>
      basic_string& append(InputIterator first, InputIterator last);
    basic_string& append(initializer_list<charT>);
    void push_back(charT c);

    basic_string& assign(const basic_string& str);
    basic_string& assign(basic_string&& str)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    basic_string& assign(const basic_string& str, size_type pos,
                         size_type n = npos);
    basic_string& assign(basic_string_view<charT, traits> sv);
    template<class T>
      basic_string& assign(const T& t, size_type pos, size_type n = npos);
    basic_string& assign(const charT* s, size_type n);
    basic_string& assign(const charT* s);
    basic_string& assign(size_type n, charT c);
    template<class InputIterator>
      basic_string& assign(InputIterator first, InputIterator last);
    basic_string& assign(initializer_list<charT>);

    basic_string& insert(size_type pos, const basic_string& str);
    basic_string& insert(size_type pos1, const basic_string& str,
                         size_type pos2, size_type n = npos);
    basic_string& insert(size_type pos, basic_string_view<charT, traits> sv);
    template<class T>
      basic_string& insert(size_type pos1, const T& t,
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
    basic_string& replace(size_type pos1, size_type n1,
                          basic_string_view<charT, traits> sv);
    template<class T>
      basic_string& replace(size_type pos1, size_type n1, const T& t,
                            size_type pos2, size_type n2 = npos);
    basic_string& replace(size_type pos, size_type n1, const charT* s,
                          size_type n2);
    basic_string& replace(size_type pos, size_type n1, const charT* s);
    basic_string& replace(size_type pos, size_type n1, size_type n2,
                          charT c);

    basic_string& replace(const_iterator i1, const_iterator i2,
                          const basic_string& str);
    basic_string& replace(const_iterator i1, const_iterator i2,
                          basic_string_view<charT, traits> sv);
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
    void swap(basic_string& str)
      noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
               allocator_traits<Allocator>::is_always_equal::value);

    // [string.ops], string operations
    const charT* c_str() const noexcept;
    const charT* data() const noexcept;
    charT* data() noexcept;
    operator basic_string_view<charT, traits>() const noexcept;
    allocator_type get_allocator() const noexcept;

    size_type find (basic_string_view<charT, traits> sv,
                    size_type pos = 0) const noexcept;
    size_type find (const basic_string& str, size_type pos = 0) const noexcept;
    size_type find (const charT* s, size_type pos, size_type n) const;
    size_type find (const charT* s, size_type pos = 0) const;
    size_type find (charT c, size_type pos = 0) const;
    size_type rfind(basic_string_view<charT, traits> sv,
                    size_type pos = npos) const noexcept;
    size_type rfind(const basic_string& str, size_type pos = npos) const noexcept;
    size_type rfind(const charT* s, size_type pos, size_type n) const;
    size_type rfind(const charT* s, size_type pos = npos) const;
    size_type rfind(charT c, size_type pos = npos) const;

    size_type find_first_of(basic_string_view<charT, traits> sv,
                            size_type pos = 0) const noexcept;
    size_type find_first_of(const basic_string& str,
                            size_type pos = 0) const noexcept;
    size_type find_first_of(const charT* s,
                            size_type pos, size_type n) const;
    size_type find_first_of(const charT* s, size_type pos = 0) const;
    size_type find_first_of(charT c, size_type pos = 0) const;
    size_type find_last_of (basic_string_view<charT, traits> sv,
                            size_type pos = npos) const noexcept;
    size_type find_last_of (const basic_string& str,
                            size_type pos = npos) const noexcept;
    size_type find_last_of (const charT* s,
                            size_type pos, size_type n) const;
    size_type find_last_of (const charT* s, size_type pos = npos) const;
    size_type find_last_of (charT c, size_type pos = npos) const;

    size_type find_first_not_of(basic_string_view<charT, traits> sv,
                                size_type pos = 0) const noexcept;
    size_type find_first_not_of(const basic_string& str,
                                size_type pos = 0) const noexcept;
    size_type find_first_not_of(const charT* s, size_type pos,
                                size_type n) const;
    size_type find_first_not_of(const charT* s, size_type pos = 0) const;
    size_type find_first_not_of(charT c, size_type pos = 0) const;
    size_type find_last_not_of (basic_string_view<charT, traits> sv,
                                size_type pos = npos) const noexcept;
    size_type find_last_not_of (const basic_string& str,
                                size_type pos = npos) const noexcept;
    size_type find_last_not_of (const charT* s, size_type pos,
                                size_type n) const;
    size_type find_last_not_of (const charT* s,
                                size_type pos = npos) const;
    size_type find_last_not_of (charT c, size_type pos = npos) const;

    basic_string substr(size_type pos = 0, size_type n = npos) const;
    int compare(basic_string_view<charT, traits> sv) const noexcept;
    int compare(size_type pos1, size_type n1,
                basic_string_view<charT, traits> sv) const;
    template<class T>
      int compare(size_type pos1, size_type n1, const T& t,
                  size_type pos2, size_type n2 = npos) const;
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

  template<class InputIterator,
           class Allocator = allocator<typename iterator_traits<InputIterator>::value_type>>
    basic_string(InputIterator, InputIterator, Allocator = Allocator())
      -> basic_string<typename iterator_traits<InputIterator>::value_type,
                      char_traits<typename iterator_traits<InputIterator>::value_type>,
                      Allocator>;
}
```

#### `basic_string` general requirements <a id="string.require">[[string.require]]</a>

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
described in [[container.requirements.general]]. In every specialization
`basic_string<charT, traits, Allocator>`, the type `traits` shall
satisfy the character traits requirements ( [[char.traits]]), and the
type `traits::char_type` shall name the same type as `charT`.

References, pointers, and iterators referring to the elements of a
`basic_string` sequence may be invalidated by the following uses of that
`basic_string` object:

- as an argument to any standard library function taking a reference to
  non-const `basic_string` as an argument.[^3]
- Calling non-const member functions, except `operator[]`, `at`, `data`,
  `front`, `back`, `begin`, `rbegin`, `end`, and `rend`.

#### `basic_string` constructors and assignment operators <a id="string.cons">[[string.cons]]</a>

``` cpp
explicit basic_string(const Allocator& a) noexcept;
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
basic_string(const basic_string& str, size_type pos,
             const Allocator& a = Allocator());
```

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Constructs an object of class `basic_string` and determines
the effective length `rlen` of the initial string value as
`str.size() - pos`, as indicated in Table  [[tab:strings.ctr.2]].

``` cpp
basic_string(const basic_string& str, size_type pos, size_type n,
             const Allocator& a = Allocator());
```

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Constructs an object of class `basic_string` and determines
the effective length `rlen` of the initial string value as the smaller
of `n` and `str.size() - pos`, as indicated in
Table  [[tab:strings.ctr.2]].

**Table: `basic_string(const basic_string&, size_type, const Allocator&)`\protect\mbox{ }and\protect
`basic_string(const basic_string&, size_type, size_type, const Allocator&)` effects**

| Element      | Value                                                                                                                                         |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `data()`     | points at the first element of an allocated copy of `rlen` consecutive elements of the string controlled by `str` beginning at position `pos` |
| `size()`     | `rlen`                                                                                                                                        |
| `capacity()` | a value at least as large as `size()`                                                                                                         |

``` cpp
template<class T>
  basic_string(const T& t, size_type pos, size_type n,
               const Allocator& a = Allocator());
```

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t;` and then behaves the same as:

``` cpp
basic_string(sv.substr(pos, n), a);
```

*Remarks:* This constructor shall not participate in overload resolution
unless `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true`.

``` cpp
explicit basic_string(basic_string_view<charT, traits> sv,
                      const Allocator& a = Allocator());
```

*Effects:* Same as `basic_string(sv.data(), sv.size(), a)`.

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

``` cpp
basic_string(size_type n, charT c, const Allocator& a = Allocator());
```

*Requires:* `n < npos`.

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

*Effects:* If `InputIterator` is an integral type, equivalent to:

``` cpp
basic_string(static_cast<size_type>(begin), static_cast<value_type>(end), a);
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

**Table: `basic_string(const basic_string&, const Allocator&)`\protect and
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
template<class InputIterator,
         class Allocator = allocator<typename iterator_traits<InputIterator>::value_type>>
  basic_string(InputIterator, InputIterator, Allocator = Allocator())
    -> basic_string<typename iterator_traits<InputIterator>::value_type,
                    char_traits<typename iterator_traits<InputIterator>::value_type>,
                    Allocator>;
```

*Remarks:* Shall not participate in overload resolution if
`InputIterator` is a type that does not qualify as an input iterator, or
if `Allocator` is a type that does not qualify as an
allocator ( [[container.requirements.general]]).

``` cpp
basic_string& operator=(const basic_string& str);
```

*Effects:* If `*this` and `str` are not the same object, modifies
`*this` as shown in Table  [[tab:strings.op=]].

If `*this` and `str` are the same object, the member has no effect.

*Returns:* `*this`.

**Table: `operator=(const basic_string&)` effects**

| Element      | Value                                                                                                           |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| `data()`     | points at the first element of an allocated copy of the array whose first element is pointed at by `str.data()` |
| `size()`     | `str.size()`                                                                                                    |
| `capacity()` | a value at least as large as `size()`                                                                           |

``` cpp
basic_string& operator=(basic_string&& str)
  noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Effects:* Move assigns as a sequence
container ( [[container.requirements]]), except that iterators, pointers
and references may be invalidated.

*Returns:* `*this`.

``` cpp
basic_string& operator=(basic_string_view<charT, traits> sv);
```

*Effects:* Equivalent to: `return assign(sv);`

``` cpp
basic_string& operator=(const charT* s);
```

*Returns:* `*this = basic_string(s)`.

*Remarks:* Uses `traits::length()`.

``` cpp
basic_string& operator=(charT c);
```

*Returns:* `*this = basic_string(1, c)`.

``` cpp
basic_string& operator=(initializer_list<charT> il);
```

*Effects:* As if by: `*this = basic_string(il);`

*Returns:* `*this`.

#### `basic_string` iterator support <a id="string.iterators">[[string.iterators]]</a>

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

#### `basic_string` capacity <a id="string.capacity">[[string.capacity]]</a>

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

*Returns:* The largest possible number of char-like objects that can be
stored in a `basic_string`.

*Complexity:* Constant time.

``` cpp
void resize(size_type n, charT c);
```

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

*Effects:* As if by `resize(n, charT())`.

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
argument of `reserve`.

[*Note 1*: Calling `reserve()` with a `res_arg` argument less than
`capacity()` is in effect a non-binding shrink request. A call with
`res_arg <= size()` is in effect a non-binding shrink-to-fit
request. — *end note*\]

*Throws:* `length_error` if `res_arg > max_size()`.[^4]

``` cpp
void shrink_to_fit();
```

*Effects:* `shrink_to_fit` is a non-binding request to reduce
`capacity()` to `size()`.

[*Note 2*: The request is non-binding to allow latitude for
implementation-specific optimizations. — *end note*\]

It does not increase `capacity()`, but may reduce `capacity()` by
causing reallocation.

*Complexity:* Linear in the size of the sequence.

*Remarks:* Reallocation invalidates all the references, pointers, and
iterators referring to the elements in the sequence as well as the
past-the-end iterator. If no reallocation happens, they remain valid.

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

#### `basic_string` element access <a id="string.access">[[string.access]]</a>

``` cpp
const_reference operator[](size_type pos) const;
reference       operator[](size_type pos);
```

*Requires:* `pos <= size()`.

*Returns:* `*(begin() + pos)` if `pos < size()`. Otherwise, returns a
reference to an object of type `charT` with value `charT()`, where
modifying the object to any value other than `charT()` leads to
undefined behavior.

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

*Requires:* `!empty()`.

*Effects:* Equivalent to: `return operator[](0);`

``` cpp
const charT& back() const;
charT& back();
```

*Requires:* `!empty()`.

*Effects:* Equivalent to: `return operator[](size() - 1);`

#### `basic_string` modifiers <a id="string.modifiers">[[string.modifiers]]</a>

##### `basic_string::operator+=` <a id="string.op+=">[[string.op+=]]</a>

``` cpp
basic_string&
  operator+=(const basic_string& str);
```

*Effects:* Calls `append(str)`.

*Returns:* `*this`.

``` cpp
basic_string& operator+=(basic_string_view<charT, traits> sv);
```

*Effects:* Calls `append(sv)`.

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

##### `basic_string::append` <a id="string.append">[[string.append]]</a>

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

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to
append as the smaller of `n` and `str``.size() - ``pos` and calls
`append(str.data() + pos, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string& append(basic_string_view<charT, traits> sv);
```

*Effects:* Equivalent to: `return append(sv.data(), sv.size());`

``` cpp
template<class T>
  basic_string& append(const T& t, size_type pos, size_type n = npos);
```

*Throws:* `out_of_range` if `pos > sv.size()`.

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t`. Determines the effective
length `rlen` of the string to append as the smaller of `n` and
`sv.size() - pos` and calls `append(sv.data() + pos, rlen)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true` and `is_convertible_v<const T&, const charT*>` is `false`.

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

*Effects:* Equivalent to
`append(basic_string(first, last, get_allocator()))`.

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

##### `basic_string::assign` <a id="string.assign">[[string.assign]]</a>

``` cpp
basic_string& assign(const basic_string& str);
```

*Effects:* Equivalent to `*this = str`.

*Returns:* `*this`.

``` cpp
basic_string& assign(basic_string&& str)
  noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Effects:* Equivalent to `*this = std::move(str)`.

*Returns:* `*this`.

``` cpp
basic_string&
  assign(const basic_string& str, size_type pos,
         size_type n = npos);
```

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to
assign as the smaller of `n` and `str``.size() - ``pos` and calls
`assign(str.data() + pos, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string& assign(basic_string_view<charT, traits> sv);
```

*Effects:* Equivalent to: `return assign(sv.data(), sv.size());`

``` cpp
template<class T>
  basic_string& assign(const T& t, size_type pos, size_type n = npos);
```

*Throws:* `out_of_range` if `pos > sv.size()`.

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t`. Determines the effective
length `rlen` of the string to assign as the smaller of `n` and
`sv.size() - pos` and calls `assign(sv.data() + pos, rlen)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true` and `is_convertible_v<const T&, const charT*>` is `false`.

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

*Effects:* Equivalent to
`assign(basic_string(first, last, get_allocator()))`.

*Returns:* `*this`.

##### `basic_string::insert` <a id="string.insert">[[string.insert]]</a>

``` cpp
basic_string&
  insert(size_type pos,
         const basic_string& str);
```

*Effects:* Equivalent to: `return insert(pos, str.data(), str.size());`

``` cpp
basic_string&
  insert(size_type pos1,
         const basic_string& str,
         size_type pos2, size_type n = npos);
```

*Throws:* `out_of_range` if `pos1 > size()` or `pos2 > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to
insert as the smaller of `n` and `str.size() - pos2` and calls
`insert(pos1, str.data() + pos2, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string& insert(size_type pos, basic_string_view<charT, traits> sv);
```

*Effects:* Equivalent to: `return insert(pos, sv.data(), sv.size());`

``` cpp
template<class T>
  basic_string& insert(size_type pos1, const T& t,
                       size_type pos2, size_type n = npos);
```

*Throws:* `out_of_range` if `pos1 > size()` or `pos2 > sv.size()`.

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t`. Determines the effective
length `rlen` of the string to assign as the smaller of `n` and
`sv.size() - pos2` and calls `insert(pos1, sv.data() + pos2, rlen)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true` and `is_convertible_v<const T&, const charT*>` is `false`.

*Returns:* `*this`.

``` cpp
basic_string&
  insert(size_type pos, const charT* s, size_type n);
```

*Requires:* `s` points to an array of at least `n` elements of `charT`.

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

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Effects:* Equivalent to: `return insert(pos, s, traits::length(s));`

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

*Effects:* Inserts a copy of `c` before the character referred to by
`p`.

*Returns:* An iterator which refers to the copy of the inserted
character.

``` cpp
iterator insert(const_iterator p, size_type n, charT c);
```

*Requires:* `p` is a valid iterator on `*this`.

*Effects:* Inserts `n` copies of `c` before the character referred to by
`p`.

*Returns:* An iterator which refers to the copy of the first inserted
character, or `p` if `n == 0`.

``` cpp
template<class InputIterator>
  iterator insert(const_iterator p, InputIterator first, InputIterator last);
```

*Requires:* `p` is a valid iterator on `*this`. `[first, last)` is a
valid range.

*Effects:* Equivalent to
`insert(p - begin(), basic_string(first, last, get_allocator()))`.

*Returns:* An iterator which refers to the copy of the first inserted
character, or `p` if `first == last`.

``` cpp
iterator insert(const_iterator p, initializer_list<charT> il);
```

*Effects:* As if by `insert(p, il.begin(), il.end())`.

*Returns:* An iterator which refers to the copy of the first inserted
character, or `p` if `i1` is empty.

##### `basic_string::erase` <a id="string.erase">[[string.erase]]</a>

``` cpp
basic_string& erase(size_type pos = 0, size_type n = npos);
```

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

*Effects:* Removes the character referred to by `p`.

*Returns:* An iterator which points to the element immediately following
`p` prior to the element being erased. If no such element exists,
`end()` is returned.

``` cpp
iterator erase(const_iterator first, const_iterator last);
```

*Requires:* `first` and `last` are valid iterators on `*this`, defining
a range `[first, last)`.

*Throws:* Nothing.

*Effects:* Removes the characters in the range `[first, last)`.

*Returns:* An iterator which points to the element pointed to by `last`
prior to the other elements being erased. If no such element exists,
`end()` is returned.

``` cpp
void pop_back();
```

*Requires:* `!empty()`.

*Throws:* Nothing.

*Effects:* Equivalent to `erase(size() - 1, 1)`.

##### `basic_string::replace` <a id="string.replace">[[string.replace]]</a>

``` cpp
basic_string&
  replace(size_type pos1, size_type n1,
          const basic_string& str);
```

*Effects:* Equivalent to:
`return replace(pos1, n1, str.data(), str.size());`

``` cpp
basic_string&
  replace(size_type pos1, size_type n1,
          const basic_string& str,
          size_type pos2, size_type n2 = npos);
```

*Throws:* `out_of_range` if `pos1 > size()` or `pos2 > str.size()`.

*Effects:* Determines the effective length `rlen` of the string to be
inserted as the smaller of `n2` and `str.size() - pos2` and calls
`replace(pos1, n1, str.data() + pos2, rlen)`.

*Returns:* `*this`.

``` cpp
basic_string& replace(size_type pos1, size_type n1,
                      basic_string_view<charT, traits> sv);
```

*Effects:* Equivalent to:
`return replace(pos1, n1, sv.data(), sv.size());`

``` cpp
template<class T>
  basic_string& replace(size_type pos1, size_type n1, const T& t,
                        size_type pos2, size_type n2 = npos);
```

*Throws:* `out_of_range` if `pos1 > size()` or `pos2 > sv.size()`.

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t`. Determines the effective
length `rlen` of the string to be inserted as the smaller of `n2` and
`sv.size() - pos2` and calls
`replace(pos1, n1, sv.data() + pos2, rlen)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true` and `is_convertible_v<const T&, const charT*>` is `false`.

*Returns:* `*this`.

``` cpp
basic_string&
  replace(size_type pos1, size_type n1, const charT* s, size_type n2);
```

*Requires:* `s` points to an array of at least `n2` elements of `charT`.

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

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Effects:* Equivalent to:
`return replace(pos, n, s, traits::length(s));`

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
basic_string& replace(const_iterator i1, const_iterator i2,
                      basic_string_view<charT, traits> sv);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Calls `replace(i1 - begin(), i2 - i1, sv)`.

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

*Effects:* Calls
`replace(i1 - begin(), i2 - i1, basic_string(j1, j2, get_allocator()))`.

*Returns:* `*this`.

``` cpp
basic_string& replace(const_iterator i1, const_iterator i2,
                      initializer_list<charT> il);
```

*Requires:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Calls
`replace(i1 - begin(), i2 - i1, il.begin(), il.size())`.

*Returns:* `*this`.

##### `basic_string::copy` <a id="string.copy">[[string.copy]]</a>

``` cpp
size_type copy(charT* s, size_type n, size_type pos = 0) const;
```

Let `rlen` be the smaller of `n` and `size() - pos`.

*Throws:* `out_of_range` if `pos > size()`.

*Requires:* \[`s`, `s + rlen`) is a valid range.

*Effects:* Equivalent to: `traits::copy(s, data() + pos, rlen)`.

[*Note 1*: This does not terminate `s` with a null
object. — *end note*\]

*Returns:* `rlen`.

##### `basic_string::swap` <a id="string.swap">[[string.swap]]</a>

``` cpp
void swap(basic_string& s)
  noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Postconditions:* `*this` contains the same sequence of characters that
was in `s`, `s` contains the same sequence of characters that was in
`*this`.

*Throws:* Nothing.

*Complexity:* Constant time.

#### `basic_string` string operations <a id="string.ops">[[string.ops]]</a>

##### `basic_string` accessors <a id="string.accessors">[[string.accessors]]</a>

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
charT* data() noexcept;
```

*Returns:* A pointer `p` such that `p + i == &operator[](i)` for each
`i` in \[`0`, `size()`\].

*Complexity:* Constant time.

*Requires:* The program shall not alter the value stored at
`p + size()`.

``` cpp
operator basic_string_view<charT, traits>() const noexcept;
```

*Effects:* Equivalent to:
`return basic_string_view<charT, traits>(data(), size());`

``` cpp
allocator_type get_allocator() const noexcept;
```

*Returns:* A copy of the `Allocator` object used to construct the string
or, if that allocator has been replaced, a copy of the most recent
replacement.

##### `basic_string::find` <a id="string.find">[[string.find]]</a>

``` cpp
size_type find(basic_string_view<charT, traits> sv, size_type pos = 0) const noexcept;
```

*Effects:* Determines the lowest position `xpos`, if possible, such that
both of the following conditions hold:

- `pos <= xpos` and `xpos + sv.size() <= size()`;
- `traits::eq(at(xpos + I), sv.at(I))` for all elements `I` of the data
  referenced by `sv`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
size_type find(const basic_string& str, size_type pos = 0) const noexcept;
```

*Effects:* Equivalent to:
`return find(basic_string_view<charT, traits>(str), pos);`

``` cpp
size_type find(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find(basic_string_view<charT, traits>(s, n), pos)`.

``` cpp
size_type find(const charT* s, size_type pos = 0) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find(basic_string_view<charT, traits>(s), pos)`.

``` cpp
size_type find(charT c, size_type pos = 0) const;
```

*Returns:* `find(basic_string(1, c), pos)`.

##### `basic_string::rfind` <a id="string.rfind">[[string.rfind]]</a>

``` cpp
size_type rfind(basic_string_view<charT, traits> sv, size_type pos = npos) const noexcept;
```

*Effects:* Determines the highest position `xpos`, if possible, such
that both of the following conditions hold:

- `xpos <= pos` and `xpos + sv.size() <= size()`;
- `traits::eq(at(xpos + I), sv.at(I))` for all elements `I` of the data
  referenced by `sv`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
size_type rfind(const basic_string& str, size_type pos = npos) const noexcept;
```

*Effects:* Equivalent to:
`return rfind(basic_string_view<charT, traits>(str), pos);`

``` cpp
size_type rfind(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `rfind(basic_string_view<charT, traits>(s, n), pos)`.

``` cpp
size_type rfind(const charT* s, size_type pos = npos) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `rfind(basic_string_view<charT, traits>(s), pos)`.

``` cpp
size_type rfind(charT c, size_type pos = npos) const;
```

*Returns:* `rfind(basic_string(1, c), pos)`.

##### `basic_string::find_first_of` <a id="string.find.first.of">[[string.find.first.of]]</a>

``` cpp
size_type find_first_of(basic_string_view<charT, traits> sv, size_type pos = 0) const noexcept;
```

*Effects:* Determines the lowest position `xpos`, if possible, such that
both of the following conditions hold:

- `pos <= xpos` and `xpos < size()`;
- `traits::eq(at(xpos), sv.at(I))` for some element `I` of the data
  referenced by `sv`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
size_type find_first_of(const basic_string& str, size_type pos = 0) const noexcept;
```

*Effects:* Equivalent to:
`return find_first_of(basic_string_view<charT, traits>(str), pos);`

``` cpp
size_type find_first_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find_first_of(basic_string_view<charT, traits>(s, n), pos)`.

``` cpp
size_type find_first_of(const charT* s, size_type pos = 0) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_first_of(basic_string_view<charT, traits>(s), pos)`.

``` cpp
size_type find_first_of(charT c, size_type pos = 0) const;
```

*Returns:* `find_first_of(basic_string(1, c), pos)`.

##### `basic_string::find_last_of` <a id="string.find.last.of">[[string.find.last.of]]</a>

``` cpp
size_type find_last_of(basic_string_view<charT, traits> sv, size_type pos = npos) const noexcept;
```

*Effects:* Determines the highest position `xpos`, if possible, such
that both of the following conditions hold:

- `xpos <= pos` and `xpos < size()`;
- `traits::eq(at(xpos), sv.at(I))` for some element `I` of the data
  referenced by `sv`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
size_type find_last_of(const basic_string& str, size_type pos = npos) const noexcept;
```

*Effects:* Equivalent to:
`return find_last_of(basic_string_view<charT, traits>(str), pos);`

``` cpp
size_type find_last_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:* `find_last_of(basic_string_view<charT, traits>(s, n), pos)`.

``` cpp
size_type find_last_of(const charT* s, size_type pos = npos) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_last_of(basic_string_view<charT, traits>(s), pos)`.

``` cpp
size_type find_last_of(charT c, size_type pos = npos) const;
```

*Returns:* `find_last_of(basic_string(1, c), pos)`.

##### `basic_string::find_first_not_of` <a id="string.find.first.not.of">[[string.find.first.not.of]]</a>

``` cpp
size_type find_first_not_of(basic_string_view<charT, traits> sv,
                            size_type pos = 0) const noexcept;
```

*Effects:* Determines the lowest position `xpos`, if possible, such that
both of the following conditions hold:

- `pos <= xpos` and `xpos < size()`;
- `traits::eq(at(xpos), sv.at(I))` for no element `I` of the data
  referenced by `sv`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
size_type find_first_not_of(const basic_string& str, size_type pos = 0) const noexcept;
```

*Effects:* Equivalent to:

``` cpp
return find_first_not_of(basic_string_view<charT, traits>(str), pos);
```

``` cpp
size_type find_first_not_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:*
`find_first_not_of(basic_string_view<charT, traits>(s, n), pos)`.

``` cpp
size_type find_first_not_of(const charT* s, size_type pos = 0) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:*
`find_first_not_of(basic_string_view<charT, traits>(s), pos)`.

``` cpp
size_type find_first_not_of(charT c, size_type pos = 0) const;
```

*Returns:* `find_first_not_of(basic_string(1, c), pos)`.

##### `basic_string::find_last_not_of` <a id="string.find.last.not.of">[[string.find.last.not.of]]</a>

``` cpp
size_type find_last_not_of(basic_string_view<charT, traits> sv,
                           size_type pos = npos) const noexcept;
```

*Effects:* Determines the highest position `xpos`, if possible, such
that both of the following conditions hold:

- `xpos <= pos` and `xpos < size()`;
- `traits::eq(at(xpos), sv.at(I))` for no element `I` of the data
  referenced by `sv`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
size_type find_last_not_of(const basic_string& str, size_type pos = npos) const noexcept;
```

*Effects:* Equivalent to:

``` cpp
return find_last_not_of(basic_string_view<charT, traits>(str), pos);
```

``` cpp
size_type find_last_not_of(const charT* s, size_type pos, size_type n) const;
```

*Returns:*
`find_last_not_of(basic_string_view<charT, traits>(s, n), pos)`.

``` cpp
size_type find_last_not_of(const charT* s, size_type pos = npos) const;
```

*Requires:* `s` points to an array of at least `traits::length(s) + 1`
elements of `charT`.

*Returns:* `find_last_not_of(basic_string_view<charT, traits>(s), pos)`.

``` cpp
size_type find_last_not_of(charT c, size_type pos = npos) const;
```

*Returns:* `find_last_not_of(basic_string(1, c), pos)`.

##### `basic_string::substr` <a id="string.substr">[[string.substr]]</a>

``` cpp
basic_string substr(size_type pos = 0, size_type n = npos) const;
```

*Throws:* `out_of_range` if `pos > size()`.

*Effects:* Determines the effective length `rlen` of the string to copy
as the smaller of `n` and `size() - pos`.

*Returns:* `basic_string(data()+pos, rlen)`.

##### `basic_string::compare` <a id="string.compare">[[string.compare]]</a>

``` cpp
int compare(basic_string_view<charT, traits> sv) const noexcept;
```

*Effects:* Determines the effective length `rlen` of the strings to
compare as the smaller of `size()` and `sv.size()`. The function then
compares the two strings by calling
`traits::compare(data(), sv.data(), rlen)`.

*Returns:* The nonzero result if the result of the comparison is
nonzero. Otherwise, returns a value as indicated in
Table  [[tab:strings.compare]].

**Table: `compare()` results**

| Condition              | Return Value |
| ---------------------- | ------------ |
| `size() < \ sv.size()` | `< 0`        |
| `size() == sv.size()`  | ` \ 0`       |
| `size() > \ sv.size()` | `> 0`        |

``` cpp
int compare(size_type pos1, size_type n1, basic_string_view<charT, traits> sv) const;
```

*Effects:* Equivalent to:

``` cpp
return basic_string_view<charT, traits>(data(), size()).substr(pos1, n1).compare(sv);
```

``` cpp
template<class T>
  int compare(size_type pos1, size_type n1, const T& t,
              size_type pos2, size_type n2 = npos) const;
```

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return basic_string_view<charT, traits>(
    data(), size()).substr(pos1, n1).compare(sv.substr(pos2, n2));
```

*Remarks:* This function shall not participate in overload resolution
unless `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true` and `is_convertible_v<const T&, const charT*>` is `false`.

``` cpp
int compare(const basic_string& str) const noexcept;
```

*Effects:* Equivalent to:
`return compare(basic_string_view<charT, traits>(str));`

``` cpp
int compare(size_type pos1, size_type n1, const basic_string& str) const;
```

*Effects:* Equivalent to:
`return compare(pos1, n1, basic_string_view<charT, traits>(str));`

``` cpp
int compare(size_type pos1, size_type n1,
            const basic_string& str,
            size_type pos2, size_type n2 = npos) const;
```

*Effects:* Equivalent to:

``` cpp
return compare(pos1, n1, basic_string_view<charT, traits>(str), pos2, n2);
```

``` cpp
int compare(const charT* s) const;
```

*Returns:* `compare(basic_string(s))`.

``` cpp
int compare(size_type pos, size_type n1, const charT* s) const;
```

*Returns:* `basic_string(*this, pos, n1).compare(basic_string(s))`.

``` cpp
int compare(size_type pos, size_type n1, const charT* s, size_type n2) const;
```

*Returns:* `basic_string(*this, pos, n1).compare(basic_string(s, n2))`.

### `basic_string` non-member functions <a id="string.nonmembers">[[string.nonmembers]]</a>

#### `operator+` <a id="string.op+">[[string.op+]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `basic_string<charT, traits, Allocator>(lhs).append(rhs)`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `std::move(lhs.append(rhs))`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              basic_string<charT, traits, Allocator>&& rhs);
```

*Returns:* `std::move(rhs.insert(0, lhs))`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              basic_string<charT, traits, Allocator>&& rhs);
```

*Returns:* `std::move(lhs.append(rhs))`.

[*Note 1*: Or equivalently,
`std::move(rhs.insert(0, lhs))`. — *end note*\]

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(const charT* lhs,
              const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `basic_string<charT, traits, Allocator>(lhs) + rhs`.

*Remarks:* Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(const charT* lhs,
              basic_string<charT, traits, Allocator>&& rhs);
```

*Returns:* `std::move(rhs.insert(0, lhs))`.

*Remarks:* Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(charT lhs,
              const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `basic_string<charT, traits, Allocator>(1, lhs) + rhs`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(charT lhs,
              basic_string<charT, traits, Allocator>&& rhs);
```

*Returns:* `std::move(rhs.insert(0, 1, lhs))`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              const charT* rhs);
```

*Returns:* `lhs + basic_string<charT, traits, Allocator>(rhs)`.

*Remarks:* Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              const charT* rhs);
```

*Returns:* `std::move(lhs.append(rhs))`.

*Remarks:* Uses `traits::length()`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              charT rhs);
```

*Returns:* `lhs + basic_string<charT, traits, Allocator>(1, rhs)`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              charT rhs);
```

*Returns:* `std::move(lhs.append(1, rhs))`.

#### `operator==` <a id="string.operator==">[[string.operator==]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator==(const basic_string<charT, traits, Allocator>& lhs,
                  const basic_string<charT, traits, Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator==(const charT* lhs,
                  const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `rhs == lhs`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator==(const basic_string<charT, traits, Allocator>& lhs,
                  const charT* rhs);
```

*Requires:* `rhs` points to an array of at least
`traits::length(rhs) + 1` elements of `charT`.

*Returns:* `lhs.compare(rhs) == 0`.

#### `operator!=` <a id="string.op!=">[[string.op!=]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator!=(const basic_string<charT, traits, Allocator>& lhs,
                  const basic_string<charT, traits, Allocator>& rhs) noexcept;
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator!=(const charT* lhs,
                  const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `rhs != lhs`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator!=(const basic_string<charT, traits, Allocator>& lhs,
                  const charT* rhs);
```

*Requires:* `rhs` points to an array of at least
`traits::length(rhs) + 1` elements of `charT`.

*Returns:* `lhs.compare(rhs) != 0`.

#### `operator<` <a id="string.op<">[[string.op<]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator< (const basic_string<charT, traits, Allocator>& lhs,
                  const basic_string<charT, traits, Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) < 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator< (const charT* lhs,
                  const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) > 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator< (const basic_string<charT, traits, Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) < 0`.

#### `operator>` <a id="string.op>">[[string.op>]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator> (const basic_string<charT, traits, Allocator>& lhs,
                  const basic_string<charT, traits, Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) > 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator> (const charT* lhs,
                  const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) < 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator> (const basic_string<charT, traits, Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) > 0`.

#### `operator<=` <a id="string.op<=">[[string.op<=]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator<=(const basic_string<charT, traits, Allocator>& lhs,
                  const basic_string<charT, traits, Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) <= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator<=(const charT* lhs,
                  const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) >= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator<=(const basic_string<charT, traits, Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) <= 0`.

#### `operator>=` <a id="string.op>=">[[string.op>=]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  bool operator>=(const basic_string<charT, traits, Allocator>& lhs,
                  const basic_string<charT, traits, Allocator>& rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) >= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator>=(const charT* lhs,
                  const basic_string<charT, traits, Allocator>& rhs);
```

*Returns:* `rhs.compare(lhs) <= 0`.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator>=(const basic_string<charT, traits, Allocator>& lhs,
                  const charT* rhs);
```

*Returns:* `lhs.compare(rhs) >= 0`.

#### `swap` <a id="string.special">[[string.special]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  void swap(basic_string<charT, traits, Allocator>& lhs,
            basic_string<charT, traits, Allocator>& rhs)
    noexcept(noexcept(lhs.swap(rhs)));
```

*Effects:* Equivalent to: `lhs.swap(rhs);`

#### Inserters and extractors <a id="string.io">[[string.io]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT, traits>&
    operator>>(basic_istream<charT, traits>& is,
               basic_string<charT, traits, Allocator>& str);
```

*Effects:* Behaves as a formatted input
function ( [[istream.formatted.reqmts]]). After constructing a `sentry`
object, if the sentry converts to `true`, calls `str.erase()` and then
extracts characters from `is` and appends them to `str` as if by calling
`str.append(1, c)`. If `is.width()` is greater than zero, the maximum
number `n` of characters appended is `is.width()`; otherwise `n` is
`str.max_size()`. Characters are extracted and appended until any of the
following occurs:

- *n* characters are stored;
- end-of-file occurs on the input sequence;
- `isspace(c, is.getloc())` is `true` for the next available input
  character *c*.

After the last character (if any) is extracted, `is.width(0)` is called
and the `sentry` object is destroyed.

If the function extracts no characters, it calls
`is.setstate(ios::failbit)`, which may throw
`ios_base::failure` ( [[iostate.flags]]).

*Returns:* `is`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os,
               const basic_string<charT, traits, Allocator>& str);
```

*Effects:* Equivalent to:
`return os << basic_string_view<charT, traits>(str);`

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT, traits>&
    getline(basic_istream<charT, traits>& is,
            basic_string<charT, traits, Allocator>& str,
            charT delim);
template<class charT, class traits, class Allocator>
  basic_istream<charT, traits>&
    getline(basic_istream<charT, traits>&& is,
            basic_string<charT, traits, Allocator>& str,
            charT delim);
```

*Effects:* Behaves as an unformatted input
function ( [[istream.unformatted]]), except that it does not affect the
value returned by subsequent calls to `basic_istream<>::gcount()`. After
constructing a `sentry` object, if the sentry converts to `true`, calls
`str.erase()` and then extracts characters from `is` and appends them to
`str` as if by calling `str.append(1, c)` until any of the following
occurs:

- end-of-file occurs on the input sequence (in which case, the `getline`
  function calls `is.setstate(ios_base::eofbit)`).
- `traits::eq(c, delim)` for the next available input character *c* (in
  which case, *c* is extracted but not appended) ( [[iostate.flags]])
- `str.max_size()` characters are stored (in which case, the function
  calls `is.setstate(ios_base::failbit))` ( [[iostate.flags]])

The conditions are tested in the order shown. In any case, after the
last character is extracted, the `sentry` object is destroyed.

If the function extracts no characters, it calls
`is.setstate(ios_base::failbit)` which may throw
`ios_base::failure` ( [[iostate.flags]]).

*Returns:* `is`.

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT, traits>&
    getline(basic_istream<charT, traits>& is,
            basic_string<charT, traits, Allocator>& str);
template<class charT, class traits, class Allocator>
  basic_istream<charT, traits>&
    getline(basic_istream<charT, traits>&& is,
            basic_string<charT, traits, Allocator>& str);
```

*Returns:* `getline(is, str, is.widen(’\n’))`.

### Numeric conversions <a id="string.conversions">[[string.conversions]]</a>

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

*Effects:* These functions call `strtof(str.c_str(), ptr)`,
`strtod(str.c_str(), ptr)`, and `strtold(str.c_str(), ptr)`,
respectively. Each function returns the converted result, if any. The
argument `ptr` designates a pointer to an object internal to the
function that is used to determine what to store at `*idx`. If the
function does not throw an exception and `idx != 0`, the function stores
in `*idx` the index of the first unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `strtof`, `strtod`, or `strtold` reports
that no conversion could be performed. Throws `out_of_range` if
`strtof`, `strtod`, or `strtold` sets `errno` to `ERANGE` or if the
converted value is outside the range of representable values for the
return type.

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

*Effects:* These functions call `wcstof(str.c_str(), ptr)`,
`wcstod(str.c_str(), ptr)`, and `wcstold(str.c_str(), ptr)`,
respectively. Each function returns the converted result, if any. The
argument `ptr` designates a pointer to an object internal to the
function that is used to determine what to store at `*idx`. If the
function does not throw an exception and `idx != 0`, the function stores
in `*idx` the index of the first unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `wcstof`, `wcstod`, or `wcstold` reports
that no conversion could be performed. Throws `out_of_range` if
`wcstof`, `wcstod`, or `wcstold` sets `errno` to `ERANGE`.

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

### Hash support <a id="basic.string.hash">[[basic.string.hash]]</a>

``` cpp
template<> struct hash<string>;
template<> struct hash<u16string>;
template<> struct hash<u32string>;
template<> struct hash<wstring>;
```

If `S` is one of these string types, `SV` is the corresponding string
view type, and `s` is an object of type `S`, then
`hash<S>()(s) == hash<SV>()(SV(s))`.

### Suffix for `basic_string` literals <a id="basic.string.literals">[[basic.string.literals]]</a>

``` cpp
string operator""s(const char* str, size_t len);
```

*Returns:* `string{str, len}`.

``` cpp
u16string operator""s(const char16_t* str, size_t len);
```

*Returns:* `u16string{str, len}`.

``` cpp
u32string operator""s(const char32_t* str, size_t len);
```

*Returns:* `u32string{str, len}`.

``` cpp
wstring operator""s(const wchar_t* str, size_t len);
```

*Returns:* `wstring{str, len}`.

[*Note 1*: The same suffix `s` is used for `chrono::duration` literals
denoting seconds but there is no conflict, since duration suffixes apply
to numbers and string literal suffixes apply to character array
literals. — *end note*\]

## String view classes <a id="string.view">[[string.view]]</a>

The class template `basic_string_view` describes an object that can
refer to a constant contiguous sequence of char-like (
[[strings.general]]) objects with the first element of the sequence at
position zero. In the rest of this section, the type of the char-like
objects held in a `basic_string_view` object is designated by `charT`.

[*Note 1*: The library provides implicit conversions from
`const charT*` and `std::basic_string<charT, ...>` to
`std::basic_string_view<charT, ...>` so that user code can accept just
`std::basic_string_view<charT>` as a non-templated parameter wherever a
sequence of characters is expected. User-defined types should define
their own implicit conversions to `std::basic_string_view` in order to
interoperate with these functions. — *end note*\]

The complexity of `basic_string_view` member functions is unless
otherwise specified.

### Header `<string_view>` synopsis <a id="string.view.synop">[[string.view.synop]]</a>

``` cpp
namespace std {
  // [string.view.template], class template basic_string_view
  template<class charT, class traits = char_traits<charT>>
  class basic_string_view;

  // [string.view.comparison], non-member comparison functions
  template<class charT, class traits>
    constexpr bool operator==(basic_string_view<charT, traits> x,
                              basic_string_view<charT, traits> y) noexcept;
  template<class charT, class traits>
    constexpr bool operator!=(basic_string_view<charT, traits> x,
                              basic_string_view<charT, traits> y) noexcept;
  template<class charT, class traits>
    constexpr bool operator< (basic_string_view<charT, traits> x,
                              basic_string_view<charT, traits> y) noexcept;
  template<class charT, class traits>
    constexpr bool operator> (basic_string_view<charT, traits> x,
                              basic_string_view<charT, traits> y) noexcept;
  template<class charT, class traits>
    constexpr bool operator<=(basic_string_view<charT, traits> x,
                              basic_string_view<charT, traits> y) noexcept;
  template<class charT, class traits>
    constexpr bool operator>=(basic_string_view<charT, traits> x,
                              basic_string_view<charT, traits> y) noexcept;
  // see [string.view.comparison], sufficient additional overloads of comparison functions

  // [string.view.io], inserters and extractors
  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os,
                 basic_string_view<charT, traits> str);

  // basic_string_view typedef names
  using string_view    = basic_string_view<char>;
  using u16string_view = basic_string_view<char16_t>;
  using u32string_view = basic_string_view<char32_t>;
  using wstring_view   = basic_string_view<wchar_t>;

  // [string.view.hash], hash support
  template<class T> struct hash;
  template<> struct hash<string_view>;
  template<> struct hash<u16string_view>;
  template<> struct hash<u32string_view>;
  template<> struct hash<wstring_view>;

  inline namespace literals {
  inline namespace string_view_literals {
    // [string.view.literals], suffix for basic_string_view literals
    constexpr string_view    operator""sv(const char* str, size_t len) noexcept;
    constexpr u16string_view operator""sv(const char16_t* str, size_t len) noexcept;
    constexpr u32string_view operator""sv(const char32_t* str, size_t len) noexcept;
    constexpr wstring_view   operator""sv(const wchar_t* str, size_t len) noexcept;
  }
  }
}
```

The function templates defined in [[utility.swap]] and
[[iterator.range]] are available when `<string_view>` is included.

### Class template `basic_string_view` <a id="string.view.template">[[string.view.template]]</a>

``` cpp
template<class charT, class traits = char_traits<charT>>
class basic_string_view {
public:
  // types
  using traits_type            = traits;
  using value_type             = charT;
  using pointer                = value_type*;
  using const_pointer          = const value_type*;
  using reference              = value_type&;
  using const_reference        = const value_type&;
  using const_iterator         = implementation-defined  // type of basic_string_view::const_iterator; // see [string.view.iterators]
  using iterator               = const_iterator;\footnote{Because basic_string_view refers to a constant sequence, iterator and const_iterator are the same type.}
  using const_reverse_iterator = reverse_iterator<const_iterator>;
  using reverse_iterator       = const_reverse_iterator;
  using size_type              = size_t;
  using difference_type        = ptrdiff_t;
  static constexpr size_type npos = size_type(-1);

  // [string.view.cons], construction and assignment
  constexpr basic_string_view() noexcept;
  constexpr basic_string_view(const basic_string_view&) noexcept = default;
  constexpr basic_string_view& operator=(const basic_string_view&) noexcept = default;
  constexpr basic_string_view(const charT* str);
  constexpr basic_string_view(const charT* str, size_type len);

  // [string.view.iterators], iterator support
  constexpr const_iterator begin() const noexcept;
  constexpr const_iterator end() const noexcept;
  constexpr const_iterator cbegin() const noexcept;
  constexpr const_iterator cend() const noexcept;
  constexpr const_reverse_iterator rbegin() const noexcept;
  constexpr const_reverse_iterator rend() const noexcept;
  constexpr const_reverse_iterator crbegin() const noexcept;
  constexpr const_reverse_iterator crend() const noexcept;

  // [string.view.capacity], capacity
  constexpr size_type size() const noexcept;
  constexpr size_type length() const noexcept;
  constexpr size_type max_size() const noexcept;
  constexpr bool empty() const noexcept;

  // [string.view.access], element access
  constexpr const_reference operator[](size_type pos) const;
  constexpr const_reference at(size_type pos) const;
  constexpr const_reference front() const;
  constexpr const_reference back() const;
  constexpr const_pointer data() const noexcept;

  // [string.view.modifiers], modifiers
  constexpr void remove_prefix(size_type n);
  constexpr void remove_suffix(size_type n);
  constexpr void swap(basic_string_view& s) noexcept;

  // [string.view.ops], string operations
  size_type copy(charT* s, size_type n, size_type pos = 0) const;

  constexpr basic_string_view substr(size_type pos = 0, size_type n = npos) const;
  constexpr int compare(basic_string_view s) const noexcept;
  constexpr int compare(size_type pos1, size_type n1, basic_string_view s) const;
  constexpr int compare(size_type pos1, size_type n1, basic_string_view s,
                        size_type pos2, size_type n2) const;
  constexpr int compare(const charT* s) const;
  constexpr int compare(size_type pos1, size_type n1, const charT* s) const;
  constexpr int compare(size_type pos1, size_type n1, const charT* s,
                        size_type n2) const;
  constexpr size_type find(basic_string_view s, size_type pos = 0) const noexcept;
  constexpr size_type find(charT c, size_type pos = 0) const noexcept;
  constexpr size_type find(const charT* s, size_type pos, size_type n) const;
  constexpr size_type find(const charT* s, size_type pos = 0) const;
  constexpr size_type rfind(basic_string_view s, size_type pos = npos) const noexcept;
  constexpr size_type rfind(charT c, size_type pos = npos) const noexcept;
  constexpr size_type rfind(const charT* s, size_type pos, size_type n) const;
  constexpr size_type rfind(const charT* s, size_type pos = npos) const;
  constexpr size_type find_first_of(basic_string_view s, size_type pos = 0) const noexcept;
  constexpr size_type find_first_of(charT c, size_type pos = 0) const noexcept;
  constexpr size_type find_first_of(const charT* s, size_type pos, size_type n) const;
  constexpr size_type find_first_of(const charT* s, size_type pos = 0) const;
  constexpr size_type find_last_of(basic_string_view s, size_type pos = npos) const noexcept;
  constexpr size_type find_last_of(charT c, size_type pos = npos) const noexcept;
  constexpr size_type find_last_of(const charT* s, size_type pos, size_type n) const;
  constexpr size_type find_last_of(const charT* s, size_type pos = npos) const;
  constexpr size_type find_first_not_of(basic_string_view s, size_type pos = 0) const noexcept;
  constexpr size_type find_first_not_of(charT c, size_type pos = 0) const noexcept;
  constexpr size_type find_first_not_of(const charT* s, size_type pos,
                                        size_type n) const;
  constexpr size_type find_first_not_of(const charT* s, size_type pos = 0) const;
  constexpr size_type find_last_not_of(basic_string_view s,
                                       size_type pos = npos) const noexcept;
  constexpr size_type find_last_not_of(charT c, size_type pos = npos) const noexcept;
  constexpr size_type find_last_not_of(const charT* s, size_type pos,
                                       size_type n) const;
  constexpr size_type find_last_not_of(const charT* s, size_type pos = npos) const;

private:
  const_pointer data_; // exposition only
  size_type size_;     // exposition only
};
```

In every specialization `basic_string_view<charT, traits>`, the type
`traits` shall satisfy the character traits requirements (
[[char.traits]]), and the type `traits::char_type` shall name the same
type as `charT`.

#### Construction and assignment <a id="string.view.cons">[[string.view.cons]]</a>

``` cpp
constexpr basic_string_view() noexcept;
```

*Effects:* Constructs an empty `basic_string_view`.

*Postconditions:* `size_ == 0` and `data_ == nullptr`.

``` cpp
constexpr basic_string_view(const charT* str);
```

*Requires:* \[`str`, `str + traits::length(str)`) is a valid range.

*Effects:* Constructs a `basic_string_view`, with the postconditions in
Table  [[tab:string.view.ctr.2]].

*Complexity:* 𝑂(`traits::length(str)`).

``` cpp
constexpr basic_string_view(const charT* str, size_type len);
```

*Requires:* \[`str`, `str + len`) is a valid range.

*Effects:* Constructs a `basic_string_view`, with the postconditions in
Table  [[tab:string.view.ctr.3]].

#### Iterator support <a id="string.view.iterators">[[string.view.iterators]]</a>

``` cpp
using const_iterator = implementation-defined  // type of basic_string_view::const_iterator;
```

A type that meets the requirements of a constant random access
iterator ( [[random.access.iterators]]) and of a contiguous
iterator ( [[iterator.requirements.general]]) whose `value_type` is the
template parameter `charT`.

For a `basic_string_view str`, any operation that invalidates a pointer
in the range \[`str.data()`, `str.data() + str.size()`) invalidates
pointers, iterators, and references returned from `str`’s methods.

All requirements on container iterators ( [[container.requirements]])
apply to `basic_string_view::const_iterator` as well.

``` cpp
constexpr const_iterator begin() const noexcept;
constexpr const_iterator cbegin() const noexcept;
```

*Returns:* An iterator such that

- if `!empty()`, `&*begin() == data_`,
- otherwise, an unspecified value such that \[`begin()`, `end()`) is a
  valid range.

``` cpp
constexpr const_iterator end() const noexcept;
constexpr const_iterator cend() const noexcept;
```

*Returns:* `begin() + size()`.

``` cpp
constexpr const_reverse_iterator rbegin() const noexcept;
constexpr const_reverse_iterator crbegin() const noexcept;
```

*Returns:* `const_reverse_iterator(end())`.

``` cpp
constexpr const_reverse_iterator rend() const noexcept;
constexpr const_reverse_iterator crend() const noexcept;
```

*Returns:* `const_reverse_iterator(begin())`.

#### Capacity <a id="string.view.capacity">[[string.view.capacity]]</a>

``` cpp
constexpr size_type size() const noexcept;
```

*Returns:* `size_`.

``` cpp
constexpr size_type length() const noexcept;
```

*Returns:* `size_`.

``` cpp
constexpr size_type max_size() const noexcept;
```

*Returns:* The largest possible number of char-like objects that can be
referred to by a `basic_string_view`.

``` cpp
constexpr bool empty() const noexcept;
```

*Returns:* `size_ == 0`.

#### Element access <a id="string.view.access">[[string.view.access]]</a>

``` cpp
constexpr const_reference operator[](size_type pos) const;
```

*Requires:* `pos < size()`.

*Returns:* `data_[pos]`.

*Throws:* Nothing.

[*Note 1*: Unlike `basic_string::operator[]`,
`basic_string_view::operator[](size())` has undefined behavior instead
of returning `charT()`. — *end note*\]

``` cpp
constexpr const_reference at(size_type pos) const;
```

*Throws:* `out_of_range` if `pos >= size()`.

*Returns:* `data_[pos]`.

``` cpp
constexpr const_reference front() const;
```

*Requires:* `!empty()`.

*Returns:* `data_[0]`.

*Throws:* Nothing.

``` cpp
constexpr const_reference back() const;
```

*Requires:* `!empty()`.

*Returns:* `data_[size() - 1]`.

*Throws:* Nothing.

``` cpp
constexpr const_pointer data() const noexcept;
```

*Returns:* `data_`.

[*Note 2*: Unlike `basic_string::data()` and string literals, `data()`
may return a pointer to a buffer that is not null-terminated. Therefore
it is typically a mistake to pass `data()` to a function that takes just
a `const charT*` and expects a null-terminated string. — *end note*\]

#### Modifiers <a id="string.view.modifiers">[[string.view.modifiers]]</a>

``` cpp
constexpr void remove_prefix(size_type n);
```

*Requires:* `n <= size()`.

*Effects:* Equivalent to: `data_ += n; size_ -= n;`

``` cpp
constexpr void remove_suffix(size_type n);
```

*Requires:* `n <= size()`.

*Effects:* Equivalent to: `size_ -= n;`

``` cpp
constexpr void swap(basic_string_view& s) noexcept;
```

*Effects:* Exchanges the values of `*this` and `s`.

#### String operations <a id="string.view.ops">[[string.view.ops]]</a>

``` cpp
size_type copy(charT* s, size_type n, size_type pos = 0) const;
```

Let `rlen` be the smaller of `n` and `size() - pos`.

*Throws:* `out_of_range` if `pos > size()`.

*Requires:* \[`s`, `s + rlen`) is a valid range.

*Effects:* Equivalent to `traits::copy(s, data() + pos, rlen)`.

*Returns:* `rlen`.

*Complexity:* 𝑂(`rlen`).

``` cpp
constexpr basic_string_view substr(size_type pos = 0, size_type n = npos) const;
```

Let `rlen` be the smaller of `n` and `size() - pos`.

*Throws:* `out_of_range` if `pos > size()`.

*Effects:* Determines `rlen`, the effective length of the string to
reference.

*Returns:* `basic_string_view(data() + pos, rlen)`.

``` cpp
constexpr int compare(basic_string_view str) const noexcept;
```

Let `rlen` be the smaller of `size()` and `str.size()`.

*Effects:* Determines `rlen`, the effective length of the strings to
compare. The function then compares the two strings by calling
`traits::compare(data(), str.data(), rlen)`.

*Complexity:* 𝑂(`rlen`).

*Returns:* The nonzero result if the result of the comparison is
nonzero. Otherwise, returns a value as indicated in
Table  [[tab:string.view.compare]].

**Table: `compare()` results**

| Condition              | Return Value |
| ---------------------- | ------------ |
| `size() < str.size()`  | `< 0`        |
| `size() == str.size()` | ` \ 0`       |
| `size() > str.size()`  | `> 0`        |

``` cpp
constexpr int compare(size_type pos1, size_type n1, basic_string_view str) const;
```

*Effects:* Equivalent to: `return substr(pos1, n1).compare(str);`

``` cpp
constexpr int compare(size_type pos1, size_type n1, basic_string_view str,
                      size_type pos2, size_type n2) const;
```

*Effects:* Equivalent to:
`return substr(pos1, n1).compare(str.substr(pos2, n2));`

``` cpp
constexpr int compare(const charT* s) const;
```

*Effects:* Equivalent to: `return compare(basic_string_view(s));`

``` cpp
constexpr int compare(size_type pos1, size_type n1, const charT* s) const;
```

*Effects:* Equivalent to:
`return substr(pos1, n1).compare(basic_string_view(s));`

``` cpp
constexpr int compare(size_type pos1, size_type n1,
                      const charT* s, size_type n2) const;
```

*Effects:* Equivalent to:
`return substr(pos1, n1).compare(basic_string_view(s, n2));`

#### Searching <a id="string.view.find">[[string.view.find]]</a>

This section specifies the `basic_string_view` member functions named
`find`, `rfind`, `find_first_of`, `find_last_of`, `find_first_not_of`,
and `find_last_not_of`.

Member functions in this section have complexity
\bigoh{\texttt{size() \* str.size()}} at worst, although implementations
are encouraged to do better.

Each member function of the form

``` cpp
constexpr return-type F(const charT* s, size_type pos);
```

is equivalent to `return F(basic_string_view(s), pos);`

Each member function of the form

``` cpp
constexpr return-type F(const charT* s, size_type pos, size_type n);
```

is equivalent to `return F(basic_string_view(s, n), pos);`

Each member function of the form

``` cpp
constexpr return-type F(charT c, size_type pos);
```

is equivalent to `return F(basic_string_view(&c, 1), pos);`

``` cpp
constexpr size_type find(basic_string_view str, size_type pos = 0) const noexcept;
```

Let `xpos` be the lowest position, if possible, such that the following
conditions hold:

- `pos <= xpos`
- `xpos + str.size() <= size()`
- `traits::eq(at(xpos + I), str.at(I))` for all elements `I` of the
  string referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
constexpr size_type rfind(basic_string_view str, size_type pos = npos) const noexcept;
```

Let `xpos` be the highest position, if possible, such that the following
conditions hold:

- `xpos <= pos`
- `xpos + str.size() <= size()`
- `traits::eq(at(xpos + I), str.at(I))` for all elements `I` of the
  string referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
constexpr size_type find_first_of(basic_string_view str, size_type pos = 0) const noexcept;
```

Let `xpos` be the lowest position, if possible, such that the following
conditions hold:

- `pos <= xpos`
- `xpos < size()`
- `traits::eq(at(xpos), str.at(I))` for some element `I` of the string
  referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
constexpr size_type find_last_of(basic_string_view str, size_type pos = npos) const noexcept;
```

Let `xpos` be the highest position, if possible, such that the following
conditions hold:

- `xpos <= pos`
- `xpos < size()`
- `traits::eq(at(xpos), str.at(I))` for some element `I` of the string
  referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
constexpr size_type find_first_not_of(basic_string_view str, size_type pos = 0) const noexcept;
```

Let `xpos` be the lowest position, if possible, such that the following
conditions hold:

- `pos <= xpos`
- `xpos < size()`
- `traits::eq(at(xpos), str.at(I))` for no element `I` of the string
  referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

``` cpp
constexpr size_type find_last_not_of(basic_string_view str, size_type pos = npos) const noexcept;
```

Let `xpos` be the highest position, if possible, such that the following
conditions hold:

- `xpos <= pos`
- `xpos < size()`
- `traits::eq(at(xpos), str.at(I))` for no element `I` of the string
  referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

### Non-member comparison functions <a id="string.view.comparison">[[string.view.comparison]]</a>

Let `S` be `basic_string_view<charT, traits>`, and `sv` be an instance
of `S`. Implementations shall provide sufficient additional overloads
marked `constexpr` and `noexcept` so that an object `t` with an implicit
conversion to `S` can be compared according to Table 
[[tab:string.view.comparison.overloads]].

**Table: Additional `basic_string_view` comparison overloads**

| Expression | Equivalent to |
| ---------- | ------------- |
| `t == sv`  | `S(t) == sv`  |
| `sv == t`  | `sv == S(t)`  |
| `t != sv`  | `S(t) != sv`  |
| `sv != t`  | `sv != S(t)`  |
| `t < sv`   | `S(t) < sv`   |
| `sv < t`   | `sv < S(t)`   |
| `t > sv`   | `S(t) > sv`   |
| `sv > t`   | `sv > S(t)`   |
| `t <= sv`  | `S(t) <= sv`  |
| `sv <= t`  | `sv <= S(t)`  |
| `t >= sv`  | `S(t) >= sv`  |
| `sv >= t`  | `sv >= S(t)`  |


[*Example 1*:

A sample conforming implementation for `operator==` would be:

``` cpp
template<class T> using __identity = decay_t<T>;
template<class charT, class traits>
  constexpr bool operator==(basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept {
    return lhs.compare(rhs) == 0;
  }
template<class charT, class traits>
  constexpr bool operator==(basic_string_view<charT, traits> lhs,
                            __identity<basic_string_view<charT, traits>> rhs) noexcept {
    return lhs.compare(rhs) == 0;
  }
template<class charT, class traits>
  constexpr bool operator==(__identity<basic_string_view<charT, traits>> lhs,
                            basic_string_view<charT, traits> rhs) noexcept {
    return lhs.compare(rhs) == 0;
  }
```

— *end example*\]

``` cpp
template<class charT, class traits>
  constexpr bool operator==(basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template<class charT, class traits>
  constexpr bool operator!=(basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) != 0`.

``` cpp
template<class charT, class traits>
  constexpr bool operator< (basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) < 0`.

``` cpp
template<class charT, class traits>
  constexpr bool operator> (basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) > 0`.

``` cpp
template<class charT, class traits>
  constexpr bool operator<=(basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) <= 0`.

``` cpp
template<class charT, class traits>
  constexpr bool operator>=(basic_string_view<charT, traits> lhs,
                            basic_string_view<charT, traits> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) >= 0`.

### Inserters and extractors <a id="string.view.io">[[string.view.io]]</a>

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os,
               basic_string_view<charT, traits> str);
```

*Effects:* Behaves as a formatted output
function ( [[ostream.formatted.reqmts]]) of `os`. Forms a character
sequence `seq`, initially consisting of the elements defined by the
range \[`str.begin()`, `str.end()`). Determines padding for `seq` as
described in  [[ostream.formatted.reqmts]]. Then inserts `seq` as if by
calling `os.rdbuf()->sputn(seq, n)`, where `n` is the larger of
`os.width()` and `str.size()`; then calls `os.width(0)`.

*Returns:* `os`

### Hash support <a id="string.view.hash">[[string.view.hash]]</a>

``` cpp
template<> struct hash<string_view>;
template<> struct hash<u16string_view>;
template<> struct hash<u32string_view>;
template<> struct hash<wstring_view>;
```

The specialization is enabled ( [[unord.hash]]).

[*Note 1*: The hash value of a string view object is equal to the hash
value of the corresponding string object
( [[basic.string.hash]]). — *end note*\]

### Suffix for `basic_string_view` literals <a id="string.view.literals">[[string.view.literals]]</a>

``` cpp
constexpr string_view operator""sv(const char* str, size_t len) noexcept;
```

*Returns:* `string_view{str, len}`.

``` cpp
constexpr u16string_view operator""sv(const char16_t* str, size_t len) noexcept;
```

*Returns:* `u16string_view{str, len}`.

``` cpp
constexpr u32string_view operator""sv(const char32_t* str, size_t len) noexcept;
```

*Returns:* `u32string_view{str, len}`.

``` cpp
constexpr wstring_view operator""sv(const wchar_t* str, size_t len) noexcept;
```

*Returns:* `wstring_view{str, len}`.

## Null-terminated sequence utilities <a id="c.strings">[[c.strings]]</a>

### Header `<cctype>` synopsis <a id="cctype.syn">[[cctype.syn]]</a>

``` cpp
namespace std {
  int isalnum(int c);
  int isalpha(int c);
  int isblank(int c);
  int iscntrl(int c);
  int isdigit(int c);
  int isgraph(int c);
  int islower(int c);
  int isprint(int c);
  int ispunct(int c);
  int isspace(int c);
  int isupper(int c);
  int isxdigit(int c);
  int tolower(int c);
  int toupper(int c);
}
```

The contents and meaning of the header `<cctype>` are the same as the C
standard library header `<ctype.h>`.

ISO C 7.4

### Header `<cwctype>` synopsis <a id="cwctype.syn">[[cwctype.syn]]</a>

``` cpp
namespace std {
  using wint_t = see below;
  using wctrans_t = see below;
  using wctype_t = see below;

  int iswalnum(wint_t wc);
  int iswalpha(wint_t wc);
  int iswblank(wint_t wc);
  int iswcntrl(wint_t wc);
  int iswdigit(wint_t wc);
  int iswgraph(wint_t wc);
  int iswlower(wint_t wc);
  int iswprint(wint_t wc);
  int iswpunct(wint_t wc);
  int iswspace(wint_t wc);
  int iswupper(wint_t wc);
  int iswxdigit(wint_t wc);
  int iswctype(wint_t wc, wctype_t desc);
  wctype_t wctype(const char* property);
  wint_t towlower(wint_t wc);
  wint_t towupper(wint_t wc);
  wint_t towctrans(wint_t wc, wctrans_t desc);
  wctrans_t wctrans(const char* property);
}

#define WEOF see below
```

The contents and meaning of the header `<cwctype>` are the same as the C
standard library header `<wctype.h>`.

ISO C 7.30

### Header `<cstring>` synopsis <a id="cstring.syn">[[cstring.syn]]</a>

``` cpp
namespace std {
  using size_t = see [support.types.layout];

  void* memcpy(void* s1, const void* s2, size_t n);
  void* memmove(void* s1, const void* s2, size_t n);
  char* strcpy(char* s1, const char* s2);
  char* strncpy(char* s1, const char* s2, size_t n);
  char* strcat(char* s1, const char* s2);
  char* strncat(char* s1, const char* s2, size_t n);
  int memcmp(const void* s1, const void* s2, size_t n);
  int strcmp(const char* s1, const char* s2);
  int strcoll(const char* s1, const char* s2);
  int strncmp(const char* s1, const char* s2, size_t n);
  size_t strxfrm(char* s1, const char* s2, size_t n);
  const void* memchr(const void* s, int c, size_t n);  // see [library.c]
  void* memchr(void* s, int c, size_t n)  // see [library.c]
  const char* strchr(const char* s, int c)  // see [library.c]
  char* strchr(char* s, int c)  // see [library.c]
  size_t strcspn(const char* s1, const char* s2);
  const char* strpbrk(const char* s1, const char* s2)  // see [library.c]
  char* strpbrk(char* s1, const char* s2)  // see [library.c]
  const char* strrchr(const char* s, int c)  // see [library.c]
  char* strrchr(char* s, int c)  // see [library.c]
  size_t strspn(const char* s1, const char* s2);
  const char* strstr(const char* s1, const char* s2)  // see [library.c]
  char* strstr(char* s1, const char* s2)  // see [library.c]
  char* strtok(char* s1, const char* s2);
  void* memset(void* s, int c, size_t n);
  char* strerror(int errnum);
  size_t strlen(const char* s);
}

#define NULL see [support.types.nullptr]
```

The contents and meaning of the header `<cstring>` are the same as the C
standard library header `<string.h>`.

The functions `strerror` and `strtok` are not required to avoid data
races ( [[res.on.data.races]]).

The functions `memcpy` and `memmove` are signal-safe ( [[csignal.syn]]).

[*Note 1*: The functions `strchr`, `strpbrk`, `strrchr`, `strstr`, and
`memchr`, have different signatures in this International Standard, but
they have the same behavior as in the C standard library (
[[library.c]]). — *end note*\]

ISO C 7.24.

### Header `<cwchar>` synopsis <a id="cwchar.syn">[[cwchar.syn]]</a>

``` cpp
namespace std {
  using size_t = see [support.types.layout];
  using mbstate_t = see below;
  using wint_t = see below;

  struct tm;

  int fwprintf(FILE* stream, const wchar_t* format, ...);
  int fwscanf(FILE* stream, const wchar_t* format, ...);
  int swprintf(wchar_t* s, size_t n, const wchar_t* format, ...);
  int swscanf(const wchar_t* s, const wchar_t* format, ...);
  int vfwprintf(FILE* stream, const wchar_t* format, va_list arg);
  int vfwscanf(FILE* stream, const wchar_t* format, va_list arg);
  int vswprintf(wchar_t* s, size_t n, const wchar_t* format, va_list arg);
  int vswscanf(const wchar_t* s, const wchar_t* format, va_list arg);
  int vwprintf(const wchar_t* format, va_list arg);
  int vwscanf(const wchar_t* format, va_list arg);
  int wprintf(const wchar_t* format, ...);
  int wscanf(const wchar_t* format, ...);
  wint_t fgetwc(FILE* stream);
  wchar_t* fgetws(wchar_t* s, int n, FILE* stream);
  wint_t fputwc(wchar_t c, FILE* stream);
  int fputws(const wchar_t* s, FILE* stream);
  int fwide(FILE* stream, int mode);
  wint_t getwc(FILE* stream);
  wint_t getwchar();
  wint_t putwc(wchar_t c, FILE* stream);
  wint_t putwchar(wchar_t c);
  wint_t ungetwc(wint_t c, FILE* stream);
  double wcstod(const wchar_t* nptr, wchar_t** endptr);
  float wcstof(const wchar_t* nptr, wchar_t** endptr);
  long double wcstold(const wchar_t* nptr, wchar_t** endptr);
  long int wcstol(const wchar_t* nptr, wchar_t** endptr, int base);
  long long int wcstoll(const wchar_t* nptr, wchar_t** endptr, int base);
  unsigned long int wcstoul(const wchar_t* nptr, wchar_t** endptr, int base);
  unsigned long long int wcstoull(const wchar_t* nptr, wchar_t** endptr, int base);
  wchar_t* wcscpy(wchar_t* s1, const wchar_t* s2);
  wchar_t* wcsncpy(wchar_t* s1, const wchar_t* s2, size_t n);
  wchar_t* wmemcpy(wchar_t* s1, const wchar_t* s2, size_t n);
  wchar_t* wmemmove(wchar_t* s1, const wchar_t* s2, size_t n);
  wchar_t* wcscat(wchar_t* s1, const wchar_t* s2);
  wchar_t* wcsncat(wchar_t* s1, const wchar_t* s2, size_t n);
  int wcscmp(const wchar_t* s1, const wchar_t* s2);
  int wcscoll(const wchar_t* s1, const wchar_t* s2);
  int wcsncmp(const wchar_t* s1, const wchar_t* s2, size_t n);
  size_t wcsxfrm(wchar_t* s1, const wchar_t* s2, size_t n);
  int wmemcmp(const wchar_t* s1, const wchar_t* s2, size_t n);
  const wchar_t* wcschr(const wchar_t* s, wchar_t c)  // see [library.c]
  wchar_t* wcschr(wchar_t* s, wchar_t c)  // see [library.c]
  size_t wcscspn(const wchar_t* s1, const wchar_t* s2);
  const wchar_t* wcspbrk(const wchar_t* s1, const wchar_t* s2)  // see [library.c]
  wchar_t* wcspbrk(wchar_t* s1, const wchar_t* s2)  // see [library.c]
  const wchar_t* wcsrchr(const wchar_t* s, wchar_t c)  // see [library.c]
  wchar_t* wcsrchr(wchar_t* s, wchar_t c)  // see [library.c]
  size_t wcsspn(const wchar_t* s1, const wchar_t* s2);
  const wchar_t* wcsstr(const wchar_t* s1, const wchar_t* s2)  // see [library.c]
  wchar_t* wcsstr(wchar_t* s1, const wchar_t* s2)  // see [library.c]
  wchar_t* wcstok(wchar_t* s1, const wchar_t* s2, wchar_t** ptr);
  const wchar_t* wmemchr(const wchar_t* s, wchar_t c, size_t n)  // see [library.c]
  wchar_t* wmemchr(wchar_t* s, wchar_t c, size_t n)  // see [library.c]
  size_t wcslen(const wchar_t* s);
  wchar_t* wmemset(wchar_t* s, wchar_t c, size_t n);
  size_t wcsftime(wchar_t* s, size_t maxsize, const wchar_t* format, const struct tm* timeptr);
  wint_t btowc(int c);
  int wctob(wint_t c);

  // [c.mb.wcs], multibyte / wide string and character conversion functions
  int mbsinit(const mbstate_t* ps);
  size_t mbrlen(const char* s, size_t n, mbstate_t* ps);
  size_t mbrtowc(wchar_t* pwc, const char* s, size_t n, mbstate_t* ps);
  size_t wcrtomb(char* s, wchar_t wc, mbstate_t* ps);
  size_t mbsrtowcs(wchar_t* dst, const char** src, size_t len, mbstate_t* ps);
  size_t wcsrtombs(char* dst, const wchar_t** src, size_t len, mbstate_t* ps);
}

#define NULL see [support.types.nullptr]
#define WCHAR_MAX see below
#define WCHAR_MIN see below
#define WEOF see below
```

The contents and meaning of the header `<cwchar>` are the same as the C
standard library header `<wchar.h>`, except that it does not declare a
type `wchar_t`.

[*Note 1*: The functions `wcschr`, `wcspbrk`, `wcsrchr`, `wcsstr`, and
`wmemchr` have different signatures in this International Standard, but
they have the same behavior as in the C standard library (
[[library.c]]). — *end note*\]

ISO C 7.29

### Header `<cuchar>` synopsis <a id="cuchar.syn">[[cuchar.syn]]</a>

``` cpp
namespace std {
  using mbstate_t = see below;
  using size_t = see [support.types.layout];

  size_t mbrtoc16(char16_t* pc16, const char* s, size_t n, mbstate_t* ps);
  size_t c16rtomb(char* s, char16_t c16, mbstate_t* ps);
  size_t mbrtoc32(char32_t* pc32, const char* s, size_t n, mbstate_t* ps);
  size_t c32rtomb(char* s, char32_t c32, mbstate_t* ps);
}
```

The contents and meaning of the header `<cuchar>` are the same as the C
standard library header `<uchar.h>`, except that it does not declare
types `char16_t` nor `char32_t`.

ISO C 7.28

### Multibyte / wide string and character conversion functions <a id="c.mb.wcs">[[c.mb.wcs]]</a>

[*Note 1*: The headers `<cstdlib>` ( [[cstdlib.syn]]) and `<cwchar>` (
[[cwchar.syn]]) declare the functions described in this
subclause. — *end note*\]

``` cpp
int mbsinit(const mbstate_t* ps);
int mblen(const char* s, size_t n);
size_t mbstowcs(wchar_t* pwcs, const char* s, size_t n);
size_t wcstombs(char* s, const wchar_t* pwcs, size_t n);
```

*Effects:* These functions have the semantics specified in the C
standard library.

ISO C 7.22.7.1, 7.22.8, 7.29.6.2.1

``` cpp
int mbtowc(wchar_t* pwc, const char* s, size_t n);
int wctomb(char* s, wchar_t wchar);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* Calls to these functions may introduce a data
race ( [[res.on.data.races]]) with other calls to the same function.

ISO C 7.22.7

``` cpp
size_t mbrlen(const char* s, size_t n, mbstate_t* ps);
size_t mbrtowc(wchar_t* pwc, const char* s, size_t n, mbstate_t* ps);
size_t wcrtomb(char* s, wchar_t wc, mbstate_t* ps);
size_t mbsrtowcs(wchar_t* dst, const char** src, size_t len, mbstate_t* ps);
size_t wcsrtombs(char* dst, const wchar_t** src, size_t len, mbstate_t* ps);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* Calling these functions with an `mbstate_t*` argument that is
a null pointer value may introduce a data race ( [[res.on.data.races]])
with other calls to the same function with an `mbstate_t*` argument that
is a null pointer value.

ISO C 7.29.6.3

<!-- Section link definitions -->
[basic.string]: #basic.string
[basic.string.hash]: #basic.string.hash
[basic.string.literals]: #basic.string.literals
[c.mb.wcs]: #c.mb.wcs
[c.strings]: #c.strings
[cctype.syn]: #cctype.syn
[char.traits]: #char.traits
[char.traits.require]: #char.traits.require
[char.traits.specializations]: #char.traits.specializations
[char.traits.specializations.char]: #char.traits.specializations.char
[char.traits.specializations.char16_t]: #char.traits.specializations.char16_t
[char.traits.specializations.char32_t]: #char.traits.specializations.char32_t
[char.traits.specializations.wchar.t]: #char.traits.specializations.wchar.t
[char.traits.typedefs]: #char.traits.typedefs
[cstring.syn]: #cstring.syn
[cuchar.syn]: #cuchar.syn
[cwchar.syn]: #cwchar.syn
[cwctype.syn]: #cwctype.syn
[string.access]: #string.access
[string.accessors]: #string.accessors
[string.append]: #string.append
[string.assign]: #string.assign
[string.capacity]: #string.capacity
[string.classes]: #string.classes
[string.compare]: #string.compare
[string.cons]: #string.cons
[string.conversions]: #string.conversions
[string.copy]: #string.copy
[string.erase]: #string.erase
[string.find]: #string.find
[string.find.first.not.of]: #string.find.first.not.of
[string.find.first.of]: #string.find.first.of
[string.find.last.not.of]: #string.find.last.not.of
[string.find.last.of]: #string.find.last.of
[string.insert]: #string.insert
[string.io]: #string.io
[string.iterators]: #string.iterators
[string.modifiers]: #string.modifiers
[string.nonmembers]: #string.nonmembers
[string.op!=]: #string.op!=
[string.op+]: #string.op+
[string.op+=]: #string.op+=
[string.op<]: #string.op<
[string.op<=]: #string.op<=
[string.op>]: #string.op>
[string.op>=]: #string.op>=
[string.operator==]: #string.operator==
[string.ops]: #string.ops
[string.replace]: #string.replace
[string.require]: #string.require
[string.rfind]: #string.rfind
[string.special]: #string.special
[string.substr]: #string.substr
[string.swap]: #string.swap
[string.syn]: #string.syn
[string.view]: #string.view
[string.view.access]: #string.view.access
[string.view.capacity]: #string.view.capacity
[string.view.comparison]: #string.view.comparison
[string.view.cons]: #string.view.cons
[string.view.find]: #string.view.find
[string.view.hash]: #string.view.hash
[string.view.io]: #string.view.io
[string.view.iterators]: #string.view.iterators
[string.view.literals]: #string.view.literals
[string.view.modifiers]: #string.view.modifiers
[string.view.ops]: #string.view.ops
[string.view.synop]: #string.view.synop
[string.view.template]: #string.view.template
[strings]: #strings
[strings.general]: #strings.general

<!-- Link reference definitions -->
[basic.string.hash]: #basic.string.hash
[basic.types]: basic.md#basic.types
[c.strings]: #c.strings
[char.traits]: #char.traits
[char.traits.require]: #char.traits.require
[char.traits.typedefs]: #char.traits.typedefs
[container.requirements]: containers.md#container.requirements
[container.requirements.general]: containers.md#container.requirements.general
[csignal.syn]: language.md#csignal.syn
[cstdlib.syn]: language.md#cstdlib.syn
[cwchar.syn]: #cwchar.syn
[input.output]: input.md#input.output
[iostate.flags]: input.md#iostate.flags
[iostream.forward]: input.md#iostream.forward
[iostreams.limits.pos]: input.md#iostreams.limits.pos
[istream.formatted.reqmts]: input.md#istream.formatted.reqmts
[istream.unformatted]: input.md#istream.unformatted
[iterator.range]: iterators.md#iterator.range
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[length.error]: diagnostics.md#length.error
[library.c]: library.md#library.c
[ostream.formatted.reqmts]: input.md#ostream.formatted.reqmts
[out.of.range]: diagnostics.md#out.of.range
[random.access.iterators]: iterators.md#random.access.iterators
[res.on.data.races]: library.md#res.on.data.races
[sequence.reqmts]: containers.md#sequence.reqmts
[string.classes]: #string.classes
[string.io]: #string.io
[string.require]: #string.require
[string.special]: #string.special
[string.view]: #string.view
[strings.general]: #strings.general
[tab:char.traits.require]: #tab:char.traits.require
[tab:copyassignable]: #tab:copyassignable
[tab:copyconstructible]: #tab:copyconstructible
[tab:defaultconstructible]: #tab:defaultconstructible
[tab:string.view.compare]: #tab:string.view.compare
[tab:string.view.comparison.overloads]: #tab:string.view.comparison.overloads
[tab:string.view.ctr.2]: #tab:string.view.ctr.2
[tab:string.view.ctr.3]: #tab:string.view.ctr.3
[tab:strings.compare]: #tab:strings.compare
[tab:strings.ctr.1]: #tab:strings.ctr.1
[tab:strings.ctr.2]: #tab:strings.ctr.2
[tab:strings.ctr.3]: #tab:strings.ctr.3
[tab:strings.ctr.4]: #tab:strings.ctr.4
[tab:strings.ctr.5]: #tab:strings.ctr.5
[tab:strings.ctr.6]: #tab:strings.ctr.6
[tab:strings.ctr.cpy]: #tab:strings.ctr.cpy
[tab:strings.lib.summary]: #tab:strings.lib.summary
[tab:strings.op=]: #tab:strings.op=
[unord.hash]: utilities.md#unord.hash
[utility.swap]: utilities.md#utility.swap

[^1]: If `eof()` can be held in `char_type` then some iostreams
    operations may give surprising results.

[^2]: `Allocator::value_type` must name the same type as `charT` (
    [[string.require]]).

[^3]: For example, as an argument to non-member functions `swap()` (
    [[string.special]]), `operator>{}>()` ( [[string.io]]), and
    `getline()` ( [[string.io]]), or as an argument to
    `basic_string::swap()`.

[^4]: `reserve()` uses `allocator_traits<Allocator>::allocate()` which
    may throw an appropriate exception.
