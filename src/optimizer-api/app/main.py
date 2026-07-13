import os
from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge
from fastapi.responses import Response

app = FastAPI(title="FinOps & GreenOps Cloud Optimizer API")

# Definisanje Prometheus metrika za dashboard
POTENTIAL_SAVINGS = Gauge('optimizer_potential_savings_dollars', 'Potential cloud cost savings in USD')
CARBON_FOOTPRINT = Gauge('optimizer_carbon_footprint_kg', 'Current estimated carbon footprint in kg CO2e')
WASTED_RESOURCES = Gauge('optimizer_wasted_resources_count', 'Number of unoptimized or wasted resources')

@app.get("/health")
def health_check():
    # Jednostavan health check za Kubernetes probes
    return {"status": "healthy"}

@app.get("/api/v1/optimize")
def get_optimization_data():
    """
    Simulira ili stvarno povlači podatke sa AWS-a u zavisnosti od kredencijala.
    Računa FinOps uštede i GreenOps ekološki otisak.
    """
    # Provera da li imamo AWS kredencijale, ako ne - idemo u Mock mod
    aws_configured = os.getenv("AWS_ACCESS_KEY_ID") is not None
    
    if not aws_configured:
        # Mock podaci koji simuliraju predimenzionisane i zaboravljene resurse
        wasted_count = 5  # npr. 3 neaktivna EBS volumena i 2 neiskorišćena Elastic IP-ja
        savings = 124.50  # Ušteda u dolarima mesečno
        carbon = 45.20    # Karbonski otisak u kg CO2e koji možemo da smanjimo
        mode = "mock"
    else:
        # Ovde će kasnije doći stvarni Boto3 pozivi za AWS
        wasted_count = 0
        savings = 0.0
        carbon = 0.0
        mode = "production"

    # Osvežavanje Prometheus metrika prilikom svakog poziva API-ja
    POTENTIAL_SAVINGS.set(savings)
    CARBON_FOOTPRINT.set(carbon)
    WASTED_RESOURCES.set(wasted_count)

    return {
        "status": "success",
        "environment_mode": mode,
        "metrics": {
            "unoptimized_resources": wasted_count,
            "potential_monthly_savings_usd": savings,
            "potential_co2_reduction_kg": carbon
        },
        "recommendations": [
            {"resource_id": "vol-0abc1234789fa", "type": "EBS", "action": "Delete", "reason": "Unattached for 30+ days", "saving_usd": 15.50},
            {"resource_id": "i-0987654321fedc", "type": "EC2", "action": "Downsize", "reason": "CPU utilization less than 5%", "saving_usd": 109.00}
        ]
    }

@app.get("/metrics")
def metrics():
    # Endpoint namenjen Prometheus-u
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
