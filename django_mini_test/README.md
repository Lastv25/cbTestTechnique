# CB+ backend mini test 
# 1. Expected changes
* When adding a new product, the user should not have to enter a product name
* When adding a new product, the user should only be able to enter a 13 digits reference in the Gtin field
* When adding a new product, the site should send a request to OpenFoodFact to gather the product name and an image url. The api documentation can be found here: https://world.openfoodfacts.org/data
* On the home page, in the list of products, the photo from OpenFoodFact, along with the name, should be displayed

# 2. Changes Summary
To answer the different questions presented in the test changes have been made to the view.py, models.py, index.html,form.py and a new python script was created openfood.py

Changes:

form.py: the field name was commented
models.py: a field image_url was added. Setters and getters for the field were added
index.html: an image appears near the name of the product on the home page
view.py: item_create calls a function defined in the openfood.py file. This functions uses the gtin value and returns a name string and an image url. The values are set in the item objects before beign saved.
openfood.py: defines a function that makes a get request to the https://world.openfoodfacts.org/ with a gtin and returns a name and image url.


# 4. Install
To install and run the current project, follow those steps.

1. Install postgreSQL if you don't have it
2. Create a virtual environment at the root of the project
3. Open the virtual env
4. Inside the virtual env, install the dependencies described in the pipfile and the requests library
5. Run `python manage.py migrate` to create the database
6. Run `python manage.py runserver` to start the server
7. The website should be available at `http://127.0.0.1:8000/inventory/`
