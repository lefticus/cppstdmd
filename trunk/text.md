# Text processing library <a id="text">[[text]]</a>

## General <a id="text.general">[[text.general]]</a>

This Clause describes components for dealing with text. These components
are summarized in [[text.summary]].

**Table: Text library summary**

| Subclause          |                                    | Header                                                       |
| ------------------ | ---------------------------------- | ------------------------------------------------------------ |
| [[charconv]]       | Primitive numeric conversions      | `<charconv>`                                                 |
| [[localization]]   | Localization library               | `<locale>`, `<clocale>`                                      |
| [[format]]         | Formatting                         | `<format>`                                                   |
| [[text.encoding]]  | Text encodings identification      | `<text_encoding>`                                            |
| [[re]]             | Regular expressions library        | `<regex>`                                                    |
| [[text.c.strings]] | Null-terminated sequence utilities | `<cctype>`, `<cstdlib>`, `<cuchar>`, `<cwchar>`, `<cwctype>` |


## Primitive numeric conversions <a id="charconv">[[charconv]]</a>

### Header `<charconv>` synopsis <a id="charconv.syn">[[charconv.syn]]</a>

When a function is specified with a type placeholder of `integer-type`,
the implementation provides overloads for `char` and all cv-unqualified
signed and unsigned integer types in lieu of `integer-type`. When a
function is specified with a type placeholder of `floating-point-type`,
the implementation provides overloads for all cv-unqualified
floating-point types [[basic.fundamental]] in lieu of
`floating-point-type`.

``` cpp
namespace std {
  // floating-point format for primitive numerical conversion
  enum class chars_format {
    scientific = unspecified,
    fixed = unspecified,
    hex = unspecified,
    general = fixed | scientific
  };

  // [charconv.to.chars], primitive numerical output conversion
  struct to_chars_result {                                              // freestanding
    char* ptr;
    errc ec;
    friend bool operator==(const to_chars_result&, const to_chars_result&) = default;
    constexpr explicit operator bool() const noexcept { return ec == errc{}; }
  };

  constexpr to_chars_result to_chars(char* first, char* last,           // freestanding
                                     integer-type value, int base = 10);
  to_chars_result to_chars(char* first, char* last,                     // freestanding
                           bool value, int base = 10) = delete;

  to_chars_result to_chars(char* first, char* last,                     // freestanding-deleted
                           floating-point-type value);
  to_chars_result to_chars(char* first, char* last,                     // freestanding-deleted
                           floating-point-type value, chars_format fmt);
  to_chars_result to_chars(char* first, char* last,                     // freestanding-deleted
                           floating-point-type value, chars_format fmt, int precision);

  // [charconv.from.chars], primitive numerical input conversion
  struct from_chars_result {                                            // freestanding
    const char* ptr;
    errc ec;
    friend bool operator==(const from_chars_result&, const from_chars_result&) = default;
    constexpr explicit operator bool() const noexcept { return ec == errc{}; }
  };

  constexpr from_chars_result from_chars(const char* first, const char* last,   // freestanding
                                         integer-type& value, int base = 10);

  from_chars_result from_chars(const char* first, const char* last,     // freestanding-deleted
                               floating-point-type& value,
                               chars_format fmt = chars_format::general);
}
```

The type `chars_format` is a bitmask type [[bitmask.types]] with
elements `scientific`, `fixed`, and `hex`.

The types `to_chars_result` and `from_chars_result` have the data
members and special members specified above. They have no base classes
or members other than those specified.

### Primitive numeric output conversion <a id="charconv.to.chars">[[charconv.to.chars]]</a>

All functions named `to_chars` convert `value` into a character string
by successively filling the range \[`first`, `last`), where \[`first`,
`last`) is required to be a valid range. If the member `ec` of the
return value is such that the value is equal to the value of a
value-initialized `errc`, the conversion was successful and the member
`ptr` is the one-past-the-end pointer of the characters written.
Otherwise, the member `ec` has the value `errc::value_too_large`, the
member `ptr` has the value `last`, and the contents of the range
\[`first`, `last`) are unspecified.

The functions that take a floating-point `value` but not a `precision`
parameter ensure that the string representation consists of the smallest
number of characters such that there is at least one digit before the
radix point (if present) and parsing the representation using the
corresponding `from_chars` function recovers `value` exactly.

[*Note 1*: This guarantee applies only if `to_chars` and `from_chars`
are executed on the same implementation. — *end note*]

If there are several such representations, the representation with the
smallest difference from the floating-point argument value is chosen,
resolving any remaining ties using rounding according to
`round_to_nearest` [[round.style]].

The functions taking a `chars_format` parameter determine the conversion
specifier for `printf` as follows: The conversion specifier is `f` if
`fmt` is `chars_format::fixed`, `e` if `fmt` is
`chars_format::scientific`, `a` (without leading `"0x"` in the result)
if `fmt` is `chars_format::hex`, and `g` if `fmt` is
`chars_format::general`.

``` cpp
constexpr to_chars_result to_chars(char* first, char* last, integer-type value, int base = 10);
```

*Preconditions:* `base` has a value between 2 and 36 (inclusive).

*Effects:* The value of `value` is converted to a string of digits in
the given base (with no redundant leading zeroes). Digits in the range
10..35 (inclusive) are represented as lowercase characters `a`..`z`. If
`value` is less than zero, the representation starts with `’-’`.

*Throws:* Nothing.

``` cpp
to_chars_result to_chars(char* first, char* last, floating-point-type value);
```

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale. The conversion specifier is `f` or `e`, chosen
according to the requirement for a shortest representation (see above);
a tie is resolved in favor of `f`.

*Throws:* Nothing.

``` cpp
to_chars_result to_chars(char* first, char* last, floating-point-type value, chars_format fmt);
```

*Preconditions:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale.

*Throws:* Nothing.

``` cpp
to_chars_result to_chars(char* first, char* last, floating-point-type value,
                         chars_format fmt, int precision);
```

*Preconditions:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale with the given precision.

*Throws:* Nothing.

### Primitive numeric input conversion <a id="charconv.from.chars">[[charconv.from.chars]]</a>

All functions named `from_chars` analyze the string \[`first`, `last`)
for a pattern, where \[`first`, `last`) is required to be a valid range.
If no characters match the pattern, `value` is unmodified, the member
`ptr` of the return value is `first` and the member `ec` is equal to
`errc::invalid_argument`.

[*Note 1*: If the pattern allows for an optional sign, but the string
has no digit characters following the sign, no characters match the
pattern. — *end note*]

Otherwise, the characters matching the pattern are interpreted as a
representation of a value of the type of `value`. The member `ptr` of
the return value points to the first character not matching the pattern,
or has the value `last` if all characters match. If the parsed value is
not in the range representable by the type of `value`, `value` is
unmodified and the member `ec` of the return value is equal to
`errc::result_out_of_range`. Otherwise, `value` is set to the parsed
value, after rounding according to `round_to_nearest` [[round.style]],
and the member `ec` is value-initialized.

``` cpp
constexpr from_chars_result from_chars(const char* first, const char* last,
                                       integer-type&\itcorr[-1] value, int base = 10);
```

*Preconditions:* `base` has a value between 2 and 36 (inclusive).

*Effects:* The pattern is the expected form of the subject sequence in
the `"C"` locale for the given nonzero base, as described for `strtol`,
except that no `"0x"` or `"0X"` prefix shall appear if the value of
`base` is 16, and except that `’-’` is the only sign that may appear,
and only if `value` has a signed type.

*Throws:* Nothing.

``` cpp
from_chars_result from_chars(const char* first, const char* last, floating-point-type& value,
                             chars_format fmt = chars_format::general);
```

*Preconditions:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* The pattern is the expected form of the subject sequence in
the `"C"` locale, as described for `strtod`, except that

- the sign `’+’` may only appear in the exponent part;
- if `fmt` has `chars_format::scientific` set but not
  `chars_format::fixed`, the otherwise optional exponent part shall
  appear;
- if `fmt` has `chars_format::fixed` set but not
  `chars_format::scientific`, the optional exponent part shall not
  appear; and
- if `fmt` is `chars_format::hex`, the prefix `"0x"` or `"0X"` is
  assumed. \[*Example 1*: The string `0x123` is parsed to have the value
  `0` with remaining characters `x123`. — *end example*]

In any case, the resulting `value` is one of at most two floating-point
values closest to the value of the string matching the pattern.

*Throws:* Nothing.

## Localization library <a id="localization">[[localization]]</a>

### General <a id="localization.general">[[localization.general]]</a>

Subclause [[localization]] describes components that C++ programs may
use to encapsulate (and therefore be more portable when confronting)
cultural differences. The locale facility includes internationalization
support for character classification and string collation, numeric,
monetary, and date/time formatting and parsing, and message retrieval.

The following subclauses describe components for locales themselves, the
standard facets, and facilities from the C library, as summarized in
[[localization.summary]].

**Table: Localization library summary**

| Subclause             |                              | Header      |
| --------------------- | ---------------------------- | ----------- |
| [[locales]]           | Locales                      | `<locale>`  |
| [[locale.categories]] | Standard `locale` categories |             |
| [[c.locales]]         | C library locales            | `<clocale>` |


### Header `<locale>` synopsis <a id="locale.syn">[[locale.syn]]</a>

``` cpp
namespace std {
  // [locale], locale
  class locale;
  template<class Facet> const Facet& use_facet(const locale&);
  template<class Facet> bool         has_facet(const locale&) noexcept;

  // [locale.convenience], convenience interfaces
  template<class charT> bool isspace (charT c, const locale& loc);
  template<class charT> bool isprint (charT c, const locale& loc);
  template<class charT> bool iscntrl (charT c, const locale& loc);
  template<class charT> bool isupper (charT c, const locale& loc);
  template<class charT> bool islower (charT c, const locale& loc);
  template<class charT> bool isalpha (charT c, const locale& loc);
  template<class charT> bool isdigit (charT c, const locale& loc);
  template<class charT> bool ispunct (charT c, const locale& loc);
  template<class charT> bool isxdigit(charT c, const locale& loc);
  template<class charT> bool isalnum (charT c, const locale& loc);
  template<class charT> bool isgraph (charT c, const locale& loc);
  template<class charT> bool isblank (charT c, const locale& loc);
  template<class charT> charT toupper(charT c, const locale& loc);
  template<class charT> charT tolower(charT c, const locale& loc);

  // [category.ctype], ctype
  class ctype_base;
  template<class charT> class ctype;
  template<>            class ctype<char>;      // specialization
  template<class charT> class ctype_byname;
  class codecvt_base;
  template<class internT, class externT, class stateT> class codecvt;
  template<class internT, class externT, class stateT> class codecvt_byname;

  // [category.numeric], numeric
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class num_get;
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class num_put;
  template<class charT>
    class numpunct;
  template<class charT>
    class numpunct_byname;

  // [category.collate], collation
  template<class charT> class collate;
  template<class charT> class collate_byname;

  // [category.time], date and time
  class time_base;
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class time_get;
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class time_get_byname;
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class time_put;
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class time_put_byname;

  // [category.monetary], money
  class money_base;
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class money_get;
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class money_put;
  template<class charT, bool Intl = false>
    class moneypunct;
  template<class charT, bool Intl = false>
    class moneypunct_byname;

  // [category.messages], message retrieval
  class messages_base;
  template<class charT> class messages;
  template<class charT> class messages_byname;
}
```

The header `<locale>` defines classes and declares functions that
encapsulate and manipulate the information peculiar to a locale.[^1]

### Locales <a id="locales">[[locales]]</a>

#### Class `locale` <a id="locale">[[locale]]</a>

##### General <a id="locale.general">[[locale.general]]</a>

``` cpp
namespace std {
  class locale {
  public:
    // [locale.types], types
    // [locale.facet], class locale::facet
    class facet;
    // [locale.id], class locale::id
    class id;
    // [locale.category], type locale::category
    using category = int;
    static const category   // values assigned here are for exposition only
      none     = 0,
      collate  = 0x010, ctype    = 0x020,
      monetary = 0x040, numeric  = 0x080,
      time     = 0x100, messages = 0x200,
      all = collate | ctype | monetary | numeric | time | messages;

    // [locale.cons], construct/copy/destroy
    locale() noexcept;
    locale(const locale& other) noexcept;
    explicit locale(const char* std_name);
    explicit locale(const string& std_name);
    locale(const locale& other, const char* std_name, category);
    locale(const locale& other, const string& std_name, category);
    template<class Facet> locale(const locale& other, Facet* f);
    locale(const locale& other, const locale& one, category);
    ~locale();                  // not virtual
    const locale& operator=(const locale& other) noexcept;

    // [locale.members], locale operations
    template<class Facet> locale combine(const locale& other) const;
    string name() const;
    text_encoding encoding() const;

    bool operator==(const locale& other) const;

    template<class charT, class traits, class Allocator>
      bool operator()(const basic_string<charT, traits, Allocator>& s1,
                      const basic_string<charT, traits, Allocator>& s2) const;

    // [locale.statics], global locale objects
    static       locale  global(const locale&);
    static const locale& classic();
  };
}
```

Class `locale` implements a type-safe polymorphic set of facets, indexed
by facet *type*. In other words, a facet has a dual role: in one sense,
it’s just a class interface; at the same time, it’s an index into a
locale’s set of facets.

Access to the facets of a `locale` is via two function templates,
`use_facet<>` and `has_facet<>`.

[*Example 1*:

An iostream `operator<<` can be implemented as:

[^2]

``` cpp
template<class charT, class traits>
basic_ostream<charT, traits>&
operator<< (basic_ostream<charT, traits>& s, Date d) {
  typename basic_ostream<charT, traits>::sentry cerberos(s);
  if (cerberos) {
    tm tmbuf; d.extract(tmbuf);
    bool failed =
      use_facet<time_put<charT, ostreambuf_iterator<charT, traits>>>(
        s.getloc()).put(s, s, s.fill(), &tmbuf, 'x').failed();
    if (failed)
      s.setstate(s.badbit);     // can throw
  }
  return s;
}
```

— *end example*]

In the call to `use_facet<Facet>(loc)`, the type argument chooses a
facet, making available all members of the named type. If `Facet` is not
present in a locale, it throws the standard exception `bad_cast`. A C++
program can check if a locale implements a particular facet with the
function template `has_facet<Facet>()`. User-defined facets may be
installed in a locale, and used identically as may standard facets.

[*Note 1*:

All locale semantics are accessed via `use_facet<>` and `has_facet<>`,
except that:

- A member operator template
  ``` cpp
  operator()(const basic_string<C, T, A>&, const basic_string<C, T, A>&)
  ```

  is provided so that a locale can be used as a predicate argument to
  the standard collections, to collate strings.
- Convenient global interfaces are provided for traditional `ctype`
  functions such as `isdigit()` and `isspace()`, so that given a locale
  object `loc` a C++ program can call `isspace(c, loc)`. (This eases
  upgrading existing extractors [[istream.formatted]].)

— *end note*]

Once a facet reference is obtained from a locale object by calling
`use_facet<>`, that reference remains usable, and the results from
member functions of it may be cached and re-used, as long as some locale
object refers to that facet.

In successive calls to a locale facet member function on a facet object
installed in the same locale, the returned result shall be identical.

A `locale` constructed from a name string (such as `"POSIX"`), or from
parts of two named locales, has a name; all others do not. Named locales
may be compared for equality; an unnamed locale is equal only to (copies
of) itself. For an unnamed locale, `locale::name()` returns the string
`"*"`.

Whether there is one global locale object for the entire program or one
global locale object per thread is *implementation-defined*.
Implementations should provide one global locale object per thread. If
there is a single global locale object for the entire program,
implementations are not required to avoid data races on it
[[res.on.data.races]].

##### Types <a id="locale.types">[[locale.types]]</a>

###### Type `locale::category` <a id="locale.category">[[locale.category]]</a>

``` cpp
using category = int;
```

*Valid* `category` values include the `locale` member bitmask elements
`collate`, `ctype`, `monetary`, `numeric`, `time`, and `messages`, each
of which represents a single locale category. In addition, `locale`
member bitmask constant `none` is defined as zero and represents no
category. And `locale` member bitmask constant `all` is defined such
that the expression

``` cpp
(collate | ctype | monetary | numeric | time | messages | all) == all
```

is `true`, and represents the union of all categories. Further, the
expression `(X | Y)`, where `X` and `Y` each represent a single
category, represents the union of the two categories.

`locale` member functions expecting a `category` argument require one of
the `category` values defined above, or the union of two or more such
values. Such a `category` value identifies a set of locale categories.
Each locale category, in turn, identifies a set of locale facets,
including at least those shown in [[locale.category.facets]].

**Table: Locale category facets**

| Category | Includes facets                                       |
| -------- | ----------------------------------------------------- |
| collate  | `collate<char>`, `collate<wchar_t>`                   |
| ctype    | `ctype<char>`, `ctype<wchar_t>`                       |
|          | `codecvt<char, char, mbstate_t>`                      |
|          | `codecvt<wchar_t, char, mbstate_t>`                   |
| monetary | `moneypunct<char>`, `moneypunct<wchar_t>`             |
|          | `moneypunct<char, true>`, `moneypunct<wchar_t, true>` |
|          | `money_get<char>`, `money_get<wchar_t>`               |
|          | `money_put<char>`, `money_put<wchar_t>`               |
| numeric  | `numpunct<char>`, `numpunct<wchar_t>`                 |
|          | `num_get<char>`, `num_get<wchar_t>`                   |
|          | `num_put<char>`, `num_put<wchar_t>`                   |
| time     | `time_get<char>`, `time_get<wchar_t>`                 |
|          | `time_put<char>`, `time_put<wchar_t>`                 |
| messages | `messages<char>`, `messages<wchar_t>`                 |


For any locale `loc` either constructed, or returned by
`locale::classic()`, and any facet `Facet` shown in
[[locale.category.facets]], `has_facet<Facet>(loc)` is `true`. Each
`locale` member function which takes a `locale::category` argument
operates on the corresponding set of facets.

An implementation is required to provide those specializations for facet
templates identified as members of a category, and for those shown in
[[locale.spec]].

**Table: Required specializations**

| Category | Includes facets                                           |
| -------- | --------------------------------------------------------- |
| collate  | `collate_byname<char>`, `collate_byname<wchar_t>`         |
| ctype    | `ctype_byname<char>`, `ctype_byname<wchar_t>`             |
|          | `codecvt_byname<char, char, mbstate_t>`                   |
|          | `codecvt_byname<wchar_t, char, mbstate_t>`                |
| monetary | `moneypunct_byname<char, International>`                  |
|          | `moneypunct_byname<wchar_t, International>`               |
|          | `money_get<C, InputIterator>`                             |
|          | `money_put<C, OutputIterator>`                            |
| numeric  | `numpunct_byname<char>`, `numpunct_byname<wchar_t>`       |
|          | `num_get<C, InputIterator>`, `num_put<C, OutputIterator>` |
| time     | `time_get<char, InputIterator>`                           |
|          | `time_get_byname<char, InputIterator>`                    |
|          | `time_get<wchar_t, InputIterator>`                        |
|          | `time_get_byname<wchar_t, InputIterator>`                 |
|          | `time_put<char, OutputIterator>`                          |
|          | `time_put_byname<char, OutputIterator>`                   |
|          | `time_put<wchar_t, OutputIterator>`                       |
|          | `time_put_byname<wchar_t, OutputIterator>`                |
| messages | `messages_byname<char>`, `messages_byname<wchar_t>`       |


The provided implementation of members of facets `num_get<charT>` and
`num_put<charT>` calls `use_facet<F>(l)` only for facet `F` of types
`numpunct<charT>` and `ctype<charT>`, and for locale `l` the value
obtained by calling member `getloc()` on the `ios_base&` argument to
these functions.

In declarations of facets, a template parameter with name
`InputIterator` or `OutputIterator` indicates the set of all possible
specializations on parameters that meet the *Cpp17InputIterator*
requirements or *Cpp17OutputIterator* requirements, respectively
[[iterator.requirements]]. A template parameter with name `C` represents
the set of types containing `char`, `wchar_t`, and any other
*implementation-defined* character container types
[[defns.character.container]] that meet the requirements for a character
on which any of the iostream components can be instantiated. A template
parameter with name `International` represents the set of all possible
specializations on a bool parameter.

###### Class `locale::facet` <a id="locale.facet">[[locale.facet]]</a>

``` cpp
namespace std {
  class locale::facet {
  protected:
    explicit facet(size_t refs = 0);
    virtual ~facet();
    facet(const facet&) = delete;
    void operator=(const facet&) = delete;
  };
}
```

Class `facet` is the base class for locale feature sets. A class is a
*facet* if it is publicly derived from another facet, or if it is a
class derived from `locale::facet` and contains a publicly accessible
declaration as follows:[^3]

``` cpp
static ::std::locale::id id;
```

Template parameters in this Clause which are required to be facets are
those named `Facet` in declarations. A program that passes a type that
is *not* a facet, or a type that refers to a volatile-qualified facet,
as an (explicit or deduced) template parameter to a locale function
expecting a facet, is ill-formed. A const-qualified facet is a valid
template argument to any locale function that expects a `Facet` template
parameter.

The `refs` argument to the constructor is used for lifetime management.
For `refs == 0`, the implementation performs
`delete static_cast<locale::facet*>(f)` (where `f` is a pointer to the
facet) when the last `locale` object containing the facet is destroyed;
for `refs == 1`, the implementation never destroys the facet.

Constructors of all facets defined in this Clause take such an argument
and pass it along to their `facet` base class constructor. All
one-argument constructors defined in this Clause are explicit,
preventing their participation in implicit conversions.

For some standard facets a standard “…`_byname`” class, derived from it,
implements the virtual function semantics equivalent to that facet of
the locale constructed by `locale(const char*)` with the same name. Each
such facet provides a constructor that takes a `const char*` argument,
which names the locale, and a `refs` argument, which is passed to the
base class constructor. Each such facet also provides a constructor that
takes a `string` argument `str` and a `refs` argument, which has the
same effect as calling the first constructor with the two arguments
`str.c_str()` and `refs`. If there is no “…`_byname`” version of a
facet, the base class implements named locale semantics itself by
reference to other facets.

###### Class `locale::id` <a id="locale.id">[[locale.id]]</a>

``` cpp
namespace std {
  class locale::id {
  public:
    id();
    void operator=(const id&) = delete;
    id(const id&) = delete;
  };
}
```

The class `locale::id` provides identification of a locale facet
interface, used as an index for lookup and to encapsulate
initialization.

[*Note 2*: Because facets are used by iostreams, potentially while
static constructors are running, their initialization cannot depend on
programmed static initialization. One initialization strategy is for
`locale` to initialize each facet’s `id` member the first time an
instance of the facet is installed into a locale. This depends only on
static storage being zero before constructors run
[[basic.start.static]]. — *end note*]

##### Constructors and destructor <a id="locale.cons">[[locale.cons]]</a>

``` cpp
locale() noexcept;
```

*Effects:* Constructs a copy of the argument last passed to
`locale::global(locale&)`, if it has been called; else, the resulting
facets have virtual function semantics identical to those of
`locale::classic()`.

[*Note 1*: This constructor yields a copy of the current global locale.
It is commonly used as a default argument for function parameters of
type `const locale&`. — *end note*]

``` cpp
explicit locale(const char* std_name);
```

*Effects:* Constructs a locale using standard C locale names, e.g.,
`"POSIX"`. The resulting locale implements semantics defined to be
associated with that name.

*Throws:* `runtime_error` if the argument is not valid, or is null.

*Remarks:* The set of valid string argument values is `"C"`, `""`, and
any *implementation-defined* values.

``` cpp
explicit locale(const string& std_name);
```

*Effects:* Equivalent to `locale(std_name.c_str())`.

``` cpp
locale(const locale& other, const char* std_name, category cats);
```

*Preconditions:* `cats` is a valid `category` value [[locale.category]].

*Effects:* Constructs a locale as a copy of `other` except for the
facets identified by the `category` argument, which instead implement
the same semantics as `locale(std_name)`.

*Throws:* `runtime_error` if the second argument is not valid, or is
null.

*Remarks:* The locale has a name if and only if `other` has a name.

``` cpp
locale(const locale& other, const string& std_name, category cats);
```

*Effects:* Equivalent to `locale(other, std_name.c_str(), cats)`.

``` cpp
template<class Facet> locale(const locale& other, Facet* f);
```

*Effects:* Constructs a locale incorporating all facets from the first
argument except that of type `Facet`, and installs the second argument
as the remaining facet. If `f` is null, the resulting object is a copy
of `other`.

*Remarks:* If `f` is null, the resulting locale has the same name as
`other`. Otherwise, the resulting locale has no name.

``` cpp
locale(const locale& other, const locale& one, category cats);
```

*Preconditions:* `cats` is a valid `category` value.

*Effects:* Constructs a locale incorporating all facets from the first
argument except those that implement `cats`, which are instead
incorporated from the second argument.

*Remarks:* If `cats` is equal to `locale::none`, the resulting locale
has a name if and only if the first argument has a name. Otherwise, the
resulting locale has a name if and only if the first two arguments both
have names.

``` cpp
const locale& operator=(const locale& other) noexcept;
```

*Effects:* Creates a copy of `other`, replacing the current value.

*Returns:* `*this`.

##### Members <a id="locale.members">[[locale.members]]</a>

``` cpp
template<class Facet> locale combine(const locale& other) const;
```

*Effects:* Constructs a locale incorporating all facets from `*this`
except for that one facet of `other` that is identified by `Facet`.

*Returns:* The newly created locale.

*Throws:* `runtime_error` if `has_facet<Facet>(other)` is `false`.

*Remarks:* The resulting locale has no name.

``` cpp
string name() const;
```

*Returns:* The name of `*this`, if it has one; otherwise, the string
`"*"`.

``` cpp
text_encoding encoding() const;
```

*Mandates:* `CHAR_BIT == 8` is `true`.

*Returns:* A `text_encoding` object representing the
implementation-defined encoding scheme associated with the locale
`*this`.

##### Operators <a id="locale.operators">[[locale.operators]]</a>

``` cpp
bool operator==(const locale& other) const;
```

*Returns:* `true` if both arguments are the same locale, or one is a
copy of the other, or each has a name and the names are identical;
`false` otherwise.

``` cpp
template<class charT, class traits, class Allocator>
  bool operator()(const basic_string<charT, traits, Allocator>& s1,
                  const basic_string<charT, traits, Allocator>& s2) const;
```

*Effects:* Compares two strings according to the `std::collate<charT>`
facet.

*Returns:*

``` cpp
use_facet<std::collate<charT>>(*this).compare(s1.data(), s1.data() + s1.size(),
                                              s2.data(), s2.data() + s2.size()) < 0
```

*Remarks:* This member operator template (and therefore `locale` itself)
meets the requirements for a comparator predicate template
argument [[algorithms]] applied to strings.

[*Example 1*:

A vector of strings `v` can be collated according to collation rules in
locale `loc` simply by [[alg.sort,vector]]:

``` cpp
std::sort(v.begin(), v.end(), loc);
```

— *end example*]

##### Static members <a id="locale.statics">[[locale.statics]]</a>

``` cpp
static locale global(const locale& loc);
```

*Effects:* Sets the global locale to its argument. Causes future calls
to the constructor `locale()` to return a copy of the argument. If the
argument has a name, does

``` cpp
setlocale(LC_ALL, loc.name().c_str());
```

otherwise, the effect on the C locale, if any, is
*implementation-defined*.

*Returns:* The previous value of `locale()`.

*Remarks:* No library function other than `locale::global()` affects the
value returned by `locale()`.

[*Note 2*: See  [[c.locales]] for data race considerations when
`setlocale` is invoked. — *end note*]

``` cpp
static const locale& classic();
```

The `"C"` locale.

*Returns:* A locale that implements the classic `"C"` locale semantics,
equivalent to the value `locale("C")`.

*Remarks:* This locale, its facets, and their member functions, do not
change with time.

#### `locale` globals <a id="locale.global.templates">[[locale.global.templates]]</a>

``` cpp
template<class Facet> const Facet& use_facet(const locale& loc);
```

*Mandates:* `Facet` is a facet class whose definition contains the
public static member `id` as defined in  [[locale.facet]].

*Returns:* A reference to the corresponding facet of `loc`, if present.

*Throws:* `bad_cast` if `has_facet<Facet>(loc)` is `false`.

*Remarks:* The reference returned remains valid at least as long as any
copy of `loc` exists.

``` cpp
template<class Facet> bool has_facet(const locale& loc) noexcept;
```

*Returns:* `true` if the facet requested is present in `loc`; otherwise
`false`.

#### Convenience interfaces <a id="locale.convenience">[[locale.convenience]]</a>

##### Character classification <a id="classification">[[classification]]</a>

``` cpp
template<class charT> bool isspace (charT c, const locale& loc);
template<class charT> bool isprint (charT c, const locale& loc);
template<class charT> bool iscntrl (charT c, const locale& loc);
template<class charT> bool isupper (charT c, const locale& loc);
template<class charT> bool islower (charT c, const locale& loc);
template<class charT> bool isalpha (charT c, const locale& loc);
template<class charT> bool isdigit (charT c, const locale& loc);
template<class charT> bool ispunct (charT c, const locale& loc);
template<class charT> bool isxdigit(charT c, const locale& loc);
template<class charT> bool isalnum (charT c, const locale& loc);
template<class charT> bool isgraph (charT c, const locale& loc);
template<class charT> bool isblank (charT c, const locale& loc);
```

Each of these functions `isF` returns the result of the expression:

``` cpp
use_facet<ctype<charT>>(loc).is(ctype_base::F, c)
```

where `F` is the `ctype_base::mask` value corresponding to that function
[[category.ctype]].[^4]

##### Character conversions <a id="conversions.character">[[conversions.character]]</a>

``` cpp
template<class charT> charT toupper(charT c, const locale& loc);
```

*Returns:* `use_facet<ctype<charT>>(loc).toupper(c)`.

``` cpp
template<class charT> charT tolower(charT c, const locale& loc);
```

*Returns:* `use_facet<ctype<charT>>(loc).tolower(c)`.

### Standard `locale` categories <a id="locale.categories">[[locale.categories]]</a>

#### General <a id="locale.categories.general">[[locale.categories.general]]</a>

Each of the standard categories includes a family of facets. Some of
these implement formatting or parsing of a datum, for use by standard or
users’ iostream operators `<<` and `>>`, as members `put()` and `get()`,
respectively. Each such member function takes an `ios_base&` argument
whose members `flags()`, `precision()`, and `width()`, specify the
format of the corresponding datum [[ios.base]]. Those functions which
need to use other facets call its member `getloc()` to retrieve the
locale imbued there. Formatting facets use the character argument `fill`
to fill out the specified width where necessary.

The `put()` members make no provision for error reporting. (Any failures
of the OutputIterator argument can be extracted from the returned
iterator.) The `get()` members take an `ios_base::iostate&` argument
whose value they ignore, but set to `ios_base::failbit` in case of a
parse error.

Within [[locale.categories]] it is unspecified whether one virtual
function calls another virtual function.

#### The `ctype` category <a id="category.ctype">[[category.ctype]]</a>

##### General <a id="category.ctype.general">[[category.ctype.general]]</a>

``` cpp
namespace std {
  class ctype_base {
  public:
    using mask = see below;

    // numeric values are for exposition only.
    static constexpr mask space  = 1 << 0;
    static constexpr mask print  = 1 << 1;
    static constexpr mask cntrl  = 1 << 2;
    static constexpr mask upper  = 1 << 3;
    static constexpr mask lower  = 1 << 4;
    static constexpr mask alpha  = 1 << 5;
    static constexpr mask digit  = 1 << 6;
    static constexpr mask punct  = 1 << 7;
    static constexpr mask xdigit = 1 << 8;
    static constexpr mask blank  = 1 << 9;
    static constexpr mask alnum  = alpha | digit;
    static constexpr mask graph  = alnum | punct;
  };
}
```

The type `mask` is a bitmask type [[bitmask.types]].

##### Class template `ctype` <a id="locale.ctype">[[locale.ctype]]</a>

###### General <a id="locale.ctype.general">[[locale.ctype.general]]</a>

``` cpp
namespace std {
  template<class charT>
    class ctype : public locale::facet, public ctype_base {
    public:
      using char_type = charT;

      explicit ctype(size_t refs = 0);

      bool         is(mask m, charT c) const;
      const charT* is(const charT* low, const charT* high, mask* vec) const;
      const charT* scan_is(mask m, const charT* low, const charT* high) const;
      const charT* scan_not(mask m, const charT* low, const charT* high) const;
      charT        toupper(charT c) const;
      const charT* toupper(charT* low, const charT* high) const;
      charT        tolower(charT c) const;
      const charT* tolower(charT* low, const charT* high) const;

      charT        widen(char c) const;
      const char*  widen(const char* low, const char* high, charT* to) const;
      char         narrow(charT c, char dfault) const;
      const charT* narrow(const charT* low, const charT* high, char dfault, char* to) const;

      static locale::id id;

    protected:
      ~ctype();
      virtual bool         do_is(mask m, charT c) const;
      virtual const charT* do_is(const charT* low, const charT* high, mask* vec) const;
      virtual const charT* do_scan_is(mask m, const charT* low, const charT* high) const;
      virtual const charT* do_scan_not(mask m, const charT* low, const charT* high) const;
      virtual charT        do_toupper(charT) const;
      virtual const charT* do_toupper(charT* low, const charT* high) const;
      virtual charT        do_tolower(charT) const;
      virtual const charT* do_tolower(charT* low, const charT* high) const;
      virtual charT        do_widen(char) const;
      virtual const char*  do_widen(const char* low, const char* high, charT* dest) const;
      virtual char         do_narrow(charT, char dfault) const;
      virtual const charT* do_narrow(const charT* low, const charT* high,
                                     char dfault, char* dest) const;
    };
}
```

Class `ctype` encapsulates the C library `<cctype>` features. `istream`
members are required to use `ctype<>` for character classing during
input parsing.

The specializations required in [[locale.category.facets]]
[[locale.category]], namely `ctype<char>` and `ctype<wchar_t>`,
implement character classing appropriate to the implementation’s native
character set.

###### `ctype` members <a id="locale.ctype.members">[[locale.ctype.members]]</a>

``` cpp
bool         is(mask m, charT c) const;
const charT* is(const charT* low, const charT* high, mask* vec) const;
```

*Returns:* `do_is(m, c)` or `do_is(low, high, vec)`.

``` cpp
const charT* scan_is(mask m, const charT* low, const charT* high) const;
```

*Returns:* `do_scan_is(m, low, high)`.

``` cpp
const charT* scan_not(mask m, const charT* low, const charT* high) const;
```

*Returns:* `do_scan_not(m, low, high)`.

``` cpp
charT        toupper(charT c) const;
const charT* toupper(charT* low, const charT* high) const;
```

*Returns:* `do_toupper(c)` or `do_toupper(low, high)`.

``` cpp
charT        tolower(charT c) const;
const charT* tolower(charT* low, const charT* high) const;
```

*Returns:* `do_tolower(c)` or `do_tolower(low, high)`.

``` cpp
charT       widen(char c) const;
const char* widen(const char* low, const char* high, charT* to) const;
```

*Returns:* `do_widen(c)` or `do_widen(low, high, to)`.

``` cpp
char         narrow(charT c, char dfault) const;
const charT* narrow(const charT* low, const charT* high, char dfault, char* to) const;
```

*Returns:* `do_narrow(c, dfault)` or `do_narrow(low, high, dfault, to)`.

###### `ctype` virtual functions <a id="locale.ctype.virtuals">[[locale.ctype.virtuals]]</a>

``` cpp
bool         do_is(mask m, charT c) const;
const charT* do_is(const charT* low, const charT* high, mask* vec) const;
```

*Effects:* Classifies a character or sequence of characters. For each
argument character, identifies a value `M` of type `ctype_base::mask`.
The second form identifies a value `M` of type `ctype_base::mask` for
each `*p` where `(low <= p && p < high)`, and places it into
`vec[p - low]`.

*Returns:* The first form returns the result of the expression
`(M & m) != 0`; i.e., `true` if the character has the characteristics
specified. The second form returns `high`.

``` cpp
const charT* do_scan_is(mask m, const charT* low, const charT* high) const;
```

*Effects:* Locates a character in a buffer that conforms to a
classification `m`.

*Returns:* The smallest pointer `p` in the range \[`low`, `high`) such
that `is(m, *p)` would return `true`; otherwise, returns `high`.

``` cpp
const charT* do_scan_not(mask m, const charT* low, const charT* high) const;
```

*Effects:* Locates a character in a buffer that fails to conform to a
classification `m`.

*Returns:* The smallest pointer `p`, if any, in the range \[`low`,
`high`) such that `is(m, *p)` would return `false`; otherwise, returns
`high`.

``` cpp
charT        do_toupper(charT c) const;
const charT* do_toupper(charT* low, const charT* high) const;
```

*Effects:* Converts a character or characters to upper case. The second
form replaces each character `*p` in the range \[`low`, `high`) for
which a corresponding upper-case character exists, with that character.

*Returns:* The first form returns the corresponding upper-case character
if it is known to exist, or its argument if not. The second form returns
`high`.

``` cpp
charT        do_tolower(charT c) const;
const charT* do_tolower(charT* low, const charT* high) const;
```

*Effects:* Converts a character or characters to lower case. The second
form replaces each character `*p` in the range \[`low`, `high`) and for
which a corresponding lower-case character exists, with that character.

*Returns:* The first form returns the corresponding lower-case character
if it is known to exist, or its argument if not. The second form returns
`high`.

``` cpp
charT        do_widen(char c) const;
const char*  do_widen(const char* low, const char* high, charT* dest) const;
```

*Effects:* Applies the simplest reasonable transformation from a `char`
value or sequence of `char` values to the corresponding `charT` value or
values.[^5]

The only characters for which unique transformations are required are
those in the basic character set [[lex.charset]].

For any named `ctype` category with a `ctype<char>` facet `ctc` and
valid `ctype_base::mask` value `M`,
`(ctc.is(M, c) || !is(M, do_widen(c)) )` is `true`.[^6]

The second form transforms each character `*p` in the range \[`low`,
`high`), placing the result in `dest[p - low]`.

*Returns:* The first form returns the transformed value. The second form
returns `high`.

``` cpp
char         do_narrow(charT c, char dfault) const;
const charT* do_narrow(const charT* low, const charT* high, char dfault, char* dest) const;
```

*Effects:* Applies the simplest reasonable transformation from a `charT`
value or sequence of `charT` values to the corresponding `char` value or
values.

For any character `c` in the basic character set [[lex.charset]] the
transformation is such that

``` cpp
do_widen(do_narrow(c, 0)) == c
```

For any named `ctype` category with a `ctype<char>` facet `ctc` however,
and `ctype_base::mask` value `M`,

``` cpp
(is(M, c) || !ctc.is(M, do_narrow(c, dfault)) )
```

is `true` (unless `do_narrow` returns `dfault`). In addition, for any
digit character `c`, the expression `(do_narrow(c, dfault) - ’0’)`
evaluates to the digit value of the character. The second form
transforms each character `*p` in the range \[`low`, `high`), placing
the result (or `dfault` if no simple transformation is readily
available) in `dest[p - low]`.

*Returns:* The first form returns the transformed value; or `dfault` if
no mapping is readily available. The second form returns `high`.

##### Class template `ctype_byname` <a id="locale.ctype.byname">[[locale.ctype.byname]]</a>

``` cpp
namespace std {
  template<class charT>
    class ctype_byname : public ctype<charT> {
    public:
      using mask = ctype<charT>::mask;
      explicit ctype_byname(const char*, size_t refs = 0);
      explicit ctype_byname(const string&, size_t refs = 0);

    protected:
      ~ctype_byname();
    };
}
```

##### `ctype<char>` specialization <a id="facet.ctype.special">[[facet.ctype.special]]</a>

###### General <a id="facet.ctype.special.general">[[facet.ctype.special.general]]</a>

``` cpp
namespace std {
  template<>
    class ctype<char> : public locale::facet, public ctype_base {
    public:
      using char_type = char;

      explicit ctype(const mask* tab = nullptr, bool del = false, size_t refs = 0);

      bool is(mask m, char c) const;
      const char* is(const char* low, const char* high, mask* vec) const;
      const char* scan_is (mask m, const char* low, const char* high) const;
      const char* scan_not(mask m, const char* low, const char* high) const;

      char        toupper(char c) const;
      const char* toupper(char* low, const char* high) const;
      char        tolower(char c) const;
      const char* tolower(char* low, const char* high) const;

      char  widen(char c) const;
      const char* widen(const char* low, const char* high, char* to) const;
      char  narrow(char c, char dfault) const;
      const char* narrow(const char* low, const char* high, char dfault, char* to) const;

      static locale::id id;
      static const size_t table_size = implementation-defined;

      const mask* table() const noexcept;
      static const mask* classic_table() noexcept;

    protected:
      ~ctype();
      virtual char        do_toupper(char c) const;
      virtual const char* do_toupper(char* low, const char* high) const;
      virtual char        do_tolower(char c) const;
      virtual const char* do_tolower(char* low, const char* high) const;

      virtual char        do_widen(char c) const;
      virtual const char* do_widen(const char* low, const char* high, char* to) const;
      virtual char        do_narrow(char c, char dfault) const;
      virtual const char* do_narrow(const char* low, const char* high,
                                    char dfault, char* to) const;
    };
}
```

A specialization `ctype<char>` is provided so that the member functions
on type `char` can be implemented inline.[^7]

The *implementation-defined* value of member `table_size` is at least
256.

###### Destructor <a id="facet.ctype.char.dtor">[[facet.ctype.char.dtor]]</a>

``` cpp
~ctype();
```

*Effects:* If the constructor’s first argument was nonzero, and its
second argument was `true`, does `delete [] table()`.

###### Members <a id="facet.ctype.char.members">[[facet.ctype.char.members]]</a>

In the following member descriptions, for `unsigned char` values `v`
where `v >= table_size`, `table()[v]` is assumed to have an
implementation-specific value (possibly different for each such value
`v`) without performing the array lookup.

``` cpp
explicit ctype(const mask* tbl = nullptr, bool del = false, size_t refs = 0);
```

*Preconditions:* Either `tbl == nullptr` is `true` or \[`tbl`,
`tbl + table_size`) is a valid range.

*Effects:* Passes its `refs` argument to its base class constructor.

``` cpp
bool        is(mask m, char c) const;
const char* is(const char* low, const char* high, mask* vec) const;
```

*Effects:* The second form, for all `*p` in the range \[`low`, `high`),
assigns into `vec[p - low]` the value `table()[(unsigned char)*p]`.

*Returns:* The first form returns `table()[(unsigned char)c] & m`; the
second form returns `high`.

``` cpp
const char* scan_is(mask m, const char* low, const char* high) const;
```

*Returns:* The smallest `p` in the range \[`low`, `high`) such that

``` cpp
table()[(unsigned char) *p] & m
```

is `true`.

``` cpp
const char* scan_not(mask m, const char* low, const char* high) const;
```

*Returns:* The smallest `p` in the range \[`low`, `high`) such that

``` cpp
table()[(unsigned char) *p] & m
```

is `false`.

``` cpp
char        toupper(char c) const;
const char* toupper(char* low, const char* high) const;
```

*Returns:* `do_toupper(c)` or `do_toupper(low, high)`, respectively.

``` cpp
char        tolower(char c) const;
const char* tolower(char* low, const char* high) const;
```

*Returns:* `do_tolower(c)` or `do_tolower(low, high)`, respectively.

``` cpp
char  widen(char c) const;
const char* widen(const char* low, const char* high, char* to) const;
```

*Returns:* `do_widen(c)` or `do_widen(low, high, to)`, respectively.

``` cpp
char        narrow(char c, char dfault) const;
const char* narrow(const char* low, const char* high, char dfault, char* to) const;
```

*Returns:* `do_narrow(c, dfault)` or `do_narrow(low, high, dfault, to)`,
respectively.

``` cpp
const mask* table() const noexcept;
```

*Returns:* The first constructor argument, if it was nonzero, otherwise
`classic_table()`.

###### Static members <a id="facet.ctype.char.statics">[[facet.ctype.char.statics]]</a>

``` cpp
static const mask* classic_table() noexcept;
```

*Returns:* A pointer to the initial element of an array of size
`table_size` which represents the classifications of characters in the
`"C"` locale.

###### Virtual functions <a id="facet.ctype.char.virtuals">[[facet.ctype.char.virtuals]]</a>

``` cpp
char        do_toupper(char) const;
const char* do_toupper(char* low, const char* high) const;
char        do_tolower(char) const;
const char* do_tolower(char* low, const char* high) const;

virtual char        do_widen(char c) const;
virtual const char* do_widen(const char* low, const char* high, char* to) const;
virtual char        do_narrow(char c, char dfault) const;
virtual const char* do_narrow(const char* low, const char* high,
                              char dfault, char* to) const;
```

These functions are described identically as those members of the same
name in the `ctype` class template [[locale.ctype.members]].

##### Class template `codecvt` <a id="locale.codecvt">[[locale.codecvt]]</a>

###### General <a id="locale.codecvt.general">[[locale.codecvt.general]]</a>

``` cpp
namespace std {
  class codecvt_base {
  public:
    enum result { ok, partial, error, noconv };
  };

  template<class internT, class externT, class stateT>
    class codecvt : public locale::facet, public codecvt_base {
    public:
      using intern_type = internT;
      using extern_type = externT;
      using state_type  = stateT;

      explicit codecvt(size_t refs = 0);

      result out(
        stateT& state,
        const internT* from, const internT* from_end, const internT*& from_next,
              externT*   to,       externT*   to_end,       externT*&   to_next) const;

      result unshift(
        stateT& state,
              externT*    to,      externT*   to_end,       externT*&   to_next) const;

      result in(
        stateT& state,
        const externT* from, const externT* from_end, const externT*& from_next,
              internT*   to,       internT*   to_end,       internT*&   to_next) const;

      int encoding() const noexcept;
      bool always_noconv() const noexcept;
      int length(stateT&, const externT* from, const externT* end, size_t max) const;
      int max_length() const noexcept;

      static locale::id id;

    protected:
      ~codecvt();
      virtual result do_out(
        stateT& state,
        const internT* from, const internT* from_end, const internT*& from_next,
              externT* to,         externT*   to_end,       externT*&   to_next) const;
      virtual result do_in(
        stateT& state,
        const externT* from, const externT* from_end, const externT*& from_next,
              internT* to,         internT*   to_end,       internT*&   to_next) const;
      virtual result do_unshift(
        stateT& state,
              externT* to,         externT*   to_end,       externT*&   to_next) const;

      virtual int do_encoding() const noexcept;
      virtual bool do_always_noconv() const noexcept;
      virtual int do_length(stateT&, const externT* from, const externT* end, size_t max) const;
      virtual int do_max_length() const noexcept;
    };
}
```

The class `codecvt<internT, externT, stateT>` is for use when converting
from one character encoding to another, such as from wide characters to
multibyte characters or between wide character encodings such as UTF-32
and EUC.

The `stateT` argument selects the pair of character encodings being
mapped between.

The specializations required in [[locale.category.facets]]
[[locale.category]] convert the implementation-defined native character
set. `codecvt<char, char, mbstate_t>` implements a degenerate
conversion; it does not convert at all.
`codecvt<wchar_t, char, mbstate_t>` converts between the native
character sets for ordinary and wide characters. Specializations on
`mbstate_t` perform conversion between encodings known to the library
implementer. Other encodings can be converted by specializing on a
program-defined `stateT` type. Objects of type `stateT` can contain any
state that is useful to communicate to or from the specialized `do_in`
or `do_out` members.

###### Members <a id="locale.codecvt.members">[[locale.codecvt.members]]</a>

``` cpp
result out(
  stateT& state,
  const internT* from, const internT* from_end, const internT*& from_next,
  externT* to, externT* to_end, externT*& to_next) const;
```

*Returns:*
`do_out(state, from, from_end, from_next, to, to_end, to_next)`.

``` cpp
result unshift(stateT& state, externT* to, externT* to_end, externT*& to_next) const;
```

*Returns:* `do_unshift(state, to, to_end, to_next)`.

``` cpp
result in(
  stateT& state,
  const externT* from, const externT* from_end, const externT*& from_next,
  internT* to, internT* to_end, internT*& to_next) const;
```

*Returns:*
`do_in(state, from, from_end, from_next, to, to_end, to_next)`.

``` cpp
int encoding() const noexcept;
```

*Returns:* `do_encoding()`.

``` cpp
bool always_noconv() const noexcept;
```

*Returns:* `do_always_noconv()`.

``` cpp
int length(stateT& state, const externT* from, const externT* from_end, size_t max) const;
```

*Returns:* `do_length(state, from, from_end, max)`.

``` cpp
int max_length() const noexcept;
```

*Returns:* `do_max_length()`.

###### Virtual functions <a id="locale.codecvt.virtuals">[[locale.codecvt.virtuals]]</a>

``` cpp
result do_out(
  stateT& state,
  const internT* from, const internT* from_end, const internT*& from_next,
  externT* to, externT* to_end, externT*& to_next) const;

result do_in(
  stateT& state,
  const externT* from, const externT* from_end, const externT*& from_next,
  internT* to, internT* to_end, internT*& to_next) const;
```

*Preconditions:* `(from <= from_end && to <= to_end)` is well-defined
and `true`; `state` is initialized, if at the beginning of a sequence,
or else is equal to the result of converting the preceding characters in
the sequence.

*Effects:* Translates characters in the source range \[`from`,
`from_end`), placing the results in sequential positions starting at
destination `to`. Converts no more than `(from_end - from)` source
elements, and stores no more than `(to_end - to)` destination elements.

Stops if it encounters a character it cannot convert. It always leaves
the `from_next` and `to_next` pointers pointing one beyond the last
element successfully converted. If it returns `noconv`, `internT` and
`externT` are the same type, and the converted sequence is identical to
the input sequence \[`from`, `from``next`), `to_next` is set equal to
`to`, the value of `state` is unchanged, and there are no changes to the
values in \[`to`, `to_end`).

A `codecvt` facet that is used by `basic_filebuf`[[file.streams]] shall
have the property that if

``` cpp
do_out(state, from, from_end, from_next, to, to_end, to_next)
```

would return `ok`, where `from != from_end`, then

``` cpp
do_out(state, from, from + 1, from_next, to, to_end, to_next)
```

shall also return `ok`, and that if

``` cpp
do_in(state, from, from_end, from_next, to, to_end, to_next)
```

would return `ok`, where `to != to_end`, then

``` cpp
do_in(state, from, from_end, from_next, to, to + 1, to_next)
```

shall also return `ok`.[^8]

[*Note 1*: As a result of operations on `state`, it can return `ok` or
`partial` and set `from_next == from` and
`to_next != to`. — *end note*]

*Returns:* An enumeration value, as summarized in
[[locale.codecvt.inout]].

**Table: `do_in/do_out` result values**

| Value     | Meaning                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------ |
| `ok`      | completed the conversion                                                                         |
| `partial` | not all source characters converted                                                              |
| `error`   | encountered a character in {[}`from`, `from_end`{)} that cannot be converted                     |
| `noconv`  | `internT` and `externT` are the same type, and input sequence is identical to converted sequence |


A return value of `partial`, if `(from_next == from_end)`, indicates
that either the destination sequence has not absorbed all the available
destination elements, or that additional source elements are needed
before another destination element can be produced.

*Remarks:* Its operations on `state` are unspecified.

[*Note 2*: This argument can be used, for example, to maintain shift
state, to specify conversion options (such as count only), or to
identify a cache of seek offsets. — *end note*]

``` cpp
result do_unshift(stateT& state, externT* to, externT* to_end, externT*& to_next) const;
```

*Preconditions:* `(to <= to_end)` is well-defined and `true`; `state` is
initialized, if at the beginning of a sequence, or else is equal to the
result of converting the preceding characters in the sequence.

*Effects:* Places characters starting at `to` that should be appended to
terminate a sequence when the current `stateT` is given by `state`.[^9]

Stores no more than `(to_end - to)` destination elements, and leaves the
`to_next` pointer pointing one beyond the last element successfully
stored.

*Returns:* An enumeration value, as summarized in
[[locale.codecvt.unshift]].

**Table: `do_unshift` result values**

| Value     | Meaning                                                                                                              |
| --------- | -------------------------------------------------------------------------------------------------------------------- |
| `ok`      | completed the sequence                                                                                               |
| `partial` | space for more than `to_end - to` destination elements was needed to terminate a sequence given the value of `state` |
| `error`   | an unspecified error has occurred                                                                                    |
| `noconv`  | no termination is needed for this `state_type`                                                                       |

``` cpp
int do_encoding() const noexcept;
```

*Returns:* `-1` if the encoding of the `externT` sequence is
state-dependent; else the constant number of `externT` characters needed
to produce an internal character; or `0` if this number is not a
constant.[^10]

``` cpp
bool do_always_noconv() const noexcept;
```

*Returns:* `true` if `do_in()` and `do_out()` return `noconv` for all
valid argument values. `codecvt<char, char, mbstate_t>` returns `true`.

``` cpp
int do_length(stateT& state, const externT* from, const externT* from_end, size_t max) const;
```

*Preconditions:* `(from <= from_end)` is well-defined and `true`;
`state` is initialized, if at the beginning of a sequence, or else is
equal to the result of converting the preceding characters in the
sequence.

*Effects:* The effect on the `state` argument is as if it called
`do_in(state, from, from_end, from, to, to + max, to)` for `to` pointing
to a buffer of at least `max` elements.

*Returns:* `(from_next - from)` where `from_next` is the largest value
in the range \[`from`, `from_end`\] such that the sequence of values in
the range \[`from`, `from_next`) represents `max` or fewer valid
complete characters of type `internT`. The specialization
`codecvt<char, char, mbstate_t>`, returns the lesser of `max` and
`(from_end - from)`.

``` cpp
int do_max_length() const noexcept;
```

*Returns:* The maximum value that `do_length(state, from, from_end, 1)`
can return for any valid range \[`from`, `from_end`) and `stateT` value
`state`. The specialization
`codecvt<char, char, mbstate_t>::do_max_length()` returns 1.

##### Class template `codecvt_byname` <a id="locale.codecvt.byname">[[locale.codecvt.byname]]</a>

``` cpp
namespace std {
  template<class internT, class externT, class stateT>
    class codecvt_byname : public codecvt<internT, externT, stateT> {
    public:
      explicit codecvt_byname(const char*, size_t refs = 0);
      explicit codecvt_byname(const string&, size_t refs = 0);

    protected:
      ~codecvt_byname();
    };
}
```

#### The numeric category <a id="category.numeric">[[category.numeric]]</a>

##### General <a id="category.numeric.general">[[category.numeric.general]]</a>

The classes `num_get<>` and `num_put<>` handle numeric formatting and
parsing. Virtual functions are provided for several numeric types.
Implementations may (but are not required to) delegate extraction of
smaller types to extractors for larger types.[^11]

All specifications of member functions for `num_put` and `num_get` in
the subclauses of  [[category.numeric]] only apply to the
specializations required in Tables  [[tab:locale.category.facets]] and 
[[tab:locale.spec]] [[locale.category]], namely `num_get<char>`,
`num_get<wchar_t>`, `num_get<C, InputIterator>`, `num_put<char>`,
`num_put<wchar_t>`, and `num_put<C, OutputIterator>`. These
specializations refer to the `ios_base&` argument for formatting
specifications [[locale.categories]], and to its imbued locale for the
`numpunct<>` facet to identify all numeric punctuation preferences, and
also for the `ctype<>` facet to perform character classification.

Extractor and inserter members of the standard iostreams use `num_get<>`
and `num_put<>` member functions for formatting and parsing numeric
values [[istream.formatted.reqmts]], [[ostream.formatted.reqmts]].

##### Class template `num_get` <a id="locale.num.get">[[locale.num.get]]</a>

###### General <a id="locale.num.get.general">[[locale.num.get.general]]</a>

``` cpp
namespace std {
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class num_get : public locale::facet {
    public:
      using char_type = charT;
      using iter_type = InputIterator;

      explicit num_get(size_t refs = 0);

      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, bool& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, long& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, long long& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, unsigned short& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, unsigned int& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, unsigned long& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, unsigned long long& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, float& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, double& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, long double& v) const;
      iter_type get(iter_type in, iter_type end, ios_base&,
                    ios_base::iostate& err, void*& v) const;

      static locale::id id;

    protected:
      ~num_get();
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, bool& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, long& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, long long& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, unsigned short& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, unsigned int& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, unsigned long& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, unsigned long long& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, float& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, double& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, long double& v) const;
      virtual iter_type do_get(iter_type, iter_type, ios_base&,
                               ios_base::iostate& err, void*& v) const;
    };
}
```

The facet `num_get` is used to parse numeric values from an input
sequence such as an istream.

###### Members <a id="facet.num.get.members">[[facet.num.get.members]]</a>

``` cpp
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, bool& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, long& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, long long& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, unsigned short& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, unsigned int& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, unsigned long& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, unsigned long long& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, float& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, double& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, long double& val) const;
iter_type get(iter_type in, iter_type end, ios_base& str,
              ios_base::iostate& err, void*& val) const;
```

*Returns:* `do_get(in, end, str, err, val)`.

###### Virtual functions <a id="facet.num.get.virtuals">[[facet.num.get.virtuals]]</a>

``` cpp
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, long& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, long long& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, unsigned short& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, unsigned int& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, unsigned long& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, unsigned long long& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, float& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, double& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, long double& val) const;
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, void*& val) const;
```

*Effects:* Reads characters from `in`, interpreting them according to
`str.flags()`, `use_facet<ctype<charT>>(loc)`, and
`use_facet<numpunct<charT>>(loc)`, where `loc` is `str.getloc()`.

The details of this operation occur in three stages:

- Stage 1: Determine a conversion specifier.
- Stage 2: Extract characters from `in` and determine a corresponding
  `char` value for the format expected by the conversion specification
  determined in stage 1.
- Stage 3: Store results.

The details of the stages are presented below.

[*Example 1*:

Given an input sequence of `"0x1a.bp+07p"`,

- if the conversion specifier returned by Stage 1 is `%d`, `"0"` is
  accumulated;
- if the conversion specifier returned by Stage 1 is `%i`, `"0x1a"` are
  accumulated;
- if the conversion specifier returned by Stage 1 is `%g`,
  `"0x1a.bp+07"` are accumulated.

In all cases, the remainder is left in the input.

— *end example*]

Digit grouping is checked. That is, the positions of discarded
separators are examined for consistency with
`use_facet<numpunct<charT>>(loc).grouping()`. If they are not consistent
then `ios_base::failbit` is assigned to `err`.

In any case, if stage 2 processing was terminated by the test for
`in == end` then `err |= ios_base::eofbit` is performed.

``` cpp
iter_type do_get(iter_type in, iter_type end, ios_base& str,
                 ios_base::iostate& err, bool& val) const;
```

*Effects:* If `(str.flags() & ios_base::boolalpha) == 0` then input
proceeds as it would for a `long` except that if a value is being stored
into `val`, the value is determined according to the following: If the
value to be stored is 0 then `false` is stored. If the value is `1` then
`true` is stored. Otherwise `true` is stored and `ios_base::failbit` is
assigned to `err`.

Otherwise target sequences are determined “as if” by calling the members
`falsename()` and `truename()` of the facet obtained by
`use_facet<numpunct<charT>>(str.getloc())`. Successive characters in the
range \[`in`, `end`) (see  [[sequence.reqmts]]) are obtained and matched
against corresponding positions in the target sequences only as
necessary to identify a unique match. The input iterator `in` is
compared to `end` only when necessary to obtain a character. If a target
sequence is uniquely matched, `val` is set to the corresponding value.
Otherwise `false` is stored and `ios_base::failbit` is assigned to
`err`.

The `in` iterator is always left pointing one position beyond the last
character successfully matched. If `val` is set, then `err` is set to
`str.goodbit`; or to `str.eofbit` if, when seeking another character to
match, it is found that `(in == end)`. If `val` is not set, then `err`
is set to `str.failbit`; or to `(str.failbit | str.eofbit)` if the
reason for the failure was that `(in == end)`.

[*Example 2*: For targets `true`: `"a"` and `false`: `"abb"`, the input
sequence `"a"` yields `val == true` and `err == str.eofbit`; the input
sequence `"abc"` yields `err = str.failbit`, with `in` ending at the
`’c’` element. For targets `true`: `"1"` and `false`: `"0"`, the input
sequence `"1"` yields `val == true` and `err == str.goodbit`. For empty
targets `("")`, any input sequence yields
`err == str.failbit`. — *end example*]

*Returns:* `in`.

##### Class template `num_put` <a id="locale.nm.put">[[locale.nm.put]]</a>

###### General <a id="locale.nm.put.general">[[locale.nm.put.general]]</a>

``` cpp
namespace std {
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class num_put : public locale::facet {
    public:
      using char_type = charT;
      using iter_type = OutputIterator;

      explicit num_put(size_t refs = 0);

      iter_type put(iter_type s, ios_base& f, char_type fill, bool v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, long v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, long long v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, unsigned long v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, unsigned long long v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, double v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, long double v) const;
      iter_type put(iter_type s, ios_base& f, char_type fill, const void* v) const;

      static locale::id id;

    protected:
      ~num_put();
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, bool v) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, long v) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, long long v) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, unsigned long) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, unsigned long long) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, double v) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, long double v) const;
      virtual iter_type do_put(iter_type, ios_base&, char_type fill, const void* v) const;
    };
}
```

The facet `num_put` is used to format numeric values to a character
sequence such as an ostream.

###### Members <a id="facet.num.put.members">[[facet.num.put.members]]</a>

``` cpp
iter_type put(iter_type out, ios_base& str, char_type fill, bool val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, long val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, long long val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, unsigned long val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, unsigned long long val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, double val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, long double val) const;
iter_type put(iter_type out, ios_base& str, char_type fill, const void* val) const;
```

*Returns:* `do_put(out, str, fill, val)`.

###### Virtual functions <a id="facet.num.put.virtuals">[[facet.num.put.virtuals]]</a>

``` cpp
iter_type do_put(iter_type out, ios_base& str, char_type fill, long val) const;
iter_type do_put(iter_type out, ios_base& str, char_type fill, long long val) const;
iter_type do_put(iter_type out, ios_base& str, char_type fill, unsigned long val) const;
iter_type do_put(iter_type out, ios_base& str, char_type fill, unsigned long long val) const;
iter_type do_put(iter_type out, ios_base& str, char_type fill, double val) const;
iter_type do_put(iter_type out, ios_base& str, char_type fill, long double val) const;
iter_type do_put(iter_type out, ios_base& str, char_type fill, const void* val) const;
```

*Effects:* Writes characters to the sequence `out`, formatting `val` as
desired. In the following description, `loc` names a local variable
initialized as

``` cpp
locale loc = str.getloc();
```

The details of this operation occur in several stages:

- Stage 1: Determine a printf conversion specifier `spec` and determine
  the characters that would be printed by `printf`[[c.files]] given this
  conversion specifier for
  ``` cpp
  printf(spec, val)
  ```

  assuming that the current locale is the `"C"` locale.
- Stage 2: Adjust the representation by converting each `char`
  determined by stage 1 to a `charT` using a conversion and values
  returned by members of `use_facet<numpunct<charT>>(loc)`.
- Stage 3: Determine where padding is required.
- Stage 4: Insert the sequence into the `out`.

Detailed descriptions of each stage follow.

*Returns:* `out`.

- **Stage 1:**

The first action of stage 1 is to determine a conversion specifier. The
tables that describe this determination use the following local
variables

``` cpp
fmtflags flags = str.flags();
fmtflags basefield =  (flags & (ios_base::basefield));
fmtflags uppercase =  (flags & (ios_base::uppercase));
fmtflags floatfield = (flags & (ios_base::floatfield));
fmtflags showpos =    (flags & (ios_base::showpos));
fmtflags showbase =   (flags & (ios_base::showbase));
fmtflags showpoint =  (flags & (ios_base::showpoint));
```

All tables used in describing stage 1 are ordered. That is, the first
line whose condition is true applies. A line without a condition is the
default behavior when none of the earlier lines apply.

For conversion from an integral type other than a character type, the
function determines the integral conversion specifier as indicated in
[[facet.num.put.int]].

**Table: Integer conversions**

| State                                        | `stdio` equivalent |
| -------------------------------------------- | ------------------ |
| `basefield == ios_base::oct`                 | `%o`               |
| `(basefield == ios_base::hex) && !uppercase` | `%x`               |
| `(basefield == ios_base::hex)`               | `%X`               |
| for a `signed` integral type                 | `%d`               |
| for an `unsigned` integral type              | `%u`               |


For conversion from a floating-point type, the function determines the
floating-point conversion specifier as indicated in
[[facet.num.put.fp]].

**Table: Floating-point conversions**

| State                                                                  | `stdio` equivalent |
| ---------------------------------------------------------------------- | ------------------ |
| `floatfield == ios_base::fixed && !uppercase`                          | `%f`               |
| `floatfield == ios_base::fixed`                                        | `%F`               |
| `floatfield == ios_base::scientific && !uppercase`                     | `%e`               |
| `floatfield == ios_base::scientific`                                   | `%E`               |
| `floatfield == (ios_base::fixed | ios_base::scientific) && !uppercase` | `%a`               |
| `floatfield == (ios_base::fixed | ios_base::scientific)`               | `%A`               |
| `!uppercase`                                                           | `%g`               |
| otherwise                                                              | `%G`               |


For conversions from an integral or floating-point type a length
modifier is added to the conversion specifier as indicated in
[[facet.num.put.length]].

**Table: Length modifier**

| Type                 | Length modifier |
| -------------------- | --------------- |
| `long`               | `l`             |
| `long long`          | `ll`            |
| `unsigned long`      | `l`             |
| `unsigned long long` | `ll`            |
| `long double`        | `L`             |
| otherwise            | none            |


The conversion specifier has the following optional additional
qualifiers prepended as indicated in [[facet.num.put.conv]].

**Table: Numeric conversions**

| Type(s)               | State       | `stdio` equivalent |
| --------------------- | ----------- | ------------------ |
| an integral type      | `showpos`   | `+`                |
|                       | `showbase`  | `#`                |
| a floating-point type | `showpos`   | `+`                |
|                       | `showpoint` | `#`                |


For conversion from a floating-point type, if
`floatfield != (ios_base::fixed | ios_base::scientific)`,
`str.precision()` is specified as precision in the conversion
specification. Otherwise, no precision is specified.

For conversion from `void*` the specifier is `%p`.

The representations at the end of stage 1 consists of the `char`’s that
would be printed by a call of `printf(s, val)` where `s` is the
conversion specifier determined above.

- **Stage 2:**

Any character `c` other than a decimal point(.) is converted to a
`charT` via

``` cpp
use_facet<ctype<charT>>(loc).widen(c)
```

A local variable `punct` is initialized via

``` cpp
const numpunct<charT>& punct = use_facet<numpunct<charT>>(loc);
```

For arithmetic types, `punct.thousands_sep()` characters are inserted
into the sequence as determined by the value returned by
`punct.do_grouping()` using the method described
in [[facet.numpunct.virtuals]].

Decimal point characters(.) are replaced by `punct.decimal_point()`.

- **Stage 3:**

A local variable is initialized as

``` cpp
fmtflags adjustfield = (flags & (ios_base::adjustfield));
```

The location of any padding[^12]

is determined according to [[facet.num.put.fill]].

**Table: Fill padding**

| State                                                                          | Location           |
| ------------------------------------------------------------------------------ | ------------------ |
| `adjustfield == ios_base::left`                                                | pad after          |
| `adjustfield == ios_base::right`                                               | pad before         |
| `adjustfield == internal` and a sign occurs in the representation              | pad after the sign |
| `adjustfield == internal` and representation after stage 1 began with 0x or 0X | pad after x or X   |
| otherwise                                                                      | pad before         |


If `str.width()` is nonzero and the number of `charT`’s in the sequence
after stage 2 is less than `str.width()`, then enough `fill` characters
are added to the sequence at the position indicated for padding to bring
the length of the sequence to `str.width()`.

`str.width(0)` is called.

- **Stage 4:**

The sequence of `charT`’s at the end of stage 3 are output via

``` cpp
*out++ = c
```

``` cpp
iter_type do_put(iter_type out, ios_base& str, char_type fill, bool val) const;
```

*Returns:* If `(str.flags() & ios_base::boolalpha) == 0` returns
`do_put(out, str, fill,`  
`(int)val)`, otherwise obtains a string `s` as if by

``` cpp
string_type s =
  val ? use_facet<numpunct<charT>>(loc).truename()
      : use_facet<numpunct<charT>>(loc).falsename();
```

and then inserts each character `c` of `s` into `out` via `*out++ = c`
and returns `out`.

#### The numeric punctuation facet <a id="facet.numpunct">[[facet.numpunct]]</a>

##### Class template `numpunct` <a id="locale.numpunct">[[locale.numpunct]]</a>

###### General <a id="locale.numpunct.general">[[locale.numpunct.general]]</a>

``` cpp
namespace std {
  template<class charT>
    class numpunct : public locale::facet {
    public:
      using char_type   = charT;
      using string_type = basic_string<charT>;

      explicit numpunct(size_t refs = 0);

      char_type   decimal_point() const;
      char_type   thousands_sep() const;
      string      grouping()      const;
      string_type truename()      const;
      string_type falsename()     const;

      static locale::id id;

    protected:
      ~numpunct();                                              // virtual
      virtual char_type   do_decimal_point() const;
      virtual char_type   do_thousands_sep() const;
      virtual string      do_grouping()      const;
      virtual string_type do_truename()      const;             // for bool
      virtual string_type do_falsename()     const;             // for bool
    };
}
```

`numpunct<>` specifies numeric punctuation. The specializations required
in [[locale.category.facets]] [[locale.category]], namely
`numpunct<{}wchar_t>` and `numpunct<char>`, provide classic `"C"`
numeric formats, i.e., they contain information equivalent to that
contained in the `"C"` locale or their wide character counterparts as if
obtained by a call to `widen`.

The syntax for number formats is as follows, where represents the radix
set specified by the `fmtflags` argument value, and and are the results
of corresponding `numpunct<charT>` members. Integer values have the
format:

``` bnf
{\BnfNontermshape intval\itcorr}:
    signₒₚₜ units
```

``` bnf
{\BnfNontermshape sign\itcorr}:
    '+'
    '-'
```

``` bnf
{\BnfNontermshape units\itcorr}:
    digits
    digits thousands-sep units
```

``` bnf
{\BnfNontermshape digits\itcorr}:
    digit digitsₒₚₜ
```

and floating-point values have:

``` bnf
{\BnfNontermshape floatval\itcorr}:
    signₒₚₜ units fractionalₒₚₜ exponentₒₚₜ
    signₒₚₜ decimal-point digits exponentₒₚₜ
```

``` bnf
{\BnfNontermshape fractional\itcorr}:
    decimal-point digitsₒₚₜ
```

``` bnf
{\BnfNontermshape exponent\itcorr}:
    e signₒₚₜ digits
```

``` bnf
{\BnfNontermshape e\itcorr}:
    'e'
    'E'
```

where the number of digits between is as specified by `do_grouping()`.
For parsing, if the portion contains no thousands-separators, no
grouping constraint is applied.

###### Members <a id="facet.numpunct.members">[[facet.numpunct.members]]</a>

``` cpp
char_type decimal_point() const;
```

*Returns:* `do_decimal_point()`.

``` cpp
char_type thousands_sep() const;
```

*Returns:* `do_thousands_sep()`.

``` cpp
string grouping() const;
```

*Returns:* `do_grouping()`.

``` cpp
string_type truename()  const;
string_type falsename() const;
```

*Returns:* `do_truename()` or `do_falsename()`, respectively.

###### Virtual functions <a id="facet.numpunct.virtuals">[[facet.numpunct.virtuals]]</a>

``` cpp
char_type do_decimal_point() const;
```

*Returns:* A character for use as the decimal radix separator. The
required specializations return `’.’` or `L’.’`.

``` cpp
char_type do_thousands_sep() const;
```

*Returns:* A character for use as the digit group separator. The
required specializations return `’,’` or `L’,’`.

``` cpp
string do_grouping() const;
```

*Returns:* A `string` `vec` used as a vector of integer values, in which
each element `vec[i]` represents the number of digits[^13]

in the group at position `i`, starting with position 0 as the rightmost
group. If `vec.size() <= i`, the number is the same as group `(i - 1)`;
if `(i < 0 || vec[i] <= 0 || vec[i] == CHAR_MAX)`, the size of the digit
group is unlimited.

The required specializations return the empty string, indicating no
grouping.

``` cpp
string_type do_truename()  const;
string_type do_falsename() const;
```

*Returns:* A string representing the name of the boolean value `true` or
`false`, respectively.

In the base class implementation these names are `"true"` and `"false"`,
or `L"true"` and `L"false"`.

##### Class template `numpunct_byname` <a id="locale.numpunct.byname">[[locale.numpunct.byname]]</a>

``` cpp
namespace std {
  template<class charT>
    class numpunct_byname : public numpunct<charT> {
    // this class is specialized for char and wchar_t.
    public:
      using char_type   = charT;
      using string_type = basic_string<charT>;

      explicit numpunct_byname(const char*, size_t refs = 0);
      explicit numpunct_byname(const string&, size_t refs = 0);

    protected:
      ~numpunct_byname();
    };
}
```

#### The collate category <a id="category.collate">[[category.collate]]</a>

##### Class template `collate` <a id="locale.collate">[[locale.collate]]</a>

###### General <a id="locale.collate.general">[[locale.collate.general]]</a>

``` cpp
namespace std {
  template<class charT>
    class collate : public locale::facet {
    public:
      using char_type   = charT;
      using string_type = basic_string<charT>;

      explicit collate(size_t refs = 0);

      int compare(const charT* low1, const charT* high1,
                  const charT* low2, const charT* high2) const;
      string_type transform(const charT* low, const charT* high) const;
      long hash(const charT* low, const charT* high) const;

      static locale::id id;

    protected:
      ~collate();
      virtual int do_compare(const charT* low1, const charT* high1,
                             const charT* low2, const charT* high2) const;
      virtual string_type do_transform(const charT* low, const charT* high) const;
      virtual long do_hash (const charT* low, const charT* high) const;
    };
}
```

The class `collate<charT>` provides features for use in the collation
(comparison) and hashing of strings. A locale member function template,
`operator()`, uses the collate facet to allow a locale to act directly
as the predicate argument for standard algorithms [[algorithms]] and
containers operating on strings. The specializations required in
[[locale.category.facets]] [[locale.category]], namely `collate<char>`
and `collate<wchar_t>`, apply lexicographical ordering
[[alg.lex.comparison]].

Each function compares a string of characters `*p` in the range \[`low`,
`high`).

###### Members <a id="locale.collate.members">[[locale.collate.members]]</a>

``` cpp
int compare(const charT* low1, const charT* high1,
            const charT* low2, const charT* high2) const;
```

*Returns:* `do_compare(low1, high1, low2, high2)`.

``` cpp
string_type transform(const charT* low, const charT* high) const;
```

*Returns:* `do_transform(low, high)`.

``` cpp
long hash(const charT* low, const charT* high) const;
```

*Returns:* `do_hash(low, high)`.

###### Virtual functions <a id="locale.collate.virtuals">[[locale.collate.virtuals]]</a>

``` cpp
int do_compare(const charT* low1, const charT* high1,
               const charT* low2, const charT* high2) const;
```

*Returns:* `1` if the first string is greater than the second, `-1` if
less, zero otherwise. The specializations required in
[[locale.category.facets]][[locale.category]], namely `collate<char>`
and `collate<wchar_t>`, implement a lexicographical
comparison [[alg.lex.comparison]].

``` cpp
string_type do_transform(const charT* low, const charT* high) const;
```

*Returns:* A `basic_string<charT>` value that, compared
lexicographically with the result of calling `transform()` on another
string, yields the same result as calling `do_compare()` on the same two
strings.[^14]

``` cpp
long do_hash(const charT* low, const charT* high) const;
```

*Returns:* An integer value equal to the result of calling `hash()` on
any other string for which `do_compare()` returns 0 (equal) when passed
the two strings.

*Recommended practice:* The probability that the result equals that for
another string which does not compare equal should be very small,
approaching `(1.0/numeric_limits<unsigned long>::max())`.

##### Class template `collate_byname` <a id="locale.collate.byname">[[locale.collate.byname]]</a>

``` cpp
namespace std {
  template<class charT>
    class collate_byname : public collate<charT> {
    public:
      using string_type = basic_string<charT>;

      explicit collate_byname(const char*, size_t refs = 0);
      explicit collate_byname(const string&, size_t refs = 0);

    protected:
      ~collate_byname();
    };
}
```

#### The time category <a id="category.time">[[category.time]]</a>

##### General <a id="category.time.general">[[category.time.general]]</a>

Templates `time_get<charT, InputIterator>` and
`time_put<charT, OutputIterator>` provide date and time formatting and
parsing. All specifications of member functions for `time_put` and
`time_get` in the subclauses of  [[category.time]] only apply to the
specializations required in Tables  [[tab:locale.category.facets]] and 
[[tab:locale.spec]] [[locale.category]]. Their members use their
`ios_base&`, `ios_base::iostate&`, and `fill` arguments as described in 
[[locale.categories]], and the `ctype<>` facet, to determine formatting
details.

##### Class template `time_get` <a id="locale.time.get">[[locale.time.get]]</a>

###### General <a id="locale.time.get.general">[[locale.time.get.general]]</a>

``` cpp
namespace std {
  class time_base {
  public:
    enum dateorder { no_order, dmy, mdy, ymd, ydm };
  };

  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class time_get : public locale::facet, public time_base {
    public:
      using char_type = charT;
      using iter_type = InputIterator;

      explicit time_get(size_t refs = 0);

      dateorder date_order() const { return do_date_order(); }
      iter_type get_time(iter_type s, iter_type end, ios_base& f,
                         ios_base::iostate& err, tm* t) const;
      iter_type get_date(iter_type s, iter_type end, ios_base& f,
                         ios_base::iostate& err, tm* t) const;
      iter_type get_weekday(iter_type s, iter_type end, ios_base& f,
                            ios_base::iostate& err, tm* t) const;
      iter_type get_monthname(iter_type s, iter_type end, ios_base& f,
                              ios_base::iostate& err, tm* t) const;
      iter_type get_year(iter_type s, iter_type end, ios_base& f,
                         ios_base::iostate& err, tm* t) const;
      iter_type get(iter_type s, iter_type end, ios_base& f,
                    ios_base::iostate& err, tm* t, char format, char modifier = 0) const;
      iter_type get(iter_type s, iter_type end, ios_base& f,
                    ios_base::iostate& err, tm* t, const char_type* fmt,
                    const char_type* fmtend) const;

      static locale::id id;

    protected:
      ~time_get();
      virtual dateorder do_date_order() const;
      virtual iter_type do_get_time(iter_type s, iter_type end, ios_base&,
                                    ios_base::iostate& err, tm* t) const;
      virtual iter_type do_get_date(iter_type s, iter_type end, ios_base&,
                                    ios_base::iostate& err, tm* t) const;
      virtual iter_type do_get_weekday(iter_type s, iter_type end, ios_base&,
                                       ios_base::iostate& err, tm* t) const;
      virtual iter_type do_get_monthname(iter_type s, iter_type end, ios_base&,
                                         ios_base::iostate& err, tm* t) const;
      virtual iter_type do_get_year(iter_type s, iter_type end, ios_base&,
                                    ios_base::iostate& err, tm* t) const;
      virtual iter_type do_get(iter_type s, iter_type end, ios_base& f,
                               ios_base::iostate& err, tm* t, char format, char modifier) const;
    };
}
```

`time_get` is used to parse a character sequence, extracting components
of a time or date into a `tm` object. Each `get` member parses a format
as produced by a corresponding format specifier to `time_put<>::put`. If
the sequence being parsed matches the correct format, the corresponding
members of the `tm` argument are set to the values used to produce the
sequence; otherwise either an error is reported or unspecified values
are assigned.[^15]

If the end iterator is reached during parsing by any of the `get()`
member functions, the member sets `ios_base::eofbit` in `err`.

###### Members <a id="locale.time.get.members">[[locale.time.get.members]]</a>

``` cpp
dateorder date_order() const;
```

*Returns:* `do_date_order()`.

``` cpp
iter_type get_time(iter_type s, iter_type end, ios_base& str,
                   ios_base::iostate& err, tm* t) const;
```

*Returns:* `do_get_time(s, end, str, err, t)`.

``` cpp
iter_type get_date(iter_type s, iter_type end, ios_base& str,
                   ios_base::iostate& err, tm* t) const;
```

*Returns:* `do_get_date(s, end, str, err, t)`.

``` cpp
iter_type get_weekday(iter_type s, iter_type end, ios_base& str,
                      ios_base::iostate& err, tm* t) const;
iter_type get_monthname(iter_type s, iter_type end, ios_base& str,
                        ios_base::iostate& err, tm* t) const;
```

*Returns:* `do_get_weekday(s, end, str, err, t)` or
`do_get_monthname(s, end, str, err, t)`.

``` cpp
iter_type get_year(iter_type s, iter_type end, ios_base& str,
                   ios_base::iostate& err, tm* t) const;
```

*Returns:* `do_get_year(s, end, str, err, t)`.

``` cpp
iter_type get(iter_type s, iter_type end, ios_base& f, ios_base::iostate& err,
              tm* t, char format, char modifier = 0) const;
```

*Returns:* `do_get(s, end, f, err, t, format, modifier)`.

``` cpp
iter_type get(iter_type s, iter_type end, ios_base& f, ios_base::iostate& err,
              tm* t, const char_type* fmt, const char_type* fmtend) const;
```

*Preconditions:* \[`fmt`, `fmtend`) is a valid range.

*Effects:* The function starts by evaluating `err = ios_base::goodbit`.
It then enters a loop, reading zero or more characters from `s` at each
iteration. Unless otherwise specified below, the loop terminates when
the first of the following conditions holds:

- The expression `fmt == fmtend` evaluates to `true`.
- The expression `err == ios_base::goodbit` evaluates to `false`.
- The expression `s == end` evaluates to `true`, in which case the
  function evaluates `err = ios_base::eofbit | ios_base::failbit`.
- The next element of `fmt` is equal to `’%’`, optionally followed by a
  modifier character, followed by a conversion specifier character,
  `format`, together forming a conversion specification valid for the
  POSIX function `strptime`. If the number of elements in the range
  \[`fmt`, `fmtend`) is not sufficient to unambiguously determine
  whether the conversion specification is complete and valid, the
  function evaluates `err = ios_base::failbit`. Otherwise, the function
  evaluates `s = do_get(s, end, f, err, t, format, modifier)`, where the
  value of `modifier` is `’\0’` when the optional modifier is absent
  from the conversion specification. If `err == ios_base::goodbit` holds
  after the evaluation of the expression, the function increments `fmt`
  to point just past the end of the conversion specification and
  continues looping.
- The expression `isspace(*fmt, f.getloc())` evaluates to `true`, in
  which case the function first increments `fmt` until
  `fmt == fmtend || !isspace(*fmt, f.getloc())` evaluates to `true`,
  then advances `s` until `s == end || !isspace(*s, f.getloc())` is
  `true`, and finally resumes looping.
- The next character read from `s` matches the element pointed to by
  `fmt` in a case-insensitive comparison, in which case the function
  evaluates `++fmt, ++s` and continues looping. Otherwise, the function
  evaluates `err = ios_base::failbit`.

[*Note 1*: The function uses the `ctype<charT>` facet installed in
`f`’s locale to determine valid whitespace characters. It is unspecified
by what means the function performs case-insensitive comparison or
whether multi-character sequences are considered while doing
so. — *end note*]

*Returns:* `s`.

###### Virtual functions <a id="locale.time.get.virtuals">[[locale.time.get.virtuals]]</a>

``` cpp
dateorder do_date_order() const;
```

*Returns:* An enumeration value indicating the preferred order of
components for those date formats that are composed of day, month, and
year.[^16]

Returns `no_order` if the date format specified by `’x’` contains other
variable components (e.g., Julian day, week number, week day).

``` cpp
iter_type do_get_time(iter_type s, iter_type end, ios_base& str,
                      ios_base::iostate& err, tm* t) const;
```

*Effects:* Reads characters starting at `s` until it has extracted those
`tm` members, and remaining format characters, used by `time_put<>::put`
to produce the format specified by `"%H:%M:%S"`, or until it encounters
an error or end of sequence.

*Returns:* An iterator pointing immediately beyond the last character
recognized as possibly part of a valid time.

``` cpp
iter_type do_get_date(iter_type s, iter_type end, ios_base& str,
                      ios_base::iostate& err, tm* t) const;
```

*Effects:* Reads characters starting at `s` until it has extracted those
`tm` members and remaining format characters used by `time_put<>::put`
to produce one of the following formats, or until it encounters an
error. The format depends on the value returned by `date_order()` as
shown in [[locale.time.get.dogetdate]].

**Table: `do_get_date` effects**

| `date_order()` | Format     |
| -------------- | ---------- |
| `no_order`     | `"%m%d%y"` |
| `dmy`          | `"%d%m%y"` |
| `mdy`          | `"%m%d%y"` |
| `ymd`          | `"%y%m%d"` |
| `ydm`          | `"%y%d%m"` |


An implementation may also accept additional *implementation-defined*
formats.

*Returns:* An iterator pointing immediately beyond the last character
recognized as possibly part of a valid date.

``` cpp
iter_type do_get_weekday(iter_type s, iter_type end, ios_base& str,
                         ios_base::iostate& err, tm* t) const;
iter_type do_get_monthname(iter_type s, iter_type end, ios_base& str,
                           ios_base::iostate& err, tm* t) const;
```

*Effects:* Reads characters starting at `s` until it has extracted the
(perhaps abbreviated) name of a weekday or month. If it finds an
abbreviation that is followed by characters that can match a full name,
it continues reading until it matches the full name or fails. It sets
the appropriate `tm` member accordingly.

*Returns:* An iterator pointing immediately beyond the last character
recognized as part of a valid name.

``` cpp
iter_type do_get_year(iter_type s, iter_type end, ios_base& str,
                      ios_base::iostate& err, tm* t) const;
```

*Effects:* Reads characters starting at `s` until it has extracted an
unambiguous year identifier. It is *implementation-defined* whether
two-digit year numbers are accepted, and (if so) what century they are
assumed to lie in. Sets the `t->tm_year` member accordingly.

*Returns:* An iterator pointing immediately beyond the last character
recognized as part of a valid year identifier.

``` cpp
iter_type do_get(iter_type s, iter_type end, ios_base& f,
                 ios_base::iostate& err, tm* t, char format, char modifier) const;
```

*Preconditions:* `t` points to an object.

*Effects:* The function starts by evaluating `err = ios_base::goodbit`.
It then reads characters starting at `s` until it encounters an error,
or until it has extracted and assigned those `tm` members, and any
remaining format characters, corresponding to a conversion specification
appropriate for the POSIX function `strptime`, formed by concatenating
`’%’`, the `modifier` character, when non-NUL, and the `format`
character. When the concatenation fails to yield a complete valid
directive the function leaves the object pointed to by `t` unchanged and
evaluates `err |= ios_base::failbit`. When `s == end` evaluates to
`true` after reading a character the function evaluates
`err |= ios_base::eofbit`.

For complex conversion specifications such as `%c`, `%x`, or `%X`, or
conversion specifications that involve the optional modifiers `E` or
`O`, when the function is unable to unambiguously determine some or all
`tm` members from the input sequence \[`s`, `end`), it evaluates
`err |= ios_base::eofbit`. In such cases the values of those `tm`
members are unspecified and may be outside their valid range.

*Returns:* An iterator pointing immediately beyond the last character
recognized as possibly part of a valid input sequence for the given
`format` and `modifier`.

*Remarks:* It is unspecified whether multiple calls to `do_get()` with
the address of the same `tm` object will update the current contents of
the object or simply overwrite its members. Portable programs should
zero out the object before invoking the function.

##### Class template `time_get_byname` <a id="locale.time.get.byname">[[locale.time.get.byname]]</a>

``` cpp
namespace std {
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class time_get_byname : public time_get<charT, InputIterator> {
    public:
      using dateorder = time_base::dateorder;
      using iter_type = InputIterator;

      explicit time_get_byname(const char*, size_t refs = 0);
      explicit time_get_byname(const string&, size_t refs = 0);

    protected:
      ~time_get_byname();
    };
}
```

##### Class template `time_put` <a id="locale.time.put">[[locale.time.put]]</a>

###### General <a id="locale.time.put.general">[[locale.time.put.general]]</a>

``` cpp
namespace std {
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class time_put : public locale::facet {
    public:
      using char_type = charT;
      using iter_type = OutputIterator;

      explicit time_put(size_t refs = 0);

      // the following is implemented in terms of other member functions.
      iter_type put(iter_type s, ios_base& f, char_type fill, const tm* tmb,
                    const charT* pattern, const charT* pat_end) const;
      iter_type put(iter_type s, ios_base& f, char_type fill,
                    const tm* tmb, char format, char modifier = 0) const;

      static locale::id id;

    protected:
      ~time_put();
      virtual iter_type do_put(iter_type s, ios_base&, char_type, const tm* t,
                               char format, char modifier) const;
    };
}
```

###### Members <a id="locale.time.put.members">[[locale.time.put.members]]</a>

``` cpp
iter_type put(iter_type s, ios_base& str, char_type fill, const tm* t,
              const charT* pattern, const charT* pat_end) const;
iter_type put(iter_type s, ios_base& str, char_type fill, const tm* t,
              char format, char modifier = 0) const;
```

*Effects:* The first form steps through the sequence from `pattern` to
`pat_end`, identifying characters that are part of a format sequence.
Each character that is not part of a format sequence is written to `s`
immediately, and each format sequence, as it is identified, results in a
call to `do_put`; thus, format elements and other characters are
interleaved in the output in the order in which they appear in the
pattern. Format sequences are identified by converting each character
`c` to a `char` value as if by `ct.narrow(c, 0)`, where `ct` is a
reference to `ctype<charT>` obtained from `str.getloc()`. The first
character of each sequence is equal to `’%’`, followed by an optional
modifier character `mod` and a format specifier character `spec` as
defined for the function `strftime`. If no modifier character is
present, `mod` is zero. For each valid format sequence identified, calls
`do_put(s, str, fill, t, spec, mod)`.

The second form calls `do_put(s, str, fill, t, format, modifier)`.

[*Note 2*: The `fill` argument can be used in the
implementation-defined formats or by derivations. A space character is a
reasonable default for this argument. — *end note*]

*Returns:* An iterator pointing immediately after the last character
produced.

###### Virtual functions <a id="locale.time.put.virtuals">[[locale.time.put.virtuals]]</a>

``` cpp
iter_type do_put(iter_type s, ios_base&, char_type fill, const tm* t,
                 char format, char modifier) const;
```

*Effects:* Formats the contents of the parameter `t` into characters
placed on the output sequence `s`. Formatting is controlled by the
parameters `format` and `modifier`, interpreted identically as the
format specifiers in the string argument to the standard library
function `strftime()`, except that the sequence of characters produced
for those specifiers that are described as depending on the C locale are
instead *implementation-defined*.

[*Note 3*: Interpretation of the `modifier` argument is
implementation-defined. — *end note*]

*Returns:* An iterator pointing immediately after the last character
produced.

[*Note 4*: The `fill` argument can be used in the
implementation-defined formats or by derivations. A space character is a
reasonable default for this argument. — *end note*]

*Recommended practice:* Interpretation of the `modifier` should follow
POSIX conventions. Implementations should refer to other standards such
as POSIX for a specification of the character sequences produced for
those specifiers described as depending on the C locale.

##### Class template `time_put_byname` <a id="locale.time.put.byname">[[locale.time.put.byname]]</a>

``` cpp
namespace std {
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class time_put_byname : public time_put<charT, OutputIterator> {
    public:
      using char_type = charT;
      using iter_type = OutputIterator;

      explicit time_put_byname(const char*, size_t refs = 0);
      explicit time_put_byname(const string&, size_t refs = 0);

    protected:
      ~time_put_byname();
    };
}
```

#### The monetary category <a id="category.monetary">[[category.monetary]]</a>

##### General <a id="category.monetary.general">[[category.monetary.general]]</a>

These templates handle monetary formats. A template parameter indicates
whether local or international monetary formats are to be used.

All specifications of member functions for `money_put` and `money_get`
in the subclauses of  [[category.monetary]] only apply to the
specializations required in Tables  [[tab:locale.category.facets]] and 
[[tab:locale.spec]] [[locale.category]]. Their members use their
`ios_base&`, `ios_base::iostate&`, and `fill` arguments as described in 
[[locale.categories]], and the `moneypunct<>` and `ctype<>` facets, to
determine formatting details.

##### Class template `money_get` <a id="locale.money.get">[[locale.money.get]]</a>

###### General <a id="locale.money.get.general">[[locale.money.get.general]]</a>

``` cpp
namespace std {
  template<class charT, class InputIterator = istreambuf_iterator<charT>>
    class money_get : public locale::facet {
    public:
      using char_type   = charT;
      using iter_type   = InputIterator;
      using string_type = basic_string<charT>;

      explicit money_get(size_t refs = 0);

      iter_type get(iter_type s, iter_type end, bool intl,
                    ios_base& f, ios_base::iostate& err,
                    long double& units) const;
      iter_type get(iter_type s, iter_type end, bool intl,
                    ios_base& f, ios_base::iostate& err,
                    string_type& digits) const;

      static locale::id id;

    protected:
      ~money_get();
      virtual iter_type do_get(iter_type, iter_type, bool, ios_base&,
                               ios_base::iostate& err, long double& units) const;
      virtual iter_type do_get(iter_type, iter_type, bool, ios_base&,
                               ios_base::iostate& err, string_type& digits) const;
    };
}
```

###### Members <a id="locale.money.get.members">[[locale.money.get.members]]</a>

``` cpp
iter_type get(iter_type s, iter_type end, bool intl, ios_base& f,
              ios_base::iostate& err, long double& quant) const;
iter_type get(iter_type s, iter_type end, bool intl, ios_base& f,
              ios_base::iostate& err, string_type& quant) const;
```

*Returns:* `do_get(s, end, intl, f, err, quant)`.

###### Virtual functions <a id="locale.money.get.virtuals">[[locale.money.get.virtuals]]</a>

``` cpp
iter_type do_get(iter_type s, iter_type end, bool intl, ios_base& str,
                 ios_base::iostate& err, long double& units) const;
iter_type do_get(iter_type s, iter_type end, bool intl, ios_base& str,
                 ios_base::iostate& err, string_type& digits) const;
```

*Effects:* Reads characters from `s` to parse and construct a monetary
value according to the format specified by a `moneypunct<charT, Intl>`
facet reference `mp` and the character mapping specified by a
`ctype<charT>` facet reference `ct` obtained from the locale returned by
`str.getloc()`, and `str.flags()`. If a valid sequence is recognized,
does not change `err`; otherwise, sets `err` to `(err | str.failbit)`,
or `(err | str.failbit | str.eofbit)` if no more characters are
available, and does not change `units` or `digits`. Uses the pattern
returned by `mp.neg_format()` to parse all values. The result is
returned as an integral value stored in `units` or as a sequence of
digits possibly preceded by a minus sign (as produced by `ct.widen(c)`
where `c` is `’-’` or in the range from `’0’` through `’9’` (inclusive))
stored in `digits`.

[*Example 1*: The sequence `$1,056.23` in a common United States locale
would yield, for `units`, `105623`, or, for `digits`,
`"105623"`. — *end example*]

If `mp.grouping()` indicates that no thousands separators are permitted,
any such characters are not read, and parsing is terminated at the point
where they first appear. Otherwise, thousands separators are optional;
if present, they are checked for correct placement only after all format
components have been read.

Where `money_base::space` or `money_base::none` appears as the last
element in the format pattern, no whitespace is consumed. Otherwise,
where `money_base::space` appears in any of the initial elements of the
format pattern, at least one whitespace character is required. Where
`money_base::none` appears in any of the initial elements of the format
pattern, whitespace is allowed but not required. If
`(str.flags() & str.showbase)` is `false`, the currency symbol is
optional and is consumed only if other characters are needed to complete
the format; otherwise, the currency symbol is required.

If the first character (if any) in the string `pos` returned by
`mp.positive_sign()` or the string `neg` returned by
`mp.negative_sign()` is recognized in the position indicated by `sign`
in the format pattern, it is consumed and any remaining characters in
the string are required after all the other format components.

[*Example 2*: If `showbase` is off, then for a `neg` value of `"()"`
and a currency symbol of `"L"`, in `"(100 L)"` the `"L"` is consumed;
but if `neg` is `"-"`, the `"L"` in `"-100 L"` is not
consumed. — *end example*]

If `pos` or `neg` is empty, the sign component is optional, and if no
sign is detected, the result is given the sign that corresponds to the
source of the empty string. Otherwise, the character in the indicated
position must match the first character of `pos` or `neg`, and the
result is given the corresponding sign. If the first character of `pos`
is equal to the first character of `neg`, or if both strings are empty,
the result is given a positive sign.

Digits in the numeric monetary component are extracted and placed in
`digits`, or into a character buffer `buf1` for conversion to produce a
value for `units`, in the order in which they appear, preceded by a
minus sign if and only if the result is negative. The value `units` is
produced as if by[^17]

``` cpp
for (int i = 0; i < n; ++i)
  buf2[i] = src[find(atoms, atoms + sizeof(src), buf1[i]) - atoms];
buf2[n] = 0;
sscanf(buf2, "%Lf", &units);
```

where `n` is the number of characters placed in `buf1`, `buf2` is a
character buffer, and the values `src` and `atoms` are defined as if by

``` cpp
static const char src[] = "0123456789-";
charT atoms[sizeof(src)];
ct.widen(src, src + sizeof(src) - 1, atoms);
```

*Returns:* An iterator pointing immediately beyond the last character
recognized as part of a valid monetary quantity.

##### Class template `money_put` <a id="locale.money.put">[[locale.money.put]]</a>

###### General <a id="locale.money.put.general">[[locale.money.put.general]]</a>

``` cpp
namespace std {
  template<class charT, class OutputIterator = ostreambuf_iterator<charT>>
    class money_put : public locale::facet {
    public:
      using char_type   = charT;
      using iter_type   = OutputIterator;
      using string_type = basic_string<charT>;

      explicit money_put(size_t refs = 0);

      iter_type put(iter_type s, bool intl, ios_base& f,
                    char_type fill, long double units) const;
      iter_type put(iter_type s, bool intl, ios_base& f,
                    char_type fill, const string_type& digits) const;

      static locale::id id;

    protected:
      ~money_put();
      virtual iter_type do_put(iter_type, bool, ios_base&, char_type fill,
                               long double units) const;
      virtual iter_type do_put(iter_type, bool, ios_base&, char_type fill,
                               const string_type& digits) const;
    };
}
```

###### Members <a id="locale.money.put.members">[[locale.money.put.members]]</a>

``` cpp
iter_type put(iter_type s, bool intl, ios_base& f, char_type fill, long double quant) const;
iter_type put(iter_type s, bool intl, ios_base& f, char_type fill, const string_type& quant) const;
```

*Returns:* `do_put(s, intl, f, fill, quant)`.

###### Virtual functions <a id="locale.money.put.virtuals">[[locale.money.put.virtuals]]</a>

``` cpp
iter_type do_put(iter_type s, bool intl, ios_base& str,
                 char_type fill, long double units) const;
iter_type do_put(iter_type s, bool intl, ios_base& str,
                 char_type fill, const string_type& digits) const;
```

*Effects:* Writes characters to `s` according to the format specified by
a `moneypunct<charT, Intl>` facet reference `mp` and the character
mapping specified by a `ctype<charT>` facet reference `ct` obtained from
the locale returned by `str.getloc()`, and `str.flags()`. The argument
`units` is transformed into a sequence of wide characters as if by

``` cpp
ct.widen(buf1, buf1 + sprintf(buf1, "%.0Lf", units), buf2)
```

for character buffers `buf1` and `buf2`. If the first character in
`digits` or `buf2` is equal to `ct.widen(’-’)`, then the pattern used
for formatting is the result of `mp.neg_format()`; otherwise the pattern
is the result of `mp.pos_format()`. Digit characters are written,
interspersed with any thousands separators and decimal point specified
by the format, in the order they appear (after the optional leading
minus sign) in `digits` or `buf2`. In `digits`, only the optional
leading minus sign and the immediately subsequent digit characters (as
classified according to `ct`) are used; any trailing characters
(including digits appearing after a non-digit character) are ignored.
Calls `str.width(0)`.

*Returns:* An iterator pointing immediately after the last character
produced.

*Remarks:* The currency symbol is generated if and only if
`(str.flags() & str.showbase)` is nonzero. If the number of characters
generated for the specified format is less than the value returned by
`str.width()` on entry to the function, then copies of `fill` are
inserted as necessary to pad to the specified width. For the value `af`
equal to `(str.flags() & str.adjustfield)`, if `(af == str.internal)` is
`true`, the fill characters are placed where `none` or `space` appears
in the formatting pattern; otherwise if `(af == str.left)` is `true`,
they are placed after the other characters; otherwise, they are placed
before the other characters.

[*Note 1*: It is possible, with some combinations of format patterns
and flag values, to produce output that cannot be parsed using
`num_get<>::get`. — *end note*]

##### Class template `moneypunct` <a id="locale.moneypunct">[[locale.moneypunct]]</a>

###### General <a id="locale.moneypunct.general">[[locale.moneypunct.general]]</a>

``` cpp
namespace std {
  class money_base {
  public:
    enum part { none, space, symbol, sign, value };
    struct pattern { char field[4]; };
  };

  template<class charT, bool International = false>
    class moneypunct : public locale::facet, public money_base {
    public:
      using char_type   = charT;
      using string_type = basic_string<charT>;

      explicit moneypunct(size_t refs = 0);

      charT       decimal_point() const;
      charT       thousands_sep() const;
      string      grouping()      const;
      string_type curr_symbol()   const;
      string_type positive_sign() const;
      string_type negative_sign() const;
      int         frac_digits()   const;
      pattern     pos_format()    const;
      pattern     neg_format()    const;

      static locale::id id;
      static const bool intl = International;

    protected:
      ~moneypunct();
      virtual charT       do_decimal_point() const;
      virtual charT       do_thousands_sep() const;
      virtual string      do_grouping()      const;
      virtual string_type do_curr_symbol()   const;
      virtual string_type do_positive_sign() const;
      virtual string_type do_negative_sign() const;
      virtual int         do_frac_digits()   const;
      virtual pattern     do_pos_format()    const;
      virtual pattern     do_neg_format()    const;
    };
}
```

The `moneypunct<>` facet defines monetary formatting parameters used by
`money_get<>` and `money_put<>`. A monetary format is a sequence of four
components, specified by a `pattern` value `p`, such that the `part`
value `static_cast<part>(p.field[i])` determines the `i`^\text{th}
component of the format.[^18]

In the `field` member of a `pattern` object, each value `symbol`,
`sign`, `value`, and either `space` or `none` appears exactly once. The
value `none`, if present, is not first; the value `space`, if present,
is neither first nor last.

Where `none` or `space` appears, whitespace is permitted in the format,
except where `none` appears at the end, in which case no whitespace is
permitted. The value `space` indicates that at least one space is
required at that position. Where `symbol` appears, the sequence of
characters returned by `curr_symbol()` is permitted, and can be
required. Where `sign` appears, the first (if any) of the sequence of
characters returned by `positive_sign()` or `negative_sign()`
(respectively as the monetary value is non-negative or negative) is
required. Any remaining characters of the sign sequence are required
after all other format components. Where `value` appears, the absolute
numeric monetary value is required.

The format of the numeric monetary value is a decimal number:

``` bnf
{\BnfNontermshape value\itcorr}:
    units fractionalₒₚₜ
    decimal-point digits
```

``` bnf
{\BnfNontermshape fractional\itcorr}:
    decimal-point digitsₒₚₜ
```

if `frac_digits()` returns a positive value, or

``` bnf
{\BnfNontermshape value\itcorr}:
    units
```

otherwise. The symbol indicates the character returned by
`decimal_point()`. The other symbols are defined as follows:

``` bnf
{\BnfNontermshape units\itcorr}:
    digits
    digits thousands-sep units
```

``` bnf
{\BnfNontermshape digits\itcorr}:
    adigit digitsₒₚₜ
```

In the syntax specification, the symbol is any of the values
`ct.widen(c)` for `c` in the range `'0'` through `'9'` (inclusive) and
`ct` is a reference of type `const ctype<charT>&` obtained as described
in the definitions of `money_get<>` and `money_put<>`. The symbol is the
character returned by `thousands_sep()`. The space character used is the
value `ct.widen(' ')`. Whitespace characters are those characters `c`
for which `ci.is(space, c)` returns `true`. The number of digits
required after the decimal point (if any) is exactly the value returned
by `frac_digits()`.

The placement of thousands-separator characters (if any) is determined
by the value returned by `grouping()`, defined identically as the member
`numpunct<>::do_grouping()`.

###### Members <a id="locale.moneypunct.members">[[locale.moneypunct.members]]</a>

``` cpp
charT       decimal_point() const;
charT       thousands_sep() const;
string      grouping()      const;
string_type curr_symbol()   const;
string_type positive_sign() const;
string_type negative_sign() const;
int         frac_digits()   const;
pattern     pos_format()    const;
pattern     neg_format()    const;
```

Each of these functions `F` returns the result of calling the
corresponding virtual member function `do_F()`.

###### Virtual functions <a id="locale.moneypunct.virtuals">[[locale.moneypunct.virtuals]]</a>

``` cpp
charT do_decimal_point() const;
```

*Returns:* The radix separator to use in case `do_frac_digits()` is
greater than zero.[^19]

``` cpp
charT do_thousands_sep() const;
```

*Returns:* The digit group separator to use in case `do_grouping()`
specifies a digit grouping pattern.[^20]

``` cpp
string do_grouping() const;
```

*Returns:* A pattern defined identically as, but not necessarily equal
to, the result of `numpunct<charT>::do_grouping()`.[^21]

``` cpp
string_type do_curr_symbol() const;
```

*Returns:* A string to use as the currency identifier symbol.

[*Note 2*: For specializations where the second template parameter is
`true`, this is typically four characters long: a three-letter code as
specified by ISO 4217 followed by a space. — *end note*]

``` cpp
string_type do_positive_sign() const;
string_type do_negative_sign() const;
```

*Returns:* `do_positive_sign()` returns the string to use to indicate a
positive monetary value;[^22]

`do_negative_sign()` returns the string to use to indicate a negative
value.

``` cpp
int do_frac_digits() const;
```

*Returns:* The number of digits after the decimal radix separator, if
any.[^23]

``` cpp
pattern do_pos_format() const;
pattern do_neg_format() const;
```

*Returns:* The specializations required in
[[locale.spec]][[locale.category]], namely

- `moneypunct<char>`,
- `moneypunct<wchar_t>`,
- `moneypunct<char, true>`, and
- `moneypunct<wchar_t, true>`,

return an object of type `pattern` initialized to
`{ symbol, sign, none, value }`.[^24]

##### Class template `moneypunct_byname` <a id="locale.moneypunct.byname">[[locale.moneypunct.byname]]</a>

``` cpp
namespace std {
  template<class charT, bool Intl = false>
    class moneypunct_byname : public moneypunct<charT, Intl> {
    public:
      using pattern     = money_base::pattern;
      using string_type = basic_string<charT>;

      explicit moneypunct_byname(const char*, size_t refs = 0);
      explicit moneypunct_byname(const string&, size_t refs = 0);

    protected:
      ~moneypunct_byname();
    };
}
```

#### The message retrieval category <a id="category.messages">[[category.messages]]</a>

##### General <a id="category.messages.general">[[category.messages.general]]</a>

Class `messages<charT>` implements retrieval of strings from message
catalogs.

##### Class template `messages` <a id="locale.messages">[[locale.messages]]</a>

###### General <a id="locale.messages.general">[[locale.messages.general]]</a>

``` cpp
namespace std {
  class messages_base {
  public:
    using catalog = unspecified signed integer type;
  };

  template<class charT>
    class messages : public locale::facet, public messages_base {
    public:
      using char_type   = charT;
      using string_type = basic_string<charT>;

      explicit messages(size_t refs = 0);

      catalog open(const string& fn, const locale&) const;
      string_type get(catalog c, int set, int msgid,
                      const string_type& dfault) const;
      void close(catalog c) const;

      static locale::id id;

    protected:
      ~messages();
      virtual catalog do_open(const string&, const locale&) const;
      virtual string_type do_get(catalog, int set, int msgid,
                                 const string_type& dfault) const;
      virtual void do_close(catalog) const;
    };
}
```

Values of type `messages_base::catalog` usable as arguments to members
`get` and `close` can be obtained only by calling member `open`.

###### Members <a id="locale.messages.members">[[locale.messages.members]]</a>

``` cpp
catalog open(const string& name, const locale& loc) const;
```

*Returns:* `do_open(name, loc)`.

``` cpp
string_type get(catalog cat, int set, int msgid, const string_type& dfault) const;
```

*Returns:* `do_get(cat, set, msgid, dfault)`.

``` cpp
void close(catalog cat) const;
```

*Effects:* Calls `do_close(cat)`.

###### Virtual functions <a id="locale.messages.virtuals">[[locale.messages.virtuals]]</a>

``` cpp
catalog do_open(const string& name, const locale& loc) const;
```

*Returns:* A value that may be passed to `get()` to retrieve a message
from the message catalog identified by the string `name` according to an
*implementation-defined* mapping. The result can be used until it is
passed to `close()`.

Returns a value less than 0 if no such catalog can be opened.

*Remarks:* The locale argument `loc` is used for character set code
conversion when retrieving messages, if needed.

``` cpp
string_type do_get(catalog cat, int set, int msgid, const string_type& dfault) const;
```

*Preconditions:* `cat` is a catalog obtained from `open()` and not yet
closed.

*Returns:* A message identified by arguments `set`, `msgid`, and
`dfault`, according to an *implementation-defined* mapping. If no such
message can be found, returns `dfault`.

``` cpp
void do_close(catalog cat) const;
```

*Preconditions:* `cat` is a catalog obtained from `open()` and not yet
closed.

*Effects:* Releases unspecified resources associated with `cat`.

*Remarks:* The limit on such resources, if any, is
*implementation-defined*.

##### Class template `messages_byname` <a id="locale.messages.byname">[[locale.messages.byname]]</a>

``` cpp
namespace std {
  template<class charT>
    class messages_byname : public messages<charT> {
    public:
      using catalog     = messages_base::catalog;
      using string_type = basic_string<charT>;

      explicit messages_byname(const char*, size_t refs = 0);
      explicit messages_byname(const string&, size_t refs = 0);

    protected:
      ~messages_byname();
    };
}
```

### C library locales <a id="c.locales">[[c.locales]]</a>

#### Header `<clocale>` synopsis <a id="clocale.syn">[[clocale.syn]]</a>

``` cpp
namespace std {
  struct lconv;

  char* setlocale(int category, const char* locale);
  lconv* localeconv();
}

#define \libmacro{NULL} see [support.types.nullptr]
#define \libmacro{LC_ALL} see below
#define \libmacro{LC_COLLATE} see below
#define \libmacro{LC_CTYPE} see below
#define \libmacro{LC_MONETARY} see below
#define \libmacro{LC_NUMERIC} see below
#define \libmacro{LC_TIME} see below
```

The contents and meaning of the header `<clocale>` are the same as the C
standard library header `<locale.h>`.

#### Data races <a id="clocale.data.races">[[clocale.data.races]]</a>

Calls to the function `setlocale` may introduce a data race
[[res.on.data.races]] with other calls to `setlocale` or with calls to
the functions listed in [[setlocale.data.races]].

**Table: Potential `setlocale` data races**

|           |            |             |              |            |
| --------- | ---------- | ----------- | ------------ | ---------- |
| `fprintf` | `isprint`  | `iswdigit`  | `localeconv` | `tolower`  |
| `fscanf`  | `ispunct`  | `iswgraph`  | `mblen`      | `toupper`  |
| `isalnum` | `isspace`  | `iswlower`  | `mbstowcs`   | `towlower` |
| `isalpha` | `isupper`  | `iswprint`  | `mbtowc`     | `towupper` |
| `isblank` | `iswalnum` | `iswpunct`  | `setlocale`  | `wcscoll`  |
| `iscntrl` | `iswalpha` | `iswspace`  | `strcoll`    | `wcstod`   |
| `isdigit` | `iswblank` | `iswupper`  | `strerror`   | `wcstombs` |
| `isgraph` | `iswcntrl` | `iswxdigit` | `strtod`     | `wcsxfrm`  |
| `islower` | `iswctype` | `isxdigit`  | `strxfrm`    | `wctomb`   |


## Text encodings identification <a id="text.encoding">[[text.encoding]]</a>

### Header `<text_encoding>` synopsis <a id="text.encoding.syn">[[text.encoding.syn]]</a>

``` cpp
namespace std {
  struct text_encoding;

  // [text.encoding.hash], hash support
  template<class T> struct hash;
  template<> struct hash<text_encoding>;
}
```

### Class `text_encoding` <a id="text.encoding.class">[[text.encoding.class]]</a>

#### Overview <a id="text.encoding.overview">[[text.encoding.overview]]</a>

The class `text_encoding` describes an interface for accessing the IANA
Character Sets registry.

``` cpp
namespace std {
  struct text_encoding {
    static constexpr size_t max_name_length = 63;

    // [text.encoding.id], enumeration text_encoding::id
    enum class id : int_least32_t {
      see below
    };
    using enum id;

    constexpr text_encoding() = default;
    constexpr explicit text_encoding(string_view enc) noexcept;
    constexpr text_encoding(id i) noexcept;

    constexpr id mib() const noexcept;
    constexpr const char* name() const noexcept;

    // [text.encoding.aliases], class text_encoding::aliases_view
    struct aliases_view;
    constexpr aliases_view aliases() const noexcept;

    friend constexpr bool operator==(const text_encoding& a,
                                     const text_encoding& b) noexcept;
    friend constexpr bool operator==(const text_encoding& encoding, id i) noexcept;

    static consteval text_encoding literal() noexcept;
    static text_encoding environment();
    template<id i> static bool environment_is();

  private:
    id mib_ = id::unknown;                                              // exposition only
    char name_[max_name_length + 1] = {0};                              // exposition only
    static constexpr bool comp-name(string_view a, string_view b);      // exposition only
  };
}
```

Class `text_encoding` is a trivially copyable type
[[term.trivially.copyable.type]].

#### General <a id="text.encoding.general">[[text.encoding.general]]</a>

A *registered character encoding* is a character encoding scheme in the
IANA Character Sets registry.

[*Note 1*: The IANA Character Sets registry uses the term “character
sets” to refer to character encodings. — *end note*]

The primary name of a registered character encoding is the name of that
encoding specified in the IANA Character Sets registry.

The set of known registered character encodings contains every
registered character encoding specified in the IANA Character Sets
registry except for the following:

- NATS-DANO (33)
- NATS-DANO-ADD (34)

Each known registered character encoding is identified by an enumerator
in `text_encoding::id`, and has a set of zero or more *aliases*.

The set of aliases of a known registered character encoding is an
*implementation-defined* superset of the aliases specified in the IANA
Character Sets registry. The set of aliases for US-ASCII includes
“ASCII”. No two aliases or primary names of distinct registered
character encodings are equivalent when compared by
`text_encoding::comp-name`.

How a `text_encoding` object is determined to be representative of a
character encoding scheme implemented in the translation or execution
environment is *implementation-defined*.

An object `e` of type `text_encoding` such that
`e.mib() == text_encoding::id::unknown` is `false` and
`e.mib() == text_encoding::id::other` is `false` maintains the following
invariants:

- `*e.name() == '\0'` is `false`, and
- `e.mib() == text_encoding(e.name()).mib()` is `true`.

*Recommended practice:*

- Implementations should not consider registered encodings to be
  interchangeable. \[*Example 2*: Shift_JIS and Windows-31J denote
  different encodings. — *end example*]
- Implementations should not use the name of a registered encoding to
  describe another similar yet different non-registered encoding unless
  there is a precedent on that implementation.
  \[*Example 3*: Big5 — *end example*]

#### Members <a id="text.encoding.members">[[text.encoding.members]]</a>

``` cpp
constexpr explicit text_encoding(string_view enc) noexcept;
```

*Preconditions:*

- `enc` represents a string in the ordinary literal encoding consisting
  only of elements of the basic character set [[lex.charset]].
- `enc.size() <= max_name_length` is `true`.
- `enc.contains(’\0’)` is `false`.

*Ensures:*

- If there exists a primary name or alias `a` of a known registered
  character encoding such that *`comp-name`*`(a, enc)` is `true`,
  *mib\_* has the value of the enumerator of `id` associated with that
  registered character encoding. Otherwise, *`mib_`*` == id::other` is
  `true`.
- `enc.compare(`*`name_`*`) == 0` is `true`.

``` cpp
constexpr text_encoding(id i) noexcept;
```

*Preconditions:* `i` has the value of one of the enumerators of `id`.

*Ensures:*

- *`mib_`*` == i` is `true`.
- If `(`*`mib_`*` == id::unknown || `*`mib_`*` == id::other)` is `true`,
  `strlen(`*`name_`*`) == 0` is `true`. Otherwise,
  `ranges::contains(aliases(), string_view(`*`name_`*`))` is `true`.

``` cpp
constexpr id mib() const noexcept;
```

*Returns:* *mib\_*.

``` cpp
constexpr const char* name() const noexcept;
```

*Returns:* *name\_*.

*Remarks:* `name()` is an NTBS and accessing elements of *name\_*
outside of the range `name()`+\[0, `strlen(name()) + 1`) is undefined
behavior.

``` cpp
constexpr aliases_view aliases() const noexcept;
```

Let `r` denote an instance of `aliases_view`. If `*this` represents a
known registered character encoding, then:

- `r.front()` is the primary name of the registered character encoding,
- `r` contains the aliases of the registered character encoding, and
- `r` does not contain duplicate values when compared with `strcmp`.

Otherwise, `r` is an empty range.

Each element in `r` is a non-null, non-empty NTBS encoded in the literal
character encoding and comprising only characters from the basic
character set.

*Returns:* `r`.

[*Note 1*: The order of aliases in `r` is unspecified. — *end note*]

``` cpp
static consteval text_encoding literal() noexcept;
```

*Mandates:* `CHAR_BIT == 8` is `true`.

*Returns:* A `text_encoding` object representing the ordinary character
literal encoding [[lex.charset]].

``` cpp
static text_encoding environment();
```

*Mandates:* `CHAR_BIT == 8` is `true`.

*Returns:* A `text_encoding` object representing the
*implementation-defined* character encoding scheme of the environment.
On a POSIX implementation, this is the encoding scheme associated with
the POSIX locale denoted by the empty string `""`.

[*Note 2*: This function is not affected by calls to
`setlocale`. — *end note*]

*Recommended practice:* Implementations should return a value that is
not affected by calls to the POSIX function `setenv` and other functions
which can modify the environment [[support.runtime]].

``` cpp
template<id i>
  static bool environment_is();
```

*Mandates:* `CHAR_BIT == 8` is `true`.

*Returns:* `environment() == i`.

``` cpp
static constexpr bool comp-name(string_view a, string_view b);
```

*Returns:* `true` if the two strings `a` and `b` encoded in the ordinary
literal encoding are equal, ignoring, from left-to-right,

- all elements that are not digits or letters [[character.seq.general]],
- character case, and
- any sequence of one or more `0` characters not immediately preceded by
  a numeric prefix, where a numeric prefix is a sequence consisting of a
  digit in the range \[`1`, `9`\] optionally followed by one or more
  elements which are not digits or letters,

and `false` otherwise.

[*Note 3*: This comparison is identical to the “Charset Alias Matching”
algorithm described in the Unicode Technical Standard 22. — *end note*]

[*Example 1*:

``` cpp
static_assert(comp-name("UTF-8", "utf8") == true);
static_assert(comp-name("u.t.f-008", "utf8") == true);
static_assert(comp-name("ut8", "utf8") == false);
static_assert(comp-name("utf-80", "utf8") == false);
```

— *end example*]

#### Comparison functions <a id="text.encoding.cmp">[[text.encoding.cmp]]</a>

``` cpp
friend constexpr bool operator==(const text_encoding& a, const text_encoding& b) noexcept;
```

*Returns:* If `a.`*`mib_`*` == id::other && b.`*`mib_`*` == id::other`
is `true`, then *`comp-name`*`(a.`*`name_`*`,b.`*`name_`*`)`. Otherwise,
`a.`*`mib_`*` == b.`*`mib_`*.

``` cpp
friend constexpr bool operator==(const text_encoding& encoding, id i) noexcept;
```

*Returns:* `encoding.`*`mib_`*` == i`.

*Remarks:* This operator induces an equivalence relation on its
arguments if and only if `i != id::other` is `true`.

#### Class `text_encoding::aliases_view` <a id="text.encoding.aliases">[[text.encoding.aliases]]</a>

``` cpp
struct text_encoding::aliases_view : ranges::view_interface<text_encoding::aliases_view> {
  constexpr implementation-defined  // type of text_encoding::aliases_view::begin() begin() const;
  constexpr implementation-defined  // type of text_encoding::aliases_view::end() end() const;
};
```

`text_encoding::aliases_view` models `copyable`, `ranges::view`,
`ranges::random_access_range`, and `ranges::borrowed_range`.

[*Note 1*: `text_encoding::aliases_view` is not required to satisfy
`ranges::``common_range`, nor `default_initializable`. — *end note*]

Both `ranges::range_value_t<text_encoding::aliases_view>` and
`ranges::range_reference_t<text_encoding::aliases_view>` denote
`const char*`.

`ranges::iterator_t<text_encoding::aliases_view>` is a constexpr
iterator [[iterator.requirements.general]].

#### Enumeration `text_encoding::id` <a id="text.encoding.id">[[text.encoding.id]]</a>

``` cpp
namespace std {
  enum class text_encoding::id : int_least32_t {
    other = 1,
    unknown = 2,
    ASCII = 3,
    ISOLatin1 = 4,
    ISOLatin2 = 5,
    ISOLatin3 = 6,
    ISOLatin4 = 7,
    ISOLatinCyrillic = 8,
    ISOLatinArabic = 9,
    ISOLatinGreek = 10,
    ISOLatinHebrew = 11,
    ISOLatin5 = 12,
    ISOLatin6 = 13,
    ISOTextComm = 14,
    HalfWidthKatakana = 15,
    JISEncoding = 16,
    ShiftJIS = 17,
    EUCPkdFmtJapanese = 18,
    EUCFixWidJapanese = 19,
    ISO4UnitedKingdom = 20,
    ISO11SwedishForNames = 21,
    ISO15Italian = 22,
    ISO17Spanish = 23,
    ISO21German = 24,
    ISO60DanishNorwegian = 25,
    ISO69French = 26,
    ISO10646UTF1 = 27,
    ISO646basic1983 = 28,
    INVARIANT = 29,
    ISO2IntlRefVersion = 30,
    NATSSEFI = 31,
    NATSSEFIADD = 32,
    ISO10Swedish = 35,
    KSC56011987 = 36,
    ISO2022KR = 37,
    EUCKR = 38,
    ISO2022JP = 39,
    ISO2022JP2 = 40,
    ISO13JISC6220jp = 41,
    ISO14JISC6220ro = 42,
    ISO16Portuguese = 43,
    ISO18Greek7Old = 44,
    ISO19LatinGreek = 45,
    ISO25French = 46,
    ISO27LatinGreek1 = 47,
    ISO5427Cyrillic = 48,
    ISO42JISC62261978 = 49,
    ISO47BSViewdata = 50,
    ISO49INIS = 51,
    ISO50INIS8 = 52,
    ISO51INISCyrillic = 53,
    ISO54271981 = 54,
    ISO5428Greek = 55,
    ISO57GB1988 = 56,
    ISO58GB231280 = 57,
    ISO61Norwegian2 = 58,
    ISO70VideotexSupp1 = 59,
    ISO84Portuguese2 = 60,
    ISO85Spanish2 = 61,
    ISO86Hungarian = 62,
    ISO87JISX0208 = 63,
    ISO88Greek7 = 64,
    ISO89ASMO449 = 65,
    ISO90 = 66,
    ISO91JISC62291984a = 67,
    ISO92JISC62991984b = 68,
    ISO93JIS62291984badd = 69,
    ISO94JIS62291984hand = 70,
    ISO95JIS62291984handadd = 71,
    ISO96JISC62291984kana = 72,
    ISO2033 = 73,
    ISO99NAPLPS = 74,
    ISO102T617bit = 75,
    ISO103T618bit = 76,
    ISO111ECMACyrillic = 77,
    ISO121Canadian1 = 78,
    ISO122Canadian2 = 79,
    ISO123CSAZ24341985gr = 80,
    ISO88596E = 81,
    ISO88596I = 82,
    ISO128T101G2 = 83,
    ISO88598E = 84,
    ISO88598I = 85,
    ISO139CSN369103 = 86,
    ISO141JUSIB1002 = 87,
    ISO143IECP271 = 88,
    ISO146Serbian = 89,
    ISO147Macedonian = 90,
    ISO150 = 91,
    ISO151Cuba = 92,
    ISO6937Add = 93,
    ISO153GOST1976874 = 94,
    ISO8859Supp = 95,
    ISO10367Box = 96,
    ISO158Lap = 97,
    ISO159JISX02121990 = 98,
    ISO646Danish = 99,
    USDK = 100,
    DKUS = 101,
    KSC5636 = 102,
    Unicode11UTF7 = 103,
    ISO2022CN = 104,
    ISO2022CNEXT = 105,
    UTF8 = 106,
    ISO885913 = 109,
    ISO885914 = 110,
    ISO885915 = 111,
    ISO885916 = 112,
    GBK = 113,
    GB18030 = 114,
    OSDEBCDICDF0415 = 115,
    OSDEBCDICDF03IRV = 116,
    OSDEBCDICDF041 = 117,
    ISO115481 = 118,
    KZ1048 = 119,
    UCS2 = 1000,
    UCS4 = 1001,
    UnicodeASCII = 1002,
    UnicodeLatin1 = 1003,
    UnicodeJapanese = 1004,
    UnicodeIBM1261 = 1005,
    UnicodeIBM1268 = 1006,
    UnicodeIBM1276 = 1007,
    UnicodeIBM1264 = 1008,
    UnicodeIBM1265 = 1009,
    Unicode11 = 1010,
    SCSU = 1011,
    UTF7 = 1012,
    UTF16BE = 1013,
    UTF16LE = 1014,
    UTF16 = 1015,
    CESU8 = 1016,
    UTF32 = 1017,
    UTF32BE = 1018,
    UTF32LE = 1019,
    BOCU1 = 1020,
    UTF7IMAP = 1021,
    Windows30Latin1 = 2000,
    Windows31Latin1 = 2001,
    Windows31Latin2 = 2002,
    Windows31Latin5 = 2003,
    HPRoman8 = 2004,
    AdobeStandardEncoding = 2005,
    VenturaUS = 2006,
    VenturaInternational = 2007,
    DECMCS = 2008,
    PC850Multilingual = 2009,
    PCp852 = 2010,
    PC8CodePage437 = 2011,
    PC8DanishNorwegian = 2012,
    PC862LatinHebrew = 2013,
    PC8Turkish = 2014,
    IBMSymbols = 2015,
    IBMThai = 2016,
    HPLegal = 2017,
    HPPiFont = 2018,
    HPMath8 = 2019,
    HPPSMath = 2020,
    HPDesktop = 2021,
    VenturaMath = 2022,
    MicrosoftPublishing = 2023,
    Windows31J = 2024,
    GB2312 = 2025,
    Big5 = 2026,
    Macintosh = 2027,
    IBM037 = 2028,
    IBM038 = 2029,
    IBM273 = 2030,
    IBM274 = 2031,
    IBM275 = 2032,
    IBM277 = 2033,
    IBM278 = 2034,
    IBM280 = 2035,
    IBM281 = 2036,
    IBM284 = 2037,
    IBM285 = 2038,
    IBM290 = 2039,
    IBM297 = 2040,
    IBM420 = 2041,
    IBM423 = 2042,
    IBM424 = 2043,
    IBM500 = 2044,
    IBM851 = 2045,
    IBM855 = 2046,
    IBM857 = 2047,
    IBM860 = 2048,
    IBM861 = 2049,
    IBM863 = 2050,
    IBM864 = 2051,
    IBM865 = 2052,
    IBM868 = 2053,
    IBM869 = 2054,
    IBM870 = 2055,
    IBM871 = 2056,
    IBM880 = 2057,
    IBM891 = 2058,
    IBM903 = 2059,
    IBM904 = 2060,
    IBM905 = 2061,
    IBM918 = 2062,
    IBM1026 = 2063,
    IBMEBCDICATDE = 2064,
    EBCDICATDEA = 2065,
    EBCDICCAFR = 2066,
    EBCDICDKNO = 2067,
    EBCDICDKNOA = 2068,
    EBCDICFISE = 2069,
    EBCDICFISEA = 2070,
    EBCDICFR = 2071,
    EBCDICIT = 2072,
    EBCDICPT = 2073,
    EBCDICES = 2074,
    EBCDICESA = 2075,
    EBCDICESS = 2076,
    EBCDICUK = 2077,
    EBCDICUS = 2078,
    Unknown8BiT = 2079,
    Mnemonic = 2080,
    Mnem = 2081,
    VISCII = 2082,
    VIQR = 2083,
    KOI8R = 2084,
    HZGB2312 = 2085,
    IBM866 = 2086,
    PC775Baltic = 2087,
    KOI8U = 2088,
    IBM00858 = 2089,
    IBM00924 = 2090,
    IBM01140 = 2091,
    IBM01141 = 2092,
    IBM01142 = 2093,
    IBM01143 = 2094,
    IBM01144 = 2095,
    IBM01145 = 2096,
    IBM01146 = 2097,
    IBM01147 = 2098,
    IBM01148 = 2099,
    IBM01149 = 2100,
    Big5HKSCS = 2101,
    IBM1047 = 2102,
    PTCP154 = 2103,
    Amiga1251 = 2104,
    KOI7switched = 2105,
    BRF = 2106,
    TSCII = 2107,
    CP51932 = 2108,
    windows874 = 2109,
    windows1250 = 2250,
    windows1251 = 2251,
    windows1252 = 2252,
    windows1253 = 2253,
    windows1254 = 2254,
    windows1255 = 2255,
    windows1256 = 2256,
    windows1257 = 2257,
    windows1258 = 2258,
    TIS620 = 2259,
    CP50220 = 2260
  };
}
```

[*Note 1*:

The `text_encoding::id` enumeration contains an enumerator for each
known registered character encoding. For each encoding, the
corresponding enumerator is derived from the alias beginning with
“`cs`”, as follows

- `csUnicode` is mapped to `text_encoding::id::UCS2`,
- `csIBBM904` is mapped to `text_encoding::id::IBM904`, and
- the “`cs`” prefix is removed from other names.

— *end note*]

#### Hash support <a id="text.encoding.hash">[[text.encoding.hash]]</a>

``` cpp
template<> struct hash<text_encoding>;
```

The specialization is enabled [[unord.hash]].

## Formatting <a id="format">[[format]]</a>

### Header `<format>` synopsis <a id="format.syn">[[format.syn]]</a>

``` cpp
namespace std {
  // [format.context], class template basic_format_context
  template<class Out, class charT> class basic_format_context;
  using format_context = basic_format_context<unspecified, char>;
  using wformat_context = basic_format_context<unspecified, wchar_t>;

  // [format.args], class template basic_format_args
  template<class Context> class basic_format_args;
  using format_args = basic_format_args<format_context>;
  using wformat_args = basic_format_args<wformat_context>;

  // [format.fmt.string], class template basic_format_string
  template<class charT, class... Args>
    struct basic_format_string;

  template<class charT> struct runtime-format-string {                  // exposition only
  private:
    basic_string_view<charT> str;                                       // exposition only
  public:
    runtime-format-string(basic_string_view<charT> s) noexcept : str(s) {}
    runtime-format-string(const runtime-format-string&) = delete;
    runtime-format-string& operator=(const runtime-format-string&) = delete;
  };
  runtime-format-string<char> runtime_format(string_view fmt) noexcept { return fmt; }
  runtime-format-string<wchar_t> runtime_format(wstring_view fmt) noexcept { return fmt; }

  template<class... Args>
    using format_string = basic_format_string<char, type_identity_t<Args>...>;
  template<class... Args>
    using wformat_string = basic_format_string<wchar_t, type_identity_t<Args>...>;

  // [format.functions], formatting functions
  template<class... Args>
    string format(format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    wstring format(wformat_string<Args...> fmt, Args&&... args);
  template<class... Args>
    string format(const locale& loc, format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    wstring format(const locale& loc, wformat_string<Args...> fmt, Args&&... args);

  string vformat(string_view fmt, format_args args);
  wstring vformat(wstring_view fmt, wformat_args args);
  string vformat(const locale& loc, string_view fmt, format_args args);
  wstring vformat(const locale& loc, wstring_view fmt, wformat_args args);

  template<class Out, class... Args>
    Out format_to(Out out, format_string<Args...> fmt, Args&&... args);
  template<class Out, class... Args>
    Out format_to(Out out, wformat_string<Args...> fmt, Args&&... args);
  template<class Out, class... Args>
    Out format_to(Out out, const locale& loc, format_string<Args...> fmt, Args&&... args);
  template<class Out, class... Args>
    Out format_to(Out out, const locale& loc, wformat_string<Args...> fmt, Args&&... args);

  template<class Out>
    Out vformat_to(Out out, string_view fmt, format_args args);
  template<class Out>
    Out vformat_to(Out out, wstring_view fmt, wformat_args args);
  template<class Out>
    Out vformat_to(Out out, const locale& loc, string_view fmt, format_args args);
  template<class Out>
    Out vformat_to(Out out, const locale& loc, wstring_view fmt, wformat_args args);

  template<class Out> struct format_to_n_result {
    Out out;
    iter_difference_t<Out> size;
  };
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        format_string<Args...> fmt, Args&&... args);
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        wformat_string<Args...> fmt, Args&&... args);
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        const locale& loc, format_string<Args...> fmt,
                                        Args&&... args);
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        const locale& loc, wformat_string<Args...> fmt,
                                        Args&&... args);

  template<class... Args>
    size_t formatted_size(format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    size_t formatted_size(wformat_string<Args...> fmt, Args&&... args);
  template<class... Args>
    size_t formatted_size(const locale& loc, format_string<Args...> fmt, Args&&... args);
  template<class... Args>
    size_t formatted_size(const locale& loc, wformat_string<Args...> fmt, Args&&... args);

  // [format.formatter], formatter
  template<class T, class charT = char> struct formatter;

  // [format.formatter.locking], formatter locking
  template<class T>
    constexpr bool enable_nonlocking_formatter_optimization = false;

  // [format.formattable], concept formattable
  template<class T, class charT>
    concept formattable = see below;

  template<class R, class charT>
    concept const-formattable-range =                                   // exposition only
      ranges::input_range<const R> &&
      formattable<ranges::range_reference_t<const R>, charT>;

  template<class R, class charT>
    using fmt-maybe-const =                                             // exposition only
      conditional_t<const-formattable-range<R, charT>, const R, R>;

  // [format.parse.ctx], class template basic_format_parse_context
  template<class charT> class basic_format_parse_context;
  using format_parse_context = basic_format_parse_context<char>;
  using wformat_parse_context = basic_format_parse_context<wchar_t>;

  // [format.range], formatting of ranges
  // [format.range.fmtkind], variable template format_kind
  enum class range_format {
    disabled,
    map,
    set,
    sequence,
    string,
    debug_string
  };

  template<class R>
    constexpr unspecified format_kind = unspecified;

  template<ranges::input_range R>
    requires same_as<R, remove_cvref_t<R>>
    constexpr range_format format_kind<R> = see below;

  // [format.range.formatter], class template range_formatter
  template<class T, class charT = char>
    requires same_as<remove_cvref_t<T>, T> && formattable<T, charT>
  class range_formatter;

  // [format.range.fmtdef], class template range-default-formatter
  template<range_format K, ranges::input_range R, class charT>
    struct range-default-formatter;                                     // exposition only

  // [format.range.fmtmap], [format.range.fmtset], [format.range.fmtstr], specializations for maps, sets, and strings
  template<ranges::input_range R, class charT>
    requires (format_kind<R> != range_format::disabled) &&
             formattable<ranges::range_reference_t<R>, charT>
  struct formatter<R, charT> : range-default-formatter<format_kind<R>, R, charT> { };

  template<ranges::input_range R>
    requires (format_kind<R> != range_format::disabled)
    constexpr bool enable_nonlocking_formatter_optimization<R> = false;

  // [format.arguments], arguments
  // [format.arg], class template basic_format_arg
  template<class Context> class basic_format_arg;

  // [format.arg.store], class template format-arg-store
  template<class Context, class... Args> class format-arg-store;        // exposition only

  template<class Context = format_context, class... Args>
    format-arg-store<Context, Args...>
      make_format_args(Args&... fmt_args);
  template<class... Args>
    format-arg-store<wformat_context, Args...>
      make_wformat_args(Args&... args);

  // [format.error], class format_error
  class format_error;
}
```

The class template `format_to_n_result` has the template parameters,
data members, and special members specified above. It has no base
classes or members other than those specified.

### Format string <a id="format.string">[[format.string]]</a>

#### General <a id="format.string.general">[[format.string.general]]</a>

A *format string* for arguments `args` is a (possibly empty) sequence of
*replacement fields*, *escape sequences*, and characters other than `{`
and `}`. Let `charT` be the character type of the format string. Each
character that is not part of a replacement field or an escape sequence
is copied unchanged to the output. An escape sequence is one of `{{` or
`}}`. It is replaced with `{` or `}`, respectively, in the output. The
syntax of replacement fields is as follows:

``` bnf
\fmtnontermdef{replacement-field}
    \terminal{\ arg-idₒₚₜ format-specifierₒₚₜ \terminal{\}}
```

``` bnf
\fmtnontermdef{arg-id}
    '0'
    positive-integer
```

``` bnf
\fmtnontermdef{positive-integer}
    nonzero-digit
    positive-integer digit
```

``` bnf
\fmtnontermdef{nonnegative-integer}
    digit
    nonnegative-integer digit
```

``` bnf
\fmtnontermdef{nonzero-digit} one of
    '1 2 3 4 5 6 7 8 9'
```

``` bnf
\fmtnontermdef{digit} one of
    '0 1 2 3 4 5 6 7 8 9'
```

``` bnf
\fmtnontermdef{format-specifier}
    ':' format-spec
```

``` bnf
\fmtnontermdef{format-spec}
    as specified by the formatter specialization for the argument type; cannot start with '}'
```

The *arg-id* field specifies the index of the argument in `args` whose
value is to be formatted and inserted into the output instead of the
replacement field. If there is no argument with the index *arg-id* in
`args`, the string is not a format string for `args`. The optional
*format-specifier* field explicitly specifies a format for the
replacement value.

[*Example 1*:

``` cpp
string s = format("{0}-{{", 8);         // value of s is "8-{"
```

— *end example*]

If all *arg-id*s in a format string are omitted (including those in the
*format-spec*, as interpreted by the corresponding `formatter`
specialization), argument indices 0, 1, 2, … will automatically be used
in that order. If some *arg-id*s are omitted and some are present, the
string is not a format string.

[*Note 1*: A format string cannot contain a mixture of automatic and
manual indexing. — *end note*]

[*Example 2*:

``` cpp
string s0 = format("{} to {}",   "a", "b"); // OK, automatic indexing
string s1 = format("{1} to {0}", "a", "b"); // OK, manual indexing
string s2 = format("{0} to {}",  "a", "b"); // not a format string (mixing automatic and manual indexing),
                                            // ill-formed
string s3 = format("{} to {1}",  "a", "b"); // not a format string (mixing automatic and manual indexing),
                                            // ill-formed
```

— *end example*]

The *format-spec* field contains *format specifications* that define how
the value should be presented. Each type can define its own
interpretation of the *format-spec* field. If *format-spec* does not
conform to the format specifications for the argument type referred to
by *arg-id*, the string is not a format string for `args`.

[*Example 3*:

- For arithmetic, pointer, and string types the *format-spec* is
  interpreted as a *std-format-spec* as described in 
  [[format.string.std]].
- For chrono types the *format-spec* is interpreted as a
  *chrono-format-spec* as described in  [[time.format]].
- For user-defined `formatter` specializations, the behavior of the
  `parse` member function determines how the *format-spec* is
  interpreted.

— *end example*]

#### Standard format specifiers <a id="format.string.std">[[format.string.std]]</a>

Each `formatter` specialization described in [[format.formatter.spec]]
for fundamental and string types interprets *format-spec* as a
*std-format-spec*.

[*Note 1*: The format specification can be used to specify such details
as minimum field width, alignment, padding, and decimal precision. Some
of the formatting options are only supported for arithmetic
types. — *end note*]

The syntax of format specifications is as follows:

``` bnf
\fmtnontermdef{std-format-spec}
    fill-and-alignₒₚₜ signₒₚₜ '#'ₒₚₜ '0'ₒₚₜ widthₒₚₜ precisionₒₚₜ 'L'ₒₚₜ typeₒₚₜ
```

``` bnf
\fmtnontermdef{fill-and-align}
    fillₒₚₜ align
```

``` bnf
\fmtnontermdef{fill}
    \textnormal{any character other than \ or \texttt{\}}
```

``` bnf
\fmtnontermdef{align} one of
    '< > ^'
```

``` bnf
\fmtnontermdef{sign} one of
    '+ -' space
```

``` bnf
\fmtnontermdef{width}
    positive-integer
    \terminal{\ arg-idₒₚₜ \terminal{\}}
```

``` bnf
\fmtnontermdef{precision}
    '.' nonnegative-integer
    '.' \terminal{\ arg-idₒₚₜ \terminal{\}}
```

``` bnf
\fmtnontermdef{type} one of
    'a A b B c d e E f F g G o p P s x X ?'
```

Field widths are specified in *field width units*; the number of column
positions required to display a sequence of characters in a terminal.
The *minimum field width* is the number of field width units a
replacement field minimally requires of the formatted sequence of
characters produced for a format argument. The *estimated field width*
is the number of field width units that are required for the formatted
sequence of characters produced for a format argument independent of the
effects of the *width* option. The *padding width* is the greater of `0`
and the difference of the minimum field width and the estimated field
width.

[*Note 2*: The POSIX `wcswidth` function is an example of a function
that, given a string, returns the number of column positions required by
a terminal to display the string. — *end note*]

The *fill character* is the character denoted by the *fill* option or,
if the *fill* option is absent, the space character. For a format
specification in UTF-8, UTF-16, or UTF-32, the fill character
corresponds to a single Unicode scalar value.

[*Note 3*: The presence of a *fill* option is signaled by the character
following it, which must be one of the alignment options. If the second
character of *std-format-spec* is not a valid alignment option, then it
is assumed that the *fill* and *align* options are both
absent. — *end note*]

The *align* option applies to all argument types. The meaning of the
various alignment options is as specified in [[format.align]].

[*Example 1*:

``` cpp
char c = 120;
string s0 = format("{:6}", 42);             // value of s0 is "\ \ \ \ 42"
string s1 = format("{:6}", 'x');            // value of s1 is "x\ \ \ \ \ "
string s2 = format("{:*<6}", 'x');          // value of s2 is "x*****"
string s3 = format("{:*>6}", 'x');          // value of s3 is "*****x"
string s4 = format("{:*^6}", 'x');          // value of s4 is "**x***"
string s5 = format("{:6d}", c);             // value of s5 is "\ \ \ 120"
string s6 = format("{:6}", true);           // value of s6 is "true\ \ "
string s7 = format("{:*<6.3}", "123456");   // value of s7 is "123***"
string s8 = format("{:02}", 1234);          // value of s8 is "1234"
string s9 = format("{:*<}", "12");          // value of s9 is "12"
string sA = format("{:*<6}", "12345678");   // value of sA is "12345678"
string sB = format("{:\importexample[-2pt]{example_05}\kern0.75pt^6}", "x");         // value of sB is "\importexample[-2pt]{example_05\importexample[-2pt]{example_05}x\importexample[-2pt]{example_05}\importexample[-2pt]{example_05}\importexample[-2pt]{example_05}"}
string sC = format("{:*^6}", "\importexample[-2pt]{example_05}\kern0.75pt\importexample[-2pt]{example_05}\kern0.75pt\importexample[-2pt]{example_05}\kern0.75pt");     // value of sC is "\importexample[-2pt]{example_05\importexample[-2pt]{example_05}\importexample[-2pt]{example_05}"}
```

— *end example*]

[*Note 4*: The *fill*, *align*, and `0` options have no effect when the
minimum field width is not greater than the estimated field width
because padding width is `0` in that case. Since fill characters are
assumed to have a field width of `1`, use of a character with a
different field width can produce misaligned output. The
(U+1f921 (clown face)) character has a field width of `2`. The examples
above that include that character illustrate the effect of the field
width when that character is used as a fill character as opposed to when
it is used as a formatting argument. — *end note*]

**Table: Meaning of align options**

| Option | Meaning                                                                                                                                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `<`    | Forces the formatted argument to be aligned to the start of the field by inserting $n$ fill characters after the formatted argument where $n$ is the padding width. This is the default for non-arithmetic non-pointer types, `charT`, and `bool`, unless an integer presentation type is specified.         |
| % `>`  | Forces the formatted argument to be aligned to the end of the field by inserting $n$ fill characters before the formatted argument where $n$ is the padding width. This is the default for arithmetic types other than `charT` and `bool`, pointer types, or when an integer presentation type is specified. |
| % `^`  | Forces the formatted argument to be centered within the field by inserting $\bigl\lfloor \frac{n}{2} \bigr\rfloor$ fill characters before and $\bigl\lceil \frac{n}{2} \bigr\rceil$ fill characters after the formatted argument, where $n$ is the padding width.                                            |


The *sign* option is only valid for arithmetic types other than `charT`
and `bool` or when an integer presentation type is specified. The
meaning of the various options is as specified in [[format.sign]].

**Table: Meaning of sign options**

| Option  | Meaning                                                                                                                                                                                                                                                                                                                                    |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `+`     | Indicates that a sign should be used for both non-negative and negative numbers. The `+` sign is inserted before the output of `to_chars` for non-negative numbers other than negative zero. *For negative numbers and negative zero the output of `to_chars` will already contain the sign so no additional transformation is performed.* |
| % `-`   | Indicates that a sign should be used for negative numbers and negative zero only (this is the default behavior).                                                                                                                                                                                                                           |
| % space | Indicates that a leading space should be used for non-negative numbers other than negative zero, and a minus sign for negative numbers and negative zero.                                                                                                                                                                                  |


The *sign* option applies to floating-point infinity and NaN.

[*Example 2*:

``` cpp
double inf = numeric_limits<double>::infinity();
double nan = numeric_limits<double>::quiet_NaN();
string s0 = format("{0:},{0:+},{0:-},{0: }", 1);        // value of s0 is "1,+1,1, 1"
string s1 = format("{0:},{0:+},{0:-},{0: }", -1);       // value of s1 is "-1,-1,-1,-1"
string s2 = format("{0:},{0:+},{0:-},{0: }", inf);      // value of s2 is "inf,+inf,inf, inf"
string s3 = format("{0:},{0:+},{0:-},{0: }", nan);      // value of s3 is "nan,+nan,nan, nan"
```

— *end example*]

The `#` option causes the *alternate form* to be used for the
conversion. This option is valid for arithmetic types other than `charT`
and `bool` or when an integer presentation type is specified, and not
otherwise. For integral types, the alternate form inserts the base
prefix (if any) specified in [[format.type.int]] into the output after
the sign character (possibly space) if there is one, or before the
output of `to_chars` otherwise. For floating-point types, the alternate
form causes the result of the conversion of finite values to always
contain a decimal-point character, even if no digits follow it.
Normally, a decimal-point character appears in the result of these
conversions only if a digit follows it. In addition, for `g` and `G`
conversions, trailing zeros are not removed from the result.

The `0` option is valid for arithmetic types other than `charT` and
`bool`, pointer types, or when an integer presentation type is
specified. For formatting arguments that have a value other than an
infinity or a NaN, this option pads the formatted argument by inserting
the `0` character n times following the sign or base prefix indicators
(if any) where n is `0` if the *align* option is present and is the
padding width otherwise.

[*Example 3*:

``` cpp
char c = 120;
string s1 = format("{:+06d}", c);       // value of s1 is "+00120"
string s2 = format("{:#06x}", 0xa);     // value of s2 is "0x000a"
string s3 = format("{:<06}", -42);      // value of s3 is "-42\ \ \ " (0 has no effect)
string s4 = format("{:06}", inf);       // value of s4 is "\ \ \ inf" (0 has no effect)
```

— *end example*]

The *width* option specifies the minimum field width. If the *width*
option is absent, the minimum field width is `0`.

If `{ arg-idₒₚₜ }` is used in a *width* or *precision* option, the value
of the corresponding formatting argument is used as the value of the
option. The option is valid only if the corresponding formatting
argument is of standard signed or unsigned integer type. If its value is
negative, an exception of type `format_error` is thrown.

If *positive-integer* is used in a *width* option, the value of the
*positive-integer* is interpreted as a decimal integer and used as the
value of the option.

For the purposes of width computation, a string is assumed to be in a
locale-independent, *implementation-defined* encoding. Implementations
should use either UTF-8, UTF-16, or UTF-32, on platforms capable of
displaying Unicode text in a terminal.

[*Note 5*:

This is the case for Windows\textregistered-based

[^25]

and many POSIX-based operating systems.

— *end note*]

For a sequence of characters in UTF-8, UTF-16, or UTF-32, an
implementation should use as its field width the sum of the field widths
of the first code point of each extended grapheme cluster. Extended
grapheme clusters are defined by UAX \#29 of the Unicode Standard. The
following code points have a field width of 2:

- any code point with the `East_Asian_Width="W"` or
  `East_Asian_Width="F"` property as described by UAX \#44 of the
  Unicode Standard
- `U+4dc0` – `U+4dff` (Yijing Hexagram Symbols)
- `U+1f300` – `U+1f5ff` (Miscellaneous Symbols and Pictographs)
- `U+1f900` – `U+1f9ff` (Supplemental Symbols and Pictographs)

The field width of all other code points is 1.

For a sequence of characters in neither UTF-8, UTF-16, nor UTF-32, the
field width is unspecified.

The *precision* option is valid for floating-point and string types. For
floating-point types, the value of this option specifies the precision
to be used for the floating-point presentation type. For string types,
this option specifies the longest prefix of the formatted argument to be
included in the replacement field such that the field width of the
prefix is no greater than the value of this option.

If *nonnegative-integer* is used in a *precision* option, the value of
the decimal integer is used as the value of the option.

When the `L` option is used, the form used for the conversion is called
the *locale-specific form*. The `L` option is only valid for arithmetic
types, and its effect depends upon the type.

- For integral types, the locale-specific form causes the context’s
  locale to be used to insert the appropriate digit group separator
  characters.
- For floating-point types, the locale-specific form causes the
  context’s locale to be used to insert the appropriate digit group and
  radix separator characters.
- For the textual representation of `bool`, the locale-specific form
  causes the context’s locale to be used to insert the appropriate
  string as if obtained with `numpunct::truename` or
  `numpunct::falsename`.

The *type* determines how the data should be presented.

The available string presentation types are specified in
[[format.type.string]].

**Table: Meaning of type options for strings**

| Type      | Meaning                                                            |
| --------- | ------------------------------------------------------------------ |
| none, `s` | Copies the string to the output.                                   |
| % `?`     | Copies the escaped string [[format.string.escaped]] to the output. |


The meaning of some non-string presentation types is defined in terms of
a call to `to_chars`. In such cases, let \[`first`, `last`) be a range
large enough to hold the `to_chars` output and `value` be the formatting
argument value. Formatting is done as if by calling `to_chars` as
specified and copying the output through the output iterator of the
format context.

[*Note 6*: Additional padding and adjustments are performed prior to
copying the output through the output iterator as specified by the
format specifiers. — *end note*]

The available integer presentation types for integral types other than
`bool` and `charT` are specified in [[format.type.int]].

[*Example 4*:

``` cpp
string s0 = format("{}", 42);                           // value of s0 is "42"
string s1 = format("{0:b} {0:d} {0:o} {0:x}", 42);      // value of s1 is "101010 42 52 2a"
string s2 = format("{0:#x} {0:#X}", 42);                // value of s2 is "0x2a 0X2A"
string s3 = format("{:L}", 1234);                       // value of s3 can be "1,234"
                                                        // (depending on the locale)
```

— *end example*]

**Table: Meaning of type options for integer types**

| Type   | Meaning                                                                                                                                                   |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `b`    | `to_chars(first, last, value, 2)`; \indextext{base prefix}% the base prefix is `0b`.                                                                      |
| % `B`  | The same as `b`, except that \indextext{base prefix}% the base prefix is `0B`.                                                                            |
| % `c`  | Copies the character `static_cast<charT>(value)` to the output. Throws `format_error` if `value` is not in the range of representable values for `charT`. |
| % `d`  | `to_chars(first, last, value)`.                                                                                                                           |
| % `o`  | `to_chars(first, last, value, 8)`; \indextext{base prefix}% the base prefix is `0` if `value` is nonzero and is empty otherwise.                          |
| % `x`  | `to_chars(first, last, value, 16)`; \indextext{base prefix}% the base prefix is `0x`.                                                                     |
| % `X`  | The same as `x`, except that it uses uppercase letters for digits above 9 and \indextext{base prefix}% the base prefix is `0X`.                           |
| % none | The same as `d`. *If the formatting argument type is `charT` or `bool`, the default is instead `c` or `s`, respectively.*                                 |


The available `charT` presentation types are specified in
[[format.type.char]].

**Table: Meaning of type options for `charT`**

| Type                           | Meaning                                                                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| none, `c`                      | Copies the character to the output.                                                                        |
| % `b`, `B`, `d`, `o`, `x`, `X` | As specified in [[format.type.int]] with `value` converted to the unsigned version of the underlying type. |
| % `?`                          | Copies the escaped character [[format.string.escaped]] to the output.                                      |


The available `bool` presentation types are specified in
[[format.type.bool]].

**Table: Meaning of type options for `bool`**

| Type                           | Meaning                                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| none, `s`                      | Copies textual representation, either `true` or `false`, to the output.                |
| % `b`, `B`, `d`, `o`, `x`, `X` | As specified in [[format.type.int]] for the value `static_cast<unsigned char>(value)`. |


The available floating-point presentation types and their meanings for
values other than infinity and NaN are specified in
[[format.type.float]]. For lower-case presentation types, infinity and
NaN are formatted as `inf` and `nan`, respectively. For upper-case
presentation types, infinity and NaN are formatted as `INF` and `NAN`,
respectively.

[*Note 7*: In either case, a sign is included if indicated by the
*sign* option. — *end note*]

**Table: Meaning of type options for floating-point types**

| Type       | Meaning                                                                                                                                                                                                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `a`        | If precision is specified, equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::hex, precision) \end{codeblock} where `precision` is the specified formatting precision; equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::hex) \end{codeblock} otherwise. |
| % `A`      | The same as `a`, except that it uses uppercase letters for digits above 9 and `P` to indicate the exponent.                                                                                                                                                                                               |
| % `e`      | Equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::scientific, precision) \end{codeblock} where `precision` is the specified formatting precision, or `6` if precision is not specified.                                                                                          |
| % `E`      | The same as `e`, except that it uses `E` to indicate exponent.                                                                                                                                                                                                                                            |
| % `f`, `F` | Equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::fixed, precision) \end{codeblock} where `precision` is the specified formatting precision, or `6` if precision is not specified.                                                                                               |
| % `g`      | Equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::general, precision) \end{codeblock} where `precision` is the specified formatting precision, or `6` if precision is not specified.                                                                                             |
| % `G`      | The same as `g`, except that it uses `E` to indicate exponent.                                                                                                                                                                                                                                            |
| % none     | If precision is specified, equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::general, precision) \end{codeblock} where `precision` is the specified formatting precision; equivalent to \begin{codeblock} to_chars(first, last, value) \end{codeblock} otherwise.                |


The available pointer presentation types and their mapping to `to_chars`
are specified in [[format.type.ptr]].

[*Note 8*: Pointer presentation types also apply to
`nullptr_t`. — *end note*]

**Table: Meaning of type options for pointer types**

| Type      | Meaning                                                                                                                                                                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| none, `p` | If `uintptr_t` is defined, \begin{codeblock} to_chars(first, last, reinterpret_cast<uintptr_t>(value), 16) \end{codeblock} with the prefix `0x` inserted immediately before the output of `to_chars`; otherwise, implementation-defined. |
| `P`       | The same as `p`, except that it uses uppercase letters for digits above `9` and the base prefix is `0X`.                                                                                                                                 |


### Error reporting <a id="format.err.report">[[format.err.report]]</a>

Formatting functions throw `format_error` if an argument `fmt` is passed
that is not a format string for `args`. They propagate exceptions thrown
by operations of `formatter` specializations and iterators. Failure to
allocate storage is reported by throwing an exception as described in 
[[res.on.exception.handling]].

### Class template `basic_format_string` <a id="format.fmt.string">[[format.fmt.string]]</a>

``` cpp
namespace std {
  template<class charT, class... Args>
  struct basic_format_string {
  private:
    basic_string_view<charT> str;         // exposition only

  public:
    template<class T> consteval basic_format_string(const T& s);
    basic_format_string(runtime-format-string<charT> s) noexcept : str(s.str) {}

    constexpr basic_string_view<charT> get() const noexcept { return str; }
  };
}
```

``` cpp
template<class T> consteval basic_format_string(const T& s);
```

*Constraints:* `const T&` models
`convertible_to<basic_string_view<charT>>`.

*Effects:* Direct-non-list-initializes *str* with `s`.

*Remarks:* A call to this function is not a core constant
expression [[expr.const]] unless there exist `args` of types `Args` such
that *str* is a format string for `args`.

### Formatting functions <a id="format.functions">[[format.functions]]</a>

In the description of the functions, operator `+` is used for some of
the iterator categories for which it does not have to be defined. In
these cases the semantics of `a + n` are the same as in
[[algorithms.requirements]].

``` cpp
template<class... Args>
  string format(format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(fmt.str, make_format_args(args...));
```

``` cpp
template<class... Args>
  wstring format(wformat_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(fmt.str, make_wformat_args(args...));
```

``` cpp
template<class... Args>
  string format(const locale& loc, format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(loc, fmt.str, make_format_args(args...));
```

``` cpp
template<class... Args>
  wstring format(const locale& loc, wformat_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(loc, fmt.str, make_wformat_args(args...));
```

``` cpp
string vformat(string_view fmt, format_args args);
wstring vformat(wstring_view fmt, wformat_args args);
string vformat(const locale& loc, string_view fmt, format_args args);
wstring vformat(const locale& loc, wstring_view fmt, wformat_args args);
```

*Returns:* A string object holding the character representation of
formatting arguments provided by `args` formatted according to
specifications given in `fmt`. If present, `loc` is used for
locale-specific formatting.

*Throws:* As specified in  [[format.err.report]].

``` cpp
template<class Out, class... Args>
  Out format_to(Out out, format_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat_to(std::move(out), fmt.str, make_format_args(args...));
```

``` cpp
template<class Out, class... Args>
  Out format_to(Out out, wformat_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat_to(std::move(out), fmt.str, make_wformat_args(args...));
```

``` cpp
template<class Out, class... Args>
  Out format_to(Out out, const locale& loc, format_string<Args...>  fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat_to(std::move(out), loc, fmt.str, make_format_args(args...));
```

``` cpp
template<class Out, class... Args>
  Out format_to(Out out, const locale& loc, wformat_string<Args...> fmt, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat_to(std::move(out), loc, fmt.str, make_wformat_args(args...));
```

``` cpp
template<class Out>
  Out vformat_to(Out out, string_view fmt, format_args args);
template<class Out>
  Out vformat_to(Out out, wstring_view fmt, wformat_args args);
template<class Out>
  Out vformat_to(Out out, const locale& loc, string_view fmt, format_args args);
template<class Out>
  Out vformat_to(Out out, const locale& loc, wstring_view fmt, wformat_args args);
```

Let `charT` be `decltype(fmt)::value_type`.

*Constraints:* `Out` satisfies `output_iterator<const charT&>`.

*Preconditions:* `Out` models `output_iterator<const charT&>`.

*Effects:* Places the character representation of formatting the
arguments provided by `args`, formatted according to the specifications
given in `fmt`, into the range \[`out`, `out + N`), where `N` is the
number of characters in that character representation. If present, `loc`
is used for locale-specific formatting.

*Returns:* `out + N`.

*Throws:* As specified in  [[format.err.report]].

``` cpp
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      format_string<Args...> fmt, Args&&... args);
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      wformat_string<Args...> fmt, Args&&... args);
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      const locale& loc, format_string<Args...> fmt,
                                      Args&&... args);
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      const locale& loc, wformat_string<Args...> fmt,
                                      Args&&... args);
```

Let

- `charT` be `decltype(fmt.`*`str`*`)::value_type`,
- `N` be `formatted_size(fmt, args...)` for the functions without a
  `loc` parameter and `formatted_size(loc, fmt, args...)` for the
  functions with a `loc` parameter, and
- `M` be `clamp(n, 0, N)`.

*Constraints:* `Out` satisfies `output_iterator<const charT&>`.

*Preconditions:* `Out` models `output_iterator<const charT&>`, and
`formatter<``remove_cvref_t<Tᵢ``>, charT>` meets the
requirements [[formatter.requirements]] for each `Tᵢ` in `Args`.

*Effects:* Places the first `M` characters of the character
representation of formatting the arguments provided by `args`, formatted
according to the specifications given in `fmt`, into the range \[`out`,
`out + M`). If present, `loc` is used for locale-specific formatting.

*Returns:* `{out + M, N}`.

*Throws:* As specified in  [[format.err.report]].

``` cpp
template<class... Args>
  size_t formatted_size(format_string<Args...> fmt, Args&&... args);
template<class... Args>
  size_t formatted_size(wformat_string<Args...> fmt, Args&&... args);
template<class... Args>
  size_t formatted_size(const locale& loc, format_string<Args...> fmt, Args&&... args);
template<class... Args>
  size_t formatted_size(const locale& loc, wformat_string<Args...> fmt, Args&&... args);
```

Let `charT` be `decltype(fmt.`*`str`*`)::value_type`.

*Preconditions:* `formatter<``remove_cvref_t<Tᵢ``>, charT>` meets the
requirements [[formatter.requirements]] for each `Tᵢ` in `Args`.

*Returns:* The number of characters in the character representation of
formatting arguments `args` formatted according to specifications given
in `fmt`. If present, `loc` is used for locale-specific formatting.

*Throws:* As specified in  [[format.err.report]].

### Formatter <a id="format.formatter">[[format.formatter]]</a>

#### Formatter requirements <a id="formatter.requirements">[[formatter.requirements]]</a>

A type `F` meets the requirements if it meets the

- *Cpp17DefaultConstructible* ([[cpp17.defaultconstructible]]),
- *Cpp17CopyConstructible* ([[cpp17.copyconstructible]]),
- *Cpp17CopyAssignable* ([[cpp17.copyassignable]]),
- *Cpp17Swappable* [[swappable.requirements]], and
- *Cpp17Destructible* ([[cpp17.destructible]])

requirements, and the expressions shown in [[formatter.basic]] are valid
and have the indicated semantics.

A type `F` meets the requirements if it meets the requirements and the
expressions shown in [[formatter]] are valid and have the indicated
semantics.

Given character type `charT`, output iterator type `Out`, and formatting
argument type `T`, in [[formatter.basic]] and [[formatter]]:

- `f` is a value of type (possibly const) `F`,
- `g` is an lvalue of type `F`,
- `u` is an lvalue of type `T`,
- `t` is a value of a type convertible to (possibly const) `T`,
- `PC` is `basic_format_parse_context<charT>`,
- `FC` is `basic_format_context<Out, charT>`,
- `pc` is an lvalue of type `PC`, and
- `fc` is an lvalue of type `FC`.

`pc.begin()` points to the beginning of the *format-spec*
[[format.string]] of the replacement field being formatted in the format
string. If *format-spec* is not present or empty then either
`pc.begin() == pc.end()` or `*pc.begin() == '}'`.

[*Note 1*: This allows formatters to emit meaningful error
messages. — *end note*]

**Table: \newoldconcept{Formatter} requirements**

| Expression        | Return type    | Requirement                                                                                                                                                                                                                                                                                                                                 |
| ----------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `f.format(t, fc)` | `FC::iterator` | Formats `t` according to the specifiers stored in `*this`, writes the output to `fc.out()`, and returns an iterator past the end of the output range. The output shall only depend on `t`, `fc.locale()`, `fc.arg(n)` for any value `n` of type `size_t`, and the range {[}`pc.begin()`, `pc.end()`{)} from the last call to `f.parse(pc)`. |
| `f.format(u, fc)` | `FC::iterator` | As above, but does not modify `u`.                                                                                                                                                                                                                                                                                                          |


#### Formatter locking <a id="format.formatter.locking">[[format.formatter.locking]]</a>

``` cpp
template<class T>
  constexpr bool enable_nonlocking_formatter_optimization = false;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`enable_nonlocking_formatter_optimization` for cv-unqualified
program-defined types. Such specializations shall be usable in constant
expressions [[expr.const]] and have type `const bool`.

#### Concept  <a id="format.formattable">[[format.formattable]]</a>

Let `fmt-iter-for<charT>` be an unspecified type that models
`output_iterator<const charT&>` [[iterator.concept.output]].

``` cpp
template<class T, class Context,
         class Formatter = typename Context::template formatter_type<remove_const_t<T>>>
  concept formattable-with =                // exposition only
    semiregular<Formatter> &&
    requires(Formatter& f, const Formatter& cf, T&& t, Context fc,
             basic_format_parse_context<typename Context::char_type> pc)
    {
      { f.parse(pc) } -> same_as<typename decltype(pc)::iterator>;
      { cf.format(t, fc) } -> same_as<typename Context::iterator>;
    };

template<class T, class charT>
  concept formattable =
    formattable-with<remove_reference_t<T>, basic_format_context<fmt-iter-for<charT>, charT>>;
```

A type `T` and a character type `charT` model `formattable` if
`formatter<remove_cvref_t<T>, charT>` meets the requirements
[[formatter.requirements]] and, if `remove_reference_t<T>` is
const-qualified, the requirements.

#### Formatter specializations <a id="format.formatter.spec">[[format.formatter.spec]]</a>

The functions defined in [[format.functions]] use specializations of the
class template `formatter` to format individual arguments.

Let `charT` be either `char` or `wchar_t`. Each specialization of
`formatter` is either enabled or disabled, as described below. A
*debug-enabled* specialization of `formatter` additionally provides a
public, constexpr, non-static member function `set_debug_format()` which
modifies the state of the `formatter` to be as if the type of the
*std-format-spec* parsed by the last call to `parse` were `?`. Each
header that declares the template `formatter` provides the following
enabled specializations:

- The debug-enabled specializations
  ``` cpp
  template<> struct formatter<char, char>;
  template<> struct formatter<char, wchar_t>;
  template<> struct formatter<wchar_t, wchar_t>;
  ```
- For each `charT`, the debug-enabled string type specializations
  ``` cpp
  template<> struct formatter<charT*, charT>;
  template<> struct formatter<const charT*, charT>;
  template<size_t N> struct formatter<charT[N], charT>;
  template<class traits, class Allocator>
    struct formatter<basic_string<charT, traits, Allocator>, charT>;
  template<class traits>
    struct formatter<basic_string_view<charT, traits>, charT>;
  ```
- For each `charT`, for each cv-unqualified arithmetic type
  `ArithmeticT` other than `char`, `wchar_t`, `char8_t`, `char16_t`, or
  `char32_t`, a specialization
  ``` cpp
  template<> struct formatter<ArithmeticT, charT>;
  ```
- For each `charT`, the pointer type specializations
  ``` cpp
  template<> struct formatter<nullptr_t, charT>;
  template<> struct formatter<void*, charT>;
  template<> struct formatter<const void*, charT>;
  ```

The `parse` member functions of these formatters interpret the format
specification as a *std-format-spec* as described in 
[[format.string.std]].

Unless specified otherwise, for each type `T` for which a `formatter`
specialization is provided by the library, each of the headers provides
the following specialization:

``` cpp
template<> inline constexpr bool enable_nonlocking_formatter_optimization<T> = true;
```

[*Note 1*: Specializations such as `formatter<wchar_t, char>` that
would require implicit multibyte / wide string or character conversion
are disabled. — *end note*]

The header `<format>` provides the following disabled specializations:

- The string type specializations
  ``` cpp
  template<> struct formatter<char*, wchar_t>;
  template<> struct formatter<const char*, wchar_t>;
  template<size_t N> struct formatter<char[N], wchar_t>;
  template<class traits, class Allocator>
    struct formatter<basic_string<char, traits, Allocator>, wchar_t>;
  template<class traits>
    struct formatter<basic_string_view<char, traits>, wchar_t>;
  ```

For any types `T` and `charT` for which neither the library nor the user
provides an explicit or partial specialization of the class template
`formatter`, `formatter<T, charT>` is disabled.

If the library provides an explicit or partial specialization of
`formatter<T, charT>`, that specialization is enabled and meets the
requirements except as noted otherwise.

If `F` is a disabled specialization of `formatter`, these values are
`false`:

- `is_default_constructible_v<F>`,
- `is_copy_constructible_v<F>`,
- `is_move_constructible_v<F>`,
- `is_copy_assignable_v<F>`, and
- `is_move_assignable_v<F>`.

An enabled specialization `formatter<T, charT>` meets the requirements
[[formatter.requirements]].

[*Example 1*:

``` cpp
#include <format>
#include <string>

enum color { red, green, blue };
const char* color_names[] = { "red", "green", "blue" };

template<> struct std::formatter<color> : std::formatter<const char*> {
  auto format(color c, format_context& ctx) const {
    return formatter<const char*>::format(color_names[c], ctx);
  }
};

struct err {};

std::string s0 = std::format("{}", 42);         // OK, library-provided formatter
std::string s1 = std::format("{}", L"foo");     // error: disabled formatter
std::string s2 = std::format("{}", red);        // OK, user-provided formatter
std::string s3 = std::format("{}", err{});      // error: disabled formatter
```

— *end example*]

#### Formatting escaped characters and strings <a id="format.string.escaped">[[format.string.escaped]]</a>

A character or string can be formatted as *escaped* to make it more
suitable for debugging or for logging.

The escaped string *E* representation of a string *S* is constructed by
encoding a sequence of characters as follows. The associated character
encoding *CE* for `charT` ([[lex.string.literal]]) is used to both
interpret *S* and construct *E*.

- U+0022 (quotation mark) (`"`) is appended to *E*.
- For each code unit sequence *X* in *S* that either encodes a single
  character, is a shift sequence, or is a sequence of ill-formed code
  units, processing is in order as follows:
  - If *X* encodes a single character *C*, then:
    - If *C* is one of the characters in [[format.escape.sequences]],
      then the two characters shown as the corresponding escape sequence
      are appended to *E*.
    - Otherwise, if *C* is not U+0020 (space) and
      - *CE* is UTF-8, UTF-16, or UTF-32 and *C* corresponds to a
        Unicode scalar value whose Unicode property `General_Category`
        has a value in the groups `Separator` (`Z`) or `Other` (`C`), as
        described by UAX \#44 of the Unicode Standard, or
      - *CE* is UTF-8, UTF-16, or UTF-32 and *C* corresponds to a
        Unicode scalar value with the Unicode property
        `Grapheme_Extend=Yes` as described by UAX \#44 of the Unicode
        Standard and *C* is not immediately preceded in *S* by a
        character *P* appended to *E* without translation to an escape
        sequence, or
      - *CE* is neither UTF-8, UTF-16, nor UTF-32 and *C* is one of an
        implementation-defined set of separator or non-printable
        characters

      then the sequence `\u{hex-digit-sequence}` is appended to *E*,
      where `hex-digit-sequence` is the shortest hexadecimal
      representation of *C* using lower-case hexadecimal digits.
    - Otherwise, *C* is appended to *E*.
  - Otherwise, if *X* is a shift sequence, the effect on *E* and further
    decoding of *S* is unspecified. *Recommended practice:* A shift
    sequence should be represented in *E* such that the original code
    unit sequence of *S* can be reconstructed.
  - Otherwise (*X* is a sequence of ill-formed code units), each code
    unit *U* is appended to *E* in order as the sequence
    `\x{hex-digit-sequence}`, where `hex-digit-sequence` is the shortest
    hexadecimal representation of *U* using lower-case hexadecimal
    digits.
- Finally, U+0022 (quotation mark) (`"`) is appended to *E*.

**Table: Mapping of characters to escape sequences**

| Character                     | Escape sequence |
| ----------------------------- | --------------- |
| U+0009 (character tabulation) | `\t`            |
| % U+000a (line feed)          | `\n`            |
| % U+000d (carriage return)    | `\r`            |
| % U+0022 (quotation mark)     | `\"`            |
| % U+005c (reverse solidus)    | ``              |


The escaped string representation of a character *C* is equivalent to
the escaped string representation of a string of *C*, except that:

- the result starts and ends with U+0027 (apostrophe) (`'`) instead of
  U+0022 (quotation mark) (`"`), and
- if *C* is U+0027 (apostrophe), the two characters `\'` are appended to
  *E*, and
- if *C* is U+0022 (quotation mark), then *C* is appended unchanged.

[*Example 1*:

``` cpp
string s0 = format("[{}]", "h\tllo");                   // s0 has value: [h\ \ \ \ llo]
string s1 = format("[{:?}]", "h\tllo");                 // s1 has value: ["h\ tllo"]
string s2 = format("[{:?}]", "\importexample[-2.5pt]{example_01}");  \kern1.25pt// s2 has value: ["\importexample[-2.5pt]{example_01"]}
string s3 = format("[{:?}, {:?}]", '\'', '"');          // s3 has value: ['\ '', '"']

// The following examples assume use of the UTF-8 encoding
string s4 = format("[{:?}]", string("\0 \n \t \x02 \x1b", 9));
                                                    // s4 has value: ["\ u{0\ \ n \ t \ u{2} \ u{1b}"]}
string s5 = format("[{:?}]", "\xc3\x28");           // invalid UTF-8, s5 has value: ["\ x{c3\("]}
string s6 = format("[{:?}]", "\importexample{example_02}");                 \kern0.75pt// s6 has value: ["\importexample{example_03{u}{200d}\importexample{example_04}"]}
string s7 = format("[{:?}]", "\u0301");             // s7 has value: ["\ u{301\"]}
string s8 = format("[{:?}]", "\\\u0301");           // s8 has value: ["\ \ \ u{301\"]}
string s9 = format("[{:?}]", "e\u0301\u0323");      // s9 has value: ["\importexample[-2pt]{example_06"]}
```

— *end example*]

#### Class template `basic_format_parse_context` <a id="format.parse.ctx">[[format.parse.ctx]]</a>

``` cpp
namespace std {
  template<class charT>
  class basic_format_parse_context {
  public:
    using char_type = charT;
    using const_iterator = basic_string_view<charT>::const_iterator;
    using iterator = const_iterator;

  private:
    iterator begin_;                                    // exposition only
    iterator end_;                                      // exposition only
    enum indexing { unknown, manual, automatic };       // exposition only
    indexing indexing_;                                 // exposition only
    size_t next_arg_id_;                                // exposition only
    size_t num_args_;                                   // exposition only

  public:
    constexpr explicit basic_format_parse_context(basic_string_view<charT> fmt) noexcept;
    basic_format_parse_context(const basic_format_parse_context&) = delete;
    basic_format_parse_context& operator=(const basic_format_parse_context&) = delete;

    constexpr const_iterator begin() const noexcept;
    constexpr const_iterator end() const noexcept;
    constexpr void advance_to(const_iterator it);

    constexpr size_t next_arg_id();
    constexpr void check_arg_id(size_t id);

    template<class... Ts>
      constexpr void check_dynamic_spec(size_t id) noexcept;
    constexpr void check_dynamic_spec_integral(size_t id) noexcept;
    constexpr void check_dynamic_spec_string(size_t id) noexcept;
  };
}
```

An instance of `basic_format_parse_context` holds the format string
parsing state, consisting of the format string range being parsed and
the argument counter for automatic indexing.

If a program declares an explicit or partial specialization of
`basic_format_parse_context`, the program is ill-formed, no diagnostic
required.

``` cpp
constexpr explicit basic_format_parse_context(basic_string_view<charT> fmt) noexcept;
```

*Effects:* Initializes `begin_` with `fmt.begin()`, `end_` with
`fmt.end()`, `indexing_` with `unknown`, `next_arg_id_` with `0`, and
`num_args_` with `0`.

[*Note 1*: Any call to `next_arg_id`, `check_arg_id`, or
`check_dynamic_spec` on an instance of `basic_format_parse_context`
initialized using this constructor is not a core constant
expression. — *end note*]

``` cpp
constexpr const_iterator begin() const noexcept;
```

*Returns:* `begin_`.

``` cpp
constexpr const_iterator end() const noexcept;
```

*Returns:* `end_`.

``` cpp
constexpr void advance_to(const_iterator it);
```

*Preconditions:* `end()` is reachable from `it`.

*Effects:* Equivalent to: `begin_ = it;`

``` cpp
constexpr size_t next_arg_id();
```

*Effects:* If `indexing_ != manual` is `true`, equivalent to:

``` cpp
if (indexing_ == unknown)
  indexing_ = automatic;
return next_arg_id_++;
```

*Throws:* `format_error` if `indexing_ == manual` is `true`.

[*Note 2*: This indicates mixing of automatic and manual argument
indexing. — *end note*]

*Remarks:* Let *`cur-arg-id`* be the value of `next_arg_id_` prior to
this call. Call expressions where *`cur-arg-id`*` >= num_args_` is
`true` are not core constant expressions [[expr.const]].

``` cpp
constexpr void check_arg_id(size_t id);
```

*Effects:* If `indexing_ != automatic` is `true`, equivalent to:

``` cpp
if (indexing_ == unknown)
  indexing_ = manual;
```

*Throws:* `format_error` if `indexing_ == automatic` is `true`.

[*Note 3*: This indicates mixing of automatic and manual argument
indexing. — *end note*]

*Remarks:* A call to this function is a core constant
expression [[expr.const]] only if `id < num_args_` is `true`.

``` cpp
template<class... Ts>
  constexpr void check_dynamic_spec(size_t id) noexcept;
```

*Mandates:* `sizeof...(Ts)` \ge 1. The types in `Ts...` are unique. Each
type in `Ts...` is one of `bool`, `char_type`, `int`, `unsigned int`,
`long long int`, `unsigned long long int`, `float`, `double`,
`long double`, `const char_type*`, `basic_string_view<char_type>`, or
`const void*`.

*Remarks:* A call to this function is a core constant expression only if

- `id < num_args_` is `true` and
- the type of the corresponding format argument (after conversion to
  `basic_format_arg<Context>`) is one of the types in `Ts...`.

``` cpp
constexpr void check_dynamic_spec_integral(size_t id) noexcept;
```

*Effects:* Equivalent to:

``` cpp
check_dynamic_spec<int, unsigned int, long long int, unsigned long long int>(id);
```

``` cpp
constexpr void check_dynamic_spec_string(size_t id) noexcept;
```

*Effects:* Equivalent to:

``` cpp
check_dynamic_spec<const char_type*, basic_string_view<char_type>>(id);
```

#### Class template `basic_format_context` <a id="format.context">[[format.context]]</a>

``` cpp
namespace std {
  template<class Out, class charT>
  class basic_format_context {
    basic_format_args<basic_format_context> args_;      // exposition only
    Out out_;                                           // exposition only

    basic_format_context(const basic_format_context&) = delete;
    basic_format_context& operator=(const basic_format_context&) = delete;

  public:
    using iterator = Out;
    using char_type = charT;
    template<class T> using formatter_type = formatter<T, charT>;

    basic_format_arg<basic_format_context> arg(size_t id) const noexcept;
    std::locale locale();

    iterator out();
    void advance_to(iterator it);
  };
}
```

An instance of `basic_format_context` holds formatting state consisting
of the formatting arguments and the output iterator.

If a program declares an explicit or partial specialization of
`basic_format_context`, the program is ill-formed, no diagnostic
required.

`Out` shall model `output_iterator<const charT&>`.

`format_context` is an alias for a specialization of
`basic_format_context` with an output iterator that appends to `string`,
such as `back_insert_iterator<string>`. Similarly, `wformat_context` is
an alias for a specialization of `basic_format_context` with an output
iterator that appends to `wstring`.

*Recommended practice:* For a given type `charT`, implementations should
provide a single instantiation of `basic_format_context` for appending
to `basic_string<charT>`, `vector<charT>`, or any other container with
contiguous storage by wrapping those in temporary objects with a uniform
interface (such as a `span<charT>`) and polymorphic reallocation.

``` cpp
basic_format_arg<basic_format_context> arg(size_t id) const noexcept;
```

*Returns:* `args_.get(id)`.

``` cpp
std::locale locale();
```

*Returns:* The locale passed to the formatting function if the latter
takes one, and `std::locale()` otherwise.

``` cpp
iterator out();
```

*Effects:* Equivalent to: `return std::move(out_);`

``` cpp
void advance_to(iterator it);
```

*Effects:* Equivalent to: `out_ = std::move(it);`

[*Example 1*:

``` cpp
struct S { int value; };

template<> struct std::formatter<S> {
  size_t width_arg_id = 0;

  // Parses a width argument id in the format { digit }.
  constexpr auto parse(format_parse_context& ctx) {
    auto iter = ctx.begin();
    auto is_digit = [](auto c) { return c >= '0' && c <= '9'; };
    auto get_char = [&]() { return iter != ctx.end() ? *iter : 0; };
    if (get_char() != '{')
      return iter;
    ++iter;
    char c = get_char();
    if (!is_digit(c) || (++iter, get_char()) != '}')
      throw format_error("invalid format");
    width_arg_id = c - '0';
    ctx.check_arg_id(width_arg_id);
    return ++iter;
  }

  // Formats an S with width given by the argument width_arg_id.
  auto format(S s, format_context& ctx) const {
    int width = ctx.arg(width_arg_id).visit([](auto value) -> int {
      if constexpr (!is_integral_v<decltype(value)>)
        throw format_error("width is not integral");
      else if (value < 0 || value > numeric_limits<int>::max())
        throw format_error("invalid width");
      else
        return value;
      });
    return format_to(ctx.out(), "{0:x>{1}}", s.value, width);
  }
};

std::string s = std::format("{0:{1}}", S{42}, 10);  // value of s is "xxxxxxxx42"
```

— *end example*]

### Formatting of ranges <a id="format.range">[[format.range]]</a>

#### Variable template `format_kind` <a id="format.range.fmtkind">[[format.range.fmtkind]]</a>

``` cpp
template<ranges::input_range R>
    requires same_as<R, remove_cvref_t<R>>
  constexpr range_format format_kind<R> = see below;
```

A program that instantiates the primary template of `format_kind` is
ill-formed.

For a type `R`, `format_kind<R>` is defined as follows:

- If `same_as<remove_cvref_t<ranges::range_reference_t<R>>, R>` is
  `true`, `format_kind<R>` is `range_format::disabled`. \[*Note 1*: This
  prevents constraint recursion for ranges whose reference type is the
  same range type. For example, `std::filesystem::path` is a range of
  `std::filesystem::path`. — *end note*]
- Otherwise, if the *qualified-id* `R::key_type` is valid and denotes a
  type:
  - If the *qualified-id* `R::mapped_type` is valid and denotes a type,
    let `U` be `remove_cvref_t<ranges::range_reference_t<R>>`. If either
    `U` is a specialization of `pair` or `U` is a specialization of
    `tuple` and `tuple_size_v<U> == 2`, `format_kind<R>` is
    `range_format::map`.
  - Otherwise, `format_kind<R>` is `range_format::set`.
- Otherwise, `format_kind<R>` is `range_format::sequence`.

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`format_kind` for cv-unqualified program-defined types that model
`ranges::input_range`. Such specializations shall be usable in constant
expressions [[expr.const]] and have type `const range_format`.

#### Class template `range_formatter` <a id="format.range.formatter">[[format.range.formatter]]</a>

``` cpp
namespace std {
  template<class T, class charT = char>
    requires same_as<remove_cvref_t<T>, T> && formattable<T, charT>
  class range_formatter {
    formatter<T, charT> underlying_;                                          // exposition only
    basic_string_view<charT> separator_ = STATICALLY-WIDEN<charT>(", ");      // exposition only
    basic_string_view<charT> opening-bracket_ = STATICALLY-WIDEN<charT>("["); // exposition only
    basic_string_view<charT> closing-bracket_ = STATICALLY-WIDEN<charT>("]"); // exposition only

  public:
    constexpr void set_separator(basic_string_view<charT> sep) noexcept;
    constexpr void set_brackets(basic_string_view<charT> opening,
                                basic_string_view<charT> closing) noexcept;
    constexpr formatter<T, charT>& underlying() noexcept { return underlying_; }
    constexpr const formatter<T, charT>& underlying() const noexcept { return underlying_; }

    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<ranges::input_range R, class FormatContext>
        requires formattable<ranges::range_reference_t<R>, charT> &&
                 same_as<remove_cvref_t<ranges::range_reference_t<R>>, T>
      typename FormatContext::iterator
        format(R&& r, FormatContext& ctx) const;
  };
}
```

The class template `range_formatter` is a utility for implementing
`formatter` specializations for range types.

`range_formatter` interprets *format-spec* as a *range-format-spec*. The
syntax of format specifications is as follows:

``` bnf
\fmtnontermdef{range-format-spec}
    range-fill-and-alignₒₚₜ widthₒₚₜ 'n'ₒₚₜ range-typeₒₚₜ range-underlying-specₒₚₜ
```

``` bnf
\fmtnontermdef{range-fill-and-align}
    range-fillₒₚₜ align
```

``` bnf
\fmtnontermdef{range-fill}
    any character other than \terminal{\ or \terminal{\}} or \terminal{:}
```

``` bnf
\fmtnontermdef{range-type}
    'm'
    's'
    '?s'
```

``` bnf
\fmtnontermdef{range-underlying-spec}
    ':' format-spec
```

For `range_formatter<T, charT>`, the *format-spec* in a
*range-underlying-spec*, if any, is interpreted by
`formatter<T, charT>`.

The *range-fill-and-align* is interpreted the same way as a
*fill-and-align* [[format.string.std]]. The productions *align* and
*width* are described in [[format.string]].

The `n` option causes the range to be formatted without the opening and
closing brackets.

[*Note 1*: This is equivalent to invoking
`set_brackets({}, {})`. — *end note*]

The *range-type* specifier changes the way a range is formatted, with
certain options only valid with certain argument types. The meaning of
the various type options is as specified in [[formatter.range.type]].

**Table: Meaning of range-type options**

| Option | Requirements                                                                                                      | Meaning                                                                                                                                                                                                                                                                                                                                |
| ------ | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| % `m`  | `T` shall be either a specialization of `pair` or a specialization of `tuple` such that `tuple_size_v<T>` is `2`. | Indicates that the opening bracket should be `"{"`, the closing bracket should be `"}"`, the separator should be `", "`, and each range element should be formatted as if `m` were specified for its tuple-type. *If the `n` option is provided in addition to the `m` option, both the opening and closing brackets are still empty.* |
| % `s`  | `T` shall be `charT`.                                                                                             | Indicates that the range should be formatted as a `string`.                                                                                                                                                                                                                                                                            |
| % `?s` | `T` shall be `charT`.                                                                                             | Indicates that the range should be formatted as an escaped string [[format.string.escaped]].                                                                                                                                                                                                                                           |


If the *range-type* is `s` or `?s`, then there shall be no `n` option
and no *range-underlying-spec*.

``` cpp
constexpr void set_separator(basic_string_view<charT> sep) noexcept;
```

*Effects:* Equivalent to: *`separator_`*` = sep;`

``` cpp
constexpr void set_brackets(basic_string_view<charT> opening,
                            basic_string_view<charT> closing) noexcept;
```

*Effects:* Equivalent to:

``` cpp
opening-bracket_ = opening;
closing-bracket_ = closing;
```

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Parses the format specifiers as a *range-format-spec* and
stores the parsed specifiers in `*this`. Calls
*`underlying_`*`.parse(ctx)` to parse *format-spec* in
*range-format-spec* or, if the latter is not present, an empty
*format-spec*. The values of *opening-bracket\_*, *closing-bracket\_*,
and *separator\_* are modified if and only if required by the
*range-type* or the `n` option, if present. If:

- the *range-type* is neither `s` nor `?s`,
- *`underlying_`*`.set_debug_format()` is a valid expression, and
- there is no *range-underlying-spec*,

then calls *`underlying_`*`.set_debug_format()`.

*Returns:* An iterator past the end of the *range-format-spec*.

``` cpp
template<ranges::input_range R, class FormatContext>
    requires formattable<ranges::range_reference_t<R>, charT> &&
             same_as<remove_cvref_t<ranges::range_reference_t<R>>, T>
  typename FormatContext::iterator
    format(R&& r, FormatContext& ctx) const;
```

*Effects:* Writes the following into `ctx.out()`, adjusted according to
the *range-format-spec*:

- If the *range-type* was `s`, then as if by formatting
  `basic_string<charT>(from_range, r)`.
- Otherwise, if the *range-type* was `?s`, then as if by formatting
  `basic_string<charT>(from_range, r)` as an escaped
  string [[format.string.escaped]].
- Otherwise,
  - *opening-bracket\_*,
  - for each element `e` of the range `r`:
    - the result of writing `e` via *underlying\_* and
    - *separator\_*, unless `e` is the last element of `r`, and
  - *closing-bracket\_*.

*Returns:* An iterator past the end of the output range.

#### Class template *range-default-formatter* <a id="format.range.fmtdef">[[format.range.fmtdef]]</a>

``` cpp
namespace std {
  template<ranges::input_range R, class charT>
  struct range-default-formatter<range_format::sequence, R, charT> {    // exposition only
  private:
    using maybe-const-r = fmt-maybe-const<R, charT>;                    // exposition only
    range_formatter<remove_cvref_t<ranges::range_reference_t<maybe-const-r>>,
                    charT> underlying_;                                 // exposition only

  public:
    constexpr void set_separator(basic_string_view<charT> sep) noexcept;
    constexpr void set_brackets(basic_string_view<charT> opening,
                                basic_string_view<charT> closing) noexcept;

    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(maybe-const-r& elems, FormatContext& ctx) const;
  };
}
```

``` cpp
constexpr void set_separator(basic_string_view<charT> sep) noexcept;
```

*Effects:* Equivalent to: *`underlying_`*`.set_separator(sep);`

``` cpp
constexpr void set_brackets(basic_string_view<charT> opening,
                            basic_string_view<charT> closing) noexcept;
```

*Effects:* Equivalent to:
*`underlying_`*`.set_brackets(opening, closing);`

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Equivalent to: `return `*`underlying_`*`.parse(ctx);`

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(maybe-const-r& elems, FormatContext& ctx) const;
```

*Effects:* Equivalent to: `return `*`underlying_`*`.format(elems, ctx);`

#### Specialization of *range-default-formatter* for maps <a id="format.range.fmtmap">[[format.range.fmtmap]]</a>

``` cpp
namespace std {
  template<ranges::input_range R, class charT>
  struct range-default-formatter<range_format::map, R, charT> {
  private:
    using maybe-const-map = fmt-maybe-const<R, charT>;                  // exposition only
    using element-type =                                                // exposition only
      remove_cvref_t<ranges::range_reference_t<maybe-const-map>>;
    range_formatter<element-type, charT> underlying_;                   // exposition only

  public:
    constexpr range-default-formatter();

    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(maybe-const-map& r, FormatContext& ctx) const;
  };
}
```

``` cpp
constexpr range-default-formatter();
```

*Mandates:* Either:

- *element-type* is a specialization of `pair`, or
- *element-type* is a specialization of `tuple` and
  `tuple_size_v<`*`element-type`*`> == 2`.

*Effects:* Equivalent to:

``` cpp
underlying_.set_brackets(STATICALLY-WIDEN<charT>("{"), STATICALLY-WIDEN<charT>("}"));
underlying_.underlying().set_brackets({}, {});
underlying_.underlying().set_separator(STATICALLY-WIDEN<charT>(": "));
```

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Equivalent to: `return `*`underlying_`*`.parse(ctx);`

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(maybe-const-map& r, FormatContext& ctx) const;
```

*Effects:* Equivalent to: `return `*`underlying_`*`.format(r, ctx);`

#### Specialization of *range-default-formatter* for sets <a id="format.range.fmtset">[[format.range.fmtset]]</a>

``` cpp
namespace std {
  template<ranges::input_range R, class charT>
  struct range-default-formatter<range_format::set, R, charT> {
  private:
    using maybe-const-set = fmt-maybe-const<R, charT>;                  // exposition only
    range_formatter<remove_cvref_t<ranges::range_reference_t<maybe-const-set>>,
                    charT> underlying_;                                 // exposition only

  public:
    constexpr range-default-formatter();

    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(maybe-const-set& r, FormatContext& ctx) const;
  };
}
```

``` cpp
constexpr range-default-formatter();
```

*Effects:* Equivalent to:

``` cpp
underlying_.set_brackets(STATICALLY-WIDEN<charT>("{"), STATICALLY-WIDEN<charT>("}"));
```

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Equivalent to: `return `*`underlying_`*`.parse(ctx);`

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(maybe-const-set& r, FormatContext& ctx) const;
```

*Effects:* Equivalent to: `return `*`underlying_`*`.format(r, ctx);`

#### Specialization of *range-default-formatter* for strings <a id="format.range.fmtstr">[[format.range.fmtstr]]</a>

``` cpp
namespace std {
  template<range_format K, ranges::input_range R, class charT>
    requires (K == range_format::string || K == range_format::debug_string)
  struct range-default-formatter<K, R, charT> {
  private:
    formatter<basic_string<charT>, charT> underlying_;                  // exposition only

  public:
    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(see below& str, FormatContext& ctx) const;
  };
}
```

*Mandates:* `same_as<remove_cvref_t<range_reference_t<R>>, charT>` is
`true`.

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Equivalent to:

``` cpp
auto i = underlying_.parse(ctx);
if constexpr (K == range_format::debug_string) {
  underlying_.set_debug_format();
}
return i;
```

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(see below& r, FormatContext& ctx) const;
```

The type of `r` is `const R&` if `ranges::input_range<const R>` is
`true` and `R&` otherwise.

*Effects:* Let *`s`* be a `basic_string<charT>` such that
`ranges::equal(`*`s`*`, r)` is `true`. Equivalent to:
`return `*`underlying_`*`.format(`*`s`*`, ctx);`

### Arguments <a id="format.arguments">[[format.arguments]]</a>

#### Class template `basic_format_arg` <a id="format.arg">[[format.arg]]</a>

``` cpp
namespace std {
  template<class Context>
  class basic_format_arg {
  public:
    class handle;

  private:
    using char_type = Context::char_type;                                       // exposition only

    variant<monostate, bool, char_type,
            int, unsigned int, long long int, unsigned long long int,
            float, double, long double,
            const char_type*, basic_string_view<char_type>,
            const void*, handle> value;                                         // exposition only

    template<class T> explicit basic_format_arg(T& v) noexcept;                 // exposition only

  public:
    basic_format_arg() noexcept;

    explicit operator bool() const noexcept;

    template<class Visitor>
      decltype(auto) visit(this basic_format_arg arg, Visitor&& vis);
    template<class R, class Visitor>
      R visit(this basic_format_arg arg, Visitor&& vis);
  };
}
```

An instance of `basic_format_arg` provides access to a formatting
argument for user-defined formatters.

The behavior of a program that adds specializations of
`basic_format_arg` is undefined.

``` cpp
basic_format_arg() noexcept;
```

*Ensures:* `!(*this)`.

``` cpp
template<class T> explicit basic_format_arg(T& v) noexcept;
```

*Constraints:* `T` satisfies `formattable-with<Context>`.

*Preconditions:* If `decay_t<T>` is `char_type*` or `const char_type*`,
`static_cast<const char_type*>(v)` points to an NTCTS [[defns.ntcts]].

*Effects:* Let `TD` be `remove_const_t<T>`.

- If `TD` is `bool` or `char_type`, initializes `value` with `v`;
- otherwise, if `TD` is `char` and `char_type` is `wchar_t`, initializes
  `value` with `static_cast<wchar_t>(static_cast<unsigned char>(v))`;
- otherwise, if `TD` is a signed integer type [[basic.fundamental]] and
  `sizeof(TD) <= sizeof(int)`, initializes `value` with
  `static_cast<int>(v)`;
- otherwise, if `TD` is an unsigned integer type and
  `sizeof(TD) <= sizeof(unsigned int)`, initializes `value` with
  `static_cast<unsigned int>(v)`;
- otherwise, if `TD` is a signed integer type and
  `sizeof(TD) <= sizeof(long long int)`, initializes `value` with
  `static_cast<long long int>(v)`;
- otherwise, if `TD` is an unsigned integer type and
  `sizeof(TD) <= sizeof(unsigned long long int)`, initializes `value`
  with `static_cast<unsigned long long int>(v)`;
- otherwise, if `TD` is a standard floating-point type, initializes
  `value` with `v`;
- otherwise, if `TD` is a specialization of `basic_string_view` or
  `basic_string` and `TD::value_type` is `char_type`, initializes
  `value` with `basic_string_view<char_type>(v.data(), v.size())`;
- otherwise, if `decay_t<TD>` is `char_type*` or `const char_type*`,
  initializes `value` with `static_cast<const char_type*>(v)`;
- otherwise, if `is_void_v<remove_pointer_t<TD>>` is `true` or
  `is_null_pointer_v<TD>` is `true`, initializes `value` with
  `static_cast<const void*>(v)`;
- otherwise, initializes `value` with `handle(v)`.

[*Note 1*: Constructing `basic_format_arg` from a pointer to a member
is ill-formed unless the user provides an enabled specialization of
`formatter` for that pointer to member type. — *end note*]

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `!holds_alternative<monostate>(value)`.

``` cpp
template<class Visitor>
  decltype(auto) visit(this basic_format_arg arg, Visitor&& vis);
```

*Effects:* Equivalent to:
`return arg.value.visit(std::forward<Visitor>(vis));`

``` cpp
template<class R, class Visitor>
  R visit(this basic_format_arg arg, Visitor&& vis);
```

*Effects:* Equivalent to:
`return arg.value.visit<R>(std::forward<Visitor>(vis));`

The class `handle` allows formatting an object of a user-defined type.

``` cpp
namespace std {
  template<class Context>
  class basic_format_arg<Context>::handle {
    const void* ptr_;                                           // exposition only
    void (*format_)(basic_format_parse_context<char_type>&,
                    Context&, const void*);                     // exposition only

    template<class T> explicit handle(T& val) noexcept;         // exposition only

  public:
    void format(basic_format_parse_context<char_type>&, Context& ctx) const;
  };
}
```

``` cpp
template<class T> explicit handle(T& val) noexcept;
```

Let

- `TD` be `remove_const_t<T>`,
- `TQ` be `const TD` if `const TD` satisfies `formattable-with<Context>`
  and `TD` otherwise.

*Mandates:* `TQ` satisfies `formattable-with<Context>`.

*Effects:* Initializes `ptr_` with `addressof(val)` and `format_` with

``` cpp
[](basic_format_parse_context<char_type>& parse_ctx,
   Context& format_ctx, const void* ptr) {
  typename Context::template formatter_type<TD> f;
  parse_ctx.advance_to(f.parse(parse_ctx));
  format_ctx.advance_to(f.format(*const_cast<TQ*>(static_cast<const TD*>(ptr)),
                                 format_ctx));
}
```

``` cpp
void format(basic_format_parse_context<char_type>& parse_ctx, Context& format_ctx) const;
```

*Effects:* Equivalent to: `format_(parse_ctx, format_ctx, ptr_);`

#### Class template *format-arg-store* <a id="format.arg.store">[[format.arg.store]]</a>

``` cpp
namespace std {
  template<class Context, class... Args>
  class format-arg-store {                                      // exposition only
    array<basic_format_arg<Context>, sizeof...(Args)> args;     // exposition only
  };
}
```

An instance of *format-arg-store* stores formatting arguments.

``` cpp
template<class Context = format_context, class... Args>
  format-arg-store<Context, Args...> make_format_args(Args&... fmt_args);
```

*Preconditions:* The type
`typename Context::template formatter_type<remove_const_t<``Tᵢ``>>`
meets the requirements [[formatter.requirements]] for each `Tᵢ` in
`Args`.

*Returns:* An object of type *`format-arg-store`*`<Context, Args...>`
whose *args* data member is initialized with
`{basic_format_arg<Context>(fmt_args)...}`.

``` cpp
template<class... Args>
  format-arg-store<wformat_context, Args...> make_wformat_args(Args&... args);
```

*Effects:* Equivalent to:
`return make_format_args<wformat_context>(args...);`

#### Class template `basic_format_args` <a id="format.args">[[format.args]]</a>

``` cpp
namespace std {
  template<class Context>
  class basic_format_args {
    size_t size_;                               // exposition only
    const basic_format_arg<Context>* data_;     // exposition only

  public:
    template<class... Args>
      basic_format_args(const format-arg-store<Context, Args...>& store) noexcept;

    basic_format_arg<Context> get(size_t i) const noexcept;
  };

  template<class Context, class... Args>
    basic_format_args(format-arg-store<Context, Args...>) -> basic_format_args<Context>;
}
```

An instance of `basic_format_args` provides access to formatting
arguments. Implementations should optimize the representation of
`basic_format_args` for a small number of formatting arguments.

[*Note 1*: For example, by storing indices of type alternatives
separately from values and packing the former. — *end note*]

``` cpp
template<class... Args>
  basic_format_args(const format-arg-store<Context, Args...>& store) noexcept;
```

*Effects:* Initializes `size_` with `sizeof...(Args)` and `data_` with
`store.args.data()`.

``` cpp
basic_format_arg<Context> get(size_t i) const noexcept;
```

*Returns:* `i < size_ ? data_[i] : basic_format_arg<Context>()`.

### Tuple formatter <a id="format.tuple">[[format.tuple]]</a>

For each of `pair` and `tuple`, the library provides the following
formatter specialization where `pair-or-tuple` is the name of the
template:

``` cpp
namespace std {
  template<class charT, formattable<charT>... Ts>
  struct formatter<pair-or-tuple<Ts...>, charT> {
  private:
    tuple<formatter<remove_cvref_t<Ts>, charT>...> underlying_;               // exposition only
    basic_string_view<charT> separator_ = STATICALLY-WIDEN<charT>(", ");      // exposition only
    basic_string_view<charT> opening-bracket_ = STATICALLY-WIDEN<charT>("("); // exposition only
    basic_string_view<charT> closing-bracket_ = STATICALLY-WIDEN<charT>(")"); // exposition only

  public:
    constexpr void set_separator(basic_string_view<charT> sep) noexcept;
    constexpr void set_brackets(basic_string_view<charT> opening,
                                basic_string_view<charT> closing) noexcept;

    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(see below& elems, FormatContext& ctx) const;
  };

  template<class... Ts>
    constexpr bool enable_nonlocking_formatter_optimization<pair-or-tuple<Ts...>> =
      (enable_nonlocking_formatter_optimization<Ts> && ...);
}
```

The `parse` member functions of these formatters interpret the format
specification as a *tuple-format-spec* according to the following
syntax:

``` bnf
\fmtnontermdef{tuple-format-spec}
    tuple-fill-and-alignₒₚₜ widthₒₚₜ tuple-typeₒₚₜ
```

``` bnf
\fmtnontermdef{tuple-fill-and-align}
    tuple-fillₒₚₜ align
```

``` bnf
\fmtnontermdef{tuple-fill}
    any character other than \terminal{\ or \terminal{\}} or \terminal{:}
```

``` bnf
\fmtnontermdef{tuple-type}
    'm'
    'n'
```

The *tuple-fill-and-align* is interpreted the same way as a
*fill-and-align* [[format.string.std]]. The productions *align* and
*width* are described in [[format.string]].

The *tuple-type* specifier changes the way a `pair` or `tuple` is
formatted, with certain options only valid with certain argument types.
The meaning of the various type options is as specified in
[[formatter.tuple.type]].

**Table: Meaning of tuple-type options**

| Option | Requirements | Meaning                                |
| ------ | ------------ | -------------------------------------- |
| <charT>(": ")); set_brackets({}, {}); \end{codeblock}% |
| % `n`  | none         | Equivalent to: `set_brackets({}, {});` |
| % none | none         | No effects                             |

``` cpp
constexpr void set_separator(basic_string_view<charT> sep) noexcept;
```

*Effects:* Equivalent to: *`separator_`*` = sep;`

``` cpp
constexpr void set_brackets(basic_string_view<charT> opening,
                            basic_string_view<charT> closing) noexcept;
```

*Effects:* Equivalent to:

``` cpp
opening-bracket_ = opening;
closing-bracket_ = closing;
```

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Parses the format specifiers as a *tuple-format-spec* and
stores the parsed specifiers in `*this`. The values of
*opening-bracket\_*, *closing-bracket\_*, and *separator\_* are modified
if and only if required by the *tuple-type*, if present. For each
element *`e`* in *underlying\_*, calls *`e`*`.parse(ctx)` to parse an
empty *format-spec* and, if *`e`*`.set_debug_format()` is a valid
expression, calls *`e`*`.set_debug_format()`.

*Returns:* An iterator past the end of the *tuple-format-spec*.

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(see below& elems, FormatContext& ctx) const;
```

The type of `elems` is:

- If `(formattable<const Ts, charT> && ...)` is `true`,
  `const `*`pair-or-tuple`*`<Ts...>&`.
- Otherwise *`pair-or-tuple`*`<Ts...>&`.

*Effects:* Writes the following into `ctx.out()`, adjusted according to
the *tuple-format-spec*:

- *opening-bracket\_*,
- for each index `I` in the \[`0`, `sizeof...(Ts)`):
  - if `I != 0`, *separator\_*,
  - the result of writing `get<I>(elems)` via
    `get<I>(`*`underlying_`*`)`, and
- *closing-bracket\_*.

*Returns:* An iterator past the end of the output range.

### Class `format_error` <a id="format.error">[[format.error]]</a>

``` cpp
namespace std {
  class format_error : public runtime_error {
  public:
    constexpr explicit format_error(const string& what_arg);
    constexpr explicit format_error(const char* what_arg);
  };
}
```

The class `format_error` defines the type of objects thrown as
exceptions to report errors from the formatting library.

``` cpp
constexpr format_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
constexpr format_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

## Regular expressions library <a id="re">[[re]]</a>

### General <a id="re.general">[[re.general]]</a>

Subclause [[re]] describes components that C++ programs may use to
perform operations involving regular expression matching and searching.

The following subclauses describe a basic regular expression class
template and its traits that can handle char-like [[strings.general]]
template arguments, two specializations of this class template that
handle sequences of `char` and `wchar_t`, a class template that holds
the result of a regular expression match, a series of algorithms that
allow a character sequence to be operated upon by a regular expression,
and two iterator types for enumerating regular expression matches, as
summarized in [[re.summary]].

**Table: Regular expressions library summary**

| Subclause       |                             | Header    |
| --------------- | --------------------------- | --------- |
| [[re.req]]      | Requirements                |           |
| [[re.const]]    | Constants                   | `<regex>` |
| [[re.badexp]]   | Exception type              |           |
| [[re.traits]]   | Traits                      |           |
| [[re.regex]]    | Regular expression template |           |
| [[re.submatch]] | Submatches                  |           |
| [[re.results]]  | Match results               |           |
| [[re.alg]]      | Algorithms                  |           |
| [[re.iter]]     | Iterators                   |           |
| [[re.grammar]]  | Grammar                     |           |


The ECMAScript Language Specification described in Standard Ecma-262 is
called *ECMA-262* in this Clause.

### Requirements <a id="re.req">[[re.req]]</a>

This subclause defines requirements on classes representing regular
expression traits.

[*Note 1*: The class template `regex_traits`, defined in [[re.traits]],
meets these requirements. — *end note*]

The class template `basic_regex`, defined in [[re.regex]], needs a set
of related types and functions to complete the definition of its
semantics. These types and functions are provided as a set of member
*typedef-name*s and functions in the template parameter `traits` used by
the `basic_regex` class template. This subclause defines the semantics
of these members.

To specialize class template `basic_regex` for a character container
`CharT` and its related regular expression traits class `Traits`, use
`basic_regex<CharT, Traits>`.

In the following requirements,

- `X` denotes a traits class defining types and functions for the
  character container type `charT`;
- `u` is an object of type `X`;
- `v` is an object of type `const X`;
- `p` is a value of type `const charT*`;
- `I1` and `I2` are input iterators [[input.iterators]];
- `F1` and `F2` are forward iterators [[forward.iterators]];
- `c` is a value of type `const charT`;
- `s` is an object of type `X::string_type`;
- `cs` is an object of type `const X::string_type`;
- `b` is a value of type `bool`;
- `I` is a value of type `int`;
- `cl` is an object of type `X::char_class_type`; and
- `loc` is an object of type `X::locale_type`.

A traits class `X` meets the regular expression traits requirements if
the following types and expressions are well-formed and have the
specified semantics.

``` cpp
typename X::char_type
```

*Result:* `charT`, the character container type used in the
implementation of class template `basic_regex`.

``` cpp
typename X::string_type
```

*Result:* `basic_string<charT>`

``` cpp
typename X::locale_type
```

*Result:* A copy constructible type that represents the locale used by
the traits class.

``` cpp
typename X::char_class_type
```

*Result:* A bitmask type [[bitmask.types]] representing a particular
character classification.

``` cpp
X::length(p)
```

*Result:* `size_t`

*Returns:* The smallest `i` such that `p[i] == 0`.

*Complexity:* Linear in `i`.

``` cpp
v.translate(c)
```

*Result:* `X::char_type`

*Returns:* A character such that for any character `d` that is to be
considered equivalent to `c` then `v.translate(c) == v.translate(d)`.

``` cpp
v.translate_nocase(c)
```

*Result:* `X::char_type`

*Returns:* For all characters `C` that are to be considered equivalent
to `c` when comparisons are to be performed without regard to case, then
`v.translate_nocase(c) == v.translate_nocase(C)`.

``` cpp
v.transform(F1, F2)
```

*Result:* `X::string_type`

*Returns:* A sort key for the character sequence designated by the
iterator range \[`F1`, `F2`) such that if the character sequence \[`G1`,
`G2`) sorts before the character sequence \[`H1`, `H2`) then
`v.transform(G1, G2) < v.transform(H1, H2)`.

``` cpp
v.transform_primary(F1, F2)
```

*Result:* `X::string_type`

*Returns:* A sort key for the character sequence designated by the
iterator range \[`F1`, `F2`) such that if the character sequence \[`G1`,
`G2`) sorts before the character sequence \[`H1`, `H2`) when character
case is not considered then
`v.transform_primary(G1, G2) < v.transform_primary(H1, H2)`.

``` cpp
v.lookup_collatename(F1, F2)
```

*Result:* `X::string_type`

*Returns:* A sequence of characters that represents the collating
element consisting of the character sequence designated by the iterator
range \[`F1`, `F2`). Returns an empty string if the character sequence
is not a valid collating element.

``` cpp
v.lookup_classname(F1, F2, b)
```

*Result:* `X::char_class_type`

*Returns:* Converts the character sequence designated by the iterator
range \[`F1`, `F2`) into a value of a bitmask type that can subsequently
be passed to `isctype`. Values returned from `lookup_classname` can be
bitwise ’ed together; the resulting value represents membership in
either of the corresponding character classes. If `b` is `true`, the
returned bitmask is suitable for matching characters without regard to
their case. Returns `0` if the character sequence is not the name of a
character class recognized by `X`. The value returned shall be
independent of the case of the characters in the sequence.

``` cpp
v.isctype(c, cl)
```

*Result:* `bool`

*Returns:* Returns `true` if character `c` is a member of one of the
character classes designated by `cl`, `false` otherwise.

``` cpp
v.value(c, I)
```

*Result:* `int`

*Returns:* Returns the value represented by the digit *c* in base *I* if
the character *c* is a valid digit in base *I*; otherwise returns `-1`.

[*Note 1*: The value of *I* will only be 8, 10, or 16. — *end note*]

``` cpp
u.imbue(loc)
```

*Result:* `X::locale_type`

*Effects:* Imbues `u` with the locale `loc` and returns the previous
locale used by `u` if any.

``` cpp
v.getloc()
```

*Result:* `X::locale_type`

*Returns:* Returns the current locale used by `v`, if any.

[*Note 2*: Class template `regex_traits` meets the requirements for a
regular expression traits class when it is specialized for `char` or
`wchar_t`. This class template is described in the header `<regex>`, and
is described in [[re.traits]]. — *end note*]

### Header `<regex>` synopsis <a id="re.syn">[[re.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [re.const], regex constants
  namespace regex_constants {
    using syntax_option_type = T1;
    using match_flag_type = T2;
    using error_type = T3;
  }

  // [re.badexp], class regex_error
  class regex_error;

  // [re.traits], class template regex_traits
  template<class charT> struct regex_traits;

  // [re.regex], class template basic_regex
  template<class charT, class traits = regex_traits<charT>> class basic_regex;

  using regex  = basic_regex<char>;
  using wregex = basic_regex<wchar_t>;

  // [re.regex.swap], basic_regex swap
  template<class charT, class traits>
    void swap(basic_regex<charT, traits>& e1, basic_regex<charT, traits>& e2);

  // [re.submatch], class template sub_match
  template<class BidirectionalIterator>
    class sub_match;

  using csub_match  = sub_match<const char*>;
  using wcsub_match = sub_match<const wchar_t*>;
  using ssub_match  = sub_match<string::const_iterator>;
  using wssub_match = sub_match<wstring::const_iterator>;

  // [re.submatch.op], sub_match non-member operators
  template<class BiIter>
    bool operator==(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
  template<class BiIter>
    auto operator<=>(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);

  template<class BiIter, class ST, class SA>
    bool operator==(
      const sub_match<BiIter>& lhs,
      const basic_string<typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
  template<class BiIter, class ST, class SA>
    auto operator<=>(
      const sub_match<BiIter>& lhs,
      const basic_string<typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);

  template<class BiIter>
    bool operator==(const sub_match<BiIter>& lhs,
                    const typename iterator_traits<BiIter>::value_type* rhs);
  template<class BiIter>
    auto operator<=>(const sub_match<BiIter>& lhs,
                     const typename iterator_traits<BiIter>::value_type* rhs);

  template<class BiIter>
    bool operator==(const sub_match<BiIter>& lhs,
                    const typename iterator_traits<BiIter>::value_type& rhs);
  template<class BiIter>
    auto operator<=>(const sub_match<BiIter>& lhs,
                     const typename iterator_traits<BiIter>::value_type& rhs);

  template<class charT, class ST, class BiIter>
    basic_ostream<charT, ST>&
      operator<<(basic_ostream<charT, ST>& os, const sub_match<BiIter>& m);

  // [re.results], class template match_results
  template<class BidirectionalIterator,
           class Allocator = allocator<sub_match<BidirectionalIterator>>>
    class match_results;

  using cmatch  = match_results<const char*>;
  using wcmatch = match_results<const wchar_t*>;
  using smatch  = match_results<string::const_iterator>;
  using wsmatch = match_results<wstring::const_iterator>;

  // match_results comparisons
  template<class BidirectionalIterator, class Allocator>
    bool operator==(const match_results<BidirectionalIterator, Allocator>& m1,
                    const match_results<BidirectionalIterator, Allocator>& m2);

  // [re.results.swap], match_results swap
  template<class BidirectionalIterator, class Allocator>
    void swap(match_results<BidirectionalIterator, Allocator>& m1,
              match_results<BidirectionalIterator, Allocator>& m2);

  // [re.alg.match], function template regex_match
  template<class BidirectionalIterator, class Allocator, class charT, class traits>
    bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                     match_results<BidirectionalIterator, Allocator>& m,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class BidirectionalIterator, class charT, class traits>
    bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class charT, class Allocator, class traits>
    bool regex_match(const charT* str, match_results<const charT*, Allocator>& m,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class ST, class SA, class Allocator, class charT, class traits>
    bool regex_match(const basic_string<charT, ST, SA>& s,
                     match_results<typename basic_string<charT, ST, SA>::const_iterator,
                                   Allocator>& m,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class ST, class SA, class Allocator, class charT, class traits>
    bool regex_match(const basic_string<charT, ST, SA>&&,
                     match_results<typename basic_string<charT, ST, SA>::const_iterator,
                                   Allocator>&,
                     const basic_regex<charT, traits>&,
                     regex_constants::match_flag_type = regex_constants::match_default) = delete;
  template<class charT, class traits>
    bool regex_match(const charT* str,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class ST, class SA, class charT, class traits>
    bool regex_match(const basic_string<charT, ST, SA>& s,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags = regex_constants::match_default);

  // [re.alg.search], function template regex_search
  template<class BidirectionalIterator, class Allocator, class charT, class traits>
    bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                      match_results<BidirectionalIterator, Allocator>& m,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class BidirectionalIterator, class charT, class traits>
    bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class charT, class Allocator, class traits>
    bool regex_search(const charT* str,
                      match_results<const charT*, Allocator>& m,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class charT, class traits>
    bool regex_search(const charT* str,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class ST, class SA, class charT, class traits>
    bool regex_search(const basic_string<charT, ST, SA>& s,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class ST, class SA, class Allocator, class charT, class traits>
    bool regex_search(const basic_string<charT, ST, SA>& s,
                      match_results<typename basic_string<charT, ST, SA>::const_iterator,
                                    Allocator>& m,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class ST, class SA, class Allocator, class charT, class traits>
    bool regex_search(const basic_string<charT, ST, SA>&&,
                      match_results<typename basic_string<charT, ST, SA>::const_iterator,
                                    Allocator>&,
                      const basic_regex<charT, traits>&,
                      regex_constants::match_flag_type
                        = regex_constants::match_default) = delete;

  // [re.alg.replace], function template regex_replace
  template<class OutputIterator, class BidirectionalIterator,
           class traits, class charT, class ST, class SA>
    OutputIterator
      regex_replace(OutputIterator out,
                    BidirectionalIterator first, BidirectionalIterator last,
                    const basic_regex<charT, traits>& e,
                    const basic_string<charT, ST, SA>& fmt,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class OutputIterator, class BidirectionalIterator, class traits, class charT>
    OutputIterator
      regex_replace(OutputIterator out,
                    BidirectionalIterator first, BidirectionalIterator last,
                    const basic_regex<charT, traits>& e,
                    const charT* fmt,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class traits, class charT, class ST, class SA, class FST, class FSA>
    basic_string<charT, ST, SA>
      regex_replace(const basic_string<charT, ST, SA>& s,
                    const basic_regex<charT, traits>& e,
                    const basic_string<charT, FST, FSA>& fmt,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class traits, class charT, class ST, class SA>
    basic_string<charT, ST, SA>
      regex_replace(const basic_string<charT, ST, SA>& s,
                    const basic_regex<charT, traits>& e,
                    const charT* fmt,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class traits, class charT, class ST, class SA>
    basic_string<charT>
      regex_replace(const charT* s,
                    const basic_regex<charT, traits>& e,
                    const basic_string<charT, ST, SA>& fmt,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
  template<class traits, class charT>
    basic_string<charT>
      regex_replace(const charT* s,
                    const basic_regex<charT, traits>& e,
                    const charT* fmt,
                    regex_constants::match_flag_type flags = regex_constants::match_default);

  // [re.regiter], class template regex_iterator
  template<class BidirectionalIterator,
           class charT = typename iterator_traits<BidirectionalIterator>::value_type,
           class traits = regex_traits<charT>>
    class regex_iterator;

  using cregex_iterator  = regex_iterator<const char*>;
  using wcregex_iterator = regex_iterator<const wchar_t*>;
  using sregex_iterator  = regex_iterator<string::const_iterator>;
  using wsregex_iterator = regex_iterator<wstring::const_iterator>;

  // [re.tokiter], class template regex_token_iterator
  template<class BidirectionalIterator,
           class charT = typename iterator_traits<BidirectionalIterator>::value_type,
           class traits = regex_traits<charT>>
    class regex_token_iterator;

  using cregex_token_iterator  = regex_token_iterator<const char*>;
  using wcregex_token_iterator = regex_token_iterator<const wchar_t*>;
  using sregex_token_iterator  = regex_token_iterator<string::const_iterator>;
  using wsregex_token_iterator = regex_token_iterator<wstring::const_iterator>;

  namespace pmr {
    template<class BidirectionalIterator>
      using match_results =
        std::match_results<BidirectionalIterator,
                           polymorphic_allocator<sub_match<BidirectionalIterator>>>;

    using cmatch  = match_results<const char*>;
    using wcmatch = match_results<const wchar_t*>;
    using smatch  = match_results<string::const_iterator>;
    using wsmatch = match_results<wstring::const_iterator>;
  }
}
```

### Namespace `std::regex_constants` <a id="re.const">[[re.const]]</a>

#### General <a id="re.const.general">[[re.const.general]]</a>

The namespace `std::regex_constants` holds symbolic constants used by
the regular expression library. This namespace provides three types,
`syntax_option_type`, `match_flag_type`, and `error_type`, along with
several constants of these types.

#### Bitmask type `syntax_option_type` <a id="re.synopt">[[re.synopt]]</a>

``` cpp
namespace std::regex_constants {
  using syntax_option_type = T1;
  inline constexpr syntax_option_type icase = unspecified;
  inline constexpr syntax_option_type nosubs = unspecified;
  inline constexpr syntax_option_type optimize = unspecified;
  inline constexpr syntax_option_type collate = unspecified;
  inline constexpr syntax_option_type ECMAScript = unspecified;
  inline constexpr syntax_option_type basic = unspecified;
  inline constexpr syntax_option_type extended = unspecified;
  inline constexpr syntax_option_type awk = unspecified;
  inline constexpr syntax_option_type grep = unspecified;
  inline constexpr syntax_option_type egrep = unspecified;
  inline constexpr syntax_option_type multiline = unspecified;
}
```

The type `syntax_option_type` is an *implementation-defined* bitmask
type [[bitmask.types]]. Setting its elements has the effects listed in
[[re.synopt]]. A valid value of type `syntax_option_type` shall have at
most one of the grammar elements `ECMAScript`, `basic`, `extended`,
`awk`, `grep`, `egrep`, set. If no grammar element is set, the default
grammar is `ECMAScript`.

**Table: `syntax_option_type` effects**

| Element        | Effect(s) if set                                                                                                                                                                                                                                                                                                             |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| % `icase`      | Specifies that matching of regular expressions against a character container sequence shall be performed without regard to case. \indexlibrarymember{syntax_option_type}{icase}%                                                                                                                                             |
| % `nosubs`     | Specifies that no sub-expressions shall be considered to be marked, so that when a regular expression is matched against a character container sequence, no sub-expression matches shall be stored in the supplied `match_results` object. \indexlibrarymember{syntax_option_type}{nosubs}%                                  |
| % `optimize`   | Specifies that the regular expression engine should pay more attention to the speed with which regular expressions are matched, and less to the speed with which regular expression objects are constructed. Otherwise it has no detectable effect on the program output. \indexlibrarymember{syntax_option_type}{optimize}% |
| % `collate`    | Specifies that character ranges of the form `"[a-b]"` shall be locale sensitive.% \indexlibrarymember{syntax_option_type}{collate}% \indextext{locale}%                                                                                                                                                                      |
| % `ECMAScript` | Specifies that the grammar recognized by the regular expression engine shall be that used by ECMAScript in ECMA-262, as modified in~ [[re.grammar]]. \newline \xref{ECMA-262 15.10} \indextext{ECMAScript}% \indexlibrarymember{syntax_option_type}{ECMAScript}%                                                             |
| % `basic`      | Specifies that the grammar recognized by the regular expression engine shall be that used by basic regular expressions in POSIX. \newline \xref{POSIX, Base Definitions and Headers, Section 9.3} \indextext{POSIX!regular expressions}% \indexlibrarymember{syntax_option_type}{basic}%                                     |
| % `extended`   | Specifies that the grammar recognized by the regular expression engine shall be that used by extended regular expressions in POSIX. \newline \xref{POSIX, Base Definitions and Headers, Section 9.4} \indextext{POSIX!extended regular expressions}% \indexlibrarymember{syntax_option_type}{extended}%                      |
| % `awk`        | Specifies that the grammar recognized by the regular expression engine shall be that used by the utility awk in POSIX. \indexlibrarymember{syntax_option_type}{awk}%                                                                                                                                                         |
| % `grep`       | Specifies that the grammar recognized by the regular expression engine shall be that used by the utility grep in POSIX. \indexlibrarymember{syntax_option_type}{grep}%                                                                                                                                                       |
| % `egrep`      | Specifies that the grammar recognized by the regular expression engine shall be that used by the utility grep when given the -E option in POSIX. \indexlibrarymember{syntax_option_type}{egrep}%                                                                                                                             |
| % `multiline`  | Specifies that `^` shall match the beginning of a line and `$` shall match the end of a line, if the `ECMAScript` engine is selected. \indexlibrarymember{syntax_option_type}{multiline}%                                                                                                                                    |


#### Bitmask type `match_flag_type` <a id="re.matchflag">[[re.matchflag]]</a>

``` cpp
namespace std::regex_constants {
  using match_flag_type = T2;
  inline constexpr match_flag_type match_default = {};
  inline constexpr match_flag_type match_not_bol = unspecified;
  inline constexpr match_flag_type match_not_eol = unspecified;
  inline constexpr match_flag_type match_not_bow = unspecified;
  inline constexpr match_flag_type match_not_eow = unspecified;
  inline constexpr match_flag_type match_any = unspecified;
  inline constexpr match_flag_type match_not_null = unspecified;
  inline constexpr match_flag_type match_continuous = unspecified;
  inline constexpr match_flag_type match_prev_avail = unspecified;
  inline constexpr match_flag_type format_default = {};
  inline constexpr match_flag_type format_sed = unspecified;
  inline constexpr match_flag_type format_no_copy = unspecified;
  inline constexpr match_flag_type format_first_only = unspecified;
}
```

The type `match_flag_type` is an *implementation-defined* bitmask type
[[bitmask.types]]. The constants of that type, except for
`match_default` and `format_default`, are bitmask elements. The
`match_default` and `format_default` constants are empty bitmasks.
Matching a regular expression against a sequence of characters
\[`first`, `last`) proceeds according to the rules of the grammar
specified for the regular expression object, modified according to the
effects listed in [[re.matchflag]] for any bitmask elements set.

**Table: `regex_constants::match_flag_type` effects**

| Element                                                       | Effect(s) if set                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| % \indexlibraryglobal{match_not_bol}% `match_not_bol`         | The first character in the sequence {[}`first`, `last`{)} shall be treated as though it is not at the beginning of a line, so the character \verb|^| in the regular expression shall not match {[}`first`, `first`{)}.                                                                                                                                                                                                                                                      |
| % \indexlibraryglobal{match_not_eol}% `match_not_eol`         | The last character in the sequence {[}`first`, `last`{)} shall be treated as though it is not at the end of a line, so the character \verb|"$"| in the regular expression shall not match {[}`last`, `last`{)}.                                                                                                                                                                                                                                                             |
| % \indexlibraryglobal{match_not_bow}% `match_not_bow`         | The expression \verb|"b"| shall not match the sub-sequence {[}`first`, `first`{)}.                                                                                                                                                                                                                                                                                                                                                                                          |
| % \indexlibraryglobal{match_not_eow}% `match_not_eow`         | The expression \verb|"b"| shall not match the sub-sequence {[}`last`, `last`{)}.                                                                                                                                                                                                                                                                                                                                                                                            |
| % \indexlibraryglobal{match_any}% `match_any`                 | If more than one match is possible then any match is an acceptable result.                                                                                                                                                                                                                                                                                                                                                                                                  |
| % \indexlibraryglobal{match_not_null}% `match_not_null`       | The expression shall not match an empty sequence.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| % \indexlibraryglobal{match_continuous}% `match_continuous`   | The expression shall only match a sub-sequence that begins at `first`.                                                                                                                                                                                                                                                                                                                                                                                                      |
| % \indexlibraryglobal{match_prev_avail}% `match_prev_avail`   | \verb!--first! is a valid iterator position. When this flag is set the flags `match_not_bol` and `match_not_bow` shall be ignored by the regular expression algorithms [[re.alg]] and iterators [[re.iter]].                                                                                                                                                                                                                                                                |
| % \indexlibraryglobal{format_default}% `format_default`       | When a regular expression match is to be replaced by a new string, the new string shall be constructed using the rules used by the ECMAScript replace function in ECMA-262, part 15.5.4.11 String.prototype.replace. In addition, during search and replace operations all non-overlapping occurrences of the regular expression shall be located and replaced, and sections of the input that did not match the expression shall be copied unchanged to the output string. |
| % \indexlibraryglobal{format_sed}% `format_sed`               | When a regular expression match is to be replaced by a new string, the new string shall be constructed using the rules used by the sed utility in POSIX.                                                                                                                                                                                                                                                                                                                    |
| % \indexlibraryglobal{format_no_copy}% `format_no_copy`       | During a search and replace operation, sections of the character container sequence being searched that do not match the regular expression shall not be copied to the output string.                                                                                                                                                                                                                                                                                       |
| % \indexlibraryglobal{format_first_only}% `format_first_only` | When specified during a search and replace operation, only the first occurrence of the regular expression shall be replaced.                                                                                                                                                                                                                                                                                                                                                |


#### Implementation-defined `error_type` <a id="re.err">[[re.err]]</a>

``` cpp
namespace std::regex_constants {
  using error_type = T3;
  inline constexpr error_type error_collate = unspecified;
  inline constexpr error_type error_ctype = unspecified;
  inline constexpr error_type error_escape = unspecified;
  inline constexpr error_type error_backref = unspecified;
  inline constexpr error_type error_brack = unspecified;
  inline constexpr error_type error_paren = unspecified;
  inline constexpr error_type error_brace = unspecified;
  inline constexpr error_type error_badbrace = unspecified;
  inline constexpr error_type error_range = unspecified;
  inline constexpr error_type error_space = unspecified;
  inline constexpr error_type error_badrepeat = unspecified;
  inline constexpr error_type error_complexity = unspecified;
  inline constexpr error_type error_stack = unspecified;
}
```

The type `error_type` is an *implementation-defined* enumerated type
[[enumerated.types]]. Values of type `error_type` represent the error
conditions described in [[re.err]]:

**Table: `error_type` values in the C locale**

| Value                | Error condition                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `error_collate`      | The expression contains an invalid collating element name.                                                         |
| % `error_ctype`      | The expression contains an invalid character class name.                                                           |
| % `error_escape`     | The expression contains an invalid escaped character, or a trailing escape.                                        |
| % `error_backref`    | The expression contains an invalid back reference.                                                                 |
| % `error_brack`      | The expression contains mismatched \verb|[| and \verb|]|.                                                          |
| % `error_paren`      | The expression contains mismatched \verb|(| and \verb|)|.                                                          |
| % `error_brace`      | The expression contains mismatched \verb|{| and \verb|}|.                                                          |
| % `error_badbrace`   | The expression contains an invalid range in a \verb|{}| expression.                                                |
| % `error_range`      | The expression contains an invalid character range, such as \verb|[b-a]| in most encodings.                        |
| % `error_space`      | There is insufficient memory to convert the expression into a finite state machine.                                |
| % `error_badrepeat`  | One of \verb|*?+{| is not preceded by a valid regular expression.                                                  |
| % `error_complexity` | The complexity of an attempted match against a regular expression exceeds a pre-set level.                         |
| % `error_stack`      | There is insufficient memory to determine whether the regular expression matches the specified character sequence. |


### Class `regex_error` <a id="re.badexp">[[re.badexp]]</a>

``` cpp
namespace std {
  class regex_error : public runtime_error {
  public:
    explicit regex_error(regex_constants::error_type ecode);
    regex_constants::error_type code() const;
  };
}
```

The class `regex_error` defines the type of objects thrown as exceptions
to report errors from the regular expression library.

``` cpp
regex_error(regex_constants::error_type ecode);
```

*Ensures:* `ecode == code()`.

``` cpp
regex_constants::error_type code() const;
```

*Returns:* The error code that was passed to the constructor.

### Class template `regex_traits` <a id="re.traits">[[re.traits]]</a>

``` cpp
namespace std {
  template<class charT>
    struct regex_traits {
      using char_type       = charT;
      using string_type     = basic_string<char_type>;
      using locale_type     = locale;
      using char_class_type = bitmask_type;

      regex_traits();
      static size_t length(const char_type* p);
      charT translate(charT c) const;
      charT translate_nocase(charT c) const;
      template<class ForwardIterator>
        string_type transform(ForwardIterator first, ForwardIterator last) const;
      template<class ForwardIterator>
        string_type transform_primary(
          ForwardIterator first, ForwardIterator last) const;
      template<class ForwardIterator>
        string_type lookup_collatename(
          ForwardIterator first, ForwardIterator last) const;
      template<class ForwardIterator>
        char_class_type lookup_classname(
          ForwardIterator first, ForwardIterator last, bool icase = false) const;
      bool isctype(charT c, char_class_type f) const;
      int value(charT ch, int radix) const;
      locale_type imbue(locale_type l);
      locale_type getloc() const;
    };
}
```

The specializations `regex_traits<char>` and `regex_traits<wchar_t>`
meet the requirements for a regular expression traits class [[re.req]].

``` cpp
using char_class_type = bitmask_type;
```

The type `char_class_type` is used to represent a character
classification and is capable of holding an implementation specific set
returned by `lookup_classname`.

``` cpp
static size_t length(const char_type* p);
```

*Returns:* `char_traits<charT>::length(p)`.

``` cpp
charT translate(charT c) const;
```

*Returns:* `c`.

``` cpp
charT translate_nocase(charT c) const;
```

*Returns:* `use_facet<ctype<charT>>(getloc()).tolower(c)`.

``` cpp
template<class ForwardIterator>
  string_type transform(ForwardIterator first, ForwardIterator last) const;
```

*Effects:* As if by:

``` cpp
string_type str(first, last);
return use_facet<collate<charT>>(
  getloc()).transform(str.data(), str.data() + str.length());
```

``` cpp
template<class ForwardIterator>
  string_type transform_primary(ForwardIterator first, ForwardIterator last) const;
```

*Effects:* If

``` cpp
typeid(use_facet<collate<charT>>(getloc())) == typeid(collate_byname<charT>)
```

and the form of the sort key returned by
`collate_byname<charT>::transform(first, last)` is known and can be
converted into a primary sort key then returns that key, otherwise
returns an empty string.

``` cpp
template<class ForwardIterator>
  string_type lookup_collatename(ForwardIterator first, ForwardIterator last) const;
```

*Returns:* A sequence of one or more characters that represents the
collating element consisting of the character sequence designated by the
iterator range \[`first`, `last`). Returns an empty string if the
character sequence is not a valid collating element.

``` cpp
template<class ForwardIterator>
  char_class_type lookup_classname(
    ForwardIterator first, ForwardIterator last, bool icase = false) const;
```

*Returns:* An unspecified value that represents the character
classification named by the character sequence designated by the
iterator range \[`first`, `last`). If the parameter `icase` is `true`
then the returned mask identifies the character classification without
regard to the case of the characters being matched, otherwise it does
honor the case of the characters being matched.[^26]

The value returned shall be independent of the case of the characters in
the character sequence. If the name is not recognized then returns
`char_class_type()`.

*Remarks:* For `regex_traits<char>`, at least the narrow character names
in [[re.traits.classnames]] shall be recognized. For
`regex_traits<wchar_t>`, at least the wide character names in
[[re.traits.classnames]] shall be recognized.

``` cpp
bool isctype(charT c, char_class_type f) const;
```

*Effects:* Determines if the character `c` is a member of the character
classification represented by `f`.

*Returns:* Given the following function declaration:

``` cpp
// for exposition only
template<class C>
  ctype_base::mask convert(typename regex_traits<C>::char_class_type f);
```

that returns a value in which each `ctype_base::mask` value
corresponding to a value in `f` named in [[re.traits.classnames]] is
set, then the result is determined as if by:

``` cpp
ctype_base::mask m = convert<charT>(f);
const ctype<charT>& ct = use_facet<ctype<charT>>(getloc());
if (ct.is(m, c)) {
  return true;
} else if (c == ct.widen('_')) {
  charT w[1] = { ct.widen('w') };
  char_class_type x = lookup_classname(w, w+1);
  return (f&x) == x;
} else {
  return false;
}
```

[*Example 1*:

``` cpp
regex_traits<char> t;
string d("d");
string u("upper");
regex_traits<char>::char_class_type f;
f = t.lookup_classname(d.begin(), d.end());
f |= t.lookup_classname(u.begin(), u.end());
ctype_base::mask m = convert<char>(f);  // m == ctype_base::digit | ctype_base::upper
```

— *end example*]

[*Example 2*:

``` cpp
regex_traits<char> t;
string w("w");
regex_traits<char>::char_class_type f;
f = t.lookup_classname(w.begin(), w.end());
t.isctype('A', f);  // returns true
t.isctype('_', f);  // returns true
t.isctype(' ', f);  // returns false
```

— *end example*]

``` cpp
int value(charT ch, int radix) const;
```

*Preconditions:* The value of `radix` is 8, 10, or 16.

*Returns:* The value represented by the digit `ch` in base `radix` if
the character `ch` is a valid digit in base `radix`; otherwise returns
`-1`.

``` cpp
locale_type imbue(locale_type loc);
```

*Effects:* Imbues `*this` with a copy of the locale `loc`.

[*Note 1*: Calling `imbue` with a different locale than the one
currently in use invalidates all cached data held by
`*this`. — *end note*]

*Ensures:* `getloc() == loc`.

*Returns:* If no locale has been previously imbued then a copy of the
global locale in effect at the time of construction of `*this`,
otherwise a copy of the last argument passed to `imbue`.

``` cpp
locale_type getloc() const;
```

*Returns:* If no locale has been imbued then a copy of the global locale
in effect at the time of construction of `*this`, otherwise a copy of
the last argument passed to `imbue`.

**Table: Character class names and corresponding `ctype` masks**

| Narrow character name | Wide character name | Corresponding `ctype_base::mask` value |
| --------------------- | ------------------- | -------------------------------------- |
| `"alnum"`             | `L"alnum"`          | `ctype_base::alnum`                    |
| `"alpha"`             | `L"alpha"`          | `ctype_base::alpha`                    |
| `"blank"`             | `L"blank"`          | `ctype_base::blank`                    |
| `"cntrl"`             | `L"cntrl"`          | `ctype_base::cntrl`                    |
| `"digit"`             | `L"digit"`          | `ctype_base::digit`                    |
| `"d"`                 | `L"d"`              | `ctype_base::digit`                    |
| `"graph"`             | `L"graph"`          | `ctype_base::graph`                    |
| `"lower"`             | `L"lower"`          | `ctype_base::lower`                    |
| `"print"`             | `L"print"`          | `ctype_base::print`                    |
| `"punct"`             | `L"punct"`          | `ctype_base::punct`                    |
| `"space"`             | `L"space"`          | `ctype_base::space`                    |
| `"s"`                 | `L"s"`              | `ctype_base::space`                    |
| `"upper"`             | `L"upper"`          | `ctype_base::upper`                    |
| `"w"`                 | `L"w"`              | `ctype_base::alnum`                    |
| `"xdigit"`            | `L"xdigit"`         | `ctype_base::xdigit`                   |


### Class template `basic_regex` <a id="re.regex">[[re.regex]]</a>

#### General <a id="re.regex.general">[[re.regex.general]]</a>

For a char-like type `charT`, specializations of class template
`basic_regex` represent regular expressions constructed from character
sequences of `charT` characters. In the rest of  [[re.regex]], `charT`
denotes a given char-like type. Storage for a regular expression is
allocated and freed as necessary by the member functions of class
`basic_regex`.

Objects of type specialization of `basic_regex` are responsible for
converting the sequence of `charT` objects to an internal
representation. It is not specified what form this representation takes,
nor how it is accessed by algorithms that operate on regular
expressions.

[*Note 1*: Implementations will typically declare some function
templates as friends of `basic_regex` to achieve this. — *end note*]

The functions described in [[re.regex]] report errors by throwing
exceptions of type `regex_error`.

``` cpp
namespace std {
  template<class charT, class traits = regex_traits<charT>>
    class basic_regex {
    public:
      // types
      using value_type  = charT;
      using traits_type = traits;
      using string_type = traits::string_type;
      using flag_type   = regex_constants::syntax_option_type;
      using locale_type = traits::locale_type;

      // [re.synopt], constants
      static constexpr flag_type icase = regex_constants::icase;
      static constexpr flag_type nosubs = regex_constants::nosubs;
      static constexpr flag_type optimize = regex_constants::optimize;
      static constexpr flag_type collate = regex_constants::collate;
      static constexpr flag_type ECMAScript = regex_constants::ECMAScript;
      static constexpr flag_type basic = regex_constants::basic;
      static constexpr flag_type extended = regex_constants::extended;
      static constexpr flag_type awk = regex_constants::awk;
      static constexpr flag_type grep = regex_constants::grep;
      static constexpr flag_type egrep = regex_constants::egrep;
      static constexpr flag_type multiline = regex_constants::multiline;

      // [re.regex.construct], construct/copy/destroy
      basic_regex();
      explicit basic_regex(const charT* p, flag_type f = regex_constants::ECMAScript);
      basic_regex(const charT* p, size_t len, flag_type f = regex_constants::ECMAScript);
      basic_regex(const basic_regex&);
      basic_regex(basic_regex&&) noexcept;
      template<class ST, class SA>
        explicit basic_regex(const basic_string<charT, ST, SA>& s,
                             flag_type f = regex_constants::ECMAScript);
      template<class ForwardIterator>
        basic_regex(ForwardIterator first, ForwardIterator last,
                    flag_type f = regex_constants::ECMAScript);
      basic_regex(initializer_list<charT> il, flag_type f = regex_constants::ECMAScript);

      ~basic_regex();

      // [re.regex.assign], assign
      basic_regex& operator=(const basic_regex& e);
      basic_regex& operator=(basic_regex&& e) noexcept;
      basic_regex& operator=(const charT* p);
      basic_regex& operator=(initializer_list<charT> il);
      template<class ST, class SA>
        basic_regex& operator=(const basic_string<charT, ST, SA>& s);

      basic_regex& assign(const basic_regex& e);
      basic_regex& assign(basic_regex&& e) noexcept;
      basic_regex& assign(const charT* p, flag_type f = regex_constants::ECMAScript);
      basic_regex& assign(const charT* p, size_t len, flag_type f = regex_constants::ECMAScript);
      template<class ST, class SA>
        basic_regex& assign(const basic_string<charT, ST, SA>& s,
                            flag_type f = regex_constants::ECMAScript);
      template<class InputIterator>
        basic_regex& assign(InputIterator first, InputIterator last,
                            flag_type f = regex_constants::ECMAScript);
      basic_regex& assign(initializer_list<charT>,
                          flag_type f = regex_constants::ECMAScript);

      // [re.regex.operations], const operations
      unsigned mark_count() const;
      flag_type flags() const;

      // [re.regex.locale], locale
      locale_type imbue(locale_type loc);
      locale_type getloc() const;

      // [re.regex.swap], swap
      void swap(basic_regex&);
    };

  template<class ForwardIterator>
    basic_regex(ForwardIterator, ForwardIterator,
                regex_constants::syntax_option_type = regex_constants::ECMAScript)
      -> basic_regex<typename iterator_traits<ForwardIterator>::value_type>;
}
```

#### Constructors <a id="re.regex.construct">[[re.regex.construct]]</a>

``` cpp
basic_regex();
```

*Ensures:* `*this` does not match any character sequence.

``` cpp
explicit basic_regex(const charT* p, flag_type f = regex_constants::ECMAScript);
```

*Preconditions:* \[`p`, `p + char_traits<charT>::length(p)`) is a valid
range.

*Effects:* The object’s internal finite state machine is constructed
from the regular expression contained in the sequence of characters
\[`p`, `p + char_traits<charT>::length(p)`), and interpreted according
to the flags `f`.

*Ensures:* `flags()` returns `f`. `mark_count()` returns the number of
marked sub-expressions within the expression.

*Throws:* `regex_error` if \[`p`, `p + char_traits<charT>::length(p)`)
is not a valid regular expression.

``` cpp
basic_regex(const charT* p, size_t len, flag_type f = regex_constants::ECMAScript);
```

*Preconditions:* \[`p`, `p + len`) is a valid range.

*Effects:* The object’s internal finite state machine is constructed
from the regular expression contained in the sequence of characters
\[`p`, `p + len`), and interpreted according the flags specified in `f`.

*Ensures:* `flags()` returns `f`. `mark_count()` returns the number of
marked sub-expressions within the expression.

*Throws:* `regex_error` if \[`p`, `p + len`) is not a valid regular
expression.

``` cpp
basic_regex(const basic_regex& e);
```

*Ensures:* `flags()` and `mark_count()` return `e.flags()` and
`e.mark_count()`, respectively.

``` cpp
basic_regex(basic_regex&& e) noexcept;
```

*Ensures:* `flags()` and `mark_count()` return the values that
`e.flags()` and `e.mark_count()`, respectively, had before construction.

``` cpp
template<class ST, class SA>
  explicit basic_regex(const basic_string<charT, ST, SA>& s,
                       flag_type f = regex_constants::ECMAScript);
```

*Effects:* The object’s internal finite state machine is constructed
from the regular expression contained in the string `s`, and interpreted
according to the flags specified in `f`.

*Ensures:* `flags()` returns `f`. `mark_count()` returns the number of
marked sub-expressions within the expression.

*Throws:* `regex_error` if `s` is not a valid regular expression.

``` cpp
template<class ForwardIterator>
  basic_regex(ForwardIterator first, ForwardIterator last,
              flag_type f = regex_constants::ECMAScript);
```

*Effects:* The object’s internal finite state machine is constructed
from the regular expression contained in the sequence of characters
\[`first`, `last`), and interpreted according to the flags specified in
`f`.

*Ensures:* `flags()` returns `f`. `mark_count()` returns the number of
marked sub-expressions within the expression.

*Throws:* `regex_error` if the sequence \[`first`, `last`) is not a
valid regular expression.

``` cpp
basic_regex(initializer_list<charT> il, flag_type f = regex_constants::ECMAScript);
```

*Effects:* Same as `basic_regex(il.begin(), il.end(), f)`.

#### Assignment <a id="re.regex.assign">[[re.regex.assign]]</a>

``` cpp
basic_regex& operator=(const basic_regex& e);
```

*Ensures:* `flags()` and `mark_count()` return `e.flags()` and
`e.mark_count()`, respectively.

``` cpp
basic_regex& operator=(basic_regex&& e) noexcept;
```

*Ensures:* `flags()` and `mark_count()` return the values that
`e.flags()` and `e.mark_count()`, respectively, had before assignment.
`e` is in a valid state with unspecified value.

``` cpp
basic_regex& operator=(const charT* p);
```

*Effects:* Equivalent to: `return assign(p);`

``` cpp
basic_regex& operator=(initializer_list<charT> il);
```

*Effects:* Equivalent to: `return assign(il.begin(), il.end());`

``` cpp
template<class ST, class SA>
  basic_regex& operator=(const basic_string<charT, ST, SA>& s);
```

*Effects:* Equivalent to: `return assign(s);`

``` cpp
basic_regex& assign(const basic_regex& e);
```

*Effects:* Equivalent to: `return *this = e;`

``` cpp
basic_regex& assign(basic_regex&& e) noexcept;
```

*Effects:* Equivalent to: `return *this = std::move(e);`

``` cpp
basic_regex& assign(const charT* p, flag_type f = regex_constants::ECMAScript);
```

*Effects:* Equivalent to: `return assign(string_type(p), f);`

``` cpp
basic_regex& assign(const charT* p, size_t len, flag_type f = regex_constants::ECMAScript);
```

*Effects:* Equivalent to: `return assign(string_type(p, len), f);`

``` cpp
template<class ST, class SA>
  basic_regex& assign(const basic_string<charT, ST, SA>& s,
                      flag_type f = regex_constants::ECMAScript);
```

*Effects:* Assigns the regular expression contained in the string `s`,
interpreted according the flags specified in `f`. If an exception is
thrown, `*this` is unchanged.

*Ensures:* If no exception is thrown, `flags()` returns `f` and
`mark_count()` returns the number of marked sub-expressions within the
expression.

*Returns:* `*this`.

*Throws:* `regex_error` if `s` is not a valid regular expression.

``` cpp
template<class InputIterator>
  basic_regex& assign(InputIterator first, InputIterator last,
                      flag_type f = regex_constants::ECMAScript);
```

*Effects:* Equivalent to: `return assign(string_type(first, last), f);`

``` cpp
basic_regex& assign(initializer_list<charT> il,
                    flag_type f = regex_constants::ECMAScript);
```

*Effects:* Equivalent to: `return assign(il.begin(), il.end(), f);`

#### Constant operations <a id="re.regex.operations">[[re.regex.operations]]</a>

``` cpp
unsigned mark_count() const;
```

*Effects:* Returns the number of marked sub-expressions within the
regular expression.

``` cpp
flag_type flags() const;
```

*Effects:* Returns a copy of the regular expression syntax flags that
were passed to the object’s constructor or to the last call to `assign`.

#### Locale <a id="re.regex.locale">[[re.regex.locale]]</a>

``` cpp
locale_type imbue(locale_type loc);
```

*Effects:* Returns the result of `traits_inst.imbue(loc)` where
`traits_inst` is a (default-initialized) instance of the template type
argument `traits` stored within the object. After a call to `imbue` the
`basic_regex` object does not match any character sequence.

``` cpp
locale_type getloc() const;
```

*Effects:* Returns the result of `traits_inst.getloc()` where
`traits_inst` is a (default-initialized) instance of the template
parameter `traits` stored within the object.

#### Swap <a id="re.regex.swap">[[re.regex.swap]]</a>

``` cpp
void swap(basic_regex& e);
```

*Effects:* Swaps the contents of the two regular expressions.

*Ensures:* `*this` contains the regular expression that was in `e`, `e`
contains the regular expression that was in `*this`.

*Complexity:* Constant time.

#### Non-member functions <a id="re.regex.nonmemb">[[re.regex.nonmemb]]</a>

``` cpp
template<class charT, class traits>
  void swap(basic_regex<charT, traits>& lhs, basic_regex<charT, traits>& rhs);
```

*Effects:* Calls `lhs.swap(rhs)`.

### Class template `sub_match` <a id="re.submatch">[[re.submatch]]</a>

#### General <a id="re.submatch.general">[[re.submatch.general]]</a>

``` cpp
namespace std {
  template<class BidirectionalIterator>
    class sub_match : public pair<BidirectionalIterator, BidirectionalIterator> {
    public:
      using value_type      = iterator_traits<BidirectionalIterator>::value_type;
      using difference_type = iterator_traits<BidirectionalIterator>::difference_type;
      using iterator        = BidirectionalIterator;
      using string_type     = basic_string<value_type>;

      bool matched;

      constexpr sub_match();

      difference_type length() const;
      operator string_type() const;
      string_type str() const;

      int compare(const sub_match& s) const;
      int compare(const string_type& s) const;
      int compare(const value_type* s) const;

      void swap(sub_match& s) noexcept(see below);
    };
}
```

#### Members <a id="re.submatch.members">[[re.submatch.members]]</a>

``` cpp
constexpr sub_match();
```

*Effects:* Value-initializes the `pair` base class subobject and the
member `matched`.

``` cpp
difference_type length() const;
```

*Returns:* `matched ? distance(first, second) : 0`.

``` cpp
operator string_type() const;
```

*Returns:* `matched ? string_type(first, second) : string_type()`.

``` cpp
string_type str() const;
```

*Returns:* `matched ? string_type(first, second) : string_type()`.

``` cpp
int compare(const sub_match& s) const;
```

*Returns:* `str().compare(s.str())`.

``` cpp
int compare(const string_type& s) const;
```

*Returns:* `str().compare(s)`.

``` cpp
int compare(const value_type* s) const;
```

*Returns:* `str().compare(s)`.

``` cpp
void swap(sub_match& s) noexcept(see below);
```

*Preconditions:* `BidirectionalIterator` meets the *Cpp17Swappable*
requirements [[swappable.requirements]].

*Effects:* Equivalent to:

``` cpp
this->pair<BidirectionalIterator, BidirectionalIterator>::swap(s);
std::swap(matched, s.matched);
```

*Remarks:* The exception specification is equivalent to
`is_nothrow_swappable_v<BidirectionalIterator>`.

#### Non-member operators <a id="re.submatch.op">[[re.submatch.op]]</a>

Let `SM-CAT(I)` be

``` cpp
compare_three_way_result_t<basic_string<typename iterator_traits<I>::value_type>>
```

``` cpp
template<class BiIter>
  bool operator==(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template<class BiIter>
  auto operator<=>(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `static_cast<`*`SM-CAT`*`(BiIter)>(lhs.compare(rhs) <=> 0)`.

``` cpp
template<class BiIter, class ST, class SA>
  bool operator==(
      const sub_match<BiIter>& lhs,
      const basic_string<typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:*

``` cpp
lhs.compare(typename sub_match<BiIter>::string_type(rhs.data(), rhs.size())) == 0
```

``` cpp
template<class BiIter, class ST, class SA>
  auto operator<=>(
      const sub_match<BiIter>& lhs,
      const basic_string<typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:*

``` cpp
static_cast<SM-CAT(BiIter)>(lhs.compare(
    typename sub_match<BiIter>::string_type(rhs.data(), rhs.size()))
      <=> 0
    )
```

``` cpp
template<class BiIter>
  bool operator==(const sub_match<BiIter>& lhs,
                  const typename iterator_traits<BiIter>::value_type* rhs);
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template<class BiIter>
  auto operator<=>(const sub_match<BiIter>& lhs,
                   const typename iterator_traits<BiIter>::value_type* rhs);
```

*Returns:* `static_cast<`*`SM-CAT`*`(BiIter)>(lhs.compare(rhs) <=> 0)`.

``` cpp
template<class BiIter>
  bool operator==(const sub_match<BiIter>& lhs,
                  const typename iterator_traits<BiIter>::value_type& rhs);
```

*Returns:*
`lhs.compare(typename sub_match<BiIter>::string_type(1, rhs)) == 0`.

``` cpp
template<class BiIter>
  auto operator<=>(const sub_match<BiIter>& lhs,
                   const typename iterator_traits<BiIter>::value_type& rhs);
```

*Returns:*

``` cpp
static_cast<SM-CAT(BiIter)>(lhs.compare(
    typename sub_match<BiIter>::string_type(1, rhs))
      <=> 0
    )
```

``` cpp
template<class charT, class ST, class BiIter>
  basic_ostream<charT, ST>&
    operator<<(basic_ostream<charT, ST>& os, const sub_match<BiIter>& m);
```

*Returns:* `os << m.str()`.

### Class template `match_results` <a id="re.results">[[re.results]]</a>

#### General <a id="re.results.general">[[re.results.general]]</a>

The class template `match_results` meets the requirements of an
allocator-aware container [[container.alloc.reqmts]] and of a sequence
container [[container.requirements.general]], [[sequence.reqmts]] except
that only copy assignment, move assignment, and operations defined for
const-qualified sequence containers are supported and that the semantics
of the comparison operator functions are different from those required
for a container.

A default-constructed `match_results` object has no fully established
result state. A match result is *ready* when, as a consequence of a
completed regular expression match modifying such an object, its result
state becomes fully established. The effects of calling most member
functions from a `match_results` object that is not ready are undefined.

The `sub_match` object stored at index 0 represents sub-expression 0,
i.e., the whole match. In this case the `sub_match` member `matched` is
always `true`. The `sub_match` object stored at index `n` denotes what
matched the marked sub-expression `n` within the matched expression. If
the sub-expression `n` participated in a regular expression match then
the `sub_match` member `matched` evaluates to `true`, and members
`first` and `second` denote the range of characters \[`first`, `second`)
which formed that match. Otherwise `matched` is `false`, and members
`first` and `second` point to the end of the sequence that was searched.

[*Note 1*: The `sub_match` objects representing different
sub-expressions that did not participate in a regular expression match
need not be distinct. — *end note*]

``` cpp
namespace std {
  template<class BidirectionalIterator,
           class Allocator = allocator<sub_match<BidirectionalIterator>>>
    class match_results {
    public:
      using value_type      = sub_match<BidirectionalIterator>;
      using const_reference = const value_type&;
      using reference       = value_type&;
      using const_iterator  = implementation-defined  // type of match_results::const_iterator;
      using iterator        = const_iterator;
      using difference_type = iterator_traits<BidirectionalIterator>::difference_type;
      using size_type       = allocator_traits<Allocator>::size_type;
      using allocator_type  = Allocator;
      using char_type       = iterator_traits<BidirectionalIterator>::value_type;
      using string_type     = basic_string<char_type>;

      // [re.results.const], construct/copy/destroy
      match_results() : match_results(Allocator()) {}
      explicit match_results(const Allocator& a);
      match_results(const match_results& m);
      match_results(const match_results& m, const Allocator& a);
      match_results(match_results&& m) noexcept;
      match_results(match_results&& m, const Allocator& a);
      match_results& operator=(const match_results& m);
      match_results& operator=(match_results&& m);
      ~match_results();

      // [re.results.state], state
      bool ready() const;

      // [re.results.size], size
      size_type size() const;
      size_type max_size() const;
      bool empty() const;

      // [re.results.acc], element access
      difference_type length(size_type sub = 0) const;
      difference_type position(size_type sub = 0) const;
      string_type str(size_type sub = 0) const;
      const_reference operator[](size_type n) const;

      const_reference prefix() const;
      const_reference suffix() const;
      const_iterator begin() const;
      const_iterator end() const;
      const_iterator cbegin() const;
      const_iterator cend() const;

      // [re.results.form], format
      template<class OutputIter>
        OutputIter
          format(OutputIter out,
                 const char_type* fmt_first, const char_type* fmt_last,
                 regex_constants::match_flag_type flags = regex_constants::format_default) const;
      template<class OutputIter, class ST, class SA>
        OutputIter
          format(OutputIter out,
                 const basic_string<char_type, ST, SA>& fmt,
                 regex_constants::match_flag_type flags = regex_constants::format_default) const;
      template<class ST, class SA>
        basic_string<char_type, ST, SA>
          format(const basic_string<char_type, ST, SA>& fmt,
                 regex_constants::match_flag_type flags = regex_constants::format_default) const;
      string_type
        format(const char_type* fmt,
               regex_constants::match_flag_type flags = regex_constants::format_default) const;

      // [re.results.all], allocator
      allocator_type get_allocator() const;

      // [re.results.swap], swap
      void swap(match_results& that);
    };
}
```

#### Constructors <a id="re.results.const">[[re.results.const]]</a>

[[re.results.const]] lists the postconditions of `match_results`
copy/move constructors and copy/move assignment operators. For move
operations, the results of the expressions depending on the parameter
`m` denote the values they had before the respective function calls.

``` cpp
explicit match_results(const Allocator& a);
```

*Effects:* The stored `Allocator` value is constructed from `a`.

*Ensures:* `ready()` returns `false`. `size()` returns `0`.

``` cpp
match_results(const match_results& m);
match_results(const match_results& m, const Allocator& a);
```

*Effects:* For the first form, the stored `Allocator` value is obtained
as specified in [[container.reqmts]]. For the second form, the stored
`Allocator` value is constructed from `a`.

*Ensures:* As specified in [[re.results.const]].

``` cpp
match_results(match_results&& m) noexcept;
match_results(match_results&& m, const Allocator& a);
```

*Effects:* For the first form, the stored `Allocator` value is move
constructed from `m.get_allocator()`. For the second form, the stored
`Allocator` value is constructed from `a`.

*Ensures:* As specified in [[re.results.const]].

*Throws:* The second form throws nothing if `a == m.get_allocator()` is
`true`.

``` cpp
match_results& operator=(const match_results& m);
```

*Ensures:* As specified in [[re.results.const]].

``` cpp
match_results& operator=(match_results&& m);
```

*Ensures:* As specified in [[re.results.const]].

**Table: `match_results` copy/move operation postconditions**

| Element       | Value                                                        |
| ------------- | ------------------------------------------------------------ |
| `ready()`     | `m.ready()`                                                  |
| `size()`      | `m.size()`                                                   |
| `str(n)`      | `m.str(n)` for all non-negative integers `n < m.size()`      |
| `prefix()`    | `m.prefix()`                                                 |
| `suffix()`    | `m.suffix()`                                                 |
| `(*this)[n]`  | `m[n]` for all non-negative integers `n < m.size()`          |
| `length(n)`   | `m.length(n)` for all non-negative integers `n < m.size()`   |
| `position(n)` | `m.position(n)` for all non-negative integers `n < m.size()` |


#### State <a id="re.results.state">[[re.results.state]]</a>

``` cpp
bool ready() const;
```

*Returns:* `true` if `*this` has a fully established result state,
otherwise `false`.

#### Size <a id="re.results.size">[[re.results.size]]</a>

``` cpp
size_type size() const;
```

*Returns:* One plus the number of marked sub-expressions in the regular
expression that was matched if `*this` represents the result of a
successful match. Otherwise returns `0`.

[*Note 1*: The state of a `match_results` object can be modified only
by passing that object to `regex_match` or `regex_search`.
Subclauses  [[re.alg.match]] and  [[re.alg.search]] specify the effects
of those algorithms on their `match_results` arguments. — *end note*]

``` cpp
size_type max_size() const;
```

*Returns:* The maximum number of `sub_match` elements that can be stored
in `*this`.

``` cpp
bool empty() const;
```

*Returns:* `size() == 0`.

#### Element access <a id="re.results.acc">[[re.results.acc]]</a>

``` cpp
difference_type length(size_type sub = 0) const;
```

*Preconditions:* `ready() == true`.

*Returns:* `(*this)[sub].length()`.

``` cpp
difference_type position(size_type sub = 0) const;
```

*Preconditions:* `ready() == true`.

*Returns:* The distance from the start of the target sequence to
`(*this)[sub].first`.

``` cpp
string_type str(size_type sub = 0) const;
```

*Preconditions:* `ready() == true`.

*Returns:* `string_type((*this)[sub])`.

``` cpp
const_reference operator[](size_type n) const;
```

*Preconditions:* `ready() == true`.

*Returns:* A reference to the `sub_match` object representing the
character sequence that matched marked sub-expression `n`. If `n == 0`
then returns a reference to a `sub_match` object representing the
character sequence that matched the whole regular expression. If
`n >= size()` then returns a `sub_match` object representing an
unmatched sub-expression.

``` cpp
const_reference prefix() const;
```

*Preconditions:* `ready() == true`.

*Returns:* A reference to the `sub_match` object representing the
character sequence from the start of the string being matched/searched
to the start of the match found.

``` cpp
const_reference suffix() const;
```

*Preconditions:* `ready() == true`.

*Returns:* A reference to the `sub_match` object representing the
character sequence from the end of the match found to the end of the
string being matched/searched.

``` cpp
const_iterator begin() const;
const_iterator cbegin() const;
```

*Returns:* A starting iterator that enumerates over all the
sub-expressions stored in `*this`.

``` cpp
const_iterator end() const;
const_iterator cend() const;
```

*Returns:* A terminating iterator that enumerates over all the
sub-expressions stored in `*this`.

#### Formatting <a id="re.results.form">[[re.results.form]]</a>

``` cpp
template<class OutputIter>
  OutputIter format(
    OutputIter out,
    const char_type* fmt_first, const char_type* fmt_last,
    regex_constants::match_flag_type flags = regex_constants::format_default) const;
```

*Preconditions:* `ready() == true` and `OutputIter` meets the
requirements for a *Cpp17OutputIterator*[[output.iterators]].

*Effects:* Copies the character sequence \[`fmt_first`, `fmt_last`) to
OutputIter `out`. Replaces each format specifier or escape sequence in
the copied range with either the character(s) it represents or the
sequence of characters within `*this` to which it refers. The bitmasks
specified in `flags` determine which format specifiers and escape
sequences are recognized.

*Returns:* `out`.

``` cpp
template<class OutputIter, class ST, class SA>
  OutputIter format(
    OutputIter out,
    const basic_string<char_type, ST, SA>& fmt,
    regex_constants::match_flag_type flags = regex_constants::format_default) const;
```

*Effects:* Equivalent to:

``` cpp
return format(out, fmt.data(), fmt.data() + fmt.size(), flags);
```

``` cpp
template<class ST, class SA>
  basic_string<char_type, ST, SA> format(
    const basic_string<char_type, ST, SA>& fmt,
    regex_constants::match_flag_type flags = regex_constants::format_default) const;
```

*Preconditions:* `ready() == true`.

*Effects:* Constructs an empty string `result` of type
`basic_string<char_type, ST, SA>` and calls:

``` cpp
format(back_inserter(result), fmt, flags);
```

*Returns:* `result`.

``` cpp
string_type format(
  const char_type* fmt,
  regex_constants::match_flag_type flags = regex_constants::format_default) const;
```

*Preconditions:* `ready() == true`.

*Effects:* Constructs an empty string `result` of type `string_type` and
calls:

``` cpp
format(back_inserter(result), fmt, fmt + char_traits<char_type>::length(fmt), flags);
```

*Returns:* `result`.

#### Allocator <a id="re.results.all">[[re.results.all]]</a>

``` cpp
allocator_type get_allocator() const;
```

*Returns:* A copy of the Allocator that was passed to the object’s
constructor or, if that allocator has been replaced, a copy of the most
recent replacement.

#### Swap <a id="re.results.swap">[[re.results.swap]]</a>

``` cpp
void swap(match_results& that);
```

*Effects:* Swaps the contents of the two sequences.

*Ensures:* `*this` contains the sequence of matched sub-expressions that
were in `that`, `that` contains the sequence of matched sub-expressions
that were in `*this`.

*Complexity:* Constant time.

``` cpp
template<class BidirectionalIterator, class Allocator>
  void swap(match_results<BidirectionalIterator, Allocator>& m1,
            match_results<BidirectionalIterator, Allocator>& m2);
```

*Effects:* As if by `m1.swap(m2)`.

#### Non-member functions <a id="re.results.nonmember">[[re.results.nonmember]]</a>

``` cpp
template<class BidirectionalIterator, class Allocator>
  bool operator==(const match_results<BidirectionalIterator, Allocator>& m1,
                  const match_results<BidirectionalIterator, Allocator>& m2);
```

*Returns:* `true` if neither match result is ready, `false` if one match
result is ready and the other is not. If both match results are ready,
returns `true` only if

- `m1.empty() && m2.empty()`, or
- `!m1.empty() && !m2.empty()`, and the following conditions are
  satisfied:
  - `m1.prefix() == m2.prefix()`,
  - `m1.size() == m2.size() && equal(m1.begin(), m1.end(), m2.begin())`,
    and
  - `m1.suffix() == m2.suffix()`.

[*Note 1*: The algorithm `equal` is defined in
[[algorithms]]. — *end note*]

### Regular expression algorithms <a id="re.alg">[[re.alg]]</a>

#### Exceptions <a id="re.except">[[re.except]]</a>

#### `regex_match` <a id="re.alg.match">[[re.alg.match]]</a>

``` cpp
template<class BidirectionalIterator, class Allocator, class charT, class traits>
  bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                   match_results<BidirectionalIterator, Allocator>& m,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Preconditions:* `BidirectionalIterator` models
`bidirectional_iterator`[[iterator.concept.bidir]].

*Effects:* Determines whether there is a match between the regular
expression `e`, and all of the character sequence \[`first`, `last`).
The parameter `flags` is used to control how the expression is matched
against the character sequence. When determining if there is a match,
only potential matches that match the entire character sequence are
considered. Returns `true` if such a match exists, `false` otherwise.

[*Example 1*:

``` cpp
std::regex re("Get|GetValue");
std::cmatch m;
regex_search("GetValue", m, re);        // returns true, and m[0] contains "Get"
regex_match ("GetValue", m, re);        // returns true, and m[0] contains "GetValue"
regex_search("GetValues", m, re);       // returns true, and m[0] contains "Get"
regex_match ("GetValues", m, re);       // returns false
```

— *end example*]

*Ensures:* `m.ready() == true` in all cases. If the function returns
`false`, then the effect on parameter `m` is unspecified except that
`m.size()` returns `0` and `m.empty()` returns `true`. Otherwise the
effects on parameter `m` are given in [[re.alg.match]].

**Table: Effects of `regex_match` algorithm**

| Element              | Value                                                                                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `m.size()`           | `1 + e.mark_count()`                                                                                                                                                                |
| `m.empty()`          | `false`                                                                                                                                                                             |
| `m.prefix().first`   | `first`                                                                                                                                                                             |
| `m.prefix().second`  | `first`                                                                                                                                                                             |
| `m.prefix().matched` | `false`                                                                                                                                                                             |
| `m.suffix().first`   | `last`                                                                                                                                                                              |
| `m.suffix().second`  | `last`                                                                                                                                                                              |
| `m.suffix().matched` | `false`                                                                                                                                                                             |
| `m[0].first`         | `first`                                                                                                                                                                             |
| `m[0].second`        | `last`                                                                                                                                                                              |
| `m[0].matched`       | `true`                                                                                                                                                                              |
| `m[n].first`         | For all integers `0 < n < m.size()`, the start of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last`. |
| `m[n].second`        | For all integers `0 < n < m.size()`, the end of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last`.   |
| `m[n].matched`       | For all integers `0 < n < m.size()`, `true` if sub-expression `n` participated in the match, `false` otherwise.                                                                     |

``` cpp
template<class BidirectionalIterator, class charT, class traits>
  bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Effects:* Behaves “as if” by constructing an instance of
`match_results<BidirectionalIterator> what`, and then returning the
result of `regex_match(first, last, what, e, flags)`.

``` cpp
template<class charT, class Allocator, class traits>
  bool regex_match(const charT* str,
                   match_results<const charT*, Allocator>& m,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:*
`regex_match(str, str + char_traits<charT>::length(str), m, e, flags)`.

``` cpp
template<class ST, class SA, class Allocator, class charT, class traits>
  bool regex_match(const basic_string<charT, ST, SA>& s,
                   match_results<typename basic_string<charT, ST, SA>::const_iterator,
                                 Allocator>& m,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:* `regex_match(s.begin(), s.end(), m, e, flags)`.

``` cpp
template<class charT, class traits>
  bool regex_match(const charT* str,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:*
`regex_match(str, str + char_traits<charT>::length(str), e, flags)`.

``` cpp
template<class ST, class SA, class charT, class traits>
  bool regex_match(const basic_string<charT, ST, SA>& s,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:* `regex_match(s.begin(), s.end(), e, flags)`.

#### `regex_search` <a id="re.alg.search">[[re.alg.search]]</a>

``` cpp
template<class BidirectionalIterator, class Allocator, class charT, class traits>
  bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                    match_results<BidirectionalIterator, Allocator>& m,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Preconditions:* `BidirectionalIterator` models
`bidirectional_iterator`[[iterator.concept.bidir]].

*Effects:* Determines whether there is some sub-sequence within
\[`first`, `last`) that matches the regular expression `e`. The
parameter `flags` is used to control how the expression is matched
against the character sequence. Returns `true` if such a sequence
exists, `false` otherwise.

*Ensures:* `m.ready() == true` in all cases. If the function returns
`false`, then the effect on parameter `m` is unspecified except that
`m.size()` returns `0` and `m.empty()` returns `true`. Otherwise the
effects on parameter `m` are given in [[re.alg.search]].

**Table: Effects of `regex_search` algorithm**

| Element              | Value                                                                                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `m.size()`           | `1 + e.mark_count()`                                                                                                                                                                |
| `m.empty()`          | `false`                                                                                                                                                                             |
| `m.prefix().first`   | `first`                                                                                                                                                                             |
| `m.prefix().second`  | `m[0].first`                                                                                                                                                                        |
| `m.prefix().matched` | `m.prefix().first != m.prefix().second`                                                                                                                                             |
| `m.suffix().first`   | `m[0].second`                                                                                                                                                                       |
| `m.suffix().second`  | `last`                                                                                                                                                                              |
| `m.suffix().matched` | `m.suffix().first != m.suffix().second`                                                                                                                                             |
| `m[0].first`         | The start of the sequence of characters that matched the regular expression                                                                                                         |
| `m[0].second`        | The end of the sequence of characters that matched the regular expression                                                                                                           |
| `m[0].matched`       | `true`                                                                                                                                                                              |
| `m[n].first`         | For all integers `0 < n < m.size()`, the start of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last`. |
| `m[n].second`        | For all integers `0 < n < m.size()`, the end of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last`.   |
| `m[n].matched`       | For all integers `0 < n < m.size()`, `true` if sub-expression `n` participated in the match, `false` otherwise.                                                                     |

``` cpp
template<class charT, class Allocator, class traits>
  bool regex_search(const charT* str, match_results<const charT*, Allocator>& m,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:*
`regex_search(str, str + char_traits<charT>::length(str), m, e, flags)`.

``` cpp
template<class ST, class SA, class Allocator, class charT, class traits>
  bool regex_search(const basic_string<charT, ST, SA>& s,
                    match_results<typename basic_string<charT, ST, SA>::const_iterator,
                                  Allocator>& m,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:* `regex_search(s.begin(), s.end(), m, e, flags)`.

``` cpp
template<class BidirectionalIterator, class charT, class traits>
  bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Effects:* Behaves “as if” by constructing an object `what` of type
`match_results<BidirectionalIterator>` and returning
`regex_search(first, last, what, e, flags)`.

``` cpp
template<class charT, class traits>
  bool regex_search(const charT* str,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:*
`regex_search(str, str + char_traits<charT>::length(str), e, flags)`.

``` cpp
template<class ST, class SA, class charT, class traits>
  bool regex_search(const basic_string<charT, ST, SA>& s,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Returns:* `regex_search(s.begin(), s.end(), e, flags)`.

#### `regex_replace` <a id="re.alg.replace">[[re.alg.replace]]</a>

``` cpp
template<class OutputIterator, class BidirectionalIterator,
         class traits, class charT, class ST, class SA>
  OutputIterator
    regex_replace(OutputIterator out,
                  BidirectionalIterator first, BidirectionalIterator last,
                  const basic_regex<charT, traits>& e,
                  const basic_string<charT, ST, SA>& fmt,
                  regex_constants::match_flag_type flags = regex_constants::match_default);
template<class OutputIterator, class BidirectionalIterator, class traits, class charT>
  OutputIterator
    regex_replace(OutputIterator out,
                  BidirectionalIterator first, BidirectionalIterator last,
                  const basic_regex<charT, traits>& e,
                  const charT* fmt,
                  regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Effects:* Constructs a `regex_iterator` object `i` as if by

``` cpp
regex_iterator<BidirectionalIterator, charT, traits> i(first, last, e, flags)
```

and uses `i` to enumerate through all of the matches `m` of type
`match_results<BidirectionalIterator>` that occur within the sequence
\[`first`, `last`). If no such matches are found and
`!(flags & regex_constants::format_no_copy)`, then calls

``` cpp
out = copy(first, last, out)
```

If any matches are found then, for each such match:

- If `!(flags & regex_constants::format_no_copy)`, calls
  ``` cpp
  out = copy(m.prefix().first, m.prefix().second, out)
  ```
- Then calls
  ``` cpp
  out = m.format(out, fmt, flags)
  ```

  for the first form of the function and
  ``` cpp
  out = m.format(out, fmt, fmt + char_traits<charT>::length(fmt), flags)
  ```

  for the second.

Finally, if such a match is found and
`!(flags & regex_constants::format_no_copy)`, calls

``` cpp
out = copy(last_m.suffix().first, last_m.suffix().second, out)
```

where `last_m` is a copy of the last match found. If
`flags & regex_constants::format_first_only` is nonzero, then only the
first match found is replaced.

*Returns:* `out`.

``` cpp
template<class traits, class charT, class ST, class SA, class FST, class FSA>
  basic_string<charT, ST, SA>
    regex_replace(const basic_string<charT, ST, SA>& s,
                  const basic_regex<charT, traits>& e,
                  const basic_string<charT, FST, FSA>& fmt,
                  regex_constants::match_flag_type flags = regex_constants::match_default);
template<class traits, class charT, class ST, class SA>
  basic_string<charT, ST, SA>
    regex_replace(const basic_string<charT, ST, SA>& s,
                  const basic_regex<charT, traits>& e,
                  const charT* fmt,
                  regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Effects:* Constructs an empty string `result` of type
`basic_string<charT, ST, SA>` and calls:

``` cpp
regex_replace(back_inserter(result), s.begin(), s.end(), e, fmt, flags);
```

*Returns:* `result`.

``` cpp
template<class traits, class charT, class ST, class SA>
  basic_string<charT>
    regex_replace(const charT* s,
                  const basic_regex<charT, traits>& e,
                  const basic_string<charT, ST, SA>& fmt,
                  regex_constants::match_flag_type flags = regex_constants::match_default);
template<class traits, class charT>
  basic_string<charT>
    regex_replace(const charT* s,
                  const basic_regex<charT, traits>& e,
                  const charT* fmt,
                  regex_constants::match_flag_type flags = regex_constants::match_default);
```

*Effects:* Constructs an empty string `result` of type
`basic_string<charT>` and calls:

``` cpp
regex_replace(back_inserter(result), s, s + char_traits<charT>::length(s), e, fmt, flags);
```

*Returns:* `result`.

### Regular expression iterators <a id="re.iter">[[re.iter]]</a>

#### Class template `regex_iterator` <a id="re.regiter">[[re.regiter]]</a>

##### General <a id="re.regiter.general">[[re.regiter.general]]</a>

``` cpp
namespace std {
  template<class BidirectionalIterator,
           class charT = typename iterator_traits<BidirectionalIterator>::value_type,
           class traits = regex_traits<charT>>
    class regex_iterator {
    public:
      using regex_type        = basic_regex<charT, traits>;
      using iterator_category = forward_iterator_tag;
      using iterator_concept  = input_iterator_tag;
      using value_type        = match_results<BidirectionalIterator>;
      using difference_type   = ptrdiff_t;
      using pointer           = const value_type*;
      using reference         = const value_type&;

      regex_iterator();
      regex_iterator(BidirectionalIterator a, BidirectionalIterator b,
                     const regex_type& re,
                     regex_constants::match_flag_type m = regex_constants::match_default);
      regex_iterator(BidirectionalIterator, BidirectionalIterator,
                     const regex_type&&,
                     regex_constants::match_flag_type = regex_constants::match_default) = delete;
      regex_iterator(const regex_iterator&);
      regex_iterator& operator=(const regex_iterator&);
      bool operator==(const regex_iterator&) const;
      bool operator==(default_sentinel_t) const { return *this == regex_iterator(); }
      const value_type& operator*() const;
      const value_type* operator->() const;
      regex_iterator& operator++();
      regex_iterator operator++(int);

    private:
      BidirectionalIterator                begin;               // exposition only
      BidirectionalIterator                end;                 // exposition only
      const regex_type*                    pregex;              // exposition only
      regex_constants::match_flag_type     flags;               // exposition only
      match_results<BidirectionalIterator> match;               // exposition only
    };
}
```

An object of type `regex_iterator` that is not an end-of-sequence
iterator holds a *zero-length match* if `match[0].matched == true` and
`match[0].first == match[0].second`.

[*Note 1*: For example, this can occur when the part of the regular
expression that matched consists only of an assertion (such as `'^'`,
`'$'`, `'\backslashb'`, `'\backslashB'`). — *end note*]

##### Constructors <a id="re.regiter.cnstr">[[re.regiter.cnstr]]</a>

``` cpp
regex_iterator();
```

*Effects:* Constructs an end-of-sequence iterator.

``` cpp
regex_iterator(BidirectionalIterator a, BidirectionalIterator b,
               const regex_type& re,
               regex_constants::match_flag_type m = regex_constants::match_default);
```

*Effects:* Initializes `begin` and `end` to `a` and `b`, respectively,
sets `pregex` to `addressof(re)`, sets `flags` to `m`, then calls
`regex_search(begin, end, match, *pregex, flags)`. If this call returns
`false` the constructor sets `*this` to the end-of-sequence iterator.

##### Comparisons <a id="re.regiter.comp">[[re.regiter.comp]]</a>

``` cpp
bool operator==(const regex_iterator& right) const;
```

*Returns:* `true` if `*this` and `right` are both end-of-sequence
iterators or if the following conditions all hold:

- `begin == right.begin`,
- `end == right.end`,
- `pregex == right.pregex`,
- `flags == right.flags`, and
- `match[0] == right.match[0]`;

otherwise `false`.

##### Indirection <a id="re.regiter.deref">[[re.regiter.deref]]</a>

``` cpp
const value_type& operator*() const;
```

*Returns:* `match`.

``` cpp
const value_type* operator->() const;
```

*Returns:* `addressof(match)`.

##### Increment <a id="re.regiter.incr">[[re.regiter.incr]]</a>

``` cpp
regex_iterator& operator++();
```

*Effects:* Constructs a local variable `start` of type
`BidirectionalIterator` and initializes it with the value of
`match[0].second`.

If the iterator holds a zero-length match and `start == end` the
operator sets `*this` to the end-of-sequence iterator and returns
`*this`.

Otherwise, if the iterator holds a zero-length match, the operator
calls:

``` cpp
regex_search(start, end, match, *pregex,
             flags | regex_constants::match_not_null | regex_constants::match_continuous)
```

If the call returns `true` the operator returns `*this`. Otherwise the
operator increments `start` and continues as if the most recent match
was not a zero-length match.

If the most recent match was not a zero-length match, the operator sets
`flags` to `flags | regex_constants::match_prev_avail` and calls
`regex_search(start, end, match, *pregex, flags)`. If the call returns
`false` the iterator sets `*this` to the end-of-sequence iterator. The
iterator then returns `*this`.

In all cases in which the call to `regex_search` returns `true`,
`match.prefix().first` shall be equal to the previous value of
`match[0].second`, and for each index `i` in the half-open range \[`0`,
`match.size()`) for which `match[i].matched` is `true`,
`match.position(i)` shall return `distance(begin, match[i].first)`.

[*Note 1*: This means that `match.position(i)` gives the offset from
the beginning of the target sequence, which is often not the same as the
offset from the sequence passed in the call to
`regex_search`. — *end note*]

It is unspecified how the implementation makes these adjustments.

[*Note 2*: This means that an implementation can call an
implementation-specific search function, in which case a program-defined
specialization of `regex_search` will not be called. — *end note*]

``` cpp
regex_iterator operator++(int);
```

*Effects:* As if by:

``` cpp
regex_iterator tmp = *this;
++(*this);
return tmp;
```

#### Class template `regex_token_iterator` <a id="re.tokiter">[[re.tokiter]]</a>

##### General <a id="re.tokiter.general">[[re.tokiter.general]]</a>

The class template `regex_token_iterator` is an iterator adaptor; that
is to say it represents a new view of an existing iterator sequence, by
enumerating all the occurrences of a regular expression within that
sequence, and presenting one or more sub-expressions for each match
found. Each position enumerated by the iterator is a `sub_match` class
template instance that represents what matched a particular
sub-expression within the regular expression.

When class `regex_token_iterator` is used to enumerate a single
sub-expression with index -1 the iterator performs field splitting: that
is to say it enumerates one sub-expression for each section of the
character container sequence that does not match the regular expression
specified.

After it is constructed, the iterator finds and stores a value
`regex_iterator<BidirectionalIterator> position` and sets the internal
count `N` to zero. It also maintains a sequence `subs` which contains a
list of the sub-expressions which will be enumerated. Every time
`operator++` is used the count `N` is incremented; if `N` exceeds or
equals `subs.size()`, then the iterator increments member `position` and
sets count `N` to zero.

If the end of sequence is reached (`position` is equal to the end of
sequence iterator), the iterator becomes equal to the end-of-sequence
iterator value, unless the sub-expression being enumerated has index -1,
in which case the iterator enumerates one last sub-expression that
contains all the characters from the end of the last regular expression
match to the end of the input sequence being enumerated, provided that
this would not be an empty sub-expression.

The default constructor constructs an end-of-sequence iterator object,
which is the only legitimate iterator to be used for the end condition.
The result of `operator*` on an end-of-sequence iterator is not defined.
For any other iterator value a `const sub_match<BidirectionalIterator>&`
is returned. The result of `operator->` on an end-of-sequence iterator
is not defined. For any other iterator value a `const
sub_match<BidirectionalIterator>*` is returned.

It is impossible to store things into `regex_token_iterator`s. Two
end-of-sequence iterators are always equal. An end-of-sequence iterator
is not equal to a non-end-of-sequence iterator. Two non-end-of-sequence
iterators are equal when they are constructed from the same arguments.

``` cpp
namespace std {
  template<class BidirectionalIterator,
           class charT = typename iterator_traits<BidirectionalIterator>::value_type,
           class traits = regex_traits<charT>>
    class regex_token_iterator {
    public:
      using regex_type        = basic_regex<charT, traits>;
      using iterator_category = forward_iterator_tag;
      using iterator_concept  = input_iterator_tag;
      using value_type        = sub_match<BidirectionalIterator>;
      using difference_type   = ptrdiff_t;
      using pointer           = const value_type*;
      using reference         = const value_type&;

      regex_token_iterator();
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type& re,
                           int submatch = 0,
                           regex_constants::match_flag_type m =
                             regex_constants::match_default);
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type& re,
                           const vector<int>& submatches,
                           regex_constants::match_flag_type m =
                             regex_constants::match_default);
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type& re,
                           initializer_list<int> submatches,
                           regex_constants::match_flag_type m =
                             regex_constants::match_default);
      template<size_t N>
        regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                             const regex_type& re,
                             const int (&submatches)[N],
                             regex_constants::match_flag_type m =
                               regex_constants::match_default);
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type&& re,
                           int submatch = 0,
                           regex_constants::match_flag_type m =
                             regex_constants::match_default) = delete;
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type&& re,
                           const vector<int>& submatches,
                           regex_constants::match_flag_type m =
                             regex_constants::match_default) = delete;
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type&& re,
                           initializer_list<int> submatches,
                           regex_constants::match_flag_type m =
                             regex_constants::match_default) = delete;
      template<size_t N>
      regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                           const regex_type&& re,
                           const int (&submatches)[N],
                           regex_constants::match_flag_type m =
                             regex_constants::match_default) = delete;
      regex_token_iterator(const regex_token_iterator&);
      regex_token_iterator& operator=(const regex_token_iterator&);
      bool operator==(const regex_token_iterator&) const;
      bool operator==(default_sentinel_t) const { return *this == regex_token_iterator(); }
      const value_type& operator*() const;
      const value_type* operator->() const;
      regex_token_iterator& operator++();
      regex_token_iterator operator++(int);

    private:
      using position_iterator =
        regex_iterator<BidirectionalIterator, charT, traits>;   // exposition only
      position_iterator position;                               // exposition only
      const value_type* result;                                 // exposition only
      value_type suffix;                                        // exposition only
      size_t N;                                                 // exposition only
      vector<int> subs;                                         // exposition only
    };
}
```

A *suffix iterator* is a `regex_token_iterator` object that points to a
final sequence of characters at the end of the target sequence. In a
suffix iterator the member `result` holds a pointer to the data member
`suffix`, the value of the member `suffix.match` is `true`,
`suffix.first` points to the beginning of the final sequence, and
`suffix.second` points to the end of the final sequence.

[*Note 1*: For a suffix iterator, data member `suffix.first` is the
same as the end of the last match found, and `suffix.second` is the same
as the end of the target sequence. — *end note*]

The *current match* is `(*position).prefix()` if `subs[N] == -1`, or
`(*position)[subs[N]]` for any other value of `subs[N]`.

##### Constructors <a id="re.tokiter.cnstr">[[re.tokiter.cnstr]]</a>

``` cpp
regex_token_iterator();
```

*Effects:* Constructs the end-of-sequence iterator.

``` cpp
regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                     const regex_type& re,
                     int submatch = 0,
                     regex_constants::match_flag_type m = regex_constants::match_default);

regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                     const regex_type& re,
                     const vector<int>& submatches,
                     regex_constants::match_flag_type m = regex_constants::match_default);

regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                     const regex_type& re,
                     initializer_list<int> submatches,
                     regex_constants::match_flag_type m = regex_constants::match_default);

template<size_t N>
  regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                       const regex_type& re,
                       const int (&submatches)[N],
                       regex_constants::match_flag_type m = regex_constants::match_default);
```

*Preconditions:* Each of the initialization values of `submatches` is
`>= -1`.

*Effects:* The first constructor initializes the member `subs` to hold
the single value `submatch`. The second, third, and fourth constructors
initialize the member `subs` to hold a copy of the sequence of integer
values pointed to by the iterator range \[`begin(submatches)`,
`end(submatches)`).

Each constructor then sets `N` to 0, and `position` to
`position_iterator(a, b, re, m)`. If `position` is not an
end-of-sequence iterator the constructor sets `result` to the address of
the current match. Otherwise if any of the values stored in `subs` is
equal to -1 the constructor sets `*this` to a suffix iterator that
points to the range \[`a`, `b`), otherwise the constructor sets `*this`
to an end-of-sequence iterator.

##### Comparisons <a id="re.tokiter.comp">[[re.tokiter.comp]]</a>

``` cpp
bool operator==(const regex_token_iterator& right) const;
```

*Returns:* `true` if `*this` and `right` are both end-of-sequence
iterators, or if `*this` and `right` are both suffix iterators and
`suffix == right.suffix`; otherwise returns `false` if `*this` or
`right` is an end-of-sequence iterator or a suffix iterator. Otherwise
returns `true` if `position == right.position`, `N == right.N`, and
`subs == right.subs`. Otherwise returns `false`.

##### Indirection <a id="re.tokiter.deref">[[re.tokiter.deref]]</a>

``` cpp
const value_type& operator*() const;
```

*Returns:* `*result`.

``` cpp
const value_type* operator->() const;
```

*Returns:* `result`.

##### Increment <a id="re.tokiter.incr">[[re.tokiter.incr]]</a>

``` cpp
regex_token_iterator& operator++();
```

*Effects:* Constructs a local variable `prev` of type
`position_iterator`, initialized with the value of `position`.

If `*this` is a suffix iterator, sets `*this` to an end-of-sequence
iterator.

Otherwise, if `N + 1 < subs.size()`, increments `N` and sets `result` to
the address of the current match.

Otherwise, sets `N` to 0 and increments `position`. If `position` is not
an end-of-sequence iterator the operator sets `result` to the address of
the current match.

Otherwise, if any of the values stored in `subs` is equal to -1 and
`prev->suffix().length()` is not 0 the operator sets `*this` to a suffix
iterator that points to the range \[`prev->suffix().first`,
`prev->suffix().second`).

Otherwise, sets `*this` to an end-of-sequence iterator.

*Returns:* `*this`.

``` cpp
regex_token_iterator& operator++(int);
```

*Effects:* Constructs a copy `tmp` of `*this`, then calls `++(*this)`.

*Returns:* `tmp`.

### Modified ECMAScript regular expression grammar <a id="re.grammar">[[re.grammar]]</a>

The regular expression grammar recognized by `basic_regex` objects
constructed with the ECMAScript flag is that specified by ECMA-262,
except as specified below.

Objects of type specialization of `basic_regex` store within themselves
a default-constructed instance of their `traits` template parameter,
henceforth referred to as `traits_inst`. This `traits_inst` object is
used to support localization of the regular expression; `basic_regex`
member functions shall not call any locale dependent C or C++ API,
including the formatted string input functions. Instead they shall call
the appropriate traits member function to achieve the required effect.

The following productions within the ECMAScript grammar are modified as
follows:

``` bnf
\renontermdef{ClassAtom}
  '-'
  ClassAtomNoDash
  ClassAtomExClass
  ClassAtomCollatingElement
  ClassAtomEquivalence
```

``` bnf
\renontermdef{IdentityEscape}
  SourceCharacter \textbf{but not} 'c'
```

The following new productions are then added:

``` bnf
\renontermdef{ClassAtomExClass}
  '[:' ClassName ':]'
```

``` bnf
\renontermdef{ClassAtomCollatingElement}
  '[.' ClassName '.]'
```

``` bnf
\renontermdef{ClassAtomEquivalence}
  '[=' ClassName '=]'
```

``` bnf
\renontermdef{ClassName}
  ClassNameCharacter
  ClassNameCharacter ClassName
```

``` bnf
\renontermdef{ClassNameCharacter}
  SourceCharacter \textbf{but not one of} '.' \textbf{or} '=' \textbf{or} ':'
```

The productions , and provide functionality equivalent to that of the
same features in regular expressions in POSIX.

The regular expression grammar may be modified by any
`regex_constants::syntax_option_type` flags specified when constructing
an object of type specialization of `basic_regex` according to the rules
in [[re.synopt]].

A production, when used in , is not valid if
`traits_inst.lookup_classname` returns zero for that name. The names
recognized as valid s are determined by the type of the traits class,
but at least the following names shall be recognized: `alnum`, `alpha`,
`blank`, `cntrl`, `digit`, `graph`, `lower`, `print`, `punct`, `space`,
`upper`, `xdigit`, `d`, `s`, `w`. In addition the following expressions
shall be equivalent:

``` cpp
\d \textnormal{and} [[:digit:]]

\D \textnormal{and} [^[:digit:]]

\s \textnormal{and} [[:space:]]

\S \textnormal{and} [^[:space:]]

\w \textnormal{and} [_[:alnum:]]

\W \textnormal{and} [^_[:alnum:]]
```

A production when used in a production is not valid if the value
returned by `traits_inst.lookup_collatename` for that name is an empty
string.

The results from multiple calls to `traits_inst.lookup_classname` can be
bitwise ’ed together and subsequently passed to `traits_inst.isctype`.

A production when used in a production is not valid if the value
returned by `traits_inst.lookup_collatename` for that name is an empty
string or if the value returned by `traits_inst.transform_primary` for
the result of the call to `traits_inst.lookup_collatename` is an empty
string.

When the sequence of characters being transformed to a finite state
machine contains an invalid class name the translator shall throw an
exception object of type `regex_error`.

If the *CV* of a *UnicodeEscapeSequence* is greater than the largest
value that can be held in an object of type `charT` the translator shall
throw an exception object of type `regex_error`.

[*Note 1*: This means that values of the form `"\uxxxx"` that do not
fit in a character are invalid. — *end note*]

Where the regular expression grammar requires the conversion of a
sequence of characters to an integral value, this is accomplished by
calling `traits_inst.value`.

The behavior of the internal finite state machine representation when
used to match a sequence of characters is as described in ECMA-262. The
behavior is modified according to any `match_flag_type` flags
[[re.matchflag]] specified when using the regular expression object in
one of the regular expression algorithms [[re.alg]]. The behavior is
also localized by interaction with the traits class template parameter
as follows:

- During matching of a regular expression finite state machine against a
  sequence of characters, two characters `c` and `d` are compared using
  the following rules:
  - if `(flags() & regex_constants::icase)` the two characters are equal
    if
    `traits_inst.translate_nocase(c) == traits_inst.translate_nocase(d)`;
  - otherwise, if `flags() & regex_constants::collate` the two
    characters are equal if
    `traits_inst.translate(c) == traits_inst.translate(d)`;
  - otherwise, the two characters are equal if `c == d`.
- During matching of a regular expression finite state machine against a
  sequence of characters, comparison of a collating element range
  `c1-c2` against a character `c` is conducted as follows: if
  `flags() & regex_constants::collate` is `false` then the character `c`
  is matched if `c1
  <= c && c <= c2`, otherwise `c` is matched in accordance with the
  following algorithm:
  ``` cpp
  string_type str1 = string_type(1,
    flags() & icase ?
      traits_inst.translate_nocase(c1) : traits_inst.translate(c1));
  string_type str2 = string_type(1,
    flags() & icase ?
      traits_inst.translate_nocase(c2) : traits_inst.translate(c2));
  string_type str = string_type(1,
    flags() & icase ?
      traits_inst.translate_nocase(c) : traits_inst.translate(c));
  return traits_inst.transform(str1.begin(), str1.end())
        <= traits_inst.transform(str.begin(), str.end())
    && traits_inst.transform(str.begin(), str.end())
        <= traits_inst.transform(str2.begin(), str2.end());
  ```
- During matching of a regular expression finite state machine against a
  sequence of characters, testing whether a collating element is a
  member of a primary equivalence class is conducted by first converting
  the collating element and the equivalence class to sort keys using
  `traits::transform_primary`, and then comparing the sort keys for
  equality.
- During matching of a regular expression finite state machine against a
  sequence of characters, a character `c` is a member of a character
  class designated by an iterator range \[`first`, `last`) if
  `traits_inst.isctype(c, traits_inst.lookup_classname(first, last, flags() & icase))`
  is `true`.

## Null-terminated sequence utilities <a id="text.c.strings">[[text.c.strings]]</a>

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

#define \libmacro{WEOF} see below
```

The contents and meaning of the header `<cwctype>` are the same as the C
standard library header `<wctype.h>`.

### Header `<cwchar>` synopsis <a id="cwchar.syn">[[cwchar.syn]]</a>

``` cpp
#define __STDC_VERSION_WCHAR_H__ 202311L

namespace std {
  using size_t = see [support.types.layout];                                             // freestanding
  using mbstate_t = see below;                                          // freestanding
  using wint_t = see below;                                             // freestanding

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
  wchar_t* wcscpy(wchar_t* s1, const wchar_t* s2);                      // freestanding
  wchar_t* wcsncpy(wchar_t* s1, const wchar_t* s2, size_t n);           // freestanding
  wchar_t* wmemcpy(wchar_t* s1, const wchar_t* s2, size_t n);           // freestanding
  wchar_t* wmemmove(wchar_t* s1, const wchar_t* s2, size_t n);          // freestanding
  wchar_t* wcscat(wchar_t* s1, const wchar_t* s2);                      // freestanding
  wchar_t* wcsncat(wchar_t* s1, const wchar_t* s2, size_t n);           // freestanding
  int wcscmp(const wchar_t* s1, const wchar_t* s2);                     // freestanding
  int wcscoll(const wchar_t* s1, const wchar_t* s2);
  int wcsncmp(const wchar_t* s1, const wchar_t* s2, size_t n);          // freestanding
  size_t wcsxfrm(wchar_t* s1, const wchar_t* s2, size_t n);
  int wmemcmp(const wchar_t* s1, const wchar_t* s2, size_t n);          // freestanding
  const wchar_t* wcschr(const wchar_t* s, wchar_t c);                   // freestanding; see [library.c]
  wchar_t* wcschr(wchar_t* s, wchar_t c);                               // freestanding; see [library.c]
  size_t wcscspn(const wchar_t* s1, const wchar_t* s2);                 // freestanding
  const wchar_t* wcspbrk(const wchar_t* s1, const wchar_t* s2);         // freestanding; see [library.c]
  wchar_t* wcspbrk(wchar_t* s1, const wchar_t* s2);                     // freestanding; see [library.c]
  const wchar_t* wcsrchr(const wchar_t* s, wchar_t c);                  // freestanding; see [library.c]
  wchar_t* wcsrchr(wchar_t* s, wchar_t c);                              // freestanding; see [library.c]
  size_t wcsspn(const wchar_t* s1, const wchar_t* s2);                  // freestanding
  const wchar_t* wcsstr(const wchar_t* s1, const wchar_t* s2);          // freestanding; see [library.c]
  wchar_t* wcsstr(wchar_t* s1, const wchar_t* s2);                      // freestanding; see [library.c]
  wchar_t* wcstok(wchar_t* s1, const wchar_t* s2, wchar_t** ptr);       // freestanding
  const wchar_t* wmemchr(const wchar_t* s, wchar_t c, size_t n);        // freestanding; see [library.c]
  wchar_t* wmemchr(wchar_t* s, wchar_t c, size_t n);                    // freestanding; see [library.c]
  size_t wcslen(const wchar_t* s);                                      // freestanding
  wchar_t* wmemset(wchar_t* s, wchar_t c, size_t n);                    // freestanding
  size_t wcsftime(wchar_t* s, size_t maxsize, const wchar_t* format, const tm* timeptr);
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

#define \libmacro{NULL} see [support.types.nullptr]                                                  // freestanding
#define \libmacro{WCHAR_MAX} see below                                             // freestanding
#define \libmacro{WCHAR_MIN} see below                                             // freestanding
#define \libmacro{WEOF} see below                                                  // freestanding
#define \libmacro{WCHAR_WIDTH} see below                                           // freestanding
```

The contents and meaning of the header `<cwchar>` are the same as the C
standard library header `<wchar.h>`, except that it does not declare a
type `wchar_t`.

[*Note 1*: The functions `wcschr`, `wcspbrk`, `wcsrchr`, `wcsstr`, and
`wmemchr` have different signatures in this document, but they have the
same behavior as in the C standard library [[library.c]]. — *end note*]

### Header `<cuchar>` synopsis <a id="cuchar.syn">[[cuchar.syn]]</a>

``` cpp
#define __STDC_VERSION_UCHAR_H__ 202311L

namespace std {
  using mbstate_t = see below;
  using size_t = see [support.types.layout];

  size_t mbrtoc8(char8_t* pc8, const char* s, size_t n, mbstate_t* ps);
  size_t c8rtomb(char* s, char8_t c8, mbstate_t* ps);
  size_t mbrtoc16(char16_t* pc16, const char* s, size_t n, mbstate_t* ps);
  size_t c16rtomb(char* s, char16_t c16, mbstate_t* ps);
  size_t mbrtoc32(char32_t* pc32, const char* s, size_t n, mbstate_t* ps);
  size_t c32rtomb(char* s, char32_t c32, mbstate_t* ps);
}
```

The contents and meaning of the header `<cuchar>` are the same as the C
standard library header `<uchar.h>`, except that it does not declare
types `char8_t`, `char16_t`, or `char32_t`.

### Multibyte / wide string and character conversion functions <a id="c.mb.wcs">[[c.mb.wcs]]</a>

[*Note 1*: The headers `<cstdlib>`, `<cuchar>`, and `<cwchar>` declare
the functions described in this subclause. — *end note*]

``` cpp
int mbsinit(const mbstate_t* ps);
int mblen(const char* s, size_t n);
size_t mbstowcs(wchar_t* pwcs, const char* s, size_t n);
size_t wcstombs(char* s, const wchar_t* pwcs, size_t n);
```

*Effects:* These functions have the semantics specified in the C
standard library.

``` cpp
int mbtowc(wchar_t* pwc, const char* s, size_t n);
int wctomb(char* s, wchar_t wchar);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* Calls to these functions may introduce a data
race [[res.on.data.races]] with other calls to the same function.

``` cpp
size_t mbrlen(const char* s, size_t n, mbstate_t* ps);
size_t mbrtowc(wchar_t* pwc, const char* s, size_t n, mbstate_t* ps);
size_t wcrtomb(char* s, wchar_t wc, mbstate_t* ps);
size_t mbrtoc8(char8_t* pc8, const char* s, size_t n, mbstate_t* ps);
size_t c8rtomb(char* s, char8_t c8, mbstate_t* ps);
size_t mbrtoc16(char16_t* pc16, const char* s, size_t n, mbstate_t* ps);
size_t c16rtomb(char* s, char16_t c16, mbstate_t* ps);
size_t mbrtoc32(char32_t* pc32, const char* s, size_t n, mbstate_t* ps);
size_t c32rtomb(char* s, char32_t c32, mbstate_t* ps);
size_t mbsrtowcs(wchar_t* dst, const char** src, size_t len, mbstate_t* ps);
size_t wcsrtombs(char* dst, const wchar_t** src, size_t len, mbstate_t* ps);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* Calling these functions with an `mbstate_t*` argument that is
a null pointer value may introduce a data race [[res.on.data.races]]
with other calls to the same function with an `mbstate_t*` argument that
is a null pointer value.

<!-- Section link definitions -->
[c.locales]: #c.locales
[c.mb.wcs]: #c.mb.wcs
[category.collate]: #category.collate
[category.ctype]: #category.ctype
[category.ctype.general]: #category.ctype.general
[category.messages]: #category.messages
[category.messages.general]: #category.messages.general
[category.monetary]: #category.monetary
[category.monetary.general]: #category.monetary.general
[category.numeric]: #category.numeric
[category.numeric.general]: #category.numeric.general
[category.time]: #category.time
[category.time.general]: #category.time.general
[cctype.syn]: #cctype.syn
[charconv]: #charconv
[charconv.from.chars]: #charconv.from.chars
[charconv.syn]: #charconv.syn
[charconv.to.chars]: #charconv.to.chars
[classification]: #classification
[clocale.data.races]: #clocale.data.races
[clocale.syn]: #clocale.syn
[conversions.character]: #conversions.character
[cuchar.syn]: #cuchar.syn
[cwchar.syn]: #cwchar.syn
[cwctype.syn]: #cwctype.syn
[facet.ctype.char.dtor]: #facet.ctype.char.dtor
[facet.ctype.char.members]: #facet.ctype.char.members
[facet.ctype.char.statics]: #facet.ctype.char.statics
[facet.ctype.char.virtuals]: #facet.ctype.char.virtuals
[facet.ctype.special]: #facet.ctype.special
[facet.ctype.special.general]: #facet.ctype.special.general
[facet.num.get.members]: #facet.num.get.members
[facet.num.get.virtuals]: #facet.num.get.virtuals
[facet.num.put.members]: #facet.num.put.members
[facet.num.put.virtuals]: #facet.num.put.virtuals
[facet.numpunct]: #facet.numpunct
[facet.numpunct.members]: #facet.numpunct.members
[facet.numpunct.virtuals]: #facet.numpunct.virtuals
[format]: #format
[format.arg]: #format.arg
[format.arg.store]: #format.arg.store
[format.args]: #format.args
[format.arguments]: #format.arguments
[format.context]: #format.context
[format.err.report]: #format.err.report
[format.error]: #format.error
[format.fmt.string]: #format.fmt.string
[format.formattable]: #format.formattable
[format.formatter]: #format.formatter
[format.formatter.locking]: #format.formatter.locking
[format.formatter.spec]: #format.formatter.spec
[format.functions]: #format.functions
[format.parse.ctx]: #format.parse.ctx
[format.range]: #format.range
[format.range.fmtdef]: #format.range.fmtdef
[format.range.fmtkind]: #format.range.fmtkind
[format.range.fmtmap]: #format.range.fmtmap
[format.range.fmtset]: #format.range.fmtset
[format.range.fmtstr]: #format.range.fmtstr
[format.range.formatter]: #format.range.formatter
[format.string]: #format.string
[format.string.escaped]: #format.string.escaped
[format.string.general]: #format.string.general
[format.string.std]: #format.string.std
[format.syn]: #format.syn
[format.tuple]: #format.tuple
[formatter.requirements]: #formatter.requirements
[locale]: #locale
[locale.categories]: #locale.categories
[locale.categories.general]: #locale.categories.general
[locale.category]: #locale.category
[locale.codecvt]: #locale.codecvt
[locale.codecvt.byname]: #locale.codecvt.byname
[locale.codecvt.general]: #locale.codecvt.general
[locale.codecvt.members]: #locale.codecvt.members
[locale.codecvt.virtuals]: #locale.codecvt.virtuals
[locale.collate]: #locale.collate
[locale.collate.byname]: #locale.collate.byname
[locale.collate.general]: #locale.collate.general
[locale.collate.members]: #locale.collate.members
[locale.collate.virtuals]: #locale.collate.virtuals
[locale.cons]: #locale.cons
[locale.convenience]: #locale.convenience
[locale.ctype]: #locale.ctype
[locale.ctype.byname]: #locale.ctype.byname
[locale.ctype.general]: #locale.ctype.general
[locale.ctype.members]: #locale.ctype.members
[locale.ctype.virtuals]: #locale.ctype.virtuals
[locale.facet]: #locale.facet
[locale.general]: #locale.general
[locale.global.templates]: #locale.global.templates
[locale.id]: #locale.id
[locale.members]: #locale.members
[locale.messages]: #locale.messages
[locale.messages.byname]: #locale.messages.byname
[locale.messages.general]: #locale.messages.general
[locale.messages.members]: #locale.messages.members
[locale.messages.virtuals]: #locale.messages.virtuals
[locale.money.get]: #locale.money.get
[locale.money.get.general]: #locale.money.get.general
[locale.money.get.members]: #locale.money.get.members
[locale.money.get.virtuals]: #locale.money.get.virtuals
[locale.money.put]: #locale.money.put
[locale.money.put.general]: #locale.money.put.general
[locale.money.put.members]: #locale.money.put.members
[locale.money.put.virtuals]: #locale.money.put.virtuals
[locale.moneypunct]: #locale.moneypunct
[locale.moneypunct.byname]: #locale.moneypunct.byname
[locale.moneypunct.general]: #locale.moneypunct.general
[locale.moneypunct.members]: #locale.moneypunct.members
[locale.moneypunct.virtuals]: #locale.moneypunct.virtuals
[locale.nm.put]: #locale.nm.put
[locale.nm.put.general]: #locale.nm.put.general
[locale.num.get]: #locale.num.get
[locale.num.get.general]: #locale.num.get.general
[locale.numpunct]: #locale.numpunct
[locale.numpunct.byname]: #locale.numpunct.byname
[locale.numpunct.general]: #locale.numpunct.general
[locale.operators]: #locale.operators
[locale.statics]: #locale.statics
[locale.syn]: #locale.syn
[locale.time.get]: #locale.time.get
[locale.time.get.byname]: #locale.time.get.byname
[locale.time.get.general]: #locale.time.get.general
[locale.time.get.members]: #locale.time.get.members
[locale.time.get.virtuals]: #locale.time.get.virtuals
[locale.time.put]: #locale.time.put
[locale.time.put.byname]: #locale.time.put.byname
[locale.time.put.general]: #locale.time.put.general
[locale.time.put.members]: #locale.time.put.members
[locale.time.put.virtuals]: #locale.time.put.virtuals
[locale.types]: #locale.types
[locales]: #locales
[localization]: #localization
[localization.general]: #localization.general
[re]: #re
[re.alg]: #re.alg
[re.alg.match]: #re.alg.match
[re.alg.replace]: #re.alg.replace
[re.alg.search]: #re.alg.search
[re.badexp]: #re.badexp
[re.const]: #re.const
[re.const.general]: #re.const.general
[re.err]: #re.err
[re.except]: #re.except
[re.general]: #re.general
[re.grammar]: #re.grammar
[re.iter]: #re.iter
[re.matchflag]: #re.matchflag
[re.regex]: #re.regex
[re.regex.assign]: #re.regex.assign
[re.regex.construct]: #re.regex.construct
[re.regex.general]: #re.regex.general
[re.regex.locale]: #re.regex.locale
[re.regex.nonmemb]: #re.regex.nonmemb
[re.regex.operations]: #re.regex.operations
[re.regex.swap]: #re.regex.swap
[re.regiter]: #re.regiter
[re.regiter.cnstr]: #re.regiter.cnstr
[re.regiter.comp]: #re.regiter.comp
[re.regiter.deref]: #re.regiter.deref
[re.regiter.general]: #re.regiter.general
[re.regiter.incr]: #re.regiter.incr
[re.req]: #re.req
[re.results]: #re.results
[re.results.acc]: #re.results.acc
[re.results.all]: #re.results.all
[re.results.const]: #re.results.const
[re.results.form]: #re.results.form
[re.results.general]: #re.results.general
[re.results.nonmember]: #re.results.nonmember
[re.results.size]: #re.results.size
[re.results.state]: #re.results.state
[re.results.swap]: #re.results.swap
[re.submatch]: #re.submatch
[re.submatch.general]: #re.submatch.general
[re.submatch.members]: #re.submatch.members
[re.submatch.op]: #re.submatch.op
[re.syn]: #re.syn
[re.synopt]: #re.synopt
[re.tokiter]: #re.tokiter
[re.tokiter.cnstr]: #re.tokiter.cnstr
[re.tokiter.comp]: #re.tokiter.comp
[re.tokiter.deref]: #re.tokiter.deref
[re.tokiter.general]: #re.tokiter.general
[re.tokiter.incr]: #re.tokiter.incr
[re.traits]: #re.traits
[text]: #text
[text.c.strings]: #text.c.strings
[text.encoding]: #text.encoding
[text.encoding.aliases]: #text.encoding.aliases
[text.encoding.class]: #text.encoding.class
[text.encoding.cmp]: #text.encoding.cmp
[text.encoding.general]: #text.encoding.general
[text.encoding.hash]: #text.encoding.hash
[text.encoding.id]: #text.encoding.id
[text.encoding.members]: #text.encoding.members
[text.encoding.overview]: #text.encoding.overview
[text.encoding.syn]: #text.encoding.syn
[text.general]: #text.general

<!-- Link reference definitions -->
[alg.lex.comparison]: algorithms.md#alg.lex.comparison
[alg.sort,vector]: #alg.sort,vector
[algorithms]: algorithms.md#algorithms
[algorithms.requirements]: algorithms.md#algorithms.requirements
[basic.fundamental]: basic.md#basic.fundamental
[basic.start.static]: basic.md#basic.start.static
[bitmask.types]: library.md#bitmask.types
[c.files]: input.md#c.files
[c.locales]: #c.locales
[category.ctype]: #category.ctype
[category.monetary]: #category.monetary
[category.numeric]: #category.numeric
[category.time]: #category.time
[character.seq.general]: library.md#character.seq.general
[charconv]: #charconv
[container.alloc.reqmts]: containers.md#container.alloc.reqmts
[container.reqmts]: containers.md#container.reqmts
[container.requirements.general]: containers.md#container.requirements.general
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[defns.character.container]: #defns.character.container
[defns.ntcts]: #defns.ntcts
[enumerated.types]: library.md#enumerated.types
[expr.const]: expr.md#expr.const
[file.streams]: input.md#file.streams
[format]: #format
[format.align]: #format.align
[format.err.report]: #format.err.report
[format.escape.sequences]: #format.escape.sequences
[format.formatter.spec]: #format.formatter.spec
[format.functions]: #format.functions
[format.sign]: #format.sign
[format.string]: #format.string
[format.string.escaped]: #format.string.escaped
[format.string.std]: #format.string.std
[format.type.bool]: #format.type.bool
[format.type.char]: #format.type.char
[format.type.float]: #format.type.float
[format.type.int]: #format.type.int
[format.type.ptr]: #format.type.ptr
[format.type.string]: #format.type.string
[formatter]: #formatter
[formatter.basic]: #formatter.basic
[formatter.range.type]: #formatter.range.type
[formatter.requirements]: #formatter.requirements
[formatter.tuple.type]: #formatter.tuple.type
[forward.iterators]: iterators.md#forward.iterators
[input.iterators]: iterators.md#input.iterators
[ios.base]: input.md#ios.base
[istream.formatted]: input.md#istream.formatted
[istream.formatted.reqmts]: input.md#istream.formatted.reqmts
[iterator.concept.bidir]: iterators.md#iterator.concept.bidir
[iterator.concept.output]: iterators.md#iterator.concept.output
[iterator.requirements]: iterators.md#iterator.requirements
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[lex.charset]: lex.md#lex.charset
[lex.string.literal]: #lex.string.literal
[library.c]: library.md#library.c
[locale.categories]: #locale.categories
[locale.category]: #locale.category
[locale.category.facets]: #locale.category.facets
[locale.codecvt.inout]: #locale.codecvt.inout
[locale.codecvt.unshift]: #locale.codecvt.unshift
[locale.ctype.members]: #locale.ctype.members
[locale.facet]: #locale.facet
[locale.spec]: #locale.spec
[locale.time.get.dogetdate]: #locale.time.get.dogetdate
[locales]: #locales
[localization]: #localization
[localization.summary]: #localization.summary
[namespace.std]: library.md#namespace.std
[ostream.formatted.reqmts]: input.md#ostream.formatted.reqmts
[output.iterators]: iterators.md#output.iterators
[re]: #re
[re.alg]: #re.alg
[re.alg.match]: #re.alg.match
[re.alg.search]: #re.alg.search
[re.badexp]: #re.badexp
[re.const]: #re.const
[re.err]: #re.err
[re.grammar]: #re.grammar
[re.iter]: #re.iter
[re.matchflag]: #re.matchflag
[re.regex]: #re.regex
[re.req]: #re.req
[re.results]: #re.results
[re.results.const]: #re.results.const
[re.submatch]: #re.submatch
[re.summary]: #re.summary
[re.synopt]: #re.synopt
[re.traits]: #re.traits
[re.traits.classnames]: #re.traits.classnames
[res.on.data.races]: library.md#res.on.data.races
[res.on.exception.handling]: library.md#res.on.exception.handling
[round.style]: support.md#round.style
[sequence.reqmts]: containers.md#sequence.reqmts
[setlocale.data.races]: #setlocale.data.races
[strings.general]: strings.md#strings.general
[support.runtime]: support.md#support.runtime
[swappable.requirements]: library.md#swappable.requirements
[tab:locale.category.facets]: #tab:locale.category.facets
[tab:locale.spec]: #tab:locale.spec
[term.trivially.copyable.type]: #term.trivially.copyable.type
[text.c.strings]: #text.c.strings
[text.encoding]: #text.encoding
[text.summary]: #text.summary
[time.format]: time.md#time.format
[unord.hash]: utilities.md#unord.hash

[^1]: In this subclause, the type name `tm` is an incomplete type that
    is defined in `<ctime>`.

[^2]: Note that in the call to `put`, the stream is implicitly converted
    to an `ostreambuf_iterator<charT, traits>`.

[^3]: This is a complete list of requirements; there are no other
    requirements. Thus, a facet class need not have a public copy
    constructor, assignment, default constructor, destructor, etc.

[^4]: When used in a loop, it is faster to cache the `ctype<>` facet and
    use it directly, or use the vector form of `ctype<>::is`.

[^5]: The parameter `c` of `do_widen` is intended to accept values
    derived from *character-literal*s for conversion to the locale’s
    encoding.

[^6]: In other words, the transformed character is not a member of any
    character classification that `c` is not also a member of.

[^7]: Only the `char` (not `unsigned char` and `signed char`) form is
    provided. The specialization is specified in the standard, and not
    left as an implementation detail, because it affects the derivation
    interface for `ctype<char>`.

[^8]: Informally, this means that `basic_filebuf` assumes that the
    mappings from internal to external characters is 1 to N: that a
    `codecvt` facet that is used by `basic_filebuf` can translate
    characters one internal character at a time.

[^9]: Typically these will be characters to return the state to
    `stateT()`.

[^10]: If `encoding()` yields `-1`, then more than `max_length()`
    `externT` elements can be consumed when producing a single `internT`
    character, and additional `externT` elements can appear at the end
    of a sequence after those that yield the final `internT` character.

[^11]: Parsing `"-1"` correctly into, e.g., an `unsigned short` requires
    that the corresponding member `get()` at least extract the sign
    before delegating.

[^12]: The conversion specification `#o` generates a leading `0` which
    is *not* a padding character.

[^13]: Thus, the string `"\003"` specifies groups of 3 digits each, and
    `"3"` probably indicates groups of 51 (!) digits each, because 51 is
    the ASCII value of `"3"`.

[^14]: This function is useful when one string is being compared to many
    other strings.

[^15]: In other words, user confirmation is required for reliable
    parsing of user-entered dates and times, but machine-generated
    formats can be parsed reliably. This allows parsers to be aggressive
    about interpreting user variations on standard formats.

[^16]: This function is intended as a convenience only, for common
    formats, and can return `no_order` in valid locales.

[^17]: The semantics here are different from `ct.narrow`.

[^18]: An array of `char`, rather than an array of `part`, is specified
    for `pattern::field` purely for efficiency.

[^19]: In common U.S. locales this is `’.’`.

[^20]: In common U.S. locales this is `’,’`.

[^21]: To specify grouping by 3s, the value is `"\003"` *not* `"3"`.

[^22]: This is usually the empty string.

[^23]: In common U.S. locales, this is 2.

[^24]: Note that the international symbol returned by `do_curr_symbol()`
    usually contains a space, itself; for example, `"USD "`.

[^25]: Windows is a registered trademark of Microsoft Corporation. This
    information is given for the convenience of users of this document
    and does not constitute an endorsement by ISO or IEC of this
    product.

[^26]: For example, if the parameter `icase` is `true` then
    `[[:lower:]]` is the same as `[[:alpha:]]`.
