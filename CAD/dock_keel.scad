// Keel dock for the Doyle light-vee jaws — Rev G (Rev F on 1/4-20 hardware: 9/32 holes, 1/4-20 x 1-1/4 button heads, no washer; PRINT ON END)
// A double-vee keel that is the negative of the jaw vee (15deg faces, 1.00" above and below the apex),
// so it drops between the jaws, self-centers when clamped, and carries a swappable top (mag insert etc.).
// Two 1/4-20 x 1-1/4 button heads come UP through counterbores in the keel bottom, into 1/4-20 nuts dropped down hex
// pockets inside the mag stub; the nuts bear on the insert base, so base + keel web are clamped.
// Print upright (as modeled): bottom on the bed, no supports.  Units: parameters in inches, model in mm.

in = 25.4;

/* [Keel] */
keel_length_in     = 4.50;   // = the plate seat width: clamps right over the casting, no wing loading
keel_apex_width_in = 2.50;   // jaw-apex to jaw-apex when clamped (max opening at apex is 3.00")
face_angle_deg     = 15;     // must match the jaws
vee_half_height_in = 1.00;   // must match the jaws (keel is 2x this tall)
end_stops          = false;   // plates at both ends that bracket the jaw ends so the keel can't walk
stop_thick_in      = 0.20;
stop_gap_in        = 0.03;   // clearance to the jaw end faces
stop_overlap_in    = 0.50;   // how far the stops reach onto the jaw ends, each side

/* [Set tab — a fin on one side that drops into the jaw's foam-lip groove so you can set the keel on the
   fixed jaw and then tighten. Fits deep: keel sits tab_lift low until the closing vee faces lift it. */
set_tab            = true;
tab_length_in      = 4.50;   // full keel length
tab_thick_in       = 0.07;   // Rev I jaw slot is 0.10"
tab_clear_in       = 0.01;   // gap to the jaw face
tab_depth_in       = 0.26;   // below the keel bottom (groove is 0.30" deep -> 0.04" of lift before it bottoms)
rail_relief_in     = 0.08;   // relief over the foam-lip rails on both bottom edges so they never carry the keel
rail_relief_wid_in = 0.30;   // from the bottom corner inward (Rev I lip reaches 0.245" in from the vee edge)
print_on_end       = false;  // true = stand on an end face for printing (tab, pocket, reliefs all become vertical walls)

/* [Top-piece interface — Rev B: two M6 x 30 from the TOP through ears on the insert base,
   into M6 nuts in side-entry slots in the keel (nut bears UP on keel material, so the joint actually clamps) */
pocket_len_in      = 2.64;   // insert base footprint (matches the PMAG block tang: 2.64" x 1.34")
pocket_wid_in      = 1.34;
pocket_depth_in    = 0.15;
pocket_clear_in    = 0.01;
bolt_cc_in         = 1.60;   // bolt center-to-center (inside the stub footprint, +/-0.80")
bolt_dia_in        = 0.28;   // 9/32 clearance for 1/4-20
head_cbore_in      = 0.52;   // Ø for a 1/4-20 button head (0.44 dia), from the bottom — no washer, the keel bottom is only 1.96 wide
keel_under_bolt_in = 0.50;   // solid keel web between the head and the pocket floor: 0.50 + 0.40 base + 0.22 nut = 1.12" < 1-1/4 screw

$fn = 48;

L   = keel_length_in * in;
W   = keel_apex_width_in * in;
VH  = vee_half_height_in * in;
DEP = VH * tan(face_angle_deg);
KH  = 2 * VH;                      // keel height
WT  = W - 2 * DEP;                 // width at top and bottom
ST  = stop_thick_in * in; SG = stop_gap_in * in; SO = stop_overlap_in * in;

echo(str("keel ", L/in, " x ", W/in, " (apex) / ", WT/in, " (top,bottom) x ", KH/in, " tall; total length with stops = ", (L + 2*(SG+ST))/in));

module keel_profile() {   // in (Y, Z): hexagon, apex at Z = VH
    polygon([[-WT/2, 0], [WT/2, 0], [W/2, VH], [WT/2, KH], [-WT/2, KH], [-W/2, VH]]);
}

TL = tab_length_in * in; TT = tab_thick_in * in; TC = tab_clear_in * in; TD = tab_depth_in * in;
RR = rail_relief_in * in; RW = rail_relief_wid_in * in;

module keel() {
    difference() {
        union() {
            rotate([90, 0, 90]) translate([0, 0, -L/2]) linear_extrude(L) keel_profile();
            if (set_tab)   // fin hanging below the bottom, on the -Y side, sitting in the groove behind the foam lip
                translate([-TL/2, -(WT/2 - TC), -TD]) cube([TL, TT, TD + 1]);
            if (end_stops)
                for (s = [-1, 1])
                    translate([s * (L/2 + SG + ST/2), 0, KH/2])
                        cube([ST, WT + 2 * SO, KH], center = true);
        }
        // relief over the foam-lip rails, both bottom edges (keel must hang on the vee faces, not the rails)
        if (set_tab)
            for (sy = [-1, 1])
                translate([-L/2 - 1, sy > 0 ? WT/2 - RW : -WT/2 - 1, -1]) cube([L + 2, RW + 1, RR + 1]);
        // pocket for the top piece
        translate([0, 0, KH - pocket_depth_in * in])
            linear_extrude(pocket_depth_in * in + 1)
                offset(r = pocket_clear_in * in) square([pocket_len_in * in, pocket_wid_in * in], center = true);
        // two bolts from below: clearance hole + deep counterbore for the head (4 mm T-handle reaches)
        for (s = [-1, 1]) {
            bx = s * bolt_cc_in * in / 2;
            translate([bx, 0, -1]) cylinder(d = bolt_dia_in * in, h = KH + 2);
            translate([bx, 0, -1]) cylinder(d = head_cbore_in * in, h = KH - pocket_depth_in * in - keel_under_bolt_in * in + 1);
        }
    }
}

if (print_on_end) translate([0, 0, L/2]) rotate([0, -90, 0]) keel(); else keel();   // pop can: stands on an end face
