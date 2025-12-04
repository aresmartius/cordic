# Versión 30-11-2025 - CORDIC UNIFICADO - Javier Martín Marcos

# Importamos librerias
from math import degrees, atan, atanh,ldexp


# Ángulos necesarios a ser precargados antes de generar iteraciones
def preload(v):
    # Calculamos los ángulos diádicos hasta el m pedido.
    beta = [degrees(atan(1 / 2 ** i)) for i in range(v)]
    return beta

def preload_h(v):
    # Igual que preload(v), pero los ángulos se calculan con atanh
    beta = [atanh(1 / 2 ** i) for i in range(1, v)]
    return beta


#ITERACIONES REQUERIDAS POR EL USUARIO
m = int(input('¿Cuántas iteraciones?: ')) + 1



class ITERATE:
    def __init__(self, theta):
        '''
        En esta sección vamos a configurar los parámetros de la iteración
        según el modo correspondiente.
        Va a ser configurado como una superfunción de Python (def __init__),
        para facilitar la lectura de variables en las distintas funciones
        del programa.
        '''
        self.LN2 = 0.6931471805599453  #ln(2)
        #Factor P y J respectivamente
        self.cosine_alpha = 0.607252935 if mode != 3 else 1.20753406
        self.sine_alpha = theta * self.cosine_alpha if mode == 2  else 0
        self.hyperbolic_reducing_factor = round(theta/self.LN2)
        self.theta_remaining = (self.normalize(theta) if mode != 3 else theta
        - (self.hyperbolic_reducing_factor)*self.LN2)
        self.beta = preload(m) if mode != 3 else preload_h(m + 1)
        self.alpha = 0
        self.hyperbolic_related = 1
        '''
        self.hyperbolic_related no es más que un indicador para saber si restar
        o sumar en self.cosine_alpha en la iteración dependiendo de si es una
        función hiperbólica o trigonométrica

        self.hyperbolic_reducing_factor nos sirve para reducir el valor theta
        que requerimos , pues la suma de todos los valores beta convergen en
        1.055, el cual no es suficiente para valores muy altos.
        '''
        print(self.theta_remaining)

    # Normalizamos los ángulos para que se encuentren en el primer cuadrante
    def normalize(self, theta): #solo en trigonométricas
        global inversion, sine_sign, cosine_sign
        cosine_sign = 1
        sine_sign = 1
        normalize_theta = theta // 360
        theta -= normalize_theta * 360
        inversion = 0
        if theta > 270:
            theta -= 270
            sine_sign = -1
            inversion += 1
        elif theta > 180:
            theta -= 180
            sine_sign = -1
            cosine_sign = -1
        elif theta > 90:
            theta -= 90
            cosine_sign = -1
            inversion += 1
        return theta

    def step(self, m):
        global mode
        old_cos = self.cosine_alpha
        old_sin = self.sine_alpha
        if mode == 2:
            D = 1 if old_cos * old_sin < 0 else -1
        elif mode == 3:
            D = 1 if self.theta_remaining >= 0 else -1
            self.hyperbolic_related = -1

        else:
            D = 1 if self.theta_remaining >= 0 else -1

        '''
        E hace referencia a los racionales diádicos tienen diferente valor en
        el exponente, simplemente porque cuando nos encontramos en el modo
        hiperbólico los valores son válidos a partir de m >=1, mientras que en
        el resto a partir de m >= 0, por facilidad de la unificación esta es la
        forma más sencilla de implementarlo
        '''
        E = (1 / (2 ** (m - 1))) if mode !=3 else (1 / (2 ** m))

        # Esto es la esencia del algoritmo iterativo de CORDIC
        self.cosine_alpha = (old_cos - self.hyperbolic_related * D * E * old_sin) # C_m
        self.sine_alpha = (old_sin + D * E * old_cos) # S_m
        self.theta_remaining -= D * self.beta[m - 1] # Diferencia entre el ángulo que llevamos y el idílico
        self.alpha += D * self.beta[m - 1] # "Ángulo que llevamos"

        if mode == 1:
            '''
            Cuando el ángulo va pasando por los distintos cuadrantes se
            invierten los valores de seno y coseno, por lo que debemos de
            arreglarlo en el caso de que sea asi, devolviendolos
            a su valor correspondiente
            '''
            if inversion != 0:
                print(
                    f"Iteración {m}: D={D}, cos(α)={self.sine_alpha * cosine_sign}, sin(α)={self.cosine_alpha * sine_sign}, θ_m={abs(self.theta_remaining)}, α= {self.alpha}")
            else:
                print(
                    f"Iteración {m}: D={D}, cos(α)={self.cosine_alpha * cosine_sign}, sin(α)={self.sine_alpha * sine_sign}, θ_m={abs(self.theta_remaining)}, α={self.alpha}")
        elif mode == 2:
            print(f"Iteración {m}: D={D}, α= {abs(self.alpha)}")
        elif mode == 3:
            print(
                f"Iteración {m}: D={D}, cosh(α)={self.cosine_alpha}, sinh(α)={self.sine_alpha},  α= {self.alpha}, θ_m={self.theta_remaining}")

    def hyperbolic_refactoring(self):
        #Tenemos que reconstruir el ángulo que hemos reducido
        exp_reduced_theta = self.cosine_alpha + self.sine_alpha #e^x

        # Aplicamos el factor de escala 2^k
        # math.ldexp(x, k) es equivalente a x * (2**k) (Desplazamiento de bits)
        exp_theta = ldexp(exp_reduced_theta, self.hyperbolic_reducing_factor)

        '''
        cosh(t) = (e^t + e^-t) / 2
        sinh(t) = (e^t - e^-t) / 2

        Siguiendo las propiedades hiperbólicas calculamos el inverso
        '''
        inverse_exp_theta = 1 / exp_theta

        self.cosine_alpha = (exp_theta + inverse_exp_theta) * (1/2)
        self.sine_alpha = (exp_theta - inverse_exp_theta) * (1/2)
        print('-'*55)
        print(f'Este es el resultado del CORDIC hiperbólico tras haberle aplicado el factor de aumento: senh(Ψ)= {self.sine_alpha} , cosh(Ψ)= {self.cosine_alpha}')
        print('-' * 67)
        [print(self.sine_alpha / self.cosine_alpha)] if input(
            '¿Quieres la tangente hiperbólica? SI/NO: ') == 'SI' else print('')

