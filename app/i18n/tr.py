"""Türkçe metinler."""

STRINGS: dict[str, str] = {
    # --- genel ---
    "app.title": "Elyaf Takviyeli Kompozit Hesaplayıcı",
    "app.caption": "Callister & Rethwisch, Bölüm 16 bağıntılarıyla adım adım kompozit hesapları",
    "list.and": " ve ",
    "lang.label": "Dil / Language",
    "nav.compare": "Karşılaştırma ve sıralama",
    "nav.continuous": "Sürekli elyaf",
    "nav.discontinuous": "Süreksiz elyaf",
    "nav.random_particle": "Yönlenme ve parçacık",
    "about.title": "Hakkında",
    "about.body": (
        "Bağıntılar Callister & Rethwisch, *Malzeme Bilimi ve Mühendisliği*, Bölüm 16'dan "
        "alınmıştır. Birimler: gerilme MPa, modül GPa, uzunluk mm. Tipik malzeme değerleri "
        "yaklaşıktır; tasarım değeri olarak kullanılmamalıdır."
    ),
    "steps.title": "Adım adım hesap",
    "unit.mpa": "MPa",
    "unit.gpa": "GPa",
    "unit.mm": "mm",
    "error.row": "Satır {row}: {error}",
    "error.input": "Girdi hatası: {error}",
    # --- elyaf türleri ---
    "fiber.glass": "cam",
    "fiber.carbon": "karbon",
    "fiber.aramid": "aramid",
    "fiber.other": "diğer",
    "regime.long": "l > lc",
    "regime.short": "l < lc",
    # --- karşılaştırma sayfası ---
    "cmp.title": "Kompozit karşılaştırma ve sıralama",
    "cmp.intro": (
        "Hizalanmış süreksiz elyaflı kompozitleri takviye doğrultusundaki dayanımlarına göre "
        "sıralar; elyaf türü, hacim oranı, elyaf dayanımı, ortalama elyaf uzunluğu ve kritik "
        "uzunluğun etkisini ayrı ayrı yorumlar. Tablodaki değerleri doğrudan düzenleyebilir, "
        "satır ekleyip silebilirsiniz."
    ),
    "cmp.preset": "Hazır veri",
    "preset.kk16_2": "Kavram Kontrol 16.2 (Callister)",
    "preset.blank": "Boş şablon (tek satır)",
    "cmp.load": "Yükle",
    "col.name": "Kompozit",
    "col.fiber": "Elyaf türü",
    "col.vf": "Vf",
    "col.sigma_f": "σf* (MPa)",
    "col.l": "l (mm)",
    "col.lc": "lc (mm)",
    "col.rank": "Sıra",
    "col.ratio": "l/lc",
    "col.regime": "Bölge",
    "col.eff": "Uzunluk verimi η",
    "col.fiber_term": "Elyaf terimi (MPa)",
    "col.matrix_term": "Matris terimi (MPa)",
    "col.strength": "σcd* (MPa)",
    "col.near": "l ≥ 15·lc",
    "cmp.matrix_toggle": "Matris katkısını dahil et (σm' biliniyor)",
    "cmp.matrix_value": "Ortak matris gerilmesi σm' (MPa)",
    "cmp.matrix_help": (
        "σm', elyaflar kırıldığı andaki matris gerilmesidir (matrisin çekme dayanımı değil). "
        "Tüm kompozitlerde aynı matris varsayılır."
    ),
    "cmp.results": "Sonuçlar",
    "cmp.metric_top": "En yüksek dayanım",
    "cmp.metric_order": "Sıralama",
    "cmp.metric_threshold": "Sırayı bozan σm' eşiği",
    "cmp.metric_threshold_none": "yok",
    "cmp.charts": "Grafikler",
    "cmp.interpretation": "Yorum",
    "cmp.need_rows": "En az bir geçerli kompozit satırı girin.",
    "cmp.report": "Rapor",
    "rep.course": "Ders",
    "rep.course_default": "Malzeme Bilimi",
    "rep.title": "Rapor başlığı",
    "rep.title_default": "Hizalanmış Süreksiz Elyaflı Kompozitlerin Dayanım Sıralaması",
    "rep.question": "Soru metni",
    "rep.question_default": (
        "A'dan D'ye kadar adlandırılmış dört hayali hizalanmış süreksiz elyaf takviyeli "
        "kompozitin takviye doğrultusundaki dayanımlarını en yüksekten en düşüğe doğru "
        "sıralayınız ve sıralamanın doğruluğunu gösteriniz. Yorumda elyaf türü, elyaf hacim "
        "oranı, elyaf dayanımı, ortalama elyaf uzunluğu ve kritik uzunluk dikkate alınacaktır "
        "(Callister, Kavram Kontrol 16.2)."
    ),
    "rep.student": "Ad Soyad",
    "rep.number": "Öğrenci no",
    "rep.date": "Tarih",
    "rep.footer_toggle": "Rapora program adını yaz (alt bilgi)",
    "rep.download": "PDF raporu indir",
    "rep.filename": "kompozit_rapor.pdf",
    # --- rapor bölümleri ---
    "rep.sec.question": "1. Soru ve verilenler",
    "rep.sec.theory": "2. Kuramsal arka plan",
    "rep.sec.calc": "3. Hesaplar",
    "rep.sec.results": "4. Sonuçlar ve grafikler",
    "rep.sec.discussion": "5. Yorum",
    "rep.sec.verification": "6. Sıralamanın doğruluğunun gösterilmesi",
    "rep.sec.conclusion": "7. Sonuç",
    "rep.sec.references": "Kaynak",
    "rep.given": "Verilenler",
    "rep.theory.p1": (
        "Hizalanmış süreksiz elyaflı bir kompozitte yük, matristen elyafa ara yüzeydeki kayma "
        "gerilmesiyle aktarılır. Elyafın kırılma dayanımına kadar yüklenebilmesi için gereken "
        "en küçük uzunluk kritik uzunluktur: lc = σf*·d / (2·τc). Burada d elyaf çapı, τc ise "
        "elyaf–matris bağ dayanımı ile matrisin kayma akma dayanımından küçük olanıdır."
    ),
    "rep.theory.p2": (
        "l > lc olduğunda takviye doğrultusundaki dayanım σcd* = σf*·Vf·(1 − lc/2l) + "
        "σm'·(1 − Vf) bağıntısıyla, l < lc olduğunda ise σcd*' = (l·τc/d)·Vf + σm'·(1 − Vf) "
        "bağıntısıyla hesaplanır. σm', elyaflar kırıldığı andaki matris gerilmesidir."
    ),
    "rep.theory.p3": (
        'Bu raporda (1 − lc/2l) çarpanı "uzunluk verimi" η olarak adlandırılmıştır: elyaf '
        "dayanımının ne kadarının kullanılabildiğini gösterir; l = lc'de 0,5'tir ve l/lc "
        "büyüdükçe 1'e yaklaşır. l ≥ 15·lc olan elyaflar pratikte sürekli elyaf gibi davranır."
    ),
    "rep.calc.intro": "Her kompozit için önce uzunluk bölgesi belirlenmiş, ardından dayanım hesaplanmıştır.",
    "rep.calc.composite": "Kompozit {name} ({fiber} elyaf)",
    "rep.results.table": "Tablo 2. Hesap sonuçları (dayanıma göre sıralı)",
    "rep.given.table": "Tablo 1. Verilen kompozit özellikleri",
    "rep.fig": "Şekil {n}. {title}",
    "rep.references.callister": (
        "W. D. Callister, D. G. Rethwisch, Malzeme Bilimi ve Mühendisliği (Türkçe çeviri), "
        "Nobel Akademik Yayıncılık, Bölüm 16: Kompozitler."
    ),
    "rep.footer": "fiber-composite-calculator ile hazırlanmıştır",
    "rep.page": "Sayfa {n}",
    # --- yorum bölüm başlıkları ---
    "sec.ranking": "Sıralama",
    "sec.fiber": "Elyaf türü ve elyaf dayanımı",
    "sec.vf": "Elyaf hacim oranı",
    "sec.length": "Ortalama elyaf uzunluğu ve kritik uzunluk",
    "sec.matrix": "Matris katkısı",
    "sec.conclusion": "Sonuç",
    # --- yorum cümleleri ---
    "rank.order": (
        "Takviye doğrultusundaki dayanıma göre sıralama (yüksekten düşüğe): {order}. Matris "
        "verisi verilmediğinden sıralama elyaf terimi σf*·Vf·(1 − lc/2l) ile yapılmıştır."
    ),
    "rank.order_with_matrix": (
        "Takviye doğrultusundaki dayanıma göre sıralama (yüksekten düşüğe): {order}. Hesapta "
        "elyaf ve matris terimleri birlikte kullanılmıştır."
    ),
    "fiber.single": "tüm kompozitler {type} elyaf kullandığından elyaf türü sıralamada fark yaratmaz.",
    "fiber.group": "{type} elyaflı kompozitlerde ({names}) elyaf dayanımı {hi} MPa'dır.",
    "fiber.group_range": "{type} elyaflı kompozitlerde ({names}) elyaf dayanımı {lo}–{hi} MPa aralığındadır.",
    "fiber.ratio": (
        "{top} elyafın dayanımı {low} elyafınkinin {ratio} katıdır. Elyaf terimi σf* ile doğru "
        "orantılı olduğundan bu fark kompozit dayanımına doğrudan yansır."
    ),
    "fiber.dominant": (
        "bu nedenle {type} elyaflı kompozitlerin tamamı ({names}) sıralamanın en üstünde yer "
        "alır; elyaf türü sıralamayı belirleyen birinci etkendir."
    ),
    "fiber.overtaken": (
        "ancak elyaf türü tek başına belirleyici değildir: {upper_type} elyaflı {upper} "
        "(Vf = {upper_vf}), daha güçlü {lower_type} elyafı kullanan {lower} kompozitini "
        "(Vf = {lower_vf}) geride bırakır. Belirleyici olan σf*·Vf çarpımıdır."
    ),
    "vf.rule": (
        "aynı elyaf türü içinde elyaf terimi σf*·Vf·η, Vf ile doğru orantılıdır; dolayısıyla "
        "elyaf hacim oranı ikinci belirleyici etkendir."
    ),
    "vf.follows": (
        "{hi} (Vf = {hi_vf}) ile {lo} (Vf = {lo_vf}) karşılaştırıldığında hacim oranları oranı "
        "{vf_ratio}, elyaf terimleri oranı {str_ratio} çıkar; aradaki farkın neredeyse tamamı "
        "hacim oranından gelir."
    ),
    "vf.follows_other": (
        "{hi} (Vf = {hi_vf}) ile {lo} (Vf = {lo_vf}) karşılaştırıldığında hacim oranları oranı "
        "{vf_ratio}, elyaf terimleri oranı {str_ratio} çıkar; farkın bir bölümü elyaf dayanımı "
        "ya da uzunluk verimindeki farklardan gelir."
    ),
    "vf.equal": (
        "{hi} ve {lo} aynı hacim oranına sahiptir (Vf = {hi_vf}); aralarındaki fark elyaf "
        "dayanımı ya da uzunluk veriminden kaynaklanır."
    ),
    "vf.against": (
        "{hi}, daha düşük hacim oranına (Vf = {hi_vf}) rağmen {lo} kompozitinden (Vf = {lo_vf}) "
        "daha dayanıklıdır; bunun nedeni daha yüksek elyaf dayanımı ya da uzunluk verimidir."
    ),
    "vf.no_pairs": (
        "her elyaf türünden tek kompozit bulunduğundan hacim oranının etkisi aynı tür içinde "
        "ayrıca karşılaştırılamaz; etkisi σf*·Vf çarpımı üzerinden sıralamaya yansır."
    ),
    "len.all_long": (
        "tüm kompozitlerde ortalama elyaf uzunluğu kritik uzunluktan büyüktür (l > lc; en küçük "
        "oran l/lc = {ratio}, {name}). Elyaflar kırılma dayanımlarına kadar yüklenebilir ve "
        "σcd* = σf*·Vf·(1 − lc/2l) + σm'·(1 − Vf) bağıntısı geçerlidir."
    ),
    "len.short": (
        "{names} için l < lc'dir: elyaflar kırılma dayanımına ulaşmadan matristen sıyrılır, "
        "uzunluk verimi %50'nin altına düşer ve σcd*' = (l·τc/d)·Vf + σm'·(1 − Vf) bağıntısı "
        "kullanılır."
    ),
    "len.efficiency": "uzunluk verimi η = 1 − lc/2l, {lo_eff} ({lo}) ile {hi_eff} ({hi}) arasındadır.",
    "len.longest": (
        "en uzun elyaflar {name} kompozitindedir (l = {l} mm); ancak verimi belirleyen mutlak "
        "uzunluk değil l/lc oranıdır. {name} için lc = {lc} mm olduğundan l/lc = {ratio} olur."
    ),
    "len.no_order_change": (
        "verimler birbirine yakın olduğundan uzunluk etkisi sıralamayı değiştirmez: yalnızca "
        "σf*·Vf çarpımına göre yapılan sıralama da {product_order} şeklindedir. Uzunluk, "
        "dayanımları yalnızca birkaç yüzde düşürür."
    ),
    "len.no_order_change_wide": (
        "verimler arasında belirgin fark olsa da uzunluk etkisi sıralamayı değiştirmez: σf*·Vf "
        "çarpımına göre sıralama da {product_order} şeklindedir."
    ),
    "len.order_change": (
        "uzunluk etkisi sıralamayı değiştirir: σf*·Vf çarpımına göre sıralama {product_order} "
        "iken uzunluk verimi hesaba katıldığında {fiber_order} olur."
    ),
    "len.near_continuous_some": (
        "elyaf uzunluğu l ≥ 15·lc koşulunu sağlayan kompozitler ({near}) pratikte sürekli elyaflı gibi "
        "davranır; {far} ise bu sınırın altında kalır ve süreksizlik etkisi daha belirgindir."
    ),
    "len.near_continuous_all": "tüm kompozitlerde l ≥ 15·lc'dir; elyaflar pratikte sürekli elyaf gibi davranır.",
    "len.near_continuous_none": "hiçbir kompozit l ≥ 15·lc koşulunu sağlamaz; süreksizlik etkisi tümünde belirgindir.",
    "mat.unknown": (
        "matris dayanımı verilmediğinden hesap elyaf terimiyle yapılmıştır. Matris terimi "
        "σm'·(1 − Vf), hacim oranı düşük olan kompozitlere görece daha fazla katkı verir; bu "
        "yüzden matris eklendiğinde sıralamanın değişip değişmeyeceği kontrol edilmelidir."
    ),
    "mat.included": (
        "ortak matris gerilmesi σm' = {value} MPa alınarak matris terimi σm'·(1 − Vf) her "
        "kompozite eklenmiştir."
    ),
    "mat.changed_order": (
        "matris terimi sıralamayı değiştirmiştir: yalnızca elyaf terimine göre {fiber_order} "
        "olan sıralama {order} olmuştur."
    ),
    "mat.threshold": (
        "iki kompozitin yer değiştirmesi için gereken en küçük ortak matris gerilmesi "
        "σm' = Δ(elyaf terimi) / ΔVf ≈ {value} MPa'dır ({upper}–{lower} çifti)."
    ),
    "mat.unrealistic": (
        "polimer matrislerin çekme dayanımı tipik olarak 100 MPa'nın altındadır ve σm' bu "
        "değeri aşamaz. {value} MPa'lık eşik gerçekçi değerlerin çok üzerinde "
        "olduğundan sıralama matristen bağımsızdır; sıralamanın doğruluğu bu şekilde gösterilmiş olur."
    ),
    "mat.sensitive": (
        "bu eşik gerçekçi matris gerilmeleri aralığına yakındır ({limit} MPa altı); matris "
        "verisi olmadan sıralama kesin kabul edilmemelidir."
    ),
    "mat.no_flip": (
        "hiçbir kompozit çifti matris terimiyle yer değiştiremez: sıralamada üstte olan her "
        "kompozitin hacim oranı alttakinden büyük değildir, bu yüzden matris terimi farkı "
        "yalnızca açar. Sıralama matristen bağımsızdır."
    ),
    "concl.summary": (
        "takviye doğrultusundaki dayanım sıralaması {order} şeklindedir. En yüksek dayanım "
        "{top} ({top_value} MPa), en düşük dayanım {bottom} ({bottom_value} MPa) kompozitindedir."
    ),
    "concl.driver_type_then_vf": "sıralamayı önce elyaf türü (elyaf dayanımı), aynı tür içinde ise elyaf hacim oranı belirler.",
    "concl.driver_vf": "elyaf türü ortak olduğundan sıralamayı esas olarak elyaf hacim oranı ve uzunluk verimi belirler.",
    "concl.driver_product": "sıralamayı tek bir etken değil, elyaf dayanımı ile hacim oranının çarpımı (σf*·Vf) belirler.",
    "concl.length_minor": "elyaf uzunluğunun etkisi ikincildir: verimler sıralamayı değiştirmez.",
    "concl.length_major": "elyaf uzunluğu (l/lc oranı) sıralamayı değiştirecek kadar etkilidir.",
    "concl.matrix_robust": "matris katkısı gerçekçi değerlerde sıralamayı değiştiremez.",
    "concl.matrix_sensitive": "matris katkısı sıralamayı değiştirebilecek düzeydedir; matris verisi önemlidir.",
    # --- adım adım ---
    "step.regime_long": "Bölge kontrolü: l > lc, σcd* bağıntısı kullanılır",
    "step.regime_short": "Bölge kontrolü: l < lc, σcd*' bağıntısı kullanılır (τc/d = σf*/2lc)",
    "step.efficiency": "Uzunluk verimi",
    "step.fiber_term": "Elyaf terimi",
    "step.matrix_term": "Matris terimi",
    "step.total": "Kompozit dayanımı",
    "step.ecl": "Boyuna elastik modül (eş-gerinim)",
    "step.ect": "Enine elastik modül (eş-gerilme)",
    "step.load_ratio": "Elyaf/matris yük oranı",
    "step.sigma_cl": "Boyuna çekme dayanımı",
    "step.forces": "Yük paylaşımı",
    "step.stresses": "Elyaf ve matristeki gerilmeler",
    "step.strain": "Birim şekil değiştirme",
    "step.lc": "Kritik uzunluk",
    "step.ecd": "Yönlenme verimiyle elastik modül",
    "step.particle_upper": "Üst sınır",
    "step.particle_lower": "Alt sınır",
    "step.density": "Kompozit yoğunluğu",
    # --- grafikler ---
    "chart.strength.title": "Takviye doğrultusundaki dayanım",
    "chart.strength.y": "Dayanım σcd* (MPa)",
    "chart.strength.fiber": "Elyaf terimi",
    "chart.strength.matrix": "Matris terimi",
    "chart.ratio.title": "Ortalama elyaf uzunluğu / kritik uzunluk",
    "chart.ratio.x": "l / lc",
    "chart.ratio.critical": "l = lc",
    "chart.ratio.continuous": "l = 15·lc (pratikte sürekli)",
    "chart.eff.title": "Uzunluk verimi eğrisi",
    "chart.eff.x": "l / lc",
    "chart.eff.y": "Uzunluk verimi η",
    "chart.mix.title": "Karışım kuralı: elastik modül",
    "chart.mix.x": "Elyaf hacim oranı Vf",
    "chart.mix.y": "Elastik modül (GPa)",
    "chart.mix.long": "Boyuna Ecl (eş-gerinim)",
    "chart.mix.trans": "Enine Ect (eş-gerilme)",
    "chart.mix.current": "Seçilen Vf",
    "chart.sl.title": "Dayanımın elyaf uzunluğuyla değişimi",
    "chart.sl.x": "Elyaf uzunluğu l (mm)",
    "chart.sl.y": "Dayanım σcd (MPa)",
    "chart.sl.current": "Seçilen l",
    "chart.orient.title": "Elyaf yönlenmesinin elastik modüle etkisi",
    "chart.orient.x": "Elastik modül (GPa)",
    "chart.particle.title": "Parçacık kompozit: elastik modül sınırları",
    "chart.particle.x": "Parçacık hacim oranı Vp",
    "chart.particle.upper": "Üst sınır",
    "chart.particle.lower": "Alt sınır",
    # --- sürekli elyaf sayfası ---
    "cont.title": "Sürekli ve hizalanmış elyaf",
    "cont.intro": (
        "Boyuna (eş-gerinim) ve enine (eş-gerilme) elastik modülleri, yük paylaşımını ve boyuna "
        "çekme dayanımını hesaplar. Varsayılan değerler Callister Örnek 16.1'dir (cam/polyester)."
    ),
    "cont.fill": "Tipik malzemeden doldur",
    "cont.fiber": "Elyaf",
    "cont.matrix": "Matris",
    "cont.apply": "Değerleri uygula",
    "cont.reset": "Örnek 16.1'e dön",
    "cont.ef": "Elyaf modülü Ef (GPa)",
    "cont.em": "Matris modülü Em (GPa)",
    "cont.vf": "Elyaf hacim oranı Vf",
    "cont.sigma_f": "Elyaf dayanımı σf* (MPa)",
    "cont.sigma_m": "Elyaf kırılmasındaki matris gerilmesi σm' (MPa)",
    "cont.load": "Yük paylaşımı (isteğe bağlı)",
    "cont.stress": "Uygulanan boyuna gerilme σc (MPa)",
    "cont.area": "Kesit alanı A (mm²)",
    "cont.ecl": "Ecl (boyuna)",
    "cont.ect": "Ect (enine)",
    "cont.ratio": "Ff / Fm",
    "cont.sigma_cl": "σcl* (boyuna dayanım)",
    "cont.ff": "Elyaf yükü Ff",
    "cont.fm": "Matris yükü Fm",
    "cont.sf": "Elyaf gerilmesi σf",
    "cont.sm": "Matris gerilmesi σm",
    "cont.strain": "Birim şekil değiştirme ε",
    "material.e_glass": "E-camı",
    "material.carbon_sm": "Karbon (standart modül)",
    "material.aramid": "Aramid (Kevlar 49)",
    "material.epoxy": "Epoksi",
    "material.polyester": "Polyester",
    # --- süreksiz elyaf sayfası ---
    "disc.title": "Süreksiz ve hizalanmış elyaf",
    "disc.intro": (
        "Tek bir kompozit için kritik uzunluğu, uzunluk verimini ve takviye doğrultusundaki "
        "dayanımı hesaplar; dayanımın elyaf uzunluğuyla nasıl değiştiğini gösterir."
    ),
    "disc.lc_mode": "Kritik uzunluk",
    "disc.lc_direct": "Doğrudan gir",
    "disc.lc_compute": "σf*, d ve τc'den hesapla",
    "disc.sigma_f": "Elyaf dayanımı σf* (MPa)",
    "disc.vf": "Elyaf hacim oranı Vf",
    "disc.l": "Ortalama elyaf uzunluğu l (mm)",
    "disc.lc": "Kritik uzunluk lc (mm)",
    "disc.d": "Elyaf çapı d (µm)",
    "disc.tau": "Ara yüzey kayma dayanımı τc (MPa)",
    "disc.sigma_m": "Matris gerilmesi σm' (MPa)",
    "disc.strength": "σcd*",
    "disc.ratio": "l / lc",
    "disc.eff": "Uzunluk verimi η",
    "disc.near": "l ≥ 15·lc: pratikte sürekli elyaf gibi davranır.",
    "disc.short": "l < lc: elyaflar kırılmadan matristen sıyrılır; dayanım belirgin biçimde düşer.",
    "disc.between": "lc < l < 15·lc: süreksizlik etkisi hissedilir; uzunluk verimi {eff}.",
    # --- yönlenme ve parçacık sayfası ---
    "rp.title": "Elyaf yönlenmesi ve parçacık kompozitler",
    "rp.orient": "Elyaf yönlenme verimi (K)",
    "rp.orient_intro": "Ecd = K·Ef·Vf + Em·Vm bağıntısıyla yönlenmenin elastik modüle etkisi.",
    "rp.particle": "Büyük parçacıklı kompozit",
    "rp.particle_intro": (
        "Karışım kuralının üst ve alt sınırları. Varsayılan değerler bakır matris + tungsten "
        "parçacıktır (Callister)."
    ),
    "rp.k.aligned_par": "Hizalı, elyafa paralel (K = 1)",
    "rp.k.aligned_perp": "Hizalı, elyafa dik (K = 0)",
    "rp.k.random_2d": "Düzlemde rastgele (K = 3/8)",
    "rp.k.random_3d": "Üç boyutta rastgele (K = 1/5)",
    "rp.ep": "Parçacık modülü Ep (GPa)",
    "rp.em": "Matris modülü Em (GPa)",
    "rp.vp": "Parçacık hacim oranı Vp",
    "rp.upper": "Üst sınır Ec(u)",
    "rp.lower": "Alt sınır Ec(l)",
    "rp.k_note": (
        "Not: Enine yönde K = 0 alınması matrisin katkısını tek başına bırakan kaba bir "
        "yaklaşımdır; sürekli elyafta enine modül için eş-gerilme bağıntısı daha doğrudur."
    ),
}
