import streamlit as st
from connect import create_snowflake_connection

# Function for checking if email, phone number, or name combination already exists
def is_unique(email, phone_number, first_name, last_name):
    conn = create_snowflake_connection()
    cur = conn.cursor()

    try:
        # Check for existing email
        cur.execute(f"SELECT COUNT(*) FROM students WHERE email = '{email}'")
        email_count = cur.fetchone()[0]

        # Check for existing phone number
        cur.execute(f"SELECT COUNT(*) FROM students WHERE phone_number = '{phone_number}'")
        phone_count = cur.fetchone()[0]

        # Check for existing first name + last name combination
        cur.execute(f"SELECT COUNT(*) FROM students WHERE first_name = '{first_name}' AND last_name = '{last_name}'")
        name_combination_count = cur.fetchone()[0]

        # Return True if all checks are unique (i.e., no duplicates found)
        if email_count == 0 and phone_count == 0 and name_combination_count == 0:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error checking uniqueness: {str(e)}")
        return False
    finally:
        cur.close()
        conn.close()

# Function for the sign-up form
def show_register_form():
    st.title("Sign Up")

    first_name = st.text_input("First Name", key="register_first_name")
    last_name = st.text_input("Last Name", key="register_last_name")
    email = st.text_input("Email", key="register_email")
    phone_number = st.text_input("Phone Number", key="register_phone_number")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
    
    # Dropdown for role selection
    role = st.selectbox("Select Role", ["1-student", "2-teacher"], key="register_role")

    if st.button("Register", key="register_button"):
        if password == confirm_password:
            # Check if email, phone, and name combination are unique
            if is_unique(email, phone_number, first_name, last_name):
                conn = create_snowflake_connection()
                cur = conn.cursor()

                try:
                    # Insert the role into the database
                    cur.execute(f"""
                        INSERT INTO students (first_name, last_name, email, phone_number, password, role)
                        VALUES ('{first_name}', '{last_name}', '{email}', '{phone_number}', '{password}', '{role}');
                    """)
                    st.success("Registration successful!")
                    # Set session state with role
                    st.session_state.logged_in = True
                    st.session_state.first_name = first_name
                    st.session_state.last_name = last_name
                    st.session_state.role = role
                    show_home_page(first_name, last_name, role)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    cur.close()
                    conn.close()
            else:
                st.error("Email, phone number, or name combination already exists.")
        else:
            st.error("Passwords do not match!")

# Function for the login form
def show_login_form():
    st.title("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        conn = create_snowflake_connection()
        cur = conn.cursor()

        try:
            # Fetch the user information, including the role
            cur.execute(f"""
                SELECT first_name, last_name, role FROM students WHERE email = '{email}' AND password = '{password}';
            """)
            user = cur.fetchone()

            if user:
                st.success(f"Welcome, {user[0]} {user[1]}!")
                # Store user details and role in session state
                st.session_state.logged_in = True
                st.session_state.first_name = user[0]
                st.session_state.last_name = user[1]
                st.session_state.role = user[2]
                show_home_page(user[0], user[1], user[2])
            else:
                st.error("Invalid email or password!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            cur.close()
            conn.close()

# Function to show the home page after registration or login
def show_home_page(first_name, last_name, role):
    if role == "2-teacher":
        # If the user is a teacher, greet them as with their last name
        st.title(f"Welcome, Professor {last_name}!")
    else:
        # If the user is a student, greet them with their full name
        st.title(f"Welcome, {first_name} {last_name}!")

# Main function to handle navigation based on user input
def index():
    st.title("Intelevaluation")

    # Initialize session state for logged_in if not already set
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    #  show the home page if user is logged in
    if st.session_state.logged_in:
        show_home_page(st.session_state.first_name, st.session_state.last_name, st.session_state.role)
    else:
        # Show the register or login form based on the user interaction
        if st.button("Register", key="index_register_button"):
            st.session_state.show_form = "register"
        elif st.button("Login", key="index_login_button"):
            st.session_state.show_form = "login"

        # Check if the user has selected to show a form and display it
        if "show_form" in st.session_state:
            if st.session_state.show_form == "register":
                show_register_form()
            elif st.session_state.show_form == "login":
                show_login_form()

# running the main function
if __name__ == "__main__":
    index()
