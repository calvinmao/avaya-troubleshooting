---
title: "SPI-SYN24 - complete source pages 101-120"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 101-120

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-101"></a>

## PDF page 101

Source: SPI-SYN24; PDF page 101; extracted characters: 1265.

```text
Format C:

For condition 10 (if digits), the following fields are contained in the message.
For condition 19 (A-Z, V1-V5 (variable)), var_c applies.
For condition 20, 21 and 22 (CM 3.0 and later), the following fields are contained in the message.

     7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0   7    6   5   4   3   2   1   0
        stype17 or         -     c                    -                          cond                           table
         stype-18
     -       cmp                  -                     -              v       -                 -                        -
                                  dest                                          step-num                            var_t
      v_t                    var_c                                       -                                        -
          d1              d2               d3              d4               d5              d6               d7              d8
          d9              d10             d11              d12             d13              d14             d15              d16
           -               -                -               -                -               -                -               -
```

<a id="pdf-page-102"></a>

## PDF page 102

Source: SPI-SYN24; PDF page 102; extracted characters: 2919.

```text
stype-17 or          goto step or goto vector
stype-18
c                    1=this step is commented out
dest                 Step number to go to (1-32) if stype-17.
                     Vector to go to (1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later) if
                     stype-18
table                Vector routing table number in which to check digits: 1-100 (through CM5.2), 1-999
                     (CM6.0 or later). If comparator is 7 or 8, if table=0 then v=1.
cmp                  For condition 20 and 21 only comparators 3 and 4 are valid.
                     For condition 22 comparators 1-6 are valid.

                       Comparator         Comparator          Comparators
                       s                  s
                       1 >                4 <>                7 in (table)
                       2 <                5 >=                8 not-in (table)
                       3 =                6 <=
var_t                Variable threshold: 1-26 for variable A-Z (if comparator is 1-6) (MV2 and later),
                     1-26 for variable A-Z (if comparator is 7-8) (CM 3.0 and later),
                     27-31 for VDN variable V1-V5 (if comparator is 1-8) (CM 3.0 and later)
var_c                Variable condition:
                     1-26 for variable A-Z, for condition 19 only (if comparator is 1-6) (MV2 and later),
                     27-31 for VDN variable V1-V5, for condition 19 only (if comparator is 1-8) (CM 3.0 and
                     later)
v                    Variable threshold flag: 0=no variable in var_t, 1=variable is in var_t (MV2 and later)
step_num             Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
d1-d16               Digits for condition 10, 19, 20, 21 and 22 (if comparator is 1-6 and "v" is 0) are as
                     follows:
                     The hex 0, representing null, is used when digits = "none".
                       hex    char     hex     char
                       0      null     a       0
                       1      1        b       *
                       2      2        c       #  (only valid in a single-character digit string)
                       3      3        d       ?
                       4      4        e       any (only condition 20 and 21 in a single-character digit string)
                       5      5        f       all (only condition 20 and 21 in a single-character digit string)
                       6      6
                       7      7        d       main (only condition 22 in a single-character digit string)
                       8      8        e       ess  (only condition 22 in a single-character digit string)
                       9      9        f       lsp  (only condition 22 in a single-character digit string)

                       hex    char     meaning
                       e0     +        (used in wildcarding)
```

<a id="pdf-page-103"></a>

## PDF page 103

Source: SPI-SYN24; PDF page 103; extracted characters: 1972.

