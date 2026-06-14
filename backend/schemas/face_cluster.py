from pydantic import BaseModel


class ClusterLabelUpdate(
    BaseModel
):
    label: str