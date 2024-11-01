import streamlit as st

# Set the title of the app
st.title('Contact Us')

# Create a form for user input
with st.form(key='contact_form'):
    # User input fields
    name = st.text_input('Your Name:')
    email = st.text_input('Your Email:')
    message = st.text_area('Your Message:')
    
    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# When the user submits the form
if submit_button:
    # Display a thank you message
    st.success(f'Thank you, {name}! Your message has been submitted.')
    st.write(f'Email: {email}')
    st.write(f'Message: {message}')