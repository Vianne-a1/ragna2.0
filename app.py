from flask import Flask, render_template, request
import random

app = Flask(__name__)

properties = {
    'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1, 'J': 1,
    'K': 1, 'L': 1, 'M': 1, 'N': 1, 'O': 1, 'P': 1, 'Q': 1,
    'Frost': 2, 'Hota': 2, 'Jabber': 2, 'Obsc': 2, 'Sino': 2, 'Vaga': 2,
    'DW': 3
}

linkage = {
    'A': ['K', 'L', 'B'],
    'B': ['A', 'Vaga', 'Jabber', 'C'],
    'C': ['B', 'Jabber', 'D'],
    'D': ['C', 'O', 'P'],
    'E': ['F', 'Hota'],
    'F': ['G', 'Obsc', 'E'],
    'G': ['H', 'Frost', 'Obsc', 'F'],
    'H': ['J', 'N', 'Frost', 'G'],
    'J': ['K', 'Sino'],
    'K': ['Sino', 'L', 'M', 'A'],
    'L': ['A', 'K', 'Vaga'],
    'M': ['K', 'Vaga', 'N'],
    'N': ['Sino', 'M', 'DW', 'H'],
    'O': ['Jabber', 'D', 'Q'],
    'P': ['Q', 'Hota'],
    'Q': ['Obsc', 'O', 'P'],
    'Frost': ['H', 'G', 'Obsc'],
    'Hota': ['E', 'P', 'D'],
    'Jabber': ['DW', 'O', 'C', 'B'],
    'Obsc': ['Frost', 'DW', 'Q', 'F'],
    'Sino': ['J', 'N', 'K'],
    'Vaga': ['M', 'DW', 'L', 'Jabber'],
    'DW': ['N', 'Vaga', 'Jabber', 'Obsc']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    # Initialize guilds with their starting properties
    guilds = {}
    for i in range(1, 5):
        name = request.form.get(f'guild{i}_name', '').strip()
        props = request.form.get(f'guild{i}_properties', '').strip()
        
        if not name:
            return render_template('index.html', error=f"Guild {i} name is required.")
        if not props:
            return render_template('index.html', error=f"Guild {i} properties are required.")
        
        properties_list = [p.strip() for p in props.split(',') if p.strip()]
        for prop in properties_list:
            if prop not in properties:
                return render_template('index.html', error=f"Invalid property '{prop}' for Guild {i}.")
        
        guilds[name] = {'properties': properties_list, 'points': 0}

    # Simulation setup
    days = 6
    ownership = {day: {guild: [] for guild in guilds} for day in range(1, days + 1)}
    points = {guild: {day: 0 for day in range(1, days + 1)} for guild in guilds}
    claimed_properties = set()

    # Simulate each day
    for day in range(1, days + 1):
        for guild, info in guilds.items():
            # Claim new properties
            new_claims = claim_properties(info['properties'], linkage, claimed_properties)
            info['properties'].extend(new_claims)
            daily_points = sum(properties[prop] for prop in new_claims)
            info['points'] += daily_points

            # Update daily records
            ownership[day][guild] = list(info['properties'])
            points[guild][day] = info['points']
            claimed_properties.update(new_claims)

    return render_template('index.html', ownership=ownership, points=points, guilds=guilds)

def claim_properties(owned_properties, linkage, claimed_properties):
    # Find properties linked to the guild's current properties
    available_properties = set()
    for prop in owned_properties:
        if prop in linkage:
            for linked_prop in linkage[prop]:
                if linked_prop not in owned_properties and linked_prop not in claimed_properties:
                    available_properties.add(linked_prop)
    return random.sample(list(available_properties), min(3, len(available_properties)))

if __name__ == '__main__':
    app.run(debug=True)
