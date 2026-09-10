import pandas as pd

df_preds = pd.read_pickle("pickled_predictions4.df")
print(df_preds.columns)
df_mcs   = pd.read_pickle("pickled_panda6.df")
print(df_mcs.columns)
df = pd.concat([df_preds,df_mcs], ignore_index=True)

df2= pd.DataFrame()
df2["material_name"] = df["material_name"]
df2["formula"] = df["formula"]
df2["class"] = df["class"]
df2["−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)"]=-df["deltaSm_2T"]
df2["−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)"]=-df["deltaSm_5T"]
df2["Curie temperature (K)"]=df["Tc"]
df2["energy of spin-polarization (eV/atom)"]=df["SCP_3_atomic_spin_polarization_eng"]
df2["magnetic deformation (Σm), %"]=df["SCP_3_dold"]
df2["magnetic volume change (%)"]=df["SCP_3_vol_proxy"]
df2["largest local moment (µB)"]=df["SCP_3_max_moment"]
df2["element carrying largest moment"]=df["SCP_3_max_moment_sym"]
df2["theoretical density (g/cm³)"]=df["SCP_3_density"]
df2["gravimetric moment (emu/g)"]=df["SCP_3_grav_moment"].abs()
df2["volumetric moment (emu/cm³)"]=df["SCP_3_vol_moment"].abs()
df2["moment per atom (µB/atom)"]=df["SCP_3_atomic_moment"].abs()
#df2["Σm x gravimetric moment"]=df["SCP_3_combined_dold_gm"].abs()

df2["source (experimental)"] = ["dx.doi.org/10.1021/acs.chemmater.6b04729" if x=="present work" else x for x in df["doi_link"]]
df2["source (experimental)"] = [r'<a href="{}">{}</a>'.format(x,x) for x in df2["source (experimental)"]]

df2["cid"] = df.index

df2.to_pickle("clean_pickle.df")
df2.to_csv("clean_df.csv")