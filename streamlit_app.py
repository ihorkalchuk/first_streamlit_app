import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

#streamlit.stop()

def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized


streamlit.title('My Mom"s New Helthy Diner')
streamlit.header('🥣🍞 Breakfast Menu', divider='rainbow')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥑 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
   
streamlit.header('🍌🥭 Fruityvice Menu! 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)




streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
   streamlit.error()







#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)


streamlit.header("The fruit load list containes")
#Snowflake related functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * FROM fruit_load_list")
            return my_cur.fetchall()

#Add a button to load the list
if streamlit.button("Get Fruit Load List"):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      streamlit.dataframe(my_data_rows)    

     


#my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchall()
#streamlit.text("The fruit load list containes:")
#streamlit.dataframe(my_data_row)


#fruit_choice = streamlit.text_input('What fruit would you like to add?')



#my_cur.execute("insert into FRUIT_LOAD_LIST values (" + fruit_choice + ")")


# Allow the user add Fruit to Snowflake:
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into FRUIT_LOAD_LIST values ('" + new_fruit + "')")
            return "Thanks for adding " + new_fruit
      


#Add a button to add a fruit
try:
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      fruit_choice = streamlit.text_input('What fruit would you like to add?')
      if not fruit_choice:
            streamlit.error("Please select a fruit to add")
      else:
            insert_row_snowflake(fruit_choice)
      
except URLError as e:
   streamlit.error()

   

