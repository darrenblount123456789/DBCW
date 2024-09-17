from vrp_problem import VRPProblem
from vrp_solution import VRPSolution

import numpy as np

# Abstract class for VRP solvers.
class VRPSolver:
    # Attributes : VRPProblem
    def __init__(self, problem):
        self.problem = problem

   



    



class ClarkWright(VRPSolver):
    def __init__(self, problem):
        self.problem = problem
    
    
    def which_route(self, link, routes):
        node_sel = []
        i_route = [-1, -1]
        count_in = 0

        for i, route in enumerate(routes):
            route_set = set(route)
            for node in link:
                if node in route_set:
                    i_route[count_in] = i
                    node_sel.append(node)
                    count_in += 1

        overlap = 1 if i_route[0] == i_route[1] else 0

        return node_sel, count_in, i_route, overlap

    def merge(self, route0, route1, link):
        # Avoid reversing multiple times unnecessarily
        if route0[-1] != link[0]:
            route0.reverse()
        
        if route1[0] != link[1]:
            route1.reverse()

        return route0 + route1


    def interior(self, node, route):
        try:
            i = route.index(node)
            return 0 < i < len(route) - 1
        except ValueError:
            return False
        
    # sum up to obtain the total passengers belonging to a route
    def sum_cap(self, route):
        sum_cap = 0
        for node in route:
            sum_cap += self.problem.weights[node]
        return sum_cap
    

    def calculate_sorted_savings(self):
        costs = self.problem.costs
        num_customers = len(costs) - 1  # Number of customers (excluding depot)
        sorted_savings = []
        for i in range(1, num_customers + 1):  # Exclude depot (node 0)
            for j in range(i + 1, num_customers + 1):
                saving = costs[0][i] + costs[0][j] - costs[i][j]
                saving = round(saving, 1)
                sorted_savings.append((i, j, saving))
        sorted_savings.sort(key=lambda x: x[2], reverse=True)  # Sort by savings in descending order
        return sorted_savings

    
    def sum_demands(self, route):
        weights = self.problem.weights
        weightsTotal = 0
        for node in route:
            weightsTotal += weights[node]
        return weightsTotal

    def is_capacity_violated(self, route, extra_demand):
        total_demand = self.sum_demands(route) + extra_demand
        return total_demand > self.problem.capacities[0]


    
    def check_constraints(self, route, destToBeAdded, capacity_of_route):
        return not self.is_capacity_violated(route, self.problem.weights[destToBeAdded])

    def canMerge(self, route1, route2, capacity_of_route):
        return not self.is_capacity_violated(route1, self.sum_demands(route2))
    



    def check_constraintsTime(self, route, destToBeAdded, capacity_of_route):
        return not self.is_capacity_violated(route, self.problem.weights[destToBeAdded])

    def canMergeTime(self, route1, route2, capacity_of_route):
        return not self.is_capacity_violated(route1, self.sum_demands(route2))

    
    def is_time_violated(self, route):
        currentTime = 0
        problem = self.problem
        time_intervals = problem.time_intervals
        services = problem.services
        costs = problem.costs

        for i in range(len(route) - 1):
            node = route[i]
            next_node = route[i + 1]

            # Get time window for current node
            ready_time, due_date = time_intervals[str(node)]
            
            # Check if the current time falls within the time window
            if ready_time <= currentTime <= due_date:
                # Add service time and travel time to the next node
                currentTime += services[0] + costs[node][next_node]
            else:
                return False  # Time window constraint violated

        # Final check for the last node (depot return)
        depot_time_window = time_intervals['0']
        if depot_time_window[0] <= currentTime <= depot_time_window[1]:
            return True

        return False  # Depot return violated




    
    
    # def create_vrp_problem(problem, route1, route2):
    #     capacity = 
    #     numOfVehicles = int(parsed_data["vehicleNumber"])
    #     demands = parsed_data["demands"]
    #     time_intervals = parsed_data["time_interval"]
    #     weights = list(demands.values())
    #     weights = np.array((weights), dtype=int)
    #     capacities = [capacity] * numOfVehicles
    #     service = int(parsed_data["service"])   
    #     services = [service]
    #     dests = list(demands.keys())
    #     dests = [int(dest) for dest in dests]
    #     sources = [int(dests.pop(0))]
    #     node_coords = parsed_data["node_coords"] 



    #     costs = np.zeros((num_nodes, num_nodes), dtype=float)

    #     node_list = list(g.nodes)
    #     for i, node1 in enumerate(node_list):
    #         for j, node2 in enumerate(node_list):
    #             if node1 != node2:
    #                 dist = math.sqrt((g.nodes[node1]["pos"][0] - g.nodes[node2]["pos"][0])**2 +
    #                                 (g.nodes[node1]["pos"][1] - g.nodes[node2]["pos"][1])**2)
    #                 costs[i][j] = dist

    #     costs = np.round(costs, 1)
    #     print("Sources:\n", sources)
    #     print("Cost Matrix:\n", costs)
    #     print("Capacities:\n", capacities)
    #     print("Destination nodes:\n", dests)
    #     print("Weights:\n", weights)
    #     print("Time Intervals:\n", time_intervals)

    #     return VRPProblem(sources, costs, capacities, dests, weights, time_intervals, services, node_coords), g



            
















































    def solveWithoutTime(self):

        def indiciesConnectedToDepot(route):
            #route = [0,1,2,3,0]
            leftIndex = route[1] #1
            rightIndex = route[-2] #3
            return leftIndex, rightIndex
        
        #returns which route dest is a part of
        def whichRoute(destination):
            route = whichRouteDict[destination]
            return route
        
        #returns true if dest1 and dest2 are in dif routes
        def isInDifRoutes(dest1, dest2):
            return whichRoute(dest1) != whichRoute(dest2)
        
        def updateEverything(routeTemp, currentRouteIndex1, currentRouteIndex2, routes):
            print(f'RouteTemp: {routeTemp}')

            if (currentRouteIndex1 > currentRouteIndex2):
                del routes[currentRouteIndex1]
                del routes[currentRouteIndex2]
            else:
                del routes[currentRouteIndex2]
                del routes[currentRouteIndex1]

            print(f'Routes(After Delete): {routes}')
            
            routes.append(routeTemp)

            print(f'Routes(After Add): {routes}')
            print(f'DictB: {whichRouteDict}')
            for i, route in enumerate(routes):
                for node in route:
                    whichRouteDict[node] = i + 1
            print(f'DictA: {whichRouteDict}')
        
        
        problem = self.problem
        weights = problem.weights
        nodes = problem.dests #excludes depot
        capacities = problem.capacities
        # time_intervals = problem.time_intervals
        # services = problem.services

        #creating dictionary {1: 1, 2: 2, 3: 3, 4: 4} for easy node lookup and removal
        nodesDict = {}
        whichRouteDict = {} #5:3 means dest 5 is in route 3
        for i, node in enumerate(nodes):
            nodesDict[i + 1] = node

        routes = []

        #savings contains (1, 2, 51.1) where 51.1 is the savings from dest 1 to 2 rather than depot to 1 + depot to 2
        savings = self.calculate_sorted_savings()

        for dest1, dest2, saving in savings: #link -> (dest1, dest2)
            #check to see if nodes are a part of any route
            is_dest1_in_dict = dest1 in nodesDict #true means dest is not a part of a route
            is_dest2_in_dict = dest2 in nodesDict
            print(f'Routes: {routes}')

            
            if is_dest1_in_dict:
                if not is_dest2_in_dict: #dest1 = true, dest2 = false
                    currentRouteIndex = whichRoute(dest2) - 1
                    if self.check_constraints(routes[currentRouteIndex], dest1, capacities[0]):
                        leftIndex, rightIndex = indiciesConnectedToDepot(routes[currentRouteIndex])
                        #print(f'dest2: {dest2} left: {leftIndex} right: {rightIndex}')
                        if(dest2 == leftIndex):
                            routes[currentRouteIndex].insert(1, dest1)
                            del nodesDict[dest1]
                            whichRouteDict[dest1] = currentRouteIndex + 1
                        elif(dest2 == rightIndex):
                            routes[currentRouteIndex].insert(-1, dest1)
                            del nodesDict[dest1]
                            whichRouteDict[dest1] = currentRouteIndex + 1
                    else:
                        continue

                else: #dest1 = true, dest2 = true #means current dests are not in a route
                    #create route
                    if (weights[dest1] + weights[dest2] <= capacities[0]):
                        routes.append([0,dest1,dest2,0])
                        whichRouteDict[dest1] = len(routes)
                        whichRouteDict[dest2] = len(routes)
                        del nodesDict[dest1]
                        del nodesDict[dest2]
            else:
                if is_dest2_in_dict:  #dest1 = false, dest2 = true
                    currentRouteIndex = whichRoute(dest1) - 1
                    if self.check_constraints(routes[currentRouteIndex], dest2, capacities[0]):
                        leftIndex, rightIndex = indiciesConnectedToDepot(routes[currentRouteIndex])
                        #print(f'dest2: {dest1} left: {leftIndex} right: {rightIndex}')
                        if(dest1 == leftIndex):
                            routes[currentRouteIndex].insert(1, dest2)
                            del nodesDict[dest2]
                            whichRouteDict[dest2] = currentRouteIndex + 1
                        elif(dest1 == rightIndex):
                            routes[currentRouteIndex].insert(-1, dest2)
                            del nodesDict[dest2]
                            whichRouteDict[dest2] = currentRouteIndex + 1
                else: ##dest1 = false, dest2 = false
                    #1.check if dest1 and dest2 are in different routes
                    #2. check if dest1 and dest2 are both exterior nodes
                    #3. merge routes if 1 and 2 are met
                    if(isInDifRoutes(dest1, dest2)):
                        #in different routes
                        print(f'Different Routes: ({dest1}, {dest2})')
                        currentRouteIndex1 = whichRoute(dest1) - 1
                        route1 = routes[currentRouteIndex1]
                        leftIndex1, rightIndex1= indiciesConnectedToDepot(route1)
                        currentRouteIndex2 = whichRoute(dest2) - 1
                        route2 = routes[currentRouteIndex2]
                        leftIndex2, rightIndex2= indiciesConnectedToDepot(route2)
                        route1 = route1[1:-1] #routes without attached depot
                        route2 = route2[1:-1]
                        canMerge = self.canMerge(route1, route2, capacities[0])
                        routeTemp = None

                        if (canMerge):
                            if(dest1 == leftIndex1):
                                if(dest2 == rightIndex2):
                                    #dest1 = left, dest2 = right
                                    routeTemp = [0] + route2 + route1 + [0]
                                    print(f'left: {dest1} right: {dest2}')
                                elif (dest2 == leftIndex2):
                                    #dest1 = left, dest2 = left
                                    routeTemp = [0] + route1[::-1] + route2 + [0]
                                    print(f'left: {dest1} left: {dest2}')
                            elif (dest1 == rightIndex1):
                                if(dest2 == rightIndex2):
                                    #dest1 = right, dest2 = right
                                    routeTemp = [0] + route1 + route2[::-1] + [0]
                                    print(f'right: {dest1} right: {dest2}')
                                elif (dest2 == leftIndex2):
                                    #dest1 = right, dest2 = left
                                    routeTemp = [0] + route1 + route2 + [0]
                                    print(f'right: {dest1} left: {dest2}')

                            #update whichRouteDict and routes
                            if routeTemp is not None:
                                updateEverything(routeTemp, currentRouteIndex1, currentRouteIndex2, routes)
                        

                    else:
                        #in same route
                        continue

        
        #print(f"routes: {routes}")
        return VRPSolution(problem, routes)
                

        

    def solve1(self):
        problem = self.problem
        num_customers = len(problem.dests)
        nodes = problem.dests
        capacities = problem.capacities
        costs = problem.costs



        print("Customers" + str(num_customers))
        print("Nodes" + str(nodes))
        print("Capacities" + str(capacities))
        print("Costs" + str(costs))

        # Calculate savings matrix
        savings = np.zeros((num_customers, num_customers))
        for i in range(num_customers):
            for j in range(i+1, num_customers):
                savings[i][j] = costs[0][i+1] + costs[0][j+1] - costs[i+1][j+1]
                
        # Sort savings matrix in decreasing order
        savings_flat = [(i, j, savings[i][j]) for i in range(num_customers) for j in range(i+1, num_customers)]
        savings_flat = [(i+1, j+1, savings[i][j]) for i in range(num_customers - 1) for j in range(i+1, num_customers - 1)]
        savings_flat_sorted = sorted(savings_flat, key=lambda x: x[2], reverse=True)

        #print("SAVINGS")
        #print(savings_flat_sorted)

        savings_flat_sorted = [[node1, node2] for node1, node2, savings in savings_flat_sorted]
        for item in savings_flat_sorted:
            if 0 in item:
                #print(item)
                lol = 0

        


        # Create empty routes
        routes = []
        currentTimesForRoutes = []


        # Get a list of nodes, excluding the depot
        node_list = list(nodes)

        #if there are any remaining customers to be served
        remaining = True
        
        for link in savings_flat_sorted:
            #print("LINK: " + str(link))
            if remaining:
                
                node_sel, num_in, i_route, overlap = self.which_route(link, routes)
                 # condition a. Either, neither i nor j have already been assigned to a route, 
                # ...in which case a new route is initiated including both i and j.
                if num_in == 0:
                    if self.sum_cap(link) <= capacities[0]:
                        routes.append(link)
                        node_list.remove(link[0])
                        node_list.remove(link[1])
                        #print('\t','Link ', link, ' fulfills criteria a), so it is created as a new route')
                    else:
                        lol = 5
                        #print('\t','Though Link ', link, ' fulfills criteria a), it exceeds maximum load, so skip this link.')
                        
                # condition b. Or, exactly one of the two nodes (i or j) has already been included 
                # ...in an existing route and that point is not interior to that route 
                # ...(a point is interior to a route if it is not adjacent to the depot D in the order of traversal of nodes), 
                # ...in which case the link (i, j) is added to that same route.    
                elif num_in == 1:
                    n_sel = node_sel[0]
                    i_rt = i_route[0]
                    position = routes[i_rt].index(n_sel)
                    link_temp = link.copy()
                    link_temp.remove(n_sel)
                    node = link_temp[0]

                    cond1 = (not self.interior(n_sel, routes[i_rt]))
                    cond2 = (self.sum_cap(routes[i_rt] + [node]) <= capacities[0])

                    if cond1:
                        if cond2:
                            #print('\t','Link ', link, ' fulfills criteria b), so a new node is added to route ', routes[i_rt], '.')
                            if position == 0:
                                routes[i_rt].insert(0, node)
                            else:
                                routes[i_rt].append(node)
                            node_list.remove(node)
                        else:
                           # print('\t','Though Link ', link, ' fulfills criteria b), it exceeds maximum load, so skip this link.')
                            continue
                    else:
                        #print('\t','For Link ', link, ', node ', n_sel, ' is interior to route ', routes[i_rt], ', so skip this link')
                        continue
                    
                # condition c. Or, both i and j have already been included in two different existing routes 
                # ...and neither point is interior to its route, in which case the two routes are merged.        
                else:
                    if overlap == 0:
                        cond1 = (not self.interior(node_sel[0], routes[i_route[0]]))
                        cond2 = (not self.interior(node_sel[1], routes[i_route[1]]))
                        cond3 = (self.sum_cap(routes[i_route[0]] + routes[i_route[1]]) <= capacities[0])

                        if cond1 and cond2:
                            if cond3:
                                route_temp = self.merge(routes[i_route[0]], routes[i_route[1]], node_sel)
                                temp1 = routes[i_route[0]]
                                temp2 = routes[i_route[1]]
                                routes.remove(temp1)
                                routes.remove(temp2)
                                routes.append(route_temp)
                                try:
                                    node_list.remove(link[0])
                                    node_list.remove(link[1])
                                except:
                                    #print('\t', f"Node {link[0]} or {link[1]} has been removed in a previous step.")
                                    pass
                                #print('\t','Link ', link, ' fulfills criteria c), so route ', temp1, ' and route ', temp2, ' are merged')
                            else:
                                #print('\t','Though Link ', link, ' fulfills criteria c), it exceeds maximum load, so skip this link.')
                                continue
                        else:
                           # print('\t','For link ', link, ', Two nodes are found in two different routes, but not all the nodes fulfill interior requirement, so skip this link')
                            continue
                    else:
                        #print('\t','Link ', link, ' is already included in the routes')
                        continue
                    
                for route in routes: 
                    lol = 0
                    #print('\t','route: ', route, ' with load ', self.sum_cap(route))
            else:
                #print('-------')
                #print('All nodes are included in the routes, algorithm closed')
                break
            
            remaining = bool(len(node_list) > 0)

        # check if any node is left, assign to a unique route
        for node_o in node_list:
            routes.append([node_o])

        # add depot to the routes
        for route in routes:
            route.insert(0,0)
            route.append(0)


        return VRPSolution(problem, routes)