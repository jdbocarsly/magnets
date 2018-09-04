# styles and data-munging for the magnet website

trans = str.maketrans('0123456789.-','₀₁₂₃₄₅₆₇₈₉.₋')

def make_subscripts(string):
   return string.translate(trans)

FONTSIZE="14pt"
TYPEFACE = "Lato"
#SIZES = list(range(6, 22, 3))
#COLORS = Plasma256
TOOLS="box_zoom, reset, hover,tap"

style = {'attrs': {

    # apply defaults to Figure properties
    'Figure': {
        'toolbar_location': "above",
        'outline_line_color': None,
        'min_border_right': 10,
    },
    'Title': {
    'text_font_size':FONTSIZE,
    'text_font_style':'bold',
    'text_font': TYPEFACE,
    },

    # apply defaults to Axis properties
    'Axis': {
        'axis_label_text_font': TYPEFACE,
        'axis_label_text_font_style':'normal',
        'axis_label_text_font_size': FONTSIZE,
        'major_tick_in': None,
        'minor_tick_out': None,
        'minor_tick_in': None,
        'axis_line_color': '#CAC6B6',
        'major_tick_line_color': '#CAC6B6',
        'major_label_text_font_size': FONTSIZE,
        'axis_label_standoff':15
    },

     # apply defaults to Legend properties
    'Legend': {
        'background_fill_alpha': 0.8,
    }
}}

dos_cols = [
"Curie temperature (K)",
"−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)",
"−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)",
"magnetic deformation (Σm), %",
"largest local moment (µB)",
"gravimetric moment (emu/g)",
"volumetric moment (emu/cm³)",
"moment per atom (µB/atom)",
"energy of spin-polarization (eV/atom)",
"theoretical density (g/cm³)",
"source (experimental)",
]

axis_columns_groups = [
("experimental properties",
    [
    "Curie temperature (K)",
    "−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)",
    "−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)",
    ]),
("calculated magnetic properties",
    [
    "gravimetric moment (emu/g)",
    "volumetric moment (emu/cm³)",
    "moment per atom (µB/atom)",
    "largest local moment (µB)",
    "energy of spin-polarization (eV/atom)",
    "magnetic deformation (Σm), %",
    "Σm x gravimetric moment",
    ]),
("structural properties",
    [
    "theoretical density (g/cm³)",
    ]),
("magnetocaloric properties",
    [
    "−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)",
    "−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)",
    "magnetic deformation (Σm), %",
    ]),
]

axis_columns = [
"class",
"element carrying largest moment",
"−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)",
"−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)",
"Curie temperature (K)",
"gravimetric moment (emu/g)",
"volumetric moment (emu/cm³)",
"moment per atom (µB/atom)",
"largest local moment (µB)",
"theoretical density (g/cm³)",
"magnetic volume change (%)",
"magnetic deformation (Σm), %",
"Σm x gravimetric moment",

]

discrete_columns = {
'element carrying largest moment':["Cr","Mn","Fe","Co","Ni"],
'class':["heusler","perovskite","antiperovskite","Co2P","MnAs"],
}