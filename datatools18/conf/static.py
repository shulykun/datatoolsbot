import os
# '/home/admin/web/algame9-vps.roborumba.com/public_html'

basedir = os.path.abspath(os.path.dirname(__file__))


my_folder = 'datatools18'

## web
path_to_files = '{}/{}/storage/dict'.format(os.path.abspath(''), my_folder)
path_to_storage= '{}/{}/storage/content'.format(os.path.abspath(''), my_folder)

# ## local
# path_to_files = '{}/storage/dict'.format(os.path.abspath(''))
# path_to_storage= '{}/storage/content'.format(os.path.abspath(''))
