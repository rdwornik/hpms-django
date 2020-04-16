import random 

methods = {
    "GET" : ("G","008000"),
    "POST" : ("P","0000FF"),
    "HEAD" : ("H", "FFFF00")
}

def get_or_create_methods_tag(request_method):
    if request_method not in methods:
        i = 0
        tag = request_method[i]
        color = "%06x" % random.randint(0, 0xFFFFFF)
        tags = [tag[0] for tag in methods.values()]
        colors = [color[1] for color in methods.values()]
        while request_method[i] in tags:
            i += 1
            tag += request_method[i]
        while color in colors:
            color = "%06x" % random.randint(0, 0xFFFFFF)
        methods[request_method] = (tag, color)
    return methods[request_method]
    