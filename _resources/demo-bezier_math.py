from fontTools.misc.bezierTools import splitCubicAtT, splitQuadraticAtT
from fontTools.pens.basePen import decomposeSuperBezierSegment

Variable([
    dict(name="point_amount", ui="EditText", args=dict(text='1')),
    dict(name="show_curve", ui="CheckBox"),
    dict(name="super_bezier", ui="CheckBox"),
    dict(name="factor", ui="Slider", args=dict(value=0, minValue=0, maxValue=1)),
], globals())

w, h = 1920, 1080

shape_w, shape_h = 1800, 1000
w_margin, h_margin = (w-shape_w)/2, (h-shape_h)/2

fg = (1,1,1,1)
bg = (0,0,0,1)
highlight1 = (1,0,1,1)
highlight2 = (0,0.8,1,1)
highlight3 = (0,1,0,1)
highlight4 = (1,0.2,0.2,1)
highlight5 = (1,0.9,0,1)
highlight_colors = [highlight1, highlight2, highlight3, highlight4, highlight5]
highlight_colors = highlight_colors*10
point_radius  = 35
handle_radius = 20
text_size = 24
curve_stroke_thickness = 4
quartic_plus_res = 800

names = {
    0: "Non-existent",
    1: "Linear",
    2: "Quadratic",
    3: "Cubic",
    4: "Quartic",
    5: "Quintic",
    6: "Sextic",
    7: "Septic",
    10: "Decic",
    }

def draw_centered_oval(x, y, radius):
    oval(x-radius/2, y-radius/2, radius, radius)
    
def get_midpoint(point1, point2, factor):
    mid_point_x = (point2[0] - point1[0])*factor + point1[0]
    mid_point_y = (point2[1] - point1[1])*factor + point1[1]
    return (mid_point_x, mid_point_y)
    
def get_meta_points(points, factor):
    next_level_points = []
    for i, point in enumerate(points):
        if i == len(points) - 1:
            break
        next_level_points.append(get_midpoint(points[i], points[i+1], factor))
    return next_level_points
    
def get_all_meta_points(points, factor):
    all_meta_points = []
    all_meta_points.append(get_meta_points(points, factor))
    for i in range(len(points)-2):
        all_meta_points.append(get_meta_points(all_meta_points[i], factor))
    return all_meta_points
    
def draw_superbezier_curve(points, factor):
    prev_subsegment = None
    for subsegment in decomposeSuperBezierSegment(points[1:]):
        subsegment = list(subsegment)
        print(prev_subsegment, subsegment)
        if prev_subsegment == None:
            draw_curve([points[0]] + subsegment, factor)
            prev_subsegment = subsegment
        else:
            draw_curve([prev_subsegment[-1]] + subsegment, factor)
            prev_subsegment = subsegment
    
    
def draw_curve(all_points, factor):
    all_meta_points = get_all_meta_points(all_points, factor)
    
    # Draw the curve
    if show_curve == True:
        if super_bezier == True:
            fill(None)
            points_to_draw_curve = all_points
            if len(all_points) == 4:
                points_to_draw_curve = splitCubicAtT(*all_points, factor)[0]
            elif len(all_points) == 3:
                points_to_draw_curve = splitQuadraticAtT(*all_points, factor)[0]
            stroke(*fg)
            strokeWidth(curve_stroke_thickness)
            bez = BezierPath()
            bez.moveTo(points_to_draw_curve[0])
            bez.curveTo(*points_to_draw_curve[1:])
            drawPath(bez)
        else:
            for i in range(quartic_plus_res):
                local_factor = i/quartic_plus_res
                if local_factor >= factor:  # Only draw up until the active dot
                    break
                # Draw an oval up until the point to fake the curve (pens won't draw quartic+)
                stroke(None)
                fill(*fg)
                fake_meta_point = get_all_meta_points(all_points, local_factor)[-1][0]
                draw_centered_oval(fake_meta_point[0], fake_meta_point[1], curve_stroke_thickness)
    
    # Draw the points
    for point in [all_points[0], all_points[-1]]:
        fill(*fg)
        stroke(None)
        draw_centered_oval(point[0], point[1], point_radius)
    
    # Draw the handle dots and dashed lines
    prev_point = None
    for point in all_points:
        stroke(None)
        fill(1)
        draw_centered_oval(point[0], point[1], handle_radius) 
        # Draw the dashed lines
        if prev_point != None:
            strokeWidth(1)
            fill(None)
            stroke(*fg)
            lineDash(8, 8)
            line(prev_point, point)
        prev_point = point
    
    # Draw the handle lines
    if len(all_points) > 3:
        for (point1, point2) in [(all_points[0], all_points[1]), (all_points[-2], all_points[-1])]:
            fill(None)
            lineDash(None)
            stroke(*fg)
            strokeWidth(2)
            line(point1, point2)

    # Draw progress midpoints (all levels)
    for i, level in enumerate(all_meta_points):
        highlight = highlight_colors[i]
        prev_point = None
        for point in level:
            stroke(None)
            fill(*highlight)
            midpoint_radius = handle_radius
            if i == len(all_meta_points)-1:
                fill(*fg)
                midpoint_radius = handle_radius*2
            draw_centered_oval(point[0], point[1], midpoint_radius) 
            if prev_point != None:
                lineDash(None)
                fill(None)
                stroke(*highlight)
                line(prev_point, point)
            prev_point = point
     
