from __future__ import print_function

import requests
import hostlist
from builtins import input

from cloudmesh.common.console import Console
from cloudmesh.comet.comet import Comet
from cloudmesh.common.Printer import Printer

from cloudmesh.common.parameter import Parameter
import time
from datetime import datetime
import pytz
from pprint import pprint


class Cluster(object):
    WALLTIME_MINS = 60 * 24 * 2
    N_ALLOCATIONS_PER_LINE = 5
    MINS_PER_UNIT = {"m": 1, "h": 60, "d": 1440, "w": 10080}
    SECS_PER_DAY = 60 * 60 * 24
    STUCK_COMPUTESETS = ["submitted", "ending"]
    FINISHED_COMPUTESETS = ["completed", "failed"]
    ACTIVE_COMPUTESETS = ["running", "submitted", "created"]
    PENDING_COMPUTESETS = ["queued", "submitted", "created"]
    CLUSTER_ORDER=[
                  "name",
                  "state",
                  "kind",
                  "type",
                  "mac",
                  "ip",
                  "cpus",
                  "cluster",
                  "memory",
                  "disksize",
                  "active_computeset",
                  "allocation",
                  "admin_state"
                    ]

    CLUSTER_HEADER=[
                  "name",
                  "state",
                  "kind",
                  "type",
                  "mac",
                  "ip",
                  "cpus",
                  "cluster",
                  "RAM(M)",
                  "disk(G)",
                  "computeset",
                  "allocation",
                  "admin_state"
                    ]

    CLUSTER_ORDER_TABLE=[
                  "name",
                  "state",
                  "active_computeset",
                  "allocation",
                  "admin_state",
                  "mac",
                  "ip",
                  "cluster",
                  "kind",
                  "type",
                  "cpus",
                  "memory",
                  "disksize"
                    ]

    CLUSTER_HEADER_TABLE=[
                  "name",
                  "state",
                  "computeset",
                  "allocation",
                  "admin_state",
                  "mac",
                  "ip",
                  "cluster",
                  "kind",
                  "type",
                  "cpus",
                  "RAM(M)",
                  "disk(G)"
                    ]

    CLUSTER_ORDER_TABLE_CONCISE=[
                  "name",
                  "state",
                  "active_computeset",
                  "allocation",
                  "admin_state",
                  "mac",
                  "ip",
                  "cluster"
                    ]

    CLUSTER_HEADER_TABLE_CONCISE=[
                  "name",
                  "state",
                  "computeset",
                  "allocation",
                  "admin_state",
                  "mac",
                  "ip",
                  "cluster"
                    ]

    CLUSTER_ORDER_TABLE_STATE=[
                  "name",
                  "state",
                  "active_computeset",
                  "allocation",
                  "admin_state"
                    ]

    CLUSTER_HEADER_TABLE_STATE=[
                  "name",
                  "state",
                  "computeset",
                  "allocation",
                  "admin_state"
                    ]

    CLUSTER_TABLE_VIEW = \
                {"FULL": {"header": CLUSTER_HEADER_TABLE,
                          "order": CLUSTER_ORDER_TABLE},
                 "CONCISE": {"header": CLUSTER_HEADER_TABLE_CONCISE,
                             "order": CLUSTER_ORDER_TABLE_CONCISE},
                 "STATE": {"header": CLUSTER_HEADER_TABLE_STATE,
                           "order": CLUSTER_ORDER_TABLE_STATE}
                }

    '''
    CLUSTER_SORT_KEY=[
                      "name",
                      "state",
                      "kind",
                      "type",
                      "mac",
                      "ip",
                      "cpus",
                      "cluster",
                      "ram",
                      "disk",
                      "computeset",
                      "allocation",
                      "admin_state"]
    '''
    CLUSTER_SORT_KEY=CLUSTER_HEADER[:]
    CLUSTER_SORT_KEY[CLUSTER_HEADER.index("RAM(M)")] = "ram"
    CLUSTER_SORT_KEY[CLUSTER_HEADER.index("disk(G)")] = "disk"

    '''
    NODEINFO_ORDER=[
                    'cpus',
                    'disksize',
                    'dns1',
                    'dns2',
                    'frontend_state',
                    'gateway',
                    'interface',
                    'memory',
                    'name',
                    'ntp',
                    'pub_ip',
                    'pub_mac',
                    'pub_netmask',
                    'state',
                    'type']
    '''

    @staticmethod
    def simple_list(id=None, format="table"):
        result = ""
        if id is None:
            r = Comet.get(Comet.url("cluster/"))
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))
            if r is None:
                Console.error("Error finding cluster `{}`"
                              .format(id))
                return result
            r = [r]

        if r is not None:
            if 'error' in r:
                Console.error("An error occurred: {error}".format(**r))
                raise ValueError("COMET Error")
            elif len(r) > 0 and 'error' in r[0]:
                Console.error("An error occurred: {error}".format(**r[0]))
                raise ValueError("COMET Error")

            if format == "rest":
                result = r
            else:
                elements = {}
                for cluster in r:
                    element = {}
                    if 'allocations' in cluster:
                        if format == 'table':
                            element["allocations"] = \
                                    "\n".join(cluster["allocations"])
                        else:
                            element["allocations"] = \
                                    ";".join(cluster["allocations"])

                    for attribute in ["project", "name", "description"]:
                        element[attribute] = cluster[attribute]
                        element["nodes"] = len(cluster["computes"])
                    for attribute in cluster["frontend"]:
                        element["frontend " + attribute] = \
                                    cluster["frontend"][attribute]
                    names = []
                    for compute in cluster["computes"]:
                        names.append(compute["name"])

                    element["computes"] = hostlist.collect_hostlist(names)

                    elements[cluster["name"]] = element

                result = Printer.write(elements,
                                       order=[
                                           "name",
                                           "project",
                                           "nodes",
                                           "computes",
                                           "frontend name",
                                           "frontend state",
                                           "frontend type",
                                           "allocations",
                                           "description",
                                       ],
                                       header=[
                                           "Name",
                                           "Project",
                                           "Count",
                                           "Nodes",
                                           "Frontend (Fe)",
                                           "State (Fe)",
                                           "Type (Fe)",
                                           "allocations",
                                           "Description",
                                       ],

                                       output=format)
            return result

    @staticmethod
    def list(id=None, format="table", sort=None, view="FULL"):

        def check_for_error(r):
            if r is not None:
                if 'error' in r:
                    Console.error("An error occurred: {error}".format(**r))
                    raise ValueError("COMET Error")

        result = ""
        if id is None:
            r = Comet.get(Comet.url("cluster/"))
            check_for_error(r)
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))
            check_for_error(r)
            if r is None:
                Console.error("Error finding cluster `{}`"
                              .format(id))
                return result
            r = [r]

        #
        # getting account/allocation for each computeset
        # to display in the cluster view
        computeset_account = {}
        # stuck_computesets = {}
        computesets = Comet.get_computeset()

        # pprint (computesets)
        if computesets:
            computesets_submitted = Comet.get_computeset(state="submitted")
            if computesets_submitted:
                computesets += computesets_submitted
            computesets_ending = Comet.get_computeset(state="ending")
            if computesets_ending:
                computesets += computesets_ending
            for computeset in computesets:
                id = computeset["id"]
                account = computeset["account"]
                if id not in computeset_account:
                    computeset_account[id] = account

        # no longer track and display the (possible) stuck
        # computeset in this way
        '''
        stuck_computesets = {}
        computesets = Comet.get_computeset()
        if computesets:
            for computeset in computesets:
                if computeset["state"] in Cluster.STUCK_COMPUTESETS:
                    cluster = computeset["cluster"]
                    id = computeset["id"]
                    nodes = computeset["computes"]

                    if cluster not in stuck_computesets:
                        stuck_computesets[cluster] = {}
                    for node in nodes:
                        stuck_computesets[cluster][node["name"]] = \
                            "{}({})".format (id, computeset["state"])
        '''

        if r is not None:
            if format == "rest":
                result = r
            else:
                result = ''
                data = []

                empty = {
                    'cluster': None,
                    'cpus': None,
                    'host': None,
                    "mac": None,
                    'ip': None,
                    'memory': None,
                    'disksize': None,
                    'name': None,
                    'state': None,
                    'type': None,
                    'active_computeset': None,
                    'kind': 'frontend',
                    'admin_state': None
                }

                for cluster in sorted(r, key=lambda x: x["name"]):

                    clients = cluster["computes"]
                    for client in clients:
                        client["kind"] = "compute"
                    frontend = dict(empty)
                    frontend.update(cluster["frontend"])
                    pubip = cluster["frontend"]["pub_ip"]
                    pubmac = cluster["frontend"]["pub_mac"]
                    frontend["ip"] = pubip
                    frontend["pub_mac"] = pubmac
                    frontend["admin_state"] = cluster["frontend"]["frontend_state"]
                    result += "Cluster: %s\tFrontend: %s\tIP: %s\n" % \
                                (cluster["name"],
                                 cluster["frontend"]["name"],
                                 pubip)
                    if len(clients) > 0:
                        frontend['cluster'] = clients[0]['cluster']
                    else:
                        frontend['cluster'] = frontend['name']
                    data += [frontend]
                    data += clients

                for index, anode in enumerate(data):
                    bnode = dict(anode)
                    pubmac = None
                    if 'pub_mac' in bnode:
                        pubmac = bnode["pub_mac"]
                    if "interface" in bnode:
                        macs = []
                        macs_pub_order = []
                        # ips = []
                        for ipaddr in anode["interface"]:
                            macs.append(ipaddr["mac"])
                            # ips.append(ipaddr["ip"] or "N/A")
                        if pubmac in macs:
                            macs_pub_order.append(pubmac)
                            for mac in macs:
                                if mac != pubmac:
                                    macs_pub_order.append(mac)
                        else:
                            macs_pub_order = macs
                        if format == 'table':
                            bnode["mac"] = "\n".join(macs_pub_order)
                        else:
                            bnode["mac"] = ";".join(macs_pub_order)

                        if "active_computeset_state" in anode and \
                                anode["active_computeset"] is not None and \
                                anode["active_computeset_state"] is not None:
                            # if not running state, show also the status after
                            # the computeset id
                            if anode["active_computeset_state"] != 'running':
                                bnode["active_computeset"] = "%s(%s)" % \
                                                    (anode["active_computeset"],
                                                     anode["active_computeset_state"])
                            # if an active computeset has a valid account
                            # associated with it, display the account/allocation
                            # does this for computeset in all states
                            if anode["active_computeset"] in computeset_account:
                                bnode["allocation"] = \
                                computeset_account[anode["active_computeset"]]

                        if "compute_state" in anode:
                            bnode["admin_state"] = anode["compute_state"]
                        #anode["ip"] = "; ".join(ips)
                        if "ip" not in bnode:
                            bnode["ip"] = None

                    del bnode["interface"]
                    #
                    # stuck state included in cluster data via API
                    '''
                    if bnode["cluster"] in stuck_computesets and \
                                    bnode["name"] in stuck_computesets[bnode["cluster"]]:
                        bnode["active_computeset"] = \
                            stuck_computesets[bnode["cluster"]][bnode["name"]]
                    '''
                    data[index] = bnode

                sort_keys = ('cluster','mac')
                if sort:
                    if sort in Cluster.CLUSTER_SORT_KEY:
                        # print (sort)
                        idx = Cluster.CLUSTER_SORT_KEY.index(sort)
                        # print (idx)
                        sortkey = Cluster.CLUSTER_ORDER[idx]
                        # print (sortkey)
                        sort_keys = (sortkey,)
                        # print (sort_keys)
                if "table" == format:
                    result_print = Printer.write(data,
                            order=Cluster.CLUSTER_TABLE_VIEW[view]["order"],
                            header=Cluster.CLUSTER_TABLE_VIEW[view]["header"],
                            output=format,
                            sort_keys=sort_keys)
                    result += str(result_print)
                else:
                    result_print = Printer.write(data,
                                                 order=Cluster.CLUSTER_ORDER,
                                                 header=Cluster.CLUSTER_HEADER,
                                                 output=format,
                                                 sort_keys=sort_keys)
                    result = result_print
            return result

    @staticmethod
    def display_get_allocation(allocations):
        allocation = None
        allocations_sorted = sorted(allocations)
        i = 1
        while i < len(allocations_sorted) + 1:
            for j in range(0, Cluster.N_ALLOCATIONS_PER_LINE):
                if i < len(allocations_sorted) + 1:
                    print ("{}: {}".format(i, allocations_sorted[i - 1]),
                          end="\t")
                    i += 1
            print("")
        print("")
        chosen_alloc = -1
        while chosen_alloc < 0:
            allocation_input = input("Pick an allocation by specifying its index: ")
            try:
                chosen_alloc = int(allocation_input)
                if 0 < chosen_alloc < len(allocations_sorted) + 1:
                    allocation = allocations_sorted[chosen_alloc - 1]
                else:
                    chosen_alloc = -1
                    print("Invalid index specified. "
                          "Please choose between 1 and {}"
                          .format(len(allocations_sorted))
                          )
            except:
                if allocation_input in allocations_sorted:
                    chosen_alloc = 0
                    allocation = allocation_input
        return allocation

    @staticmethod
    def info():
        Console.error("comet cluster info: to be implemented")
        pass

    @staticmethod
    def add():
        pass

    @staticmethod
    def start(id):
        data = {"id": id}
        r = requests.post(Comet.url("cluster/{id}/start".format(**data)))
        print(r)

    @staticmethod
    def stop(id):
        data = {"id": id}
        r = requests.post(Comet.url("cluster/{id}/stop".format(**data)))
        print(r)

    @staticmethod
    def computeset(id=None, cluster=None, state=None, allocation=None):
        #
        # state could be one of
        # ['created' or 'submitted' or 'failed' or 'running'
        #   or 'cancelled' or 'ending' or 'completed']
        computesets = Comet.get_computeset(id, state)
        if computesets is not None:
            if 'cluster' in computesets:
                result = Cluster.output_computeset(computesets)
            else:
                result = ''
                for acomputeset in computesets:
                    result += Cluster.output_computeset(acomputeset,
                                                        cluster,
                                                        allocation)
        else:
            if id:
                result = "No computeset found with the specified ID"
            else:
                result = "No computeset found"
        return result

    @staticmethod
    def output_computeset(computesetdict, cluster=None, allocation=None):
        # print (cluster, state, allocation)
        result = ""
        # filter out based on query criteria
        if cluster and 'cluster' in computesetdict:
            if computesetdict["cluster"] != cluster:
                return result
        # no longer needing state filter as handled by API
        # if state and 'state' in computesetdict:
        #     if "ALL" != state and computesetdict["state"] != state:
        #         return result
        if allocation and 'account' in computesetdict:
            if computesetdict["account"] != allocation:
                return result

        # no longer needing state filter as handled by API
        # if (state and ("ALL" == state or computesetdict["state"] == state)) or \
        #    (computesetdict["state"] not in Cluster.FINISHED_COMPUTESETS):
        starttime = ''
        endtime = ''
        walltime = ''
        runningTime = ''
        remainingTime = ''
        if 'walltime_mins' in computesetdict:
            walltime = computesetdict["walltime_mins"]
            walltime_seconds = walltime * 60
            walltime = Cluster.format_ddd_hh_mm(walltime_seconds)
        if 'start_time' in computesetdict and \
            computesetdict["start_time"] is not None:
            start_seconds = int(computesetdict["start_time"])
            end_seconds = start_seconds + walltime_seconds
            if computesetdict["state"] in Cluster.FINISHED_COMPUTESETS \
                or computesetdict["state"] == 'ending':
                runningSecs = walltime_seconds
            else:
                runningSecs = int(time.time())-start_seconds
            remainingSecs = walltime_seconds - runningSecs
            starttime = time.strftime("%D %H:%M %Z",
                                time.localtime(start_seconds))
            endtime = time.strftime("%D %H:%M %Z",
                                time.localtime(end_seconds))
            runningTime = Cluster.format_ddd_hh_mm(runningSecs)
            remainingTime = Cluster.format_ddd_hh_mm(remainingSecs)

        result += "\nClusterID: {}\tComputesetID: {}\t State: {}\t\tAllocation: {}\n" \
                  "Start (est): {}\t\tEnd (est): {}\n"\
                  "Requested Time (ddd-hh:mm): {}\tRunning Time (est): {}\t\tRemaining Time (est): {}\n"\
                    .format(computesetdict["cluster"],
                            computesetdict["id"],
                            computesetdict["state"],
                            computesetdict["account"],
                            starttime,
                            endtime,
                            walltime,
                            runningTime,
                            remainingTime
                            )
        data = computesetdict["computes"]
        for index, anode in enumerate(data):
            bnode = dict(anode)
            if "interface" in bnode:
                macs = []
                #ips = []
                for ipaddr in anode["interface"]:
                    macs.append(ipaddr["mac"])
                    #ips.append(ipaddr["ip"] or "N/A")
                if format=='table':
                    bnode["mac"] = "\n".join(macs)
                else:
                    bnode["mac"] = ";".join(macs)
                #anode["ip"] = "; ".join(ips)
            del bnode["interface"]
            data[index] = bnode
        result += str(Printer.write(data,
                                   order=[
                                       "name",
                                       "state",
                                       "type",
                                       "mac",
                                       #"ip",
                                       "cpus",
                                       "cluster",
                                       "host",
                                       "memory",
                                   ],
                                   output="table",
                                   sort_keys='cluster'))
        return result

    @staticmethod
    def format_ddd_hh_mm(time_duration_secs):
        ddd = time_duration_secs // Cluster.SECS_PER_DAY
        secs = time_duration_secs % Cluster.SECS_PER_DAY
        hh = secs // 3600
        mm = (secs % 3600) // 60

        if ddd != 0:
            ret = "%s-%02d:%02d" % (ddd, hh, mm)
        else:
            ret = "%02d:%02d" % (hh, mm)
        return ret

    @staticmethod
    def convert_to_mins(s):
        mins = None
        if s is not None:
            s = s.lower()
            if s[-1] in Cluster.MINS_PER_UNIT:
                mins = int(s[:-1]) * Cluster.MINS_PER_UNIT[s[-1]]
        return mins

    @staticmethod
    def check_nodes_computesets(clusterid, computenodeids):
        hosts_param = hostlist.expand_hostlist(computenodeids)
        hosts_param_set = set(hosts_param)
        nodes_free = True
        nodes_allocated = False
        nodes_checked = False
        # computesetid = -1
        computesets = Comet.get_computeset()
        # get all active computeset and put nodes into a set
        allhosts = set()
        for computeset in computesets:
            if computeset["cluster"] == clusterid \
                    and (computeset["state"] in Cluster.ACTIVE_COMPUTESETS):
                computesetid = computeset["id"]
                # print (computesetid)
                for compute in computeset["computes"]:
                    allhosts.add(compute["name"])

        # all nodes allocated
        if hosts_param_set <= allhosts:
            nodes_allocated = True
            nodes_free = False
            nodes_checked = True
        # at least one specified host not in any Active computeset
        else:
            for host in hosts_param:
                # some specified nodes are in Active computeset
                if host in allhosts:
                    nodes_free = False
                    nodes_checked = True
                    break

        # print ("nodes_checked: %s" % nodes_checked)
        # print ("nodes_free: %s" % nodes_free)
        return [nodes_free, nodes_allocated]

    @staticmethod
    def computeset_start(clusterid,
                         computenodeids=None,
                         numnodes=None,
                         allocation=None,
                         reservation=None,
                         walltime=None):
        ret = ''
        # print ("clusterid: %s" % clusterid)
        # print ("computenodeids: %s" % computenodeids)
        # print ("numnodes: %s" % numnodes)
        # print ("allocation: %s" % allocation)
        # print ("walltime: %s" % walltime)
        data = None
        # validating and initiating allocation and walltime values
        if not allocation:
            cluster = Cluster.list(clusterid, format='rest')
            # use the first one if no provided
            allocation = cluster[0]['allocations'][0]
        if not walltime:
            walltime = Cluster.WALLTIME_MINS

        # preparing parameters for the post call
        # num of nodes to start
        #
        # Now it accepts
        # {"cluster":"vc3","computes":"compute[1-2]"},
        # {"cluster":"vc3","computes":["compute1","compute2"]} and
        # {"cluster":"vc3","count":2}
        #
        if numnodes:
            data = {"cluster": "%s" % clusterid,
                    "count": "%s" % numnodes,
                    "walltime_mins": "%s" % walltime,
                    "allocation": "%s" % allocation}
        # computenodeids in hostlist format
        elif computenodeids:
            nodes_free = Cluster.check_nodes_computesets(clusterid, computenodeids)[0]
            if not nodes_free:
                Console.error("Some nodes are already in active computesets",
                              traceflag=False)
                return ret
            else:
                data = {"computes": "%s" % computenodeids,
                        "cluster": "%s" % clusterid,
                        "walltime_mins": "%s" % walltime,
                        "allocation": "%s" % allocation}

        if reservation:
            data["reservation"] = reservation

        # print("Issuing request to start/allocate and power on nodes...")
        posturl = Comet.url("computeset/")
        # print ("POST data: %s" % data)
        r = Comet.post(posturl, data=data)
        # print("RETURNED RESULTS:")
        # print (r)
        if r is None:
            ret = "An error occured. Please check your command and try again"
        else:
            if 'cluster' in r:
                if 'state' in r and \
                                r['state'] in Cluster.PENDING_COMPUTESETS:
                    computesetid = r['id']
                    ret = 'Request accepted! Check status with:\n' \
                          'comet cluster {}\n'.format(clusterid) + \
                          'or:\n' \
                          'comet computeset {}\n'.format(computesetid)
                else:
                    # in case of some internal problem
                    ret = ''
            elif 'error' in r:
                ret = "An error occurred: {}".format(r['error'])
            else:
                ret = "An internal error occured. " \
                      "Please submit a ticket with the " \
                      "following info:\n {}\n" \
                    .format(r)
        return ret

    @staticmethod
    def computeset_terminate(computesetid):
        ret = ''
        url = Comet.url("computeset/")
        action = "shutdown"
        puturl = "{:}{:}/{}".format(url, computesetid, action)
        # print (puturl)
        r = Comet.put(puturl)
        if r is not None:
            if '' != r.strip():
                ret = r
            else:
                ret = "Request Accepted. " \
                      "In the process of terminating the computeset"
        else:
            ret = "Problem executing the request. " \
                  "Check if the computeset exists"
        return ret

    @staticmethod
    def power(clusterid, subject, param=None, action=None):
        ret = ''
        # print ("clusterid: %s" % clusterid)
        # print ("subject: %s" % subject)
        # print ("param: %s" % param)
        # print ("action: %s" % action)
        if subject in ['HOSTS']:
            nodes_allocated = Cluster.check_nodes_computesets(clusterid, param)[1]
            if nodes_allocated:
                hosts_param = hostlist.expand_hostlist(param)
                # print (hosts_param)
                for host in hosts_param:
                    url = Comet.url("cluster/{}/compute/{}"
                                    .format(clusterid, host))
                    if action in ["on", "off"]:
                        action = "power{}".format(action)
                    puturl = "{}/{}".format(url, action)
                    # print (puturl)
                    r = Comet.put(puturl)
                    if r is not None:
                        if '' != r.strip():
                            ret = r
                        else:
                            ret += "Request Accepted. " \
                                   "In the process of {} node {}\n" \
                                .format(action, host)
                    else:
                        ret += "Problem executing the request. " \
                               "Check if the node {} belongs to the cluster" \
                            .format(host)
                        # print(ret)
            else:
                Console.error("At least one specified node is not in any "
                              "active computesets thus cannot be powered on.\n"
                              "Please start the node(s) with 'comet start' first",
                              traceflag=False)
        elif 'FE' == subject:
            url = Comet.url("cluster/{}/frontend/".format(clusterid))
            if action in ["on", "off", "reboot", "reset", "shutdown"]:
                if action in ["on", "off"]:
                    action = "power{}".format(action)
                puturl = "{}{}".format(url, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        ret = r
                    else:
                        ret = "Request Accepted. " \
                              "In the process of {} the front-end node".format(action)
                else:
                    ret = "Problem executing the request. " \
                          "Check if the cluster exists"
            else:
                ret = "Action not supported! Try these: on/off/reboot/reset/shutdown"
        elif 'COMPUTESET' == subject:
            url = Comet.url("computeset/")
            if action in ["on", "off"]:
                ret = "Action NOT SUPPORTED! Use 'comet start/terminate'!"
            elif action in ["reboot", "reset", "shutdown"]:
                if action in ["off"]:
                    action = "power{}".format(action)
                puturl = "{:}{:}/{}".format(url, param, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        ret = r
                    else:
                        ret = "Request Accepted. " \
                              "In the process of {} the computeset".format(action)
                else:
                    ret = "Problem executing the request. " \
                          "Check if the computeset exists"
            else:
                ret = "Action not supported! Try these: reboot/reset/shutdown"
        return ret

    @staticmethod
    def detach_iso(clusterid, nodeids=None, action='Detaching'):
        return Cluster.attach_iso('', clusterid, nodeids, action='Detaching')

    @staticmethod
    def attach_iso(iso_id_name, clusterid, nodeids=None, action='Attaching'):
        ret = ''
        # print ("Attaching ISO image")
        # print ("iso_id_name: %s" % iso_id_name)
        # print ("cluster: %s" % clusterid)
        # print ("node: %s" % nodeid)

        # obtain the list of iso first to support attach by index
        # and easy verification of image name
        isodict = {}
        isos = (Comet.list_iso())
        idx = 0
        for iso in isos:
            if iso.startswith("public/"):
                iso = iso.split("/")[1]
            idx += 1
            isodict[str(idx)] = iso

        if iso_id_name != '':
            if iso_id_name.isdigit():
                if iso_id_name in isodict:
                    iso_id_name = isodict[iso_id_name]
                else:
                    iso_id_name = None
            else:
                if not iso_id_name in list(isodict.values()):
                    iso_id_name = None

        if iso_id_name is not None:
            # currently only those in public directory is accessible
            # for empty string, DO NOT append as that is for detach
            if len(iso_id_name) != 0:
                iso_id_name = "public/{}".format(iso_id_name)
            urls = {}
            # attaching to compute node
            if nodeids:
                nodeids = hostlist.expand_hostlist(nodeids)
                for nodeid in nodeids:
                    url = Comet.url("cluster/{}/compute/{}/attach_iso?iso_name={}") \
                        .format(clusterid, nodeid, iso_id_name)
                    urls["Node {}".format(nodeid)] = url
            else:
                # attaching to fronend node
                url = Comet.url("cluster/{}/frontend/attach_iso?iso_name={}") \
                    .format(clusterid, iso_id_name)
                urls['Frontend'] = url
            # data = {"iso_name": "%s" % iso_id_name}
            # print ("url: %s" % url)
            # print ("data: %s" % data)
            tofrom = {}
            tofrom['Attaching'] = 'to'
            tofrom['Detaching'] = 'from'
            for node, url in urls.items():
                url = url.replace("+","%2B")
                r = Comet.put(url)
                # print (r)
                if r is not None:
                    if '' != r.strip():
                        ret += r
                    else:
                        ret += "Request Accepted. {} the iso image {} {} of cluster {}\n" \
                            .format(action, tofrom[action], node, clusterid)
                else:
                    ret += "Something wrong during {} the iso image {} {} of cluster {}!" \
                           "Please check the command and try again\n" \
                        .format(action, tofrom[action], node, clusterid)
        else:
            ret = "ERROR: The specified index or image name not matching any from the ISO list!\n"\
                  "Check 'cm comet iso list'"
        return ret

    @staticmethod
    def rename_node(clusterid, old_compute_name, new_compute_name):
        url = Comet.url("cluster/{}/compute/{}/rename"
                        .format(clusterid, old_compute_name))
        data = {"name": "%s" % new_compute_name}
        ret = ""
        r = Comet.post(url, data=data)
        # print (r)
        if r is not None:
            if '' != r.strip():
                ret = r
            else:
                ret = "Request Accepted."
        return ret

    @staticmethod
    def node_info(clusterid, nodeid=None, format='table'):
        if nodeid:
            url = Comet.url("cluster/{}/compute/{}/"
                            .format(clusterid, nodeid))
        else:
            url = Comet.url("cluster/{}/frontend/"
                            .format(clusterid))
        r = Comet.get(url)
        ret = "ERROR: Node not available. Please check the cluster/node name!\n"
        if r:
            ret = Printer.attribute(r,
                                 #order=Cluster.NODEINFO_ORDER,
                                 output=format)
        return ret

    @staticmethod
    def delete():
        pass
