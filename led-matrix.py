#
# led-matrix.py
#
# grid with diffusor for 16x16 LED-matrix (https://de.aliexpress.com/item/4000544584524.html)
#
# Print with 0.2 mm layer height, first two layers in white filament and then filament change to black for the grid matrix
#

import cadquery as cq
from cadquery import exporters

pcb_x = 160.0 # PCB x size
pcb_y = 160.0 # PCB y size
pcb_th = 2.0 # PCB thickness
pcb_cl = 0.4 # PCB clearance to outer wall

wall_th = 1.2 # outer wall thickness

diff_h = 0.4 # diffusor height

cnt_x = 16 # LED count in X
cnt_y = 16 # LED count in Y

div_th = 1.0 # divider wall thickness
div_hx = 8.0 # X divider height 
div_hy = 9.0 # Y divider height

###

box_x = pcb_x + 2*pcb_cl + 2*wall_th # over all X size
box_y = pcb_y + 2*pcb_cl + 2*wall_th # over all Y size

div_cnt_x = cnt_x - 1 # number of X dividers
div_cnt_y = cnt_y - 1 # number of Y dividers

div_dist_x = pcb_x / cnt_x # divider X distance
div_dist_y = pcb_y / cnt_y # divider X distance


# diffusor sketch
s_diff = (cq.Sketch()
          .rect(box_x, box_y)
)

f_diff = (cq.Workplane("XY")
          .placeSketch(s_diff)
          .extrude(diff_h)   
)

f1 = (cq.Workplane("XY")) #basic workplane object

# create X dividers (perpendicular to X axis)
f_x_div = (cq.Workplane("XY")
       .rect(div_th, box_y)
       .extrude(div_hx)
)

div_x_pts = [(x * div_dist_x - (div_dist_x*(div_cnt_x - 1))/2
             ,0
             ) for x in range(0, div_cnt_x)]

f1x = f1.pushPoints(div_x_pts).eachpoint(lambda loc: f_x_div.val().moved(loc))

# create Y dividers (perpendicular to Y axis)
f_y_div = (cq.Workplane("XY")
       .rect(box_x, div_th)
       .extrude(div_hy)
)

div_y_pts = [(0
             ,y * div_dist_y - (div_dist_y*(div_cnt_y - 1))/2
             ) for y in range(0, div_cnt_y)]

f1y = f1.pushPoints(div_y_pts).eachpoint(lambda loc: f_y_div.val().moved(loc))

# create outer box wall with 

f_wall = (cq.Workplane("XY")
       .rect(box_x, box_y)
       .rect(box_x - 2*(wall_th + div_th/2), box_y - 2*(wall_th + div_th/2)) # PCB support surface below PCB
       .extrude(div_hy)
       .faces(">Z").workplane()
       .rect(box_x, box_y)
       .rect(box_x - 2*wall_th, box_y - 2*wall_th) # outer rim around PCB
       .extrude(pcb_th)
)

result = f_diff.union(f1x)
result = result.union(f1y)
result = result.union(f_wall)

#round side edges
result = result.edges("|Z and (>X or <X)").fillet(1.2)

show_object(result)

filename = f"led-matrix-{cnt_x}x{cnt_y}.stl"
exporters.export(result, filename, tolerance=0.99, angularTolerance=2)