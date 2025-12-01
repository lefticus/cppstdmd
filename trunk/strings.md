# Strings library <a id="strings">[[strings]]</a>

## General <a id="strings.general">[[strings.general]]</a>

This Clause describes components for manipulating sequences of any
non-array trivially copyable standard-layout
[[term.standard.layout.type]] type `T` where
`is_trivially_default_constructible_v<T>` is `true`. Such types are
called *char-like types*, and objects of char-like types are called
*char-like objects* or simply *characters*.

The following subclauses describe a character traits class, string
classes, and null-terminated sequence utilities, as summarized in
[[strings.summary]].

## Character traits <a id="char.traits">[[char.traits]]</a>

### General <a id="char.traits.general">[[char.traits.general]]</a>

Subclause [[char.traits]] defines requirements on classes representing
*character traits*, and defines a class template `char_traits<charT>`,
along with five specializations, `char_traits<char>`,
`char_traits<char8_t>`, `char_traits<char16_t>`,
`char_traits<char32_t>`, and `char_traits<wchar_t>`, that meet those
requirements.

Most classes specified in [[string.classes]], [[string.view]], and
[[input.output]] need a set of related types and functions to complete
the definition of their semantics. These types and functions are
provided as a set of member *typedef-name*s and functions in the
template parameter `traits` used by each such template. Subclause
[[char.traits]] defines the semantics of these members.

To specialize those templates to generate a string, string view, or
iostream class to handle a particular character container type
[[defns.character.container]] `C`, that and its related character traits
class `X` are passed as a pair of parameters to the string, string view,
or iostream template as parameters `charT` and `traits`. If
`X::char_type` is not the same type as `C`, the program is ill-formed.

### Character traits requirements <a id="char.traits.require">[[char.traits.require]]</a>

In [[char.traits.req]], `X` denotes a traits class defining types and
functions for the character container type `C`; `c` and `d` denote
values of type `C`; `p` and `q` denote values of type `const C*`; `s`
denotes a value of type `C*`; `n`, `i` and `j` denote values of type
`size_t`; `e` and `f` denote values of type `X::int_type`; `pos` denotes
a value of type `X::pos_type`; and `r` denotes an lvalue of type `C`. No
expression which is part of the character traits requirements specified
in [[char.traits.require]] shall exit via an exception.

The class template

``` cpp
template<class charT> struct char_traits;
```

is provided in the header `<string>` as a basis for explicit
specializations.

### Traits typedefs <a id="char.traits.typedefs">[[char.traits.typedefs]]</a>

``` cpp
using int_type = see below;
```

*Preconditions:* `int_type` shall be able to represent all of the valid
characters converted from the corresponding `char_type` values, as well
as an end-of-file value, `eof()`.[^1]

``` cpp
using state_type = see below;
```

*Preconditions:* `state_type` meets the *Cpp17Destructible*
([[cpp17.destructible]]), *Cpp17CopyAssignable*
([[cpp17.copyassignable]]), *Cpp17CopyConstructible*
([[cpp17.copyconstructible]]), and *Cpp17DefaultConstructible*
([[cpp17.defaultconstructible]]) requirements.

### `char_traits` specializations <a id="char.traits.specializations">[[char.traits.specializations]]</a>

#### General <a id="char.traits.specializations.general">[[char.traits.specializations.general]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char>;
  template<> struct char_traits<char8_t>;
  template<> struct char_traits<char16_t>;
  template<> struct char_traits<char32_t>;
  template<> struct char_traits<wchar_t>;
}
```

The header `<string>` defines five specializations of the class template
`char_traits`: `char_traits<{}char>`, `char_traits<char8_t>`,
`char_traits<char16_t>`, `char_traits<char32_t>`, and
`char_traits<wchar_t>`.

#### `struct char_traits<char>` <a id="char.traits.specializations.char">[[char.traits.specializations.char]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char> {
    using char_type  = char;
    using int_type   = int;
    using off_type   = streamoff;
    using pos_type   = streampos;
    using state_type = mbstate_t;
    using comparison_category = strong_ordering;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
                                           const char_type& a);
    static constexpr char_type* move(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The type `mbstate_t` is defined in `<cwchar>` and can represent any of
the conversion states that can occur in an *implementation-defined* set
of supported multibyte character encoding rules.

The two-argument member `assign` is defined identically to the built-in
operator `=`. The two-argument members `eq` and `lt` are defined
identically to the built-in operators `==` and `<` for type
`unsigned char`.

The member `eof()` returns `EOF`.

#### `struct char_traits<char8_t>` <a id="char.traits.specializations.char8.t">[[char.traits.specializations.char8.t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char8_t> {
    using char_type  = char8_t;
    using int_type   = unsigned int;
    using off_type   = streamoff;
    using pos_type   = u8streampos;
    using state_type = mbstate_t;
    using comparison_category = strong_ordering;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
                                           const char_type& a);
    static constexpr char_type* move(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* assign(char_type* s, size_t n, char_type a);
    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The two-argument members `assign`, `eq`, and `lt` are defined
identically to the built-in operators `=`, `==`, and `<` respectively.

The member `eof()` returns an *implementation-defined* constant that
cannot appear as a valid UTF-8 code unit.

#### `struct char_traits<char16_t>` <a id="char.traits.specializations.char16.t">[[char.traits.specializations.char16.t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char16_t> {
    using char_type  = char16_t;
    using int_type   = uint_least16_t;
    using off_type   = streamoff;
    using pos_type   = u16streampos;
    using state_type = mbstate_t;
    using comparison_category = strong_ordering;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
                                           const char_type& a);
    static constexpr char_type* move(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The two-argument members `assign`, `eq`, and `lt` are defined
identically to the built-in operators `=`, `==`, and `<`, respectively.

The member `eof()` returns an *implementation-defined* constant that
cannot appear as a valid UTF-16 code unit.

#### `struct char_traits<char32_t>` <a id="char.traits.specializations.char32.t">[[char.traits.specializations.char32.t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<char32_t> {
    using char_type  = char32_t;
    using int_type   = uint_least32_t;
    using off_type   = streamoff;
    using pos_type   = u32streampos;
    using state_type = mbstate_t;
    using comparison_category = strong_ordering;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
                                           const char_type& a);
    static constexpr char_type* move(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The two-argument members `assign`, `eq`, and `lt` are defined
identically to the built-in operators `=`, `==`, and `<`, respectively.

The member `eof()` returns an *implementation-defined* constant that
cannot appear as a Unicode code point.

#### `struct char_traits<wchar_t>` <a id="char.traits.specializations.wchar.t">[[char.traits.specializations.wchar.t]]</a>

``` cpp
namespace std {
  template<> struct char_traits<wchar_t> {
    using char_type  = wchar_t;
    using int_type   = wint_t;
    using off_type   = streamoff;
    using pos_type   = wstreampos;
    using state_type = mbstate_t;
    using comparison_category = strong_ordering;

    static constexpr void assign(char_type& c1, const char_type& c2) noexcept;
    static constexpr bool eq(char_type c1, char_type c2) noexcept;
    static constexpr bool lt(char_type c1, char_type c2) noexcept;

    static constexpr int compare(const char_type* s1, const char_type* s2, size_t n);
    static constexpr size_t length(const char_type* s);
    static constexpr const char_type* find(const char_type* s, size_t n,
                                           const char_type& a);
    static constexpr char_type* move(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* copy(char_type* s1, const char_type* s2, size_t n);
    static constexpr char_type* assign(char_type* s, size_t n, char_type a);

    static constexpr int_type not_eof(int_type c) noexcept;
    static constexpr char_type to_char_type(int_type c) noexcept;
    static constexpr int_type to_int_type(char_type c) noexcept;
    static constexpr bool eq_int_type(int_type c1, int_type c2) noexcept;
    static constexpr int_type eof() noexcept;
  };
}
```

The two-argument members `assign`, `eq`, and `lt` are defined
identically to the built-in operators `=`, `==`, and `<`, respectively.

The member `eof()` returns `WEOF`.

## String view classes <a id="string.view">[[string.view]]</a>

### General <a id="string.view.general">[[string.view.general]]</a>

The class template `basic_string_view` describes an object that can
refer to a constant contiguous sequence of char-like [[strings.general]]
objects with the first element of the sequence at position zero. In the
rest of [[string.view]], the type of the char-like objects held in a
`basic_string_view` object is designated by `charT`.

[*Note 1*: The library provides implicit conversions from
`const charT*` and `std::basic_string<charT, ...>` to
`std::basic_string_view<charT, ...>` so that user code can accept just
`std::basic_string_view<charT>` as a non-templated parameter wherever a
sequence of characters is expected. User-defined types can define their
own implicit conversions to `std::basic_string_view<charT>` in order to
interoperate with these functions. — *end note*]

### Header `<string_view>` synopsis <a id="string.view.synop">[[string.view.synop]]</a>

``` cpp
// mostly freestanding
#include <compare>              // see [compare.syn]

namespace std {
  // [string.view.template], class template basic_string_view
  template<class charT, class traits = char_traits<charT>>
  class basic_string_view;                                              // partially freestanding

  template<class charT, class traits>
    constexpr bool ranges::\libspec{enable_view}{basic_string_view}<basic_string_view<charT, traits>> = true;
  template<class charT, class traits>
    constexpr bool ranges::\libspec{enable_borrowed_range}{basic_string_view}<basic_string_view<charT, traits>> = true;

  // [string.view.comparison], non-member comparison functions
  template<class charT, class traits>
    constexpr bool operator==(basic_string_view<charT, traits> x,
                              type_identity_t<basic_string_view<charT, traits>> y) noexcept;
  template<class charT, class traits>
    constexpr see below operator<=>(basic_string_view<charT, traits> x,
              \itcorr                      type_identity_t<basic_string_view<charT,
              \itcorr                                      traits>> y) noexcept;

  // [string.view.io], inserters and extractors
  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os,
                 basic_string_view<charT, traits> str);                 // hosted

  // basic_string_view typedef-names
  using string_view    = basic_string_view<char>;
  using u8string_view  = basic_string_view<char8_t>;
  using u16string_view = basic_string_view<char16_t>;
  using u32string_view = basic_string_view<char32_t>;
  using wstring_view   = basic_string_view<wchar_t>;

  // [string.view.hash], hash support
  template<class T> struct hash;
  template<> struct hash<string_view>;
  template<> struct hash<u8string_view>;
  template<> struct hash<u16string_view>;
  template<> struct hash<u32string_view>;
  template<> struct hash<wstring_view>;

