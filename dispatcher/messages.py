import base64
import io
import json
import urllib.parse
from filtering import process_selector

import requests

from settings import API_URL, TOKEN, VERIFY_CERTIFICATE

from loguru import logger


class MessageRegistry:
    REGISTRY = {}

    def add(self, message):
        self.REGISTRY[message.__name__] = message


message_registry = MessageRegistry()


def get_resource_endpoint(message: dict, resource_endpoint: str | None = None) -> str:
    """
    Determines the resource endpoint from either the function parameter or the message.
    """
    if resource_endpoint is None:
        resource_endpoint = message.get("resource")
        if resource_endpoint is None:
            raise Exception(
                "No resource endpoint provided. Provide via function parameter or message 'resource' key."
            )
    return resource_endpoint


def extract_update_data(message: dict) -> tuple[dict, dict]:
    """
    Extracts and validates the selector and update values from the message.
    Returns a tuple of (selector, values).
    """
    selector = message.get("selector", {})
    values = message.get("values", {})

    if not values:
        raise Exception("No update values provided in the message.")

    if not selector:
        raise Exception("No selector provided.")

    return selector, values


def get_object_ids(
    selector: dict,
    resource_endpoint: str,
    selector_mapping: dict[str, str] | None = None,
) -> list:
    """
    Uses the selector to query the API and return a list of object IDs.
    """
    if selector_mapping is None:
        selector_mapping = {}

    search_endpoint = f"{API_URL}/{resource_endpoint}/"
    result = process_selector(
        selector,
        selector_mapping=selector_mapping,
        endpoint=search_endpoint,
        token=str(TOKEN),
        verify_certificate=VERIFY_CERTIFICATE,
    )

    if isinstance(result, list):
        return result
    else:
        return [result]


def update_single_object(resource_endpoint: str, obj_id: str, values: dict) -> dict:
    """
    Updates a single object using a PATCH request and returns the updated object.
    """
    patch_url = f"{API_URL}/{resource_endpoint}/{obj_id}/"
    data = json.dumps(values)

    logger.debug(f"Updating {resource_endpoint} {obj_id}", values=values)

    res = requests.patch(
        patch_url,
        data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Token {TOKEN}",
        },
        verify=VERIFY_CERTIFICATE,
    )

    if res.status_code not in [200, 204]:
        logger.exception(
            f"Failed to update {resource_endpoint} {obj_id}: {res.status_code}",
            response=res.text,
        )
        raise Exception(
            f"Failed to update {resource_endpoint} {obj_id}: {res.status_code}, {res.text}"
        )

    logger.success(
        f"Successfully updated object {obj_id}",
        resource=resource_endpoint,
        response=res.json() if res.text else {"id": obj_id, **values},
    )
    # Return JSON response if available, else construct a dict with the provided values.
    return res.json() if res.text else {"id": obj_id, **values}


def update_objects(
    message: dict,
    resource_endpoint: str | None = None,
    selector_mapping: dict[str, str] | None = None,
) -> list:
    """
    Generic function to update an object.

    Args:
        message (dict): The update message which must include:
            - "values" (dict): The fields and values to update.
            - "selector" (dict): A dictionary of key/value pairs to select object(s).
            - Optionally, "resource": the resource endpoint (e.g. "applied-controls")
              if not provided via the function parameter.
        resource_endpoint (str, optional): The API resource endpoint (e.g., "applied-controls").
            If not provided, the function will look for a "resource" key in the message.
        selector_mapping (dict, optional): Mapping rules for selectors if needed.

    Returns:
        list: A list containing the responses for the updated objects.

    Raises:
        Exception: If no selector is provided, or if the update fails.
    """
    if selector_mapping is None:
        selector_mapping = {}

    # Determine resource endpoint
    resource_endpoint = get_resource_endpoint(message, resource_endpoint)

    # Extract update data (selector and values)
    selector, values = extract_update_data(message)

    # Retrieve object IDs to update using the selector
    object_ids = get_object_ids(selector, resource_endpoint, selector_mapping)

    updated_objects = []

    logger.info("Updating objects", resource=resource_endpoint, ids=object_ids)

    # Process each update
    for obj_id in object_ids:
        updated_obj = update_single_object(resource_endpoint, obj_id, values)
        updated_objects.append(updated_obj)

    logger.success(
        "Successfully updated objects", resource=resource_endpoint, ids=object_ids
    )

    return updated_objects


