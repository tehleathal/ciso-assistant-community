import pytest
from rest_framework.test import APIClient
from core.models import Framework
from core.models import RiskMatrix
from iam.models import Folder
from rest_framework import status

from test_vars import GROUPS_PERMISSIONS
from test_utils import EndpointTestsQueries, EndpointTestsUtils


@pytest.mark.django_db
class TestLibrariesUnauthenticated:
    """Perform tests on Libraries API endpoint without authentication"""

    client = APIClient()

    def test_get_libraries(self):
        """test to get libraries from the API without authentication"""

        EndpointTestsQueries.get_object(self.client, "Libraries")

    def test_import_frameworks(self):
        """test to import libraries with the API without authentication"""

        EndpointTestsQueries.import_object(self.client, "Framework")

    def test_delete_frameworks(self, authenticated_client):
        """test to delete libraries with the API without authentication"""

        EndpointTestsQueries.Auth.import_object(authenticated_client, "Framework")
        EndpointTestsQueries.delete_object(self.client, "Frameworks", Framework)

    def test_import_risk_matrix(self):
        """test to import libraries with the API without authentication"""

        EndpointTestsQueries.import_object(self.client, "Risk matrix")

    def test_delete_risk_matrix(self, authenticated_client):
        """test to delete libraries with the API without authentication"""

        EndpointTestsQueries.Auth.import_object(authenticated_client, "Risk matrix")
        EndpointTestsQueries.delete_object(self.client, "Risk matrices", RiskMatrix)


@pytest.mark.django_db
@pytest.mark.parametrize("test", GROUPS_PERMISSIONS.keys(), ids=[GROUPS_PERMISSIONS[key]["name"] for key in GROUPS_PERMISSIONS.keys()], indirect=True)
class TestLibrariesAuthenticated:
    """Perform tests on Libraries API endpoint with authentication"""

    def test_get_libraries(self, test):
        """test to get libraries from the API with authentication"""

        EndpointTestsQueries.Auth.get_object(
            test.client, "Libraries", base_count=-1, user_group=test.user_group
        )

    def test_import_frameworks(self, test):
        """test to import frameworks with the API with authentication"""


        # Uses the API endpoint to get library details with the admin client
        lib_detail_response = test.admin_client.get(
            EndpointTestsUtils.get_object_urn("Framework")
        ).json()["objects"]["framework"]

        # Asserts that the library is not already imported
        assert (
            Framework.objects.all().count() == 0
        ), "libraries are already imported in the database"
        EndpointTestsQueries.Auth.get_object(test.client, "Frameworks", user_group=test.user_group)

        EndpointTestsQueries.Auth.import_object(test.client, "Framework", user_group=test.user_group)

        expect = {"BI-UG-ADM": True, "BI-UG-GAD": False, "BI-UG-GVA": False, "BI-UG-DMA": False, 
            "BI-UG-ANA": False, "BI-UG-VAL": False, "BI-UG-AUD": False}

        assert (
            Framework.objects.all().count() == (1 if expect[test['user_group']] else 0)
        ), "frameworks are not correctly imported in the database"
        if expect[test['user_group']]:
            # Uses the API endpoint to assert that the library was properly imported
            EndpointTestsQueries.Auth.get_object(
                test.client,
                "Frameworks",
                test_params={
                    "name": lib_detail_response["name"],
                    "description": lib_detail_response["description"],
                    "urn": lib_detail_response["urn"],
                    "folder": {"str": Folder.get_root_folder().name},
                },
                base_count=1,
                user_group=test.user_group,
            )

    def test_delete_frameworks(self, test):
        """test to delete frameworks with the API with authentication"""

        EndpointTestsQueries.Auth.import_object(test.admin_client, "Framework")
        assert (
            Framework.objects.all().count() == 1
        ), "frameworks for deletion are not correctly imported in the database"
        expect = {"BI-UG-ADM": True, "BI-UG-GAD": False, "BI-UG-GVA": False, "BI-UG-DMA": False, 
            "BI-UG-ANA": False, "BI-UG-VAL": False, "BI-UG-AUD": False}
        should_work = expect[test['user_group']]
        if should_work: # this if should be removed, but it is not working as expected, todo
            EndpointTestsQueries.Auth.delete_object(
                test.client, "Frameworks", Framework, user_group=test.user_group, fails=not(should_work)
            )
        if not should_work: # remove object
            EndpointTestsQueries.Auth.delete_object(
                test.admin_client, "Frameworks", Framework
            )

    def test_import_risk_matrix(self, test):
        """test to import risk matrix with the API with authentication"""

        # Uses the API endpoint to get library details with the admin client
        lib_detail_response = test.admin_client.get(
            EndpointTestsUtils.get_object_urn("Risk matrix")
        ).json()["objects"]["risk_matrix"][0]

        # Asserts that the library is not already imported
        assert (
            RiskMatrix.objects.all().count() == 0
        ), "libraries are already imported in the database"
        EndpointTestsQueries.Auth.get_object(test.client, "Risk matrices", user_group=test.user_group)
        
        EndpointTestsQueries.Auth.import_object(test.client, "Risk matrix", user_group=test.user_group)

        # Uses the API endpoint to assert that the library was properly imported
        expect = {"BI-UG-ADM": True, "BI-UG-GAD": False, "BI-UG-GVA": False, "BI-UG-DMA": False, 
            "BI-UG-ANA": False, "BI-UG-VAL": False, "BI-UG-AUD": False}

        assert (
            RiskMatrix.objects.all().count() == (1 if expect[test['user_group']] else 0)
        ), "Risk matrices are not correctly imported in the database"
        if expect[test['user_group']]:
            EndpointTestsQueries.Auth.get_object(
                test.client,
                "Risk matrices",
                test_params={
                    "name": lib_detail_response["name"],
                    "description": lib_detail_response["description"],
                    "urn": lib_detail_response["urn"],
                    "folder": {"str": Folder.get_root_folder().name},
                    #                                 'json_definition': lib_detail_response  # TODO: restore this test
                },
                base_count=1,
                user_group=test.user_group,
            )

    def test_delete_matrix(self, test):
        """test to delete risk matrix with the API with authentication"""

        EndpointTestsQueries.Auth.import_object(test.admin_client, "Risk matrix")
        expect = {"BI-UG-ADM": True, "BI-UG-GAD": False, "BI-UG-GVA": False, "BI-UG-DMA": False, 
            "BI-UG-ANA": False, "BI-UG-VAL": False, "BI-UG-AUD": False}
        should_work = expect[test['user_group']]
        if should_work: # this if should be removed, but it is not working as expected, todo
            EndpointTestsQueries.Auth.delete_object(
                test.client, "Risk matrices", RiskMatrix, user_group=test.user_group,  fails=not(should_work)
            )
        if not should_work: # remove object
            EndpointTestsQueries.Auth.delete_object(
                test.admin_client, "Risk matrices", RiskMatrix
            )
 