  inline namespace literals {
    inline namespace string_view_literals {
      // [string.view.literals], suffix for basic_string_view literals
      constexpr string_view    operator""sv(const char* str, size_t len) noexcept;
      constexpr u8string_view  operator""sv(const char8_t* str, size_t len) noexcept;
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

#### General <a id="string.view.template.general">[[string.view.template.general]]</a>

``` cpp
namespace std {
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
    using iterator               = const_iterator;
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
    basic_string_view(nullptr_t) = delete;
    constexpr basic_string_view(const charT* str, size_type len);
    template<class It, class End>
      constexpr basic_string_view(It begin, End end);
    template<class R>
      constexpr explicit basic_string_view(R&& r);

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
    constexpr const_reference at(size_type pos) const;                  // freestanding-deleted
    constexpr const_reference front() const;
    constexpr const_reference back() const;
    constexpr const_pointer data() const noexcept;

    // [string.view.modifiers], modifiers
    constexpr void remove_prefix(size_type n);
    constexpr void remove_suffix(size_type n);
    constexpr void swap(basic_string_view& s) noexcept;

    // [string.view.ops], string operations
    constexpr size_type copy(charT* s, size_type n,
                             size_type pos = 0) const;                  // freestanding-deleted

    constexpr basic_string_view substr(size_type pos = 0,
                                       size_type n = npos) const;       // freestanding-deleted
    constexpr basic_string_view subview(size_type pos = 0,
                                        size_type n = npos) const;      // freestanding-deleted

    constexpr int compare(basic_string_view s) const noexcept;
    constexpr int compare(size_type pos1, size_type n1,
                          basic_string_view s) const;                   // freestanding-deleted
    constexpr int compare(size_type pos1, size_type n1, basic_string_view s,
                          size_type pos2, size_type n2) const;          // freestanding-deleted
    constexpr int compare(const charT* s) const;
    constexpr int compare(size_type pos1, size_type n1,
                          const charT* s) const;                        // freestanding-deleted
    constexpr int compare(size_type pos1, size_type n1, const charT* s,
                          size_type n2) const;                          // freestanding-deleted

    constexpr bool starts_with(basic_string_view x) const noexcept;
    constexpr bool starts_with(charT x) const noexcept;
    constexpr bool starts_with(const charT* x) const;
    constexpr bool ends_with(basic_string_view x) const noexcept;
    constexpr bool ends_with(charT x) const noexcept;
    constexpr bool ends_with(const charT* x) const;

    constexpr bool contains(basic_string_view x) const noexcept;
    constexpr bool contains(charT x) const noexcept;
    constexpr bool contains(const charT* x) const;

    // [string.view.find], searching
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
    const_pointer data_;        // exposition only
    size_type size_;            // exposition only
  };

  // [string.view.deduct], deduction guides
  template<class It, class End>
    basic_string_view(It, End) -> basic_string_view<iter_value_t<It>>;
  template<class R>
    basic_string_view(R&&) -> basic_string_view<ranges::range_value_t<R>>;
}
```

[^2]

In every specialization `basic_string_view<charT, traits>`, the type
`traits` shall meet the character traits requirements [[char.traits]].

[*Note 1*: The program is ill-formed if `traits::char_type` is not the
same type as `charT`. — *end note*]

For a `basic_string_view str`, any operation that invalidates a pointer
in the range

``` cpp
{[}str.data(), str.data() + str.size(){)}
```

invalidates pointers, iterators, and references to elements of `str`.

The complexity of `basic_string_view` member functions is 𝑂(1) unless
otherwise specified.

`basic_string_view<charT, traits>` is a trivially copyable type
[[term.trivially.copyable.type]].

#### Construction and assignment <a id="string.view.cons">[[string.view.cons]]</a>

``` cpp
constexpr basic_string_view() noexcept;
```

*Ensures:* *`size_`*` == 0` and *`data_`*` == nullptr`.

``` cpp
constexpr basic_string_view(const charT* str);
```

*Preconditions:* \[`str`, `str + traits::length(str)`) is a valid range.

*Effects:* Constructs a `basic_string_view`, initializing *data\_* with
`str` and initializing *size\_* with `traits::length(str)`.

*Complexity:* 𝑂(`traits::length(str)`).

``` cpp
constexpr basic_string_view(const charT* str, size_type len);
```

*Preconditions:* \[`str`, `str + len`) is a valid range.

*Effects:* Constructs a `basic_string_view`, initializing *data\_* with
`str` and initializing *size\_* with `len`.

``` cpp
template<class It, class End>
  constexpr basic_string_view(It begin, End end);
```

*Constraints:*

- `It` satisfies `contiguous_iterator`.
- `End` satisfies `sized_sentinel_for<It>`.
- `is_same_v<iter_value_t<It>, charT>` is `true`.
- `is_convertible_v<End, size_type>` is `false`.

*Preconditions:*

- \[`begin`, `end`) is a valid range.
- `It` models `contiguous_iterator`.
- `End` models `sized_sentinel_for<It>`.

*Effects:* Initializes *data\_* with `to_address(begin)` and initializes
*size\_* with `end - begin`.

*Throws:* When and what `end - begin` throws.

``` cpp
template<class R>
  constexpr explicit basic_string_view(R&& r);
```

Let `d` be an lvalue of type `remove_cvref_t<R>`.

*Constraints:*

- `remove_cvref_t<R>` is not the same type as `basic_string_view`,
- `R` models `ranges::contiguous_range` and `ranges::sized_range`,
- `is_same_v<ranges::range_value_t<R>, charT>` is `true`,
- `is_convertible_v<R, const charT*>` is `false`, and
- `d.operator ::std::basic_string_view<charT, traits>()` is not a valid
  expression.

*Effects:* Initializes *data\_* with `ranges::data(r)` and *size\_* with
`ranges::size(r)`.

*Throws:* Any exception thrown by `ranges::data(r)` and
`ranges::size(r)`.

#### Deduction guides <a id="string.view.deduct">[[string.view.deduct]]</a>

``` cpp
template<class It, class End>
  basic_string_view(It, End) -> basic_string_view<iter_value_t<It>>;
```

*Constraints:*

- `It` satisfies `contiguous_iterator`.
- `End` satisfies `sized_sentinel_for<It>`.

``` cpp
template<class R>
  basic_string_view(R&&) -> basic_string_view<ranges::range_value_t<R>>;
```

*Constraints:* `R` satisfies `ranges::contiguous_range`.

#### Iterator support <a id="string.view.iterators">[[string.view.iterators]]</a>

``` cpp
using const_iterator = implementation-defined  // type of basic_string_view::const_iterator;
```

A type that meets the requirements of a constant
*Cpp17RandomAccessIterator*[[random.access.iterators]], models
`contiguous_iterator`[[iterator.concept.contiguous]], and meets the
constexpr iterator requirements [[iterator.requirements.general]], whose
`value_type` is the template parameter `charT`.

All requirements on container iterators [[container.requirements]] apply
to `basic_string_view::const_iterator` as well.

``` cpp
constexpr const_iterator begin() const noexcept;
constexpr const_iterator cbegin() const noexcept;
```

*Returns:* An iterator such that

- if `!empty()`, `addressof(*begin()) == `*`data_`*,
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
constexpr size_type length() const noexcept;
```

*Returns:* *size\_*.

``` cpp
constexpr size_type max_size() const noexcept;
```

*Returns:* The largest possible number of char-like objects that can be
referred to by a `basic_string_view`.

``` cpp
constexpr bool empty() const noexcept;
```

*Returns:* *`size_`*` == 0`.

#### Element access <a id="string.view.access">[[string.view.access]]</a>

``` cpp
constexpr const_reference operator[](size_type pos) const;
```

`pos < size()` is `true`.

[*Note 1*: This precondition is stronger than the one on
`basic_string::operator[]`. — *end note*]

*Returns:* *`data_`*`[pos]`.

*Throws:* Nothing.

``` cpp
constexpr const_reference at(size_type pos) const;
```

*Returns:* *`data_`*`[pos]`.

*Throws:* `out_of_range` if `pos >= size()`.

``` cpp
constexpr const_reference front() const;
```

`empty()` is `false`.

*Returns:* *`data_`*`[0]`.

*Throws:* Nothing.

``` cpp
constexpr const_reference back() const;
```

`empty()` is `false`.

*Returns:* *`data_`*`[size() - 1]`.

*Throws:* Nothing.

``` cpp
constexpr const_pointer data() const noexcept;
```

*Returns:* *data\_*.

[*Note 2*: Unlike `basic_string::data()` and *string-literal*s,
`data()` can return a pointer to a buffer that is not null-terminated.
Therefore it is typically a mistake to pass `data()` to a function that
takes just a `const charT*` and expects a null-terminated
string. — *end note*]

#### Modifiers <a id="string.view.modifiers">[[string.view.modifiers]]</a>

``` cpp
constexpr void remove_prefix(size_type n);
```

`n <= size()` is `true`.

*Effects:* Equivalent to: *`data_`*` += n; `*`size_`*` -= n;`

``` cpp
constexpr void remove_suffix(size_type n);
```

`n <= size()` is `true`.

*Effects:* Equivalent to: *`size_`*` -= n;`

``` cpp
constexpr void swap(basic_string_view& s) noexcept;
```

*Effects:* Exchanges the values of `*this` and `s`.

#### String operations <a id="string.view.ops">[[string.view.ops]]</a>

``` cpp
constexpr size_type copy(charT* s, size_type n, size_type pos = 0) const;
```

Let `rlen` be the smaller of `n` and `size() - pos`.

*Preconditions:* \[`s`, `s + rlen`) is a valid range.

*Effects:* Equivalent to `traits::copy(s, data() + pos, rlen)`.

*Returns:* `rlen`.

*Throws:* `out_of_range` if `pos > size()`.

*Complexity:* 𝑂(`rlen`).

``` cpp
constexpr basic_string_view substr(size_type pos = 0, size_type n = npos) const;
constexpr basic_string_view subview(size_type pos = 0, size_type n = npos) const;
```

Let `rlen` be the smaller of `n` and `size() - pos`.

*Effects:* Determines `rlen`, the effective length of the string to
reference.

*Returns:* `basic_string_view(data() + pos, rlen)`.

*Throws:* `out_of_range` if `pos > size()`.

``` cpp
constexpr int compare(basic_string_view str) const noexcept;
```

Let `rlen` be the smaller of `size()` and `str.size()`.

*Effects:* Determines `rlen`, the effective length of the strings to
compare. The function then compares the two strings by calling
`traits::compare(data(), str.data(), rlen)`.

*Returns:* The nonzero result if the result of the comparison is
nonzero. Otherwise, returns a value as indicated in
[[string.view.compare]].

**Table: `compare()` results** <a id="string.view.compare">[string.view.compare]</a>

| Condition              | Return Value |
| ---------------------- | ------------ |
| `size() < str.size()`  | `< 0`        |
| `size() == str.size()` | ` \ 0`       |
| `size() > str.size()`  | `> 0`        |


*Complexity:* 𝑂(`rlen`).

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
constexpr int compare(size_type pos1, size_type n1, const charT* s, size_type n2) const;
```

*Effects:* Equivalent to:
`return substr(pos1, n1).compare(basic_string_view(s, n2));`

``` cpp
constexpr bool starts_with(basic_string_view x) const noexcept;
```

Let `rlen` be the smaller of `size()` and `x.size()`.

*Effects:* Equivalent to: `return basic_string_view(data(), rlen) == x;`

``` cpp
constexpr bool starts_with(charT x) const noexcept;
```

*Effects:* Equivalent to: `return !empty() && traits::eq(front(), x);`

``` cpp
constexpr bool starts_with(const charT* x) const;
```

*Effects:* Equivalent to: `return starts_with(basic_string_view(x));`

``` cpp
constexpr bool ends_with(basic_string_view x) const noexcept;
```

Let `rlen` be the smaller of `size()` and `x.size()`.

*Effects:* Equivalent to:

``` cpp
return basic_string_view(data() + (size() - rlen), rlen) == x;
```

``` cpp
constexpr bool ends_with(charT x) const noexcept;
```

*Effects:* Equivalent to: `return !empty() && traits::eq(back(), x);`

``` cpp
constexpr bool ends_with(const charT* x) const;
```

*Effects:* Equivalent to: `return ends_with(basic_string_view(x));`

``` cpp
constexpr bool contains(basic_string_view x) const noexcept;
constexpr bool contains(charT x) const noexcept;
constexpr bool contains(const charT* x) const;
```

*Effects:* Equivalent to: `return find(x) != npos;`

#### Searching <a id="string.view.find">[[string.view.find]]</a>

Member functions in this subclause have complexity
𝑂(`size() * str.size()`) at worst, although implementations should do
better.

Let *F* be one of `find`, `rfind`, `find_first_of`, `find_last_of`,
`find_first_not_of`, and `find_last_not_of`.

- Each member function of the form
  ``` cpp
  constexpr return-type F(const charT* s, size_type pos) const;
  ```

  has effects equivalent to: `return F(basic_string_view(s), pos);`
- Each member function of the form
  ``` cpp
  constexpr return-type F(const charT* s, size_type pos, size_type n) const;
  ```

  has effects equivalent to: `return F(basic_string_view(s, n), pos);`
- Each member function of the form
  ``` cpp
  constexpr return-type F(charT c, size_type pos) const noexcept;
  ```

  has effects equivalent to:
  `return F(basic_string_view(addressof(c), 1), pos);`

``` cpp
constexpr size_type find(basic_string_view str, size_type pos = 0) const noexcept;
```

Let `xpos` be the lowest position, if possible, such that the following
conditions hold:

- `pos <= xpos`
- `xpos + str.size() <= size()`
- `traits::eq(`*`data_`*`[xpos + I], str[I])` for all elements `I` of
  the string referenced by `str`.

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
- `traits::eq(`*`data_`*`[xpos + I], str[I])` for all elements `I` of
  the string referenced by `str`.

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
- `traits::eq(`*`data_`*`[xpos], str[I])` for some element `I` of the
  string referenced by `str`.

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
- `traits::eq(`*`data_`*`[xpos], str[I])` for some element `I` of the
  string referenced by `str`.

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
- `traits::eq(`*`data_`*`[xpos], str[I])` for no element `I` of the
  string referenced by `str`.

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
- `traits::eq(`*`data_`*`[xpos], str[I])` for no element `I` of the
  string referenced by `str`.

*Effects:* Determines `xpos`.

*Returns:* `xpos` if the function can determine such a value for `xpos`.
Otherwise, returns `npos`.

### Non-member comparison functions <a id="string.view.comparison">[[string.view.comparison]]</a>

``` cpp
template<class charT, class traits>
  constexpr bool operator==(basic_string_view<charT, traits> lhs,
                            type_identity_t<basic_string_view<charT, traits>> rhs) noexcept;
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template<class charT, class traits>
  constexpr see below operator<=>(basic_string_view<charT, traits> lhs,
            \itcorr                      type_identity_t<basic_string_view<charT, traits>> rhs) noexcept;
```

Let `R` denote the type `traits::comparison_category` if that
*qualified-id* is valid and denotes a type [[temp.deduct]], otherwise
`R` is `weak_ordering`.

*Mandates:* `R` denotes a comparison category type [[cmp.categories]].

*Returns:* `static_cast<R>(lhs.compare(rhs) <=> 0)`.

[*Note 1*: The usage of `type_identity_t` as parameter ensures that an
object of type `basic_string_view<charT, traits>` can always be compared
with an object of a type `T` with an implicit conversion to
`basic_string_view<charT, traits>`, and vice versa, as per
[[over.match.oper]]. — *end note*]

### Inserters and extractors <a id="string.view.io">[[string.view.io]]</a>

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, basic_string_view<charT, traits> str);
```

*Effects:* Behaves as a formatted output
function [[ostream.formatted.reqmts]] of `os`. Forms a character
sequence `seq`, initially consisting of the elements defined by the
range \[`str.begin()`, `str.end()`). Determines padding for `seq` as
described in  [[ostream.formatted.reqmts]]. Then inserts `seq` as if by
calling `os.rdbuf()->sputn(seq, n)`, where `n` is the larger of
`os.width()` and `str.size()`; then calls `os.width(0)`.

*Returns:* `os`.

### Hash support <a id="string.view.hash">[[string.view.hash]]</a>

``` cpp
template<> struct hash<string_view>;
template<> struct hash<u8string_view>;
template<> struct hash<u16string_view>;
template<> struct hash<u32string_view>;
template<> struct hash<wstring_view>;
```

The specialization is enabled [[unord.hash]].

[*Note 1*: The hash value of a string view object is equal to the hash
value of the corresponding string
object [[basic.string.hash]]. — *end note*]

### Suffix for `basic_string_view` literals <a id="string.view.literals">[[string.view.literals]]</a>

``` cpp
constexpr string_view operator""sv(const char* str, size_t len) noexcept;
```

*Returns:* `string_view{str, len}`.

``` cpp
constexpr u8string_view operator""sv(const char8_t* str, size_t len) noexcept;
```

*Returns:* `u8string_view{str, len}`.

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

## String classes <a id="string.classes">[[string.classes]]</a>

### General <a id="string.classes.general">[[string.classes.general]]</a>

The header `<string>` defines the `basic_string` class template for
manipulating varying-length sequences of char-like objects and five
*typedef-name*s, `string`, `u8string`, `u16string`, `u32string`, and
`wstring`, that name the specializations `basic_string<char>`,
`basic_string<char8_t>`, `basic_string<char16_t>`,
`basic_string<char32_t>`, and `basic_string<{}wchar_t>`, respectively.

### Header `<string>` synopsis <a id="string.syn">[[string.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [char.traits], character traits
  template<class charT> struct char_traits;                             // freestanding
  template<> struct char_traits<char>;                                  // freestanding
  template<> struct char_traits<char8_t>;                               // freestanding
  template<> struct char_traits<char16_t>;                              // freestanding
  template<> struct char_traits<char32_t>;                              // freestanding
  template<> struct char_traits<wchar_t>;                               // freestanding

  // [basic.string], basic_string
  template<class charT, class traits = char_traits<charT>, class Allocator = allocator<charT>>
    class basic_string;

  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const charT* lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const charT* lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(charT lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(charT lhs,
                basic_string<charT, traits, Allocator>&& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                const charT* rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                const charT* rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                charT rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                charT rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(const basic_string<charT, traits, Allocator>& lhs,
                type_identity_t<basic_string_view<charT, traits>> rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(basic_string<charT, traits, Allocator>&& lhs,
                type_identity_t<basic_string_view<charT, traits>> rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(type_identity_t<basic_string_view<charT, traits>> lhs,
                const basic_string<charT, traits, Allocator>& rhs);
  template<class charT, class traits, class Allocator>
    constexpr basic_string<charT, traits, Allocator>
      operator+(type_identity_t<basic_string_view<charT, traits>> lhs,
                basic_string<charT, traits, Allocator>&& rhs);

  template<class charT, class traits, class Allocator>
    constexpr bool
      operator==(const basic_string<charT, traits, Allocator>& lhs,
                 const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    constexpr bool operator==(const basic_string<charT, traits, Allocator>& lhs,
                              const charT* rhs);

  template<class charT, class traits, class Allocator>
    constexpr see below operator<=>(const basic_string<charT, traits, Allocator>& lhs,
              \itcorr                      const basic_string<charT, traits, Allocator>& rhs) noexcept;
  template<class charT, class traits, class Allocator>
    constexpr see below operator<=>(const basic_string<charT, traits, Allocator>& lhs,
              \itcorr                      const charT* rhs);

  // [string.special], swap
  template<class charT, class traits, class Allocator>
    constexpr void
      swap(basic_string<charT, traits, Allocator>& lhs,
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

  // [string.erasure], erasure
  template<class charT, class traits, class Allocator, class U = charT>
    constexpr typename basic_string<charT, traits, Allocator>::size_type
      erase(basic_string<charT, traits, Allocator>& c, const U& value);
  template<class charT, class traits, class Allocator, class Predicate>
    constexpr typename basic_string<charT, traits, Allocator>::size_type
      erase_if(basic_string<charT, traits, Allocator>& c, Predicate pred);

  // basic_string typedef-names
  using string    = basic_string<char>;
  using u8string  = basic_string<char8_t>;
  using u16string = basic_string<char16_t>;
  using u32string = basic_string<char32_t>;
  using wstring   = basic_string<wchar_t>;

  // [string.conversions], numeric conversions
  int stoi(const string& str, size_t* idx = nullptr, int base = 10);
  long stol(const string& str, size_t* idx = nullptr, int base = 10);
  unsigned long stoul(const string& str, size_t* idx = nullptr, int base = 10);
  long long stoll(const string& str, size_t* idx = nullptr, int base = 10);
  unsigned long long stoull(const string& str, size_t* idx = nullptr, int base = 10);
  float stof(const string& str, size_t* idx = nullptr);
  double stod(const string& str, size_t* idx = nullptr);
  long double stold(const string& str, size_t* idx = nullptr);
  string to_string(int val);
  string to_string(unsigned val);
  string to_string(long val);
  string to_string(unsigned long val);
  string to_string(long long val);
  string to_string(unsigned long long val);
  string to_string(float val);
  string to_string(double val);
  string to_string(long double val);

  int stoi(const wstring& str, size_t* idx = nullptr, int base = 10);
  long stol(const wstring& str, size_t* idx = nullptr, int base = 10);
  unsigned long stoul(const wstring& str, size_t* idx = nullptr, int base = 10);
  long long stoll(const wstring& str, size_t* idx = nullptr, int base = 10);
  unsigned long long stoull(const wstring& str, size_t* idx = nullptr, int base = 10);
  float stof(const wstring& str, size_t* idx = nullptr);
  double stod(const wstring& str, size_t* idx = nullptr);
  long double stold(const wstring& str, size_t* idx = nullptr);
  wstring to_wstring(int val);
  wstring to_wstring(unsigned val);
  wstring to_wstring(long val);
  wstring to_wstring(unsigned long val);
  wstring to_wstring(long long val);
  wstring to_wstring(unsigned long long val);
  wstring to_wstring(float val);
  wstring to_wstring(double val);
  wstring to_wstring(long double val);

  namespace pmr {
    template<class charT, class traits = char_traits<charT>>
      using basic_string = std::basic_string<charT, traits, polymorphic_allocator<charT>>;

    using string    = basic_string<char>;
    using u8string  = basic_string<char8_t>;
    using u16string = basic_string<char16_t>;
    using u32string = basic_string<char32_t>;
    using wstring   = basic_string<wchar_t>;
  }

  // [basic.string.hash], hash support
  template<class T> struct hash;
  template<class A> struct hash<basic_string<char, char_traits<char>, A>>;
  template<class A> struct hash<basic_string<char8_t, char_traits<char8_t>, A>>;
  template<class A> struct hash<basic_string<char16_t, char_traits<char16_t>, A>>;
  template<class A> struct hash<basic_string<char32_t, char_traits<char32_t>, A>>;
  template<class A> struct hash<basic_string<wchar_t, char_traits<wchar_t>, A>>;

  inline namespace literals {
    inline namespace string_literals {
      // [basic.string.literals], suffix for basic_string literals
      constexpr string    operator""s(const char* str, size_t len);
      constexpr u8string  operator""s(const char8_t* str, size_t len);
      constexpr u16string operator""s(const char16_t* str, size_t len);
      constexpr u32string operator""s(const char32_t* str, size_t len);
      constexpr wstring   operator""s(const wchar_t* str, size_t len);
    }
  }
}
```

### Class template `basic_string` <a id="basic.string">[[basic.string]]</a>

#### General <a id="basic.string.general">[[basic.string.general]]</a>

The class template `basic_string` describes objects that can store a
sequence consisting of a varying number of arbitrary char-like objects
with the first element of the sequence at position zero. Such a sequence
is also called a “string” if the type of the char-like objects that it
holds is clear from context. In the rest of [[basic.string]], the type
of the char-like objects held in a `basic_string` object is designated
by `charT`.

A specialization of `basic_string` is a contiguous container
[[container.reqmts]].

In all cases, \[`data()`, `data() + size()`\] is a valid range,
`data() + size()` points at an object with value `charT()` (a “null
terminator”), and `size() <= capacity()` is `true`.

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>,
           class Allocator = allocator<charT>>
  class basic_string {
  public:
    // types
    using traits_type            = traits;
    using value_type             = charT;
    using allocator_type         = Allocator;
    using size_type              = allocator_traits<Allocator>::size_type;
    using difference_type        = allocator_traits<Allocator>::difference_type;
    using pointer                = allocator_traits<Allocator>::pointer;
    using const_pointer          = allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;

    using iterator               = implementation-defined  // type of basic_string::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of basic_string::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    static constexpr size_type npos = size_type(-1);

    // [string.cons], construct/copy/destroy
    constexpr basic_string() noexcept(noexcept(Allocator())) : basic_string(Allocator()) { }
    constexpr explicit basic_string(const Allocator& a) noexcept;
    constexpr basic_string(const basic_string& str);
    constexpr basic_string(basic_string&& str) noexcept;
    constexpr basic_string(const basic_string& str, size_type pos,
                           const Allocator& a = Allocator());
    constexpr basic_string(const basic_string& str, size_type pos, size_type n,
                           const Allocator& a = Allocator());
    constexpr basic_string(basic_string&& str, size_type pos,
                           const Allocator& a = Allocator());
    constexpr basic_string(basic_string&& str, size_type pos, size_type n,
                           const Allocator& a = Allocator());
    template<class T>
      constexpr basic_string(const T& t, size_type pos, size_type n,
                             const Allocator& a = Allocator());
    template<class T>
      constexpr explicit basic_string(const T& t, const Allocator& a = Allocator());
    constexpr basic_string(const charT* s, size_type n, const Allocator& a = Allocator());
    constexpr basic_string(const charT* s, const Allocator& a = Allocator());
    basic_string(nullptr_t) = delete;
    constexpr basic_string(size_type n, charT c, const Allocator& a = Allocator());
    template<class InputIterator>
      constexpr basic_string(InputIterator begin, InputIterator end,
                             const Allocator& a = Allocator());
    template<container-compatible-range<charT> R>
      constexpr basic_string(from_range_t, R&& rg, const Allocator& a = Allocator());
    constexpr basic_string(initializer_list<charT>, const Allocator& = Allocator());
    constexpr basic_string(const basic_string&, const Allocator&);
    constexpr basic_string(basic_string&&, const Allocator&);
    constexpr ~basic_string();

    constexpr basic_string& operator=(const basic_string& str);
    constexpr basic_string& operator=(basic_string&& str)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    template<class T>
      constexpr basic_string& operator=(const T& t);
    constexpr basic_string& operator=(const charT* s);
    basic_string& operator=(nullptr_t) = delete;
    constexpr basic_string& operator=(charT c);
    constexpr basic_string& operator=(initializer_list<charT>);

    // [string.iterators], iterators
    constexpr iterator       begin() noexcept;
    constexpr const_iterator begin() const noexcept;
    constexpr iterator       end() noexcept;
    constexpr const_iterator end() const noexcept;

    constexpr reverse_iterator       rbegin() noexcept;
    constexpr const_reverse_iterator rbegin() const noexcept;
    constexpr reverse_iterator       rend() noexcept;
    constexpr const_reverse_iterator rend() const noexcept;

    constexpr const_iterator         cbegin() const noexcept;
    constexpr const_iterator         cend() const noexcept;
    constexpr const_reverse_iterator crbegin() const noexcept;
    constexpr const_reverse_iterator crend() const noexcept;

    // [string.capacity], capacity
    constexpr size_type size() const noexcept;
    constexpr size_type length() const noexcept;
    constexpr size_type max_size() const noexcept;
    constexpr void resize(size_type n, charT c);
    constexpr void resize(size_type n);
    template<class Operation> constexpr void resize_and_overwrite(size_type n, Operation op);
    constexpr size_type capacity() const noexcept;
    constexpr void reserve(size_type res_arg);
    constexpr void shrink_to_fit();
    constexpr void clear() noexcept;
    constexpr bool empty() const noexcept;

    // [string.access], element access
    constexpr const_reference operator[](size_type pos) const;
    constexpr reference       operator[](size_type pos);
    constexpr const_reference at(size_type n) const;
    constexpr reference       at(size_type n);

    constexpr const charT& front() const;
    constexpr charT&       front();
    constexpr const charT& back() const;
    constexpr charT&       back();

    // [string.modifiers], modifiers
    constexpr basic_string& operator+=(const basic_string& str);
    template<class T>
      constexpr basic_string& operator+=(const T& t);
    constexpr basic_string& operator+=(const charT* s);
    constexpr basic_string& operator+=(charT c);
    constexpr basic_string& operator+=(initializer_list<charT>);
    constexpr basic_string& append(const basic_string& str);
    constexpr basic_string& append(const basic_string& str, size_type pos, size_type n = npos);
    template<class T>
      constexpr basic_string& append(const T& t);
    template<class T>
      constexpr basic_string& append(const T& t, size_type pos, size_type n = npos);
    constexpr basic_string& append(const charT* s, size_type n);
    constexpr basic_string& append(const charT* s);
    constexpr basic_string& append(size_type n, charT c);
    template<class InputIterator>
      constexpr basic_string& append(InputIterator first, InputIterator last);
    template<container-compatible-range<charT> R>
      constexpr basic_string& append_range(R&& rg);
    constexpr basic_string& append(initializer_list<charT>);

    constexpr void push_back(charT c);

    constexpr basic_string& assign(const basic_string& str);
    constexpr basic_string& assign(basic_string&& str)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    constexpr basic_string& assign(const basic_string& str, size_type pos, size_type n = npos);
    template<class T>
      constexpr basic_string& assign(const T& t);
    template<class T>
      constexpr basic_string& assign(const T& t, size_type pos, size_type n = npos);
    constexpr basic_string& assign(const charT* s, size_type n);
    constexpr basic_string& assign(const charT* s);
    constexpr basic_string& assign(size_type n, charT c);
    template<class InputIterator>
      constexpr basic_string& assign(InputIterator first, InputIterator last);
    template<container-compatible-range<charT> R>
      constexpr basic_string& assign_range(R&& rg);
    constexpr basic_string& assign(initializer_list<charT>);

    constexpr basic_string& insert(size_type pos, const basic_string& str);
    constexpr basic_string& insert(size_type pos1, const basic_string& str,
                                   size_type pos2, size_type n = npos);
    template<class T>
      constexpr basic_string& insert(size_type pos, const T& t);
    template<class T>
      constexpr basic_string& insert(size_type pos1, const T& t,
                                     size_type pos2, size_type n = npos);
    constexpr basic_string& insert(size_type pos, const charT* s, size_type n);
    constexpr basic_string& insert(size_type pos, const charT* s);
    constexpr basic_string& insert(size_type pos, size_type n, charT c);
    constexpr iterator insert(const_iterator p, charT c);
    constexpr iterator insert(const_iterator p, size_type n, charT c);
    template<class InputIterator>
      constexpr iterator insert(const_iterator p, InputIterator first, InputIterator last);
    template<container-compatible-range<charT> R>
      constexpr iterator insert_range(const_iterator p, R&& rg);
    constexpr iterator insert(const_iterator p, initializer_list<charT>);

    constexpr basic_string& erase(size_type pos = 0, size_type n = npos);
    constexpr iterator erase(const_iterator p);
    constexpr iterator erase(const_iterator first, const_iterator last);

    constexpr void pop_back();

    constexpr basic_string& replace(size_type pos1, size_type n1, const basic_string& str);
    constexpr basic_string& replace(size_type pos1, size_type n1, const basic_string& str,
                                    size_type pos2, size_type n2 = npos);
    template<class T>
      constexpr basic_string& replace(size_type pos1, size_type n1, const T& t);
    template<class T>
      constexpr basic_string& replace(size_type pos1, size_type n1, const T& t,
                                      size_type pos2, size_type n2 = npos);
    constexpr basic_string& replace(size_type pos, size_type n1, const charT* s, size_type n2);
    constexpr basic_string& replace(size_type pos, size_type n1, const charT* s);
    constexpr basic_string& replace(size_type pos, size_type n1, size_type n2, charT c);
    constexpr basic_string& replace(const_iterator i1, const_iterator i2,
                                    const basic_string& str);
    template<class T>
      constexpr basic_string& replace(const_iterator i1, const_iterator i2, const T& t);
    constexpr basic_string& replace(const_iterator i1, const_iterator i2, const charT* s,
                                    size_type n);
    constexpr basic_string& replace(const_iterator i1, const_iterator i2, const charT* s);
    constexpr basic_string& replace(const_iterator i1, const_iterator i2, size_type n, charT c);
    template<class InputIterator>
      constexpr basic_string& replace(const_iterator i1, const_iterator i2,
                                      InputIterator j1, InputIterator j2);
    template<container-compatible-range<charT> R>
      constexpr basic_string& replace_with_range(const_iterator i1, const_iterator i2, R&& rg);
    constexpr basic_string& replace(const_iterator, const_iterator, initializer_list<charT>);

    constexpr size_type copy(charT* s, size_type n, size_type pos = 0) const;

    constexpr void swap(basic_string& str)
      noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
               allocator_traits<Allocator>::is_always_equal::value);

    // [string.ops], string operations
    constexpr const charT* c_str() const noexcept;
    constexpr const charT* data() const noexcept;
    constexpr charT* data() noexcept;
    constexpr operator basic_string_view<charT, traits>() const noexcept;
    constexpr allocator_type get_allocator() const noexcept;

    template<class T>
      constexpr size_type find(const T& t, size_type pos = 0) const noexcept(see below);
    constexpr size_type find(const basic_string& str, size_type pos = 0) const noexcept;
    constexpr size_type find(const charT* s, size_type pos, size_type n) const;
    constexpr size_type find(const charT* s, size_type pos = 0) const;
    constexpr size_type find(charT c, size_type pos = 0) const noexcept;
    template<class T>
      constexpr size_type rfind(const T& t, size_type pos = npos) const noexcept(see below);
    constexpr size_type rfind(const basic_string& str, size_type pos = npos) const noexcept;
    constexpr size_type rfind(const charT* s, size_type pos, size_type n) const;
    constexpr size_type rfind(const charT* s, size_type pos = npos) const;
    constexpr size_type rfind(charT c, size_type pos = npos) const noexcept;

    template<class T>
      constexpr size_type find_first_of(const T& t, size_type pos = 0) const noexcept(see below);
    constexpr size_type find_first_of(const basic_string& str, size_type pos = 0) const noexcept;
    constexpr size_type find_first_of(const charT* s, size_type pos, size_type n) const;
    constexpr size_type find_first_of(const charT* s, size_type pos = 0) const;
    constexpr size_type find_first_of(charT c, size_type pos = 0) const noexcept;
    template<class T>
      constexpr size_type find_last_of(const T& t,
                                       size_type pos = npos) const noexcept(see below);
    constexpr size_type find_last_of(const basic_string& str,
                                     size_type pos = npos) const noexcept;
    constexpr size_type find_last_of(const charT* s, size_type pos, size_type n) const;
    constexpr size_type find_last_of(const charT* s, size_type pos = npos) const;
    constexpr size_type find_last_of(charT c, size_type pos = npos) const noexcept;

    template<class T>
      constexpr size_type find_first_not_of(const T& t,
                                            size_type pos = 0) const noexcept(see below);
    constexpr size_type find_first_not_of(const basic_string& str,
                                          size_type pos = 0) const noexcept;
    constexpr size_type find_first_not_of(const charT* s, size_type pos, size_type n) const;
    constexpr size_type find_first_not_of(const charT* s, size_type pos = 0) const;
    constexpr size_type find_first_not_of(charT c, size_type pos = 0) const noexcept;
    template<class T>
      constexpr size_type find_last_not_of(const T& t,
                                           size_type pos = npos) const noexcept(see below);
    constexpr size_type find_last_not_of(const basic_string& str,
                                         size_type pos = npos) const noexcept;
    constexpr size_type find_last_not_of(const charT* s, size_type pos, size_type n) const;
    constexpr size_type find_last_not_of(const charT* s, size_type pos = npos) const;
    constexpr size_type find_last_not_of(charT c, size_type pos = npos) const noexcept;

    constexpr basic_string substr(size_type pos = 0, size_type n = npos) const &;
    constexpr basic_string substr(size_type pos = 0, size_type n = npos) &&;
    constexpr basic_string_view<charT, traits> subview(size_type pos = 0,
                                                       size_type n = npos) const;

    template<class T>
      constexpr int compare(const T& t) const noexcept(see below);
    template<class T>
      constexpr int compare(size_type pos1, size_type n1, const T& t) const;
    template<class T>
      constexpr int compare(size_type pos1, size_type n1, const T& t,
                            size_type pos2, size_type n2 = npos) const;
    constexpr int compare(const basic_string& str) const noexcept;
    constexpr int compare(size_type pos1, size_type n1, const basic_string& str) const;
    constexpr int compare(size_type pos1, size_type n1, const basic_string& str,
                          size_type pos2, size_type n2 = npos) const;
    constexpr int compare(const charT* s) const;
    constexpr int compare(size_type pos1, size_type n1, const charT* s) const;
    constexpr int compare(size_type pos1, size_type n1, const charT* s, size_type n2) const;

    constexpr bool starts_with(basic_string_view<charT, traits> x) const noexcept;
    constexpr bool starts_with(charT x) const noexcept;
    constexpr bool starts_with(const charT* x) const;
    constexpr bool ends_with(basic_string_view<charT, traits> x) const noexcept;
    constexpr bool ends_with(charT x) const noexcept;
    constexpr bool ends_with(const charT* x) const;

    constexpr bool contains(basic_string_view<charT, traits> x) const noexcept;
    constexpr bool contains(charT x) const noexcept;
    constexpr bool contains(const charT* x) const;
  };

