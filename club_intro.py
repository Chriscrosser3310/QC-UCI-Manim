from manim import *
import random
import numpy as np
import math
from functools import partial

class Qubit(ThreeDScene):
    def construct(self):
        
        axis = ThreeDAxes().scale(0.5)
        sphere = Sphere().set_fill(BLACK)
        arrow = Arrow().put_start_and_end_on(ORIGIN, UP).set_fill(RED).set_stroke(RED)
        arrow.rotate(axis=RIGHT, angle=PI/2, about_point=ORIGIN)

        ket_0 = TextMobject(r"$\ket{0}$").next_to(axis, np.array([0,0,1]))
        ket_1 = TextMobject(r"$\ket{1}$").next_to(axis, -np.array([0,0,1]))
        ket_p = TextMobject(r"$\ket{+}$").next_to(axis, RIGHT)
        ket_m = TextMobject(r"$\ket{-}$").next_to(axis, LEFT)
        ket_pi = TextMobject(r"$\ket{+i}$").next_to(axis, UP)
        ket_mi = TextMobject(r"$\ket{-i}$").next_to(axis, DOWN)
        axis_name_group = VGroup(ket_0, ket_1, ket_p, ket_m, ket_pi, ket_mi)
        
        qubit = TextMobject(r"$\alpha \ket{0} + \beta \ket{1}$")
        
        gate_list = [TextMobject(r'H').to_corner(UP),
                      TextMobject(r'$R_z(\frac{\pi}{2})$').to_corner(UP),
                      TextMobject(r'$R_x(\frac{\pi}{2})$').to_corner(UP),
                      TextMobject(r'$R_y(\frac{\pi}{2})$').to_corner(UP)]
        
        rotation_list = [(PI, [1,0,1]),
                         (PI/2, [0,0,1]),
                         (PI/2, [1,0,0]),
                         (PI/2, [0,1,0])]
                         
        
        self.set_camera_orientation(phi=75*DEGREES, theta=0)
       
        self.wait()
        self.play(ShowCreation(axis))
        
        self.begin_ambient_camera_rotation(rate = 0.05)
        
        self.add_fixed_orientation_mobjects(ket_0, ket_1, ket_p, ket_m, ket_pi, ket_mi)
        self.play(ShowCreation(axis_name_group),
                  ShowCreation(sphere),
                  ShowCreation(arrow))
        
        i = 0
        i_last = len(gate_list)
        self.add_fixed_in_frame_mobjects(gate_list[0])
        self.play(Write(gate_list[0]),
                  Rotate(arrow, 
                         about_point=ORIGIN,
                         angle=rotation_list[i][0], 
                         axis=np.array(rotation_list[i][1])))
        
        i += 1
        while i < i_last:
            self.add_fixed_in_frame_mobjects(gate_list[i])
            self.play(FadeOut(gate_list[i-1]),
                      FadeIn(gate_list[i]),
                      Rotate(arrow, 
                             about_point=ORIGIN,
                             angle=rotation_list[i][0], 
                             axis=np.array(rotation_list[i][1])))
            i += 1
        
        self.play(Uncreate(gate_list[-1]),
                  Uncreate(axis_name_group),
                  Uncreate(axis),
                  Uncreate(sphere),
                  Uncreate(arrow))
        self.stop_ambient_camera_rotation()
        self.wait()
        
