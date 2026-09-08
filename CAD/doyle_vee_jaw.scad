// Doyle Light-Vee Jaw  —  Rev Q  (Rev P + teardrop roof on the washer pockets so the on-end print has no near-horizontal arch)
// Printed vee jaw for the Harbor Freight Doyle 4-1/2" swivel vise (HF #57737)
// Print two. Model is in mm; every parameter below is entered in inches.
// Modeled upright (Z = height, +Y = toward the workpiece, -Y = over the vise).
// PRINT STANDING ON END: set print_orientation = true (rotates so the length is Z).
// Every feature is part of the extruded profile, so on end it all prints as vertical walls.

in = 25.4;

/* [Jaw body] */
jaw_length_in       = 4.50;   // overall length (8.00 for the long version)
seat_height_in      = 0.75;   // casting top above jaw bottom (= steel plate height)  ** confirm **
apex_above_top_in   = 2.00;   // how far the vee apex sits above the vise top (the "raise")
vee_half_height_in  = 1.00;   // vee spans apex +/- this
back_to_apex_in     = 0.60;   // mounting face to vee apex (was 0.75)
face_angle_deg      = 15;     // vee face tilt off vertical (15 = 150 deg included)
apex_radius_in      = 0.0625; // fillet at the apex
end_chamfer_in      = 0.0625; // chamfer on the vertical end edges

/* [Saddle flange + solid back wedge] */
flange_depth_in     = 0.35;   // how far the saddle reaches back over the casting top (= back_taper). The casting flat is only ~1/4" before it rounds off.
flange_thick_in     = 0.40;   // lip thickness
corner_relief_in    = 0.06;   // 45deg relief at the inside corner so a radiused casting edge still seats
back_taper_in       = 0.35;   // solid wedge on the back, this thick at the saddle, tapering to 0 at the top (logo face ~82 deg)

/* [Parallel band + foam slot — a flat clamping face below the vee, proud of the vee edges like the steel
   plates were. A slot in the band top (against the vee) takes a craft-foam strip's bottom edge or the keel's
   set-tab. The lip in front of the slot is SET BACK from the band's clamp plane so a workpiece never bears on it.] */
foam_lip            = true;   // band + slot + lip on
band_proud_in       = 0.325;  // band (clamp) face proud of the vee-edge plane
foam_slot_in        = 0.10;   // slot width (2 mm craft foam; keel set-tab is 0.07)
foam_lip_height_in  = 0.30;   // slot depth = lip height; lip top is flush with the vee's lower edge
lip_setback_in      = 0.08;   // lip face behind the band clamp plane -> lip thickness = 0.325 - 0.10 - 0.08 = 0.145

/* [Edge easing — all on edges that run the length of the jaw (they are corners of the 2D profile, so they print
   as vertical walls on end). Bottom-of-feature edges get 45deg CHAMFERS (safe overhangs on the upright branded
   print); top edges get FILLETS. End-face edges keep the plain 1/16" end_chamfer.] */
ease_edges          = true;
ease_big_in         = 0.0625; // jaw bottom, flange underside, band top/bottom, top-front (vee) edge
ease_top_back_in    = 0.05;   // wedge/top-face edge (keeps the top face flat under the text)
ease_small_in       = 0.03;   // lip top edges, slot mouth, lip/band inside corner
ease_fn             = 10;     // segments per fillet

/* [Vise / screw pattern] */
vise_width_in       = 4.50;   // width of the plate seat (Doyle 4-1/2")
screw_cc_in         = 2.40;   // screw center-to-center (measured: holes 1.05" from each end of the 4.47" seat); 1/4-20 x 1-1/4 button heads
screw_height_in     = 0.35;   // screw axis above jaw bottom (= above plate bottom)
thru_dia_in         = 0.28;   // 9/32 clearance for 1/4-20 (the vise's jaw screws: 5/32 hex button heads, 20 tpi)
cbore_dia_in        = 1.06;   // clears a 1" OD fender washer; pocket is open through the jaw bottom, washer hangs 0.15" below it over air past the ~3/8" ledge
slot_travel_in      = 0.25;   // horizontal slot travel (1/8" each way)
slot_vert_in        = 0.08;   // vertical slop: the machined ledge sets the height, the saddle lands where the rough casting top puts it, the screws never fight either
wall_under_head_in  = 0.35;   // solid plastic between washer and casting (in compression; 0.35 leaves a 3/4" 1/4-20 with 0.34" of engagement)
cbore_open_bottom   = true;   // washer pocket opens through the jaw bottom (no knife-edge sliver under a 16 mm washer; the plate seat closes it)

