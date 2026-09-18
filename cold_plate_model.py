import numpy as np

RHO = 988.04       # water density @ 50C, kg/m^3
MU = 0.0005465     # dynamic viscosity @ 50C, Pa*s
K_WATER = 0.644    # thermal conductivity @ 50C, W/m*K
PR = 3.56          # Prandtl number @ 50C
EPS = 0.00001      # surface roughness, m 
PLATE_WIDTH_MM = 180
PLATE_LENGTH_MM = 339
WALL_THICKNESS_MM = 2  # placeholder until manufacturing method is confirmed

def channel_length_from_width(width_mm, plate_width_mm, plate_length_mm, wall_thickness_mm):
    pitch = width_mm + wall_thickness_mm
    num_passes = int(plate_width_mm // pitch)
    length_mm = num_passes * plate_length_mm
    return length_mm, num_passes

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

def compute(width_mm, height_mm, flow_Lmin):
    length_mm, num_passes = channel_length_from_width(
        width_mm, PLATE_WIDTH_MM, PLATE_LENGTH_MM, WALL_THICKNESS_MM
    )

    a = height_mm / 1000
    b = width_mm / 1000
    L = length_mm / 1000
    area = a * b
    Dh = (2 * a * b) / (a + b)

    vol_flow = flow_Lmin / 60000
    velocity = vol_flow / area

    Re = reynolds_number(RHO, velocity, Dh, MU)
    f = friction_factor_swamee_jain(Re, Dh, EPS)
    Nu = nusselt_gnielinski(f, Re, PR)
    h_conv = convective_coefficient(Nu, K_WATER, Dh)
    dP = pressure_drop(f, L, Dh, RHO, velocity)

    return {
        "Re": Re, "f": f, "Nu": Nu, "h_conv": h_conv,
        "dP_kPa": dP / 1000, "length_mm": length_mm,
        "num_passes": num_passes, "valid": Re >= 3000,
    }

if __name__ == "__main__":
    #test = compute(width_mm=10, height_mm=10, length_mm=1332, flow_Lmin=20)
    test = compute(width_mm=10, height_mm=10, flow_Lmin=20)
    print(test)
    # Expected: Re~60264.7, f~0.0236, Nu~324.47, h_conv~20895.8
    # length_mm~5085, num_passes~15, dP_kPa~65.88