  template<class InputIterator,
           class Allocator = allocator<typename iterator_traits<InputIterator>::value_type>>
    basic_string(InputIterator, InputIterator, Allocator = Allocator())
      -> basic_string<typename iterator_traits<InputIterator>::value_type,
                      char_traits<typename iterator_traits<InputIterator>::value_type>,
                      Allocator>;

  template<ranges::input_range R,
           class Allocator = allocator<ranges::range_value_t<R>>>
    basic_string(from_range_t, R&&, Allocator = Allocator())
      -> basic_string<ranges::range_value_t<R>, char_traits<ranges::range_value_t<R>>,
                      Allocator>;

  template<class charT,
           class traits,
           class Allocator = allocator<charT>>
    explicit basic_string(basic_string_view<charT, traits>, const Allocator& = Allocator())
      -> basic_string<charT, traits, Allocator>;

  template<class charT,
           class traits,
           class Allocator = allocator<charT>>
    basic_string(basic_string_view<charT, traits>,
                 typename see below::size_type, typename see below::size_type,
                 const Allocator& = Allocator())
      -> basic_string<charT, traits, Allocator>;
}
```

A `size_type` parameter type in a `basic_string` deduction guide refers
to the `size_type` member type of the type deduced by the deduction
guide.

The types `iterator` and `const_iterator` meet the constexpr iterator
requirements [[iterator.requirements.general]].

#### General requirements <a id="string.require">[[string.require]]</a>

If any operation would cause `size()` to exceed `max_size()`, that
operation throws an exception object of type `length_error`.

If any member function or operator of `basic_string` throws an
exception, that function or operator has no other effect on the
`basic_string` object.

Every object of type `basic_string<charT, traits, Allocator>` uses an
object of type `Allocator` to allocate and free storage for the
contained `charT` objects as needed. The `Allocator` object used is
obtained as described in [[container.reqmts]]. In every specialization
`basic_string<charT, traits, Allocator>`, the type `traits` shall meet
the character traits requirements [[char.traits]].

[*Note 1*: Every specialization
`basic_string<charT, traits, Allocator>` is an allocator-aware container
[[container.alloc.reqmts]], but does not use the allocator’s `construct`
and `destroy` member functions [[container.requirements.pre]]. The
program is ill-formed if `Allocator::value_type` is not the same type as
`charT`. — *end note*]

[*Note 2*: The program is ill-formed if `traits::char_type` is not the
same type as `charT`. — *end note*]

References, pointers, and iterators referring to the elements of a
`basic_string` sequence may be invalidated by the following uses of that
`basic_string` object:

- Passing as an argument to any standard library function taking a
  reference to non-const `basic_string` as an argument.[^3]
- Calling non-const member functions, except `operator[]`, `at`, `data`,
  `front`, `back`, `begin`, `rbegin`, `end`, and `rend`.

#### Constructors and assignment operators <a id="string.cons">[[string.cons]]</a>

``` cpp
constexpr explicit basic_string(const Allocator& a) noexcept;
```

*Ensures:* `size()` is equal to `0`.

``` cpp
constexpr basic_string(const basic_string& str);
constexpr basic_string(basic_string&& str) noexcept;
```

*Effects:* Constructs an object whose value is that of `str` prior to
this call.

*Remarks:* In the second form, `str` is left in a valid but unspecified
state.

``` cpp
constexpr basic_string(const basic_string& str, size_type pos,
                       const Allocator& a = Allocator());
