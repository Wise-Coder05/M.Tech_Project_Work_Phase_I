#!/bin/bash

# Log file for tracking actions
LOGFILE="traffic_generation.log"
target_ip = "20.6.129.240"
duration = "0.01"

# Function to log messages with timestamps
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOGFILE
}

# Function to setup Azure VM Environment
setup_azure_vm() {
    log_message "Setting up Azure VM environment..."
    
    # Install necessary packages
    sudo apt-get update >> $LOGFILE 2>&1
    sudo apt-get install -y python3 python3-pip tshark scapy flask pandas scikit-learn matplotlib >> $LOGFILE 2>&1
    
    log_message "Azure VM setup completed."
}

# Function to validate IP address format
validate_ip() {
    local ip=$1
    if [[ $ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to generate Normal Traffic
generate_normal_traffic() {
    local target_ip=$1
    local duration=$2
    
    log_message "Generating normal traffic to $target_ip for $duration seconds..."
    
    end_time=$(($(date +%s) + duration))
    
    while [ $(date +%s) -lt $end_time ]; do
        ping -c 1 $target_ip > /dev/null 2>&1
        log_message "Normal ping to $target_ip"
        sleep 1 # Control rate of normal traffic
    done
    
    log_message "Normal traffic generation completed."
}

# Function to generate Malicious Traffic (Ping Flood)
generate_malicious_traffic() {
    local target_ip=$1
    local duration=$2
    
    log_message "Generating malicious traffic (ping flood) to $target_ip for $duration seconds..."
    
    end_time=$(($(date +%s) + duration))
    
    while [ $(date +%s) -lt $end_time ]; do
        for i in {1..5}; do
            hping3 --icmp -c 1 $target_ip > /dev/null 2>&1
            log_message "Malicious ping flood to $target_ip"
        done
        sleep 0.1 # Control rate of malicious traffic
    done
    
    log_message "Malicious traffic generation completed."
}

# Function to extract features using TShark
extract_features() {
    local pcap_file=$1
    
    log_message "Extracting features from $pcap_file using TShark..."
    
    tshark -r "$pcap_file" -T fields -e ip.src -e ip.dst -e icmp.type -e icmp.code > features.csv 2>>$LOGFILE
    
    if [ $? -eq 0 ]; then
        log_message "Feature extraction completed. Features saved to features.csv."
    else
        log_message "Error during feature extraction."
        exit 1
    fi
}

# Function to train machine learning models (simplified)
train_models() {
    log_message "Training machine learning models..."
    
    # Placeholder for Python script execution to train models
    python3 train_models.py >> $LOGFILE 2>&1
    
    if [ $? -eq 0 ]; then
        log_message "Model training completed."
    else
        log_message "Error during model training."
        exit 1
    fi
}

# Function to setup dashboard for visualization
setup_dashboard() {
    log_message "Setting up dashboard..."
    
    FLASK_APP=dashboard.py flask run --host=0.0.0.0 --port=5000 &
    
    if [ $? -eq 0 ]; then
        log_message "Dashboard is running at http://localhost:5000"
    else
        log_message "Error starting the dashboard."
        exit 1
    fi
}

# Main Execution Flow with Error Handling and Logging 
main() {
    setup_azure_vm

    target_ip="192.168.1.100" # Example target IP address

    # Validate IP address format before proceeding 
    if ! validate_ip "$target_ip"; then 
        echo "Invalid IP address format: $target_ip"
        exit 1 
    fi 

    duration=60 # Duration in seconds for traffic generation

    generate_normal_traffic "$target_ip" "$duration"
    
    generate_malicious_traffic "$target_ip" "$duration"
    
    extract_features "traffic_capture.pcap" # Example pcap file from previous captures
    
    train_models
    
    setup_dashboard

}

# run the main function and handle errors globally 
{
   main 
} || { 
   echo "An error occurred during execution. Check the log file for details." 
   exit 1 
}