/* [Branding — reads correctly on the MOVABLE jaw (wedge faces the operator)] */
brand_logo          = false;  // DCV Applied Technology logo debossed into the back wedge
logo_svg            = "dcv_logo_scad.svg";
logo_width_in       = 3.80;   // logo width across the wedge (wedge is jaw_length long)
brand_text          = false;  // "FUCK YEAH" debossed into the top face
brand_text_str      = "FUCK YEAH";
brand_font          = "Bangers";   // Bangers or Luckiest Guy (Google Fonts, OFL/Apache) — baked into the STL
brand_text_size_in  = 0.60;   // cap height on the 1.02"-wide top face
deboss_depth_in     = 0.04;   // 1 mm
flip_for_fixed_jaw  = false;  // mirror the text/logo so it reads right on the fixed jaw instead

/* [Witness marks — V-grooves at the 4.50" plate width (and center) for lining the jaw up on the vise] */
witness_marks       = false;
witness_width_in    = 4.50;   // = vise plate seat width
witness_v_in        = 0.08;   // groove width (90deg V, so depth is half this)
witness_slope_len_in= 0.50;   // length of the tick up the back wedge from the flange edge

/* [Options] */
side_cheeks         = false;  // fill the wings in under the flange to hug the casting sides (needs casting width)
casting_width_in    = 4.50;
cheek_clearance_in  = 0.03;
magnet_pockets      = false;
magnet_dia_in       = 0.25;
magnet_depth_in     = 0.13;
magnet_x_in         = [1.50, 4.00, 6.50];
magnet_offset_in    = 0.50;
show_test_plate     = false;  // 0.2" hole-pattern coupon instead of the jaw
print_orientation   = false;  // true = stand on end for printing

$fn = 64;

// ---------- derived ----------
L    = jaw_length_in * in;
SEAT = seat_height_in * in;
ZA   = SEAT + apex_above_top_in * in;          // apex height
VH   = vee_half_height_in * in;
H    = ZA + VH;                                 // overall height
ZL   = ZA - VH;                                 // lower edge of the vee
TA   = back_to_apex_in * in;
DEP  = VH * tan(face_angle_deg);
TE   = TA + DEP;                                // thickness at vee edges
FD   = flange_depth_in * in;
FT   = flange_thick_in * in;
BT   = back_taper_in * in;
CC   = screw_cc_in * in;
SH   = screw_height_in * in;
SLOT = slot_travel_in * in;
SLV  = slot_vert_in * in;
R    = apex_radius_in * in;
CH   = end_chamfer_in * in;
FG   = foam_slot_in * in;
BP   = band_proud_in * in;
FLH  = foam_lip_height_in * in;
LS   = lip_setback_in * in;
YMAX = TE + (foam_lip ? BP : 0);                // outermost +Y extent
DB   = deboss_depth_in * in;

echo(str("Length = ", L/in, " in   height = ", H/in, " in   apex at ", ZA/in, " in   opening at apex = ",
         (vise_width_in*in - 2*TA)/in, " in   overhang each side = ", (L - vise_width_in*in)/2/in, " in"));

// (Y,Z) profile.  Rev J builds the whole outline (vee included) as one corner list so every corner can be
// sharp (0), chamfered (1) or filleted (2) individually.  Fallback: the Rev H/I union-of-boxes profile.
function unit(v) = v / norm(v);
function arc(ctr, r, a1, d, n) = [for (k = [0 : n]) ctr + r * [cos(a1 + d * k / n), sin(a1 + d * k / n)]];
function corner(P, C, N, t, s, n) =
    t == 0 || s <= 0 ? [C] :
    let(u1 = unit(P - C), u2 = unit(N - C))
    t == 1 ? [C + u1 * s, C + u2 * s] :
    let(ang = acos(max(-1, min(1, u1 * u2))), th = ang / 2, tl = s / tan(th),
        ctr = C + unit(u1 + u2) * s / sin(th),
        p1 = C + u1 * tl, p2 = C + u2 * tl,
        a1 = atan2(p1[1] - ctr[1], p1[0] - ctr[0]), a2 = atan2(p2[1] - ctr[1], p2[0] - ctr[0]),
        d = ((a2 - a1 + 540) % 360) - 180)
    arc(ctr, s, a1, d, n);
