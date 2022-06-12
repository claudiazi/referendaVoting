import os

from apps import overview, search  # import your app modules here
from multiapp import MultiApp
from utils.data_preparation import load_data, preprocessing

mongodb_url = os.getenv("MONGODB_URL")
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")
votes_df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
votes_df = preprocessing(votes_df)

app = MultiApp(df=votes_df)

# Add all your application here
app.add_app("Overview", "kanban", overview.app)
app.add_app("Stalk a specific account", "eyeglasses", search.app)

# The main app
app.run()
