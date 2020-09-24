import logging
import brightway2 as bw

def getActivity(activityArrayOrName):
    try:
        lca_act = bw.Database(activityArrayOrName[0]).get(activityArrayOrName[1]) # if written as list [database, activity]
    except:
        try:
            lca_act = bw.Database("own_activities").get(activityArrayOrName[1]) # if written as ['', activity]
        except:
            try:
                lca_act = bw.Database("own_activities").get(activityArrayOrName) # if written as 'activity'
            except:
                logging.exception("message")
    return lca_act