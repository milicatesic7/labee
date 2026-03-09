from cmath import sin

from promptovi import prompts
from google.genai import types
import json
import math




def analysis(client, images, vezba_id):

    print("We are buzzing through your report…")

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
    )

    parts = [types.Part.from_bytes(data=img, mime_type="image/jpeg") for img in images]

    contents = [*parts, prompts[vezba_id]]

    return client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=contents,
        config=config,
    )


def difrakcija(response):

    raw = response.text.strip()

    if "```" in raw:
        raw = raw.split("```")[1]

    raw = raw.strip()

    data = json.loads(raw)

    grating = data["grating"]

    def transform_m(m_dict, m):

        result = {}

        for color in ["blue", "green", "red"]:

            theta_L = m_dict[color]["theta_L"]
            theta_D = m_dict[color]["theta_D"]
            theta_m = m_dict[color]["theta_m"]
            lambda_nm = m_dict[color]["lambda_nm"]

            if theta_m == 0 and (theta_L or theta_D):
                theta_m = (theta_L + theta_D) / 2

            if lambda_nm == 0 and theta_m != 0:

                theta_rad = math.radians(theta_m)

                N = 100
                a = 1 / N

                lambda_nm = (a * math.sin(theta_rad)) / m
                lambda_nm = lambda_nm * 1e9
                lambda_nm = round(lambda_nm, 2)

            result[color] = {
                "theta_L": theta_L,
                "theta_D": theta_D,
                "theta_m": round(theta_m,3),
                "lambda_nm": lambda_nm
            }

        return result


    m1 = transform_m(grating["m1"],1)
    m2 = transform_m(grating["m2"],2)

    avg = {}

    for color in ["blue","green","red"]:

        lam1 = m1[color]["lambda_nm"]
        lam2 = m2[color]["lambda_nm"]

        if lam1 and lam2:
            avg[color] = round((lam1 + lam2)/2,2)
        else:
            avg[color] = 0


    grating_result = {
        "m1": m1,
        "m2": m2,
        "average": avg
    }


    laser = data["laser"]

    ambient = laser["ambient_photocurrent_uA"]
    orders = laser["orders"]

    laser_result = {}

    for order in ["0","1","-1","2","-2","3","-3"]:

        row = orders[order]

        distance_read = row["distance_read_mm"]
        distance_relative = row["distance_relative_mm"]
        measured = row["measured_photocurrent_uA"]
        corrected = row["diffraction_photocurrent_uA"]

        if corrected == 0 and measured != 0:
            corrected = measured - ambient

        laser_result[order] = {
            "distance_read_mm": distance_read,
            "distance_relative_mm": distance_relative,
            "measured_photocurrent_uA": measured,
            "diffraction_photocurrent_uA": corrected
        }


    laser_final = {
        "ambient_photocurrent_uA": ambient,
        "orders": laser_result
    }


    score = 100

    expected = {
        "blue": 460,
        "green": 540,
        "red": 650
    }

    errors = []

    for color in ["blue","green","red"]:

        lam = avg[color]

        if lam != 0:

            err = abs(lam - expected[color]) / expected[color] * 100
            errors.append(err)

    if errors:
        score = max(0, round(100 - sum(errors)/len(errors),2))


    return {
        "grating": grating_result,
        "laser": laser_final,
        "score": {
            "measurement_accuracy": score
        }
    }

def gustina(response):

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]

    data = json.loads(raw)

    density = data["density"]
    gravity = data["gravity"]

    result = {}

    liquid = density["liquid"]

    meas = liquid["measurements"]
    res = liquid["results"]

    m1 = meas["m1"]
    m2 = meas["m2"]
    m3 = meas["m3"]

    rho = res["rho_liquid"]

    if rho == 0 and m2 != m1:
        rho = (m3 - m1) / (m2 - m1)

    result["liquid_density"] = {
        "measurements": {
            "m1": m1,
            "m2": m2,
            "m3": m3
        },
        "results": {
            "rho": round(rho, 4),
            "um_mass": res["um_mass"],
            "u_rho": res["u_rho"],
            "Uc": res["Uc"],
            "final": res["final_rho_value"]
        }
    }

    granular = density["granular"]

    meas = granular["measurements"]
    res = granular["results"]

    m = meas["m"]
    m1 = meas["m1"]
    m2 = meas["m2"]

    rho = res["rho_solid"]

    if rho == 0 and (m1 - m2) != 0:
        rho = m / (m1 - m2)

    result["granular_density"] = {
        "measurements": {
            "m": m,
            "m1": m1,
            "m2": m2
        },
        "results": {
            "rho": round(rho, 4),
            "um_mass": res["um_mass"],
            "u_rho": res["u_rho"],
            "Uc": res["Uc"],
            "final": res["final_rho_value"]
        }
    }

    hydro = density["hydrostatic"]

    meas = hydro["measurements"]
    res = hydro["results"]

    m = meas["m"]
    m1 = meas["m1"]

    rho = res["rho_hydro"]

    if rho == 0 and (m - m1) != 0:
        rho = m / (m - m1)

    result["hydrostatic_density"] = {
        "measurements": {
            "m": m,
            "m1": m1
        },
        "results": {
            "rho": round(rho, 4),
            "um_mass": res["um_mass"],
            "u_rho": res["u_rho"],
            "Uc": res["Uc"],
            "final": res["final_rho_value"]
        }
    }

    meas = gravity["measurements"]
    res = gravity["results"]

    ls = meas["ls"]
    T2 = meas["T_squared"]

    a = res["a"]

    if a == 0 and len(ls) == 5:
        num = sum(ls[i] * T2[i] for i in range(5))
        den = sum(ls[i] ** 2 for i in range(5))

        if den != 0:
            a = num / den

    g = res["g"]

    if g == 0 and a != 0:
        g = (4 * math.pi ** 2) / a

    result["gravity"] = {
        "measurements": meas,
        "results": {
            "a": round(a, 5),
            "g": round(g, 4),
            "relative_error_percent": res["relative_error_percent"],
            "absolute_error": res["absolute_error"],
            "final": res["final_g_value"]
        }
    }

    score = data["score"]["measurement_accuracy"]

    result["score"] = {
        "measurement_accuracy": score
    }

    return result