newPage(w,h)
fill(*bg)
rect(0,0,w,h)

fill(*fg)
fontSize(text_size)
font('Helvetica')

name_key = int(int(point_amount)-1)
preface = ""
if super_bezier == True:
    preface = "Super-Bezier Truly Cubic But Sort Of "
    
if name_key in names.keys():
    name = preface + names[name_key]
else:
    name = f"{preface}{name_key}th order"
    
text(f"{name} Bézier curve", (40, 40), align='left')
text(f"{int(factor*100)}% rendered", (w-40, 40), align='right')

# ===========================

point_amount = int(point_amount)

# Random higher order curves
random_points = []
if point_amount > 1:
    u_w, u_h =  (w-w_margin*2)/(point_amount-1), (h-h_margin*2)/(point_amount-1)
    for i in range(point_amount):
        random_points.append((w_margin + u_w*i, randint(h_margin, h-h_margin)))

static = [(100, 100), (216, 130), (202, 314), (382, 276), (400, 400)]

curves = {
    1: [(w/2, h/2)],
    2: [(60, 170), (1860, 1013)],
    3: [(60, 999), (60, 200), (1860, 200)],
    4: [(290, 150), (290, 660), (819, 1000), (1700, 1000)],
    # 4: [(60, 999), (60, 200), (1860, 200), (1860, 200)],  # Cubic trying to be quadratic
    5: [(300, 978), (60, 600), (960.0, 60), (1800, 600), (1600, 979)],
    6: [(60, 140), (60, 674), (609, 1000), (1860, 1000), (1000, 60), (1000, 500)],
    7: [(60, 134), (60, 820), (600, 1000), (600, 200), (1260, 60), (1560, 1000), (1860, 528)],
    8: [(60, 620), (317, 200), (574, 200), (1400, 1000), (1500, 1000), (1345, 200), (1860, 200), (1860, 945)],
    9: [(60.0, 213), (285.0, 975), (510.0, 169), (735.0, 272), (960.0, 990), (1185.0, 300), (1410.0, 720), (1635.0, 545), (1860.0, 834)],
    15: [(60, 823), (188, 208), (317, 922), (445, 1000), (574, 913), (702, 530), (831, 520), (960, 871), (1088, 414), (1217, 200), (1345, 280), (1474, 1000), (1602, 1034), (1731, 200), (1860, 138)],
    23: [(60.0, 199), (141.8181818181818, 977), (223.63636363636363, 816), (305.45454545454544, 470), (387.27272727272725, 582), (469.09090909090907, 828), (550.9090909090909, 55), (632.7272727272727, 556), (714.5454545454545, 362), (796.3636363636363, 807), (878.1818181818181, 925), (960.0, 425), (1041.8181818181818, 468), (1123.6363636363635, 614), (1205.4545454545455, 380), (1287.2727272727273, 284), (1369.090909090909, 188), (1450.9090909090908, 300), (1532.7272727272725, 175), (1614.5454545454545, 462), (1696.3636363636363, 983), (1778.181818181818, 663), (1860.0, 640)]

    }

print("Random points for the chosen point_amount:\n")
print(random_points)

if point_amount in curves.keys():
    points = curves[point_amount]
else:
    points = random_points

if super_bezier == True and len(points) > 3:
    draw_superbezier_curve(points, factor)
else:
    draw_curve(points, factor)




    
    
    