function eased(pts, n) = [for (i = [0 : len(pts) - 1])
    for (p = corner(pts[(i - 1 + len(pts)) % len(pts)][0], pts[i][0], pts[(i + 1) % len(pts)][0], pts[i][1], pts[i][2], n)) p];

module profile_2d() {
    if (ease_edges && foam_lip) {
        CR = corner_relief_in * in;
        EB = ease_big_in * in; ET = ease_top_back_in * in; ES = ease_small_in * in;
        // [ [y, z], type (0 sharp / 1 chamfer / 2 fillet), size ]  — clockwise in (Y,Z)
        pts = [
            [[0, 0],                    1, EB],   // jaw bottom / mounting face
            [[0, SEAT - CR],            0, 0],    // inside-corner relief (45deg notch for the casting edge radius)
            [[CR, SEAT],                0, 0],
            [[0, SEAT + CR],            0, 0],
            [[-CR, SEAT],               0, 0],
            [[-FD, SEAT],               1, EB],   // flange underside / back face
            [[-FD, SEAT + FT],          2, EB],   // back face / wedge slope
            [[0, H],                    2, ET],   // wedge / top face
            [[TE, H],                   2, EB],   // top face / upper vee face
            [[TA, ZA],                  2, R],    // apex
            [[TE, ZL],                  1, ES],   // lower vee face / slot back wall
            [[TE, ZL - FLH],            0, 0],    // slot floor
            [[TE + FG, ZL - FLH],       0, 0],
            [[TE + FG, ZL],             1, ES],   // lip inside top
            [[TE + BP - LS, ZL],        1, ES],   // lip outside top
            [[TE + BP - LS, ZL - FLH],  2, ES],   // lip face / band top (inside corner)
            [[TE + BP, ZL - FLH],       2, EB],   // band top / clamp face
            [[TE + BP, 0],              1, EB],   // clamp face / jaw bottom
        ];
        polygon(eased(pts, ease_fn));
    } else {
        difference() {
            union() {
                square([TE, H]);                                     // face block
                translate([-FD, SEAT]) square([FD + 1, FT]);         // saddle lip over the vise top
                if (BT > 0)                                          // solid back wedge
                    polygon([[-BT, SEAT + FT - 0.01], [0.01, SEAT + FT - 0.01], [0.01, H]]);
                if (foam_lip) {                                      // parallel band, jaw bottom up to the slot floor
                    translate([TE - 0.01, 0]) square([BP + 0.01, ZL - FLH]);
                    translate([TE + FG, ZL - FLH - 0.01]) square([BP - FG - LS, FLH + 0.01]);
                }
            }
            translate([0, SEAT]) rotate(45) square(corner_relief_in * in * sqrt(2), center = true);
        }
    }
}

// vee wedge (in Y,Z), apex rounded
module vee_wedge_2d() {
    // bounded to the vee's own height so it can't shave the foam lip below it
    offset(r = R) offset(delta = -R)
        polygon([
            [TA, ZA],
            [TE, ZL],
            [TE + 20, ZL],
            [TE + 20, ZA + VH],
            [TE, ZA + VH]
        ]);
}

// rounded-rectangle slot, axis along Y, from y0 to y1
module slot(d, x, z, y0, y1, vert = 0, open_bottom = false, teardrop = false) {
    translate([x, y0, z]) rotate([-90, 0, 0])
        hull() {
            for (sx = [-1, 1], sz = [-1, 1])
                translate([sx * SLOT/2, sz * vert/2, 0]) cylinder(d = d, h = y1 - y0);
            if (teardrop)   // 45deg roof: apex at r*sqrt(2) above centre, so no arch crown goes flat on the on-end print
                for (sx = [-1, 1]) translate([sx * SLOT/2, -(vert/2 + d/2 * sqrt(2)), 0]) cylinder(d = 0.5, h = y1 - y0, $fn = 8);
        }
    if (open_bottom)   // straight walls from the bore centreline down through the jaw bottom
        translate([x - SLOT/2 - d/2, y0, -1]) cube([SLOT + d, y1 - y0, z + 1]);
}

module magnet_pocket(x, upper) {
    zf = ZA + (upper ? 1 : -1) * magnet_offset_in * in;
    yf = TA + magnet_offset_in * in * tan(face_angle_deg);
    ang = upper ? -90 - face_angle_deg : -90 + face_angle_deg;
    translate([x, yf, zf]) rotate([ang, 0, 0])
        translate([0, 0, -magnet_depth_in * in]) cylinder(d = magnet_dia_in * in, h = magnet_depth_in * in + 3);
}

