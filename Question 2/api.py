from flask import Flask, request, jsonify
import concurrent.futures
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Process sensor data
def process_reading(reading):
    logging.info(f"Processing reading: {reading}")
    # Simulate some processing time
    time.sleep(0.1)
    # Example transformation
    processed_reading = {
        'sensor_id': reading['sensor_id'],
        'value': reading['value'] * 2,  # Example transformation
        'timestamp': time.time()
    }
    logging.info(f"Processed reading: {processed_reading}")
    return processed_reading

# API endpoint to receive sensor readings
@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if not data or 'readings' not in data:
        return jsonify({'error': 'Invalid data format'}), 400

    readings = data['readings']
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Process each reading concurrently
        processed_readings = list(executor.map(process_reading, readings))

    return jsonify({'processed_readings': processed_readings}), 200

if __name__ == '__main__':
    # Use threaded=True to enable multithreading
    app.run(host='0.0.0.0', port=5000, threaded=True)
