from dflow.python import PythonOPTemplate
from dflow import (
    Workflow,
    Step,
    argo_range,
    SlurmRemoteExecutor,
    upload_artifact,
    download_artifact,
    InputArtifact,
    OutputArtifact,
    ShellOPTemplate
)

import dflow

import time
from dflow import config, s3_config
from dflow.plugins import bohrium
from dflow.plugins.bohrium import TiefblueClient
from DPMaterial.property.LAMMPS_OP import den_Cal
import json


# def config_argo(**machine):
#     # upload_packages.append(faraday_path)
#     #print(config)
#     if dflow.config["mode"] == "debug": return
#     if config.get("dflow_config"):
#         for k, v in config["dflow_config"].items():
#             dflow.config[k] = v
#     if config.get("bohrium_config"):
#         #print(bohrium)
#         if "username" in config["bohrium_config"]:
#             bohrium.config["username"] = config["bohrium_config"].pop("username")
#         # 将外层获取的 ticket 设置到 dflow.plugins.bohrium.config 中
#         if "ticket" in config["bohrium_config"] :
#             print("config bohrium config ticket set"
#             #, config["bohrium_config"]
#             )
#             bohrium.config["ticket"] = config["bohrium_config"].pop("ticket")
#         if "password" in config["bohrium_config"] :
#             print("config bohrium config password set")
#             bohrium.config["password"] = config["bohrium_config"].pop("password")
#         if ("ticket" in config["bohrium_config"]
#            and "password" in config["bohrium_config"]):
#             print("Warning: both bohrium ticket and password exists")
#         for k, v in config["bohrium_config"].items():
#             print("config bohrium config k", k, "v", v)
#             bohrium.config[k] = v
#     if config.get("dflow_s3_config"):
#         for k, v in config["dflow_s3_config"].items():
#             dflow.s3_config[k] = v
#     else:
#         # default bohrium s3_config
#         dflow.s3_config["repo_key"] = "oss-bohrium"
#     if dflow.s3_config["repo_key"] == "oss-bohrium":
#         dflow.s3_config["storage_client"] = TiefblueClient()


def density(location,dispatcher_executor):
    config["host"] = "https://workflows.deepmodeling.com"
    config["k8s_api_server"] = "https://workflows.deepmodeling.com"
    bohrium.config["username"] = "zhanglinshuang@dp.tech"
    bohrium.config["password"] = "lszhang@dp1031"
    bohrium.config["project_id"] = "11052"
    s3_config["repo_key"] = "oss-bohrium"
    s3_config["storage_client"] = TiefblueClient()

    den_Calculation = Step(
        "density-DPMD",
        PythonOPTemplate(den_Cal, image="registry.dp.tech/dptech/deepmd-kit:2.2.1-cuda11.6"),
        artifacts={"input": upload_artifact(location)},
        executor=dispatcher_executor,
    )
    wf = Workflow("density-task")
    wf.add(den_Calculation)
    wf.submit()
    while wf.query_status() in  [ "Pending", "Running"   ]:
        time.sleep(1)
    assert(wf.query_status() == "Succeeded")

    step = wf.query_step(name="density-DPMD")[0]
    assert(step.phase == "Succeeded")
    download_artifact(step.outputs.artifacts["output"])
    return wf


