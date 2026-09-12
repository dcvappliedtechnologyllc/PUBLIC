// Reaction-rod clamshell for the Doyle light-vee jaws — Rev A
// Two mirror halves of the keel v9 body (same double vee, same tee flange, same 0.015" lift) with a D-channel down the
// parting plane that closes on a Geissele Reaction Rod. The rod runs ALONG the jaws; the parting plane is vertical, so
// the vise closes the shell. The rod's vise flats face the jaws, so the clamp goes straight through the flats and the
// torque is reacted by the flat's edges in the channel; the round part of the bore only locates (0.008" clearance).
// The parting faces stop 0.030" short of each other with the rod in, so the clamp load cannot bypass the rod.
// Preload: two rubber bands (#64, doubled) or 1/16" O-rings in 45deg V-grooves 0.08" deep around the whole perimeter
// (self-supporting on the on-end print). The groove runs over the tee flange too, leaving 0.04" of it at the two stations.
// Two loose register pins (printed, or 1/8" x 1/2" steel dowels) in matching holes in both parting faces, so the halves cannot
// shear along the rod before the vise is on. (Rev A had the pins printed on one half; on end they are horizontal 90deg overhangs.)
// PRINT ON END like the keel (print_on_end = true): channel, grooves, pins all vertical. Units: parameters in inches, model mm.
in = 25.4;

/* [Rod — Geissele Reaction Rod, measured 2026-09-10] */
rod_dia_in        = 0.995;   // shank OD
rod_flats_in      = 0.745;   // across the vise flats
rod_flat_len_in   = 4.50;    // length of the flats that sits inside the shell. UNMEASURED: assumed >= shell length. If the flats
                             // are shorter, the channel goes round (full bore) where the rod is round — set this and flat_from_end.
flat_from_end_in  = 0.00;    // where the flats start, measured from the shell's -X end (0 = flats over the whole shell)
bore_clear_in     = 0.008;   // radial clearance on the round part of the bore (locates only)
flat_clear_in     = 0.002;   // clearance on the flats (these seat under the clamp)
part_gap_in       = 0.030;   // gap between the parting faces with the rod seated

/* [Body — keel v9 numbers, do not change without changing the keel] */
shell_length_in    = 3.50;   // see the rod-protrusion arithmetic in the Design Log: the receiver's rear face must clear the jaw end
keel_apex_width_in = 2.50;
face_angle_deg     = 15;
vee_half_height_in = 1.00;
flange_reach_in    = 0.50;
flange_thick_in    = 0.20;
keel_lift_in       = 0.015;
bottom_trim_in     = 0.15;   // keel is 0.30; less here so there is 0.35 in of wall under the bore
rod_axis_z_in      = 1.00;   // rod axis on the apex line (symmetric clamp)

/* [Preload grooves] */
groove_x_in       = 1.40;    // stations at +/- this from centre
groove_depth_in   = 0.08;    // a #64 rubber band (doubled) or a 1/16 in O-ring sits below the vee faces. Deeper than ~0.09 and the
                             // 0.20 in flange is eroded from both sides to nothing (the groove runs round the whole outline)
groove_flat_in    = 0.10;    // flat at the bottom of the V so the band seats instead of wedging
groove_step       = 0.25;    // mm per step of the 45deg walls (one layer)

/* [Register pins] */
pin_dia_in        = 0.125;   // 1/8 in dowel, or the printed pin below
pin_len_in        = 0.50;    // loose pin length; holes are (len - gap)/2 deep each side
pin_hole_clear_in = 0.006;   // radial
print_pins        = true;    // add two printed pins to the plate (lying flat)
pin_x_in          = 1.50;    // +/- from centre
pin_z_in          = 1.74;    // between the bore top (1.50) and the flange underside (1.985)

print_on_end = false;
viewer_assembled = false;
$fn = 96;

L = shell_length_in * in; W = keel_apex_width_in * in; VH = vee_half_height_in * in; KH = 2 * VH;
FR = flange_reach_in * in; FTK = flange_thick_in * in; LIFT = keel_lift_in * in; BT = bottom_trim_in * in;
ZF = KH - LIFT; WF = W - 2 * (ZF - VH) * tan(face_angle_deg); WB = W - 2 * (VH - BT) * tan(face_angle_deg); KT = ZF + FTK;
ZR = rod_axis_z_in * in; RR = rod_dia_in * in / 2; FL = rod_flats_in * in / 2; G = part_gap_in * in;
GD = groove_depth_in * in; GF = groove_flat_in * in; GX = groove_x_in * in;
PD = pin_dia_in * in; PL = pin_len_in * in; PX = pin_x_in * in; PZ = pin_z_in * in;

