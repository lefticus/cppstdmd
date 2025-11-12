## General <a id="uaxid.general">[[uaxid.general]]</a>

This Annex describes the choices made in application of UAX \#31
(“Unicode Identifier and Pattern Syntax”) to C++ in terms of the
requirements from UAX \#31 and how they do or do not apply to this
document. In terms of UAX \#31, this document conforms by meeting the
requirements R1 “Default Identifiers” and R4 “Equivalent Normalized
Identifiers” from UAX \#31. The other requirements from UAX \#31, also
listed below, are either alternatives not taken or do not apply to this
document.

## R1 Default identifiers <a id="uaxid.def">[[uaxid.def]]</a>

### General <a id="uaxid.def.general">[[uaxid.def.general]]</a>

UAX \#31 specifies a default syntax for identifiers based on properties
from the Unicode Character Database, UAX \#44. The general syntax is

``` text
<Identifier> := <Start> <Continue>* (<Medial> <Continue>+)*
```

where `<Start>` has the XID_Start property, `<Continue>` has the
XID_Continue property, and `<Medial>` is a list of characters permitted
between continue characters. For C++ we add the character
U+005f (low line), or `_`, to the set of permitted `<Start>` characters,
the `<Medial>` set is empty, and the `<Continue>` characters are
unmodified. In the grammar used in UAX \#31, this is

``` text
<Identifier> := <Start> <Continue>*
<Start> := XID_Start + U+005f
<Continue> := <Start> + XID_Continue
```

This is described in the C++ grammar in [[lex.name]], where *identifier*
is formed from *identifier-start* or *identifier* followed by
*identifier-continue*.

### R1b Stable identifiers <a id="uaxid.def.stable">[[uaxid.def.stable]]</a>

An implementation of UAX \#31 may choose to guarantee that identifiers
are stable across versions of the Unicode Standard. Once a string
qualifies as an identifier it does so in all future versions.

C++ does not make this guarantee, except to the extent that UAX \#31
guarantees the stability of the XID_Start and XID_Continue properties.

## R2 Immutable identifiers <a id="uaxid.immutable">[[uaxid.immutable]]</a>

An implementation may choose to guarantee that the set of identifiers
will never change by fixing the set of code points allowed in
identifiers forever.

C++ does not choose to make this guarantee. As scripts are added to
Unicode, additional characters in those scripts may become available for
use in identifiers.

## R3 Pattern_White_Space and Pattern_Syntax characters <a id="uaxid.pattern">[[uaxid.pattern]]</a>

UAX \#31 describes how formal languages such as computer languages
should describe and implement their use of whitespace and syntactically
significant characters during the processes of lexing and parsing.

This document does not claim conformance with this requirement from UAX
\#31.

## R4 Equivalent normalized identifiers <a id="uaxid.eqn">[[uaxid.eqn]]</a>

UAX \#31 requires that implementations describe how identifiers are
compared and considered equivalent.

This document requires that identifiers be in Normalization Form C and
therefore identifiers that compare the same under NFC are equivalent.
This is described in [[lex.name]].

## R5 Equivalent case-insensitive identifiers <a id="uaxid.eqci">[[uaxid.eqci]]</a>

This document considers case to be significant in identifier comparison,
and does not do any case folding. This requirement from UAX \#31 does
not apply to this document.

## R6 Filtered normalized identifiers <a id="uaxid.filter">[[uaxid.filter]]</a>

If any characters are excluded from normalization, UAX \#31 requires a
precise specification of those exclusions.

This document does not make any such exclusions.

## R7 Filtered case-insensitive identifiers <a id="uaxid.filterci">[[uaxid.filterci]]</a>

C++ identifiers are case sensitive, and therefore this requirement from
UAX \#31 does not apply.

## R8 Hashtag identifiers <a id="uaxid.hashtag">[[uaxid.hashtag]]</a>

There are no hashtags in C++, so this requirement from UAX \#31 does not
apply.

<!-- Section link definitions -->
[uaxid.def]: #uaxid.def
[uaxid.def.general]: #uaxid.def.general
[uaxid.def.stable]: #uaxid.def.stable
[uaxid.eqci]: #uaxid.eqci
[uaxid.eqn]: #uaxid.eqn
[uaxid.filter]: #uaxid.filter
[uaxid.filterci]: #uaxid.filterci
[uaxid.general]: #uaxid.general
[uaxid.hashtag]: #uaxid.hashtag
[uaxid.immutable]: #uaxid.immutable
[uaxid.pattern]: #uaxid.pattern

<!-- Link reference definitions -->
[lex.name]: lex.md#lex.name
