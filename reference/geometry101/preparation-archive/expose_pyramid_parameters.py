import bpy
import os

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'
pyramid = bpy.data.node_groups['002-point in middle']
boolean = bpy.data.node_groups['06 - Boolean']
source_specs = [('Value', 'Width', 1.1), ('Value.001', 'Depth', 1.2), ('Value.002', 'Height', 1.2)]
links = []
for node_name, parameter, default in source_specs:
    value_node = pyramid.nodes[node_name]
    for connection in value_node.outputs[0].links:
        links.append((parameter, connection.to_node, connection.to_socket.identifier))

for item in list(pyramid.interface.items_tree):
    if item.item_type == 'SOCKET' and item.in_out == 'INPUT' and item.name == 'Geometry':
        pyramid.interface.remove(item)

def expose(group):
    for _, name, default in source_specs:
        s = group.interface.new_socket(name=name, in_out='INPUT', socket_type='NodeSocketFloat')
        s.default_value = default
        s.min_value = 0.01
        s.max_value = 10.0
        s.description = {'Width':'Pyramid base size along X.', 'Depth':'Pyramid base size along Y.', 'Height':'Pyramid apex height above the base.'}[name]

expose(pyramid)
inputs = pyramid.nodes['Group Input']
for parameter, target, identifier in links:
    socket = next(s for s in target.inputs if s.identifier == identifier)
    pyramid.links.new(inputs.outputs[parameter], socket)
for name, _, _ in source_specs:
    pyramid.nodes.remove(pyramid.nodes[name])

parameter_frame = pyramid.nodes['Frame.005']
parameter_frame.label = 'PARAMETERS | Width / Depth / Height'
parameter_frame.location = (-950, 60)
parameter_frame.width = 300
parameter_frame.height = 240
inputs.parent = parameter_frame
inputs.location = (30, -50)
inputs.width = 230
for name in ['Frame.006', 'Frame.007']:
    pyramid.nodes.remove(pyramid.nodes[name])
intro = pyramid.nodes['Frame.008']
intro.text.clear()
intro.text.write(
    'Three exposed parameters: Width (X), Depth (Y), Height (Z).\n'
    'Four corners stay on Z = 0. The apex is (X/2, Y/2, Z).\n'
    'Your four triangles form the sides. Add the bottom to close the mesh.\n'
    'A closed mesh encloses volume: 5 vertices / 8 edges / 5 faces.\n'
    'TRY: change Height in the GeometryNodes modifier.\n'
)

# Expose the same three sockets on the final exercise; the cube stays fixed.
expose(boolean)
outer_inputs = boolean.nodes.new('NodeGroupInput')
frame = next(n for n in boolean.nodes if n.type == 'FRAME' and n.label.startswith('B |'))
frame.width = 540
frame.height = 260
outer_inputs.parent = frame
outer_inputs.location = (25, -50)
outer_inputs.width = 170
pyramid_node = boolean.nodes['Group']
pyramid_node.location = (245, -50)
pyramid_node.width = 270
for _, name, default in source_specs:
    pyramid_node.inputs[name].hide = False
    pyramid_node.inputs[name].default_value = default
    boolean.links.new(outer_inputs.outputs[name], pyramid_node.inputs[name])

for scene_name in ['05 - Solid', '06 - Boolean']:
    obj = bpy.data.scenes[scene_name].view_layers[0].objects.active
    mod = obj.modifiers['GeometryNodes']
    for s in mod.node_group.interface.items_tree:
        if s.item_type == 'SOCKET' and s.in_out == 'INPUT':
            getattr(mod.properties.inputs, s.identifier).value = s.default_value
    obj.update_tag()

intro = boolean.nodes['Frame']
intro.text.clear()
intro.text.write(
    'Start with two closed solids: a cube and the pyramid built in 05.\n'
    'DIFFERENCE = A minus B. Remove the overlapping pyramid volume.\n'
    'Transform Geometry places the cube across the pyramid.\n'
    'TRY: change pyramid Width, Depth, or Height in the modifier.\n'
)
caption = next(n for n in boolean.nodes if n.type == 'FRAME' and n.label.startswith('ONE PYRAMID'))
caption.label = 'REUSE OUR PYRAMID'
caption.text.clear()
caption.text.write(
    'The same pyramid construction, with exposed parameters.\n'
    'Select its group and press Tab to inspect the points and faces.\n'
    'Each use has its own Width, Depth, and Height.\n'
    'Later: vary Height with an attractor, then array the blocks.\n'
)

notes = bpy.data.texts['START HERE - Geometry 101']
body = notes.as_string()
body = body.replace('The three Value nodes control width X, depth Y, and height Z.',
                    'The exposed Width, Depth, and Height inputs control X, Y, and Z.\nChange them in the GeometryNodes modifier (wrench tab). Group Input feeds the nodes.')
body = body.replace('This is the same pyramid used in the Boolean exercise, not a separate copy.',
                    'The Boolean reuses this same pyramid node-group definition with its own input values.')
body = body.replace('Change its three Value parameters, or change them in 05 - Solid; both update.',
                    'Width, Depth, and Height are exposed on the pyramid group and on this modifier.\nThe Solid and Boolean exercises share the construction; their input values are independent.')
notes.clear()
notes.write(body)
with open(os.path.join(FOLDER, 'Geometry101-teaching-notes.txt'), 'w', encoding='utf-8') as f:
    f.write(body)

pyramid.update_tag()
boolean.update_tag()
result = {'pyramid_inputs':[s.name for s in pyramid.interface.items_tree if s.item_type=='SOCKET' and s.in_out=='INPUT'],
          'boolean_inputs':[s.name for s in boolean.interface.items_tree if s.item_type=='SOCKET' and s.in_out=='INPUT'],
          'pyramid_node_inputs':[s.name for s in pyramid_node.inputs]}
