# Grammar summary (informative) <a id="gram" data-annex="true" data-annex-type="informative">[[gram]]</a>

This summary of C++ grammar is intended to be an aid to comprehension.
It is not an exact statement of the language. In particular, the grammar
described here accepts a superset of valid C++ constructs.
Disambiguation rules ([[stmt.ambig]], [[dcl.spec]],
[[class.member.lookup]]) must be applied to distinguish expressions from
declarations. Further, access control, ambiguity, and type rules must be
used to weed out syntactically valid but meaningless constructs.

## Keywords <a id="gram.key">[[gram.key]]</a>

New context-dependent keywords are introduced into a program by
`typedef` ([[dcl.typedef]]), `namespace` ([[namespace.def]]),
class (Clause [[class]]), enumeration ([[dcl.enum]]), and
`template` (Clause [[temp]]) declarations.

``` bnf
typedef-name:
    identifier
```

``` bnf
namespace-name:
    identifier
    namespace-alias

namespace-alias:
    identifier
```

``` bnf
class-name:
    identifier
    simple-template-id
```

``` bnf
enum-name:
    identifier
```

``` bnf
template-name:
    identifier
```

Note that a *typedef-name* naming a class is also a *class-name* (
[[class.name]]).

<!-- Link reference definitions -->
[class]: class.md#class
[class.member.lookup]: class.md#class.member.lookup
[class.name]: class.md#class.name
[dcl.enum]: dcl.md#dcl.enum
[dcl.spec]: dcl.md#dcl.spec
[dcl.typedef]: dcl.md#dcl.typedef
[gram]: #gram
[gram.key]: #gram.key
[namespace.def]: dcl.md#namespace.def
[stmt.ambig]: stmt.md#stmt.ambig
[temp]: temp.md#temp