def process_lens(response):

    raw = response.text.strip()

    if "```" in raw:
        raw = raw.split("```")[1]

    raw = raw.strip()

    data = json.loads(raw)

    result = {}

    direct = data["direct_method"]

    p = direct["measurements"]["p_mm"]
    l = direct["measurements"]["l_mm"]
    f = direct["measurements"]["f_i_mm"]

    for i in range(5):
        if f[i] == 0 and (p[i] + l[i]) != 0:
            f[i] = (p[i] * l[i]) / (p[i] + l[i])

    f_mean = direct["results"]["f_mean"]

    if f_mean == 0 and len(f) > 0:
        f_mean = sum(f) / len(f)

    result["direct_method"] = {
        "measurements": {
            "p_mm": p,
            "l_mm": l,
            "f_i_mm": f
        },
        "results": {
            "f_mean": round(f_mean,3),
            "u_f": direct["results"]["u_f"],
            "Uc": direct["results"]["Uc"],
            "final_f_value": direct["results"]["final_f_value"]
        }
    }

    bessel = data["bessel_method"]

    D = bessel["measurements"]["D_mm"]
    d = bessel["measurements"]["d_mm"]
    f_b = bessel["measurements"]["f_i_mm"]

    for i in range(5):
        if f_b[i] == 0 and D[i] != 0:
            f_b[i] = (D[i]**2 - d[i]**2) / (4 * D[i])

    result["bessel_method"] = {
        "measurements": {
            "D_mm": D,
            "d_mm": d,
            "f_i_mm": f_b
        },
        "results": {
            "f_mean": bessel["results"]["f_mean"],
            "u_f": bessel["results"]["u_f"],
            "Uc": bessel["results"]["Uc"],
            "final_f_value": bessel["results"]["final_f_value"]
        }
    }

    diverging = data["diverging_lens"]

    pD = diverging["measurements"]["p_or_D_mm"]
    ld = diverging["measurements"]["l_or_d_mm"]
    fs = diverging["measurements"]["f_system_mm"]
    fr = diverging["measurements"]["f_diverging_mm"]

    for i in range(5):
        if fr[i] == 0 and fs[i] != 0:
            fr[i] = fs[i]

    result["diverging_lens"] = {
        "measurements": {
            "p_or_D_mm": pD,
            "l_or_d_mm": ld,
            "f_system_mm": fs,
            "f_diverging_mm": fr
        },
        "results": {
            "f_r_mean": diverging["results"]["f_r_mean"],
            "u_fr": diverging["results"]["u_fr"],
            "Uc": diverging["results"]["Uc"],
            "final_fr_value": diverging["results"]["final_fr_value"]
        }
    }

    sound = data["sound"]

    vg = sound["inputs"]["frequency_Hz"]
    n = sound["inputs"]["n_figures"]
    lv = sound["inputs"]["lv_m"]

    cv1 = sound["air"]["c_v1"]

    if cv1 == 0 and n != 0:
        cv1 = (4 * vg * lv) / n

    result["sound"] = {
        "inputs": sound["inputs"],
        "air": {
            "c_v1": round(cv1,2),
            "c_v2": sound["air"]["c_v2"],
            "c_temperature": sound["air"]["c_temperature"],
            "relative_error_1_percent": sound["air"]["relative_error_1_percent"],
            "absolute_error_1": sound["air"]["absolute_error_1"],
            "relative_error_2_percent": sound["air"]["relative_error_2_percent"],
            "absolute_error_2": sound["air"]["absolute_error_2"]
        },
        "aluminum": {
            "c_al": sound["aluminum"]["c_al"],
            "E_Y_al": sound["aluminum"]["E_Y_al"],
            "relative_error_E_percent": sound["aluminum"]["relative_error_E_percent"],
            "absolute_error_E": sound["aluminum"]["absolute_error_E"]
        }
    }

    return result

func={3:difrakcija,1:gustina,2:process_lens}