constexpr basic_string(const basic_string& str, size_type pos, size_type n,
                       const Allocator& a = Allocator());
constexpr basic_string(basic_string&& str, size_type pos,
                       const Allocator& a = Allocator());
constexpr basic_string(basic_string&& str, size_type pos, size_type n,
                       const Allocator& a = Allocator());
```

Let

- `s` be the value of `str` prior to this call and
- `rlen` be `pos + min(n, s.size() - pos)` for the overloads with
  parameter `n`, and `s.size()` otherwise.

*Effects:* Constructs an object whose initial value is the range
\[`s.data() + pos`, `s.data() + rlen`).

*Throws:* `out_of_range` if `pos > s.size()`.

*Remarks:* For the overloads with a `basic_string&&` parameter, `str` is
left in a valid but unspecified state.

*Recommended practice:* For the overloads with a `basic_string&&`
parameter, implementations should avoid allocation if
`s.get_allocator() == a` is `true`.

``` cpp
template<class T>
  constexpr basic_string(const T& t, size_type pos, size_type n, const Allocator& a = Allocator());
```

*Constraints:*
`is_convertible_v<const T&, basic_string_view<charT, traits>>` is
`true`.

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t;` and then behaves the same as:

``` cpp
basic_string(sv.substr(pos, n), a);
```

