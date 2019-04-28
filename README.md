 # Dining Concierge Chatbot

In this project, I developed a serverless web chatbot with event-driven microservices using AWS S3, API Gateway, Lambda, Cognito, SQS, SNS, and Lex. In addition, I also built a recommendation pipeline to suggest restaurants based on user inputs using SageMaker, ElasticSearch, DynamoDB, and Yelp API. This is one of the course project of COMS E6998 Cloud Computing & Big Data at Columbia University. The website can be accessed at: https://s3.amazonaws.com/www.diningchatbot.com/index.html 

### How it works

Based on a conversation with the customer, the chatbot would response and ask for user's information and preference. The chatbot will pick customer’s preferred ‘cuisine' and suggest restautants. The app will search through ElasticSearch to get suggestions of restaurant IDs with this cuisine. At this point, the app would also query the DynamoDB table with these restaurant IDs to find more information about the restaurants you want to suggest to your customers like name and address of the restaurant.

### Example Interaction
User: Hello
Bot: Hi there, how can I help?
User: I need some restaurant suggestions.
Bot: Great. I can help you with that. What city or city area are you looking to dine in?
User: Manhattan
Bot: Got it, Manhattan. What cuisine would you like to try?
User: Japanese
Bot: Ok, how many people are in your party?
User: Two
Bot: A few more to go. What date?
User: Today
Bot: What time?
User: 7 pm, please
Bot: Great. Lastly, I need your email address so I can send you my findings.
User: john.doe@columbia.edu
Bot: You’re all set. Expect my suggestions shortly! Have a good day.
User: Thank you!
Bot: You’re welcome.

(a few minutes later)

User gets the following text message:
“Hello! Here are my Japanese restaurant suggestions for 2 people, for today at 7 pm: 1. Sushi Nakazawa, located at 23 Commerce St, 2. Jin Ramen, located at 3183 Broadway, 3. Nikko, located at 1280 Amsterdam Ave. Enjoy your meal!”

### Built With
* [S3](https://aws.amazon.com/s3/) - Used to host static frontend 
* [API Gateway](https://aws.amazon.com/api-gateway/) - For creating, monitoring, and securing REST APIs at any scale. 
* [Lambda](https://aws.amazon.com/lambda/) - Function as a Service,  event-driven, and serverless computing platform. Acted as backend to run code without provisioning or managing servers.  
* [Cognito](https://aws.amazon.com/cognito/) - User signup and login.
* [SQS](https://aws.amazon.com/sqs/) - Message queue for communication between microservices.
* [SNS](https://aws.amazon.com/sns/) - Send text message to users.
* [Lex](https://aws.amazon.com/lex/) - Amazon platform to build conversational bots.
* [SageMaker](https://aws.amazon.com/sagemaker/) - Train and deploy Machine Learning models.
* [ElasticSearch](https://www.elastic.co/products/elasticsearch) - Search engine to handle unstructured search. 
* [DynamoDB](https://aws.amazon.com/dynamodb/) - NoSQL database.
* [Yelp API](https://www.yelp.com/fusion) - Scratch restaurant information.

### Architecture
![image](https://drive.google.com/uc?export=view&id=1zvnxnkfvf--xbBWSPIepTWAxvG4JgkL7)
