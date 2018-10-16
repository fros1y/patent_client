import os
from tempfile import TemporaryDirectory

import pytest

from ip.uspto_assignments import Assignment

class TestAssignment:
    def test_fetch_assignments_by_assignee(self):
        assignments = Assignment.objects.lookup(assignee="US Well Services")
        assert len(assignments) >= 22
        assert assignments[5].pat_assignor_name_first == "OEHRING, JARED"
        assignments = Assignment.objects.lookup(assignee="LogicBlox")
        assert len(assignments) >= 9

    def test_fetch_assignments_by_patent(self):
        assignments = Assignment.objects.lookup(patent="8,789,601")
        assert len(assignments) >= 1

    def test_fetch_assignments_by_application(self):
        assignments = Assignment.objects.lookup(application="14/190,982")
        assert len(assignments) >= 1

    def test_fetch_assignee_with_greater_than_500_assignments(self):
        assignments = Assignment.objects.lookup(assignee="Borealis")
        assert len(assignments) >= 1268

    def test_get_assignment_image(self):
        assignments = Assignment.objects.lookup(patent=6095661)
        assignment = assignments[0]
        assert (
            assignment.image_url
            == "http://legacy-assignments.uspto.gov/assignments/assignment-pat-038505-0128.pdf"
        )

    def test_slice_assignments(self):
        assignments = Assignment.objects.lookup(assignee="US Well Services")
        assignment_list1 = [assignment.display_id for assignment in assignments[0:5]]
        assert len(assignment_list1) == 5

        assignment_list2 = [assignment.display_id for assignment in assignments[:5]]
        assert len(assignment_list2) == 5

        assignment_list3 = [assignment.display_id for assignment in assignments[-5:]]
        assert len(assignment_list3) == 5

    def test_iterate_assignments(self):
        assignments = Assignment.objects.lookup(assignee="US Well Services")
        assignment_list = [assignment.display_id for assignment in assignments]
        assert len(assignment_list) == len(assignments)
    
    def test_get_aggregates(self):
        assignments = Assignment.objects.lookup(assignee='Covar Applied')
        assert list(assignments.aggregate('appl_num')) == ['15274746', '15251940', '15251994', '15252319', '14938523', '14938467', '14938962', '14939089', '14284013', '14284013']
        assert list(assignments.aggregate('pat_num')) == ['9908148', '9708898', '9708898']
        assert list(assignments.aggregate('publ_num')) == ['20170081931', '20170058620', '20170056928', '20170056929', '20160130917', '20160134843', '20160130928', '20160130889', '20140345940', '20140345940']
        #assert list(assignments.pct_applications) == []
        assert list(assignments.aggregate('pat_assignee_name', unique=True)) == ['COVAR APPLIED TECHNOLOGIES, INC.']
        #assert list(assignments.aggregate('pat_assignor_name')) == False
        #assert False