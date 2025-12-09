# Regular expressions library <a id="re">[[re]]</a>

## General <a id="re.general">[[re.general]]</a>

This Clause describes components that C++programs may use to perform
operations involving regular expression matching and searching.

The following subclauses describe a basic regular expression class
template and its traits that can handle char-like template arguments,
two specializations of this class template that handle sequences of
`char` and `wchar_t`, a class template that holds the result of a
regular expression match, a series of algorithms that allow a character
sequence to be operated upon by a regular expression, and two iterator
types for enumerating regular expression matches, as described in Table 
[[tab:re.lib.summary]].

**Table: Regular expressions library summary** <a id="tab:re.lib.summary">[tab:re.lib.summary]</a>

| Subclause       |                             | Header    |
| --------------- | --------------------------- | --------- |
| [[re.def]]      | Definitions                 |           |
| [[re.req]]      | Requirements                |           |
| [[re.const]]    | Constants                   |           |
| [[re.badexp]]   | Exception type              |           |
| [[re.traits]]   | Traits                      |           |
| [[re.regex]]    | Regular expression template | `<regex>` |
| [[re.submatch]] | Submatches                  |           |
| [[re.results]]  | Match results               |           |
| [[re.alg]]      | Algorithms                  |           |
| [[re.iter]]     | Iterators                   |           |
| [[re.grammar]]  | Grammar                     |           |


## Definitions <a id="re.def">[[re.def]]</a>

The following definitions shall apply to this Clause:

#### 1 collating element <a id="defns.regex.collating.element">[[defns.regex.collating.element]]</a>

a sequence of one or more characters within the current locale that
collate as if they were a single character.

#### 2 finite state machine <a id="defns.regex.finite.state.machine">[[defns.regex.finite.state.machine]]</a>

an unspecified data structure that is used to represent a regular
expression, and which permits efficient matches against the regular
expression to be obtained.

#### 3 format specifier <a id="defns.regex.format.specifier">[[defns.regex.format.specifier]]</a>

a sequence of one or more characters that is to be replaced with some
part of a regular expression match.

#### 4 matched <a id="defns.regex.matched">[[defns.regex.matched]]</a>

a sequence of zero or more characters is matched by a regular expression
when the characters in the sequence correspond to a sequence of
characters defined by the pattern.

#### 5 primary equivalence class <a id="defns.regex.primary.equivalence.class">[[defns.regex.primary.equivalence.class]]</a>

a set of one or more characters which share the same primary sort key:
that is the sort key weighting that depends only upon character shape,
and not accents, case, or locale specific tailorings.

#### 6 regular expression <a id="defns.regex.regular.expression">[[defns.regex.regular.expression]]</a>

a pattern that selects specific strings from a set of character strings.

#### 7 sub-expression <a id="defns.regex.subexpression">[[defns.regex.subexpression]]</a>

a subset of a regular expression that has been marked by parenthesis.

## Requirements <a id="re.req">[[re.req]]</a>

This subclause defines requirements on classes representing regular
expression traits. The class template `regex_traits`, defined in Clause 
[[re.traits]], satisfies these requirements.

The class template `basic_regex`, defined in Clause  [[re.regex]], needs
a set of related types and functions to complete the definition of its
semantics. These types and functions are provided as a set of member
typedefs and functions in the template parameter `traits` used by the
`basic_regex` class template. This subclause defines the semantics of
these members.

To specialize class template `basic_regex` for a character container
`CharT` and its related regular expression traits class `Traits`, use
`basic_regex<CharT, Traits>`.

In Table  [[tab:re:RegexpTraits]] `X` denotes a traits class defining
types and functions for the character container type `charT`; `u` is an
object of type `X`; `v` is an object of type `const 
X`; `p` is a value of type `const charT*`; `I1` and `I2` are input
iterators ([[input.iterators]]); `F1` and `F2` are forward iterators (
[[forward.iterators]]); `c` is a value of type `const charT`; `s` is an
object of type `X::string_type`; `cs` is an object of type
`const X::string_type`; `b` is a value of type `bool`; `I` is a value of
type `int`; `cl` is an object of type `X::char_class_type`, and `loc` is
an object of type `X::locale_type`.

Class template `regex_traits` satisfies the requirements for a regular
expression traits class when it is specialized for `char` or `wchar_t`.
This class template is described in the header `<regex>`, and is
described in Clause  [[re.traits]].