``` cpp
template<class T>
  constexpr explicit basic_string(const T& t, const Allocator& a = Allocator());
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Creates a variable, `sv`, as if by
`basic_string_view<charT, traits> sv = t;` and then behaves the same as
`basic_string(sv.data(), sv.size(), a)`.

``` cpp
constexpr basic_string(const charT* s, size_type n, const Allocator& a = Allocator());
```

*Preconditions:* \[`s`, `s + n`) is a valid range.

*Effects:* Constructs an object whose initial value is the range \[`s`,
`s + n`).

*Ensures:* `size()` is equal to `n`, and `traits::compare(data(), s, n)`
is equal to `0`.

``` cpp
constexpr basic_string(const charT* s, const Allocator& a = Allocator());
```

*Constraints:* `Allocator` is a type that qualifies as an
allocator [[container.reqmts]].

[*Note 1*: This affects class template argument
deduction. — *end note*]

*Effects:* Equivalent to: `basic_string(s, traits::length(s), a)`.

``` cpp
constexpr basic_string(size_type n, charT c, const Allocator& a = Allocator());
```

*Constraints:* `Allocator` is a type that qualifies as an
allocator [[container.reqmts]].

[*Note 2*: This affects class template argument
deduction. — *end note*]

*Effects:* Constructs an object whose value consists of `n` copies of
`c`.

``` cpp
template<class InputIterator>
  constexpr basic_string(InputIterator begin, InputIterator end, const Allocator& a = Allocator());
```

*Constraints:* `InputIterator` is a type that qualifies as an input
iterator [[container.reqmts]].

*Effects:* Constructs a string from the values in the range \[`begin`,
`end`), as specified in [[sequence.reqmts]].

``` cpp
template<container-compatible-range<charT> R>
  constexpr basic_string(from_range_t, R&& rg, const Allocator& = Allocator());
```

*Effects:* Constructs a string from the values in the range `rg`, as
specified in [[sequence.reqmts]].

``` cpp
constexpr basic_string(initializer_list<charT> il, const Allocator& a = Allocator());
```

*Effects:* Equivalent to `basic_string(il.begin(), il.end(), a)`.

``` cpp
constexpr basic_string(const basic_string& str, const Allocator& alloc);
constexpr basic_string(basic_string&& str, const Allocator& alloc);
```

*Effects:* Constructs an object whose value is that of `str` prior to
this call. The stored allocator is constructed from `alloc`. In the
second form, `str` is left in a valid but unspecified state.

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

*Constraints:* `InputIterator` is a type that qualifies as an input
iterator, and `Allocator` is a type that qualifies as an
allocator [[container.reqmts]].

``` cpp
template<class charT,
         class traits,
         class Allocator = allocator<charT>>
  explicit basic_string(basic_string_view<charT, traits>, const Allocator& = Allocator())
    -> basic_string<charT, traits, Allocator>;

template<class charT,
         class traits,
         class Allocator = allocator<charT>>
  basic_string(basic_string_view<charT, traits>,
               typename see below::size_type, typename see below::size_type,
               const Allocator& = Allocator())
    -> basic_string<charT, traits, Allocator>;
```

*Constraints:* `Allocator` is a type that qualifies as an
allocator [[container.reqmts]].

``` cpp
constexpr basic_string& operator=(const basic_string& str);
```

*Effects:* If `*this` and `str` are the same object, has no effect.
Otherwise, replaces the value of `*this` with a copy of `str`.

*Returns:* `*this`.

``` cpp
constexpr basic_string& operator=(basic_string&& str)
  noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Effects:* Move assigns as a sequence container [[sequence.reqmts]],
except that iterators, pointers and references may be invalidated.

*Returns:* `*this`.

``` cpp
template<class T>
  constexpr basic_string& operator=(const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return assign(sv);
```

``` cpp
constexpr basic_string& operator=(const charT* s);
```

*Effects:* Equivalent to:
`return *this = basic_string_view<charT, traits>(s);`

``` cpp
constexpr basic_string& operator=(charT c);
```

*Effects:* Equivalent to:

``` cpp
return *this = basic_string_view<charT, traits>(addressof(c), 1);
```

``` cpp
constexpr basic_string& operator=(initializer_list<charT> il);
```

*Effects:* Equivalent to:

``` cpp
return *this = basic_string_view<charT, traits>(il.begin(), il.size());
```

#### Iterator support <a id="string.iterators">[[string.iterators]]</a>

``` cpp
constexpr iterator       begin() noexcept;
constexpr const_iterator begin() const noexcept;
constexpr const_iterator cbegin() const noexcept;
```

*Returns:* An iterator referring to the first character in the string.

``` cpp
constexpr iterator       end() noexcept;
constexpr const_iterator end() const noexcept;
constexpr const_iterator cend() const noexcept;
```

*Returns:* An iterator which is the past-the-end value.

``` cpp
constexpr reverse_iterator       rbegin() noexcept;
constexpr const_reverse_iterator rbegin() const noexcept;
constexpr const_reverse_iterator crbegin() const noexcept;
```

*Returns:* An iterator which is semantically equivalent to
`reverse_iterator(end())`.

``` cpp
constexpr reverse_iterator       rend() noexcept;
constexpr const_reverse_iterator rend() const noexcept;
constexpr const_reverse_iterator crend() const noexcept;
```

*Returns:* An iterator which is semantically equivalent to
`reverse_iterator(begin())`.

#### Capacity <a id="string.capacity">[[string.capacity]]</a>

``` cpp
constexpr size_type size() const noexcept;
constexpr size_type length() const noexcept;
```

*Returns:* A count of the number of char-like objects currently in the
string.

*Complexity:* Constant time.

``` cpp
constexpr size_type max_size() const noexcept;
```

*Returns:* The largest possible number of char-like objects that can be
stored in a `basic_string`.

*Complexity:* Constant time.

``` cpp
constexpr void resize(size_type n, charT c);
```

*Effects:* Alters the value of `*this` as follows:

- If `n <= size()`, erases the last `size() - n` elements.
- If `n > size()`, appends `n - size()` copies of `c`.

``` cpp
constexpr void resize(size_type n);
```

*Effects:* Equivalent to `resize(n, charT())`.

``` cpp
template<class Operation> constexpr void resize_and_overwrite(size_type n, Operation op);
```

Let

- `o = size()` before the call to `resize_and_overwrite`.
- `k` be `min(o, n)`.
- `p` be a value of type `charT*` or `charT* const`, such that the range
  \[`p`, `p + n`\] is valid and `this->compare(0, k, p, k) == 0` is
  `true` before the call. The values in the range \[`p + k`, `p + n`\]
  may be indeterminate [[basic.indet]].
- `m` be a value of type `size_type` or `const size_type` equal to `n`.
- *`OP`* be the expression `std::move(op)(p, m)`.
- `r` = *`OP`*.

*Mandates:* *`OP`* has an integer-like type [[iterator.concept.winc]].

*Preconditions:*

- *`OP`* does not throw an exception or modify `p` or `m`.
- `r` ≥ 0.
- `r` ≤ `m`.
- After evaluating *`OP`* there are no indeterminate values in the range
  \[`p`, `p + r`).

*Effects:* Evaluates *`OP`*, replaces the contents of `*this` with
\[`p`, `p + r`), and invalidates all pointers and references to the
range \[`p`, `p + n`\].

*Recommended practice:* Implementations should avoid unnecessary copies
and allocations by, for example, making `p` a pointer into internal
storage and by restoring `*(p + r)` to `charT()` after evaluating
*`OP`*.

``` cpp
constexpr size_type capacity() const noexcept;
```

*Returns:* The size of the allocated storage in the string.

*Complexity:* Constant time.

``` cpp
constexpr void reserve(size_type res_arg);
```

*Effects:* A directive that informs a `basic_string` of a planned change
in size, so that the storage allocation can be managed accordingly.
Following a call to `reserve`, `capacity()` is greater or equal to the
argument of `reserve` if reallocation happens; and equal to the previous
value of `capacity()` otherwise. Reallocation happens at this point if
and only if the current capacity is less than the argument of `reserve`.

*Throws:* `length_error` if `res_arg > max_size()` or any exceptions
thrown by `allocator_traits` `<Allocator>::allocate`.

``` cpp
constexpr void shrink_to_fit();
```

*Effects:* `shrink_to_fit` is a non-binding request to reduce
`capacity()` to `size()`.

[*Note 1*: The request is non-binding to allow latitude for
implementation-specific optimizations. — *end note*]

It does not increase `capacity()`, but may reduce `capacity()` by
causing reallocation.

*Complexity:* If the size is not equal to the old capacity, linear in
the size of the sequence; otherwise constant.

*Remarks:* Reallocation invalidates all the references, pointers, and
iterators referring to the elements in the sequence, as well as the
past-the-end iterator.

[*Note 2*: If no reallocation happens, they remain
valid. — *end note*]

``` cpp
constexpr void clear() noexcept;
```

*Effects:* Equivalent to: `erase(begin(), end());`

``` cpp
constexpr bool empty() const noexcept;
```

*Effects:* Equivalent to: `return size() == 0;`

#### Element access <a id="string.access">[[string.access]]</a>

``` cpp
constexpr const_reference operator[](size_type pos) const;
constexpr reference       operator[](size_type pos);
```

`pos <= size()` is `true`.

*Returns:* `*(begin() + pos)` if `pos < size()`. Otherwise, returns a
reference to an object of type `charT` with value `charT()`, where
modifying the object to any value other than `charT()` leads to
undefined behavior.

*Throws:* Nothing.

*Complexity:* Constant time.

``` cpp
constexpr const_reference at(size_type pos) const;
constexpr reference       at(size_type pos);
```

*Returns:* `operator[](pos)`.

*Throws:* `out_of_range` if `pos >= size()`.

``` cpp
constexpr const charT& front() const;
constexpr charT& front();
```

`empty()` is `false`.

*Effects:* Equivalent to: `return operator[](0);`

``` cpp
constexpr const charT& back() const;
constexpr charT& back();
```

`empty()` is `false`.

*Effects:* Equivalent to: `return operator[](size() - 1);`

#### Modifiers <a id="string.modifiers">[[string.modifiers]]</a>

##### `basic_string::operator+=` <a id="string.op.append">[[string.op.append]]</a>

``` cpp
constexpr basic_string& operator+=(const basic_string& str);
```

*Effects:* Equivalent to: `return append(str);`

``` cpp
template<class T>
  constexpr basic_string& operator+=(const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return append(sv);
```

``` cpp
constexpr basic_string& operator+=(const charT* s);
```

*Effects:* Equivalent to: `return append(s);`

``` cpp
constexpr basic_string& operator+=(charT c);
```

*Effects:* Equivalent to: `return append(size_type{1}, c);`

``` cpp
constexpr basic_string& operator+=(initializer_list<charT> il);
```

*Effects:* Equivalent to: `return append(il);`

##### `basic_string::append` <a id="string.append">[[string.append]]</a>

``` cpp
constexpr basic_string& append(const basic_string& str);
```

*Effects:* Equivalent to: `return append(str.data(), str.size());`

``` cpp
constexpr basic_string& append(const basic_string& str, size_type pos, size_type n = npos);
```

*Effects:* Equivalent to:

``` cpp
return append(basic_string_view<charT, traits>(str).substr(pos, n));
```

``` cpp
template<class T>
  constexpr basic_string& append(const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return append(sv.data(), sv.size());
```

``` cpp
template<class T>
  constexpr basic_string& append(const T& t, size_type pos, size_type n = npos);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return append(sv.substr(pos, n));
```

``` cpp
constexpr basic_string& append(const charT* s, size_type n);
```

*Preconditions:* \[`s`, `s + n`) is a valid range.

*Effects:* Appends a copy of the range \[`s`, `s + n`) to the string.

*Returns:* `*this`.

``` cpp
constexpr basic_string& append(const charT* s);
```

*Effects:* Equivalent to: `return append(s, traits::length(s));`

``` cpp
constexpr basic_string& append(size_type n, charT c);
```

*Effects:* Appends `n` copies of `c` to the string.

*Returns:* `*this`.

``` cpp
template<class InputIterator>
  constexpr basic_string& append(InputIterator first, InputIterator last);
```

*Constraints:* `InputIterator` is a type that qualifies as an input
iterator [[container.reqmts]].

*Effects:* Equivalent to:
`return append(basic_string(first, last, get_allocator()));`

``` cpp
template<container-compatible-range<charT> R>
  constexpr basic_string& append_range(R&& rg);
```

*Effects:* Equivalent to:
`return append(basic_string(from_range, std::forward<R>(rg), get_allocator()));`

``` cpp
constexpr basic_string& append(initializer_list<charT> il);
```

*Effects:* Equivalent to: `return append(il.begin(), il.size());`

``` cpp
constexpr void push_back(charT c);
```

*Effects:* Equivalent to `append(size_type{1}, c)`.

##### `basic_string::assign` <a id="string.assign">[[string.assign]]</a>

``` cpp
constexpr basic_string& assign(const basic_string& str);
```

*Effects:* Equivalent to: `return *this = str;`

