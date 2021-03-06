import pandas as pd
import numpy as np
from molar_mass import calc_molar_mass



df_mcs = pd.read_pickle("new_processed_results.df")
df_predictions = pd.read_pickle("new_predictions.df")
df_dft = pd.concat([df_mcs, df_predictions])

df_experimental = pd.read_csv("experimental_data.csv",sep='\t', comment="#")

df = pd.merge(df_dft, df_experimental, on="material_name")
df["molar_mass"] = [calc_molar_mass(f) for f in df.formula]

# df = df[df["material_name"] != "WMn2Sn"]

print(df.columns)
df2= pd.DataFrame()
df2["material_name"] = df["material_name"]
df2["formula"] = df["formula"]
df2["class"] = df["class"]
df2["−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)"]=-df["DSm_2T"]
df2["−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)"]=-df["DSm_5T"]
df2["Curie temperature (K)"]=df["Curie temperature (K)"]
df2["source (experimental)"] = df["doi_link"]
df2["−ΔSm(H = 2T) (mJ cm⁻³ K⁻¹)"]=-df["DSm_2T"]*df["density"]
df2["−ΔSm(H = 5T) (mJ cm⁻³ K⁻¹)"]=-df["DSm_5T"]*df["density"]
#df2["deltaSm_per_mag_ion"]=-1*df["DSm_5T"]/1000.*df["molar_mass"]*df["natoms"]/df["nmag_ions"]
#df2["deltaSm_per_atom"]=-1*df["DSm_5T"]/1000.*df["molar_mass"]
#J      kg     g               mol_fu
#kg K   g    mol_fu       mols magnetic ions
#DFT:
#df2["all_moments"]  = df["all_moments"]

#magnetism
df2["energy of spin-polarization (eV/atom)"]=df["spin_polarization_energy"]/df["natoms"]
df2["magnetic deformation (Σm), %"]=df["magnetic_deformation"]
df2["largest local moment (µB)"]=df["max_moment"]
df2["gravimetric moment (emu/g)"]=df["grav_moment"].abs()
df2["volumetric moment (emu/cm³)"]=df["vol_moment"].abs()
df2["moment per atom (µB/atom)"]=df["atomic_moment"].abs()
df2["element carrying largest moment"]=df["max_moment_element"]
df2["average magnetic moment (µB)"]=df['average_magnetic_moment']
df2["average magnetic moment (µB)"]=df['average_magnetic_moment']
df2["sigma_m_times_grav_moment"]=df["magnetic_deformation"]*df["grav_moment"].abs()

#dos-related
df2["spin polarization at fermi level (%)"] = df["spin_polarization_at_efermi"]*100.
df2["nonmag. DOS at fermi level (states/eV/atom)"] = df['dos_at_efermi_nsp_per_atom']

df2["nonmag. DOS at fermi level (states/eV/mag. ion)"] = df['dos_at_efermi_nsp_per_mag_ion']
# df2["nonmag. DOS at fermi level (states/eV/mag. ion)"] = df2["nonmag. DOS at fermi level (states/eV/mag. ion)"].replace(np.inf, np.nan) #avoid infinites from dividing by 0

#structural properties
df2["density (g/cm³)"]=df["density"]
df2["spacegroup number"]=df["spacegroup_number"]
df2["spacegroup symbol"]=df["spacegroup_symbol"]
df2["closest magnetic ion spacing (Å)"]=df["shortest_magnetic_ion_spacing"]
df2["number of unique magnetic sites"]=df["num_unique_magnetic_sites"].astype(int)
print(df2["number of unique magnetic sites"])

df2["natoms"] = df["natoms"]
df2["cid"] = df.index

# #df2[""]

df2.to_pickle("clean_pickle2.df")
df2.to_csv("clean_df2.csv")