class BosonSampling(GraphScene):

    def construct(self):
        
        def photon_path_func(x, offset=0):
            q = x//3
            r = x%3
            if 2<r<3:
                a = x-2*(q+1)+offset
            else:
                a = q+offset
            return a
        
        pos_path_list = []
        neg_path_list = []
        for offset in range(-14, 10, 2):
            pos_path=FunctionGraph(partial(photon_path_func, offset=offset))
            pos_path.CONFIG["x_min"] = -5
            pos_path.CONFIG["x_max"] = 5
            pos_path_list.append(pos_path)
            
            neg_path=FunctionGraph(lambda x:\
                                      -partial(photon_path_func, offset=-offset)(x)+1)
            neg_path.CONFIG["x_min"] = -5
            neg_path.CONFIG["x_max"] = 5
            neg_path_list.append(neg_path)
        
        all_path_list = pos_path_list + neg_path_list
        
        VGroup(*all_path_list).scale(0.5).move_to(LEFT*4)
        
        eqs=[]
        
        eqs.append(TextMobject("$b^{\dagger}_j$", "=",
        "$\sum_{i=1}^N$","$U_{ij}a_i^{\dagger}$").move_to(RIGHT*3+UP*2))
        
        eqs.append(TextMobject("$b_j$", "=",  
        "$\sum_{i=1}^N$","$U_{ij}^{\dagger}a_i$").move_to(RIGHT*3+UP))
        
        eqs.append(TextMobject("$\ket{\psi_{out}}$", "=",
        "$W\ket{s_1,s_2,...,s_N}$").move_to(RIGHT*3))
        
        eqs.append(TextMobject("$p(t_1,t_2,...,t_N)$", "=",
        "$\\braket{t_1,t_2,...,t_N}{\psi_{out}}$").move_to(RIGHT*3+DOWN))
        
        eqs.append(TextMobject("$p(t_1,t_2,...,t_N)$", "=",
        "$\\frac{|Perm(U_{S,T})|^2}{t_1!...t_N!s_1!...s_N!}$").move_to(RIGHT*3+DOWN*2))
        
        for eq in eqs:
            eq[0].set_fill(RED)
            eq[-1].set_fill(BLUE)
        
        self.wait()
                
        self.play(*(ShowCreation(p) for p in all_path_list),
                  *(ShowCreation(eq) for eq in eqs),
                  run_time=1)
        
        photon_list = []
        path_list = []
        
        for j in range(40):
            photon=Dot(radius=0.08).set_fill(RED)
            path = random.choice(all_path_list)
            photon.move_to(path.points[0])
            photon_list.append(photon)
            path_list.append(path)
            
        self.play(*[ShowCreation(photon) for photon\
                  in photon_list],
                  run_time=0.5,
                  rate_func=linear)
        
        self.play(AnimationGroup(
                                *[MoveAlongPath(photon, path) \
                                  for photon, path \
                                  in zip(photon_list, path_list) \
                                 ], 
                                lag_ratio=0.1),
                  run_time=5,
                  rate_func=linear)
        
        self.play(*[FadeOut(photon) for photon in photon_list],
                  *[FadeOut(path) for path in all_path_list],
                  *[FadeOut(eq) for eq in eqs],
                  run_time=0.5,
                  rate_func=linear)
        
        self.wait()
        
