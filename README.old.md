# Module 1 Group Assignment

CSCI 5117, Spring 2022, [assignment description](https://canvas.umn.edu/courses/291031/pages/project-1)

## App Info:

* Team Name: Oysters
* App Name: Dribbbl
* App Link: <https://dribbbl.herokuapp.com>

### Students

* Ace Kaung, kaung006@umn.edu
* David Nguyen, nguy3482@umn.edu
* Julia Pan, pan00079@umn.edu
* Ishan Joshi, joshi304@umn.edu
* Sai Tallapragada, talla037@umn.edu 

## For Windows
```
$env:FLASK_ENV = "development"
$env:FLASK_APP = "app.py"
```


## Key Features

**Describe the most challenging features you implemented
(one sentence per bullet, maximum 4 bullets):**

* Getting and displaying the tags for each post on a page involved complicated SQL.
* Storing and retrieving user-drawn images from a Canvas required some work with data urls and image blobs.
* Making the website responsive for smaller screen sizes. 
* The search results can be viewed page by page, which was tricky because we needed to re-use and update our query strings for the correct page.

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**

* N/A


## Screenshots of Site

![](siteImages/web1.png)
The landing page of our website.

![](siteImages/web2.png)
This is the drawing page where users customize their drawing.

![](siteImages/web3.png)
The search page which allows for text and tag-based searching.

![](siteImages/web4.png)
This is the solver page where users can make guesses to drawings.

## Mock-up 

There are a few tools for mock-ups. Paper prototypes (low-tech, but effective and cheap), Digital picture edition software (gimp / photoshop / etc.), or dedicated tools like moqups.com (I'm calling out moqups here in particular since it seems to strike the best balance between "easy-to-use" and "wants your money" -- the free tier isn't perfect, but it should be sufficient for our needs with a little "creative layout" to get around the page-limit)

In this space please either provide images (around 4) showing your prototypes, OR, a link to an online hosted mock-up tool like moqups.com

**[Add images/photos that show your paper prototype (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository) along with a very brief caption:**

**[Online Prototype](https://www.figma.com/proto/Z6p2ELqO6YclZcascV2NvU/Lo-Fi?node-id=1%3A2&scaling=scale-down&page-id=0%3A1&starting-point-node-id=1%3A2)**

### A few notes:
* Some pages will have minor layout adjustments depending on whether or not the user is logged in. For example, the user will not see "edit" icon for their posts if they are not logged in, nor they will have a "draw" icon in their header. 
* The editing page will have pop-up if the user clicks "delete the drawing," asking the user if they are sure they want to remove their drawing from our website. 
* Likewise, the user will have a popup for "submit" button on the drawing page. 
* The search page will appear once user types the tag they are looking for in the search bar. 


## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

* Library or service name: description of use
* [p5.js](https://p5js.org): Used to implement the drawing of pictures.
* [Flat jQuery Tags](https://github.com/betaWeb/inputTags-jQuery-plugin): Used for autocompleting and validating tags. Also for giving a traditional tags experience.  

**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here:**

 * Small snippets of code were used throughout the project for bug fixes and/or feature implementations. All of the code snippets taken have a comment with a link to the source.  