## Header `<regex>` synopsis <a id="re.syn">[[re.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  // [re.const], regex constants:
  namespace regex_constants {
    enum error_type;
  } // namespace regex_constants

  // [re.badexp], class regex_error:
  class regex_error;

  // [re.traits], class template regex_traits:
  template <class charT> struct regex_traits;

  // [re.regex], class template basic_regex:
  template <class charT, class traits = regex_traits<charT> > class basic_regex;

  typedef basic_regex<char>    regex;
  typedef basic_regex<wchar_t> wregex;

  // [re.regex.swap], basic_regex swap:
  template <class charT, class traits>
    void swap(basic_regex<charT, traits>& e1, basic_regex<charT, traits>& e2);

  // [re.submatch], class template sub_match:
  template <class BidirectionalIterator>
    class sub_match;

  typedef sub_match<const char*>             csub_match;
  typedef sub_match<const wchar_t*>          wcsub_match;
  typedef sub_match<string::const_iterator>  ssub_match;
  typedef sub_match<wstring::const_iterator> wssub_match;

  // [re.submatch.op], sub_match non-member operators:
  template <class BiIter>
    bool operator==(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator!=(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator<(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator<=(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator>=(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator>(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);


  template <class BiIter, class ST, class SA>
    bool operator==(
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
      const sub_match<BiIter>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator!=(
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
      const sub_match<BiIter>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator<(
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
      const sub_match<BiIter>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator>(
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
      const sub_match<BiIter>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator>=(
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
      const sub_match<BiIter>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator<=(
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
      const sub_match<BiIter>& rhs);

  template <class BiIter, class ST, class SA>
    bool operator==(
      const sub_match<BiIter>& lhs,
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator!=(
      const sub_match<BiIter>& lhs,
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator<(
      const sub_match<BiIter>& lhs,
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator>(
      const sub_match<BiIter>& lhs,
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator>=(
      const sub_match<BiIter>& lhs,
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
  template <class BiIter, class ST, class SA>
    bool operator<=(
      const sub_match<BiIter>& lhs,
      const basic_string<
        typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);

  template <class BiIter>
    bool operator==(typename iterator_traits<BiIter>::value_type const* lhs,
                    const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator!=(typename iterator_traits<BiIter>::value_type const* lhs,
                    const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator<(typename iterator_traits<BiIter>::value_type const* lhs,
                   const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator>(typename iterator_traits<BiIter>::value_type const* lhs,
                   const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator>=(typename iterator_traits<BiIter>::value_type const* lhs,
                    const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator<=(typename iterator_traits<BiIter>::value_type const* lhs,
                    const sub_match<BiIter>& rhs);

  template <class BiIter>
    bool operator==(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const* rhs);
  template <class BiIter>
    bool operator!=(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const* rhs);
  template <class BiIter>
    bool operator<(const sub_match<BiIter>& lhs,
                   typename iterator_traits<BiIter>::value_type const* rhs);
  template <class BiIter>
    bool operator>(const sub_match<BiIter>& lhs,
                   typename iterator_traits<BiIter>::value_type const* rhs);
  template <class BiIter>
    bool operator>=(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const* rhs);
  template <class BiIter>
    bool operator<=(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const* rhs);

  template <class BiIter>
    bool operator==(typename iterator_traits<BiIter>::value_type const& lhs,
                    const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator!=(typename iterator_traits<BiIter>::value_type const& lhs,
                    const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator<(typename iterator_traits<BiIter>::value_type const& lhs,
                   const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator>(typename iterator_traits<BiIter>::value_type const& lhs,
                   const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator>=(typename iterator_traits<BiIter>::value_type const& lhs,
                    const sub_match<BiIter>& rhs);
  template <class BiIter>
    bool operator<=(typename iterator_traits<BiIter>::value_type const& lhs,
                    const sub_match<BiIter>& rhs);

  template <class BiIter>
    bool operator==(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const& rhs);
  template <class BiIter>
    bool operator!=(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const& rhs);
  template <class BiIter>
    bool operator<(const sub_match<BiIter>& lhs,
                   typename iterator_traits<BiIter>::value_type const& rhs);
  template <class BiIter>
    bool operator>(const sub_match<BiIter>& lhs,
                   typename iterator_traits<BiIter>::value_type const& rhs);
  template <class BiIter>
    bool operator>=(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const& rhs);
  template <class BiIter>
    bool operator<=(const sub_match<BiIter>& lhs,
                    typename iterator_traits<BiIter>::value_type const& rhs);

  template <class charT, class ST, class BiIter>
    basic_ostream<charT, ST>&
    operator<<(basic_ostream<charT, ST>& os, const sub_match<BiIter>& m);

  // [re.results], class template match_results:
  template <class BidirectionalIterator,
            class Allocator = allocator<sub_match<BidirectionalIterator> > >
    class match_results;

  typedef match_results<const char*>             cmatch;
  typedef match_results<const wchar_t*>          wcmatch;
  typedef match_results<string::const_iterator>  smatch;
  typedef match_results<wstring::const_iterator> wsmatch;

  // match_results comparisons
  template <class BidirectionalIterator, class Allocator>
    bool operator== (const match_results<BidirectionalIterator, Allocator>& m1,
                     const match_results<BidirectionalIterator, Allocator>& m2);
  template <class BidirectionalIterator, class Allocator>
    bool operator!= (const match_results<BidirectionalIterator, Allocator>& m1,
                     const match_results<BidirectionalIterator, Allocator>& m2);

  // [re.results.swap], match_results swap:
  template <class BidirectionalIterator, class Allocator>
    void swap(match_results<BidirectionalIterator, Allocator>& m1,
              match_results<BidirectionalIterator, Allocator>& m2);

  // [re.alg.match], function template regex_match:
  template <class BidirectionalIterator, class Allocator,
      class charT, class traits>
    bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                     match_results<BidirectionalIterator, Allocator>& m,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags =
                       regex_constants::match_default);
  template <class BidirectionalIterator, class charT, class traits>
  bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
  template <class charT, class Allocator, class traits>
    bool regex_match(const charT* str, match_results<const charT*, Allocator>& m,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags =
                       regex_constants::match_default);
  template <class ST, class SA, class Allocator, class charT, class traits>
    bool regex_match(const basic_string<charT, ST, SA>& s,
                     match_results<
                       typename basic_string<charT, ST, SA>::const_iterator,
                       Allocator>& m,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags =
                       regex_constants::match_default);
  template <class ST, class SA, class Allocator, class charT, class traits>
    bool regex_match(const basic_string<charT, ST, SA>&&,
                     match_results<
                       typename basic_string<charT, ST, SA>::const_iterator,
                       Allocator>&,
                     const basic_regex<charT, traits>&,
                     regex_constants::match_flag_type =
                       regex_constants::match_default) = delete;
  template <class charT, class traits>
    bool regex_match(const charT* str,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags =
                       regex_constants::match_default);
  template <class ST, class SA, class charT, class traits>
    bool regex_match(const basic_string<charT, ST, SA>& s,
                     const basic_regex<charT, traits>& e,
                     regex_constants::match_flag_type flags =
                       regex_constants::match_default);

  // [re.alg.search], function template regex_search:
  template <class BidirectionalIterator, class Allocator,
      class charT, class traits>
    bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                      match_results<BidirectionalIterator, Allocator>& m,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags =
                        regex_constants::match_default);
  template <class BidirectionalIterator, class charT, class traits>
    bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags =
                        regex_constants::match_default);
  template <class charT, class Allocator, class traits>
    bool regex_search(const charT* str,
                      match_results<const charT*, Allocator>& m,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags =
                        regex_constants::match_default);
  template <class charT, class traits>
    bool regex_search(const charT* str,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags =
                        regex_constants::match_default);
  template <class ST, class SA, class charT, class traits>
    bool regex_search(const basic_string<charT, ST, SA>& s,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags =
                        regex_constants::match_default);
  template <class ST, class SA, class Allocator, class charT, class traits>
    bool regex_search(const basic_string<charT, ST, SA>& s,
                      match_results<
                        typename basic_string<charT, ST, SA>::const_iterator,
                        Allocator>& m,
                      const basic_regex<charT, traits>& e,
                      regex_constants::match_flag_type flags =
                        regex_constants::match_default);
  template <class ST, class SA, class Allocator, class charT, class traits>
    bool regex_search(const basic_string<charT, ST, SA>&&,
                      match_results<
                        typename basic_string<charT, ST, SA>::const_iterator,
                        Allocator>&,
                      const basic_regex<charT, traits>&,
                      regex_constants::match_flag_type =
                        regex_constants::match_default) = delete;

  // [re.alg.replace], function template regex_replace:
  template <class OutputIterator, class BidirectionalIterator,
      class traits, class charT, class ST, class SA>
    OutputIterator
    regex_replace(OutputIterator out,
                  BidirectionalIterator first, BidirectionalIterator last,
                  const basic_regex<charT, traits>& e,
                  const basic_string<charT, ST, SA>& fmt,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);
  template <class OutputIterator, class BidirectionalIterator,
      class traits, class charT>
    OutputIterator
    regex_replace(OutputIterator out,
                  BidirectionalIterator first, BidirectionalIterator last,
                  const basic_regex<charT, traits>& e,
                  const charT* fmt,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);
  template <class traits, class charT, class ST, class SA,
      class FST, class FSA>
    basic_string<charT, ST, SA>
    regex_replace(const basic_string<charT, ST, SA>& s,
                  const basic_regex<charT, traits>& e,
                  const basic_string<charT, FST, FSA>& fmt,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);
  template <class traits, class charT, class ST, class SA>
    basic_string<charT, ST, SA>
    regex_replace(const basic_string<charT, ST, SA>& s,
                  const basic_regex<charT, traits>& e,
                  const charT* fmt,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);
  template <class traits, class charT, class ST, class SA>
    basic_string<charT>
    regex_replace(const charT* s,
                  const basic_regex<charT, traits>& e,
                  const basic_string<charT, ST, SA>& fmt,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);
  template <class traits, class charT>
    basic_string<charT>
    regex_replace(const charT* s,
                  const basic_regex<charT, traits>& e,
                  const charT* fmt,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);

  // [re.regiter], class template regex_iterator:
  template <class BidirectionalIterator,
            class charT = typename iterator_traits<
              BidirectionalIterator>::value_type,
            class traits = regex_traits<charT> >
    class regex_iterator;

  typedef regex_iterator<const char*>             cregex_iterator;
  typedef regex_iterator<const wchar_t*>          wcregex_iterator;
  typedef regex_iterator<string::const_iterator>  sregex_iterator;
  typedef regex_iterator<wstring::const_iterator> wsregex_iterator;

  // [re.tokiter], class template regex_token_iterator:
  template <class BidirectionalIterator,
            class charT = typename iterator_traits<
              BidirectionalIterator>::value_type,
            class traits = regex_traits<charT> >
    class regex_token_iterator;

  typedef regex_token_iterator<const char*>             cregex_token_iterator;
  typedef regex_token_iterator<const wchar_t*>          wcregex_token_iterator;
  typedef regex_token_iterator<string::const_iterator>  sregex_token_iterator;
  typedef regex_token_iterator<wstring::const_iterator> wsregex_token_iterator;
}
```

## Namespace `std::regex_constants` <a id="re.const">[[re.const]]</a>

The namespace `std::regex_constants` holds symbolic constants used by
the regular expression library. This namespace provides three types,
`syntax_option_type`, `match_flag_type`, and `error_type`, along with
several constants of these types.

### Bitmask type `syntax_option_type` <a id="re.synopt">[[re.synopt]]</a>

``` cpp
namespace std {
  namespace regex_constants {
    typedef T1 syntax_option_type;
    constexpr syntax_option_type icase = unspecified;
    constexpr syntax_option_type nosubs = unspecified;
    constexpr syntax_option_type optimize = unspecified;
    constexpr syntax_option_type collate = unspecified;
    constexpr syntax_option_type ECMAScript = unspecified;
    constexpr syntax_option_type basic = unspecified;
    constexpr syntax_option_type extended = unspecified;
    constexpr syntax_option_type awk = unspecified;
    constexpr syntax_option_type grep = unspecified;
    constexpr syntax_option_type egrep = unspecified;
  }
}
```

The type `syntax_option_type` is an implementation-defined bitmask
type ([[bitmask.types]]). Setting its elements has the effects listed
in table  [[tab:re:syntaxoption]]. A valid value of type
`syntax_option_type` shall have at most one of the grammar elements
`ECMAScript`, `basic`, `extended`, `awk`, `grep`, `egrep`, set. If no
grammar element is set, the default grammar is `ECMAScript`.

**Table: `syntax_option_type` effects** <a id="tab:re:syntaxoption">[tab:re:syntaxoption]</a>

| Element        | Effect(s) if set                                                                                                                                                                                                                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| % `icase`      | Specifies that matching of regular expressions against a character container sequence shall be performed without regard to case. \indexlibrary{\idxcode{syntax_option_type}!\idxcode{icase}}%                                                                                                                                             |
| % `nosubs`     | Specifies that no sub-expressions shall be considered to be marked, so that when a regular expression is matched against a character container sequence, no sub-expression matches shall be stored in the supplied `match_results` structure. \indexlibrary{\idxcode{syntax_option_type}!\idxcode{nosubs}}%                               |
| % `optimize`   | Specifies that the regular expression engine should pay more attention to the speed with which regular expressions are matched, and less to the speed with which regular expression objects are constructed. Otherwise it has no detectable effect on the program output. \indexlibrary{\idxcode{syntax_option_type}!\idxcode{optimize}}% |
| % `collate`    | Specifies that character ranges of the form `"[a-b]"` shall be locale sensitive. \indexlibrary{\idxcode{syntax_option_type}!\idxcode{collate}}% \indextext{locale}%                                                                                                                                                                       |
| % `ECMAScript` | Specifies that the grammar recognized by the regular expression engine shall be that used by ECMAScript in ECMA-262, as modified in~ [[re.grammar]]. \indextext{ECMAScript}% \indexlibrary{\idxcode{syntax_option_type}!\idxcode{ECMAScript}}%                                                                                            |
| % `basic`      | Specifies that the grammar recognized by the regular expression engine shall be that used by basic regular expressions in POSIX, Base Definitions and Headers, Section 9, Regular Expressions. \indextext{POSIX!regular expressions}% \indexlibrary{\idxcode{syntax_option_type}!\idxcode{basic}}%                                        |
| % `extended`   | Specifies that the grammar recognized by the regular expression engine shall be that used by extended regular expressions in POSIX, Base Definitions and Headers, Section 9, Regular Expressions. \indextext{POSIX!extended regular expressions}% \indexlibrary{\idxcode{syntax_option_type}!\idxcode{extended}}%                         |
| % `awk`        | Specifies that the grammar recognized by the regular expression engine shall be that used by the utility awk in POSIX. \indextext{\idxcode{awk}}% \indexlibrary{\idxcode{syntax_option_type}!\idxcode{awk}}%                                                                                                                              |
| % `grep`       | Specifies that the grammar recognized by the regular expression engine shall be that used by the utility grep in POSIX. \indextext{\idxcode{grep}}% \indexlibrary{\idxcode{syntax_option_type}!\idxcode{grep}}%                                                                                                                           |
| % `egrep`      | Specifies that the grammar recognized by the regular expression engine shall be that used by the utility grep when given the -E option in POSIX. \indextext{\idxcode{egrep}}% \indexlibrary{\idxcode{syntax_option_type}!\idxcode{egrep}}%                                                                                                |


### Bitmask type `regex_constants::match_flag_type` <a id="re.matchflag">[[re.matchflag]]</a>

``` cpp
namespace std {
  namespace regex_constants{
    typedef T2 match_flag_type;
    constexpr match_flag_type match_default = {};
    constexpr match_flag_type match_not_bol = unspecified;
    constexpr match_flag_type match_not_eol = unspecified;
    constexpr match_flag_type match_not_bow = unspecified;
    constexpr match_flag_type match_not_eow = unspecified;
    constexpr match_flag_type match_any = unspecified;
    constexpr match_flag_type match_not_null = unspecified;
    constexpr match_flag_type match_continuous = unspecified;
    constexpr match_flag_type match_prev_avail = unspecified;
    constexpr match_flag_type format_default = {};
    constexpr match_flag_type format_sed = unspecified;
    constexpr match_flag_type format_no_copy = unspecified;
    constexpr match_flag_type format_first_only = unspecified;
  }
}
```

The type `regex_constants::match_flag_type` is an implementation-defined
bitmask type ([[bitmask.types]]). The constants of that type, except
for `match_default` and `format_default`, are bitmask elements. The
`match_default` and `format_default` constants are empty bitmasks.
Matching a regular expression against a sequence of characters
\[`first`, `last`) proceeds according to the rules of the grammar
specified for the regular expression object, modified according to the
effects listed in Table  [[tab:re:matchflag]] for any bitmask elements
set.

**Table: `regex_constants::match_flag_type` effects when obtaining a match against a
     character container sequence {[}`first`, `last`{)}.** <a id="tab:re:matchflag">[tab:re:matchflag]</a>

| Element                                                           | Effect(s) if set                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| % \indexlibrary{\idxcode{match_not_bol}}% `match_not_bol`         | The first character in the sequence {[}`first`, `last`{)} shall be treated as though it is not at the beginning of a line, so the character \verb|^| in the regular expression shall not match {[}`first`, `first`{)}.                                                                                                                                                                                                                                                      |
| % \indexlibrary{\idxcode{match_not_eol}}% `match_not_eol`         | The last character in the sequence {[}`first`, `last`{)} shall be treated as though it is not at the end of a line, so the character \verb|"$"| in the regular expression shall not match {[}`last`, `last`{)}.                                                                                                                                                                                                                                                             |
| % \indexlibrary{\idxcode{match_not_bow}}% `match_not_bow`         | The expression \verb|"b"| shall not match the sub-sequence {[}`first`, `first`{)}.                                                                                                                                                                                                                                                                                                                                                                                          |
| % \indexlibrary{\idxcode{match_not_eow}}% `match_not_eow`         | The expression \verb|"b"| shall not match the sub-sequence {[}`last`, `last`{)}.                                                                                                                                                                                                                                                                                                                                                                                            |
| % \indexlibrary{\idxcode{match_any}}% `match_any`                 | If more than one match is possible then any match is an acceptable result.                                                                                                                                                                                                                                                                                                                                                                                                  |
| % \indexlibrary{\idxcode{match_not_null}}% `match_not_null`       | The expression shall not match an empty sequence.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| % \indexlibrary{\idxcode{match_continuous}}% `match_continuous`   | The expression shall only match a sub-sequence that begins at `first`.                                                                                                                                                                                                                                                                                                                                                                                                      |
| % \indexlibrary{\idxcode{match_prev_avail}}% `match_prev_avail`   | \verb!--first! is a valid iterator position. When this flag is set the flags match_not_bol and match_not_bow shall be ignored by the regular expression algorithms~ [[re.alg]] and iterators~ [[re.iter]].                                                                                                                                                                                                                                                                  |
| % \indexlibrary{\idxcode{format_default}}% `format_default`       | When a regular expression match is to be replaced by a new string, the new string shall be constructed using the rules used by the ECMAScript replace function in ECMA-262, part 15.5.4.11 String.prototype.replace. In addition, during search and replace operations all non-overlapping occurrences of the regular expression shall be located and replaced, and sections of the input that did not match the expression shall be copied unchanged to the output string. |
| % \indexlibrary{\idxcode{format_sed}}% `format_sed`               | When a regular expression match is to be replaced by a new string, the new string shall be constructed using the rules used by the sed utility in POSIX.                                                                                                                                                                                                                                                                                                                    |
| % \indexlibrary{\idxcode{format_no_copy}}% `format_no_copy`       | During a search and replace operation, sections of the character container sequence being searched that do not match the regular expression shall not be copied to the output string.                                                                                                                                                                                                                                                                                       |
| % \indexlibrary{\idxcode{format_first_only}}% `format_first_only` | When specified during a search and replace operation, only the first occurrence of the regular expression shall be replaced.                                                                                                                                                                                                                                                                                                                                                |


### Implementation-defined `error_type` <a id="re.err">[[re.err]]</a>

``` cpp
namespace std {
  namespace regex_constants {
    typedef T3 error_type;
    constexpr error_type error_collate = unspecified;
    constexpr error_type error_ctype = unspecified;
    constexpr error_type error_escape = unspecified;
    constexpr error_type error_backref = unspecified;
    constexpr error_type error_brack = unspecified;
    constexpr error_type error_paren = unspecified;
    constexpr error_type error_brace = unspecified;
    constexpr error_type error_badbrace = unspecified;
    constexpr error_type error_range = unspecified;
    constexpr error_type error_space = unspecified;
    constexpr error_type error_badrepeat = unspecified;
    constexpr error_type error_complexity = unspecified;
    constexpr error_type error_stack = unspecified;
  }
}
```

The type `error_type` is an *implementation-defined* enumerated type (
[[enumerated.types]]). Values of type `error_type` represent the error
conditions described in Table  [[tab:re:errortype]]:

**Table: `error_type` values in the C locale** <a id="tab:re:errortype">[tab:re:errortype]</a>

| Value                | Error condition                                                                                                         |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `error_collate`      | The expression contained an invalid collating element name.                                                             |
| % `error_ctype`      | The expression contained an invalid character class name.                                                               |
| % `error_escape`     | The expression contained an invalid escaped character, or a trailing escape.                                            |
| % `error_backref`    | The expression contained an invalid back reference.                                                                     |
| % `error_brack`      | The expression contained mismatched \verb|[| and \verb|]|.                                                              |
| % `error_paren`      | The expression contained mismatched \verb|(| and \verb|)|.                                                              |
| % `error_brace`      | The expression contained mismatched \verb|{| and \verb|}|                                                               |
| % `error_badbrace`   | The expression contained an invalid range in a \verb|{}| expression.                                                    |
| % `error_range`      | The expression contained an invalid character range, such as \verb|[b-a]| in most encodings.                            |
| % `error_space`      | There was insufficient memory to convert the expression into a finite state machine.                                    |
| % `error_badrepeat`  | One of \verb|*?+{| was not preceded by a valid regular expression.                                                      |
| % `error_complexity` | The complexity of an attempted match against a regular expression exceeded a pre-set level.                             |
| % `error_stack`      | There was insufficient memory to determine whether the regular expression could match the specified character sequence. |


## Class `regex_error` <a id="re.badexp">[[re.badexp]]</a>

``` cpp
class regex_error : public std::runtime_error {
  public:
    explicit regex_error(regex_constants::error_type ecode);
    regex_constants::error_type code() const;
};
```

The class `regex_error` defines the type of objects thrown as exceptions
to report errors from the regular expression library.

``` cpp
regex_error(regex_constants::error_type ecode);
```

*Effects:* Constructs an object of class `regex_error`.

: `ecode == code()`

``` cpp
regex_constants::error_type code() const;
```

*Returns:* The error code that was passed to the constructor.

## Class template `regex_traits` <a id="re.traits">[[re.traits]]</a>

``` cpp
namespace std {
  template <class charT>
  struct regex_traits {
  public:
     typedef charT                        char_type;
     typedef std::basic_string<char_type> string_type;
     typedef std::locale                  locale_type;
     typedef {bitmask_type}                 char_class_type;

     regex_traits();
     static std::size_t length(const char_type* p);
     charT translate(charT c) const;
     charT translate_nocase(charT c) const;
     template <class ForwardIterator>
       string_type transform(ForwardIterator first, ForwardIterator last) const;
     template <class ForwardIterator>
       string_type transform_primary(
         ForwardIterator first, ForwardIterator last) const;
     template <class ForwardIterator>
       string_type lookup_collatename(
         ForwardIterator first, ForwardIterator last) const;
     template <class ForwardIterator>
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
shall be valid and shall satisfy the requirements for a regular
expression traits class ([[re.req]]).

``` cpp
typedef bitmask_type                 char_class_type;
```

The type `char_class_type` is used to represent a character
classification and is capable of holding an implementation specific set
returned by `lookup_classname`.

``` cpp
static std::size_t length(const char_type* p);
```

*Returns:* `char_traits<charT>::length(p);`

``` cpp
charT translate(charT c) const;
```

*Returns:* `(c)`.

``` cpp
charT translate_nocase(charT c) const;
```

*Returns:* `use_facet<ctype<charT> >(getloc()).tolower(c)`.

``` cpp
template <class ForwardIterator>
  string_type transform(ForwardIterator first, ForwardIterator last) const;
```

*Effects:*

``` cpp
string_type str(first, last);
return use_facet<collate<charT> >(
  getloc()).transform(&*str.begin(), &*str.begin() + str.length());
```

``` cpp
template <class ForwardIterator>
  string_type transform_primary(ForwardIterator first, ForwardIterator last) const;
```

*Effects:* if
`typeid(use_facet<collate<charT> >) == typeid(collate_byname<charT>)`
and the form of the sort key returned by
`collate_byname<charT> ``transform(first, last)` is known and can be
converted into a primary sort key then returns that key, otherwise
returns an empty string.

``` cpp
template <class ForwardIterator>
  string_type lookup_collatename(ForwardIterator first, ForwardIterator last) const;
```

*Returns:* a sequence of one or more characters that represents the
collating element consisting of the character sequence designated by the
iterator range \[`first`, `last`). Returns an empty string if the
character sequence is not a valid collating element.

``` cpp
template <class ForwardIterator>
  char_class_type lookup_classname(
    ForwardIterator first, ForwardIterator last, bool icase = false) const;
```

*Returns:* an unspecified value that represents the character
classification named by the character sequence designated by the
iterator range \[`first`, `last`). If the parameter `icase` is true then
the returned mask identifies the character classification without regard
to the case of the characters being matched, otherwise it does honor the
case of the characters being matched.[^1] The value returned shall be
independent of the case of the characters in the character sequence. If
the name is not recognized then returns `char_class_type()`.

*Remarks:* For `regex_traits<char>`, at least the narrow character names
in Table  [[tab:re.traits.classnames]] shall be recognized. For
`regex_traits<wchar_t>`, at least the wide character names in
Table  [[tab:re.traits.classnames]] shall be recognized.

``` cpp
bool isctype(charT c, char_class_type f) const;
```

*Effects:* Determines if the character `c` is a member of the character
classification represented by `f`.

*Returns:* Given the following function prototype:

``` cpp
// for exposition only
template<class C>
  ctype_base::mask convert(typename regex_traits<C>::char_class_type f);
```

that returns a value in which each `ctype_base::mask` value
corresponding to a value in `f` named in
Table  [[tab:re.traits.classnames]] is set, then the result is
determined as if by:

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

``` cpp
regex_traits<char> t;
string d("d");
string u("upper");
regex_traits<char>::char_class_type f;
f = t.lookup_classname(d.begin(), d.end());
f |= t.lookup_classname(u.begin(), u.end());
ctype_base::mask m = convert<char>(f); // m == ctype_base::digit|ctype_base::upper
```

``` cpp
regex_traits<char> t;
string w("w");
regex_traits<char>::char_class_type f;
f = t.lookup_classname(w.begin(), w.end());
t.isctype('A', f); // returns true
t.isctype('_', f); // returns true
t.isctype(' ', f); // returns false
```

``` cpp
int value(charT ch, int radix) const;
```

The value of *radix* shall be 8, 10, or 16.

*Returns:* the value represented by the digit *ch* in base *radix* if
the character *ch* is a valid digit in base *radix*; otherwise returns
-1.

``` cpp
locale_type imbue(locale_type loc);
```

*Effects:* Imbues `this` with a copy of the locale `loc`. Calling
`imbue` with a different locale than the one currently in use
invalidates all cached data held by `*this`.

*Returns:* if no locale has been previously imbued then a copy of the
global locale in effect at the time of construction of `*this`,
otherwise a copy of the last argument passed to `imbue`.

`getloc() == loc`.

``` cpp
locale_type getloc() const;
```

*Returns:* if no locale has been imbued then a copy of the global locale
in effect at the time of construction of `*this`, otherwise a copy of
the last argument passed to `imbue`.

**Table: Character class names and corresponding `ctype` masks** <a id="tab:re.traits.classnames">[tab:re.traits.classnames]</a>

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


## Class template `basic_regex` <a id="re.regex">[[re.regex]]</a>

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
expressions. Implementations will typically declare some function
templates as friends of `basic_regex` to achieve this

The functions described in this Clause report errors by throwing
exceptions of type `regex_error`.

``` cpp
namespace std {
  template <class charT,
            class traits = regex_traits<charT> >
  class basic_regex {
  public:
    // types:
    typedef          charT                                value_type;
    typedef          traits                               traits_type;
    typedef typename traits::string_type                  string_type;
    typedef          regex_constants::syntax_option_type  flag_type;
    typedef typename traits::locale_type                  locale_type;

    // [re.regex.const], constants:
    static constexpr regex_constants::syntax_option_type
      icase = regex_constants::icase;
    static constexpr regex_constants::syntax_option_type
      nosubs = regex_constants::nosubs;
    static constexpr regex_constants::syntax_option_type
      optimize = regex_constants::optimize;
    static constexpr regex_constants::syntax_option_type
      collate = regex_constants::collate;
    static constexpr regex_constants::syntax_option_type
      ECMAScript = regex_constants::ECMAScript;
    static constexpr regex_constants::syntax_option_type
      basic = regex_constants::basic;
    static constexpr regex_constants::syntax_option_type
      extended = regex_constants::extended;
    static constexpr regex_constants::syntax_option_type
      awk = regex_constants::awk;
    static constexpr regex_constants::syntax_option_type
      grep = regex_constants::grep;
    static constexpr regex_constants::syntax_option_type
      egrep = regex_constants::egrep;

    // [re.regex.construct], construct/copy/destroy:
    basic_regex();
    explicit basic_regex(const charT* p,
      flag_type f = regex_constants::ECMAScript);
    basic_regex(const charT* p, size_t len, flag_type f = regex_constants::ECMAScript);
    basic_regex(const basic_regex&);
    basic_regex(basic_regex&&) noexcept;
    template <class ST, class SA>
      explicit basic_regex(const basic_string<charT, ST, SA>& p,
                           flag_type f = regex_constants::ECMAScript);
    template <class ForwardIterator>
      basic_regex(ForwardIterator first, ForwardIterator last,
                  flag_type f = regex_constants::ECMAScript);
    basic_regex(initializer_list<charT>,
      flag_type = regex_constants::ECMAScript);

    ~basic_regex();

    basic_regex& operator=(const basic_regex&);
    basic_regex& operator=(basic_regex&&) noexcept;
    basic_regex& operator=(const charT* ptr);
    basic_regex& operator=(initializer_list<charT> il);
    template <class ST, class SA>
      basic_regex& operator=(const basic_string<charT, ST, SA>& p);

    // [re.regex.assign], assign:
    basic_regex& assign(const basic_regex& that);
    basic_regex& assign(basic_regex&& that) noexcept;
    basic_regex& assign(const charT* ptr,
      flag_type f = regex_constants::ECMAScript);
    basic_regex& assign(const charT* p, size_t len, flag_type f);
    template <class string_traits, class A>
      basic_regex& assign(const basic_string<charT, string_traits, A>& s,
                          flag_type f = regex_constants::ECMAScript);
    template <class InputIterator>
      basic_regex& assign(InputIterator first, InputIterator last,
                          flag_type f = regex_constants::ECMAScript);
    basic_regex& assign(initializer_list<charT>,
                        flag_type = regex_constants::ECMAScript);

    // [re.regex.operations], const operations:
    unsigned mark_count() const;
    flag_type flags() const;

    // [re.regex.locale], locale:
    locale_type imbue(locale_type loc);
    locale_type getloc() const;

    // [re.regex.swap], swap:
    void swap(basic_regex&);
  };
}
```

### `basic_regex` constants <a id="re.regex.const">[[re.regex.const]]</a>

``` cpp
static constexpr regex_constants::syntax_option_type
  icase = regex_constants::icase;
static constexpr regex_constants::syntax_option_type
  nosubs = regex_constants::nosubs;
static constexpr regex_constants::syntax_option_type
  optimize = regex_constants::optimize;
static constexpr regex_constants::syntax_option_type
  collate = regex_constants::collate;
static constexpr regex_constants::syntax_option_type
  ECMAScript = regex_constants::ECMAScript;
static constexpr regex_constants::syntax_option_type
  basic = regex_constants::basic;
static constexpr regex_constants::syntax_option_type
  extended = regex_constants::extended;
static constexpr regex_constants::syntax_option_type
  awk = regex_constants::awk;
static constexpr regex_constants::syntax_option_type
  grep = regex_constants::grep;
static constexpr regex_constants::syntax_option_type
  egrep = regex_constants::egrep;
```

The static constant members are provided as synonyms for the constants
declared in namespace `regex_constants`.

### `basic_regex` constructors <a id="re.regex.construct">[[re.regex.construct]]</a>

``` cpp
basic_regex();
```

*Effects:* Constructs an object of class `basic_regex` that does not
match any character sequence.

``` cpp
explicit basic_regex(const charT* p, flag_type f = regex_constants::ECMAScript);
```

*Requires:* *p* shall not be a null pointer.

*Throws:* `regex_error` if *p* is not a valid regular expression.

*Effects:* Constructs an object of class `basic_regex`; the object’s
internal finite state machine is constructed from the regular expression
contained in the array of `charT` of length
`char_traits<charT>::length(p)` whose first element is designated by
*p*, and interpreted according to the flags *f*.

*Postconditions:* `flags()` returns `f`. `mark_count()` returns the
number of marked sub-expressions within the expression.

``` cpp
basic_regex(const charT* p, size_t len, flag_type f);
```

*Requires:* *p* shall not be a null pointer.

*Throws:* `regex_error` if *p* is not a valid regular expression.

*Effects:* Constructs an object of class `basic_regex`; the object’s
internal finite state machine is constructed from the regular expression
contained in the sequence of characters \[`p`, `p+len`), and interpreted
according the flags specified in *f*.

*Postconditions:* `flags()` returns `f`. `mark_count()` returns the
number of marked sub-expressions within the expression.

``` cpp
basic_regex(const basic_regex& e);
```

*Effects:* Constructs an object of class `basic_regex` as a copy of the
object `e`.

*Postconditions:* `flags()` and `mark_count()` return `e.flags()` and
`e.mark_count()`, respectively.

``` cpp
basic_regex(basic_regex&& e) noexcept;
```

*Effects:* Move constructs an object of class `basic_regex` from `e`.

*Postconditions:* `flags()` and `mark_count()` return the values that
`e.flags()` and `e.mark_count()`, respectively, had before construction.
`e` is in a valid state with unspecified value.

``` cpp
template <class ST, class SA>
  explicit basic_regex(const basic_string<charT, ST, SA>& s,
                       flag_type f = regex_constants::ECMAScript);
```

*Throws:* `regex_error` if `s` is not a valid regular expression.

*Effects:* Constructs an object of class `basic_regex`; the object’s
internal finite state machine is constructed from the regular expression
contained in the string `s`, and interpreted according to the flags
specified in `f`.

*Postconditions:* `flags()` returns `f`. `mark_count()` returns the
number of marked sub-expressions within the expression.

``` cpp
template <class ForwardIterator>
  basic_regex(ForwardIterator first, ForwardIterator last,
              flag_type f = regex_constants::ECMAScript);
```

*Throws:* `regex_error` if the sequence \[`first`, `last`) is not a
valid regular expression.

*Effects:* Constructs an object of class `basic_regex`; the object’s
internal finite state machine is constructed from the regular expression
contained in the sequence of characters \[`first`, `last`), and
interpreted according to the flags specified in `f`.

*Postconditions:* `flags()` returns `f`. `mark_count()` returns the
number of marked sub-expressions within the expression.

``` cpp
basic_regex(initializer_list<charT> il,
            flag_type f = regex_constants::ECMAScript);
```

*Effects:* Same as `basic_regex(il.begin(), il.end(), f)`.

### `basic_regex` assign <a id="re.regex.assign">[[re.regex.assign]]</a>

``` cpp
basic_regex& operator=(const basic_regex& e);
```

*Effects:* returns `assign(e)`.

``` cpp
basic_regex& operator=(basic_regex&& e) noexcept;
```

*Effects:* returns `assign(std::move(e))`.

``` cpp
basic_regex& operator=(const charT* ptr);
```

*Requires:* `ptr` shall not be a null pointer.

*Effects:* returns `assign(ptr)`.

``` cpp
basic_regex& operator=(initializer_list<charT> il);
```

*Effects:* returns `assign(il.begin(), il.end())`.

``` cpp
template <class ST, class SA>
  basic_regex& operator=(const basic_string<charT, ST, SA>& p);
```

*Effects:* returns `assign(p)`.

``` cpp
basic_regex& assign(const basic_regex& that);
```

*Effects:* copies `that` into `*this` and returns `*this`.

*Postconditions:* `flags()` and `mark_count()` return `that.flags()` and
`that.mark_count()`, respectively.

``` cpp
basic_regex& assign(basic_regex&& that) noexcept;
```

*Effects:* move assigns from `that` into `*this` and returns `*this`.

*Postconditions:* `flags()` and `mark_count()` return the values that
`that.flags()` and `that.mark_count()`, respectively, had before
assignment. `that` is in a valid state with unspecified value.

``` cpp
basic_regex& assign(const charT* ptr, flag_type f = regex_constants::ECMAScript);
```

*Returns:* `assign(string_type(ptr), f)`.

``` cpp
basic_regex& assign(const charT* ptr, size_t len,
  flag_type f = regex_constants::ECMAScript);
```

*Returns:* `assign(string_type(ptr, len), f)`.

``` cpp
template <class string_traits, class A>
  basic_regex& assign(const basic_string<charT, string_traits, A>& s,
                      flag_type f = regex_constants::ECMAScript);
```

*Throws:* `regex_error` if `s` is not a valid regular expression.

*Returns:* `*this`.

*Effects:* Assigns the regular expression contained in the string `s`,
interpreted according the flags specified in `f`. If an exception is
thrown, `*this` is unchanged.

*Postconditions:* If no exception is thrown, `flags()` returns `f` and
`mark_count()` returns the number of marked sub-expressions within the
expression.

``` cpp
template <class InputIterator>
  basic_regex& assign(InputIterator first, InputIterator last,
                      flag_type f = regex_constants::ECMAScript);
```

*Requires:* The type `InputIterator` shall satisfy the requirements for
an Input Iterator ([[input.iterators]]).

*Returns:* `assign(string_type(first, last), f)`.

``` cpp
basic_regex& assign(initializer_list<charT> il,
                    flag_type f = regex_constants::ECMAScript);
```

*Effects:* Same as `assign(il.begin(), il.end(), f)`.

*Returns:* `*this`.

### `basic_regex` constant operations <a id="re.regex.operations">[[re.regex.operations]]</a>

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

### `basic_regex` locale <a id="re.regex.locale">[[re.regex.locale]]</a>

``` cpp
locale_type imbue(locale_type loc);
```

*Effects:* Returns the result of `traits_inst.imbue(loc)` where
`traits_inst` is a (default initialized) instance of the template type
argument `traits` stored within the object. After a call to `imbue` the
`basic_regex` object does not match any character sequence.

``` cpp
locale_type getloc() const;
```

*Effects:* Returns the result of `traits_inst.getloc()` where
`traits_inst` is a (default initialized) instance of the template
parameter `traits` stored within the object.

### `basic_regex` swap <a id="re.regex.swap">[[re.regex.swap]]</a>

``` cpp
void swap(basic_regex& e);
```

*Effects:* Swaps the contents of the two regular expressions.

`*this` contains the regular expression that was in `e`, `e` contains
the regular expression that was in `*this`.

*Complexity:* Constant time.

### `basic_regex` non-member functions <a id="re.regex.nonmemb">[[re.regex.nonmemb]]</a>

#### `basic_regex` non-member swap <a id="re.regex.nmswap">[[re.regex.nmswap]]</a>

``` cpp
template <class charT, class traits>
  void swap(basic_regex<charT, traits>& lhs, basic_regex<charT, traits>& rhs);
```

*Effects:* Calls `lhs.swap(rhs)`.

## Class template `sub_match` <a id="re.submatch">[[re.submatch]]</a>

Class template `sub_match` denotes the sequence of characters matched by
a particular marked sub-expression.

``` cpp
namespace std {
  template <class BidirectionalIterator>
  class sub_match : public std::pair<BidirectionalIterator, BidirectionalIterator> {
  public:
     typedef typename iterator_traits<BidirectionalIterator>::
       value_type                                               value_type;
     typedef typename iterator_traits<BidirectionalIterator>::
       difference_type                                          difference_type;
     typedef BidirectionalIterator                              iterator;
     typedef basic_string<value_type>                           string_type;

     bool matched;

     constexpr sub_match();

     difference_type length() const;
     operator string_type() const;
     string_type str() const;

     int compare(const sub_match& s) const;
     int compare(const string_type& s) const;
     int compare(const value_type* s) const;
  };
}
```

### `sub_match` members <a id="re.submatch.members">[[re.submatch.members]]</a>

``` cpp
constexpr sub_match();
```

*Effects:* Value-initializes the `pair` base class subobject and the
member `matched`.

``` cpp
difference_type length() const;
```

*Returns:* `(matched ? distance(first, second) : 0)`.

``` cpp
operator string_type() const;
```

*Returns:* `matched ? string_type(first, second) : string_type()`.

``` cpp
string_type str() const;
```

*Returns:* `matched ? string_type(first, second) : string_type()`.

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

### `sub_match` non-member operators <a id="re.submatch.op">[[re.submatch.op]]</a>

``` cpp
template <class BiIter>
  bool operator==(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template <class BiIter>
  bool operator!=(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) != 0`.

``` cpp
template <class BiIter>
  bool operator<(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) < 0`.

``` cpp
template <class BiIter>
  bool operator<=(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) <= 0`.

``` cpp
template <class BiIter>
  bool operator>=(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) >= 0`.

``` cpp
template <class BiIter>
  bool operator>(const sub_match<BiIter>& lhs, const sub_match<BiIter>& rhs);
```

*Returns:* `lhs.compare(rhs) > 0`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator==(
    const basic_string<
      typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
    const sub_match<BiIter>& rhs);
```

*Returns:* `rhs.compare(lhs.c_str()) == 0`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator!=(
    const basic_string<
      typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
    const sub_match<BiIter>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator<(
    const basic_string<
      typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
    const sub_match<BiIter>& rhs);
```

*Returns:* `rhs.compare(lhs.c_str()) > 0`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator>(
    const basic_string<
      typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
    const sub_match<BiIter>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator>=(
    const basic_string<
      typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
    const sub_match<BiIter>& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator<=(
    const basic_string<
      typename iterator_traits<BiIter>::value_type, ST, SA>& lhs,
    const sub_match<BiIter>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator==(const sub_match<BiIter>& lhs,
                  const basic_string<
                    typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:* `lhs.compare(rhs.c_str()) == 0`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator!=(const sub_match<BiIter>& lhs,
                  const basic_string<
                    typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator<(const sub_match<BiIter>& lhs,
                 const basic_string<
                   typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:* `lhs.compare(rhs.c_str()) < 0`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator>(const sub_match<BiIter>& lhs,
                 const basic_string<
                   typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator>=(const sub_match<BiIter>& lhs,
                  const basic_string<
                    typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template <class BiIter, class ST, class SA>
  bool operator<=(const sub_match<BiIter>& lhs,
                  const basic_string<
                    typename iterator_traits<BiIter>::value_type, ST, SA>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class BiIter>
  bool operator==(typename iterator_traits<BiIter>::value_type const* lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `rhs.compare(lhs) == 0`.

``` cpp
template <class BiIter>
  bool operator!=(typename iterator_traits<BiIter>::value_type const* lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class BiIter>
  bool operator<(typename iterator_traits<BiIter>::value_type const* lhs,
                 const sub_match<BiIter>& rhs);
```

*Returns:* `rhs.compare(lhs) > 0`.

``` cpp
template <class BiIter>
  bool operator>(typename iterator_traits<BiIter>::value_type const* lhs,
                 const sub_match<BiIter>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class BiIter>
  bool operator>=(typename iterator_traits<BiIter>::value_type const* lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template <class BiIter>
  bool operator<=(typename iterator_traits<BiIter>::value_type const* lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class BiIter>
  bool operator==(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const* rhs);
```

*Returns:* `lhs.compare(rhs) == 0`.

``` cpp
template <class BiIter>
  bool operator!=(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const* rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class BiIter>
  bool operator<(const sub_match<BiIter>& lhs,
                 typename iterator_traits<BiIter>::value_type const* rhs);
```

*Returns:* `lhs.compare(rhs) < 0`.

``` cpp
template <class BiIter>
  bool operator>(const sub_match<BiIter>& lhs,
                 typename iterator_traits<BiIter>::value_type const* rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class BiIter>
  bool operator>=(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const* rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template <class BiIter>
  bool operator<=(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const* rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class BiIter>
  bool operator==(typename iterator_traits<BiIter>::value_type const& lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:*
`rhs.compare(typename sub_match<BiIter>::string_type(1, lhs)) == 0`.

``` cpp
template <class BiIter>
  bool operator!=(typename iterator_traits<BiIter>::value_type const& lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class BiIter>
  bool operator<(typename iterator_traits<BiIter>::value_type const& lhs,
                 const sub_match<BiIter>& rhs);
```

*Returns:*
`rhs.compare(typename sub_match<BiIter>::string_type(1, lhs)) > 0`.

``` cpp
template <class BiIter>
  bool operator>(typename iterator_traits<BiIter>::value_type const& lhs,
                 const sub_match<BiIter>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class BiIter>
  bool operator>=(typename iterator_traits<BiIter>::value_type const& lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template <class BiIter>
  bool operator<=(typename iterator_traits<BiIter>::value_type const& lhs,
                  const sub_match<BiIter>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class BiIter>
  bool operator==(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const& rhs);
```

*Returns:*
`lhs.compare(typename sub_match<BiIter>::string_type(1, rhs)) == 0`.

``` cpp
template <class BiIter>
  bool operator!=(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class BiIter>
  bool operator<(const sub_match<BiIter>& lhs,
                 typename iterator_traits<BiIter>::value_type const& rhs);
```

*Returns:*
`lhs.compare(typename sub_match<BiIter>::string_type(1, rhs)) < 0`.

``` cpp
template <class BiIter>
  bool operator>(const sub_match<BiIter>& lhs,
                 typename iterator_traits<BiIter>::value_type const& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class BiIter>
  bool operator>=(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template <class BiIter>
  bool operator<=(const sub_match<BiIter>& lhs,
                  typename iterator_traits<BiIter>::value_type const& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class charT, class ST, class BiIter>
  basic_ostream<charT, ST>&
  operator<<(basic_ostream<charT, ST>& os, const sub_match<BiIter>& m);
```

*Returns:* `(os << m.str())`.

## Class template `match_results` <a id="re.results">[[re.results]]</a>

Class template `match_results` denotes a collection of character
sequences representing the result of a regular expression match. Storage
for the collection is allocated and freed as necessary by the member
functions of class template `match_results`.

The class template `match_results` shall satisfy the requirements of an
allocator-aware container and of a sequence container, as specified in 
[[sequence.reqmts]], except that only operations defined for
const-qualified sequence containers are supported.

A default-constructed `match_results` object has no fully established
result state. A match result is *ready* when, as a consequence of a
completed regular expression match modifying such an object, its result
state becomes fully established. The effects of calling most member
functions from a `match_results` object that is not ready are undefined.

The `sub_match` object stored at index 0 represents sub-expression 0,
i.e., the whole match. In this case the `sub_match` member `matched` is
always true. The `sub_match` object stored at index `n` denotes what
matched the marked sub-expression `n` within the matched expression. If
the sub-expression `n` participated in a regular expression match then
the `sub_match` member `matched` evaluates to true, and members `first`
and `second` denote the range of characters \[`first`, `second`) which
formed that match. Otherwise `matched` is false, and members `first` and
`second` point to the end of the sequence that was searched. The
`sub_match` objects representing different sub-expressions that did not
participate in a regular expression match need not be distinct.

``` cpp
namespace std {
  template <class BidirectionalIterator,
            class Allocator = allocator<sub_match<BidirectionalIterator>>>
  class match_results {
  public:
     typedef sub_match<BidirectionalIterator>                       value_type;
     typedef const value_type&                                      const_reference;
     typedef value_type&                                            reference;
     typedef {implementation-defined}                                 const_iterator;
     typedef const_iterator                                         iterator;
     typedef typename
      iterator_traits<BidirectionalIterator>::difference_type       difference_type;
     typedef typename allocator_traits<Allocator>::size_type        size_type;
     typedef Allocator                                              allocator_type;
     typedef typename iterator_traits<BidirectionalIterator>::
       value_type                                                   char_type;
     typedef basic_string<char_type>                                string_type;

     // [re.results.const], construct/copy/destroy:
     explicit match_results(const Allocator& a = Allocator());
     match_results(const match_results& m);
     match_results(match_results&& m) noexcept;
     match_results& operator=(const match_results& m);
     match_results& operator=(match_results&& m);
     ~match_results();

     // [re.results.state], state:
     bool ready() const;

     // [re.results.size], size:
     size_type size() const;
     size_type max_size() const;
     bool empty() const;

     // [re.results.acc], element access:
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

     // [re.results.form], format:
     template <class OutputIter>
      OutputIter
      format(OutputIter out,
             const char_type* fmt_first, const char_type* fmt_last,
             regex_constants::match_flag_type flags =
              regex_constants::format_default) const;
     template <class OutputIter, class ST, class SA>
       OutputIter
       format(OutputIter out,
              const basic_string<char_type, ST, SA>& fmt,
              regex_constants::match_flag_type flags =
                regex_constants::format_default) const;
     template <class ST, class SA>
      basic_string<char_type, ST, SA>
      format(const basic_string<char_type, ST, SA>& fmt,
             regex_constants::match_flag_type flags =
               regex_constants::format_default) const;
     string_type
     format(const char_type* fmt,
            regex_constants::match_flag_type flags =
              regex_constants::format_default) const;

     // [re.results.all], allocator:
     allocator_type get_allocator() const;

     // [re.results.swap], swap:
     void swap(match_results& that);
  };
}
```

### `match_results` constructors <a id="re.results.const">[[re.results.const]]</a>

In all `match_results` constructors, a copy of the `Allocator` argument
shall be used for any memory allocation performed by the constructor or
member functions during the lifetime of the object.

``` cpp
match_results(const Allocator& a = Allocator());
```

*Effects:* Constructs an object of class `match_results`.

*Postconditions:* `ready()` returns `false`. `size()` returns `0`.

``` cpp
match_results(const match_results& m);
```

*Effects:* Constructs an object of class `match_results`, as a copy of
`m`.

``` cpp
match_results(match_results&& m) noexcept;
```

*Effects:*  Move-constructs an object of class `match_results` from `m`
satisfying the same postconditions as Table  [[tab:re:results:assign]].
Additionally, the stored `Allocator` value is move constructed from
`m.get_allocator()`.

*Throws:* Nothing.

``` cpp
match_results& operator=(const match_results& m);
```

*Effects:* Assigns `m` to `*this`. The postconditions of this function
are indicated in Table  [[tab:re:results:assign]].

``` cpp
match_results& operator=(match_results&& m);
```

*Effects:*  Move-assigns `m` to `*this`. The postconditions of this
function are indicated in Table  [[tab:re:results:assign]].

**Table: `match_results` assignment operator effects** <a id="tab:re:results:assign">[tab:re:results:assign]</a>

| Element       | Value                                           |
| ------------- | ----------------------------------------------- |
| `ready()`     | `m.ready()`                                     |
| `size()`      | `m.size()`                                      |
| `str(n)`      | `m.str(n)` for all integers `n < m.size()`      |
| `prefix()`    | `m.prefix()`                                    |
| `suffix()`    | `m.suffix()`                                    |
| `(*this)[n]`  | `m[n]` for all integers `n < m.size()`          |
| `length(n)`   | `m.length(n)` for all integers `n < m.size()`   |
| `position(n)` | `m.position(n)` for all integers `n < m.size()` |


### `match_results` state <a id="re.results.state">[[re.results.state]]</a>

``` cpp
bool ready() const;
```

*Returns:* `true` if `*this` has a fully established result state,
otherwise `false`.

### `match_results` size <a id="re.results.size">[[re.results.size]]</a>

``` cpp
size_type size() const;
```

*Returns:* One plus the number of marked sub-expressions in the regular
expression that was matched if `*this` represents the result of a
successful match. Otherwise returns `0`. The state of a `match_results`
object can be modified only by passing that object to `regex_match` or
`regex_search`. Sections  [[re.alg.match]] and  [[re.alg.search]]
specify the effects of those algorithms on their `match_results`
arguments.

``` cpp
size_type max_size() const;
```

*Returns:* The maximum number of `sub_match` elements that can be stored
in `*this`.

``` cpp
bool empty() const;
```

*Returns:* `size() == 0`.

### `match_results` element access <a id="re.results.acc">[[re.results.acc]]</a>

``` cpp
difference_type length(size_type sub = 0) const;
```

*Requires:* `ready() == true`.

*Returns:* `(*this)[sub].length()`.

``` cpp
difference_type position(size_type sub = 0) const;
```

*Requires:* `ready() == true`.

*Returns:* The distance from the start of the target sequence to
`(*this)[sub].first`.

``` cpp
string_type str(size_type sub = 0) const;
```

*Requires:* `ready() == true`.

*Returns:* `string_type((*this)[sub])`.

``` cpp
const_reference operator[](size_type n) const;
```

*Requires:* `ready() == true`.

*Returns:* A reference to the `sub_match` object representing the
character sequence that matched marked sub-expression `n`. If `n == 0`
then returns a reference to a `sub_match` object representing the
character sequence that matched the whole regular expression. If
`n >= size()` then returns a `sub_match` object representing an
unmatched sub-expression.

``` cpp
const_reference prefix() const;
```

*Requires:* `ready() == true`.

*Returns:* A reference to the `sub_match` object representing the
character sequence from the start of the string being matched/searched
to the start of the match found.

``` cpp
const_reference suffix() const;
```

*Requires:* `ready() == true`.

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

### `match_results` formatting <a id="re.results.form">[[re.results.form]]</a>

``` cpp
template <class OutputIter>
  OutputIter format(OutputIter out,
                    const char_type* fmt_first, const char_type* fmt_last,
                    regex_constants::match_flag_type flags =
                      regex_constants::format_default) const;
```

*Requires:*  ready() == true and `OutputIter` shall satisfy the
requirements for an Output Iterator ([[output.iterators]]).

*Effects:* Copies the character sequence \[`fmt_first`, `fmt_last`) to
OutputIter `out`. Replaces each format specifier or escape sequence in
the copied range with either the character(s) it represents or the
sequence of characters within `*this` to which it refers. The bitmasks
specified in `flags` determine which format specifiers and escape
sequences are recognized.

*Returns:*  `out`.

``` cpp
template <class OutputIter, class ST, class SA>
  OutputIter format(OutputIter out,
                    const basic_string<char_type, ST, SA>& fmt,
                    regex_constants::match_flag_type flags =
                      regex_constants::format_default) const;
```

*Effects:* Equivalent to `return format(out, fmt.data(),`
`fmt.data() + fmt.size(), flags)`.

``` cpp
template <class ST, class SA>
  basic_string<char_type, ST, SA>
  format(const basic_string<char_type, ST, SA>& fmt,
         regex_constants::match_flag_type flags =
           regex_constants::format_default) const;
```

*Requires:* `ready() == true`.

*Effects:* Constructs an empty string `result` of type
`basic_string<char_type, ST, SA>` and calls
`format(back_inserter(result), fmt, flags)`.

*Returns:*  `result`.

``` cpp
string_type
  format(const char_type* fmt,
         regex_constants::match_flag_type flags =
           regex_constants::format_default) const;
```

*Requires:* `ready() == true`.

*Effects:*  Constructs an empty string `result` of type `string_type`
and
calls`format(back_inserter(result), fmt, fmt + char_traits<char_type>::length(fmt), flags)`.

*Returns:*  `result`.

### `match_results` allocator <a id="re.results.all">[[re.results.all]]</a>

``` cpp
allocator_type get_allocator() const;
```

*Returns:* A copy of the Allocator that was passed to the object’s
constructor or, if that allocator has been replaced, a copy of the most
recent replacement.

### `match_results` swap <a id="re.results.swap">[[re.results.swap]]</a>

``` cpp
void swap(match_results& that);
```

*Effects:* Swaps the contents of the two sequences.

`*this` contains the sequence of matched sub-expressions that were in
`that`, `that` contains the sequence of matched sub-expressions that
were in `*this`.

*Complexity:* Constant time.

``` cpp
template <class BidirectionalIterator, class Allocator>
  void swap(match_results<BidirectionalIterator, Allocator>& m1,
            match_results<BidirectionalIterator, Allocator>& m2);
```

*Effects:* `m1.swap(m2)`.

### `match_results` non-member functions <a id="re.results.nonmember">[[re.results.nonmember]]</a>

``` cpp
template <class BidirectionalIterator, class Allocator>
bool operator==(const match_results<BidirectionalIterator, Allocator>& m1,
                const match_results<BidirectionalIterator, Allocator>& m2);
```

*Returns:* `true` if neither match result is ready, `false` if one match
result is ready and the other is not. If both match results are ready,
returns `true` only if:

- `m1.empty() && m2.empty()`, or
- `!m1.empty() && !m2.empty()`, and the following conditions are
  satisfied:
  - `m1.prefix() == m2.prefix()`,
  - `m1.size() == m2.size() && equal(m1.begin(), m1.end(), m2.begin())`,
    and
  - `m1.suffix() == m2.suffix()`.

The algorithm `equal` is defined in Clause  [[algorithms]].

``` cpp
template <class BidirectionalIterator, class Allocator>
bool operator!=(const match_results<BidirectionalIterator, Allocator>& m1,
                const match_results<BidirectionalIterator, Allocator>& m2);
```

*Returns:* `!(m1 == m2)`.

## Regular expression algorithms <a id="re.alg">[[re.alg]]</a>

### exceptions <a id="re.except">[[re.except]]</a>

The algorithms described in this subclause may throw an exception of
type `regex_error`. If such an exception `e` is thrown, `e.code()` shall
return either `regex_constants::error_complexity` or
`regex_constants::error_stack`.

### `regex_match` <a id="re.alg.match">[[re.alg.match]]</a>

``` cpp
template <class BidirectionalIterator, class Allocator, class charT, class traits>
  bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                   match_results<BidirectionalIterator, Allocator>& m,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
```

*Requires:* The type `BidirectionalIterator` shall satisfy the
requirements of a Bidirectional Iterator
 ([[bidirectional.iterators]]).

*Effects:* Determines whether there is a match between the regular
expression `e`, and all of the character sequence \[`first`, `last`).
The parameter `flags` is used to control how the expression is matched
against the character sequence. Returns `true` if such a match exists,
`false` otherwise.

*Postconditions:* `m.ready() == true` in all cases. If the function
returns `false`, then the effect on parameter `m` is unspecified except
that `m.size()` returns `0` and `m.empty()` returns `true`. Otherwise
the effects on parameter `m` are given in Table  [[tab:re:alg:match]].

**Table: Effects of `regex_match` algorithm** <a id="tab:re:alg:match">[tab:re:alg:match]</a>

| Element              | Value                                                                                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `m.size()`           | `1 + e.mark_count()`                                                                                                                                                                |
| `m.empty()`          | false                                                                                                                                                                               |
| `m.prefix().first`   | first                                                                                                                                                                               |
| `m.prefix().second`  | first                                                                                                                                                                               |
| `m.prefix().matched` | false                                                                                                                                                                               |
| `m.suffix().first`   | last                                                                                                                                                                                |
| `m.suffix().second`  | last                                                                                                                                                                                |
| `m.suffix().matched` | false                                                                                                                                                                               |
| `m[0].first`         | first                                                                                                                                                                               |
| `m[0].second`        | last                                                                                                                                                                                |
| `m[0].matched`       | `true`                                                                                                                                                                              |
| `m[n].first`         | For all integers `0 < n < m.size()`, the start of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last`. |
| `m[n].second`        | For all integers `0 < n < m.size()`, the end of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last`.   |
| `m[n].matched`       | For all integers `0 < n < m.size()`, `true` if sub-expression `n` participated in the match, `false` otherwise.                                                                     |

``` cpp
template <class BidirectionalIterator, class charT, class traits>
  bool regex_match(BidirectionalIterator first, BidirectionalIterator last,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
```

*Effects:* Behaves “as if” by constructing an instance of
`match_results<BidirectionalIterator> what`, and then returning the
result of `regex_match(first, last, what, e, flags)`.

``` cpp
template <class charT, class Allocator, class traits>
  bool regex_match(const charT* str,
                   match_results<const charT*, Allocator>& m,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
```

*Returns:*
`regex_match(str, str + char_traits<charT>::length(str), m, e, flags)`.

``` cpp
template <class ST, class SA, class Allocator, class charT, class traits>
  bool regex_match(const basic_string<charT, ST, SA>& s,
                   match_results<
                     typename basic_string<charT, ST, SA>::const_iterator,
                     Allocator>& m,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
```

*Returns:* `regex_match(s.begin(), s.end(), m, e, flags)`.

``` cpp
template <class charT, class traits>
  bool regex_match(const charT* str,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
```

*Returns:*
`regex_match(str, str + char_traits<charT>::length(str), e, flags)`

``` cpp
template <class ST, class SA, class charT, class traits>
  bool regex_match(const basic_string<charT, ST, SA>& s,
                   const basic_regex<charT, traits>& e,
                   regex_constants::match_flag_type flags =
                     regex_constants::match_default);
```

*Returns:* `regex_match(s.begin(), s.end(), e, flags)`.

### `regex_search` <a id="re.alg.search">[[re.alg.search]]</a>

``` cpp
template <class BidirectionalIterator, class Allocator, class charT, class traits>
  bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                    match_results<BidirectionalIterator, Allocator>& m,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags =
                      regex_constants::match_default);
```

*Requires:* Type `BidirectionalIterator` shall satisfy the requirements
of a Bidirectional Iterator ([[bidirectional.iterators]]).

*Effects:* Determines whether there is some sub-sequence within
\[`first`, `last`) that matches the regular expression `e`. The
parameter `flags` is used to control how the expression is matched
against the character sequence. Returns `true` if such a sequence
exists, `false` otherwise.

*Postconditions:* `m.ready() == true` in all cases. If the function
returns `false`, then the effect on parameter `m` is unspecified except
that `m.size()` returns `0` and `m.empty()` returns `true`. Otherwise
the effects on parameter `m` are given in Table  [[tab:re:alg:search]].

**Table: Effects of `regex_search` algorithm** <a id="tab:re:alg:search">[tab:re:alg:search]</a>

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
| `m[n].second`        | For all integers `0 < n < m.size()`, the end of the sequence that matched sub-expression `n`. Alternatively, if sub-expression `n` did not participate in the match, then `last` .  |
| `m[n].matched`       | For all integers `0 < n < m.size()`, `true` if sub-expression `n` participated in the match, `false` otherwise.                                                                     |

``` cpp
template <class charT, class Allocator, class traits>
bool regex_search(const charT* str, match_results<const charT*, Allocator>& m,
                  const basic_regex<charT, traits>& e,
                  regex_constants::match_flag_type flags =
                    regex_constants::match_default);
```

*Returns:* The result of
`regex_search(str, str + char_traits<charT>::length(str), m, e, flags)`.

``` cpp
template <class ST, class SA, class Allocator, class charT, class traits>
  bool regex_search(const basic_string<charT, ST, SA>& s,
                    match_results<
                      typename basic_string<charT, ST, SA>::const_iterator,
                      Allocator>& m,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags =
                      regex_constants::match_default);
```

*Returns:* The result of
`regex_search(s.begin(), s.end(), m, e, flags)`.

``` cpp
template <class BidirectionalIterator, class charT, class traits>
  bool regex_search(BidirectionalIterator first, BidirectionalIterator last,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags =
                      regex_constants::match_default);
```

*Effects:* Behaves “as if” by constructing an object `what` of type
`match_results<BidirectionalIterator>` and then returning the result of
`regex_search(first, last, what, e, flags)`.

``` cpp
template <class charT, class traits>
  bool regex_search(const charT* str,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags =
                      regex_constants::match_default);
```

*Returns:*
`regex_search(str, str + char_traits<charT>::length(str), e, flags)`

``` cpp
template <class ST, class SA, class charT, class traits>
  bool regex_search(const basic_string<charT, ST, SA>& s,
                    const basic_regex<charT, traits>& e,
                    regex_constants::match_flag_type flags =
                      regex_constants::match_default);
```

*Returns:* `regex_search(s.begin(), s.end(), e, flags)`.

### `regex_replace` <a id="re.alg.replace">[[re.alg.replace]]</a>

``` cpp
template <class OutputIterator, class BidirectionalIterator,
    class traits, class charT, class ST, class SA>
  OutputIterator
  regex_replace(OutputIterator out,
                BidirectionalIterator first, BidirectionalIterator last,
                const basic_regex<charT, traits>& e,
                const basic_string<charT, ST, SA>& fmt,
                regex_constants::match_flag_type flags =
                  regex_constants::match_default);
template <class OutputIterator, class BidirectionalIterator,
    class traits, class charT>
  OutputIterator
  regex_replace(OutputIterator out,
                BidirectionalIterator first, BidirectionalIterator last,
                const basic_regex<charT, traits>& e,
                const charT* fmt,
                regex_constants::match_flag_type flags =
                  regex_constants::match_default);
```

*Effects:* Constructs a `regex_iterator` object `i` as if by

``` cpp
regex_iterator<BidirectionalIterator, charT, traits> i(first, last, e, flags)
```

and uses `i` to enumerate through all of the matches `m` of type
`match_results<BidirectionalIterator>` that occur within the sequence
\[`first`, `last`). If no such matches are found and
`!(flags & regex_constants::format_no_copy)` then calls

``` cpp
out = std::copy(first, last, out)
```

If any matches are found then, for each such match:

- If `!(flags & regex_constants::format_no_copy)`, calls
  ``` cpp
  out = std::copy(m.prefix().first, m.prefix().second, out)
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
out = std::copy(last_m.suffix().first, last_m.suffix().second, out)
```

where `last_m` is a copy of the last match found. If
`flags & regex_constants::format_first_only` is non-zero then only the
first match found is replaced.

*Returns:* `out`.

``` cpp
template <class traits, class charT, class ST, class SA, class FST, class FSA>
  basic_string<charT, ST, SA>
  regex_replace(const basic_string<charT, ST, SA>& s,
                const basic_regex<charT, traits>& e,
                const basic_string<charT, FST, FSA>& fmt,
                regex_constants::match_flag_type flags =
                  regex_constants::match_default);
template <class traits, class charT, class ST, class SA>
  basic_string<charT, ST, SA>
  regex_replace(const basic_string<charT, ST, SA>& s,
                const basic_regex<charT, traits>& e,
                const charT* fmt,
                regex_constants::match_flag_type flags =
                  regex_constants::match_default);
```

*Effects:* Constructs an empty string `result` of type
`basic_string<charT, ST, SA>` and calls
`regex_replace(back_inserter(result), s.begin(), s.end(), e, fmt, flags)`.

*Returns:*  `result`.

``` cpp
template <class traits, class charT, class ST, class SA>
  basic_string<charT>
  regex_replace(const charT* s,
                const basic_regex<charT, traits>& e,
                const basic_string<charT, ST, SA>& fmt,
                regex_constants::match_flag_type flags =
                  regex_constants::match_default);
template <class traits, class charT>
  basic_string<charT>
  regex_replace(const charT* s,
                const basic_regex<charT, traits>& e,
                const charT* fmt,
                regex_constants::match_flag_type flags =
                  regex_constants::match_default);
```

*Effects:* Constructs an empty string `result` of type
`basic_string<charT>` and calls `regex_replace(`
`back_inserter(result), s, s + char_traits<charT>::length(s), e, fmt, flags)`.

*Returns:*  `result`.

## Regular expression iterators <a id="re.iter">[[re.iter]]</a>

### Class template `regex_iterator` <a id="re.regiter">[[re.regiter]]</a>

The class template `regex_iterator` is an iterator adaptor. It
represents a new view of an existing iterator sequence, by enumerating
all the occurrences of a regular expression within that sequence. A
`regex_iterator` uses `regex_search` to find successive regular
expression matches within the sequence from which it was constructed.
After the iterator is constructed, and every time `operator++` is used,
the iterator finds and stores a value of
`match_results<BidirectionalIterator>`. If the end of the sequence is
reached (`regex_search` returns `false`), the iterator becomes equal to
the end-of-sequence iterator value. The default constructor constructs
an end-of-sequence iterator object, which is the only legitimate
iterator to be used for the end condition. The result of `operator*` on
an end-of-sequence iterator is not defined. For any other iterator value
a const `match_results<BidirectionalIterator>&` is returned. The result
of `operator->` on an end-of-sequence iterator is not defined. For any
other iterator value a `const match_results<BidirectionalIterator>*` is
returned. It is impossible to store things into `regex_iterator`s. Two
end-of-sequence iterators are always equal. An end-of-sequence iterator
is not equal to a non-end-of-sequence iterator. Two non-end-of-sequence
iterators are equal when they are constructed from the same arguments.

``` cpp
namespace std {
  template <class BidirectionalIterator,
            class charT = typename iterator_traits<
              BidirectionalIterator>::value_type,
              class traits = regex_traits<charT> >
  class regex_iterator {
  public:
     typedef basic_regex<charT, traits>           regex_type;
     typedef match_results<BidirectionalIterator> value_type;
     typedef std::ptrdiff_t                       difference_type;
     typedef const value_type*                    pointer;
     typedef const value_type&                    reference;
     typedef std::forward_iterator_tag            iterator_category;

     regex_iterator();
     regex_iterator(BidirectionalIterator a, BidirectionalIterator b,
                    const regex_type& re,
                    regex_constants::match_flag_type m =
                      regex_constants::match_default);
     regex_iterator(BidirectionalIterator a, BidirectionalIterator b,
                    const regex_type&& re,
                    regex_constants::match_flag_type m =
                      regex_constants::match_default) = delete;
     regex_iterator(const regex_iterator&);
     regex_iterator& operator=(const regex_iterator&);
     bool operator==(const regex_iterator&) const;
     bool operator!=(const regex_iterator&) const;
     const value_type& operator*() const;
     const value_type* operator->() const;
     regex_iterator& operator++();
     regex_iterator operator++(int);
  private:
     BidirectionalIterator                begin;  // exposition only
     BidirectionalIterator                end;    // exposition only
     const regex_type*                    pregex; // exposition only
     regex_constants::match_flag_type     flags;  // exposition only
     match_results<BidirectionalIterator> match;  // exposition only
  };
}
```

An object of type `regex_iterator` that is not an end-of-sequence
iterator holds a *zero-length match* if `match[0].matched == true` and
`match[0].first == match[0].second`. For example, this can occur when
the part of the regular expression that matched consists only of an
assertion (such as `'^'`, `'$'`, `'\b'`, `'\B'`).

#### `regex_iterator` constructors <a id="re.regiter.cnstr">[[re.regiter.cnstr]]</a>

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
sets `pregex` to `&re`, sets `flags` to `m`, then calls
`regex_search(begin, end, match, *pregex, flags)`. If this call returns
`false` the constructor sets `*this` to the end-of-sequence iterator.

#### `regex_iterator` comparisons <a id="re.regiter.comp">[[re.regiter.comp]]</a>

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

``` cpp
bool operator!=(const regex_iterator& right) const;
```

*Returns:* `!(*this == right)`.

#### `regex_iterator` indirection <a id="re.regiter.deref">[[re.regiter.deref]]</a>

``` cpp
const value_type& operator*() const;
```

*Returns:* `match`.

``` cpp
const value_type* operator->() const;
```

*Returns:* `&match`.

#### `regex_iterator` increment <a id="re.regiter.incr">[[re.regiter.incr]]</a>

``` cpp
regex_iterator& operator++();
```

*Effects:* Constructs a local variable `start` of type
`BidirectionalIterator` and initializes it with the value of
`match[0].second`.

If the iterator holds a zero-length match and `start == end` the
operator sets `*this` to the end-of-sequence iterator and returns
`*this`.

Otherwise, if the iterator holds a zero-length match the operator calls
`regex_search(start, end, match, *pregex, flags `|` regex_constants::match_not_null `|` regex_constants::match_`  
`continuous)`. If the call returns `true` the operator returns `*this`.
Otherwise the operator increments `start` and continues as if the most
recent match was not a zero-length match.

If the most recent match was not a zero-length match, the operator sets
`flags` to `flags `|` regex_constants ``match_prev_avail` and calls
`regex_search(start, end, match, *pregex, flags)`. If the call returns
`false` the iterator sets `*this` to the end-of-sequence iterator. The
iterator then returns `*this`.

In all cases in which the call to `regex_search` returns `true`,
`match.prefix().first` shall be equal to the previous value of
`match[0].second`, and for each index `i` in the half-open range
`[0, match.size())` for which `match[i].matched` is true,
`match[i].position()` shall return `distance(begin, match[i].first)`.

This means that `match[i].position()` gives the offset from the
beginning of the target sequence, which is often not the same as the
offset from the sequence passed in the call to `regex_search`.

It is unspecified how the implementation makes these adjustments.

This means that a compiler may call an implementation-specific search
function, in which case a user-defined specialization of `regex_search`
will not be called.

``` cpp
regex_iterator operator++(int);
```

*Effects:*

``` cpp
regex_iterator tmp = *this;
++(*this);
return tmp;
```

### Class template `regex_token_iterator` <a id="re.tokiter">[[re.tokiter]]</a>

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
  template <class BidirectionalIterator,
            class charT = typename iterator_traits<
              BidirectionalIterator>::value_type,
              class traits = regex_traits<charT> >
  class regex_token_iterator  {
  public:
    typedef basic_regex<charT, traits>       regex_type;
    typedef sub_match<BidirectionalIterator> value_type;
    typedef std::ptrdiff_t                   difference_type;
    typedef const value_type*                pointer;
    typedef const value_type&                reference;
    typedef std::forward_iterator_tag        iterator_category;

    regex_token_iterator();
    regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                        const regex_type& re,
                        int submatch = 0,
                        regex_constants::match_flag_type m =
                          regex_constants::match_default);
    regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                        const regex_type& re,
                        const std::vector<int>& submatches,
                        regex_constants::match_flag_type m =
                          regex_constants::match_default);
    regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                        const regex_type& re,
                        initializer_list<int> submatches,
                        regex_constants::match_flag_type m =
                          regex_constants::match_default);
    template <std::size_t N>
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
                         const std::vector<int>& submatches,
                         regex_constants::match_flag_type m =
                           regex_constants::match_default) = delete;
    regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                         const regex_type&& re,
                         initializer_list<int> submatches,
                         regex_constants::match_flag_type m =
                           regex_constants::match_default) = delete;
    template <std::size_t N>
    regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                         const regex_type&& re,
                         const int (&submatches)[N],
                         regex_constants::match_flag_type m =
                           regex_constants::match_default) = delete;
    regex_token_iterator(const regex_token_iterator&);
    regex_token_iterator& operator=(const regex_token_iterator&);
    bool operator==(const regex_token_iterator&) const;
    bool operator!=(const regex_token_iterator&) const;
    const value_type& operator*() const;
    const value_type* operator->() const;
    regex_token_iterator& operator++();
    regex_token_iterator operator++(int);
  private:
    typedef
      regex_iterator<BidirectionalIterator, charT, traits> position_iterator; // exposition only
    position_iterator position;                                               // exposition only
    const value_type* result;                                                 // exposition only
    value_type suffix;                                                        // exposition only
    std::size_t N;                                                            // exposition only
    std::vector<int> subs;                                                    // exposition only
  };
}
```

A *suffix iterator* is a `regex_token_iterator` object that points to a
final sequence of characters at the end of the target sequence. In a
suffix iterator the member `result` holds a pointer to the data member
`suffix`, the value of the member `suffix.match` is `true`,
`suffix.first` points to the beginning of the final sequence, and
`suffix.second` points to the end of the final sequence.

For a suffix iterator, data member `suffix.first` is the same as the end
of the last match found, and `suffix.second` is the same as the end of
the target sequence

The *current match* is `(*position).prefix()` if `subs[N] == -1`, or
`(*position)[subs[N]]` for any other value of `subs[N]`.

#### `regex_token_iterator` constructors <a id="re.tokiter.cnstr">[[re.tokiter.cnstr]]</a>

``` cpp
regex_token_iterator();
```

*Effects:* Constructs the end-of-sequence iterator.

``` cpp
regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                    const regex_type& re,
                    int submatch = 0,
                    regex_constants::match_flag_type m =
                     regex_constants::match_default);

regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                    const regex_type& re,
                    const std::vector<int>& submatches,
                    regex_constants::match_flag_type m =
                     regex_constants::match_default);

regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                    const regex_type& re,
                    initializer_list<int> submatches,
                    regex_constants::match_flag_type m =
                      regex_constants::match_default);

template <std::size_t N>
  regex_token_iterator(BidirectionalIterator a, BidirectionalIterator b,
                    const regex_type& re,
                    const int (&submatches)[N],
                    regex_constants::match_flag_type m =
                     regex_constants::match_default);
```

*Requires:* Each of the initialization values of `submatches` shall be
`>= -1`.

*Effects:* The first constructor initializes the member `subs` to hold
the single value `submatch`. The second constructor initializes the
member `subs` to hold a copy of the argument `submatches`. The third and
fourth constructors initialize the member `subs` to hold a copy of the
sequence of integer values pointed to by the iterator range
\[`submatches.begin()`, `submatches.end()`) and \[`&submatches`,
`&submatches + N`), respectively.

Each constructor then sets `N` to 0, and `position` to
`position_iterator(a, b, re, m)`. If `position` is not an
end-of-sequence iterator the constructor sets `result` to the address of
the current match. Otherwise if any of the values stored in `subs` is
equal to -1 the constructor sets `*this` to a suffix iterator that
points to the range \[`a`, `b`), otherwise the constructor sets `*this`
to an end-of-sequence iterator.

#### `regex_token_iterator` comparisons <a id="re.tokiter.comp">[[re.tokiter.comp]]</a>

``` cpp
bool operator==(const regex_token_iterator& right) const;
```

*Returns:* `true` if `*this` and `right` are both end-of-sequence
iterators, or if `*this` and `right` are both suffix iterators and
`suffix == right.suffix`; otherwise returns `false` if `*this` or
`right` is an end-of-sequence iterator or a suffix iterator. Otherwise
returns `true` if `position == right.position`, `N == right.N`, and
`subs == right.subs`. Otherwise returns `false`.

``` cpp
bool operator!=(const regex_token_iterator& right) const;
```

*Returns:* `!(*this == right)`.

#### `regex_token_iterator` indirection <a id="re.tokiter.deref">[[re.tokiter.deref]]</a>

``` cpp
const value_type& operator*() const;
```

*Returns:* `*result`.

``` cpp
const value_type* operator->() const;
```

*Returns:* `result`.

#### `regex_token_iterator` increment <a id="re.tokiter.incr">[[re.tokiter.incr]]</a>

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

*Returns:* `*this`

``` cpp
regex_token_iterator& operator++(int);
```

*Effects:* Constructs a copy `tmp` of `*this`, then calls `++(*this)`.

*Returns:* `tmp`.

## Modified ECMAScript regular expression grammar <a id="re.grammar">[[re.grammar]]</a>

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

``` cpp
ClassAtom ::
  -
  ClassAtomNoDash
  ClassAtomExClass
  ClassAtomCollatingElement
  ClassAtomEquivalence
```

The following new productions are then added:

``` cpp
ClassAtomExClass ::
  [: ClassName :]

ClassAtomCollatingElement ::
  [. ClassName .]

ClassAtomEquivalence ::
  [= ClassName =]

ClassName ::
  ClassNameCharacter
  ClassNameCharacter ClassName

ClassNameCharacter ::
  SourceCharacter but not one of "." "=" ":"
```

The productions `ClassAtomExClass`, `ClassAtomCollatingElement` and
`ClassAtomEquivalence` provide functionality equivalent to that of the
same features in regular expressions in POSIX.

The regular expression grammar may be modified by any
`regex_constants::syntax_option_type` flags specified when constructing
an object of type specialization of `basic_regex` according to the rules
in Table [[tab:re:syntaxoption]].

A `ClassName` production, when used in `ClassAtomExClass`, is not valid
if `traits_inst.lookup_classname` returns zero for that name. The names
recognized as valid `ClassName`s are determined by the type of the
traits class, but at least the following names shall be recognized:
`alnum`, `alpha`, `blank`, `cntrl`, `digit`, `graph`, `lower`, `print`,
`punct`, `space`, `upper`, `xdigit`, `d`, `s`, `w`. In addition the
following expressions shall be equivalent:

``` cpp
\d and [[:digit:]]

\D and [^[:digit:]]

\s and [[:space:]]

\S and [^[:space:]]

\w and [_[:alnum:]]

\W and [^_[:alnum:]]
```

A `ClassName` production when used in a `ClassAtomCollatingElement`
production is not valid if the value returned by
`traits_inst.lookup_collatename` for that name is an empty string.

The results from multiple calls to `traits_inst.lookup_classname` can be
bitwise OR’ed together and subsequently passed to `traits_inst.isctype`.

A `ClassName` production when used in a `ClassAtomEquivalence`
production is not valid if the value returned by
`traits_inst.lookup_collatename` for that name is an empty string or if
the value returned by `traits_inst.transform_primary` for the result of
the call to `traits_inst.lookup_collatename` is an empty string.

When the sequence of characters being transformed to a finite state
machine contains an invalid class name the translator shall throw an
exception object of type `regex_error`.

If the *CV* of a *UnicodeEscapeSequence* is greater than the largest
value that can be held in an object of type `charT` the translator shall
throw an exception object of type `regex_error`. This means that values
of the form `"uxxxx"` that do not fit in a character are invalid.

Where the regular expression grammar requires the conversion of a
sequence of characters to an integral value, this is accomplished by
calling `traits_inst.value`.

The behavior of the internal finite state machine representation when
used to match a sequence of characters is as described in ECMA-262. The
behavior is modified according to any match_flag_type flags 
[[re.matchflag]] specified when using the regular expression object in
one of the regular expression algorithms  [[re.alg]]. The behavior is
also localized by interaction with the traits class template parameter
as follows:

- During matching of a regular expression finite state machine against a
  sequence of characters, two characters `c` and `d` are compared using
  the following rules:
  1.  if `(flags() & regex_constants::icase)` the two characters are
      equal if
      `traits_inst.translate_nocase(c) == traits_inst.translate_nocase(d)`;
  2.  otherwise, if `flags() & regex_constants::collate` the two
      characters are equal if
      `traits_inst.translate(c) == traits_inst.translate(d)`;
  3.  otherwise, the two characters are equal if `c == d`.
- During matching of a regular expression finite state machine against a
  sequence of characters, comparison of a collating element range
  `c1-c2` against a character `c` is conducted as follows: if
  `flags() & regex_constants \colcol
  collate` is false then the character `c` is matched if `c1
  <= c && c <= c2`, otherwise `c` is matched in accordance with the
  following algorithm:
  ``` cpp
  string_type str1 = string_type(1,
    flags() & icase ?
      traits_inst.translate_nocase(c1) : traits_inst.translate(c1);
  string_type str2 = string_type(1,
    flags() & icase ?
      traits_inst.translate_nocase(c2) : traits_inst.translate(c2);
  string_type str = string_type(1,
    flags() & icase ?
      traits_inst.translate_nocase(c) : traits_inst.translate(c);
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

<!-- Link reference definitions -->
[algorithms]: algorithms.md#algorithms
[bidirectional.iterators]: iterators.md#bidirectional.iterators
[bitmask.types]: library.md#bitmask.types
[enumerated.types]: library.md#enumerated.types
[forward.iterators]: iterators.md#forward.iterators
[input.iterators]: iterators.md#input.iterators
[output.iterators]: iterators.md#output.iterators
[re]: #re
[re.alg]: #re.alg
[re.alg.match]: #re.alg.match
[re.alg.replace]: #re.alg.replace
[re.alg.search]: #re.alg.search
[re.badexp]: #re.badexp
[re.const]: #re.const
[re.def]: #re.def
[re.err]: #re.err
[re.except]: #re.except
[re.general]: #re.general
[re.grammar]: #re.grammar
[re.iter]: #re.iter
[re.matchflag]: #re.matchflag
[re.regex]: #re.regex
[re.regex.assign]: #re.regex.assign
[re.regex.const]: #re.regex.const
[re.regex.construct]: #re.regex.construct
[re.regex.locale]: #re.regex.locale
[re.regex.nmswap]: #re.regex.nmswap
[re.regex.nonmemb]: #re.regex.nonmemb
[re.regex.operations]: #re.regex.operations
[re.regex.swap]: #re.regex.swap
[re.regiter]: #re.regiter
[re.regiter.cnstr]: #re.regiter.cnstr
[re.regiter.comp]: #re.regiter.comp
[re.regiter.deref]: #re.regiter.deref
[re.regiter.incr]: #re.regiter.incr
[re.req]: #re.req
[re.results]: #re.results
[re.results.acc]: #re.results.acc
[re.results.all]: #re.results.all
[re.results.const]: #re.results.const
[re.results.form]: #re.results.form
[re.results.nonmember]: #re.results.nonmember
[re.results.size]: #re.results.size
[re.results.state]: #re.results.state
[re.results.swap]: #re.results.swap
[re.submatch]: #re.submatch
[re.submatch.members]: #re.submatch.members
[re.submatch.op]: #re.submatch.op
[re.syn]: #re.syn
[re.synopt]: #re.synopt
[re.tokiter]: #re.tokiter
[re.tokiter.cnstr]: #re.tokiter.cnstr
[re.tokiter.comp]: #re.tokiter.comp
[re.tokiter.deref]: #re.tokiter.deref
[re.tokiter.incr]: #re.tokiter.incr
[re.traits]: #re.traits
[sequence.reqmts]: containers.md#sequence.reqmts
[tab:re.lib.summary]: #tab:re.lib.summary
[tab:re.traits.classnames]: #tab:re.traits.classnames
[tab:re:RegexpTraits]: #tab:re:RegexpTraits
[tab:re:alg:match]: #tab:re:alg:match
[tab:re:alg:search]: #tab:re:alg:search
[tab:re:errortype]: #tab:re:errortype
[tab:re:matchflag]: #tab:re:matchflag
[tab:re:results:assign]: #tab:re:results:assign
[tab:re:syntaxoption]: #tab:re:syntaxoption

[^1]: For example, if the parameter `icase` is true then `[[:lower:]]`
    is the same as `[[:alpha:]]`.
