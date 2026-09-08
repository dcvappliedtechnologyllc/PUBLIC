// Keel dock for the Doyle light-vee jaws — Rev I (v9): TEE TOP. The keel hangs from a flange that rests on the jaw tops
// instead of hanging on a set-tab in the foam slot. Rev H (v8) and everything before it hung on a one-sided 0.07" fin: with the
// vise open the keel tipped ~4deg on the fin, sat 0.04" low, and a 15deg vee (centering component tan15 = 0.27) cannot out-pull
// PETG-on-PETG friction (0.3-0.5) to fix that, so it clamped cocked. Now: flange underside sits on both jaw tops (flat on flat,
// roll and pitch fixed before the handle moves); the keel apex is set keel_lift ABOVE the jaw apex so the UPPER vee faces touch
// first and their reaction pushes the keel DOWN onto the flange ("top taper dominant"). Push down -> flange; pull up -> the
// upper wedge tightens. Bottom of the keel truncated 0.30" so the lower faces are a 0.70" backup with 0.008" clearance and the
// keel bottom clears the lip tops; set-tab and rail reliefs gone. Drops in from the top and hangs on the fixed jaw alone.
// A double-vee keel that is the negative of the jaw vee (15deg faces, 1.00" above and below the apex),
// so it drops between the jaws, self-centers when clamped, and carries a swappable top (mag insert etc.).
// Two 1/4-20 x 1-1/4 button heads come UP through counterbores in the keel bottom, into 1/4-20 nuts dropped down hex
// pockets inside the mag stub; the nuts bear on the insert base, so base + keel web are clamped.
// Print on end ("pop can", print_on_end = true): flange, pocket and bores all become vertical walls, no support.
// Units: parameters in inches, model in mm.

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

/* [Tee top — flange on both sides that rests on the jaw tops. The keel hangs from it. */
top_flange         = true;
flange_reach_in    = 0.50;   // how far the flange reaches over each jaw top (jaw top is 0.87" wide from the vee edge to the back wedge)
flange_thick_in    = 0.20;   // flange thickness, above its underside
keel_lift_in       = 0.015;  // keel apex sits this far ABOVE the jaw apex when the flange is down -> upper faces engage first,
                             // lower faces get 2*lift*tan(15) = 0.008" total clearance; the clamp pushes the keel onto the flange
bottom_trim_in     = 0.30;   // keel bottom raised this much: lower faces 0.70" long, bottom 0.30" above the jaw lip tops

/* [Set tab — RETIRED in v9 (kept for the record). A fin that dropped into the jaw's foam-lip groove. It hung the keel cocked. */
set_tab            = false;
tab_length_in      = 4.50;
tab_thick_in       = 0.07;
tab_clear_in       = 0.01;
tab_depth_in       = 0.26;
rail_relief_in     = 0.08;   // only cut when set_tab is on
rail_relief_wid_in = 0.30;
print_on_end       = false;  // true = stand on an end face for printing

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

FR = flange_reach_in * in; FTK = flange_thick_in * in; LIFT = keel_lift_in * in; BT = top_flange ? bottom_trim_in * in : 0;
ZF = KH - LIFT;                                   // flange underside = jaw top plane when seated
WF = W - 2 * (ZF - VH) * tan(face_angle_deg);     // hexagon width at the flange underside
WB = W - 2 * (VH - BT) * tan(face_angle_deg);     // width at the (truncated) bottom
KT = top_flange ? ZF + FTK : KH;                  // keel top (pocket cut from here)
Z0 = BT;                                          // keel bottom

echo(str("keel ", L/in, " x ", W/in, " (apex) / ", WT/in, " (top,bottom) x ", (KT - Z0)/in, " tall (bottom at ", Z0/in, ", flange underside at ",
         ZF/in, ", top at ", KT/in, "); overall width over flanges ", (WF + 2*FR)/in, "; lower-face clearance when seated ",
         2*LIFT*tan(face_angle_deg)/in, "; total length with stops = ", (L + 2*(SG+ST))/in));

module keel_profile() {   // in (Y, Z): hexagon, apex at Z = VH; truncated at the bottom, tee flange at the top
    if (top_flange)
        polygon([[-WB/2, BT], [WB/2, BT], [W/2, VH], [WF/2, ZF], [WF/2 + FR, ZF], [WF/2 + FR, KT],
                 [-WF/2 - FR, KT], [-WF/2 - FR, ZF], [-WF/2, ZF], [-W/2, VH]]);
    else
        polygon([[-WT/2, 0], [WT/2, 0], [W/2, VH], [WT/2, KH], [-WT/2, KH], [-W/2, VH]]);
}

TL = tab_length_in * in; TT = tab_thick_in * in; TC = tab_clear_in * in; TD = tab_depth_in * in;
RR = rail_relief_in * in; RW = rail_relief_wid_in * in;

module keel() {
    union() {
        difference() {
            union() {
                rotate([90, 0, 90]) translate([0, 0, -L/2]) linear_extrude(L) keel_profile();
                if (end_stops)
                    for (s = [-1, 1])
                        translate([s * (L/2 + SG + ST/2), 0, (Z0 + KT)/2])
                            cube([ST, WF + 2 * FR + 2 * SO, KT - Z0], center = true);
            }
            // relief over the foam-lip rails, both bottom edges (keel must hang on the vee faces, not the rails)
            if (set_tab)
                for (sy = [-1, 1])
                    translate([-L/2 - 1, sy > 0 ? WT/2 - RW : -WT/2 - 1, -1]) cube([L + 2, RW + 1, RR + 1]);
            // pocket for the top piece
            translate([0, 0, KT - pocket_depth_in * in])
                linear_extrude(pocket_depth_in * in + 1)
                    offset(r = pocket_clear_in * in) square([pocket_len_in * in, pocket_wid_in * in], center = true);
            // two bolts from below: clearance hole + deep counterbore for the head (4 mm T-handle reaches)
            for (s = [-1, 1]) {
                bx = s * bolt_cc_in * in / 2;
                translate([bx, 0, Z0 - 1]) cylinder(d = bolt_dia_in * in, h = KT - Z0 + 2);
                translate([bx, 0, Z0 - 1]) cylinder(d = head_cbore_in * in, h = (KT - pocket_depth_in * in - keel_under_bolt_in * in) - (Z0 - 1));
            }
        }
        // set-tab: fin hanging below the bottom on the -Y side, sitting in the jaw's foam slot (slot is against the vee-face
        // plane, lip is 0.10" further in, so the fin at 0.01-0.08" from the edge clears the lip). Added AFTER the relief and
        // carried 1 mm up past it into the web, so it is one body with the keel. Above the vee edge it stands in open air.
        if (set_tab)
            translate([-TL/2, -(WT/2 - TC), -TD]) cube([TL, TT, TD + RR + 1]);
    }
}

if (print_on_end) translate([0, 0, L/2]) rotate([0, -90, 0]) keel(); else keel();   // pop can: stands on an end face (bottom at Z0 is irrelevant on end)
