# Formulas

Every number the app shows comes from one of the relations below. Section numbers refer to
the composites chapter (chapter 16) of Callister & Rethwisch, *Materials Science and
Engineering: An Introduction*. Equation numbers are left out on purpose: they move between
editions and translations.

Units used throughout: stress and strength in MPa, elastic modulus in GPa, lengths in mm
(fiber diameter too), volume fractions as plain numbers between 0 and 1.

Code: `app/core/formulas.py` (single formulas), `app/core/compare.py` (ranking).

## Fiber length (section 16.4)

**Critical length**

    lc = σf* · d / (2 · τc)

σf* is the fiber tensile strength, d the fiber diameter, τc the smaller of the
fiber–matrix bond strength and the matrix shear yield strength. In the app d is entered in
µm and converted to mm.

**Practically continuous fibers.** Fibers with l ≥ 15·lc are treated as continuous. The app
flags this per composite; it does not change the formula used.

## Aligned discontinuous fibers (section 16.5)

For l > lc:

    σcd* = σf* · Vf · (1 − lc / 2l) + σm' · (1 − Vf)

For l < lc:

    σcd*' = (l · τc / d) · Vf + σm' · (1 − Vf)

σm' is the stress in the matrix when the fibers fail. It is not the matrix tensile strength.

**Length efficiency η.** The app calls the fiber factor the length efficiency (this name is
ours, not the book's):

    η = 1 − lc / 2l        for l ≥ lc
    η = l / 2lc            for l < lc

The second line is the l < lc formula rewritten with τc/d = σf*/(2·lc), which follows from the
definition of lc. This way both branches need only l and lc, and the fiber term is always
σf*·Vf·η. Both branches give η = 0.5 at l = lc, and η tends to 1 as l/lc grows.

## Ranking several composites and the matrix threshold

Composites are sorted by σcd*. Without matrix data σm' is taken as 0, so the sort is on the
fiber term F = σf*·Vf·η.

To check whether a common matrix could change that order, take two composites i above j in
the fiber-term order:

    σcd,i − σcd,j = (Fi − Fj) − σm' · (Vf,i − Vf,j)

They can only swap when Vf,i > Vf,j (the higher-ranked one has more fiber and so less matrix),
at

    σm' = (Fi − Fj) / (Vf,i − Vf,j)

The app reports the smallest such value over all pairs. If no pair can swap, the order does
not depend on the matrix at all. As a further check, when σm' is unknown the ranking is
recomputed with σm' = 100 MPa (generous for polymer matrices) and shown if unchanged.

Code: `flip_threshold` in `app/core/compare.py`.

## Continuous aligned fibers (section 16.5)

Longitudinal modulus (isostrain):

    Ecl = Em · (1 − Vf) + Ef · Vf

Transverse modulus (isostress):

    Ect = Em · Ef / ((1 − Vf) · Ef + Vf · Em)

Load ratio under longitudinal load:

    Ff / Fm = Ef · Vf / (Em · (1 − Vf))

Load split for an applied stress σc on area A: Fc = σc·A, Fm = Fc / (1 + Ff/Fm),
Ff = Fc − Fm; then σf = Ff / (Vf·A), σm = Fm / ((1 − Vf)·A) and the common strain
ε = σm / Em.

Longitudinal tensile strength:

    σcl* = σm' · (1 − Vf) + σf* · Vf

Checked against Example 16.1 (glass/polyester, Ef = 69 GPa, Em = 3.4 GPa, Vf = 0.4):
Ecl = 29.6 GPa (book: 30), Ff/Fm = 13.5, Ect = 5.5 GPa, and for 50 MPa on 250 mm²:
Ff ≈ 11 640 N, Fm ≈ 860 N, σf ≈ 116 MPa, σm ≈ 5.7 MPa.

## Fiber orientation (section 16.5)

    Ecd = K · Ef · Vf + Em · (1 − Vf)

with K = 1 for aligned fibers loaded along them, 3/8 for fibers random in a plane, 1/5 for
fibers random in three dimensions, and 0 across aligned fibers. The last one is a rough
estimate; for continuous fibers the isostress relation above is better.

## Large-particle composites (section 16.2)

Upper bound:

    Ec(u) = Em · Vm + Ep · Vp

Lower bound:

    Ec(l) = Em · Ep / (Vm · Ep + Vp · Em)

The default values are a copper matrix (110 GPa) with tungsten particles (407 GPa).

## Density

    ρc = ρf · Vf + ρm · (1 − Vf)
