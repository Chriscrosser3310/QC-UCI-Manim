from colorsvg import color_svg_like_file
from manim import *
import random
import numpy as np

class ChangePointRotation(ThreeDScene):
    def construct(self):
        axis=ThreeDAxes()
        self.add(axis)
        phi_init=70 * DEGREES
        theta_init=-135 * DEGREES
        self.set_camera_orientation(phi=phi_init,theta=theta_init)
 
        self.begin_ambient_camera_rotation(rate=0.7)
        self.wait(5)
        self.stop_ambient_camera_rotation()
 
        self.wait()
 
        vector=np.array([-2,-3,1])
 
 
        cx=vector[0]*RIGHT
        cy=vector[1]*UP
        cz=vector[2]*OUT
        dashed_lines=VGroup()
        for ci,cf in zip([cx,cy,cx+cy,cz],[cx+cy,cx+cy,cx+cy+cz,cx+cy+cz]):
            dashed_lines.add(DashedLine(ci,cf))
        dashed_lines.set_color(RED)
 
        sphere=Sphere(radius=0.2).move_to(vector)
 
        self.play(ShowCreation(sphere))
 
        self.play(ShowCreation(dashed_lines))
 
        self.wait(2)
 
        self.move_camera(theta=theta_init,phi=phi_init)
        self.wait()
 
        self.move_camera(distance=self.camera.distance,
            frame_center=vector
            )
 
        self.wait()
 
        self.begin_ambient_camera_rotation(rate=0.7)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait()

class Test(ThreeDScene):
    def construct(self):
        circle = Circle()
        arrow = Arrow().put_start_and_end_on(ORIGIN, UP)
        geo_group = VGroup(circle, arrow)
        
        self.wait()
        self.play(ShowCreation(arrow))
        self.play(Rotate(geo_group))

class LogoAnimation(Scene):
    def construct(self):
        
        circle = Circle().set_fill(BLACK).set_stroke(WHITE, opacity=0.6)
        sphere = Sphere().set_fill(GREY).set_stroke(WHITE)
        arrow = Arrow().put_start_and_end_on(ORIGIN, UP)
        geo_group = VGroup(circle, arrow)

        ket_0 = TextMobject(r"$\ket{0}$").next_to(circle, UP)
        ket_1 = TextMobject(r"$\ket{1}$").next_to(circle, DOWN)
        ket_p = TextMobject(r"$\ket{+}$").next_to(circle, LEFT)
        ket_m = TextMobject(r"$\ket{-}$").next_to(circle, RIGHT)
        text_group = VGroup(ket_0, ket_1, ket_p, ket_m)
        
        slogan = TextMobject(r"Slogan Here").move_to(DOWN*2)
        logo_png = ImageMobject('QC@UCI Logo_thick.png').scale(2)
        
        
        self.wait()
        self.SKIP_ANIMATIONS = False
        self.add_sound("intro_delayed",gain=-10)
        self.play(ShowCreation(circle),
                  ShowCreation(arrow),
                  ShowCreation(text_group),
                  run_time = 1)
        
        self.play(Transform(circle, sphere),
                  Rotate(arrow, about_point=ORIGIN),
                  run_time = 1)
        #self.play(Rotate(arrow, angle=-PI/2,
        #                 axis=np.array([1, 0, 0]), 
        #                about_point=ORIGIN))
        
        self.play(FadeOut(text_group),
                  FadeOut(arrow, run_time=0.5),
                  Transform(geo_group, Square().scale(2.1)),
                  FadeIn(logo_png, run_time=1.5))
        self.play(ApplyMethod(geo_group.move_to, UP),
                  ApplyMethod(logo_png.move_to, UP),
                  FadeIn(slogan))
        self.wait(2)
        self.play(FadeOut(geo_group),
                  FadeOut(logo_png),
                  FadeOut(slogan))
