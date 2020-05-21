
class Oscillator:

    def __init__(self, pos0=0., vel0=0., w0=1., t0=0., tag=''):
        self.pos = pos0
        self.vel = vel0
        self.time = t0
        self.tag = tag if tag != '' else 'Generic SHO'
        self.omega0 = w0
        self.force = None

    def __str__(self):
        strng = "Oscillator\n"
        strng += "pos = {}, t = {}\n".format(self.pos, self.time)
        strng += "w = {}\n".format(self.omega0)
        strng += "v = {}\n".format(self.vel)
        return strng

    def get_state(self):
        return self.pos, 1.0, self.vel, 0.0, self.time

    def set_state(self, *state):
        L, vr = 0, 0
        self.pos, L, self.vel, vr, self.time = state

    def set_force(self, strength):
        self.force = strength

if __name__ == '__main__':
    # imports estandar... # numpy, scipy...
    # imports caseros... # solver, force, animate...
    pendulo1 = Oscillator()
    print("Pendulo_1: ", pendulo1)
    pendulo2 = Oscillator(1., 2., 3., 4.)
    print("Pendulo_2: ", pendulo2)


    # crear Oscillator
    # ver que las variables tengan los valores correctos
    # crear fuerza y conectarla con restoring_force
    # conectar el objeto fuerza con oscillator
    # crear una instancia de Solver: oscillator, metodo numerico, time step
    # integrar usando do_step de la instancia de Solver
    # graficar angulo y velocidad vs. tiempo