```text
Format D:

For conditions 11, 13 and 14 (ASA, ANI, and counted-calls) and condition 16 (wait-improved), one of the
two following field layouts for the message will apply. If the condition, type, and subtype match the table
below, the first message layout applies.  Otherwise, a match should be found in the second message
layout (Format E).

          Condition              Type      Subtype      # of Digits                    Threshold       var_t Allowed
          11-ASA                 VDN       ext          1-15 (< language 24)           0-999           yes
                                                        1-16 (>= language 24)
          13-ANI                 digits    N/A          1-16 (< language 24)           N/A             yes
                                                        1-24 (>= language 24)
          14-counted-calls       VDN       ext          1-15 (< language 24)           0-999           yes
                                                        1-16 (>= language 24)

    7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0   7   6  5   4   3   2   1   0
       stype17 or         -    c                   -                        cond                         table
        stype-18
    -       cmp                -                     -            v       -              type                  subtype
                                dest                                       step-num                         var_t
     v_t                     -                                      -                                      -
         d1              d2             d3              d4             d5             d6              d7             d8
         d9             d10             d11            d12            d13             d14            d15             d16
         d17            d18             d19            d20            d21             d22            d23             d24
```

<a id="pdf-page-104"></a>

## PDF page 104

Source: SPI-SYN24; PDF page 104; extracted characters: 2104.

```text
Format D (continued)

stype-17 or             goto step or goto vector
stype-18
c                       1=this step is commented out
dest                    destination.  Step number to go to (1-32) if stype-17.
                        Vector to go to: 1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
                        if stype-18
cond                    see the condition/threshold above
threshold               see the condition/threshold above (if "v" is 0)

cmp                      Comparator
                         s
                         1       >
                         2       <
                         3       =
                         4       <>
                         5       >=
                         6       <=
step_num                Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
var_t                   Variable threshold: 1-26 for variable A-Z, condition 11 and 14 (MV2 and later), 27-31
                        for VDN variable V1-V5, condition 11 and 14 (CM 3.0 and later)
v                       Variable threshold flag: 0=no variable in var_t, 1=variable is in var_t, condition 11 and
                        14 (MV2 and later)
type                     2    VDN extension
                         5    digits
subtype                  0    N/A
                         1    extension
d1-d16 (<               digits for condition 11, 13 and 14 as follows:
language 24)            The hex 0, representing null, is used when digits = "none"

d1-d24 (>=               hex     char    hex    char
language 24)             0       nul     7      7
                         1       1       8      8
                         2       2       9      9
                         3       3       a      0
                         4       4       b      *  (not valid)
                         5       5       c      #  (not valid)
                         6       6       d      ?  (condition 13 only)

                         hex     char    interpretation
                         e0      +       (used in wildcarding - condition 13 only))
```

<a id="pdf-page-105"></a>

## PDF page 105

Source: SPI-SYN24; PDF page 105; extracted characters: 2489.

```text
Format E:

For conditions 11, 12, 13 and 14 (ASA, EWT, ANI, and counted-calls) and condition 16 (wait-improved)
which do not have the message layout specified above, the message will contain the fields identified in
the following table, and the message will have the following layout.

Condition               Type         Subtype              Type_val               Threshold      d9-d12 (wait time)       var_t
11-ASA                  split/skill  N/A                  split/skill number     0-999          N/A                      yes
11-ASA                  VDN          active or latest     N/A                    0-999          N/A                      yes
12-EWT                  split/skill  N/A                  split/skill number     N/A            1-9999                   yes
12-EWT                  Call         N/A                  N/A                    N/A            1-9999                   yes
12-EWT                  Best         N/A                  N/A                    N/A            1-9999                   yes
13-ANI                  Table        N/A                  table number           N/A            N/A                      yes
14-counted-calls        VDN          active or latest     N/A                    0-999          N/A                      yes
16-wait-improved        split/skill  N/A                  split/skill number     N/A            0-9999                   yes
16-wait-improved        Best         N/A                  N/A                    N/A            0-9999                   yes



    7   6   5   4   3  2   1   0   7   6   5  4   3   2   1   0  7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0
       stype17 or        pri   c                  -                        cond                      threshold
        stype-18
    s       cmp                -                    -            v       -               type                 subtype
                               dest                                        step-num                        var_t
     v_t                     -                                     -                                      -
                             type_val                                  -              -               -              -
         d9             d10            d11            d12              -              -               -              -
          -              -               -              -              -              -               -              -
```

<a id="pdf-page-106"></a>

## PDF page 106

Source: SPI-SYN24; PDF page 106; extracted characters: 2199.

