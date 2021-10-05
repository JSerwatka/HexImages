
### Getting Started
#### Cloning
1. Close the repo: `git clone https://github.com/JSerwatka/HexImages.git`
2. Change directory: `cd HexImages`

#### Running 
1. Run the multi-container app: `docker-compose up`
2. Run bash inside the django app container: `docker exec -it hex_images bash`
3. Run migration: `python manage.py migrate`
4. Create an admin account with `python manage.py createsuperuser`
5. Your development server is available at localhost:8000
6. From the admin panel create 3 account tiers: Basic, Premium, Enterprise. Enter available image heights as comma-seperated positive integer list (e.g., "200,400").

### Warning
If `docker-compose up` don't run, make sure that wait-for-it.sh has LR line break.
