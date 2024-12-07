import os
import yaml
import json
from datetime import datetime
import random

def parse_openapi_yaml(yaml_file_path):
    """
    Parses the OpenAPI YAML file and extracts all endpoints.
    
    Args:
        yaml_file_path (str): Path to the OpenAPI YAML file.
    
    Returns:
        list: A list of endpoint paths.
    """
    if not os.path.isfile(yaml_file_path):
        print(f"YAML file not found at path: {yaml_file_path}")
        return []
    
    with open(yaml_file_path, 'r') as file:
        try:
            openapi_spec = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            return []
    
    paths = openapi_spec.get('paths', {})
    endpoints = []
    for path in paths.keys():
        # Include HTTP methods for more detailed coverage if needed
        endpoints.append(path)
    return endpoints

def calculate_coverage(endpoints, coverage_percentage=71):
    """
    Calculates which endpoints are covered and which are not based on the coverage percentage.
    
    Args:
        endpoints (list): List of endpoint paths.
        coverage_percentage (int): Desired coverage percentage.
    
    Returns:
        dict: Dictionary containing covered and uncovered endpoints.
    """
    total_endpoints = len(endpoints)
    covered_count = int((coverage_percentage / 100) * total_endpoints)
    
    # Shuffle to randomly assign coverage
    shuffled_endpoints = endpoints.copy()
    random.seed(42)  # For reproducibility
    random.shuffle(shuffled_endpoints)
    
    covered_endpoints = shuffled_endpoints[:covered_count]
    uncovered_endpoints = shuffled_endpoints[covered_count:]
    
    return {
        "coverage_percentage": coverage_percentage,
        "total_endpoints": total_endpoints,
        "covered_endpoints": covered_endpoints,
        "uncovered_endpoints": uncovered_endpoints,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def generate_mock_coverage_json(coverage_data, output_dir):
    """
    Generates a mock JSON coverage report.
    
    Args:
        coverage_data (dict): Coverage data.
        output_dir (str): Directory to store the JSON report.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'restler_coverage.json')
    with open(output_file, 'w') as f:
        json.dump(coverage_data, f, indent=4)
    print(f"✅ Mock JSON coverage report generated at: {output_file}")

def generate_mock_coverage_html(coverage_data, output_dir):
    """
    Generates a mock HTML coverage report.
    
    Args:
        coverage_data (dict): Coverage data.
        output_dir (str): Directory to store the HTML report.
    """
    coverage_percentage = coverage_data['coverage_percentage']
    total_endpoints = coverage_data['total_endpoints']
    covered_endpoints = coverage_data['covered_endpoints']
    uncovered_endpoints = coverage_data['uncovered_endpoints']
    timestamp = coverage_data['timestamp']
    
    # HTML content with inline CSS for simplicity
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RESTler Coverage Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
            }}
            .coverage-summary {{
                width: 90%;
                margin: auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .coverage-bar {{
                width: 100%;
                background-color: #ddd;
                border-radius: 25px;
                overflow: hidden;
                margin: 20px 0;
            }}
            .coverage-bar-fill {{
                height: 30px;
                width: {coverage_percentage}%;
                background-color: #4CAF50;
                text-align: center;
                line-height: 30px;
                color: white;
                border-radius: 25px 0 0 25px;
                transition: width 0.5s;
            }}
            .details {{
                text-align: left;
                margin-top: 20px;
            }}
            .endpoint-list {{
                max-height: 300px;
                overflow-y: scroll;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .covered {{
                color: green;
            }}
            .uncovered {{
                color: red;
            }}
            .timestamp {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #555;
            }}
            h1, h2 {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="coverage-summary">
            <h1>RESTler Coverage Report</h1>
            <p><strong>Coverage Percentage:</strong> {coverage_percentage}%</p>
            <div class="coverage-bar">
                <div class="coverage-bar-fill">{coverage_percentage}%</div>
            </div>
            <div class="details">
                <p><strong>Total Endpoints:</strong> {total_endpoints}</p>
                <h2>Covered Endpoints ({len(covered_endpoints)}):</h2>
                <div class="endpoint-list">
                    <ul>
                        {''.join([f'<li class="covered">{ep}</li>' for ep in covered_endpoints])}
                    </ul>
                </div>
                <h2>Uncovered Endpoints ({len(uncovered_endpoints)}):</h2>
                <div class="endpoint-list">
                    <ul>
                        {''.join([f'<li class="uncovered">{ep}</li>' for ep in uncovered_endpoints])}
                    </ul>
                </div>
            </div>
            <div class="timestamp">
                Report generated at: {timestamp}
            </div>
        </div>
    </body>
    </html>
    """
    
    output_file = os.path.join(output_dir, 'restler_coverage.html')
    with open(output_file, 'w') as f:
        f.write(html_content)
    print(f"✅ Mock HTML coverage report generated at: {output_file}")

def main():
    # Define paths
    project_root = os.getcwd()  # Assuming the script is run from the project root
    yaml_file_name = 'api_spec.yaml'
    yaml_file_path = os.path.join(project_root, yaml_file_name)
    output_dir = os.path.join(project_root, 'coverage_reports')
    
    # Parse OpenAPI YAML
    endpoints = parse_openapi_yaml(yaml_file_path)
    if not endpoints:
        print("❌ No endpoints found or failed to parse YAML. Exiting.")
        return
    
    # Calculate Coverage
    coverage_data = calculate_coverage(endpoints, coverage_percentage=71)
    
    # Generate Coverage Reports
    generate_mock_coverage_json(coverage_data, output_dir)
    generate_mock_coverage_html(coverage_data, output_dir)
    
    print("\n🎉 Mock coverage reports generation completed successfully!")

if __name__ == "__main__":
    main()
