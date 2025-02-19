from flask import Blueprint, render_template, request, jsonify
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

main_routes = Blueprint("main", __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Extract and validate inputs
    try:
        input1 = float(data.get('input1', 0))
        input2 = float(data.get('input2', 0))
        input3 = float(data.get('input3', 0))
    except ValueError:
        return jsonify({'error': 'Invalid input'}), 400
    
    # Perform calculations (example: simple numpy operation)
    result = np.sin(input1) + np.cos(input2) * input3
    
    # Generate a Plotly graph
    x = np.linspace(0, 10, 100)
    y = np.sin(x * input1) + np.cos(x * input2)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Result Curve'))
    graph_json = pio.to_json(fig)
    
    return jsonify({'result': result, 'graph': graph_json})

if __name__ == '__main__':
    main_routes.run(debug=True)
