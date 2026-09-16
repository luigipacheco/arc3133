# 01 · Constructive Solid Geometry

Open [Intro-Geometry-Nodes.blend](Intro-Geometry-Nodes.blend), scene **01 - CSG example**. This is the instructor's example with short Frame annotations.

1. **Intersection:** keep the volume shared by a cube and sphere.
2. **Rotation and Union:** rotate copies of one cylinder 90 degrees about X and Y. Union the three cylinders.
3. **Difference:** subtract the cylinders from the first solid.

A **parameter** is a value you can change, such as Radius. A **vector** has three components: X, Y and Z. Transform Geometry controls Translation, Rotation and Scale.

Change Cylinder Radius first. Undo, then change Cube Size or Sphere Radius. Predict what each change will do. Make three variants and diagram the order of operations.

Parameters are on the native nodes in this example, not exposed in the modifier. Native node names and the instructor's final geometry are preserved. Press **Home** over the node editor to fit the graph.

**Optional comparison:** connect Join Geometry to Group Output. It collects both meshes without calculating a solid union. Reconnect the final Mesh Boolean to return to the assignment result.

[Session index](../README.md) · [Screenshot index](../../../images/blender/README.md)