``` cpp
constexpr basic_string& assign(basic_string&& str)
  noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Effects:* Equivalent to: `return *this = std::move(str);`

``` cpp
constexpr basic_string& assign(const basic_string& str, size_type pos, size_type n = npos);
```

*Effects:* Equivalent to:

``` cpp
return assign(basic_string_view<charT, traits>(str).substr(pos, n));
```

``` cpp
template<class T>
  constexpr basic_string& assign(const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return assign(sv.data(), sv.size());
```

``` cpp
template<class T>
  constexpr basic_string& assign(const T& t, size_type pos, size_type n = npos);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return assign(sv.substr(pos, n));
```

``` cpp
constexpr basic_string& assign(const charT* s, size_type n);
```

*Preconditions:* \[`s`, `s + n`) is a valid range.

*Effects:* Replaces the string controlled by `*this` with a copy of the
range \[`s`, `s + n`).

*Returns:* `*this`.

``` cpp
constexpr basic_string& assign(const charT* s);
```

*Effects:* Equivalent to: `return assign(s, traits::length(s));`

``` cpp
constexpr basic_string& assign(initializer_list<charT> il);
```

*Effects:* Equivalent to: `return assign(il.begin(), il.size());`

``` cpp
constexpr basic_string& assign(size_type n, charT c);
```

*Effects:* Equivalent to:

``` cpp
clear();
resize(n, c);
return *this;
```

``` cpp
template<class InputIterator>
  constexpr basic_string& assign(InputIterator first, InputIterator last);
```

*Constraints:* `InputIterator` is a type that qualifies as an input
iterator [[container.reqmts]].

*Effects:* Equivalent to:
`return assign(basic_string(first, last, get_allocator()));`

``` cpp
template<container-compatible-range<charT> R>
  constexpr basic_string& assign_range(R&& rg);
```

*Effects:* Equivalent to:
`return assign(basic_string(from_range, std::forward<R>(rg), get_allocator()));`

##### `basic_string::insert` <a id="string.insert">[[string.insert]]</a>

``` cpp
constexpr basic_string& insert(size_type pos, const basic_string& str);
```

*Effects:* Equivalent to: `return insert(pos, str.data(), str.size());`

``` cpp
constexpr basic_string& insert(size_type pos1, const basic_string& str,
                               size_type pos2, size_type n = npos);
```

*Effects:* Equivalent to:

``` cpp
return insert(pos1, basic_string_view<charT, traits>(str), pos2, n);
```

``` cpp
template<class T>
  constexpr basic_string& insert(size_type pos, const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return insert(pos, sv.data(), sv.size());
```

``` cpp
template<class T>
  constexpr basic_string& insert(size_type pos1, const T& t,
                                 size_type pos2, size_type n = npos);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return insert(pos1, sv.substr(pos2, n));
```

``` cpp
constexpr basic_string& insert(size_type pos, const charT* s, size_type n);
```

*Preconditions:* \[`s`, `s + n`) is a valid range.

*Effects:* Inserts a copy of the range \[`s`, `s + n`) immediately
before the character at position `pos` if `pos < size()`, or otherwise
at the end of the string.

*Returns:* `*this`.

*Throws:*

- `out_of_range` if `pos > size()`,
- `length_error` if `n > max_size() - size()`, or
- any exceptions thrown by `allocator_traits<Allocator>::allocate`.

``` cpp
constexpr basic_string& insert(size_type pos, const charT* s);
```

*Effects:* Equivalent to: `return insert(pos, s, traits::length(s));`

``` cpp
constexpr basic_string& insert(size_type pos, size_type n, charT c);
```

*Effects:* Inserts `n` copies of `c` before the character at position
`pos` if `pos < size()`, or otherwise at the end of the string.

*Returns:* `*this`.

*Throws:*

- `out_of_range` if `pos > size()`,
- `length_error` if `n > max_size() - size()`, or
- any exceptions thrown by `allocator_traits<Allocator>::allocate`.

``` cpp
constexpr iterator insert(const_iterator p, charT c);
```

*Preconditions:* `p` is a valid iterator on `*this`.

*Effects:* Inserts a copy of `c` at the position `p`.

*Returns:* An iterator which refers to the inserted character.

``` cpp
constexpr iterator insert(const_iterator p, size_type n, charT c);
```

*Preconditions:* `p` is a valid iterator on `*this`.

*Effects:* Inserts `n` copies of `c` at the position `p`.

*Returns:* An iterator which refers to the first inserted character, or
`p` if `n == 0`.

``` cpp
template<class InputIterator>
  constexpr iterator insert(const_iterator p, InputIterator first, InputIterator last);
```

*Constraints:* `InputIterator` is a type that qualifies as an input
iterator [[container.reqmts]].

*Preconditions:* `p` is a valid iterator on `*this`.

*Effects:* Equivalent to
`insert(p - begin(), basic_string(first, last, get_allocator()))`.

*Returns:* An iterator which refers to the first inserted character, or
`p` if `first == last`.

``` cpp
template<container-compatible-range<charT> R>
  constexpr iterator insert_range(const_iterator p, R&& rg);
```

*Preconditions:* `p` is a valid iterator on `*this`.

*Effects:* Equivalent to
`insert(p - begin(), basic_string(from_range, std::forward<R>(rg), get_allocator()))`.

*Returns:* An iterator which refers to the first inserted character, or
`p` if `rg` is empty.

``` cpp
constexpr iterator insert(const_iterator p, initializer_list<charT> il);
```

*Effects:* Equivalent to: `return insert(p, il.begin(), il.end());`

##### `basic_string::erase` <a id="string.erase">[[string.erase]]</a>

``` cpp
constexpr basic_string& erase(size_type pos = 0, size_type n = npos);
```

*Effects:* Determines the effective length `xlen` of the string to be
removed as the smaller of `n` and `size() - pos`. Removes the characters
in the range \[`begin() + pos`, `begin() + pos + xlen`).

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` `> size()`.

``` cpp
constexpr iterator erase(const_iterator p);
```

*Preconditions:* `p` is a valid dereferenceable iterator on `*this`.

*Effects:* Removes the character referred to by `p`.

*Returns:* An iterator which points to the element immediately following
`p` prior to the element being erased. If no such element exists,
`end()` is returned.

*Throws:* Nothing.

``` cpp
constexpr iterator erase(const_iterator first, const_iterator last);
```

*Preconditions:* `first` and `last` are valid iterators on `*this`.
\[`first`, `last`) is a valid range.

*Effects:* Removes the characters in the range \[`first`, `last`).

*Returns:* An iterator which points to the element pointed to by `last`
prior to the other elements being erased. If no such element exists,
`end()` is returned.

*Throws:* Nothing.

``` cpp
constexpr void pop_back();
```

`empty()` is `false`.

*Effects:* Equivalent to `erase(end() - 1)`.

*Throws:* Nothing.

##### `basic_string::replace` <a id="string.replace">[[string.replace]]</a>

``` cpp
constexpr basic_string& replace(size_type pos1, size_type n1, const basic_string& str);
```

*Effects:* Equivalent to:
`return replace(pos1, n1, str.data(), str.size());`

``` cpp
constexpr basic_string& replace(size_type pos1, size_type n1, const basic_string& str,
                                size_type pos2, size_type n2 = npos);
```

*Effects:* Equivalent to:

``` cpp
return replace(pos1, n1, basic_string_view<charT, traits>(str).substr(pos2, n2));
```

``` cpp
template<class T>
  constexpr basic_string& replace(size_type pos1, size_type n1, const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return replace(pos1, n1, sv.data(), sv.size());
```

``` cpp
template<class T>
  constexpr basic_string& replace(size_type pos1, size_type n1, const T& t,
                                  size_type pos2, size_type n2 = npos);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return replace(pos1, n1, sv.substr(pos2, n2));
```

``` cpp
constexpr basic_string& replace(size_type pos1, size_type n1, const charT* s, size_type n2);
```

*Preconditions:* \[`s`, `s + n2`) is a valid range.

*Effects:* Determines the effective length `xlen` of the string to be
removed as the smaller of `n1` and `size() - pos1`. If
`size() - xlen >= max_size() - n2` throws `length_error`. Otherwise, the
function replaces the characters in the range \[`begin() + pos1`,
`begin() + pos1 + xlen`) with a copy of the range \[`s`, `s + n2`).

*Returns:* `*this`.

*Throws:*

- `out_of_range` if `pos1 > size()`,
- `length_error` if the length of the resulting string would exceed
  `max_size()`, or
- any exceptions thrown by `allocator_traits<Allocator>::allocate`.

``` cpp
constexpr basic_string& replace(size_type pos, size_type n, const charT* s);
```

*Effects:* Equivalent to:
`return replace(pos, n, s, traits::length(s));`

``` cpp
constexpr basic_string& replace(size_type pos1, size_type n1, size_type n2, charT c);
```

*Effects:* Determines the effective length `xlen` of the string to be
removed as the smaller of `n1` and `size() - pos1`. If
`size() - xlen >=` `max_size() - n2` throws `length_error`. Otherwise,
the function replaces the characters in the range \[`begin() + pos1`,
`begin() + pos1 + xlen`) with `n2` copies of `c`.

*Returns:* `*this`.

*Throws:*

- `out_of_range` if `pos1 > size()`,
- `length_error` if the length of the resulting string would exceed
  `max_size()`, or
- any exceptions thrown by `allocator_traits<Allocator>::allocate.`

``` cpp
constexpr basic_string& replace(const_iterator i1, const_iterator i2, const basic_string& str);
```

*Effects:* Equivalent to:
`return replace(i1, i2, basic_string_view<charT, traits>(str));`

``` cpp
template<class T>
  constexpr basic_string& replace(const_iterator i1, const_iterator i2, const T& t);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Preconditions:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> sv = t;
return replace(i1 - begin(), i2 - i1, sv.data(), sv.size());
```

``` cpp
constexpr basic_string& replace(const_iterator i1, const_iterator i2, const charT* s, size_type n);
```

*Effects:* Equivalent to:
`return replace(i1, i2, basic_string_view<charT, traits>(s, n));`

``` cpp
constexpr basic_string& replace(const_iterator i1, const_iterator i2, const charT* s);
```

*Effects:* Equivalent to:
`return replace(i1, i2, basic_string_view<charT, traits>(s));`

``` cpp
constexpr basic_string& replace(const_iterator i1, const_iterator i2, size_type n, charT c);
```

*Preconditions:* \[`begin()`, `i1`) and \[`i1`, `i2`) are valid ranges.

*Effects:* Equivalent to: `return replace(i1 - begin(), i2 - i1, n, c);`

``` cpp
template<class InputIterator>
  constexpr basic_string& replace(const_iterator i1, const_iterator i2,
                                  InputIterator j1, InputIterator j2);
```

*Constraints:* `InputIterator` is a type that qualifies as an input
iterator [[container.reqmts]].

*Effects:* Equivalent to:
`return replace(i1, i2, basic_string(j1, j2, get_allocator()));`

``` cpp
template<container-compatible-range<charT> R>
  constexpr basic_string& replace_with_range(const_iterator i1, const_iterator i2, R&& rg);
```

*Effects:* Equivalent to:

``` cpp
return replace(i1, i2, basic_string(from_range, std::forward<R>(rg), get_allocator()));
```

``` cpp
constexpr basic_string& replace(const_iterator i1, const_iterator i2, initializer_list<charT> il);
```

*Effects:* Equivalent to:
`return replace(i1, i2, il.begin(), il.size());`

##### `basic_string::copy` <a id="string.copy">[[string.copy]]</a>

``` cpp
constexpr size_type copy(charT* s, size_type n, size_type pos = 0) const;
```

*Effects:* Equivalent to:
`return basic_string_view<charT, traits>(*this).copy(s, n, pos);`

[*Note 1*: This does not terminate `s` with a null
object. — *end note*]

##### `basic_string::swap` <a id="string.swap">[[string.swap]]</a>

``` cpp
constexpr void swap(basic_string& s)
  noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Preconditions:*
`allocator_traits<Allocator>::propagate_on_container_swap::value` is
`true` or `get_allocator() == s.get_allocator()`.

*Ensures:* `*this` contains the same sequence of characters that was in
`s`, `s` contains the same sequence of characters that was in `*this`.

*Throws:* Nothing.

*Complexity:* Constant time.

#### String operations <a id="string.ops">[[string.ops]]</a>

##### Accessors <a id="string.accessors">[[string.accessors]]</a>

``` cpp
constexpr const charT* c_str() const noexcept;
constexpr const charT* data() const noexcept;
```

*Returns:* A pointer `p` such that `p + i == addressof(operator[](i))`
for each `i` in \[`0`, `size()`\].

*Complexity:* Constant time.

*Remarks:* The program shall not modify any of the values stored in the
character array; otherwise, the behavior is undefined.

``` cpp
constexpr charT* data() noexcept;
```

*Returns:* A pointer `p` such that `p + i == addressof(operator[](i))`
for each `i` in \[`0`, `size()`\].

*Complexity:* Constant time.

*Remarks:* The program shall not modify the value stored at `p + size()`
to any value other than `charT()`; otherwise, the behavior is undefined.

``` cpp
constexpr operator basic_string_view<charT, traits>() const noexcept;
```

*Effects:* Equivalent to:
`return basic_string_view<charT, traits>(data(), size());`

``` cpp
constexpr allocator_type get_allocator() const noexcept;
```

*Returns:* A copy of the `Allocator` object used to construct the string
or, if that allocator has been replaced, a copy of the most recent
replacement.

##### Searching <a id="string.find">[[string.find]]</a>

Let *F* be one of `find`, `rfind`, `find_first_of`, `find_last_of`,
`find_first_not_of`, and `find_last_not_of`.

- Each member function of the form
  ``` cpp
  constexpr size_type F(const basic_string& str, size_type pos) const noexcept;
  ```

  has effects equivalent to:
  `return F(basic_string_view<charT, traits>(str), pos);`
- Each member function of the form
  ``` cpp
  constexpr size_type F(const charT* s, size_type pos) const;
  ```

  has effects equivalent to:
  `return F(basic_string_view<charT, traits>(s), pos);`
- Each member function of the form
  ``` cpp
  constexpr size_type F(const charT* s, size_type pos, size_type n) const;
  ```

  has effects equivalent to:
  `return F(basic_string_view<charT, traits>(s, n), pos);`
- Each member function of the form
  ``` cpp
  constexpr size_type F(charT c, size_type pos) const noexcept;
  ```

  has effects equivalent to:
  ``` cpp
  return F(basic_string_view<charT, traits>(addressof(c), 1), pos);
  ```

``` cpp
template<class T>
  constexpr size_type find(const T& t, size_type pos = 0) const noexcept(see below);
template<class T>
  constexpr size_type rfind(const T& t, size_type pos = npos) const noexcept(see below);
template<class T>
  constexpr size_type find_first_of(const T& t, size_type pos = 0) const noexcept(see below);
template<class T>
  constexpr size_type find_last_of(const T& t, size_type pos = npos) const noexcept(see below);
template<class T>
  constexpr size_type find_first_not_of(const T& t, size_type pos = 0) const noexcept(see below);
template<class T>
  constexpr size_type find_last_not_of(const T& t, size_type pos = npos) const noexcept(see below);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Let *G* be the name of the function. Equivalent to:

``` cpp
basic_string_view<charT, traits> s = *this, sv = t;
return s.G(sv, pos);
```

*Remarks:* The exception specification is equivalent to
`is_nothrow_convertible_v<const T&, basic_string_view<charT, traits>>`.

##### `basic_string::substr` <a id="string.substr">[[string.substr]]</a>

``` cpp
constexpr basic_string substr(size_type pos = 0, size_type n = npos) const &;
```

*Effects:* Equivalent to: `return basic_string(*this, pos, n);`

``` cpp
constexpr basic_string substr(size_type pos = 0, size_type n = npos) &&;
```

*Effects:* Equivalent to:
`return basic_string(std::move(*this), pos, n);`

``` cpp
constexpr basic_string_view<charT, traits> subview(size_type pos = 0, size_type n = npos) const;
```

*Effects:* Equivalent to:
`return basic_string_view<charT, traits>(*this).subview(pos, n);`

##### `basic_string::compare` <a id="string.compare">[[string.compare]]</a>

``` cpp
template<class T>
  constexpr int compare(const T& t) const noexcept(see below);
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:
`return basic_string_view<charT, traits>(*this).compare(t);`

*Remarks:* The exception specification is equivalent to
`is_nothrow_convertible_v<const T&, basic_string_view<charT, traits>>`.

``` cpp
template<class T>
  constexpr int compare(size_type pos1, size_type n1, const T& t) const;
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
return basic_string_view<charT, traits>(*this).substr(pos1, n1).compare(t);
```

``` cpp
template<class T>
  constexpr int compare(size_type pos1, size_type n1, const T& t,
                        size_type pos2, size_type n2 = npos) const;
```

*Constraints:*

- `is_convertible_v<const T&, basic_string_view<charT, traits>>` is
  `true` and
- `is_convertible_v<const T&, const charT*>` is `false`.

*Effects:* Equivalent to:

``` cpp
basic_string_view<charT, traits> s = *this, sv = t;
return s.substr(pos1, n1).compare(sv.substr(pos2, n2));
```

``` cpp
constexpr int compare(const basic_string& str) const noexcept;
```

*Effects:* Equivalent to:
`return compare(basic_string_view<charT, traits>(str));`

``` cpp
constexpr int compare(size_type pos1, size_type n1, const basic_string& str) const;
```

*Effects:* Equivalent to:
`return compare(pos1, n1, basic_string_view<charT, traits>(str));`

``` cpp
constexpr int compare(size_type pos1, size_type n1, const basic_string& str,
                      size_type pos2, size_type n2 = npos) const;
```

*Effects:* Equivalent to:

``` cpp
return compare(pos1, n1, basic_string_view<charT, traits>(str), pos2, n2);
```

``` cpp
constexpr int compare(const charT* s) const;
```

*Effects:* Equivalent to:
`return compare(basic_string_view<charT, traits>(s));`

``` cpp
constexpr int compare(size_type pos, size_type n1, const charT* s) const;
```

*Effects:* Equivalent to:
`return compare(pos, n1, basic_string_view<charT, traits>(s));`

``` cpp
constexpr int compare(size_type pos, size_type n1, const charT* s, size_type n2) const;
```

*Effects:* Equivalent to:
`return compare(pos, n1, basic_string_view<charT, traits>(s, n2));`

##### `basic_string::starts_with` <a id="string.starts.with">[[string.starts.with]]</a>

``` cpp
constexpr bool starts_with(basic_string_view<charT, traits> x) const noexcept;
constexpr bool starts_with(charT x) const noexcept;
constexpr bool starts_with(const charT* x) const;
```

*Effects:* Equivalent to:

``` cpp
return basic_string_view<charT, traits>(data(), size()).starts_with(x);
```

##### `basic_string::ends_with` <a id="string.ends.with">[[string.ends.with]]</a>

``` cpp
constexpr bool ends_with(basic_string_view<charT, traits> x) const noexcept;
constexpr bool ends_with(charT x) const noexcept;
constexpr bool ends_with(const charT* x) const;
```

*Effects:* Equivalent to:

``` cpp
return basic_string_view<charT, traits>(data(), size()).ends_with(x);
```

##### `basic_string::contains` <a id="string.contains">[[string.contains]]</a>

``` cpp
constexpr bool contains(basic_string_view<charT, traits> x) const noexcept;
constexpr bool contains(charT x) const noexcept;
constexpr bool contains(const charT* x) const;
```

*Effects:* Equivalent to:

``` cpp
return basic_string_view<charT, traits>(data(), size()).contains(x);
```

### Non-member functions <a id="string.nonmembers">[[string.nonmembers]]</a>

#### `operator+` <a id="string.op.plus">[[string.op.plus]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              const basic_string<charT, traits, Allocator>& rhs);
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs, const charT* rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_string<charT, traits, Allocator> r = lhs;
r.append(rhs);
return r;
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              const basic_string<charT, traits, Allocator>& rhs);
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs, const charT* rhs);
```

*Effects:* Equivalent to:

``` cpp
lhs.append(rhs);
return std::move(lhs);
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              basic_string<charT, traits, Allocator>&& rhs);
```

*Effects:* Equivalent to:

``` cpp
lhs.append(rhs);
return std::move(lhs);
```

except that both `lhs` and `rhs` are left in valid but unspecified
states.

[*Note 1*: If `lhs` and `rhs` have equal allocators, the implementation
can move from either. — *end note*]

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              basic_string<charT, traits, Allocator>&& rhs);
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const charT* lhs, basic_string<charT, traits, Allocator>&& rhs);
```

*Effects:* Equivalent to:

``` cpp
rhs.insert(0, lhs);
return std::move(rhs);
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const charT* lhs, const basic_string<charT, traits, Allocator>& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_string<charT, traits, Allocator> r = rhs;
r.insert(0, lhs);
return r;
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(charT lhs, const basic_string<charT, traits, Allocator>& rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_string<charT, traits, Allocator> r = rhs;
r.insert(r.begin(), lhs);
return r;
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(charT lhs, basic_string<charT, traits, Allocator>&& rhs);
```

*Effects:* Equivalent to:

``` cpp
rhs.insert(rhs.begin(), lhs);
return std::move(rhs);
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs, charT rhs);
```

*Effects:* Equivalent to:

``` cpp
basic_string<charT, traits, Allocator> r = lhs;
r.push_back(rhs);
return r;
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs, charT rhs);
```

*Effects:* Equivalent to:

``` cpp
lhs.push_back(rhs);
return std::move(lhs);
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(const basic_string<charT, traits, Allocator>& lhs,
              type_identity_t<basic_string_view<charT, traits>> rhs);
