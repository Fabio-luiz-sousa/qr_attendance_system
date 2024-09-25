from functions import *

def settings():
    '''Function that configure the tab after the authorized access'''
    st.tabs(['Settings'])
    options = st.radio('Options',['Search','Insert','Delete','Log'])
    match options:
        case 'Search':
            option_search()
        case 'Insert':
            option_insert()
        case 'Delete':
            option_delete()
        case 'Log':
            option_log()


home()
check_access()

if st.session_state['verification_done'] and st.session_state['access_granted']:
    st.success('Credentials Accepted!!')
    settings()
else:
    st.error('Invalid Credentials!!!')
    
    







