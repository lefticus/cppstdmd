---
current_file: uax31
label_index_file: converted/cppstdmd/output/cpp_std_labels.lua
---

## General <a id="uaxid.general">[[uaxid.general]]</a>

This Annex describes the choices made in application of (“Unicode
Identifier and Pattern Syntax”) to C++ in terms of the requirements from
and how they do or do not apply to C++. In terms of , C++ conforms by
meeting the requirements R1 “Default Identifiers” and R4 “Equivalent
Normalized Identifiers”. The other requirements, also listed below, are
either alternatives not taken or do not apply to C++.

## R1 Default identifiers <a id="uaxid.def">[[uaxid.def]]</a>

### General <a id="uaxid.def.general">[[uaxid.def.general]]</a>

specifies a default syntax for identifiers based on properties from the
Unicode Character Database, . The general syntax is

``` cpp
<Identifier> := <Start> <Continue>* (<Medial> <Continue>+)*
```

where `<Start>` has the XID_Start property, `<Continue>` has the
XID_Continue property, and `<Medial>` is a list of characters permitted
between continue characters. For C++ we add the character , or `_`, to
the set of permitted `<Start>` characters, the `<Medial>` set is empty,
and the `<Continue>` characters are unmodified. In the grammar used in ,
this is

``` cpp
<Identifier> := <Start> <Continue>*
<Start> := XID_Start + \textrm{\ucode{005f}}
<Continue> := <Start> + XID_Continue
```

This is described in the C++ grammar in [[lex.name]], where *identifier*
is formed from *identifier-start* or *identifier* followed by
*identifier-continue*.

### R1a Restricted format characters <a id="uaxid.def.rfmt">[[uaxid.def.rfmt]]</a>

If an implementation of wishes to allow format characters such as or it
must define a profile allowing them, or describe precisely which
combinations are permitted.

C++ does not allow format characters in identifiers, so this does not
apply.

### R1b Stable identifiers <a id="uaxid.def.stable">[[uaxid.def.stable]]</a>

An implementation of may choose to guarantee that identifiers are stable
across versions of the Unicode Standard. Once a string qualifies as an
identifier it does so in all future versions.

C++ does not make this guarantee, except to the extent that guarantees
the stability of the XID_Start and XID_Continue properties.

## R2 Immutable identifiers <a id="uaxid.immutable">[[uaxid.immutable]]</a>

An implementation may choose to guarantee that the set of identifiers
will never change by fixing the set of code points allowed in
identifiers forever.

C++ does not choose to make this guarantee. As scripts are added to
Unicode, additional characters in those scripts may become available for
use in identifiers.

## R3 Pattern_White_Space and Pattern_Syntax characters <a id="uaxid.pattern">[[uaxid.pattern]]</a>

describes how formal languages such as computer languages should
describe and implement their use of whitespace and syntactically
significant characters during the processes of lexing and parsing.

C++ does not claim conformance with this requirement.

## R4 Equivalent normalized identifiers <a id="uaxid.eqn">[[uaxid.eqn]]</a>

requires that implementations describe how identifiers are compared and
considered equivalent.

C++ requires that identifiers be in Normalization Form C and therefore
identifiers that compare the same under NFC are equivalent. This is
described in [[lex.name]].

## R5 Equivalent case-insensitive identifiers <a id="uaxid.eqci">[[uaxid.eqci]]</a>

C++ considers case to be significant in identifier comparison, and does
not do any case folding. This requirement does not apply to C++.

## R6 Filtered normalized identifiers <a id="uaxid.filter">[[uaxid.filter]]</a>

If any characters are excluded from normalization, requires a precise
specification of those exclusions.

C++ does not make any such exclusions.

## R7 Filtered case-insensitive identifiers <a id="uaxid.filterci">[[uaxid.filterci]]</a>

C++ identifiers are case sensitive, and therefore this requirement does
not apply.

## R8 Hashtag identifiers <a id="uaxid.hashtag">[[uaxid.hashtag]]</a>

There are no hashtags in C++, so this requirement does not apply.

<!-- Link reference definitions -->
[[lex.name]]: lex.md#lex.name
