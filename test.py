from colorsvg import color_svg_like_file
from manim import *
import random
import numpy as np

class BlochSphere(SpecialThreeDScene):
    CONFIG = {
        "three_d_axes_config": {
            "num_axis_pieces": 1,
            "number_line_config": {
                "unit_size": 2,
                "tick_frequency": 1,
                "numbers_with_elongated_ticks": [0, 1, 2],
                "stroke_width": 2,
            }
        },
        "init_camera_orientation": {
            "phi": 80 * DEGREES,
            # "theta": -135 * DEGREES,
            "theta": 15 * DEGREES,
        },

        "circle_xz_show": False,
        "circle_xz_color": PINK,

        "circle_xy_show": True,
        "circle_xy_color": GREEN,

        "circle_yz_show": False,
        "circle_yz_color": ORANGE,

        
        "sphere_config": {
            "radius": SPHERE_RADIUS,
            "resolution": (60, 60),
        },
        
        "rotate_sphere": True,
        "rotate_circles": False,
        "rotate_time": 5,
        "operators": [
        ],
        "operator_names": [
        ],
        "show_intro": True,

        "wait_time": 2,
        "pre_operators_wait_time": 1.5,
        "final_wait_time": 3,
        "intro_wait_time": 3,
        "intro_fadeout_wait_time": 1,
    }

    def construct(self):
        if self.show_intro:
            self.present_introduction()
        self.init_camera()
        self.init_axes()
        self.init_sphere()
        self.init_states()
        self.init_text()
        self.wait(self.pre_operators_wait_time)

        for o in self.operators:
            self.apply_operator(o)
            self.wait(self.wait_time)
        self.wait(self.final_wait_time)

    def present_introduction(self):
        self.intro_tex_1 = TextMobject(
            "\\begin{flushleft}\n"
            "The State of the Qbit"
            "\\\\"
            "as represented in the Bloch Sphere."
            "\n\\end{flushleft}",
            alignment="",
        )
        # self.intro_tex_1 = TextMobject(
        #     # "\\begin{align*}\n" + "The state of the Qbit" + "\n\\end{align*}",
        #     "\\begin{flalign}\n" + "The state of the Qbit" + "\n\\end{flalign}",
        #     # "The state of the Qbit",
        #     # "\\begin{flushleft}"
        #     # "The state of the Qbit"
        #     # "\\\\"
        #     # "as represented in the Bloch Sphere."
        #     # "\\end{flushleft}",
        #     alignment="",
        #     # template_tex_file_body=TEMPLATE_TEXT_FILE_BODY,
     #        # arg_separator="",
        # )
        self.intro_tex_1.move_to(2*UP)
        self.add(self.intro_tex_1)
        self.play(
            Write(self.intro_tex_1),
            run_time=1.5
        )

        if self.operator_names:
            self.intro_tex_2 = TextMobject(
                "\\begin{flushleft}"
                "The following gates will be applied:"
                "\\\\"
                +
                "\\\\".join(f"{i+1}) {n}" for i,n in enumerate(self.operator_names))
                +
                "\n\\end{flushleft}",
                alignment="",
            )
            self.intro_tex_2.move_to(0.8*DOWN)
            self.add(self.intro_tex_2)
            self.play(
                Write(self.intro_tex_2),
                run_time=2.5
            )

        self.wait(self.intro_wait_time)

        if self.operator_names:
            self.play(
                FadeOut(self.intro_tex_1),
                FadeOut(self.intro_tex_2)
            )
        else:
            self.play(
                FadeOut(self.intro_tex_1)
            )

        self.wait(self.intro_fadeout_wait_time)

    def init_camera(self):
        self.set_camera_orientation(**self.init_camera_orientation)

    def init_axes(self):
        self.axes = self.get_axes()
        self.set_axes_labels()
        self.add(self.axes)

    def _tex(self, *s):
        tex = TexMobject(*s)
        tex.rotate(90 * DEGREES, RIGHT)
        tex.rotate(90 * DEGREES, OUT)
        tex.scale(0.5)
        return tex

    def set_axes_labels(self):
        labels = VGroup()

        zero = tex("\\ket{0}")
        zero.next_to(
            self.axes.z_axis.number_to_point(1),
            Y_AXIS + Z_AXIS,
            MED_SMALL_BUFF
        )

        one = tex("\\ket{1}")
        one.next_to(
            self.axes.z_axis.number_to_point(-1),
            Y_AXIS - Z_AXIS,
            MED_SMALL_BUFF
        )

        labels.add(zero, one)
        self.axes.z_axis.add(labels)

        x = tex("x")
        x.next_to(
            self.axes.x_axis.number_to_point(1),
            -Y_AXIS,
            MED_SMALL_BUFF
        )
        self.axes.x_axis.add(x)

        y = tex("y")
        y.next_to(
            self.axes.y_axis.number_to_point(1),
            Y_AXIS + Z_AXIS,
            MED_SMALL_BUFF
        )
        self.axes.y_axis.add(y)

    def init_sphere(self):
        sphere = self.get_sphere(**self.sphere_config)
        sphere.set_fill(BLUE_E)
        sphere.set_opacity(0.1)
        self.add(sphere)
        self.sphere = sphere

        if self.circle_xy_show:
            self.circle_xy = Circle(
                radius=SPHERE_RADIUS,
                color=self.circle_xy_color,
            )
            self.circle_xy.set_fill(self.circle_xy_color)
            self.circle_xy.set_opacity(0.1)
            self.add(self.circle_xy)

        if self.circle_xz_show:
            self.circle_xz = Circle(
                radius=SPHERE_RADIUS,
                color=self.circle_xz_color,
            )
            self.circle_xz.rotate(90 * DEGREES, RIGHT)
            self.circle_xz.set_fill(self.circle_xz_color)
            self.circle_xz.set_opacity(0.1)
            self.add(self.circle_xz)

        if self.circle_yz_show:
            self.circle_yz = Circle(
                radius=SPHERE_RADIUS,
                color=self.circle_yz_color,
            )
            self.circle_yz.rotate(90 * DEGREES, UP)
            self.circle_yz.set_fill(self.circle_yz_color)
            self.circle_yz.set_opacity(0.1)
            self.add(self.circle_yz)

    def init_text(self):
        """
        for each state, write (with its own color):
            the probabilities
            theta & phi
        """
        # the qquad is used as a placeholder, since the value changes, and the length of the value changes.
        self.tex_zero_vec   = tex("\\ket{BLUE} = ", "\\qquad \\qquad 1", " \\\\ ", "\\qquad 0")
        self.tex_zero_vec.set_color(BLUE)
        self.tex_zero_vec.move_to(Z_AXIS * 2 - Y_AXIS * 4)

        self.tex_zero_theta = tex("\\theta = ", "0.000")
        self.tex_zero_theta.set_color(BLUE)
        self.tex_zero_theta.move_to(Z_AXIS * 1 - Y_AXIS * 4)

        self.tex_zero_phi   = tex("\\phi = ", "0.000")
        self.tex_zero_phi.set_color(BLUE)
        self.tex_zero_phi.move_to(Z_AXIS * 0.5 - Y_AXIS * 4)


        self.tex_one_vec    = tex("\\ket{RED} = ", "\\qquad \\qquad 0", " \\\\ ", "\\qquad 1")
        self.tex_one_vec.set_color(RED)
        self.tex_one_vec.move_to(Z_AXIS * 2 + Y_AXIS * 3.5)

        self.tex_one_theta  = tex("\\theta = ", "180.0")
        self.tex_one_theta.set_color(RED)
        self.tex_one_theta.move_to(Z_AXIS * 1 + Y_AXIS * 4)

        self.tex_one_phi    = tex("\\phi = ", "0.000")
        self.tex_one_phi.set_color(RED)
        self.tex_one_phi.move_to(Z_AXIS * 0.5 + Y_AXIS * 4)

        self.tex_dot_product= tex("\\bra{0}\\ket{1} = ", "\\qquad \\quad 0.000")
        self.tex_dot_product.set_color(WHITE)
        self.tex_dot_product.move_to(- Z_AXIS * 2 + Y_AXIS * 3)

        self.add(
            self.tex_zero_vec,
            self.tex_zero_theta,
            self.tex_zero_phi,

            self.tex_one_vec,
            self.tex_one_theta,
            self.tex_one_phi,

            self.tex_dot_product,
        )

        # the initial values are only used to make enough space for later values
        self.play(
            *self.update_tex_transforms(self.zero, self.one),
            run_time=0.1
        )

    def update_tex_transforms(self, new_zero, new_one):
        zero_state = new_zero.get_vector()
        zero_angles = vector_to_angles(zero_state)
        one_state = new_one.get_vector()
        one_angles = vector_to_angles(one_state)

        dot_product = np.vdot( new_one.get_vector(), new_zero.get_vector())

        return(
            transform(self.tex_zero_vec[1],   complex_to_str(zero_state[0])),
            transform(self.tex_zero_vec[3],   complex_to_str(zero_state[1])),
            transform(self.tex_zero_theta[1], angle_to_str(zero_angles[0]) ),
            transform(self.tex_zero_phi[1],   angle_to_str(zero_angles[1]) ),

            transform(self.tex_one_vec[1],    complex_to_str(one_state[0]) ),
            transform(self.tex_one_vec[3],    complex_to_str(one_state[1]) ),
            transform(self.tex_one_theta[1],  angle_to_str(one_angles[0])  ),
            transform(self.tex_one_phi[1],    angle_to_str(one_angles[1])  ),

            transform(self.tex_dot_product[1],   complex_to_str(dot_product)),
        )

    def init_states(self):
        self.old_zero = self.zero = State(1, 0, r=2)
        self.old_one  = self.one  = State(0, 1, r=2)

        self.zero.set_color(BLUE)
        self.one.set_color(RED)

        self.add(self.zero, self.one)

    def apply_operator(self, operator, verbose=True):
        # preparing the rotation animation
        vg = VGroup(self.old_zero.line, self.old_one.line)
        if self.rotate_sphere:
            vg.add(self.sphere)

        if self.rotate_circles:
            if self.circle_xy_show:
                vg.add(self.circle_xy)
            if self.circle_xz_show:
                vg.add(self.circle_xz)
            if self.circle_yz_show:
                vg.add(self.circle_yz)


        rm = RotationMatrix(operator)

        if verbose:
            print(f"rotating around axis: {rm.axis} by {rm.theta / DEGREES} degrees")

        # preparing the tex update
        new_zero = self.zero.apply_operator(operator)
        new_one = self.one.apply_operator(operator)


        self.play(
            Rotate(
                vg,
                angle=rm.theta,
                axis=rm.axis
            ),
            *self.update_tex_transforms(new_zero, new_one),
            run_time=self.rotate_time
        )

        self.zero = new_zero
        self.one  = new_one

    def apply_operator_old(self, operator, verbose=True):
        if verbose:
            print()
            print("00000")
        new_zero = self.zero.apply_operator(operator)
        if verbose:
            print("11111")
        new_one = self.one.apply_operator(operator)

        self.play(
            Transform(self.old_zero, new_zero),
            Transform(self.old_one,  new_one),
            *self.update_tex_transforms(new_zero, new_one),
        )

        self.zero = new_zero
        self.one  = new_one


