# Ignite-iMed
Project iMed: A full-stack web application that allows users to quickly diagnose their conditions by putting in their symptoms. 
## How we created it
Deployed and designed the frontend server with React and Node.js, and the backend server with Flask and Python.
## How does the app figure out what to diagnose?
When the user inputs a phrase, such as "I have a runny nose and sore throat", the app distinguishes what symptoms are present in the input. To do this we took an online dataset that included 133 different symptoms and 42 unique conditions. By implementing OpenAI's GPT 3.5-turbo API, our web app extracts what symptoms are present based on the user's input. With the dataset, we trained a Random Forest Classifier (RFC) to be able to predict the given features of the symptoms that the user types. The API implementation allows the data to be sent to the RFC and then predicts the condition the patient has. Finally, this information gets sent back to the Frontend and is then displayed for the user to see.
