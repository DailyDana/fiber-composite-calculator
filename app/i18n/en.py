"""English strings."""

STRINGS: dict[str, str] = {
    # --- general ---
    "app.title": "Fiber Composite Calculator",
    "app.caption": "Step-by-step composite calculations with the relations of Callister & Rethwisch, chapter 16",
    "list.and": " and ",
    "lang.label": "Dil / Language",
    "nav.compare": "Compare and rank",
    "nav.continuous": "Continuous fibers",
    "nav.discontinuous": "Discontinuous fibers",
    "nav.random_particle": "Orientation and particles",
    "about.title": "About",
    "about.body": (
        "Relations follow Callister & Rethwisch, *Materials Science and Engineering: An "
        "Introduction*, chapter 16. Units: stress MPa, modulus GPa, length mm. Typical material "
        "values are approximate and not design allowables."
    ),
    "steps.title": "Step-by-step calculation",
    "unit.mpa": "MPa",
    "unit.gpa": "GPa",
    "unit.mm": "mm",
    "error.row": "Row {row}: {error}",
    "error.input": "Input error: {error}",
    # --- fiber types ---
    "fiber.glass": "glass",
    "fiber.carbon": "carbon",
    "fiber.aramid": "aramid",
    "fiber.other": "other",
    "regime.long": "l > lc",
    "regime.short": "l < lc",
    # --- compare page ---
    "cmp.title": "Compare and rank composites",
    "cmp.intro": (
        "Ranks aligned discontinuous-fiber composites by their strength in the direction of "
        "reinforcement and explains the effect of fiber type, volume fraction, fiber strength, "
        "mean fiber length and critical length one by one. Edit the table directly; rows can be "
        "added and deleted."
    ),
    "cmp.preset": "Preset",
    "preset.kk16_2": "Concept Check 16.2 (Callister)",
    "preset.blank": "Blank template (one row)",
    "cmp.load": "Load",
    "col.name": "Composite",
    "col.fiber": "Fiber type",
    "col.vf": "Vf",
    "col.sigma_f": "σf* (MPa)",
    "col.l": "l (mm)",
    "col.lc": "lc (mm)",
    "col.rank": "Rank",
    "col.ratio": "l/lc",
    "col.regime": "Regime",
    "col.eff": "Length efficiency η",
    "col.fiber_term": "Fiber term (MPa)",
    "col.matrix_term": "Matrix term (MPa)",
    "col.strength": "σcd* (MPa)",
    "col.near": "l ≥ 15·lc",
    "cmp.matrix_toggle": "Include the matrix contribution (σm' known)",
    "cmp.matrix_value": "Common matrix stress σm' (MPa)",
    "cmp.matrix_help": (
        "σm' is the matrix stress at the moment the fibers fail (not the matrix tensile "
        "strength). The same matrix is assumed for every composite."
    ),
    "cmp.results": "Results",
    "cmp.metric_top": "Highest strength",
    "cmp.metric_order": "Ranking",
    "cmp.metric_threshold": "σm' that would reorder",
    "cmp.metric_threshold_none": "none",
    "cmp.charts": "Charts",
    "cmp.interpretation": "Interpretation",
    "cmp.need_rows": "Enter at least one valid composite row.",
    "cmp.report": "Report",
    "rep.course": "Course",
    "rep.course_default": "Materials Science",
    "rep.title": "Report title",
    "rep.title_default": "Strength Ranking of Aligned Discontinuous-Fiber Composites",
    "rep.question": "Question",
    "rep.question_default": (
        "Rank the strengths of the four hypothetical aligned discontinuous fiber-reinforced "
        "composites A to D in the direction of reinforcement from highest to lowest and justify "
        "the ranking, taking fiber type, fiber volume fraction, fiber strength, mean fiber "
        "length and critical length into account (Callister, Concept Check 16.2)."
    ),
    "rep.student": "Name",
    "rep.number": "Student ID",
    "rep.date": "Date",
    "rep.footer_toggle": "Print the program name in the footer",
    "rep.download": "Download PDF report",
    "rep.filename": "composite_report.pdf",
    # --- report sections ---
    "rep.sec.question": "1. Question and given data",
    "rep.sec.theory": "2. Theoretical background",
    "rep.sec.calc": "3. Calculations",
    "rep.sec.results": "4. Results and charts",
    "rep.sec.discussion": "5. Discussion",
    "rep.sec.verification": "6. Verifying the ranking",
    "rep.sec.conclusion": "7. Conclusion",
    "rep.sec.references": "Reference",
    "rep.given": "Given",
    "rep.theory.p1": (
        "In an aligned discontinuous-fiber composite the load is transferred from the matrix to "
        "the fibers by shear at the interface. The shortest length at which a fiber can be "
        "loaded up to its fracture strength is the critical length: lc = σf*·d / (2·τc), where d "
        "is the fiber diameter and τc the smaller of the fiber–matrix bond strength and the "
        "matrix shear yield strength."
    ),
    "rep.theory.p2": (
        "For l > lc the strength in the direction of reinforcement is σcd* = σf*·Vf·(1 − lc/2l) "
        "+ σm'·(1 − Vf); for l < lc it is σcd*' = (l·τc/d)·Vf + σm'·(1 − Vf). σm' is the matrix "
        "stress when the fibers fail."
    ),
    "rep.theory.p3": (
        'This report calls the factor (1 − lc/2l) the "length efficiency" η: the share of the '
        "fiber strength that can be used. It is 0.5 at l = lc and approaches 1 as l/lc grows. "
        "Fibers with l ≥ 15·lc behave practically as continuous fibers."
    ),
    "rep.calc.intro": "For each composite the length regime is checked first, then the strength is computed.",
    "rep.calc.composite": "Composite {name} ({fiber} fiber)",
    "rep.results.table": "Table 2. Results (sorted by strength)",
    "rep.given.table": "Table 1. Given composite properties",
    "rep.fig": "Figure {n}. {title}",
    "rep.references.callister": (
        "W. D. Callister, D. G. Rethwisch, Materials Science and Engineering: An Introduction, "
        "Wiley, chapter 16: Composites."
    ),
    "rep.footer": "Prepared with fiber-composite-calculator",
    "rep.page": "Page {n}",
    # --- interpretation section titles ---
    "sec.ranking": "Ranking",
    "sec.fiber": "Fiber type and fiber strength",
    "sec.vf": "Fiber volume fraction",
    "sec.length": "Mean fiber length and critical length",
    "sec.matrix": "Matrix contribution",
    "sec.conclusion": "Conclusion",
    # --- interpretation sentences ---
    "rank.order": (
        "Ranking by strength in the direction of reinforcement (highest to lowest): {order}. "
        "No matrix data is given, so the ranking uses the fiber term σf*·Vf·(1 − lc/2l)."
    ),
    "rank.order_with_matrix": (
        "Ranking by strength in the direction of reinforcement (highest to lowest): {order}. "
        "Both the fiber and the matrix terms are included."
    ),
    "fiber.single": "all composites use {type} fibers, so fiber type makes no difference to the ranking.",
    "fiber.group": "the {type}-fiber composites ({names}) have a fiber strength of {hi} MPa.",
    "fiber.group_range": "the {type}-fiber composites ({names}) have fiber strengths of {lo}–{hi} MPa.",
    "fiber.ratio": (
        "{top} fiber is {ratio} times as strong as {low} fiber. The fiber term is proportional "
        "to σf*, so this difference carries straight into the composite strength."
    ),
    "fiber.dominant": (
        "therefore all {type}-fiber composites ({names}) are at the top of the ranking; fiber "
        "type is the first deciding factor."
    ),
    "fiber.overtaken": (
        "fiber type alone does not decide, however: {upper} with {upper_type} fibers "
        "(Vf = {upper_vf}) outranks {lower}, which uses the stronger {lower_type} fiber "
        "(Vf = {lower_vf}). What decides is the product σf*·Vf."
    ),
    "vf.rule": (
        "within one fiber type the fiber term σf*·Vf·η is proportional to Vf, so the fiber "
        "volume fraction is the second deciding factor."
    ),
    "vf.follows": (
        "comparing {hi} (Vf = {hi_vf}) with {lo} (Vf = {lo_vf}), the volume fractions differ by "
        "a factor of {vf_ratio} and the fiber terms by {str_ratio}; almost the whole gap comes "
        "from the volume fraction."
    ),
    "vf.follows_other": (
        "comparing {hi} (Vf = {hi_vf}) with {lo} (Vf = {lo_vf}), the volume fractions differ by "
        "a factor of {vf_ratio} and the fiber terms by {str_ratio}; part of the gap comes from "
        "differences in fiber strength or length efficiency."
    ),
    "vf.equal": (
        "{hi} and {lo} have the same volume fraction (Vf = {hi_vf}); the gap between them comes "
        "from fiber strength or length efficiency."
    ),
    "vf.against": (
        "{hi} is stronger than {lo} (Vf = {lo_vf}) despite its lower volume fraction "
        "(Vf = {hi_vf}), because of a higher fiber strength or length efficiency."
    ),
    "vf.no_pairs": (
        "there is only one composite per fiber type, so the volume fraction cannot be compared "
        "within a type; it acts through the product σf*·Vf."
    ),
    "len.all_long": (
        "in every composite the mean fiber length exceeds the critical length (l > lc; smallest "
        "ratio l/lc = {ratio}, {name}). The fibers can be loaded to their fracture strength and "
        "σcd* = σf*·Vf·(1 − lc/2l) + σm'·(1 − Vf) applies."
    ),
    "len.short": (
        "for {names}, l < lc: the fibers pull out of the matrix before they can fail, the length "
        "efficiency drops below 50% and σcd*' = (l·τc/d)·Vf + σm'·(1 − Vf) is used."
    ),
    "len.efficiency": "the length efficiency η = 1 − lc/2l ranges from {lo_eff} ({lo}) to {hi_eff} ({hi}).",
    "len.longest": (
        "the longest fibers are in {name} (l = {l} mm), but efficiency depends on the ratio "
        "l/lc, not on the absolute length. For {name}, lc = {lc} mm, so l/lc = {ratio}."
    ),
    "len.no_order_change": (
        "the efficiencies are close, so length does not change the ranking: ranking by σf*·Vf "
        "alone also gives {product_order}. Length lowers the strengths by only a few percent."
    ),
    "len.no_order_change_wide": (
        "the efficiencies differ noticeably but length still does not change the ranking: "
        "ranking by σf*·Vf alone also gives {product_order}."
    ),
    "len.order_change": (
        "length changes the ranking: by σf*·Vf alone it would be {product_order}, with the "
        "length efficiency it becomes {fiber_order}."
    ),
    "len.near_continuous_some": (
        "the composites whose fibers reach l ≥ 15·lc ({near}) behave practically as continuous-fiber "
        "composites; {far} stays below that limit, so the discontinuity matters more."
    ),
    "len.near_continuous_all": "every composite has l ≥ 15·lc; the fibers behave practically as continuous ones.",
    "len.near_continuous_none": "no composite reaches l ≥ 15·lc; the discontinuity matters in all of them.",
    "mat.unknown": (
        "no matrix strength is given, so the fiber term is used. The matrix term σm'·(1 − Vf) "
        "favours composites with a lower volume fraction, so whether adding it could change "
        "the ranking has to be checked."
    ),
    "mat.included": (
        "a common matrix stress σm' = {value} MPa is assumed and the matrix term σm'·(1 − Vf) is "
        "added to every composite."
    ),
    "mat.changed_order": (
        "the matrix term changed the ranking: {fiber_order} on the fiber term alone became {order}."
    ),
    "mat.threshold": (
        "the smallest common matrix stress that would swap two composites is "
        "σm' = Δ(fiber term) / ΔVf ≈ {value} MPa (pair {upper}–{lower})."
    ),
    "mat.unrealistic": (
        "polymer matrices typically have tensile strengths below 100 MPa and σm' cannot exceed "
        "them. The threshold of {value} MPa is far above any realistic value, so the "
        "ranking is independent of the matrix; this verifies the ranking."
    ),
    "mat.sensitive": (
        "this threshold is close to realistic matrix stresses (below {limit} MPa); without "
        "matrix data the ranking should not be taken as certain."
    ),
    "mat.no_flip": (
        "no pair of composites can swap because of the matrix term: no composite ranked higher "
        "has a larger volume fraction than one below it, so the matrix only widens the gaps. "
        "The ranking is independent of the matrix."
    ),
    "concl.summary": (
        "the ranking by strength in the direction of reinforcement is {order}. The highest "
        "strength is {top} ({top_value} MPa), the lowest {bottom} ({bottom_value} MPa)."
    ),
    "concl.driver_type_then_vf": "fiber type (fiber strength) decides first, the fiber volume fraction within a type.",
    "concl.driver_vf": "all composites share a fiber type, so volume fraction and length efficiency decide.",
    "concl.driver_product": "no single factor decides; the product of fiber strength and volume fraction (σf*·Vf) does.",
    "concl.length_minor": "fiber length is a secondary factor: the efficiencies do not change the ranking.",
    "concl.length_major": "fiber length (the ratio l/lc) is strong enough to change the ranking.",
    "concl.matrix_robust": "the matrix contribution cannot change the ranking at realistic values.",
    "concl.matrix_sensitive": "the matrix contribution could change the ranking; matrix data matters.",
    # --- step by step ---
    "step.regime_long": "Regime check: l > lc, the σcd* relation applies",
    "step.regime_short": "Regime check: l < lc, the σcd*' relation applies (τc/d = σf*/2lc)",
    "step.efficiency": "Length efficiency",
    "step.fiber_term": "Fiber term",
    "step.matrix_term": "Matrix term",
    "step.total": "Composite strength",
    "step.ecl": "Longitudinal modulus (isostrain)",
    "step.ect": "Transverse modulus (isostress)",
    "step.load_ratio": "Fiber-to-matrix load ratio",
    "step.sigma_cl": "Longitudinal tensile strength",
    "step.forces": "Load sharing",
    "step.stresses": "Stresses in fiber and matrix",
    "step.strain": "Strain",
    "step.lc": "Critical length",
    "step.ecd": "Modulus with orientation efficiency",
    "step.particle_upper": "Upper bound",
    "step.particle_lower": "Lower bound",
    "step.density": "Composite density",
    # --- charts ---
    "chart.strength.title": "Strength in the direction of reinforcement",
    "chart.strength.y": "Strength σcd* (MPa)",
    "chart.strength.fiber": "Fiber term",
    "chart.strength.matrix": "Matrix term",
    "chart.ratio.title": "Mean fiber length / critical length",
    "chart.ratio.x": "l / lc",
    "chart.ratio.critical": "l = lc",
    "chart.ratio.continuous": "l = 15·lc (practically continuous)",
    "chart.eff.title": "Length efficiency curve",
    "chart.eff.x": "l / lc",
    "chart.eff.y": "Length efficiency η",
    "chart.mix.title": "Rule of mixtures: elastic modulus",
    "chart.mix.x": "Fiber volume fraction Vf",
    "chart.mix.y": "Elastic modulus (GPa)",
    "chart.mix.long": "Longitudinal Ecl (isostrain)",
    "chart.mix.trans": "Transverse Ect (isostress)",
    "chart.mix.current": "Selected Vf",
    "chart.sl.title": "Strength versus fiber length",
    "chart.sl.x": "Fiber length l (mm)",
    "chart.sl.y": "Strength σcd (MPa)",
    "chart.sl.current": "Selected l",
    "chart.orient.title": "Effect of fiber orientation on the elastic modulus",
    "chart.orient.x": "Elastic modulus (GPa)",
    "chart.particle.title": "Particle composite: elastic modulus bounds",
    "chart.particle.x": "Particle volume fraction Vp",
    "chart.particle.upper": "Upper bound",
    "chart.particle.lower": "Lower bound",
    # --- continuous page ---
    "cont.title": "Continuous aligned fibers",
    "cont.intro": (
        "Computes the longitudinal (isostrain) and transverse (isostress) moduli, the load "
        "sharing and the longitudinal tensile strength. Defaults are Callister Example 16.1 "
        "(glass/polyester)."
    ),
    "cont.fill": "Fill from a typical material",
    "cont.fiber": "Fiber",
    "cont.matrix": "Matrix",
    "cont.apply": "Apply values",
    "cont.reset": "Back to Example 16.1",
    "cont.ef": "Fiber modulus Ef (GPa)",
    "cont.em": "Matrix modulus Em (GPa)",
    "cont.vf": "Fiber volume fraction Vf",
    "cont.sigma_f": "Fiber strength σf* (MPa)",
    "cont.sigma_m": "Matrix stress at fiber failure σm' (MPa)",
    "cont.load": "Load sharing (optional)",
    "cont.stress": "Applied longitudinal stress σc (MPa)",
    "cont.area": "Cross-sectional area A (mm²)",
    "cont.ecl": "Ecl (longitudinal)",
    "cont.ect": "Ect (transverse)",
    "cont.ratio": "Ff / Fm",
    "cont.sigma_cl": "σcl* (longitudinal strength)",
    "cont.ff": "Fiber load Ff",
    "cont.fm": "Matrix load Fm",
    "cont.sf": "Fiber stress σf",
    "cont.sm": "Matrix stress σm",
    "cont.strain": "Strain ε",
    "material.e_glass": "E-glass",
    "material.carbon_sm": "Carbon (standard modulus)",
    "material.aramid": "Aramid (Kevlar 49)",
    "material.epoxy": "Epoxy",
    "material.polyester": "Polyester",
    # --- discontinuous page ---
    "disc.title": "Discontinuous aligned fibers",
    "disc.intro": (
        "Computes the critical length, length efficiency and strength in the direction of "
        "reinforcement for one composite, and shows how strength changes with fiber length."
    ),
    "disc.lc_mode": "Critical length",
    "disc.lc_direct": "Enter directly",
    "disc.lc_compute": "Compute from σf*, d and τc",
    "disc.sigma_f": "Fiber strength σf* (MPa)",
    "disc.vf": "Fiber volume fraction Vf",
    "disc.l": "Mean fiber length l (mm)",
    "disc.lc": "Critical length lc (mm)",
    "disc.d": "Fiber diameter d (µm)",
    "disc.tau": "Interfacial shear strength τc (MPa)",
    "disc.sigma_m": "Matrix stress σm' (MPa)",
    "disc.strength": "σcd*",
    "disc.ratio": "l / lc",
    "disc.eff": "Length efficiency η",
    "disc.near": "l ≥ 15·lc: behaves practically as a continuous fiber.",
    "disc.short": "l < lc: the fibers pull out before failing; strength drops sharply.",
    "disc.between": "lc < l < 15·lc: the discontinuity is felt; length efficiency {eff}.",
    # --- orientation and particle page ---
    "rp.title": "Fiber orientation and particle composites",
    "rp.orient": "Fiber orientation efficiency (K)",
    "rp.orient_intro": "Effect of orientation on the modulus with Ecd = K·Ef·Vf + Em·Vm.",
    "rp.particle": "Large-particle composite",
    "rp.particle_intro": (
        "Upper and lower rule-of-mixtures bounds. Defaults are a copper matrix with tungsten "
        "particles (Callister)."
    ),
    "rp.k.aligned_par": "Aligned, parallel to fibers (K = 1)",
    "rp.k.aligned_perp": "Aligned, perpendicular to fibers (K = 0)",
    "rp.k.random_2d": "Random in a plane (K = 3/8)",
    "rp.k.random_3d": "Random in three dimensions (K = 1/5)",
    "rp.ep": "Particle modulus Ep (GPa)",
    "rp.em": "Matrix modulus Em (GPa)",
    "rp.vp": "Particle volume fraction Vp",
    "rp.upper": "Upper bound Ec(u)",
    "rp.lower": "Lower bound Ec(l)",
    "rp.k_note": (
        "Note: K = 0 in the transverse direction is a crude approximation that leaves only the "
        "matrix; for continuous fibers the isostress relation gives a better transverse modulus."
    ),
}