```text
Format E (continued)

stype-17 or          goto step or goto vector
stype-18
pri                  0 = low, 1 = medium, 2 = high, 3 = top (for conditions 6, 8, 12)
c                    1=this step is commented out
dest                 Destination.  Step number to go to (1-32) if stype-17.
                     Vector to go to (1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later) if
                     stype-18
cond                 see the condition/threshold above
threshold            see the condition/threshold above (if "v" is 0)
s                    0=specific split/skill in type_val, 1=VDN skill preference in type_val
cmp                    Comparators
                       1   >
                       2   <
                       3   =
                       4   <>
                       5   >=
                       6   <=
                       7   in (applies only to conditions 10 and 13)
                       8   not-in (applies only to conditions 10 and 13)
var_t                Variable threshold:
                     1-26 for variable A-Z, conditions 11 and 14 (for comparator 1-6) (MV2 and later),
                     1-26 for variable A-Z, conditions 11 and 14 (for comparator 7-8) (CM 3.0 and later),
                     27-31 for VDN variable V1-V5, conditions 11 and 14 (for comparator 1-8) (CM 3.0 and
                     later)
v                    Variable threshold flag:
                     0=no variable in var_t, 1=variable is in var_t, conditions 11 and 14 (MV2 and later)
type                   1   split/skill
                       2   VDN
                       3   call
                       4   table
                       7   best
subtype              (applies only to conditions 11 and 14)
                       0   N/A
                       2   active
                       3   latest
type_val             split/skill for type=1, 1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000 (CM6.0 and
                     later), or table number if type=4: 1-100 (through CM5.2), 1-999 (CM6.0 and later)
step_num             Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
d9-d12               Wait time, in seconds (0-9999)
```

<a id="pdf-page-107"></a>

## PDF page 107

Source: SPI-SYN24; PDF page 107; extracted characters: 3104.

```text
Format F:

For condition 15 (if ii-digits), the following fields are contained in the message.

     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
        stype17 or        -     c                   -                         cond                         table
        stype-18
     -       cmp                -                     -             v       -                 -                      -
                                dest                                         step-num                          var_t
     v_t                      -                                       -                                      -
          d1             d2              d3               -               -               -              -               -
          -               -               -               -               -               -              -               -
          -               -               -               -               -               -              -               -

stype-17 or         goto step or goto vector
stype-18
c                   1=this step is commented out
dest                destination.  Step number to go to (1-32) if stype-17.
                    Vector to go to (1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later) if
                    stype-18
table               table number in which to check digits: 1-100 (through CM5.2), 1-999 (CM6.0 or later) if
                    comparator is 7 or 8
cmp                  Comparators
                     1    >
                     2    <
                     3    =
                     4    <>
                     5    >=
                     6    <=
                     7    in (table)
                     8    not-in (table)
var_t               Variable threshold: 1-26 for variable A-Z (for comparator 1-6) (MV2 and later), 1-26 for
                    variable A-Z (for comparator 7-8) (CM 3.0 and later), 27-31 for VDN variable V1-V5 (for
                    comparator 1-8) (CM 3.0 and later)
v                   Variable threshold flag: 0=no variable in var_t, 1=variable is in var_t (MV2 and later)
d1-d2               digits for condition 15 (if comparator is 1-6 and "v" is 0) are as follows: The hex 0,
                    representing null, is used when digits = "none".
d1-d3               d1-d2 as above for most cases, d3 also needed when one digit is "+" represented by hex
                    e0.

                     hex     char     hex    char
                     0       null     7      7
                     1       1        8      8
                     2       2        9      9
                     3       3        a      0
                     4       4        b      * (not valid)
                     5       5        c      # (not valid)
                     6       6        d      ?

                     hex     char     interpretation
                     e0      +        (used in wildcarding)
step_num            Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
```

<a id="pdf-page-108"></a>

## PDF page 108

Source: SPI-SYN24; PDF page 108; extracted characters: 2253.

