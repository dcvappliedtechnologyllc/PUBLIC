// Handwheel adapter for the Doyle 4-1/2" vise screw — Rev D geometry (Rev C printed: bore had no interference -> tightened; bar seat
// depth was dead-on -> untouched; rib walls were taller than the bar so the ties hovered -> cut down to just below the bar top so they
// cinch on it). Rev E = this solid + face art (full DCV logo, "LEFTY LOOSE / RIGHTY TIGHT" arc) debossed 0.68 mm into the front face by
// handwheel_face.py (manifold3d), which reads the Rev D STL exported from here. Render this file plain -> vise_handwheel_D_plain_PRINT.stl.
// Slides over the Ø38 hub from the front (through bore), a rib across the back carries an open channel that
// drops over the sliding T-bar (Ø15) on both sides of the hub. Two cable ties, one each side, pass through the
// plate and across the channel mouth to hold the bar in. The hub sticks out through the front — how far depends
// on where the bar sits in the hub, so nothing here needs that number.
// PRINT FACE DOWN (front face on the bed), no support. Units: mm (the vise was measured in mm); inches in comments.

/* [Vise — measured] */
hub_dia        = 38;     // hub OD  (1.50")
bar_dia        = 15;     // T-bar OD (0.59")
ball_dia       = 24;     // ball ends, guess; only used for the preview
bar_len        = 220;    // preview only: 6-3/4" between the rubber washers + ~1" of rubber/ball each end

/* [Wheel] */
wheel_dia      = 165;    // 6.50" — 6-3/4" of bar between the rubber washers; rim stops 1/8" short of each, balls + rubber outside
plate_t        = 12;     // face plate thickness (0.47")
scallops       = 12;     // finger scallops around the rim
scallop_depth  = 4;      // radial amplitude of the scallops
front_chamfer  = 1.5;    // bed-side edge (prints as a 45deg overhang)
back_round     = 3;      // back-side rim edge fillet
hub_clear      = 0.4;    // bore = hub + this (Rev C at 1.0 + ribs came out with no interference at all)
bar_clear      = 1.0;    // channel = bar + this

/* [Crush ribs — tap-on fit on the hub. The bore stays at clearance; six small ribs stand proud of it and
   interfere with the hub, so they crush/shave as the wheel is tapped on and hold it tight. Kept clear of
   the channel (no ribs at 0/180 deg). Lead-in taper on the entry (back) side.] */
crush_ribs        = 6;
rib_interference  = 0.8;    // on diameter: rib crests sit at hub_dia - this (0.031"). Rev C at 0.4 did nothing.
rib_base_w        = 2.4;    // rib width at the bore wall
rib_leadin        = 2.5;    // taper to zero over this much of the entry side

/* [Bar rib + channel] */
rib_wall       = 6;      // channel wall thickness each side
rib_height     = 11.5;   // rib height off the back of the plate: top lands 0.5 mm BELOW the bar top (bar axis at 16, top at 23.5),
                         // so the tie notch floor (21) is under the bar crown and the tie wraps the bar instead of hovering over it
seat_depth     = 4;      // half-round seat for the bar cut into the plate's back face, so the bar nests below the rib floor

/* [Cable ties] */
tie_w          = 5.5;    // slot for a 4.8 mm (3/16") tie
tie_t          = 2.2;
tie_r          = 52;     // radius of the tie stations (mid-span of the exposed bar: hub edge is r=19.5, rim r=82.5)
tie_notch      = 2.5;    // notch across the rib walls so the strap lies flat over the channel mouth
tie_head_recess= 1.5;    // shallow recess on the front face for the strap between the two slots

$fn = 96;

R  = wheel_dia / 2;
HB = hub_dia + hub_clear;      // bore
CW = bar_dia + bar_clear;      // channel width
RW = CW + 2 * rib_wall;        // rib width
BZ = plate_t + seat_depth + 0;  // bar axis height above the front face when seated: seat bottom at plate_t - seat_depth ... see below

// Bar axis sits at z = plate_t - seat_depth + CW/2 (seat is a half-round Ø CW into the back of the plate)
bar_z = plate_t - seat_depth + CW / 2;

module scalloped_disc(h) {
    // rim: R - scallop_depth + scallop_depth*cos(n*theta)  (smooth lobes, nothing to catch a palm)
    pts = [for (i = [0 : 359]) let(t = i, r = R - scallop_depth + scallop_depth * cos(scallops * t)) [r * cos(t), r * sin(t)]];
    linear_extrude(h) polygon(pts);
}

