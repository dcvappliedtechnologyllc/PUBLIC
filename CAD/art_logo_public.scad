// Public branded wedge art (option A): DCV wordmark over DCV-AT.COM.  Units mm; wedge face is 4.50 x 2.67 in.
in = 25.4;
wm_w = 3.60*in;          // wordmark width
url_cap = 0.34*in;       // URL cap height
gap = 0.30*in;
// wordmark bbox after resize: width wm_w, height = wm_w * 37/114
wm_h = wm_w * 37/114;
total = wm_h + gap + url_cap;
translate([0, total/2 - wm_h/2]) resize([wm_w, 0], auto = true) import("dcv_wordmark.svg", center = true);
translate([0, -total/2 + url_cap/2]) text("DCV-AT.COM", size = url_cap, font = "Orbitron:style=Bold", halign = "center", valign = "center", spacing = 1.08);