```text
Format G:

For condition 18 (if holiday) and 23 (service hours), the following fields are contained in the message.

     7   6   5   4   3   2   1   0   7   6   5   4  3    2  1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
        stype17 or         -     c                   -                        cond                          table
         stype-18
     -       cmp                 -                     -             -       -                 -                       -
                                 dest                                         step-num                          var_t
     v_t                       -                                       -                                       -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -

stype-17 or            goto step or goto vector
stype-18
c                      1=this step is commented out
dest                   destination.  Step number to go to (1-32) if stype-17.
                       Vector to go to (1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later) if
                       stype-18
table                  holiday table number in which to check holiday: 1-10 (pre-CM 3.0), 1-99 (CM 3.0-
                       CM5.2), 1-999 (CM6.0 and later); comparator is 7 or 8 only
cmp                      Comparators
                         1   >   (not valid)
                         2   <   (not valid)
                         3   =  (not valid)
                         4   <>  (not valid)
                         5   >= (not valid)
                         6   <= (not valid)
                         7   in (table)
                         8   not-in (table)
var_t                  Variable threshold: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5 (for
                       comparator 1-8) (CM 3.0 and later)
step_num               Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
```

<a id="pdf-page-109"></a>

## PDF page 109

Source: SPI-SYN24; PDF page 109; extracted characters: 3692.

```text
3.3.21.7                     Disconnect


     7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0
         stype-7           -     c                    -                           -                              -
     -         -                 -                 var_annc           -       -                  -                       -
           -               -               -                -               -               -                -               -
           -               -               -                -               -               -                -               -
          d1              d2               d3              d4              d5               d6              d7              d8
          d9              d10             d11             d12              d13             d14             d15              d16
           -               -               -                -               -               -                -               -

stype-7                         disconnect
c                               1=this step is commented out
var_annc                        Variable announcement: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5
                                (CM 3.0 and later)
d1-d15 (< language              announcement extension (packed decimal where 0= null or "none" and
24)                             hex a is digit 0).

d1-d16 (>= language
24)


3.3.21.8                     Busy


     7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0
         stype-8           -     c                    -                           -                              -
     -         -                 -                      -             -       -                  -                       -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -

stype-8     busy
c           1=this step is commented out


3.3.21.9                     Stop


     7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0
         stype-9           -     c                    -                           -                              -
     -         -                 -                      -             -       -                  -                       -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -
           -               -                -               -               -                -               -               -

stype-9     stop
c           1=this step is commented out
```

<a id="pdf-page-110"></a>

## PDF page 110

Source: SPI-SYN24; PDF page 110; extracted characters: 3073.

```text
3.3.21.10                   Collect Digits


     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
         stype-11          -     c                 -                             -                         no_digits
     -         -               var                var_annc           -       -               type                  subtype
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
          d1              d2              d3              d4              d5              d6              d7              d8
          d9             d10             d11             d12             d13             d14              d15             d16
           -               -               -               -               -               -               -               -

stype-11                      collect digits
c                             1=this step is commented out
no_digits                     number of digits to collect (1-16). It is used if the type is 5 (digits)
var                           variable: 1-26 for variable A-Z, where 0="none",
var_annc                      Variable announcement: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5
                              (CM 3.0 and later)
type                          5=digits, 6=special digits
subtype                       4=ced, 5=cdpd; only valid with type=6
d1-d15 (< language            announcement extension (packed decimal where 0= "none" and hex a is
24)                           digit 0); only valid with type=5.

d1-d16 (>=
language 24)


3.3.21.11                   Route To Digits


     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
         stype-12        cov     c                   -                           -                             -
     -         -                 -                     -             -       -                 -                       -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -

                                         stype-12       route-to digits
                                         cov            with coverage, 0=no, 1=yes
                                         c              1=this step is commented out
```

<a id="pdf-page-111"></a>

## PDF page 111

Source: SPI-SYN24; PDF page 111; extracted characters: 3290.

