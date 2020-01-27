from yaml import load, Loader

yaml_path = './output.yml'
stream = open(yaml_path, 'r')
yaml_file = load(stream, Loader=Loader)

nodes = {}
keys = yaml_file.keys()

for key in keys:
    if key == 'nodes':
        for node in yaml_file[key]:
            file = open('{}-address'.format(node), 'w')
            nodes[node] = {}
            for node_key in yaml_file[key][node]:
                if node_key == 'host' or node_key == 'ports':
                    nodes[node][node_key] = []
                    nodes[node][node_key] = yaml_file[key][node][node_key]

            output = 'host: {}\nport: {}\n'.format(nodes[node]['host'], nodes[node]['ports']['api'])
            file.write(output)


