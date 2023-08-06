from __future__ import division

# Email Extraction Params
inbox_max_items = 500               # Max number of mails to extract from inbox folder
sentitems_max_items = 1000
subfolder_max_items = 1000
customfolder_max_items = 1000
total_max_items = 20000

# Email Structure Params
big_folder_abs_size = 50            # The least absolute size for a folder to be clf as big
big_folder_rel_fraction = 1/3       # The least rel fraction to avg folder size for the same
frequent_filer_folder_len = 10      # The least avg folder length for user to be clf as freq filer