```text
3.3.21.12                   Messaging Split


     7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0
        stype-13          -     c                   -                                             dest
     s        -                 -                     -             -       -                -                   subtype
                                  -                                              -                            var_ext
     v_e                      -                                       -                                      -
          d1             d2              d3              d4              d5             d6              d7              d8
          d9             d10            d11             d12             d13             d14             d15            d16
           -              -               -               -               -              -               -               -

stype-13                  messaging split/skill
c                         1=this step is commented out
dest                      destination.  Split or skill 1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000
                          (CM6.0 and later). For s=1 (EAS only), skill = 1, 2, or 3.
s                         0=specific skill, 1=VDN skill preference (EAS only)
subtype                     1   extension
                            2   active
                            3   latest

var_ext                   Variable Extension: 1-26 for variable A-Z (CM 3.1 and later), 27-31 for VDN variable
                          V1-V5 (CM 3.1 and later), 0 when "d1-d8" contains value.
d1-d15 (<                 the "for extension" parameter (packed decimal where hex a is digit 0). Will be
language 24)              empty unless subtype is 1 (extension).

d1-d16 (>=
language 24)


3.3.21.13                   Adjunct Routing


     7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0
        stype-14          -     c                   -                          -                             -
     -        -                 -                     -             -       -                -                       -
                                  -                                              -                            var_link
      v_l                     -                                       -                                      -
          d1             d2              d3              d4              d5              -               -               -
           -              -               -               -               -              -               -               -
           -              -               -               -               -              -               -               -

stype-       adjunct route
14
c            1=this step is commented out
var_link     Variable Link: 1-26 for variable A-Z (CM 3.1 and later), 27-31 for VDN variable V1-V5 (CM 3.1
             and later), 0 when "d1-d5" contains value.
d1-d5        the extension (G3V8-G3V10) or 1-digit to 2-digit link ID (G3V11 and later) of the adjunct link
             (packed decimal where 0= null and hex a is digit 0)
```

<a id="pdf-page-112"></a>

## PDF page 112

Source: SPI-SYN24; PDF page 112; extracted characters: 4202.

```text
3.3.21.14                   Converse


     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
         stype-15         pri    c                   -                                             dest
     s         -              var-1                  var-2           -       -                 -                       -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
           -            dtype1            d3              d4              d5              d6              d7              d8
           -            dtype2           d11             d12             d13             d14              d15             d16
           -               -               -               -               -               -               -               -

stype-15      converse-on split/skill
pri           0=low, 1=medium, 2=high, 3=top
c             1=this step is commented out
dest          Destination.  Split or skill 1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000 (CM6.0 and
              later). For s=1 (EAS only), skill = 1, 2, or 3.
s             0=specific skill, 1=VDN skill preference (EAS only)
var-1         Variable: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5 (dtype1 = 7)
var-2         Variable: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5 (dtype2 = 7)
dtype1        The first passing digits type, 0=none, 1=string of digits, 2=vdn, 3=ani, 4=collected digits,
              5=qpos, 6=ewt, 7=var-1
d3-d8         The first digits to pass (packed decimal where 0 is null, hex a is digit 0, hex b is *, hex c, #, is
              allowed as the first and only digit)
dtype2        The second passing digits type, 0=none, 1=string of digits, 2=vdn, 3=ani, 4=collected digits,
              5=qpos, 6=ewt, 7=var-2
d11-d16       The second digits to pass (packed decimal where 0 is null, hex a is digit 0, hex b is *, hex c, #,
              is allowed as the first and only digit)

3.3.21.15                   Consider


     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
         stype-19         pri    c                   -                           -                         threshold
     s         -            dest_type                  -             -       -                 -                       -
                                 dest                                              -                         var_location
      v_l               var_adjust_by                                  -                                       -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -
           -               -               -               -               -               -               -               -

stype-19             consider
pri                  Priority 0=low, 1=med, 2=high, 3=top
c                    1=this step is commented out
threshold            Amount to adjust by, 0-100
s                    0=specific split/skill (if dest_type=0), 1=VDN skill preference (EAS only, and if
                     dest_type=0)
dest_type            0=split/skill or VDN preference, 2=location
dest                 If dest_type=0, then split/skill 1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000
                     (CM6.0 and later) or VDN skill preference (1, 2, or 3).
                     If dest_type=2, then location number, 1-255.
var_location         Variable Location: 1-26 for variable A-Z (CM 3.1 and later), 27-31 for VDN variable V1-
                     V5 (CM 3.1 and later), 0 when "dest" contains value.
var_adjust_by        . Variable Adjust By: 1-26 for variable A-Z (CM 3.1 and later), 27-31 for VDN variable V1-
                     V5 (CM 3.1 and later), 0 when "threshold" contains value.
```