echo(str("channel: flat at ", (FL + flat_clear_in*in)/in, " from the axis, arcs r ", (RR + bore_clear_in*in)/in,
         "; wall under bore ", (ZR - RR - BT)/in, ", bore top to flange ", (ZF - ZR - RR)/in, "; parting gap ", G/in));

module keel_profile() {   // (Y, Z): the keel v9 outline
    polygon([[-WB/2, BT], [WB/2, BT], [W/2, VH], [WF/2, ZF], [WF/2 + FR, ZF], [WF/2 + FR, KT],
             [-WF/2 - FR, KT], [-WF/2 - FR, ZF], [-WF/2, ZF], [-W/2, VH]]);
}
module body() { rotate([90, 0, 90]) translate([0, 0, -L/2]) linear_extrude(L) keel_profile(); }

module channel() {   // the rod's section with clearance: circle clipped by the flats where the rod has flats, full circle elsewhere
    xa = -L/2 + flat_from_end_in * in; xb = min(L/2, xa + rod_flat_len_in * in);
    x0 = xa <= -L/2 + 0.01 ? -L/2 - 1 : xa;      // run the cutters 1 mm past an end face so nothing is coplanar with it
    x1 = xb >= L/2 - 0.01 ? L/2 + 1 : xb;
    rr = RR + bore_clear_in * in; fl = FL + flat_clear_in * in;
    if (x0 > -L/2 - 0.5) translate([-L/2 - 1, 0, ZR]) rotate([0, 90, 0]) cylinder(r = rr, h = x0 + L/2 + 1);   // round bore behind the flats
    if (x1 < L/2 + 0.5)  translate([x1, 0, ZR]) rotate([0, 90, 0]) cylinder(r = rr, h = L/2 + 1 - x1);          // round bore ahead of them
    translate([x0, 0, ZR]) rotate([0, 90, 0]) intersection() {                                                  // D-D section over the flats
        cylinder(r = rr, h = x1 - x0);
        translate([-rr - 1, -fl, 0]) cube([2 * rr + 2, 2 * fl, x1 - x0]);   // after rotate([0,90,0]): local x -> -Z, local y -> Y
    }
}

module groove_cutters() {   // stepped 45deg V-grooves around the whole outline at +/- GX
    n = ceil(GD / groove_step);
    for (gx = [-GX, GX]) for (i = [0 : n - 1]) {
        d = GD - i * GD / n;                       // depth of this step (deepest at the middle of the groove)
        hw = GF/2 + i * GD / n;                    // half width of this step
        translate([gx - hw, 0, 0]) rotate([90, 0, 90])
            linear_extrude(2 * hw) difference() { offset(delta = 1) keel_profile(); offset(delta = -d) keel_profile(); }
    }
}

module half(s) {   // s = +1 (has the pins) or -1 (has the holes)
    difference() {
        union() {
            difference() {
                body();
                channel();
                translate([-L/2 - 1, s > 0 ? G/2 - W : -G/2, -1]) cube([L + 2, W, KT + 2]);   // the other half plus the parting gap
                groove_cutters();
            }
        }
        for (px = [-PX, PX]) translate([px, s * (G/2 - 0.01), PZ]) rotate([s > 0 ? -90 : 90, 0, 0])
            cylinder(d = PD + 2 * pin_hole_clear_in * in, h = (PL - G) / 2 + 0.5);
    }
}

module both(gap = 20) {
    translate([0, gap/2 + W/2 + FR, 0]) half(1);
    translate([0, -(gap/2 + W/2 + FR), 0]) half(-1);
}
module pins() {   // two loose pins, lying flat beside the halves
    for (i = [0, 1]) translate([-L/2 + 5 + i * 10, 0, PD/2]) rotate([0, 0, 0]) rotate([-90, 0, 0]) translate([0, 0, -PL/2]) cylinder(d = PD, h = PL, $fn = 32);
}

if (viewer_assembled) { half(1); half(-1); } else if (print_on_end) { translate([0, 0, L/2]) rotate([0, -90, 0]) both(); if (print_pins) translate([-W - 2 * FR - 15, 0, 0]) pins(); }
else both();