```

Equivalent to:

``` cpp
basic_string<charT, traits, Allocator> r = lhs;
r.append(rhs);
return r;
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(basic_string<charT, traits, Allocator>&& lhs,
              type_identity_t<basic_string_view<charT, traits>> rhs);
```

Equivalent to:

``` cpp
lhs.append(rhs);
return std::move(lhs);
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(type_identity_t<basic_string_view<charT, traits>> lhs,
              const basic_string<charT, traits, Allocator>& rhs);
```

Equivalent to:

``` cpp
basic_string<charT, traits, Allocator> r = rhs;
r.insert(0, lhs);
return r;
```

``` cpp
template<class charT, class traits, class Allocator>
  constexpr basic_string<charT, traits, Allocator>
    operator+(type_identity_t<basic_string_view<charT, traits>> lhs,
              basic_string<charT, traits, Allocator>&& rhs);
```

Equivalent to:

``` cpp
rhs.insert(0, lhs);
return std::move(rhs);
```

[*Note 1*: Using a specialization of `type_identity_t` as a parameter
type ensures that an object of type
`basic_string<charT, traits, Allocator>` can be concatenated with an
object of a type `T` having an implicit conversion to
`basic_string_view<charT, traits>` [[over.match.oper]]. — *end note*]

#### Non-member comparison operator functions <a id="string.cmp">[[string.cmp]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  constexpr bool
    operator==(const basic_string<charT, traits, Allocator>& lhs,
               const basic_string<charT, traits, Allocator>& rhs) noexcept;
template<class charT, class traits, class Allocator>
  constexpr bool operator==(const basic_string<charT, traits, Allocator>& lhs,
                            const charT* rhs);

template<class charT, class traits, class Allocator>
  constexpr see below operator<=>(const basic_string<charT, traits, Allocator>& lhs,
            \itcorr                      const basic_string<charT, traits, Allocator>& rhs) noexcept;
template<class charT, class traits, class Allocator>
  constexpr see below operator<=>(const basic_string<charT, traits, Allocator>& lhs,
            \itcorr                      const charT* rhs);
```

*Effects:* Let *`op`* be the operator. Equivalent to:

``` cpp
return basic_string_view<charT, traits>(lhs) op basic_string_view<charT, traits>(rhs);
```

#### `swap` <a id="string.special">[[string.special]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  constexpr void
    swap(basic_string<charT, traits, Allocator>& lhs,
         basic_string<charT, traits, Allocator>& rhs)
      noexcept(noexcept(lhs.swap(rhs)));
```

*Effects:* Equivalent to `lhs.swap(rhs)`.

#### Inserters and extractors <a id="string.io">[[string.io]]</a>

``` cpp
template<class charT, class traits, class Allocator>
  basic_istream<charT, traits>&
    operator>>(basic_istream<charT, traits>& is, basic_string<charT, traits, Allocator>& str);
```

*Effects:* Behaves as a formatted input
function [[istream.formatted.reqmts]]. After constructing a `sentry`
object, if the `sentry` object returns `true` when converted to a value
of type `bool`, calls `str.erase()` and then extracts characters from
`is` and appends them to `str` as if by calling `str.append(1, c)`. If
`is.width()` is greater than zero, the maximum number `n` of characters
appended is `is.width()`; otherwise `n` is `str.max_size()`. Characters
are extracted and appended until any of the following occurs:

- *n* characters are stored;
- end-of-file occurs on the input sequence;
- `isspace(c, is.getloc())` is `true` for the next available input
  character *c*.

After the last character (if any) is extracted, `is.width(0)` is called
and the `sentry` object is destroyed.

If the function extracts no characters, `ios_base::failbit` is set in
the input function’s local error state before `setstate` is called.

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
function [[istream.unformatted]], except that it does not affect the
value returned by subsequent calls to `basic_istream<>::gcount()`. After
constructing a `sentry` object, if the `sentry` object returns `true`
when converted to a value of type `bool`, calls `str.erase()` and then
extracts characters from `is` and appends them to `str` as if by calling
`str.append(1, c)` until any of the following occurs:

- end-of-file occurs on the input sequence;
- `traits::eq(c, delim)` for the next available input character *c* (in
  which case, *c* is extracted but not appended);
- `str.max_size()` characters are stored (in which case,
  `ios_base::failbit` is set in the input function’s local error state).

The conditions are tested in the order shown. In any case, after the
last character is extracted, the `sentry` object is destroyed.

If the function extracts no characters, `ios_base::failbit` is set in
the input function’s local error state before `setstate` is called.

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

#### Erasure <a id="string.erasure">[[string.erasure]]</a>

``` cpp
template<class charT, class traits, class Allocator, class U = charT>
  constexpr typename basic_string<charT, traits, Allocator>::size_type
    erase(basic_string<charT, traits, Allocator>& c, const U& value);
