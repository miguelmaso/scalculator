from flask import Blueprint, render_template, request, jsonify
import re
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from services.sections import ConcreteSection
from services.units import Units
from services.codes import StructureTypes

csection = Blueprint("csection", __name__)

@csection.route('/')
def index():
    return render_template('csection.html')

@csection.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Extract and validate inputs
    try:
        width = float(data.get('width', 0))
        depth = float(data.get('depth', 0))
        cover = float(data.get('cover', 0))
        top_tags = data.get('tags_top', [])  # Extract tags as a list
        bottom_tags = data.get('tags_bottom', [])
    except ValueError:
        return jsonify({'error': 'Invalid input'}), 400


    uts = Units(
        force = 'kN',
        moment = 'kNm',
        dimensions = 'mm'
    )

    width *= uts.dimensions.to_si
    depth *= uts.dimensions.to_si
    cover *= uts.dimensions.to_si
    reinf_top = reinforcemet_from_tags(top_tags, width)
    reinf_bottom = reinforcemet_from_tags(bottom_tags, width)
    
    s = ConcreteSection(
        b=width,
        h=depth,
        cover=cover,
        As=reinf_bottom,
        As1=reinf_top)
    
    reduced_moment = s.reduced_moment * uts.moment.from_si

    ax_strain = np.linspace(-s.concrete.e1, s.concrete.e1)
    f = np.array([s.forces(a) for a in ax_strain])
    N, M = zip(*f)
    N = np.array(N) * uts.force.from_si
    M = np.array(M) * uts.moment.from_si

    # Plot the axial force-moment graph
    layout = go.Layout(
        xaxis = dict(
            minallowed = 0,
            title = f'N ({uts.force.name})',
            fixedrange = True,
            range=[0, max(N) * 1.05]
        ),
        yaxis = dict(
            minallowed = 0,
            title = f'M ({uts.moment.name})',
            fixedrange = True,
            range=[0, max(M) * 1.1]
        ),
        margin=dict(l=50, r=10, t=0, b=0),  # Reduce inner spacing
        paper_bgcolor='rgba(0,0,0,0)'       # Transparent background
    )
    fig = go.Figure(
        data = go.Scatter(x=N.tolist(), y=M.tolist()),
        layout = layout
    )
    graph_json = pio.to_json(fig)

    # Plot the section graph
    zero_crossing = np.where(np.diff(np.sign(N)))[0][0]
    a0 = ax_strain[zero_crossing]

    strain = s.strain(a0)
    stresses_c = s.stress_c(a0)
    z = s._z_c * uts.dimensions.from_si
    stresses_c = np.append(stresses_c, 0)
    z_c = np.append(z, z[-1])
    xrange_2 = [strain[0] * 1.05, strain[-1] * 1.05]
    xrange_1 = [strain[0] / strain[-1] * max(stresses_c) * 1.05, max(stresses_c) * 1.05]

    section_layout = go.Layout(
        xaxis = dict(
            range = xrange_1,
            fixedrange = True,
            visible = False
        ),
        xaxis2 = go.layout.XAxis(
            overlaying = 'x',
            range = xrange_2,
            fixedrange = True,
            visible = False
        ),
        yaxis = dict(
            fixedrange = True
        ),
        showlegend = False,
        margin=dict(l=50, r=10, t=0, b=40),  # Reduce inner spacing
        paper_bgcolor='rgba(0,0,0,0)'       # Transparent background
    )
    fig2 = go.Figure(layout=section_layout)
    fig2.add_trace(go.Scatter(x=stresses_c.tolist(), y=z_c.tolist(), fill='toself'))
    fig2.add_trace(go.Scatter(x=strain.tolist(), y=z.tolist(), xaxis='x2'))
    graph2_json = pio.to_json(fig2)

    return jsonify({
            'result': f'{reduced_moment:.2f}',
            'graph': graph_json,
            'graph2': graph2_json
        })


tag_pattern = re.compile(r'^(\d*)([hH])(\d+)(?:(@)(\d+))?$')

def reinforcemet_from_tags(tags, distance):
    area = 0
    for tag in tags:
        m = tag_pattern.match(tag)
        if m:
            num = m[1] or 1
            diam = m[3]
            every = m[5]
            num = int(num)
            diam = int(diam)
            a = num * np.pi * diam**2 * 0.25 * 1e-6
            if every:
                every = int(every) * 1e-3
                a *= distance / every
            area += a
    return area


if __name__ == '__main__':
    csection.run(debug=True)
