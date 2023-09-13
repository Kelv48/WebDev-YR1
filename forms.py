from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, EqualTo, NumberRange

class SearchForm(FlaskForm):
    search = StringField("Search:", validators=[InputRequired()])
    submit = SubmitField("submit")

class RegistrationForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    password2 = PasswordField("Repeat password:",
        validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    submit = SubmitField("Login")

class Emp_ManagementForm(FlaskForm):
    job_description = StringField("Enter their new job description",
                                  validators=[InputRequired()])
    department = StringField("Please enter the new department they will be working in",
                             validators=[InputRequired()])
    submit = SubmitField("Update")

class Product_ManagementForm(FlaskForm):
    description = StringField("Enter the new description",
                              validators=[InputRequired()])
    price = StringField("Enter the new price for the product/service",
                        validators=[InputRequired()])
    submit = SubmitField("Update")

class New_ProductForm(FlaskForm):
    price = IntegerField("Please enter the price of the new product",
                         validators=[InputRequired()])
    description = StringField("Please enter a description of the new product",
                              validators=[InputRequired()])
    stock = IntegerField("Please enter a starting stock for the new product",
                         validators=[InputRequired()])
    name = StringField("Enter the name of the new product",
                       validators=[InputRequired()])
    submit = SubmitField("Confirm")

class New_ServiceForm(FlaskForm):
    price = IntegerField("Please enter the price of the new service",
                         validators=[InputRequired()])
    description = StringField("Please enter a description of the new service",
                              validators=[InputRequired()])
    name = StringField("Enter the name of the new service",
                       validators=[InputRequired()])
    submit = SubmitField("Confirm")

class New_EmployeeForm(FlaskForm):
    name = StringField("Enter the name of the new employee",
                       validators=[InputRequired()])
    age = IntegerField("Enter the age of the new employee",
                       validators=[InputRequired()])
    department = StringField("Enter in the department they will be working in",
                             validators=[InputRequired()])
    job_description = StringField("Enter in their job description",
                                  validators=[InputRequired()])
    submit = SubmitField("Confirm")

class AccountForm(FlaskForm):
    new_user_id = StringField("Enter your new user_id",
                              validators=[InputRequired()])
    submit = SubmitField("Confirm")

class ResearchForm(FlaskForm):
    project_name = StringField("Enter the project name",
                            validators=[InputRequired()])
    started = StringField("Enter the starting date in yr/month/day format",
                            validators=[InputRequired()])
    description = StringField("Enter a product description",
                            validators=[InputRequired()])
    submit = SubmitField("Confirm")

class ReviewForm(FlaskForm):
    review = StringField("Your Review", 
                         validators=[InputRequired()])
    score = IntegerField("Your rating",
                         validators=[InputRequired(), NumberRange(1, 5)])
    submit = SubmitField("Confirm your review")

class SupportForm(FlaskForm):
    support = StringField("Please Describe your issue", validators=[InputRequired()])
    submit = SubmitField("Submit Ticket")

class BlogForm(FlaskForm):
    post = StringField("Whats on your mind", validators=[InputRequired()])
    submit = SubmitField("Post")

class ProfileForm(FlaskForm):
    nickname = StringField("Enter your nickname: doesn't have to be your user_id")
    age = IntegerField("Please enter your age")
    bio = StringField("Please describe yourself")
    submit = SubmitField("Confirm")