module plate() {
    // stepped chamfer on the bed side and a stepped round on the back side (hull() would convexify the scallops)
    n = 6;
    union() {
        for (i = [0 : n - 1]) {
            z0 = i * front_chamfer / n; d = front_chamfer * (1 - i / n);
            translate([0, 0, z0]) linear_extrude(front_chamfer / n + 0.01) offset(delta = -d) projection() scalloped_disc(1);
        }
        translate([0, 0, front_chamfer]) scalloped_disc(plate_t - front_chamfer - back_round);
        for (i = [0 : n - 1]) {
            a0 = i * 90 / n; a1 = (i + 1) * 90 / n;
            z0 = plate_t - back_round + back_round * sin(a0); z1 = plate_t - back_round + back_round * sin(a1);
            d = back_round * (1 - cos(a1));
            translate([0, 0, z0]) linear_extrude(max(z1 - z0, 0.01) + 0.01) offset(delta = -d) projection() scalloped_disc(1);
        }
    }
}

module rib() {
    // full-diameter rib on the back, trimmed to the disc outline, channel down the middle
    intersection() {
        translate([-R, -RW/2, plate_t - 0.01]) cube([2 * R, RW, rib_height + 0.01]);
        translate([0, 0, plate_t - 1]) scalloped_disc(rib_height + 2);
    }
}

module cuts() {
    // through bore for the hub
    translate([0, 0, -1]) cylinder(d = HB, h = plate_t + rib_height + 2);
    // bar channel: open to the back, full length
    translate([-R - 1, -CW/2, plate_t - seat_depth + CW/2]) cube([2 * R + 2, CW, rib_height + seat_depth + 1]);
    // half-round seat for the bar, sunk into the back of the plate
    translate([0, 0, bar_z]) rotate([0, 90, 0]) cylinder(d = CW, h = 2 * R + 2, center = true);
    // cable-tie stations: two slots through the plate either side of the rib, a notch across the rib walls,
    // and a strap recess on the front face between the slots
    for (s = [-1, 1]) {
        for (t = [-1, 1])
            translate([s * tie_r - tie_w/2, t * (RW/2 + tie_t/2 + 0.5) - tie_t/2, -1]) cube([tie_w, tie_t, plate_t + 2]);
        translate([s * tie_r - tie_w/2, -RW/2 - 1, plate_t + rib_height - tie_notch]) cube([tie_w, RW + 2, tie_notch + 1]);
        translate([s * tie_r - tie_w/2 - 0.5, -(RW/2 + tie_t + 1), -1]) cube([tie_w + 1, RW + 2 * tie_t + 2, tie_head_recess + 1]);
    }
}

module crush_rib_set() {
    crest_r = (hub_dia - rib_interference) / 2;        // where the rib crest sits
    h       = HB / 2 - crest_r;                        // rib height off the bore wall
    angles  = [for (i = [0 : crush_ribs - 1]) i * 360 / crush_ribs + 180 / crush_ribs];   // straddle the channel axis, never on it
    for (a = angles) rotate([0, 0, a])
        hull() {
            // rounded crest, full height minus the lead-in
            translate([crest_r + 0.6, 0, 0]) cylinder(d = 1.2, h = plate_t - rib_leadin, $fn = 24);
            // base at the wall, full height (buried 0.5 into the wall so the union is clean)
            translate([HB / 2 - 0.5, -rib_base_w / 2, 0]) cube([1, rib_base_w, plate_t]);
            // lead-in: crest runs out to the wall at the back face
            translate([HB / 2 - 0.1, 0, plate_t - 0.01]) cylinder(d = 0.2, h = 0.01, $fn = 12);
        }
}

module wheel() {
    union() {
        difference() {
            union() { plate(); rib(); }
            cuts();
        }
        // ribs only where the bore wall exists (outside the bar seat / channel)
        difference() {
            crush_rib_set();
            translate([-R - 1, -CW/2, plate_t - seat_depth + CW/2]) cube([2 * R + 2, CW, rib_height + seat_depth + 1]);
            translate([0, 0, bar_z]) rotate([0, 90, 0]) cylinder(d = CW, h = 2 * R + 2, center = true);
        }
    }
}

module preview_vise() {   // hub + bar + balls, for the section picture only
    %translate([0, 0, bar_z - 14]) cylinder(d = hub_dia, h = 50);          // hub, end face 14 mm in front of the bar axis (guess)
    %translate([0, 0, bar_z]) rotate([0, 90, 0]) cylinder(d = bar_dia, h = bar_len - ball_dia, center = true);
    %for (s = [-1, 1]) translate([s * (bar_len - ball_dia) / 2, 0, bar_z]) sphere(d = ball_dia);
}

wheel();
if ($preview) preview_vise();
