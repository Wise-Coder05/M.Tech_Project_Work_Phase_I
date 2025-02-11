import pandas as pd
from flask import Flask, render_template, jsonify
from scapy.all import sniff, ICMP
import threading
import csv
import os

app = Flask(__name__)

# Global DataFrame to store ping data
ping_data = pd.DataFrame(columns=["Malicious or Normal", "Size of the packet", "IP Address"])

# CSV file to store the data
csv_file_path = "ping_data.csv"

# Function to classify and store pings
def process_packet(packet):
    global ping_data

    if packet.haslayer(ICMP):  # Check if it's an ICMP packet
        size = len(packet)
        ip_address = packet[1].src
        
        # Simple classification logic
        if size > 100:  # Example threshold for malicious
            classification = "Malicious"
        else:
            classification = "Normal"

        # Append to DataFrame
        new_row = pd.Series([classification, size, ip_address], index=ping_data.columns)
        ping_data = ping_data.append(new_row, ignore_index=True)

        # Save to CSV
        ping_data.to_csv(csv_file_path, index=False)

# Packet capture thread
def start_sniffing():
    sniff(prn=process_packet, filter="icmp", store=0)  # Capture only ICMP packets

# Flask route for the dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch the live data
@app.route('/live-data')
def live_data():
    return jsonify(ping_data.to_dict(orient='records'))

if __name__ == '__main__':
    # Start the sniffing thread
    sniffing_thread = threading.Thread(target=start_sniffing)
    sniffing_thread.daemon = True  # Allow thread to exit when the main program does
    sniffing_thread.start()

    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
