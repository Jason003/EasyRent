# Easy Renter

EasyRenter is a house renting platform which provides services including inquiry sending, lease signing, multi-conditional search and comments.

## Basic Infomation
### Group Member
```
Jiefan Li   <jl5501>
Yuyao Zhong <yz3618>
```
### PostgreSql account
```
JL5501
```
### URL of Web Application

[http://34.74.195.72:8111/](http://34.74.195.72:8111/) 

## Description

The website includes all the functions mentioned in the part 1, with 7 entities and database set up in the part 2.

### Users
Users can create an account by clicking the "Register" button on the top right at the home page. A user needs to fill in the infomation of Username, Email and Password. After registering, users can log in by clicking the "Login" button on the top right of the page, where username and password are required. If password does match, the users can not login. After log in, a user can check his or her basic infomation on the personal web page, which can be entered by clicking the username displayed on the top right at the home page.

### Apartments
The infomation of the apartments is listed on the home page, with clear titles show the addresses of the apartments. By clicking each titles, the detailed infomation of the apartments will be displayed, including price, the number of bedrroms and bathrooms, description, and the responsible brokers. The comments on the apartment are also shown on the page.

### Comments
Users can post comments in the web page of an apartment by click the "Post Comment" button next to the title of "Comments". Before posting a comment, users must log in first. If a user does not log in but press the "Post Comment", the webpage will be redirected to the Log-In page.

### Brokers

On an apartment list, the name of the broker who is responsible for the apartment will be displayed.

### Inquiries
On each apartment list, users can send inquiries to the responsible broker by clicking the "Inquire" button next to the name of the broker. On the Inquiry page, users need to fill in the message, and click "Send" button to send the message. After sending the inquiry, users can get their history records of sent inquiries in their personal webpages.

### Lease Signing
Users can choose to sign a lease on an apartment by clicking the "Sign Lease" button on the page of the apartement. Users need to choose the start date and end date for their leases. After signing a lease, the history records of signed leases can also be quiried on the personal webpages.

### Student
A user can verify to be a student on his or her personal web page by clicking "Student Verification" next to the user name. After entering the university and student ID, the account will be come a student account. After verification, the user will be redirected to the personal webpage with notice of "Successfully Verified", and the user will also be marked as "Student" next to the user name.

## Interesting Operations
### Multi-conditional Search
At the home page, users can query by key words and location, the boundary of the price, and the numbers of bedrooms and bathrooms, which can help users decrease the range to search ideal apartments. Users do not need to fill all the blanks but instead only choose the conditions they want to add. The conditions that are not empty will be stored to the corresponding variables, then combining together to form a SQL query which includes all the conditions through string concatenation. The result of the query will be sent back and displayed on the webpage, with a list of apartments that satisfy the conditions, or empty if no apartments meet the needs.

For example, by inputing following infomation:
```
Key Word & Location: 362
Less than: $10000
```
where leaves the conditions of bedrooms and bathrooms empty, the page will then display a list with an apartment that meets the condition:
```
362 W 119th St APT 2, New York, NY 10026
```
Users can then click the title to know more details about the apartments.
It is an interesting part because it is useful in practice, which enables users to narrow down their search. It also makes SQL queries flexible, since we do not need to fill all the blank to send a query.

### The apartment webpages
The apartment webpages are used to display the detailed information, descriptions, the related brokers and the comments. To get the comprehensive components, we need to make queries among not only the apartment table, but also the broker and user tables, with apartment id as the input. 

The users can input data to the database through inquiries and comments. When users make inquiries, we also need to insert the records of inquiries to the inquiry table in the database. To post comments, firstly it will be checked whether a user has logged in, or he or she will be directed to the log-in page. Then a user will be directed to the comment page which allows them to enter comments after clicking the button. After posting, users will be redirected to the previous apartment webpage and see their comments.
For example, for the apartment of "963 Amsterdam Ave APT 6, New York, NY 10025" and a virtual user with name as "test11", before posting comments, the comment part will shows:
```
2r1rcgd (2019-05-07 02:01:00) : The location is amazing!

8g46he (2019-03-21 15:48:00) : Very good location!
```
After the user post a comment with content *"Comment just for showing an example"*, the comment part of the apartment will become:
```
test11 (2019-11-07 20:43:48) : Comment just for showing an example

2r1rcgd (2019-05-07 02:01:00) : The location is amazing!

8g46he (2019-03-21 15:48:00) : Very good location!
```
which displays the latest comment on the first row.

It is also an interesting part, because it includes comprehensive SQL queries that are related to several entities including apartments, users, brokers and comments. Users can also make insertion to the databases by sending inquiries and comments and to see their comments as soon as they make a post.


