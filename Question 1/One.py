from prometheus_client import start_http_server, Summary, Gauge, Counter
import psutil
import time
import sys

# Create Prometheus metrics to track execution time, memory usage, and errors
REQUEST_TIME = Summary('script_execution_time_seconds', 'Time spent processing')
MEMORY_USAGE = Gauge('script_memory_usage_bytes', 'Memory usage of the script')
ERRORS = Counter('script_errors_total', 'Number of errors in the script')

def monitor():
    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Track memory usage
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)

@REQUEST_TIME.time()
def main():
    try:
        monitor()
        
        # Your main script logic here
        # e.g., complex calculations, data processing, etc.
        time.sleep(5)  # Simulating some work

    except Exception as e:
        ERRORS.inc()  # Increment the error counter
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
