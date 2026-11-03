# Fabrication examples

These are teaching prototypes and snapshots of the saved default parameters. Regenerate exports after changing the Blender graphs. Physical fit and printer settings have not been tested on a machine.

- **Small print:** 45 × 36 × 22 mm, with its broad face on Z = 0. Inspect the layer preview before printing.
- **Modular parts:** nine separate parts in a spaced print layout, with three aperture sizes. Pitch 20 mm shows how the cells assemble; Pitch 26 mm separates them for printing. Test a joint and develop a fastening/backing strategy.
- **Fit coupon:** nominal 3 mm stock, with trial hole diameters 3.1, 3.3 and 3.5 mm. Test the actual material, machine and rod.
- **Sections:** 12 numbered parts, two holes per part and 22 spacer rings. Use two nominal 3 mm rods approximately 72 mm long; determine end retention through the prototype. The part and spacer thickness is 3 mm, giving a 6 mm section interval and a 69 mm stack.
- **Cutting layout:** an example 400 × 300 mm sheet; confirm the available stock. SVG coordinates are millimeters. Black paths are closed cutting boundaries. Blue labels are a separate optional engraving group. Kerf compensation has not been applied.

Match Count, Sheet Thickness and Hole Radius in the registered-section, cutting-layout and spacer scenes before producing a new cutting file. The scenes are separate examples with independent modifier values. The geometry within each scene remains parametric.

The original curved volume extends beyond the first and last sampled planes. The section model is a finite, cropped interpretation of that volume. Compare it with the source rather than claiming an exact reconstruction.

The required physical outputs are the CSG print (P2b) and laser-cut volume (P4b). The modular print is an optional reference. The small-print STL demonstrates orientation and export; students fabricate their own CSG object. Use the cutting example to understand registration and layout, then generate slices from the chosen P4a volume. Follow the current briefs for design development, physical testing, documentation and the final booklet.