class QCatUCI(Scene):
    
    class Electron(Circle):
        CONFIG = {
        "radius" : 0.2,
        "stroke_width" : 3,
        "color" : RED,
        "fill_color" : RED,
        "fill_opacity" : 0.5,
        }
        def __init__(self, **kwargs):
            Circle.__init__(self, **kwargs)
            minus = TexMobject("-")
            minus.scale(0.7)
            minus.move_to(self)
            self.add(minus)

    def construct(self):
        
        text1 = TextMobject("Q","C","@","UCI")
        
        text2 = TextMobject("Quantum", " Computing", " Club at", " UCI")
        
        text3 = TextMobject("Quantum", " Computing", " Club at", " UCI")
        text3[0].set_fill(BLUE)
        text3[1].set_fill(YELLOW)
        text3.move_to(UP*3)
        
        student = TextMobject("Undergraduate + Graduate")
        student.set_color(YELLOW).move_to(UP)
        
        goal1 = TextMobject("1. Introduce ", "Quantum Computing"," to Anteaters")
        goal1.set_color_by_tex_to_color_map({"Quantum Computing":RED})
        goal1.next_to(student, DOWN)
        
        goal2 = TextMobject("2. Build a ", "Quantum Computing"," Community")
        goal2.set_color_by_tex_to_color_map({"Quantum Computing":RED})
        goal2.next_to(goal1, DOWN).align_to(goal1, LEFT)
        
        goal3 = TextMobject("3. Promote ","Quantum Computing", " Research")
        goal3.set_color_by_tex_to_color_map({"Quantum Computing":RED})
        goal3.next_to(goal2, DOWN).align_to(goal2, LEFT)
        
        small = TextMobject("$\sim small\sim$").set_color(RED).scale(0.5)
        small.next_to(text3[0], DOWN*0.5)
        
        self.wait()
        
        self.play(Write(text1))
        self.wait()
        
        self.play(Transform(text1[:2], text2[:2]),
                  Transform(text1[2:], text2[2:]))
        self.wait()
        
        self.play(ApplyMethod(text1.move_to, UP*3))
        self.play(ShowCreation(student))
        self.wait(3)
        
        self.play(ShowCreation(goal1))
        self.play(ShowCreation(goal2))
        self.play(ShowCreation(goal3))
        self.wait(8)
        self.play(FadeOut(student),
                  FadeOut(goal1),
                  FadeOut(goal2),
                  FadeOut(goal3))
        
        self.play(Transform(text1[0], text3[0]))
        self.wait(3)
        self.play(ShowCreation(small))
        
        self.play_photon()
        self.fadeout_photon()
        
        self.play_spin()
        self.fadeout_spin()
        
        self.play_two_level()
        self.play(Transform(text1[1], text3[1]))
        self.wait(3)
        
        self.fadeout_two_level()
        self.play(FadeOut(small),
                  FadeOut(text1[2:]),
                  ApplyMethod(text1[:2].move_to, ORIGIN))
        self.wait(3)
        
        self.play(FadeOut(text1[:2]))
        self.wait()
        
    def play_photon(self):
    
        Amplitude = 0.4
        freq = 3
        angular_freq = (2*np.pi)*freq
        equation = lambda t: Amplitude*np.sin(t*angular_freq)
    
        photon = FunctionGraph(equation,x_min=-5,x_max=-4)
        light_source = Dot(photon.points[0], radius=0.5, color=YELLOW)
    
        tip = Arrow(photon.points[-1],photon.points[-1]+RIGHT*0.4)
        self.play(GrowFromCenter(light_source), run_time=0.7)
        self.play(ShowCreation(photon), ShowCreation(tip))
        photon.add(tip)
    
        animation = ApplyMethod(photon.shift, (13,0,0))
        self.play(animation)
        
        self.photon = photon
        self.light_source = light_source
    
    def fadeout_photon(self):

        self.play(FadeOut(self.photon),
                  FadeOut(self.light_source))
        
    def play_spin(self):
        
        electron = self.Electron()
        spin = Arrow().scale(0.7)
        spin.rotate(PI/2)
        spin.move_to(electron)
        
        s_group = VGroup(spin, electron)
        
        self.play(ShowCreation(spin),
                  GrowFromCenter(electron))
        
        self.wait()
        
        self.play(Rotate(spin))
        
        self.s_group = s_group
    
    def fadeout_spin(self):
        
        self.play(FadeOut(self.s_group))
        
    def play_two_level(self):
        
        line0 = Line().move_to(DOWN*0.5)
        line1 = Line().move_to(UP*0.5)
        
        dot = Dot().set_fill(RED).move_to(line0)
        
        s_dot0 = Dot().set_fill(RED, opacity = 0.5).move_to(line0)
        s_dot1 = Dot().set_fill(RED, opacity = 0.5).move_to(line1)
        s_dot_group = VGroup(s_dot0, s_dot1)
        
        zero = TextMobject("$\ket{0}$").next_to(line0, LEFT)
        one = TextMobject("$\ket{1}$").next_to(line1, LEFT)
        qubit = TextMobject("Qubit").scale(0.8).next_to(line1, UP*1.1)
        
        tl_group = VGroup(line0, line1, zero, one, dot, qubit)
        
        self.play(ShowCreation(tl_group))
        
        self.play(ApplyMethod(dot.move_to, UP*0.5))
        self.play(ApplyMethod(dot.move_to, DOWN*0.5))
        
        self.play(Transform(dot, s_dot_group))
        
        self.wait()
        
        equal = TextMobject("$\stackrel{?}{=}$")
        
        n_times = TextMobject("$N \\times$").move_to(LEFT*4)
        
        quantum = TextMobject("Quantum").scale(0.7).move_to(RIGHT*2+UP*0.2)
        
        computer = SVGMobject('computer.svg').move_to(RIGHT*2)
        
        speed_up = TextMobject('Speed up').scale(0.5).move_to(RIGHT*2+UP*1.3)
        
        point_to = Arrow().set_fill(YELLOW).set_stroke(YELLOW)
        point_to.put_start_and_end_on(RIGHT*1.8+UP*1.5, UP*2.6)
        
        self.play(ShowCreation(n_times),
                  ApplyMethod(tl_group.move_to, LEFT*2),
                  ShowCreation(equal),
                  ShowCreation(computer),
                  ShowCreation(quantum))
        
        self.wait(2)
        self.play(ShowCreation(speed_up))
        self.play(ShowCreation(point_to))
        
        self.n_times = n_times
        self.tl_group = tl_group
        self.equal = equal
        self.computer = computer
        self.quantum = quantum
        self.speed_up = speed_up
        self.point_to = point_to
    
    def fadeout_two_level(self):
        
        self.play(FadeOut(self.n_times),
                  FadeOut(self.tl_group),
                  FadeOut(self.equal),
                  FadeOut(self.computer),
                  FadeOut(self.quantum),
                  FadeOut(self.speed_up),
                  FadeOut(self.point_to))
        
