from flask import Blueprint, render_template, request, jsonify
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from services.sections import ConcreteSection
from services.units import Units

csection = Blueprint("csection", __name__)

@csection.route('/')
def index():
    return render_template('csection.html')

@csection.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Extract and validate inputs
    try:
        width = float(data.get('input1', 0))
        depth = float(data.get('input2', 0))
        covering = float(data.get('input3', 0))
    except ValueError:
        return jsonify({'error': 'Invalid input'}), 400


    uts = Units(
        force = 'kN',
        moment = 'kNm',
        dimensions = 'mm'
    )
    
    s = ConcreteSection(
        b=width/uts.dimensions.factor,
        h=depth/uts.dimensions.factor,
        covering=covering/uts.dimensions.factor,
        As=0.005,
        As1=0)
    
    a_strain = np.linspace(-s.concrete.e1, s.concrete.e1)
    f = np.array([s.forces(a) for a in a_strain])
    N, M = zip(*f)
    N = np.array(N)
    M = np.array(M)

    layout = go.Layout(
        xaxis = dict(
            minallowed = 0,
            title = f'N ({uts.force.name})',
            fixedrange = True
        ),
        yaxis = dict(
            minallowed = 0,
            title = f'M ({uts.moment.name})',
            fixedrange = True
        )
    )
    fig = go.Figure(
        data = go.Scatter(x=(uts.force.factor*N).tolist(), y=(uts.moment.factor*M).tolist()),
        layout = layout
    )
    graph_json = pio.to_json(fig)

    result = N[10] * uts.force.factor
    
    return jsonify({'result': f'{result:.2f}', 'graph': graph_json})

if __name__ == '__main__':
    csection.run(debug=True)