```

*Effects:* Equivalent to:

``` cpp
auto it = remove(c.begin(), c.end(), value);
auto r = distance(it, c.end());
c.erase(it, c.end());
return r;
```

``` cpp
template<class charT, class traits, class Allocator, class Predicate>
  constexpr typename basic_string<charT, traits, Allocator>::size_type
    erase_if(basic_string<charT, traits, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto it = remove_if(c.begin(), c.end(), pred);
auto r = distance(it, c.end());
c.erase(it, c.end());
return r;
```

### Numeric conversions <a id="string.conversions">[[string.conversions]]</a>

``` cpp
int stoi(const string& str, size_t* idx = nullptr, int base = 10);
long stol(const string& str, size_t* idx = nullptr, int base = 10);
unsigned long stoul(const string& str, size_t* idx = nullptr, int base = 10);
long long stoll(const string& str, size_t* idx = nullptr, int base = 10);
unsigned long long stoull(const string& str, size_t* idx = nullptr, int base = 10);
```

*Effects:* The first two functions call
`strtol(str.c_str(), ptr, base)`, and the last three functions call
`strtoul(str.c_str(), ptr, base)`, `strtoll(str.c_str(), ptr, base)`,
and `strtoull(str.c_str(), ptr, base)`, respectively. Each function
returns the converted result, if any. The argument `ptr` designates a
pointer to an object internal to the function that is used to determine
what to store at `*idx`. If the function does not throw an exception and
`idx != nullptr`, the function stores in `*idx` the index of the first
unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `strtol`, `strtoul`, `strtoll`, or
`strtoull` reports that no conversion can be performed. Throws
`out_of_range` if `strtol`, `strtoul`, `strtoll` or `strtoull` sets
`errno` to `ERANGE`, or if the converted value is outside the range of
representable values for the return type.

``` cpp
float stof(const string& str, size_t* idx = nullptr);
double stod(const string& str, size_t* idx = nullptr);
long double stold(const string& str, size_t* idx = nullptr);
```

*Effects:* These functions call `strtof(str.c_str(), ptr)`,
`strtod(str.c_str(), ptr)`, and `strtold(str.c_str(), ptr)`,
respectively. Each function returns the converted result, if any. The
argument `ptr` designates a pointer to an object internal to the
function that is used to determine what to store at `*idx`. If the
function does not throw an exception and `idx != nullptr`, the function
stores in `*idx` the index of the first unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `strtof`, `strtod`, or `strtold` reports
that no conversion can be performed. Throws `out_of_range` if `strtof`,
`strtod`, or `strtold` sets `errno` to `ERANGE` or if the converted
value is outside the range of representable values for the return type.

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

*Returns:* `format("{}", val)`.

``` cpp
int stoi(const wstring& str, size_t* idx = nullptr, int base = 10);
long stol(const wstring& str, size_t* idx = nullptr, int base = 10);
unsigned long stoul(const wstring& str, size_t* idx = nullptr, int base = 10);
long long stoll(const wstring& str, size_t* idx = nullptr, int base = 10);
unsigned long long stoull(const wstring& str, size_t* idx = nullptr, int base = 10);
```

*Effects:* The first two functions call
`wcstol(str.c_str(), ptr, base)`, and the last three functions call
`wcstoul(str.c_str(), ptr, base)`, `wcstoll(str.c_str(), ptr, base)`,
and `wcstoull(str.c_str(), ptr, base)`, respectively. Each function
returns the converted result, if any. The argument `ptr` designates a
pointer to an object internal to the function that is used to determine
what to store at `*idx`. If the function does not throw an exception and
`idx != nullptr`, the function stores in `*idx` the index of the first
unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `wcstol`, `wcstoul`, `wcstoll`, or
`wcstoull` reports that no conversion can be performed. Throws
`out_of_range` if the converted value is outside the range of
representable values for the return type.

``` cpp
float stof(const wstring& str, size_t* idx = nullptr);
double stod(const wstring& str, size_t* idx = nullptr);
long double stold(const wstring& str, size_t* idx = nullptr);
```

*Effects:* These functions call `wcstof(str.c_str(), ptr)`,
`wcstod(str.c_str(), ptr)`, and `wcstold(str.c_str(), ptr)`,
respectively. Each function returns the converted result, if any. The
argument `ptr` designates a pointer to an object internal to the
function that is used to determine what to store at `*idx`. If the
function does not throw an exception and `idx != nullptr`, the function
stores in `*idx` the index of the first unconverted element of `str`.

*Returns:* The converted result.

*Throws:* `invalid_argument` if `wcstof`, `wcstod`, or `wcstold` reports
that no conversion can be performed. Throws `out_of_range` if `wcstof`,
`wcstod`, or `wcstold` sets `errno` to `ERANGE`.

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

*Returns:* `format(L"{}", val)`.

### Hash support <a id="basic.string.hash">[[basic.string.hash]]</a>

``` cpp
template<class A> struct hash<basic_string<char, char_traits<char>, A>>;
template<class A> struct hash<basic_string<char8_t, char_traits<char8_t>, A>>;
template<class A> struct hash<basic_string<char16_t, char_traits<char16_t>, A>>;
template<class A> struct hash<basic_string<char32_t, char_traits<char32_t>, A>>;
template<class A> struct hash<basic_string<wchar_t, char_traits<wchar_t>, A>>;
```

If `S` is one of these string types, `SV` is the corresponding string
view type, and `s` is an object of type `S`, then
`hash<S>()(s) == hash<SV>()(SV(s))`.

### Suffix for `basic_string` literals <a id="basic.string.literals">[[basic.string.literals]]</a>

``` cpp
constexpr string operator""s(const char* str, size_t len);
```

*Returns:* `string{str, len}`.

``` cpp
constexpr u8string operator""s(const char8_t* str, size_t len);
```

*Returns:* `u8string{str, len}`.

``` cpp
constexpr u16string operator""s(const char16_t* str, size_t len);
```

*Returns:* `u16string{str, len}`.

``` cpp
constexpr u32string operator""s(const char32_t* str, size_t len);
```

*Returns:* `u32string{str, len}`.

``` cpp
constexpr wstring operator""s(const wchar_t* str, size_t len);
```

*Returns:* `wstring{str, len}`.

[*Note 1*: The same suffix `s` is used for `chrono::duration` literals
denoting seconds but there is no conflict, since duration suffixes apply
to numbers and string literal suffixes apply to character array
literals. — *end note*]

## Null-terminated sequence utilities <a id="c.strings">[[c.strings]]</a>

### Header `<cstring>` synopsis <a id="cstring.syn">[[cstring.syn]]</a>

``` cpp
#define __STDC_VERSION_STRING_H__ 202311L

namespace std {
  using size_t = see [support.types.layout];                                            // freestanding

  void* memcpy(void* s1, const void* s2, size_t n);                     // freestanding
  void* memccpy(void* s1, const void* s2, int c, size_t n);             // freestanding
  void* memmove(void* s1, const void* s2, size_t n);                    // freestanding
  char* strcpy(char* s1, const char* s2);                               // freestanding
  char* strncpy(char* s1, const char* s2, size_t n);                    // freestanding
  char* strdup(const char* s);
  char* strndup(const char* s, size_t size);
  char* strcat(char* s1, const char* s2);                               // freestanding
  char* strncat(char* s1, const char* s2, size_t n);                    // freestanding
  int memcmp(const void* s1, const void* s2, size_t n);                 // freestanding
  int strcmp(const char* s1, const char* s2);                           // freestanding
  int strcoll(const char* s1, const char* s2);
  int strncmp(const char* s1, const char* s2, size_t n);                // freestanding
  size_t strxfrm(char* s1, const char* s2, size_t n);
  const void* memchr(const void* s, int c, size_t n);                   // freestanding; see [library.c]
  void* memchr(void* s, int c, size_t n);                               // freestanding; see [library.c]
  const char* strchr(const char* s, int c);                             // freestanding; see [library.c]
  char* strchr(char* s, int c);                                         // freestanding; see [library.c]
  size_t strcspn(const char* s1, const char* s2);                       // freestanding
  const char* strpbrk(const char* s1, const char* s2);                  // freestanding; see [library.c]
  char* strpbrk(char* s1, const char* s2);                              // freestanding; see [library.c]
  const char* strrchr(const char* s, int c);                            // freestanding; see [library.c]
  char* strrchr(char* s, int c);                                        // freestanding; see [library.c]
  size_t strspn(const char* s1, const char* s2);                        // freestanding
  const char* strstr(const char* s1, const char* s2);                   // freestanding; see [library.c]
  char* strstr(char* s1, const char* s2);                               // freestanding; see [library.c]
  char* strtok(char* s1, const char* s2);
  void* memset(void* s, int c, size_t n);                               // freestanding
  void* memset_explicit(void* s, int c, size_t n);                      // freestanding
  char* strerror(int errnum);
  size_t strlen(const char* s);                                         // freestanding
}

#define NULL see [support.types.nullptr]                                                // freestanding
```

The contents and meaning of the header `<cstring>` are the same as the C
standard library header `<string.h>`.

The functions `strerror` and `strtok` are not required to avoid data
races [[res.on.data.races]].

The functions `memcpy` and `memmove` are signal-safe [[support.signal]].
Each of these functions implicitly creates objects [[intro.object]] in
the destination region of storage immediately prior to copying the
sequence of characters to the destination. Each of these functions
returns a pointer to a suitable created object, if any, otherwise the
value of the first parameter.

[*Note 1*: The functions `strchr`, `strpbrk`, `strrchr`, `strstr`, and
`memchr`, have different signatures in this document, but they have the
same behavior as in the C standard library [[library.c]]. — *end note*]

See also: ISO C 7.26

<!-- Link reference definitions -->
[basic.indet]: basic.md#basic.indet
[basic.string]: #basic.string
[basic.string.general]: #basic.string.general
[basic.string.hash]: #basic.string.hash
[basic.string.literals]: #basic.string.literals
[c.strings]: #c.strings
[char.traits]: #char.traits
[char.traits.general]: #char.traits.general
[char.traits.req]: #char.traits.req
[char.traits.require]: #char.traits.require
[char.traits.specializations]: #char.traits.specializations
[char.traits.specializations.char]: #char.traits.specializations.char
[char.traits.specializations.char16.t]: #char.traits.specializations.char16.t
[char.traits.specializations.char32.t]: #char.traits.specializations.char32.t
[char.traits.specializations.char8.t]: #char.traits.specializations.char8.t
[char.traits.specializations.general]: #char.traits.specializations.general
[char.traits.specializations.wchar.t]: #char.traits.specializations.wchar.t
[char.traits.typedefs]: #char.traits.typedefs
[cmp.categories]: support.md#cmp.categories
[container.alloc.reqmts]: containers.md#container.alloc.reqmts
[container.reqmts]: containers.md#container.reqmts
[container.requirements]: containers.md#container.requirements
[container.requirements.pre]: containers.md#container.requirements.pre
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[cstring.syn]: #cstring.syn
[defns.character.container]: intro.md#defns.character.container
[input.output]: input.md#input.output
[intro.object]: basic.md#intro.object
[iostream.forward]: input.md#iostream.forward
[iostreams.limits.pos]: input.md#iostreams.limits.pos
[istream.formatted.reqmts]: input.md#istream.formatted.reqmts
[istream.unformatted]: input.md#istream.unformatted
[iterator.concept.contiguous]: iterators.md#iterator.concept.contiguous
[iterator.concept.winc]: iterators.md#iterator.concept.winc
[iterator.range]: iterators.md#iterator.range
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[library.c]: library.md#library.c
[ostream.formatted.reqmts]: input.md#ostream.formatted.reqmts
[over.match.oper]: over.md#over.match.oper
[random.access.iterators]: iterators.md#random.access.iterators
[res.on.data.races]: library.md#res.on.data.races
[sequence.reqmts]: containers.md#sequence.reqmts
[string.access]: #string.access
[string.accessors]: #string.accessors
[string.append]: #string.append
[string.assign]: #string.assign
[string.capacity]: #string.capacity
[string.classes]: #string.classes
[string.classes.general]: #string.classes.general
[string.cmp]: #string.cmp
[string.compare]: #string.compare
[string.cons]: #string.cons
[string.contains]: #string.contains
[string.conversions]: #string.conversions
[string.copy]: #string.copy
[string.ends.with]: #string.ends.with
[string.erase]: #string.erase
[string.erasure]: #string.erasure
[string.find]: #string.find
[string.insert]: #string.insert
[string.io]: #string.io
[string.iterators]: #string.iterators
[string.modifiers]: #string.modifiers
[string.nonmembers]: #string.nonmembers
[string.op.append]: #string.op.append
[string.op.plus]: #string.op.plus
[string.ops]: #string.ops
[string.replace]: #string.replace
[string.require]: #string.require
[string.special]: #string.special
[string.starts.with]: #string.starts.with
[string.substr]: #string.substr
[string.swap]: #string.swap
[string.syn]: #string.syn
[string.view]: #string.view
[string.view.access]: #string.view.access
[string.view.capacity]: #string.view.capacity
[string.view.compare]: #string.view.compare
[string.view.comparison]: #string.view.comparison
[string.view.cons]: #string.view.cons
[string.view.deduct]: #string.view.deduct
[string.view.find]: #string.view.find
[string.view.general]: #string.view.general
[string.view.hash]: #string.view.hash
[string.view.io]: #string.view.io
[string.view.iterators]: #string.view.iterators
[string.view.literals]: #string.view.literals
[string.view.modifiers]: #string.view.modifiers
[string.view.ops]: #string.view.ops
[string.view.synop]: #string.view.synop
[string.view.template]: #string.view.template
[string.view.template.general]: #string.view.template.general
[strings]: #strings
[strings.general]: #strings.general
[strings.summary]: #strings.summary
[support.signal]: support.md#support.signal
[temp.deduct]: temp.md#temp.deduct
[term.standard.layout.type]: basic.md#term.standard.layout.type
[term.trivially.copyable.type]: basic.md#term.trivially.copyable.type
[unord.hash]: utilities.md#unord.hash
[utility.swap]: utilities.md#utility.swap

[^1]: If `eof()` can be held in `char_type` then some iostreams
    operations can give surprising results.

[^2]: Because `basic_string_view` refers to a constant sequence,
    `iterator` and `const_iterator` are the same type.

[^3]: For example, as an argument to non-member functions `swap()`
    [[string.special]], `operator>{}>()` [[string.io]], and `getline()`
    [[string.io]], or as an argument to `basic_string::swap()`.