module flip2d() { if (flip_for_fixed_jaw) mirror([1, 0]) children(); else children(); }

// Deboss cutter for printing ON END (+X is up on the printer): the +X-facing wall of every stroke is
// the cavity's ceiling, so it is chamfered 45deg — each step deeper trims one step off the +X edge.
// Local 2D x must be model X. Children: the 2D artwork; cut goes from z=0 (surface) down to z=-DB.
module chamfered_deboss(steps = 4) {
    st = DB / steps;
    for (i = [0 : steps - 1])
        translate([0, 0, -(i + 1) * st]) linear_extrude(st + 0.02)
            intersection() { children(); translate([-(i + 1) * st, 0]) children(); }
    translate([0, 0, -0.01]) linear_extrude(2) children();      // clean break-out above the surface
}

// logo debossed into the sloped back wedge, centered on it
module logo_cut() {
    run  = BT; rise = H - (SEAT + FT);
    ang  = atan2(rise, run);                          // slope angle from horizontal (~60 deg)
    yc   = -BT/2; zc = (SEAT + FT + H)/2;
    translate([L/2, yc, zc]) rotate([ang, 0, 0])
        chamfered_deboss()
            flip2d() resize([logo_width_in * in, 0], auto = true) import(logo_svg, center = true);
}

// text debossed into the top face, centered
module text_cut() {
    translate([L/2, TE/2, H])
        chamfered_deboss()
            flip2d() text(brand_text_str, size = brand_text_size_in * in, font = brand_font,
                          halign = "center", valign = "center", spacing = 1.05);
}

// 90deg V-groove: runs along local Y from 0 to len, centered at local x, V cut into -Z from the z=0 surface
module vgroove(x, len) {
    w = witness_v_in * in;
    translate([x, 0, 0]) rotate([90, 0, 0]) mirror([0, 0, 1])
        linear_extrude(len) polygon([[-w/2, 0.01], [w/2, 0.01], [0, -w/2]]);
}

module witness_cuts() {
    ang = atan2(H - (SEAT + FT), BT);
    for (x = [L/2 - witness_width_in * in / 2, L/2, L/2 + witness_width_in * in / 2]) {
        translate([0, -BT - 1, H]) vgroove(x, TE + BT + 2);                       // across the top face
        translate([0, -BT, SEAT + FT]) rotate([ang, 0, 0]) vgroove(x, witness_slope_len_in * in);   // tick up the wedge
    }
}

module jaw() {
    difference() {
        union() {
            intersection() {
                rotate([90, 0, 90]) linear_extrude(L) profile_2d();
                hull() for (x = [CH, L - CH], y = [-FD + CH, YMAX - CH])
                    translate([x, y, 0]) cylinder(r = CH, h = H, $fn = 16);
            }
            if (side_cheeks) {
                cw = casting_width_in * in / 2 + cheek_clearance_in * in;
                for (x0 = [0, L/2 + cw])
                    translate([x0, -FD, 0]) cube([L/2 - cw, FD, SEAT]);
            }
        }
        if (!(ease_edges && foam_lip)) rotate([90, 0, 90]) translate([0, 0, -1]) linear_extrude(L + 2) vee_wedge_2d();
        for (x = [L/2 - CC/2, L/2 + CC/2]) {
            slot(thru_dia_in * in, x, SH, -FD - 1, YMAX + 5, SLV);
            slot(cbore_dia_in * in, x, SH, wall_under_head_in * in, YMAX + 5, SLV, cbore_open_bottom, teardrop = true);
        }
        if (magnet_pockets)
            for (mx = magnet_x_in) for (u = [true, false]) if (mx * in < L) magnet_pocket(mx * in, u);
        if (brand_logo) logo_cut();
        if (brand_text) text_cut();
        if (witness_marks) witness_cuts();
    }
}

module test_plate() {
    t = 0.2 * in;
    difference() {
        translate([L/2 - CC/2 - 0.5*in, 0, 0]) cube([CC + 1*in, t, 1.0*in]);
        for (x = [L/2 - CC/2, L/2 + CC/2]) slot(thru_dia_in * in, x, SH, -1, t + 1, SLV);
    }
}

if (show_test_plate) test_plate();
else if (print_orientation) rotate([0, -90, 0]) jaw();   // stands on the X=0 end, length along Z
else jaw();
