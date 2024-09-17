



class VRPProblem:

    def __init__(self, sources, costs, capacities, dests, weights,
             time_intervals, services, node_coords, first_source=True, last_source=True):
    # Merging all sources into one source.
        source = 0
        weights[source] = 0
        self.source = source
        in_nearest_sources = dict()
        out_nearest_sources = dict()

        # Finding nearest source for all destinations.
        for dest in dests:
            in_nearest = sources[0]
            out_nearest = sources[0]
            for s in sources:
                costs[source][s] = 0
                costs[s][source] = 0
                if costs[s][dest] < costs[in_nearest][dest]:
                    in_nearest = s
                if costs[dest][s] < costs[dest][out_nearest]:
                    out_nearest = s
            costs[source][dest] = costs[in_nearest][dest]
            costs[dest][source] = costs[dest][out_nearest]
            in_nearest_sources[dest] = in_nearest
            out_nearest_sources[dest] = out_nearest

        # Set attributes outside the loop
        self.sources = sources
        self.costs = costs
        self.capacities = capacities
        self.dests = dests
        self.weights = weights
        self.time_intervals = time_intervals
        self.services = services
        self.first_source = first_source
        self.last_source = last_source
        self.in_nearest_sources = in_nearest_sources
        self.out_nearest_sources = out_nearest_sources
        self.node_coords = node_coords


   