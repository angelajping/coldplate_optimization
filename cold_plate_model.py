import numpy as np

RHO = 988.04       # water density @ 50C, kg/m^3
MU = 0.0005465     # dynamic viscosity @ 50C, Pa*s
K_WATER = 0.644    # thermal conductivity @ 50C, W/m*K
PR = 3.56          # Prandtl number @ 50C
EPS = 0.00001      # surface roughness, m 

def hydraulic_diameter(a, b):
    """a, b in meters. Rectangular channel."""
    return (2 * a * b) / (a + b)

def reynolds_number(rho, velocity, Dh, mu):
    return rho * velocity * Dh / mu

def friction_factor_swamee_jain(Re, Dh, eps):
    return 0.25 / (np.log10(eps / (3.7 * Dh) + 5.74 / Re**0.9))**2

def nusselt_gnielinski(f, Re, Pr):
    numerator = (f / 8) * (Re - 1000) * Pr
    denominator = 1 + 12.7 * (f / 8)**0.5 * (Pr**(2/3) - 1)
    return numerator / denominator

def convective_coefficient(Nu, k, Dh):
    return Nu * k / Dh

def pressure_drop(f, L, Dh, rho, velocity):
    return f * (L / Dh) * (rho * velocity**2 / 2)

def compute(width_mm, height_mm, length_mm, flow_Lmin):
    a = height_mm / 1000
    b = width_mm / 1000
    area = a * b
    Dh = hydraulic_diameter(a, b)

    vol_flow = flow_Lmin / 60000  # L/min -> m^3/s
    velocity = vol_flow / area

    Re = reynolds_number(RHO, velocity, Dh, MU)
    f = friction_factor_swamee_jain(Re, Dh, EPS)
    Nu = nusselt_gnielinski(f, Re, PR)
    h_conv = convective_coefficient(Nu, K_WATER, Dh)
    dP = pressure_drop(f, length_mm/1000, Dh, RHO, velocity)

    return {
        "Re": Re, "f": f, "Nu": Nu,
        "h_conv": h_conv, "dP_kPa": dP / 1000,
        "valid": 3000 <= Re <= 5000000,
    }

if __name__ == "__main__":
    test = compute(width_mm=10, height_mm=10, length_mm=1332, flow_Lmin=10)
    print(test)
    # Sanity check against your spreadsheet: Re ~30138, f ~0.0261, Nu ~172.19, h_conv ~11089