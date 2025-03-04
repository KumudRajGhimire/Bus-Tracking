from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Sample data for buses
buses = [
    {"id": 1, "route": "Route 1", "lat": 13.06329, "lng": 77.36322, "active": True},
    {"id": 2, "route": "Route 2", "lat": 12.9473949, "lng": 77.5538716, "active": True},
]

# Initial commuter location
commuter = {"lat": 0, "lng": 0}

@app.route('/')
def index():
    return render_template('index.html', buses=buses, commuter=commuter)

@app.route('/driver')
def mobile():
    return render_template('mobile.html')

@socketio.on('update_location')
def handle_update_location(data):
    if data['type'] == 'bus':
        bus_id = int(data['id'])
        bus_found = False
        for bus in buses:
            if bus['id'] == bus_id:
                if data.get('stop', False):
                    bus['active'] = False
                else:
                    bus['lat'] = float(data['lat'])
                    bus['lng'] = float(data['lng'])
                    bus['active'] = True
                bus_found = True
                break
        if not bus_found:
            new_bus = {
                "id": bus_id,
                "route": data.get('route', f"Route {bus_id}"),
                "lat": float(data['lat']),
                "lng": float(data['lng']),
                "active": True,
            }
            buses.append(new_bus)
    elif data['type'] == 'commuter':
        commuter['lat'] = float(data['lat'])
        commuter['lng'] = float(data['lng'])

    emit('location_update', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
