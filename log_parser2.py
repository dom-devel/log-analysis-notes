def parse_logs(line):
    regex = re.compile(regex_string)
    
    r = regex.search(line)
    result_set = {}
    if r:
        for k, v in r.groupdict().iteritems():
            #create dictionary entry for everything even if 
            #regex fails to find anything
            if v is None or v is "-":
                result_set[k] = ''
            if k == "request":
                #all strings need to en enclosed by quotes
                result_set["request"] = '"'+r.groupdict().pop(k)+'"'
                #we need to work with path so here don't add quotes
                if "?" in v:
                    request = v.partition("?")
                    path = request[0]
                    query = request[2]
                    result_set["query"] = '"'+query+'"'
                    result_set["has_params"] = 'yes'
                    # Store a 1 or a 0 for each known parameter
                    #for param in params:
                    #    result_set[param] = param in query
                    r.groupdict().pop(k)
                else:
                    result_set["has_params"] = 'no'
                    path = r.groupdict().pop(k)
                    result_set["query"] = ''
                result_set["path"] = '"'+path+'"'
                #page path must be pulled from path in case it has requests
                path_lstrip_slash = path.lstrip('/')
                split_path = path_lstrip_slash.split('/', 4)
                #4 page path levels must always exist
                counter = 1
                while counter < 5:
                    try: 
                        result_set["page_path_"+str(counter)] = '"'+split_path[counter-1]+'"'
                        counter += 1
                    except:
                        result_set["page_path_"+str(counter)] = ''
                        counter += 1
                        continue

            #all text strings must be wrapped in quotes to avoid
            #breaking
            elif k == "user_agent":
                result_set["user_agent"] = '"'+r.groupdict().pop(k)+'"'
            elif k == "referrer":
                result_set["referrer"] = '"'+r.groupdict().pop(k)+'"'
            else:
                result_set[k] = r.groupdict().pop(k)
        #this is currently a fake full URL it doesn't
        #use a real HTTP and host because this log file doesn't
        #have it 
        #this is for the match URL
        result_set["full_url"] = '"https://www.icanvas.com'+result_set["request"][1:-1]+'"'
    return result_set