class LogoAnimation(ThreeDScene):
    CONFIG={
        "theta_in": 0,
        "theta_end": 0.5*PI,
    }
     
    def construct(self):
        
        '''
        arrow = Arrow()
        axes = ThreeDAxes()
        sphere = ParametricSurface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]), v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        )
        '''
        
        #logo_svg = SVGMobject('QC@UCI Logo_thick.svg').scale(2)
        
        '''
        #for example, if you have four layers
        colors = it.cycle([]) #just an iterator to assign             
                                          #the colors or any other attr
        for sub_mob in logo_svg:
            color = next(colors)
            sub_mob.set_color(color)
        '''
        
        theta = ValueTracker(0)
        
        qubit = TextMobject(r"$\alpha \ket{0} + \beta \ket{1}$")

        square = Square().scale(2)
        logo_png = ImageMobject('QC@UCI Logo_thick.png').scale(2)
        
        self.wait()
        self.play(ShowCreation(qubit))

        self.play(Transform(qubit, square),
                  FadeIn(logo_png, run_time=1.8))
        self.wait()

class Test(Scene):
    CONFIG={
        "theta_in": 0,
        "theta_end": 2*PI,
    }
    def construct(self):
        self.wait(1)
        t_ob = TextMobject(r"$\alpha \ket{0} + \beta \ket{1}$")
   
        t_value = ValueTracker(self.theta_in)
        
        t_tex = DecimalNumber(t_value.get_value())
        t_tex.add_updater(lambda v: v.set_value(t_value.get_value()))
        t_label = TexMobject(r"\theta =")
        
        group = VGroup(t_tex, t_label).scale(2.6)
        t_label.next_to(t_tex, LEFT, buff=0.7,aligned_edge=t_label.get_bottom())
        group.move_to(ORIGIN)
        
        self.play(ShowCreation(t_ob))
        self.play(Transform(t_ob, \
                            TextMobject(r"$A \ket{0} + B e^{\theta} \ket{1}$")))
        
        self.play(ApplyMethod(t_ob.move_to, UP))
        self.play(ShowCreation(group))
        
        self.play(
            t_value.set_value, 2*PI,
            rate_func=linear,
            run_time=10
            )
    
        
