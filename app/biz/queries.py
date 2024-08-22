# query statements
from typing import final

QUERY_STR =  {
    "test": {
        "select" : "select * from wt_test where CA='%s'",
        "select_all" : "select * from wt_test",
        "select_error" : "select * error from wt_test"
        
    }
}