<a id="pdf-page-113"></a>

## PDF page 113

Source: SPI-SYN24; PDF page 113; extracted characters: 2182.

```text
3.3.21.16                     Reply


     7   6   5    4   3   2    1   0   7   6    5   4   3    2   1   0    7   6   5   4    3   2   1    0   7   6   5    4   3   2    1   0
         stype-20           -      c                  -                               -                                -
     -          -             dest_type                    -              -       -                   -                        -
           -                -                 -                -                -                -                -                 -
           -                -                 -                -                -                -                -                 -



                                           stype-20         reply-best
                                           c                1=this step is commented out
                                           dest_type        1 (best)

3.3.21.17                     Return


     7   6   5    4   3   2    1   0   7    6   5   4   3    2   1   0    7   6   5   4    3   2   1    0   7   6   5    4   3   2    1   0
         stype-21           -      c                    -                             -                                -
     -          -                  -                       -              -       -                  -                         -
           -                 -                -                -                -                -                -                 -
           -                 -                -                -                -                -                -                 -
           -                 -                -                -                -                -                -                 -
           -                 -                -                -                -                -                -                 -
           -                 -                -                -                -                -                -                 -

                                            stype-21       return
                                            c              1=this step is commented out
```

<a id="pdf-page-114"></a>

## PDF page 114

Source: SPI-SYN24; PDF page 114; extracted characters: 1911.

```text
3.3.21.18                  Set


    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
        stype-22          -    c                   -                          -                            -
    -     operator              -                    -             -      -
                                  -                                             -                           variable
     var                 operand-1                              operand-2                                  -
         d1              d2             d3              d4              d5             d6              d7             d8
         d9             d10             d11            d12             d13            d14             d15             d16
          -               -              -               -              -               -              -               -

stype-22         set
c                1=this step is commented out
variable         0 for digits, 1-26 for variable A-Z
operand-1        0 for digits, 1-26 for variable A-Z, 27-31 for VDN variable V1-V5, 32 for none
operand-2        0 for digits, 1-26 for variable A-Z, 27-31 for VDN variable V1-V5, 32 for none, 33 for string
                 of digits
d1-d16           digits to pass as follows:

                   hex    char     hex    char
                   0      null     7      7
                   1      1        8      8
                   2      2        9      9
                   3      3        a      0
                   4      4        b      *
                   5      5        c      +
                   6      6        d      -


operator           1   ADD
                   2   SUB
                   3   MUL
                   4   DIV
                   5   CATR
                   6   CATL
                   7   MOD70
                   8   SEL
```

<a id="pdf-page-115"></a>

## PDF page 115

Source: SPI-SYN24; PDF page 115; extracted characters: 1924.

