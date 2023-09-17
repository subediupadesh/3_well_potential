################################################################
#### Created by Upadesh Subedi 17th Sept 2023

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(layout="wide")
st.title('Free Energy 3 Well Potential')
st.write('For the equation type : G$_{free}$ = A.c$_1$ + B.c$_2$ + C.(1 - c$_1$ - c$_2$) + D.c$_1$.c$_2$ + E.c$_2$.(1 - c$_1$ - c$_2$) + F.(1 - c$_1$ - c$_2$).c$_1$ + R.T.[c$_1$.ln(c$_1$) + c$_2$.ln(c$_2$) + (1 - c$_1$ - c$_2$).ln(1 - c$_1$ - c$_2$)')
st.write('Where c1, and c2 are two composition of ternary alloy system')

cm1, cm2 = st.columns([1, 2]) 

A = cm1.slider('A', -10000, 0, -5450, 1)
B = cm1.slider('B', -10000, 0, -5120, 1)
C = cm1.slider('C', -10000, 0, -4753, 1)
D = cm1.slider('D', 0, 50000, 36500, 100)
E = cm1.slider('E', 0, 50000, 38350, 100)
F = cm1.slider('F', 0, 50000, 39150, 100)
T = cm1.slider('T', 0, 2000, 1030, 10)
R = 8.31


# Create a triangular grid
n_points = 100
c_1 = np.linspace(0.0001, 1, n_points)
c_2 = np.linspace(0.0001, 1, n_points)
C1, C2 = np.meshgrid(c_1, c_2)

# Calculate Z values using triangular grid
Gibbs_tri = np.zeros_like(C1)
for i in range(len(C1)):
    for j in range(len(C1[i])):
        c1 = C1[i][j]
        c2 = C2[i][j]
        log_c1 = c1 * np.log(c1 + 1e-10) if c1 > 0 else 0
        log_c2 = c2 * np.log(c2 + 1e-10) if c2 > 0 else 0
        log_1_minus_c1_minus_c2 = (1 - c1 - c2) * np.log(1 - c1 - c2 + 1e-10) if (1 - c1 - c2) > 0 else 0
        Gibbs_tri[i][j] = A * c1 + B * c2 + C * (1 - c1 - c2) + D * c1 * c2 + E * c2 * (1 - c1 - c2) + F * (1 - c1 - c2) * c1 + R * T * (
                    c1 * np.log(c1) + c2 * np.log(c2) + (1 - c1 - c2) * np.log(1 - c1 - c2))



# Create a 3D plot
fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])

surface = go.Surface(x=C1, y=C2, z=Gibbs_tri, colorscale='rainbow')
fig.add_trace(surface)

# Add labels and title
fig.update_layout(scene=dict(xaxis_title=r'c1', yaxis_title=r'c2', zaxis_title='Gibbs'))
fig.update_layout(scene=dict(zaxis=dict(range=[-6000, 0], type='linear')))
fig.update_layout(scene=dict(camera=dict(eye=dict(x=1.5, y=1.5, z=0.2))))

fig.update_layout(width=1200, height=900)

# Display the plot using Streamlit
cm2.plotly_chart(fig, use_container_width=True)


#########################################################