class CodeQC(Scene):
    def construct(self):
        
        sim = TextMobject("Classical Computer", " Simulation")
        real = TextMobject("Real", " Quantum Computer")
        sim[1].set_fill(RED)
        real[0].set_fill(RED)
        
        qiskit_logo = SVGMobject("Qiskit-Logo.svg").move_to(LEFT*2).scale(1.5)
        qiskit_text = TextMobject("Qiskit").next_to(qiskit_logo, DOWN*1.5)
        IBM_text= TextMobject("(IBM)").next_to(qiskit_text, DOWN)
        q_group = VGroup(qiskit_logo, qiskit_text, IBM_text)
        
        title = TextMobject("Programming Language").move_to(UP*3)
        
        real.next_to(sim, DOWN*2)
        real.align_to(sim, LEFT)
        
        t_group =  VGroup(sim, real)
        
        t_group.move_to(ORIGIN)
        
        self.play(Write(sim))
        self.wait()
        self.play(Write(real))
        self.wait()
        self.play(ApplyMethod(t_group.scale, 0.8))
        self.play(AnimationGroup(
                   AnimationGroup(
                    Write(title),
                    ApplyMethod(t_group.move_to, RIGHT*2.5)),
                   Write(q_group), lag_ratio = 0.5))
        self.wait(6)
        self.play(FadeOut(t_group), 
                  FadeOut(q_group), 
                  FadeOut(title))
        self.wait()
        
class WhoCanJoin(Scene):
    def construct(self):
        
        who = TextMobject("Who can join QC@UCI?")
        answer = TextMobject("Anyone!").set_fill(RED)
        
        self.play(Write(who))
        self.wait()
        self.play(AnimationGroup(
                    ApplyMethod(who.move_to, UP),
                    Write(answer), lag_ratio=0.5))
        self.wait()
        
        self.play(FadeOut(who),
                  FadeOut(answer))
        
        club = TextMobject("QC@UCI").scale(1.2)
        basic = TextMobject("Basic Track").scale(1).set_fill(GREEN_E).move_to(LEFT*3+UP)
        advanced = TextMobject("Advanced Track").scale(1).set_fill(BLUE_E).move_to(RIGHT*3+UP)
        
        b_know = TextMobject("Basic Knowledge").scale(0.8).set_fill(GREEN_A).next_to(basic, DOWN)
        code = TextMobject("Qiskit Introduction").scale(0.8).set_fill(GREEN_A).next_to(b_know, DOWN)
        
        a_top = TextMobject("Advanced Topics").scale(0.8).set_fill(BLUE_A).next_to(advanced, DOWN)
        project = TextMobject("Projects").scale(0.8).set_fill(BLUE_A).next_to(a_top, DOWN)
        lecture = TextMobject("Lecture Notes").scale(0.8).set_fill(BLUE_A).next_to(project, DOWN)
        paper = TextMobject("Paper Discussion").scale(0.8).set_fill(BLUE_A).next_to(lecture, DOWN)
        
        
        self.play(Write(club))
        
        self.play(AnimationGroup(
                    ApplyMethod(club.move_to, UP*2),
                    AnimationGroup(
                        Write(basic),
                        Write(advanced)), 
                    lag_ratio=0.5))
        self.wait(3)
        
        self.play(Write(b_know),
                  Write(code))
        self.wait(4)
        
        self.play(Write(a_top),
                  Write(project),
                  Write(lecture),
                  Write(paper))
        self.wait(8)
        
        self.play(FadeOut(club),
                  FadeOut(basic),
                  FadeOut(advanced),
                  FadeOut(b_know),
                  FadeOut(code),
                  FadeOut(a_top),
                  FadeOut(project),
                  FadeOut(lecture),
                  FadeOut(paper))
        
        self.wait()
        
        welcome = TextMobject("Welcome to Join QC@UCI!").scale(1.5)
        
        self.play(ShowCreation(welcome))
        self.wait(2)
        
        self.play(FadeOut(welcome))
        self.wait()


class Meet(Scene):
    def construct(self):
        
        meet = TextMobject("Meet our team at ", "QC@UCI")
        meet[1].set_fill(BLUE)
        
        self.play(Write(meet))
        self.wait(2)
        self.play(Uncreate(meet))

class You(Scene):
    def construct(self):
        
        you = TextMobject("...and ", "you")
        you[1].set_fill(RED)
        
        self.play(Write(you[0]))
        self.wait()
        self.play(Write(you[1]))
        self.wait(2)
        self.play(Uncreate(you))