```text
       3.3.22       CHGVEC20 AND CHGVEC24
The CHGVEC20 - Change Vector Parameters message is a variable-length message sent by the
reporting adjunct based on the "steps" field.  It is a request to change the vector steps of the specified
vector.  The expected response is an RCODE20 message. The first 5 bytes are always sent and will be
the same for all messages sent for a single vector.  Multiple messages will be sent for large vectors.

Vectors can have 99 steps per vector. The number of steps sent per message varies based on the
message.

The CHGVEC message has the same steps as the VECTOR message. See section 3.3.21 for the layout
of each step type.

3.3.22.1                   CHGVEC20 (New CM3.1)


                                                             Switch    Vect   Skill
                                             First Release   CM3.1     y      y/n
                                             Last Release    CM6.3

The reporting adjunct will send 9 steps per message, with up to 11 messages to send all 99 steps.

For CM6.0 and later, if a CHGVEC20 is sent with a check step with a preference level other than “all-
levels” and the SPI language is prior to 23, the request will be denied (rcode=43).



    7   6   5   4   3  2   1   0   7   6  5   4   3   2   1  0   7   6   5   4   3  2   1   0   7   6  5   4   3   2   1   0
             CHVEC20                           tag                  / / /                        vector
    m      / / /       steps

opcode      CHGVEC20 = 51 (0x33)
tag         message tag, 0-255 (it will be returned in the switch response message)
vector      vector number, 1-999 (G3V8-CM2), 1-2000 (CM3.1-CM5.2), 1-8000 (CM6.0 and later)
m           m=1, more steps for this vector will be sent in a subsequent vector, m=0, this is the last
            message for this vector
steps       number of steps (N) 0-9. This is the number of steps in this message.
```

<a id="pdf-page-116"></a>

## PDF page 116

Source: SPI-SYN24; PDF page 116; extracted characters: 1048.

```text
3.3.22.2                   CHGVEC24 (New CM7.0)


                                                              Switch   Vect   Skill
                                              First Release   CM7.0    y      y/n
                                              Last Release

The reporting adjunct will send 8 steps per message, with up to 13 messages to send all 99 steps.

7  6   5   4   3   2  1   0   7   6   5  4   3   2   1   0  7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0
       CHGVEC24                           tag                  / / /                        vector
m     / / /       steps
opcode      CHGVEC24 = 68 (0x44)
tag         message tag, 0-255 (it will be returned in the switch response message)
vector      vector number, 1-999 (G3V8-CM2), 1-2000 (CM3.1-CM5.2), 1-8000 (CM6.0 and later)
m           m=1, more steps for this vector will be sent in a subsequent vector, m=0, this is the last
            message for this vector
steps       number of steps (N) 0-8. This is the number of steps in this message.
```

<a id="pdf-page-117"></a>

## PDF page 117

Source: SPI-SYN24; PDF page 117; extracted characters: 922.

```text
       3.3.23       REQLIST5 (New G3V6)


                                                              Switch    Vect   Skill
                                              First Release   G3V6      y      y/n
                                              Last Release

The Request List message is sent by the reporting adjunct to the switch to request a list of non-empty
entities of a certain type and their modification numbers. The expected response is an ADMLIST20 with
the entities or an RCODE20 1.

                    7   6   5  4   3   2   1   0   7  6   5   4   3   2   1  0   7   6   5   4   3   2  1   0
                            REQLIST5                           tag                   / / / /       obj type

opcode        REQLIST5 = 35 (0x23)
tag           message tag, 0-255 (it will be returned in the switch response message)
obj type      type of object requested: 0=vectors, 1=VDNs (measured by CMS)
```

<a id="pdf-page-118"></a>

## PDF page 118

Source: SPI-SYN24; PDF page 118; extracted characters: 2659.

