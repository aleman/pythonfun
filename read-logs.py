import statistics

def canonical(url):
    url_parts = url.split("/")
    index = 0
    changed = False
    for part in url_parts:
        if part.isdigit():
            url_parts[index] = '{id}'
            changed = True
        index += 1
    if changed:
        return '/'.join(url_parts)
    return url


with open('sample.log') as f:
    items = {}
    for line in f:
        parts = line.split(" ")
        method = parts[3].split("=")[1]
        path = parts[4].split("=")[1]
        d = parts[7].split("=")[1]
        connect = parts[8].split("=")[1][0:-2]
        service = parts[9].split("=")[1][0:-2]
        r_time = int(connect) + int(service)
        req_identifier = method + ' ' + path
        req_identifier = canonical(req_identifier)
        item = {"called": 1, "req_identifier": req_identifier, "r_times": [], "ds" : []}
        if req_identifier in items:
            item = items[req_identifier]
            item["called"] = item["called"] + 1
            item["r_times"].append(r_time)
            item["ds"].append(d)
        else:
            item["r_times"].append(r_time)
            item["ds"].append(d)
            items[req_identifier] = item
    for k in items:
        item = items[k]
        item["d"] = statistics.mode(item['ds'])
        del item["ds"]
        item["r_time_mean"] = statistics.mean(item["r_times"])
        item["r_time_mode"] = statistics.mode(item["r_times"])
        item["r_time_median"] = statistics.median(item["r_times"])
        del item["r_times"]
        print(f"{item}")

