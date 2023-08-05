import prepare_geojson_to_agentpolisdemo

f = open("/home/martin/MOBILITY/GITHUB/agentpolis-demo/python_scripts/data/output-result.geojson","r")
nodes = open("/home/martin/MOBILITY/GITHUB/agentpolis-demo/python_scripts/data/nodes.geojson","w")
edges = open("/home/martin/MOBILITY/GITHUB/agentpolis-demo/python_scripts/data/edges.geojson","w")

geojson_file = prepare_geojson_to_agentpolisdemo.load_geojson(f)
data = prepare_geojson_to_agentpolisdemo.get_nodes_and_edges_for_agentpolisdemo(geojson_file)
print data[0]['features'][0]
prepare_geojson_to_agentpolisdemo.save_geojson(data[0],edges)
print "\n"
print data[1]['features'][0]
prepare_geojson_to_agentpolisdemo.save_geojson(data[1],nodes)