```text
       3.3.24       ADMLIST20 (New CM3.1)


                                                               Switch    Vect   Skill
                                              First Release    CM3.1     y      y/n
                                              Last Release

The Administration list message is sent by switch to the reporting adjunct in response to a REQLIST5
message to indicate the non-empty entities on the switch of the requested type. For the VDN type, these
are the VDNs which are measured by the reporting adjunct only. For vectors, these are the vectors which
are non-empty (i.e., there is a name or one or more steps).

The results of this request may not fit into a single ADMLIST20 message.  In this case, the cnt field
indicates the number of items in the current message and the end bit is set for the last message in a
series.  This is a variable length message based on the cnt field.  The first ten bytes are always sent.

These messages may form very long chains.  G3V6/R3V6 supports 8000 CMS measured VDNs.  A list of
20000 VDNs will require 254 messages to be sent. A list of 999 vectors will require 13 messages. These
calculations are based on a message buffer with a size of 244 bytes.

     7  6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2  1   0
              time_tag                      ADMLIST20                                       seq num
                           seq num (cont)                                     tot siz                          tag
         / / / /      obj type      e             cnt              /                           obj id 1
               mod 1
                                                               .  .  .
     /                          obj id N                                      mod N

time_tag       seconds past minute when messages was formed, 0-59
opcode         ADMLIST20 = 200 (0xc8)
seq num        sequence number, 0-0xffff ffff
tot siz        total size in bytes, 1-255
tag            message tag, 0-255 (as contained in the request message).
obj type       type of object which is listed: 0=vectors, 1=VDNs
e              end bit, set when this is the last message of the set needed to satisfy the request
cnt            number of objects listed in this message, 1-77
obj id 1-N     the identifying number for the object

                 obj type     entity        obj id values
                 0            vector        1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
                 1            VDN (iln)     1-32767
mod 1-N        modification number for the object
```

<a id="pdf-page-119"></a>

## PDF page 119

Source: SPI-SYN24; PDF page 119; extracted characters: 1120.

```text
       3.3.25      REQNAM20 (New CM3.1)


                                                            Switch   Vect   Skill
                                            First Release   CM3.1    y      y/n
                                            Last Release

The Request NAME message is sent by the reporting adjunct to CM to request a list of objects. The
expected response is an ADMNAM.

    7   6   5  4   3   2   1  0   7   6  5   4   3   2  1   0   7  6   5   4   3  2   1   0  7   6   5   4  3   2   1  0
            REQNAM20                          tag                      / / / / / / /      m     / / /    v  t   h   d  a

       opcode     REQNAM20 = 48 (0x30)
       tag        message tag, 1-255 (it will be returned in the switch ADMNAM response messages)
       mode       mode; 0 = all names; 1 = changed names
       v          vector names; 1 = report vector names
       t          trunk group names; 1 = report trunk group names
       h          hunt group names; 1 = report hunt group names
       d          VDN names; 1 = report VDN names
       a          agent names; 1 = report agent names
```

<a id="pdf-page-120"></a>

## PDF page 120

Source: SPI-SYN24; PDF page 120; extracted characters: 2522.

```text
       3.3.26       ADMNAM20 and ADMNAM24
The Administration NAME message is sent by switch to the reporting adjunct in response to a
REQNAM20 message to provide switch data for the requested object type. The information for each
returned object contains: object-id, name1-object-data-length, name1-object-data, name2-object-data-
length and name2-object-data.

The end bit is set for the last message in a series.  This is a variable length message based on the data-
len-name1 and data-len-name2 fields.  The first eight bytes are always sent.

3.3.26.1                    ADMNAM20 (New CM3.1)


                                                                 Switch    Vect    Skill
                                                First Release    CM3.1     y       y/n
                                                Last Release     CM6.3



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2    1   0   7   6   5   4   3   2   1   0
               time_tag                      ADMNAM20                                           seq num
                            seq num (cont)                                       tot siz                           tag
     e   r   n   n     obj type
             1   2


                                                    for vector, trunk, hunt and VDN
     b                             obj id                                    name 1 len M                    name 1 byte 1
            name 1 byte 2                   name 1 byte 3                         * * *                      name 1 byte M
            name 2 len N                   name 2 script tag                name 2 byte 1                    name 2 byte 2
            name 2 byte 3                         * * *                     name 2 byte N



                                                               for agent
      pnumber             p1              p2              p3               p4              p5              p6              p7
          p8              p9              p10             p11             p12             p13             p14             p15
            name 1 len M                    name 1 byte 1                   name 1 byte 2                    name 1 byte 3
                 * * *                      name 1 byte M                    name 2 len N                  name 2 script tag
            name 2 byte 1                   name 2 byte 2                   name 2 byte 3                         * * *
            name 2 byte N
```