def update_applied_control(message: dict):
    return update_objects(message, "applied-controls")


def update_requirement_assessment(message: dict):
    return update_objects(message, "requirement-assessments")


def upload_attachment(message: dict):
    selector = message.get("selector", {})
    values = message.get("values", {})

    file_name = values.get("file_name")
    if not file_name:
        logger.exception("No file_name provided")
        raise Exception("No file_name provided")

    file_content_b64 = values.get("file_content")
    if not file_content_b64:
        logger.exception("No file_content provided")
        raise Exception("No file_content provided")

    file_content = base64.b64decode(file_content_b64)
    in_memory_file = io.BytesIO(file_content)
    file_upload_headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Disposition": f"attachment; filename={urllib.parse.quote(file_name)}",
    }

    applied_controls_selector: list[dict] = values.get("applied_controls", [])

    evidences_endpoint = f"{API_URL}/evidences/"

    if selector:
        logger.info("Using provided selector to find evidence", selector=selector)
        selector["target"] = "single"
        evidence_id = get_object_ids(selector, "evidences")[0]
        logger.info("Found evidence", evidence_id=evidence_id)
        if not evidence_id:
            logger.exception(
                "No evidence found for the provided selector.", selector=selector
            )
            raise Exception("No evidence found for the provided selector.")
    else:
        logger.info("Creating new evidence with name: {}", file_name, values=values)
        response = requests.post(
            evidences_endpoint,
            data={"name": values.get("name", file_name)},
            headers={"Authorization": f"Token {TOKEN}"},
            verify=VERIFY_CERTIFICATE,
        )
        if not response.ok:
            logger.exception(
                "Failed to create evidence",
                status_code=response.status_code,
                response=response.text,
            )
            raise Exception(
                f"Failed to create evidence: {response.status_code}, {response.text}"
            )
        data = response.json()
        evidence_id = data["id"]
        logger.info("Created evidence", evidence_id=evidence_id, evidence=data)

    logger.info("Uploading attachment to evidence", evidence_id=evidence_id)
    upload_response = requests.post(
        f"{evidences_endpoint}{evidence_id}/upload/",
        headers=file_upload_headers,
        data=in_memory_file,
        verify=VERIFY_CERTIFICATE,
    )
    if upload_response.status_code not in [200, 204]:
        logger.exception(
            "Failed to upload attachment to evidence",
            evidence_id=evidence_id,
            status_code=upload_response.status_code,
            response=upload_response.text,
        )
        raise Exception(
            f"Failed to update evidence {evidence_id}: {upload_response.status_code}, {upload_response.text}"
        )
    logger.success(
        "Uploaded attachment to evidence", evidence_id=evidence_id, file_name=file_name
    )

    if applied_controls_selector:
        logger.info(
            "Updating applied controls with evidence",
            selector=applied_controls_selector,
        )
        applied_controls = get_object_ids(applied_controls_selector, "applied-controls")
        logger.info("Found applied controls", applied_controls=applied_controls)
        if not applied_controls:
            logger.exception(
                "No applied controls found for the provided selector.",
                selector=applied_controls_selector,
            )
            raise Exception("No applied controls found for the provided selector.")
        for control in applied_controls:
            logger.debug("Fetching applied control", control=control)
            control_endpoint = f"{API_URL}/applied-controls/{control}/"
            get_response = requests.get(
                control_endpoint, headers={"Authorization": f"Token {TOKEN}"}
            )
            control_data = get_response.json()
            logger.debug("Got applied control", control=control, data=control_data)
            evidences = control_data.get("evidences", [])
            logger.info(
                "Attaching evidence to applied control",
                control=control_data,
                evidence=evidence_id,
            )
            update_response = requests.patch(
                control_endpoint,
                json={"evidences": evidences + [evidence_id]},
                headers={"Authorization": f"Token {TOKEN}"},
            )
            if not update_response.ok:
                logger.exception(
                    "Failed to update applied control",
                    control=control,
                    response=update_response.text,
                )
                raise Exception(
                    f"Failed to update applied control {control}: {update_response.status_code}, {update_response.text}"
                )
            logger.success(
                "Updated applied control",
                control=control,
                response=update_response.json(),
            )
        logger.success(
            "Successfully updated applied controls with evidence",
            applied_controls=applied_controls,
            evidence=evidence_id,
            file_name=file_name,
        )


message_registry.add(update_applied_control)
message_registry.add(update_requirement_assessment)
message_registry.add(upload_attachment)