print('Seleccione que desea calcular con CORDIC: ')
print('1: Seno y coseno # Modo rotación de CORDIC')
print('2: Arcotangente # Modo vectorial de CORDIC')
print('3: Funciones hiperbólicas')
mode = int(input('Introduce modo: '))

if mode == 1:
    t = ITERATE(float(input('θ : ')))
elif mode == 2:
    t = ITERATE(float(input('Ψ : ')))
elif mode == 3:
    t = ITERATE(float(input('Ψ : ')))
else:
    print('Error al seleccionar modo, intentelo de nuevo')

if mode != 3:
    for j in range(1, m):
        t.step(j)
else:
    '''
    En el modo hiperbólico necesitamos repetir la iteración (3*k+1), para
    aumentar precisión
    '''
    def hyperbolic_repeat_indices(max_iter):
        repeats = [] # Indicador de m que se debe repetir en la iteración de CORDIC
        k = 4
        while k < max_iter:
            repeats.append(k)
            k = 3 * k + 1
        return repeats

    repeat_indices = hyperbolic_repeat_indices(m)
    iter_sequence = []
    for k in range(1, m):
        iter_sequence.append(k)
        if k in repeat_indices:
            iter_sequence.append(k)  # Añade la iteración repetida

    for j in iter_sequence:
        t.step(j)

    # Refactorización hiperbólica
    t.hyperbolic_refactoring()

ending = input()