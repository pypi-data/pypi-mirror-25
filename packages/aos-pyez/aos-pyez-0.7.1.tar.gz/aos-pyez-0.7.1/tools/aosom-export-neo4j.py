#!/usr/bin/env python
# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://apstra.com/eula

from __future__ import print_function
import os
from apstra.aosom.session import *
from collections import defaultdict
from csv import DictWriter

def neo4j_header(field_names, item):
    header = list()

    neo4j_type_decl = {
        type(int): 'int',
        type(bool): 'boolean',
        type(float): 'float',
        type(None): 'string'
    }

    for key in field_names:
        value = item[key]
        if key == 'id':
            header.append("node_id:ID")
        else:
            ntype = neo4j_type_decl.get(type(value), 'string')
            header.append("%s:%s" % (key, ntype))

    return header


def export_neo4jcsv(bp):
    contents = bp.contents
    nodes = contents['nodes']
    rels = contents['relationships']

    node_table_data = defaultdict(list)

    # make the data

    for node_id, node_data in nodes.items():
        node_table_data[node_data['type']].append(node_data)

    node_table_data.pop('metadata')
    skip_types = list()
    node_csv_files = dict()

    for node_type in node_table_data:
        sample = node_table_data[node_type][0]

        if any('json' in k for k in sample.keys()):
            print("skipping %s" % sample['type'])
            skip_types.append(sample['type'])
            continue

        print("Creating table [%s]" % node_type)

        # make sure 'id' is first field

        sample = node_table_data[node_type][0]
        field_names = sample.keys()
        field_names.remove('id')
        field_names.insert(0, 'id')

        # with open("%s_header.csv" % node_type, "w+") as header_file:
        #     csv_file = DictWriter(header_file,
        #                           fieldnames=neo4j_header(
        #                               field_names=field_names,
        #                               item=sample))
        #     csv_file.writeheader()

        with open("%s.csv" % node_type, 'w+') as data_file:
            csv_file = DictWriter(data_file, fieldnames=field_names)
            csv_file.writerow(dict(zip(field_names,
                                       neo4j_header(field_names=field_names,
                                                    item=sample))))
            csv_file.writerows(rowdicts=node_table_data[node_type])
            node_csv_files[node_type] = data_file.name

    with open("relationships.csv", 'w+') as rel_file:
        csv_file = DictWriter(rel_file,
                              fieldnames=['source_id', 'id', 'target_id', 'type'],
                              extrasaction='ignore')

        csv_file.writerow(dict(
            source_id=':START_ID',
            id='rel_id',
            target_id=':END_ID',
            type=':TYPE'
        ))

        for rel_data in rels.values():
            if rel_data['type'] in skip_types:
                continue
            csv_file.writerow(rel_data)

    with open('import-%s.sh' % bp.name, 'w+') as script:
        print("creating import script: %s" % script.name)
        script.write("/var/lib/neo4j/bin/neo4j-admin import \\\n")
        script.write("--database=graph.db \\\n")
        for node_type, node_file in node_csv_files.items():
            script.write("--nodes:%s_nodes %s \\\n" % (node_type, node_file))
        script.write("--relationships relationships.csv\n")


aos_server = os.getenv('AOS_SERVER', ValueError("missing AOS_SERVER"))
aos_blueprint = os.getenv('AOS_BLUEPRINT', ValueError ("missing AOS_BLUEPRINT"))


for this in [this for this in [aos_server, aos_blueprint] if isinstance(this, Exception)]:
    raise this

aos = Session(aos_server)
aos.login()
bp = aos.Blueprints[aos_blueprint]
if not bp.exists:
    print("blueprint %s does not exist" % aos_blueprint)

export_neo4jcsv(bp)
