import streamlit as st
st.set_page_config(layout="wide")
import plotly 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import filtertools as ft
import sedpy.observate as sedobs

Font = plotly.graph_objects.scatter.hoverlabel.Font

galaxy_loc = "https://raw.githubusercontent.com/gbrammer/eazy-photoz/master/templates"

@st.cache
def get_templates():
    templates = pd.read_csv("data/galaxies.csv", index_col="name")
    return templates
# templates = {"Star-forming": f"{galaxy_loc}/EAZY_v1.0/eazy_v1.0_sed2.dat", "Quiescent": f"{galaxy_loc}/EAZY_v1.0/eazy_v1.0_sed5.dat"}

# @st.cache
def load_filters_sedobs():
    filters = []
    for fname in get_all_filters():
        if "all" in fname:
            continue
        for i, loaded in enumerate(ft.load_filter(fname)):
            filters.append(sedobs.Filter(fname,  data=(loaded.data[:, 0], loaded.data[:, 1])))

    # sedobs.load_filters(filters)
    return filters

@st.cache
def fetch_template(stype):
    templates = get_templates() 
    data = pd.read_csv(f"{galaxy_loc}/{templates.loc[stype]['template_file']}", names=["wl", "f"], sep='\s+')
    return data

@st.cache
def load_spectrum(stype=None, index=None, redshift=0.0):
    if stype is None:
        return None
    data = fetch_template(stype)
    wl = data['wl']
    spec = np.zeros((wl.shape[0], 2))
    spec[:, 0] = wl*(1+redshift)
    spec[:, 1] = data['f']/data['f'].max()
    return spec

def load_filters(filternames):
    pass

@st.cache
def load_lines():
    lines = pd.read_csv("data/lines.csv")
    return lines

@st.cache
def get_all_lines():
    return sorted(list(set([x for x in load_lines()['name'].values if x != "None"])))

@st.cache
def get_all_filters():
    return ft.get_all_filters()

# @st.cache
def make_figure(spectrum, filters, lines=None, log=False, do_phot=False):
    fig = px.line(x=spectrum[:, 0], y=spectrum[:, 1], width=1400, height=700)
    fig.update_xaxes(range=[wavelength_min, wavelength_max])
    filter_profiles = load_filters(filters)
    filts = {}
    xs = []
    ys = []
    texts = []
    for fname in filters:
        for i, loaded in enumerate(ft.load_filter(fname)):
            # loaded.data[:, 1]/=loaded.data[:, 1].max()
            filts[loaded.name] = loaded
            fig.add_trace(
                go.Scatter(x=loaded.data[:, 0], y=loaded.data[:, 1], text=loaded.name,
                name=""))
            tx = loaded.data[:, 1]
            max_2 = tx.max()/2
            xloc = np.where(tx > max_2)[0]
            x_mid = (loaded.data[xloc[0], 0] + loaded.data[xloc[-1], 0])/2
            xs.append(x_mid)
            ys.append(max_2 + (i%6-3)*.05)
            texts.append(loaded.name.split(".")[-1])
        fig.add_trace(go.Scatter(x=xs, y=ys, text=texts, textposition="bottom center", mode="text"))#, name="labels" ) 


    if show_lines:
        wls = []
        xs = []
        ys = []
        texts = []
        for i, line in load_lines().iterrows():
            wls.append(line['LBDA_REST'])
            wl = line['LBDA_REST'] * (1+redshift)
            name = line['name']
            if lines is not None and name not in lines:
                continue
            if wl > wavelength_min and wl  < wavelength_max:
                xs.append(wl)
                i = i%12
                ys.append(i*0.05 + 0.3)
                texts.append(name)
                fig.add_vline(
                        x=wl,
                        line_color="orange",
                        line_dash="dashdot",
                        opacity=0.5,
                        )

        hovers = [f"{x}:{int(y)}Å" if y<10000 else f"{x}:{y/10000:.3f}um" for x,y in zip(texts, wls)]
        fig.add_trace(go.Scatter(x=xs, y=ys, text=texts, textposition="bottom center", hovertext=hovers, mode="text", hoverinfo='text', name="", 
            textfont=plotly.graph_objs.scatter.Textfont(color="#016691")))

    fig.update_layout(showlegend=False)

    if do_phot:
        obs_wavelength = spectrum[:, 0]
        obs_flux = spectrum[:, 1]*1e-18
        sedobs_filters = load_filters_sedobs()
        observed_magnitudes = sedobs.getSED(obs_wavelength, obs_flux, filterlist=sedobs_filters)
    return fig

# Set up the app

st.title('Galaxy redshifter')

wavelength_min = st.sidebar.slider("WL start", min_value=0, max_value=20000, value=1000, step=1000)
wavelength_max = st.sidebar.slider("WL end", min_value=5000, max_value=100000, value=10000, step=5000)
redshift = st.sidebar.slider("Galaxy redshift", min_value=0., max_value=20.0, value=1.0, step=.1)

log = st.sidebar.checkbox("Log lambda")
show_lines = st.sidebar.checkbox("Show lines")
photometry = st.sidebar.checkbox("Photometry")
spectrum =  st.sidebar.selectbox(
    "Plot:",
    get_templates().index.values
)

filters = st.sidebar.multiselect(
    "Filters", options=get_all_filters(), default=[], format_func=lambda x: str(x), key='filters'
)

lines = None
if show_lines:
    default_lines = ['Cɪᴠ', 'Feɪɪ', 'Heɪɪ', 'Hα', 'Hβ', 'Hγ', 'Hδ', 'Hε', 'Lyα', 'Mgb', 'Mgɪ', 'Mgɪɪ', 'Oɪɪɪ]', 'Siɪv]', 'Siɪɪ', 'Siɪɪɪ]', '[Oɪɪ]', '[Oɪɪɪ]', '[Sɪɪ]']
    lines = st.sidebar.multiselect(
        "Lines", options=get_all_lines(), default=default_lines, format_func=lambda x: str(x), key='filters'
    )
    
fig = make_figure(load_spectrum(spectrum, redshift=redshift), filters, lines=lines, log=log, do_phot=photometry)

st.plotly_chart(fig)




