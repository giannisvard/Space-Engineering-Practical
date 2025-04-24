import numpy as np
from scipy import constants
c = constants.c
planck = constants.Planck #Do not name this h...

def illumination(f, b, d, h,alpha, beta):
    """
    Calculate the power incident on the quadcells
    Issues: not vectorized
    alpha and beta are in degrees
    """
    alpha = alpha * np.pi / 180
    beta = beta * np.pi / 180
    f_angled = f*np.cos(alpha)*np.cos(beta)
    # Linear shift due to sun angle
    center_distance_a = h*np.tan(alpha) #y
    center_distance_b = h*np.tan(beta) #x
    # Calculate the illuminated areas
    bottom_a = center_distance_a - b/2
    top_a = center_distance_a + b/2
    bottom_b = center_distance_b - b/2
    top_b = center_distance_b + b/2

    # Q1 spans x: [0,d], y: [0,d]
    # I am basically demanding that the illuminated area overlaps with the cell area
    if bottom_a < d and top_a > 0 and top_b > 0 and bottom_b < d  :
        side_y1 = min(top_a, d) - max(bottom_a, 0)
        side_x1 = min(top_b, d) - max(bottom_b, 0)
        A_Q1 = side_x1*side_y1
    else: # bottom_a >= d or bottom_b >= d:
        # This is out of bounds, there is no illuminated area
        A_Q1 = 0

    # Q 2 spans x: [0,d], y: [-d,0]
    if bottom_a < 0 and top_a > -d and bottom_b < d  and top_b > 0:
        side_y2 = min(top_a, 0) - max(bottom_a, -d)
        side_x2 = min(top_b, d) - max(bottom_b, 0)
        A_Q2 = side_x2*side_y2
    else: #bottom_a >= d or bottom_b >= 0:
        A_Q2 = 0

    # Q3 spans x: [-d,0], y: [-d,0]
    if bottom_a < 0 and top_a > -d and bottom_b < 0 and top_b > -d:
        side_y3 = min(top_a, 0) - max(bottom_a, -d)
        side_x3 = min(top_b, 0) - max(bottom_b, -d)
        A_Q3 = side_x3 * side_y3
    else: #bottom_a >= 0 or bottom_b >= 0:
        A_Q3 = 0

    # Q4 spans x: [-d,0], y: [0,d]
    if bottom_a < d and top_a > 0 and bottom_b < 0 and top_b > -d:
        side_y4 = min(top_a, d) - max(bottom_a, 0)
        side_x4 = min(top_b, 0) - max(bottom_b, -d)
        A_Q4 = side_x4 * side_y4
    else: #bottom_a >= 0 or bottom_b >= d:
        A_Q4 = 0

    # Incident power calculations:
    l_1 = f_angled * A_Q1
    l_2 = f_angled * A_Q2
    l_3 = f_angled * A_Q3
    l_4 = f_angled * A_Q4
    l_max = f * d**2
    return l_1, l_2, l_3, l_4, l_max

def power_to_current(l_1, l_2, l_3, l_4, l_max):
    """
    Hi Giannis please correct this as you go
    My current assumption takes the incident power and compares it to the maximum.
    The current generation is the fraction of -2.80 mA of l_i compared to its maximum.
    I made this assumption based on Johans email telling us that the sun sensor is linear up to saturation
    Also that the maximum current(saturation point) is -2.80 mA
    """
    I1 = -2.80 * 1e-3 * l_1 / l_max
    I2 = -2.80 * 1e-3 * l_2 / l_max
    I3 = -2.80 * 1e-3 * l_3 / l_max
    I4 = -2.80 * 1e-3 * l_4 / l_max
    return I1, I2, I3, I4


def apply_noise(voltage, offset=0.0, noise_level=0.005):
    # noise for the interested
    noise = np.random.normal(0, noise_level, size=len(voltage))
    return voltage + offset + noise


def ADC_DAC(voltage, bits, ref):
    #apply a chose bit resolution to the measurement
    #assumes a voltage floor of 0
    fraction = voltage / ref
    word = (fraction * 2**bits).astype(int)
    #Calculate the angles
    word_fraction = word/2**bits
    return word_fraction


def sun_angles(Q1,Q2,Q3,Q4):
    # Calculates the sun angles
    # assumes that the maximum angle is st at 90 deg
    Q_tot = Q1+Q2+Q3+Q4
    Sa = (Q1 + Q4 - Q2 - Q3)/Q_tot
    Sb = (Q1 + Q2 - Q3 - Q4)/Q_tot
    a, b = np.arctan(Sa)*180/np.pi, np.arctan(Sb)*180/np.pi
    return a.reshape(-1,), b.reshape(-1,)