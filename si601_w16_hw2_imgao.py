import re
import urlparse
import csv
import operator

with open('access_log.txt', 'rU') as file_input:
    # input_list = []

    def is_valid(line):
        #this line actually isn't necessary, because I added the (GET|POST|HEAD) regex to the next line in order to prevent
        #this line: 66.46.181.116 - - [09/Mar/2004:22:40:07 -0500] "GET / HTTP/1.0" 200 4301 "http://Network-Tools.com" "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; AspTear 1.5)"
        #from being valid. What it was doing before adding the regex to line 16, was it was ignoring the invalid HTTP/1.0, and instead
        #matching with the http://Network-Tools.com and passing the condition test, therefore returning a valid log result
        if re.search(r'(GET|POST|HEAD)', line):
            #extract the url using regex in order to pass into urlparse function from urlparse module
            match = re.search(r'(GET|POST|HEAD)\s(http://|https://)[^"]*', line, flags=re.IGNORECASE)
            # match_invalid_url = re.search(r'HTTP/1.0', line)
            # if match_invalid_url:
            #     return False
            if match:

                url = match.group()
                #parse the url and pull out the query string
                query = urlparse.urlparse(url).query
                #separate out each query within the string, this is stored in each_query dict via urlparse.parse_qs built-in urlparse function
                each_query = urlparse.parse_qs(query)
                # print each_query
                for key, value in each_query.iteritems():
                    # if a single query is greater than 80 characters, it's not valid
                    if len(str(value)) >= 80:
                        #invalid
                        return False
                #extract the status codes using regex, will look something like: " 200
                status_code_match = re.search(r'"\s[0-9]{3}', line)
                status_code_match = status_code_match.group()
                #remove the double quote "
                status_code_temp = status_code_match.replace("\"", "")
                #remove the extra space
                status_code = status_code_temp.strip()
                if status_code.startswith('2') or status_code.startswith('3') or status_code.startswith('5'):
                    return True
        if re.search(r'CONNECT', line):
            status_code_match = re.search(r'"\s[0-9]{3}', line)
            status_code_match = status_code_match.group()
            #remove the double quote "
            status_code_temp = status_code_match.replace("\"", "")
            #remove the extra space
            status_code = status_code_temp.strip()
            if status_code.startswith('2') or status_code.startswith('3') or status_code.startswith('5'):
                return True

    def extract_ip(line):
        match = re.search(r'[0-9 .][^\s]+', line)
        print match.group()
        return match.group()


    output_valid = open('valid_access_log_imgao.txt', 'w')
    output_invalid = open('invalid_access_log_imgao.txt', 'w')
    count = 0
    suspicious_dict = {}
    suspicious_print= ()
    for line in file_input:
        if is_valid(line) is True:
            output_valid.write(line)
        else:
            output_invalid.write(line)
            ip_address = extract_ip(line)
            if ip_address in suspicious_dict:
                # print 'yes, already in dict'
                attempts = suspicious_dict[ip_address] + 1
                suspicious_dict[ip_address] = attempts
            else:
                # print 'no, not in dict'
                count = 1
                suspicious_dict[ip_address] = count

suspicious_print = sorted(suspicious_dict.items(), key=operator.itemgetter(1), reverse=True)
header = ['IP Address', 'Attempts']
with open('suspicious_ip_summary_imgao.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
    writer.writerows(suspicious_print)
