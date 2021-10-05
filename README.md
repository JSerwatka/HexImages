
### Getting Started

1. Run the multi-container app: `docker-compose up`
2. Open django container's bash: `docker exec -it hex_images bash`
3. Run migration: `python manage.py migrate`
4. Create an admin account with `python manage.py createsuperuser`
5. From the admin panel create 3 account tiers: Basic, Premium, Enterprise. Enter available image height as comma-seperated positive integer list (e.g., "200,400").