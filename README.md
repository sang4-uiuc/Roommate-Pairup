# Roommate-Pairup
410 project

1. This is a roommate pairing application. 
Users sign up and take a survey, in which the app asks them a 
variety of questions that relate to different parts of their personalities. 
That information is stored in the database and it provides a variety of functions to make that data useful to them and other users.

2. Provides functionality for login, logout, register and updating profile.

Provides functionality for leaving feedback about success

Allows users to search for roommates based on the similarity of their responses to set of personality questions

Provides the ability to search for a roommate based on their exact answers to a selected set of questions chosen by the user

Provides functionality for user to take a survey for best matches

Provides functionality for user to update their survey to get different matches.

3. The user will first register onto the website by filling out their profile information. This includes their netid, email, name, and the other attributes associated in the Students table of the database. Once the form is submitted, the user and their data  will be inserted into the Students table if their netid has not been inserted into the table already.

After the user registers, they will be able to take the questionnaire survey that will be used to find the best suitable roommate. There are four questions per category and four categories, which are Social, Interests, Habits, and Misc. Each category has a table associated with it in the database. The user can also decide which of the four categories are important to them so that only those categories are used to find roommates. Each question in the survey has four possible responses. Once the survey is submitted, a number from 1 to 4 is inserted into each of the corresponding tables in the database based on their answer to the multiple choice question. If the user marked a category as important that would be saved as 1 in the checked attribute for each table in the database and 0 otherwise.

The user will then be able click on to view matches to see the top 4 choices for potential roommates. A query is generated based on the checked categories and survey answers of the current logged in user.

The user can also search for a roommate on specific questions by clicking on the search for roommate button on the home page. A query is generated only using the specified questions and looks for exact matches. The profile information of the matched users is displayed when the form is submitted.

At the top of the website the user can leave feedback. The user fills in a form with their netid, their roommates, and a score of 1 through 10. Once this is submitted the score will be inserted into the success attribute of the RoommatePairs table. This score will be used to continue to train the linear model.
