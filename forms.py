from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import data_required, length, email, equal_to, ValidationError
from connection import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class User_Registration(FlaskForm):
    names = StringField('names', validators=[data_required(),
                                             length(min=2,
                                                    max=45
                                                    )
                                             ]
                        )
    username = StringField('username', validators=[data_required(),
                                                   length(min=2,
                                                          max=25)
                                                   ]
                           )
    email = StringField('email', validators=[data_required(),
                                             email()
                                             ]
                        )
    password = PasswordField('password', validators=[data_required()]
                             )
    confirm_password = PasswordField('confirm password', validators=[data_required(),
                                                                     equal_to('password')
                                                                     ]
                                     )
    submit = SubmitField('sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already exist')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already exists in the system', 'warning')


class User_Login(FlaskForm):
    email = StringField('email', validators=[data_required(),
                                             email()
                                             ]
                        )
    password = PasswordField('password', validators=[data_required()]
                             )
    stay_logged = BooleanField()
    submit = SubmitField('login')


class Update_acc_info(FlaskForm):
    names = StringField('names', validators=[data_required(),
                                            length(min=2,
                                                   max=45
                                                   )
                                             ]
                        )
    username = StringField('username', validators=[data_required(),
                                                   length(min=2,
                                                          max=25
                                                          )
                                                   ]
                           )
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username already exist')


class NewPost(FlaskForm):
    title = StringField('Title', validators=[data_required()])
    post = TextAreaField('Content', validators=[data_required()])
    submit = SubmitField('submit')
