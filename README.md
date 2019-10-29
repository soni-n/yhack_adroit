# Adroit (Server)
Adroit is an easy-to-use reputation and sentiment analysis tool. Enter a search term and see what complaints people have about it, and get a summary of the most frequent commentary!

Check it out [here](https://yhack-adroit.firebaseapp.com/)!

Adroit pulls data from Twitter about a certain target (e.g., "JetBlue") and uses Google's natural language API to find negative-sentiment content, indicating potential user complaints. After doing so, Adroit extracts high-importance terms from the data to indicate the general themes of those complaints. This is the server side of Adroit, which handles incoming requests for analysis. The client side can be found [here](https://github.com/paul-rinaldi/yhack2019-adroit-2).
