from LCConnect import LCConnect
from db_class import Db_class
import pandas as pd
from Note_class import Note


# For every client in client list this script will erase all the lines from the all_notes table per specific client
# and place the notes again with the updated data

class db_refresh(object):
	"""refresh the db for all users with one gen_attr
		params: account_api_key (str)
				account_investor_id (str)
				db_url (str)
				gen_attr {'clientId' : int, 'clientName' : str}"""


	def __init__(self, account_api_key, account_investor_id, db_url, gen_attr):
		account_creds = {'api_key' : account_api_key,
						 'investor_id' : account_investor_id}
		client_ids_list = [1234]

		# Get the updated notes data from LC for all users
		lc = LCConnect(api_key=account_creds['api_key'], investor_id=account_creds['investor_id'])
		notes = lc.get_user_data('detailednotes')['myNotes']
		df = pd.DataFrame(notes)
		notes = []
		for i in xrange(len(df)):
		    # Need to implement that for portfolio, retrieve the gen_attr and insert accordingly
		    notes.append(Note(note=dict(df.ix[i]), gen_attr=gen_attr))

		db_url = db_url
		db = Db_class(url=db_url)

		# drop all rows - need to think if this is the right way to do it
		db.delete_rows(table_name='all_notes', condition="all_notes.clientId = {}".format(gen_attr['clientId']))

		# Write to table again
		for note in notes:
		    db.write_to_table(table_name='all_notes', columns_names=note.string_columns_names, values=note.string_values)


