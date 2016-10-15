def parse_logs(line):
    #regex_string should be a regex string which will extract each variable as a named entity
    #note that the following variables are named in the code below:
    #user agent is extracted to user_agent
    #the path is extracted to path e.g. /category/product 
    #the query string is extracted to query
    #the referer is extracted to referer

    regex = re.compile(regex_string)

    parsed_log_line = regex.search(line)
    result_set = {}

    if parsed_log_line:
        for key, value in parsed_log_line.groupdict().iteritems():
            #create dictionary entry for everything even if 
            #regex fails to find anything
            if value is None or value is "-":
                result_set[key] = ''
            if key == "request":
                #all strings need to be enclosed by quotes for export as CSV
                result_set["request"] = '"'+parsed_log_line.groupdict().pop(key)+'"'
                if "?" in value:
                    request = value.partition("?")
                    path = request[0]
                    query = request[2]
                    result_set["query"] = '"'+query+'"'
                    result_set["has_params"] = 'yes'
                    #TODO: Possible enhancement - store a param for each known param
                    parsed_log_line.groupdict().pop(key)
                else:
                    result_set["has_params"] = 'no'
                    path = parsed_log_line.groupdict().pop(key)
                    result_set["query"] = ''
                result_set["path"] = '"'+path+'"'

                #generate page path levels
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

            #all text strings must be wrapped in quotes to export as CSV
            elif key == "user_agent":
                result_set["user_agent"] = '"'+parsed_log_line.groupdict().pop(key)+'"'
            elif key == "referer":
                result_set["referer"] = '"'+parsed_log_line.groupdict().pop(key)+'"'
            else:
                result_set[key] = parsed_log_line.groupdict().pop(key)
        #full_url_host_protocol should be the protocol and hostname for the website. 
        #for example: http://www.example.com
        #TODO: pull this automatically from log files if hostname and scheme or port exist
        result_set["full_url"] = '"'full_url_host_protocol+result_set["request"][1:-1]+'"'
    return result_set