class SliderCrankMechanism(Scene):
    CONFIG={
        "a":2,
        "b":-6.5,
        "c":1.7,
        "theta_in":70,
        "theta_end":70-2.5*360,
        "slider_color":RED,
        "crank_color":BLUE,
        "piston_color":GREEN,
        "anchor_color":TEAL,
        "line_stroke":10
    }
    def construct(self):
        O2 = Dot().shift(LEFT*4+DOWN*1.5)
        a  = self.a
        b  = self.b
        c  = self.c
        theta_in  = self.theta_in
        theta_end = self.theta_end
        slider_color = self.slider_color
        piston_color = self.piston_color
        radio = 0.08

        base_down=Line(LEFT*4,RIGHT*4)
        base_down.shift(0.1*DOWN)
        anchor_point = Dot(O2.get_center(),radius=radio)
        semi_circle_anchor = Dot(O2.get_center(),radius=0.2,color=self.anchor_color)
        anchor_rect = Square(side_length=0.4).set_stroke(None,0).set_fill(self.anchor_color,1).move_to(O2.get_center()+DOWN*semi_circle_anchor.get_width()/2)


        anchor_group = VGroup(semi_circle_anchor,anchor_rect)

        slider      = self.position_slider(O2.get_center(),theta_in,a,slider_color)
        theta_3     = np.arcsin((a*np.sin(theta_in*DEGREES)-c)/b)*180/PI
        piston      = self.position_piston(O2.get_center(),theta_in,theta_3,a,b,c,piston_color)
        crank       = Line(slider.get_end(),piston.get_center()).set_stroke(self.crank_color,self.line_stroke)
        point_bm    = Dot(slider.get_end(),radius=radio)
        point_mp    = Dot(crank.get_end(),radius=radio)
        grupo       = VGroup(slider,piston,crank,point_mp,point_bm)

        base_down.next_to(piston,DOWN,buff=0).shift(LEFT)
        self.play(*[FadeIn(objeto)for objeto in [anchor_group,base_down]],
                    ShowCreation(slider),DrawBorderThenFill(piston),ShowCreation(crank),
                    GrowFromCenter(point_mp),GrowFromCenter(point_bm),GrowFromCenter(anchor_point),
                    )
        self.add_foreground_mobject(anchor_point)
        alpha = ValueTracker(self.theta_in)

        def update(grupo):
            dx = alpha.get_value()
            slider       = self.position_slider(O2.get_center(),dx,self.a,self.slider_color)

            theta_3   = np.arcsin(np.sign(dx)*((self.a*np.sin(dx*DEGREES)-self.c)/self.b))

            piston      = self.position_piston(O2.get_center(),dx,theta_3*180/PI,self.a,self.b,self.c,self.piston_color)
            crank    = Line(slider.get_end(),piston.get_center()).set_stroke(self.crank_color,self.line_stroke)
            point_bm    = Dot(slider.get_end(),radius=radio)
            point_mp    = Dot(crank.get_end(),radius=radio)

            nuevo_grupo = VGroup(slider,piston,crank,point_mp,point_bm)
            grupo.become(nuevo_grupo)
            return grupo

        self.play(
            alpha.set_value,self.theta_end,
            UpdateFromFunc(grupo,update),
            run_time=8,rate_func=double_smooth)
        self.wait()

    def position_slider(self,origin,theta_2,length,color):
        end_point_x = length * np.cos(theta_2 * DEGREES)
        end_point_y = length * np.sin(theta_2 * DEGREES)
        end_point = origin + np.array([end_point_x, end_point_y, 0])
        slider = Line(origin,end_point, color=color).set_stroke(None,self.line_stroke)
        return slider

    def position_piston(self,origin,theta_2,theta_3,a,b,c,color):
        d = a * np.cos(theta_2 * DEGREES) - b * np.cos(theta_3 * DEGREES)
        end_point = origin + RIGHT * d + UP * c
        piston = Rectangle(color=color, height=1, witdh=1.5)\
                 .set_fill(color,0.7).scale(0.7).move_to(origin+RIGHT * d + UP*c)
        return piston

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()                    # create a circle
        circle.set_fill(PINK, opacity=0.5)   # set color and transparency
        circle.move_to(RIGHT * 2)
        
        square = Square()                    # create a square
        square.flip(RIGHT)                   # flip horizontally
        square.rotate(-3 * TAU / 8)          # rotate a certain amount
        square.move_to(LEFT * 2)

        self.wait(1)
        self.play(ShowCreation(square))      # animate the creation of the square
        self.play(Transform(square, circle)) # interpolate the square into the circle
        self.play(FadeOut(square))           # fade out animation
        self.wait(1)
        
        self.play(ShowCreation(circle))
        self.play(ApplyMethod(circle.shift, UP), run_time=1)
        self.play(ApplyMethod(circle.shift, LEFT), run_time=1)
        self.play(ApplyMethod(circle.shift, DOWN), run_time=1)
        self.play(ApplyMethod(circle.shift, RIGHT), run_time=1)
        self.wait(1)
        
class Example3DNo1(ThreeDScene):
    def construct(self):
        circle = Circle()
        arrow = Arrow()
        
        axes = ThreeDAxes()
        sphere = ParametricSurface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]), v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        )

        self.wait(1)
        self.play(Transform(circle, sphere))
        self.play(ShowCreation(axes))
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Transform(sphere, circle))
        self.play(ShowCreation(arrow))
        self.wait(1)