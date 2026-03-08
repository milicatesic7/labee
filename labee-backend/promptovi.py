prompt_dif = """
You are analyzing a physics laboratory report about diffraction.

The report may consist of multiple images (pages).
Use information from ALL provided images.

The report contains TWO sections.

==================================================
SECTION 1: Diffraction on an optical grating
==================================================

For diffraction orders:

m = 1
m = 2

and for colors:

blue
green
red

Extract the following values:

- theta_L
- theta_D
- theta_m
- lambda_nm

If theta_m is not written in the report, compute it as:

theta_m = (theta_L + theta_D) / 2

If lambda_nm is not written, return 0.

Also extract the average wavelength for:

blue
green
red

==================================================
SECTION 2: Laser diffraction
==================================================

IMPORTANT:
The values in this section are handwritten inside a table.

Read the table CAREFULLY row by row.

Above the table there is a value labeled:

"Fotostruja usled ambijentalnog osvetljenja (μA)"

Extract this value as:

ambient_photocurrent_uA

--------------------------------------------------

The table contains EXACTLY 7 rows corresponding to diffraction orders:

0
1
-1
2
-2
3
-3

Do NOT reorder rows.

--------------------------------------------------

Each row contains EXACTLY FOUR columns:

1) distance_read_mm
   distance from central maximum (first column)

2) distance_relative_mm
   relative position (second column)

3) measured_photocurrent_uA
   measured photocurrent (third column)

4) diffraction_photocurrent_uA
   photocurrent corresponding to diffraction maximum (fourth column)

--------------------------------------------------

Numbers are handwritten.

Read the digits carefully.

If a number cannot be read with confidence, return 0.

Do NOT guess values.

==================================================

Return ONLY valid JSON in EXACTLY this structure:

{
  "grating": {
    "m1": {
      "blue":  { "theta_L": 0, "theta_D": 0, "theta_m": 0, "lambda_nm": 0 },
      "green": { "theta_L": 0, "theta_D": 0, "theta_m": 0, "lambda_nm": 0 },
      "red":   { "theta_L": 0, "theta_D": 0, "theta_m": 0, "lambda_nm": 0 }
    },
    "m2": {
      "blue":  { "theta_L": 0, "theta_D": 0, "theta_m": 0, "lambda_nm": 0 },
      "green": { "theta_L": 0, "theta_D": 0, "theta_m": 0, "lambda_nm": 0 },
      "red":   { "theta_L": 0, "theta_D": 0, "theta_m": 0, "lambda_nm": 0 }
    },
    "average": {
      "blue": 0,
      "green": 0,
      "red": 0
    }
  },

  "laser": {
    "ambient_photocurrent_uA": 0,
    "orders": {
      "0":  { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 },
      "1":  { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 },
      "-1": { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 },
      "2":  { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 },
      "-2": { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 },
      "3":  { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 },
      "-3": { "distance_read_mm": 0, "distance_relative_mm": 0, "measured_photocurrent_uA": 0, "diffraction_photocurrent_uA": 0 }
    }
  },

  "score": {
    "measurement_accuracy": 0
  }
}

Do not change keys.
Do not add explanations.
Return strictly valid JSON.
"""
prompt_den = """
You are analyzing a physics laboratory report.

You must:
1) Extract all measured values
2) Compute missing calculated values using formulas
3) Estimate the measurement accuracy score.

If a value is missing but can be calculated, calculate it.

==================================================
PART 1 – Density determination (Exercise 1.1)
==================================================

Use water density:
rho0 = 1000 kg/m^3

SECTION A – Liquid density using pycnometer

Formulas:

rho_liquid = rho0 * (m3 - m1) / (m2 - m1)

Measurement uncertainty:

um_mass = Um / 3

u_rho calculated using the formula shown in the document.

Uc = 2 * u_rho

final_rho_value = rho_liquid ± Uc


SECTION B – Granular solid density

rho_solid = rho0 * m / (m1 - m2)

um_mass = Um / 3

Uc = 2 * u_rho


SECTION C – Hydrostatic method

rho_hydro = rho0 * m / (m - m1)

um_mass = Um / 3

Uc = 2 * u_rho


==================================================
PART 2 – Gravitational acceleration (Exercise 1.2)
==================================================

For each measurement:

ls = (l1 + l2) / 2

ls_squared = ls^2

T = tu / n

T_squared = T^2

Slope coefficient:

a = Σ(T_i^2 * ls_i) / Σ(ls_i^2)

Gravitational acceleration:

g = 4π^2 / a

Reference value for Belgrade:

g_ref = 9.8060226 m/s²

Relative error:

relative_error_percent = |g − g_ref| / g_ref * 100

Absolute error:

absolute_error = |g − g_ref|

final_g_value = g ± absolute_error


==================================================
ACCURACY SCORE
==================================================

Compute a score from 0 to 100 representing the overall measurement quality.

Use:

score = 100 − relative_error_percent

Clamp score between 0 and 100.

Higher score means better measurement accuracy.


==================================================

Return ONLY valid JSON in EXACTLY this structure:

{
  "density": {
    "liquid": {
      "measurements": {
        "m1": 0,
        "m2": 0,
        "m3": 0
      },
      "results": {
        "rho_liquid": 0,
        "um_mass": 0,
        "u_rho": 0,
        "Uc": 0,
        "final_rho_value": 0
      }
    },

    "granular": {
      "measurements": {
        "m": 0,
        "m1": 0,
        "m2": 0
      },
      "results": {
        "rho_solid": 0,
        "um_mass": 0,
        "u_rho": 0,
        "Uc": 0,
        "final_rho_value": 0
      }
    },

    "hydrostatic": {
      "measurements": {
        "m": 0,
        "m1": 0
      },
      "results": {
        "rho_hydro": 0,
        "um_mass": 0,
        "u_rho": 0,
        "Uc": 0,
        "final_rho_value": 0
      }
    }
  },

  "gravity": {
    "measurements": {
      "l1": [0,0,0,0,0],
      "l2": [0,0,0,0,0],
      "ls": [0,0,0,0,0],
      "ls_squared": [0,0,0,0,0],
      "tu": [0,0,0,0,0],
      "n": [0,0,0,0,0],
      "T": [0,0,0,0,0],
      "T_squared": [0,0,0,0,0]
    },

    "results": {
      "a": 0,
      "g": 0,
      "relative_error_percent": 0,
      "absolute_error": 0,
      "final_g_value": 0
    }
  },

  "score": {
    "measurement_accuracy": 0
  }
}

Do not change keys.
Do not add explanations.
Return strictly valid JSON.
If a value cannot be extracted or calculated, use 0.
"""
prompt_len = """
You are analyzing a physics laboratory report (Exercise 4).

The report may consist of multiple images (pages).
Use information from ALL images.

The report contains FOUR sections.

==================================================
SECTION A – Direct method (focal length)
==================================================

The table contains exactly 5 rows of measurements.

For each row extract:

p_mm
l_mm
f_i_mm

If f_i_mm is missing, compute:

f_i = (p * l) / (p + l)

Then compute:

f_mean = average(f_i)
u_f = sqrt( sum((f_i - f_mean)^2) / (n*(n-1)) )
Uc = 2 * u_f
final_f_value = f_mean

==================================================
SECTION B – Bessel method
==================================================

The table contains exactly 5 rows.

Extract:

D_mm
d_mm
f_i_mm

If f_i_mm is missing compute:

f_i = (D^2 - d^2) / (4 * D)

Then compute:

f_mean
u_f
Uc
final_f_value

using the same formulas as above.

==================================================
SECTION C – Diverging lens
==================================================

The table contains 5 measurements.

Extract:

p_or_D_mm
l_or_d_mm
f_system_mm
f_diverging_mm

If f_diverging_mm is missing compute:

f_r = (f_system * f_s) / (f_system - f_s)

Then compute:

f_r_mean
u_fr
Uc
final_fr_value

==================================================
SECTION D – Speed of sound (Kundt tube)
==================================================

Extract:

frequency_Hz
n_figures
lv_m
rod_length_m
rho_al
temperature_C
pressure_Pa

Compute speed of sound in air:

c_v1 = 4 * frequency_Hz * lv_m / n_figures

c_v2 = sqrt( (kappa * pressure_Pa) / rho_air )

where rho_air = 1.25 kg/m³

Speed of sound as function of temperature:

c_temperature = 331.4 + 0.6 * temperature_C

Compute errors:

relative_error_1_percent
absolute_error_1

relative_error_2_percent
absolute_error_2

==================================================

Speed of sound in aluminum:

c_al = 4 * frequency_Hz * rod_length_m

Young modulus:

E_Y_al = rho_al * c_al^2

Compute:

relative_error_E_percent
absolute_error_E

==================================================

Return ONLY valid JSON in EXACTLY this structure:

{
  "direct_method": {
    "measurements": {
      "p_mm": [0,0,0,0,0],
      "l_mm": [0,0,0,0,0],
      "f_i_mm": [0,0,0,0,0]
    },
    "results": {
      "f_mean": 0,
      "u_f": 0,
      "Uc": 0,
      "final_f_value": 0
    }
  },

  "bessel_method": {
    "measurements": {
      "D_mm": [0,0,0,0,0],
      "d_mm": [0,0,0,0,0],
      "f_i_mm": [0,0,0,0,0]
    },
    "results": {
      "f_mean": 0,
      "u_f": 0,
      "Uc": 0,
      "final_f_value": 0
    }
  },

  "diverging_lens": {
    "measurements": {
      "p_or_D_mm": [0,0,0,0,0],
      "l_or_d_mm": [0,0,0,0,0],
      "f_system_mm": [0,0,0,0,0],
      "f_diverging_mm": [0,0,0,0,0]
    },
    "results": {
      "f_r_mean": 0,
      "u_fr": 0,
      "Uc": 0,
      "final_fr_value": 0
    }
  },

  "sound": {
    "inputs": {
      "frequency_Hz": 0,
      "n_figures": 0,
      "lv_m": 0,
      "rod_length_m": 0,
      "rho_al": 0,
      "temperature_C": 0,
      "pressure_Pa": 0
    },

    "air": {
      "c_v1": 0,
      "c_v2": 0,
      "c_temperature": 0,
      "relative_error_1_percent": 0,
      "absolute_error_1": 0,
      "relative_error_2_percent": 0,
      "absolute_error_2": 0
    },

    "aluminum": {
      "c_al": 0,
      "E_Y_al": 0,
      "relative_error_E_percent": 0,
      "absolute_error_E": 0
    }
  },

  "score": {
    "measurement_accuracy": 0
  }
}

Do not change keys.
Do not add explanations.
Return strictly valid JSON.
If a value is missing return 0.
"""
prompts={1:prompt_den,2:prompt_len,3:prompt_dif}