# CB+ backend mini test 
# 1. Summary
You will be tasked with updating the project contained in this repo to add a few features and update current ones.
The website contained in this project is a small inventory in which users can add products and their expiry dates to track them.
It works well but is not very user friendly. 

# 2. Expected changes
* When adding a new product, the user should not have to enter a product name
* When adding a new product, the user should only be able to enter a 13 digits reference in the Gtin field
* When adding a new product, the site should send a request to OpenFoodFact to gather the product name and an image url. The api documentation can be found here: https://world.openfoodfacts.org/data
* On the home page, in the list of products, the photo from OpenFoodFact, along with the name, should be displayed

# 3. Expected results
1. Clone the project in this repo
2. Make the necesary changes
3. Submit the link to a public repo whith your updated code. 

# 4. Install
To install and run the current project, follow those steps.

1. Install postgreSQL if you don't have it
2. Create a virtual environment at the root of the project
3. Open the virtual env
4. Inside the virtual env, install the dependencies described in the pipfile
5. Run `python manage.py migrate` to create the database
6. Run `python manage.py runserver` to start the server
7. The website should be available at `http://127.0.0.1:8000/inventory/`