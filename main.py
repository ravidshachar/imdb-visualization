from imdb_visualization import neo4j_wrapper

if __name__ == "__main__":
    #neo4j_wrapper.insert_from_imdb()
    #print(neo4j_wrapper.get_nodes_by_years(2010, 2015))
    #print(neo4j_wrapper.get_top_actors())
    print(neo4j_wrapper.get_top_actors())
    print(neo4j_wrapper.get_top_directors())