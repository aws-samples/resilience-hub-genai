#!/bin/bash


# Infra Deployment
echo "🏗  - Building the infrastructure with CDK."
cd backend
if ./backend_deploy.sh; then
    echo "✅ - Infrastructure built successfully."
else
    echo "❌ - Error building the infrastructure with CDK ... 🤔"
    exit 1
fi

# Copy Infra Config to SPA
echo "🔂 - Copying CDK Outputs to SPA Config"
cd ..
if cp backend/output/cdk-output.json frontend/src/config/; then
    echo "✅ - CDK outputs copied to SPA config successfully."
else
    echo "❌ - Error copying CDK outputs to SPA config ... 🤔"
    exit 1
fi

# SPA Deployment
echo "🏗  - Installing, Building and Deploying SPA."
cd frontend
if npm install && ./frontend_deploy.sh; then
    echo "✅ - SPA deployed successfully."
else
    echo "❌ - Error installing, building or deploying the SPA ... 🤔"
    exit 1
fi

# Done
cd ..
echo "✅ - Done! 🚀"
