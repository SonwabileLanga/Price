#!/bin/bash

# Price Comparison Application Startup Script

echo "🚀 Starting Price Comparison Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "🌐 Starting Django development server..."
echo "📍 Application will be available at: http://127.0.0.1:8000/"
echo "📍 Admin panel: http://127.0.0.1:8000/admin/"
echo "👤 Admin credentials: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
