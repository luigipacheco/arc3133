# 06 · Point Clouds and Volumes

Open [Point-Clouds-and-Volumes.blend](Point-Clouds-and-Volumes.blend) in Blender 5.2.1 LTS or a compatible newer version.

Use the Scene selector in numbered order. Select the lesson object to see its Geometry Nodes. Change the exposed parameters in the modifier; press Home over the node editor to fit the graph.

| Scene | Exercise |
|---|---|
| 01 - Import points | IMPORT SAMPLES, NOT FACES |
| 02 - Analyze points | USE AN EXTERNAL CONDITION TO FILTER THE CLOUD |
| 03 - Points to volume | SAMPLES BECOME A SAMPLED DENSITY VOLUME |

Native node names are retained. Short explanations and things to try are in Frames. Save your own working copy.

**Keep `teaching-courtyard.ply` beside this Blender file.** The Import PLY node uses a relative path. This is a synthetic teaching dataset, not a surveyed site. [Dataset and provenance](teaching-courtyard.json).

The final output uses small mesh spheres to display the samples. To inspect the actual 1,806 source points, Ctrl+Shift+click **Mesh to Points**, then choose **Viewer Node → Point Cloud → Point** in the Spreadsheet. The display mesh has a different vertex count. See the [Viewer documentation](https://docs.blender.org/manual/sv/5.2/modeling/geometry_nodes/output/viewer.html).

[Course file index](../README.md) · [Current syllabus](../../../syllabus/ARC3133_Syllabus_Fall2026_STUDENT.md)
