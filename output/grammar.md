## General <a id="gram.general">[gram.general]</a>

This summary of C++ grammar is intended to be an aid to comprehension.
It is not an exact statement of the language. In particular, the grammar
described here accepts a superset of valid C++ constructs.
Disambiguation rules [stmt.ambig], [dcl.spec], [class.member.lookup] are
applied to distinguish expressions from declarations. Further, access
control, ambiguity, and type rules are used to weed out syntactically
valid but meaningless constructs.

## Keywords <a id="gram.key">[gram.key]</a>

New context-dependent keywords are introduced into a program by
`typedef` [dcl.typedef], `namespace` [namespace.def], class [class],
enumeration [dcl.enum], and `template` [temp] declarations.

``` bnf
typedef-name:
    identifier
    simple-template-id
```

``` bnf
namespace-name:
    identifier
    namespace-alias
```

``` bnf
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

<!-- Link reference definitions -->
[class]: class.md#class
[class.member.lookup]: basic.md#class.member.lookup
[dcl.enum]: dcl.md#dcl.enum
[dcl.spec]: dcl.md#dcl.spec
[dcl.typedef]: dcl.md#dcl.typedef
[namespace.def]: dcl.md#namespace.def
[stmt.ambig]: stmt.md#stmt.ambig
[temp]: temp.md#temp
