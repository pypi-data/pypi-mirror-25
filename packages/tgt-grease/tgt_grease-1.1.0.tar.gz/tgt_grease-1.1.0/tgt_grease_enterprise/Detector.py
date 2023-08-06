import json
from collections import defaultdict

from tgt_grease_daemon.BaseCommand import GreaseDaemonCommand
from tgt_grease_core_util.Database import Connection
from tgt_grease_core_util.ImportTools import Importer

import Detectors
from Detectors import DetectorConfiguration


class Detector(GreaseDaemonCommand):
    def __init__(self):
        super(Detector, self).__init__()
        self._conn = Connection()
        self._excelsior_config = DetectorConfiguration.ConfigurationLoader()
        self._importer = Importer(self._ioc.message())

    def execute(self, context='{}'):
        # first lets see if we have some stuff to parse
        sql = """
            SELECT
              sf.id,
              sf.source_document,
              sf.scanner
            FROM
              grease.source_file sf
            INNER JOIN grease.job_servers js ON (js.id = sf.job_server)
            WHERE
              js.host_name = %s AND
              sf.completed = FALSE AND
              sf.in_progress = FALSE
            LIMIT 15
        """
        result = self._conn.query(sql, (self._grease_identity,))
        # Now lets loop through
        self._ioc.message().debug("TOTAL SOURCE DOCUMENTS RETURNED: [{0}]".format(str(len(result))), True)
        for source in result:
            # first claiming them as ours then parsing them
            self._take_ownership(source[0])
            # now lets parse the sources
            self._ioc.message().debug("PROCESSING SOURCE ID: [{0}]".format(str(source[0])), True)
            parsed_source = self._parse_source(source[1], self._excelsior_config.get_scanner_config(source[2]))
            self._complete(source[0])
            # now lets assign this parsed source out
            if self._schedule_scheduling(parsed_source, source[2]):
                self._ioc.message().info("Successfully Scheduled Parsed Source ID: [" + str(source[0]) + "]")
                continue
            else:
                self._reverse(source[0])
                self._ioc.message().error("Failed To Schedule Parsed Source ID: [" + str(source[0]) + "]")
                continue
        return True

    def _take_ownership(self, source_file_id):
        # type: (int) -> None
        sql = """
            UPDATE
              grease.source_file
            SET
              in_progress = true,
              pick_up_time = current_timestamp
            WHERE
              id = %s
        """
        self._ioc.message().debug("TAKING OWNERSHIP OF SOURCE ID: [{0}]".format(source_file_id), True)
        self._conn.execute(sql, (source_file_id,))

    def _complete(self, source_file_id):
        # type: (int) -> None
        sql = """
            UPDATE
              grease.source_file
            SET
              completed = TRUE,
              in_progress = false,
              completed_time = current_timestamp
            WHERE
              id = %s
        """
        self._ioc.message().debug("COMPLETING SOURCE ID: [{0}]".format(source_file_id), True)
        self._conn.execute(sql, (source_file_id,))

    def _reverse(self, source_file_id):
        sql = """
            UPDATE
              grease.source_file
            SET
              in_progress = FALSE,
              completed = FALSE,
              pick_up_time = null,
              completed_time = null
            WHERE
              id = %s
        """
        self._ioc.message().debug("SOURCE FILE FAILED SCHEDULING REVERSING FILE: [{0}]".format(source_file_id), True)
        self._conn.execute(sql, (source_file_id,))

    def _parse_source(self, sources, rule_set):
        # type: (dict, list) -> dict
        # lets parse the source
        # now lets get the data out of it
        # now lets loop through those results
        # first lets setup some state tracking stuff
        final_source_data = defaultdict()
        index = 0
        total_records = len(sources)
        for source in sources:
            self._ioc.message().debug(
                "PROCESSING OBJECT [{0}] OF [{1}] INTERNAL STRUCTURE: [{2}]".format(
                    str(index + 1),
                    str(total_records),
                    str(source)
                ),
                True
            )
            # first lets initialize all the source data into the object
            final_source_data[index] = source
            # now lets create our rule_processing key
            final_source_data[index]['rule_processing'] = defaultdict()
            # now lets loop through the rules we want to parse this source with
            for rule in rule_set:
                self._ioc.message().debug("PROCESSING RULE [{0}]".format(str(rule['name'])), True)
                # first lets make the rule processing result key
                final_source_data[index]['rule_processing'][rule['name']] = defaultdict()
                # next lets compute each rule in the rule processor
                # Yes another for loop but I promise this will be fast
                # look at some point we have to iterate over data
                for detector, detector_config in rule['logic'].iteritems():
                    # lets try to new up this detector
                    detector_instance = self._importer.load('tgt_grease_enterprise.Detectors', detector, True)
                    if isinstance(detector_instance, Detectors.BaseDetector):
                        self._ioc.message().debug(
                            "PROCESSING RULE [{0}] LOGICAL BLOCK [{1}]".format(str(rule['name']), str(detector)),
                            True
                        )
                        # we have a valid detector to parse with
                        # lets compute the source with the detector config
                        detector_instance.param_compute(source, detector_config)
                        # lets observe the result
                        result = detector_instance.get_result()
                        if result['result']:
                            # we passed the rule lets set that in the final source data
                            self._ioc.message().debug(
                                "PROCESSING RULE [{0}] LOGICAL BLOCK [{1}] PASSED".format(
                                    str(rule['name']),
                                    str(detector)
                                ),
                                True
                            )
                            final_source_data[index]['rule_processing'][rule['name']]['status'] = True
                            self._ioc.message().debug("RULE [{0}] PASSED THUS FAR".format(str(rule['name'])), True)
                            result.pop('result')
                            if 'parameters' not in final_source_data[index]['rule_processing'][rule['name']]:
                                final_source_data[index]['rule_processing'][rule['name']]['parameters'] = result
                            else:
                                final_source_data[index]['rule_processing'][rule['name']]['parameters'].update(result)
                            if 'constants' in rule:
                                final_source_data[index]['rule_processing'][rule['name']]['parameters']['constants'] = rule['constants']
                            # del out the instance
                            del detector_instance
                            # route on
                            continue
                        else:
                            # rule failed
                            final_source_data[index]['rule_processing'][rule['name']]['status'] = False
                            self._ioc.message().debug(
                                "PROCESSING RULE [{0}] LOGICAL BLOCK [{1}] FAILED :: SOURCE FAILS RULE SET".format(
                                    str(rule['name']),
                                    str(detector)
                                ),
                                True
                            )
                            # del out the instance
                            del detector_instance
                            # route on
                            break
                    else:
                        # we got an invalid detector and it couldn't be found
                        self._ioc.message().error("Invalid Detector: [" + str(detector) + "]")
                        del detector_instance
                        break
                # finally lets convert back to normal dict for the rule
                final_source_data[index]['rule_processing'][rule['name']] = dict(
                    final_source_data[index]['rule_processing'][rule['name']]
                )
            # now lets convert the rule_processing back to a normal array
            final_source_data[index]['rule_processing'] = dict(final_source_data[index]['rule_processing'])
            self._ioc.message().debug(
                "FINAL SOURCE RULE PROCESSING STRUCTURE: [{0}]".format(
                    str(final_source_data[index]['rule_processing'])
                ),
                True
            )
            self._ioc.message().debug(
                "PROCESSING OBJECT [{0}] OF [{1}] COMPLETE".format(
                    str(index + 1),
                    str(total_records)
                ),
                True
            )
            # finally increment our pointer
            index += 1
        # return final for usage elsewhere
        return final_source_data

    def _schedule_scheduling(self, sources, scanner):
        # type: (dict, str)  -> bool
        # first lets get applicable servers to run detectors
        # lets only get the least assigned server so we can round robin
        sql = """
            SELECT
              js.id,
              js.jobs_assigned
            FROM
              grease.job_servers js
            WHERE
              js.scheduler = TRUE AND 
              js.active is true
            ORDER BY 
              js.jobs_assigned
            LIMIT 1
        """
        server = self._conn.query(sql)
        if len(server) <= 0:
            self._ioc.message().error("Failed to get server to schedule Scheduling!::Dropping Scan")
            return False
        else:
            server = server[0]
        # Now lets insert the sources for the determined server to work
        sql = """
            INSERT INTO
              grease.scheduling_queue
            (source_data, job_server, scanner) 
            VALUES 
            (
              %s,
              %s,
              %s
            )
        """
        self._conn.execute(sql, (json.dumps(sources), server[0], scanner,))
        # finally lets ensure we account for the fact our server is going to do
        # that job and increment the assignment counter
        sql = """
            UPDATE
              grease.job_servers
            SET
              jobs_assigned = %s
            WHERE
              id = %s
        """
        self._conn.execute(sql, (int(server[1]) + 1, server[0],))
        self._ioc.message().debug(
            "DETECTION FOR SOURCE COMPLETE::SCHEDULED TO SERVER [{0}]".format(str(server[0])),
            True
        )
        return True
